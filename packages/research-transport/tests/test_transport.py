"""Spool and consumer behavior with a stand-in crypto domain (unit tests; the E2E uses the real domain)."""

from __future__ import annotations

import copy
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest
from research_protocol import v2
from research_transport import adapters, cli
from research_transport.consumer import Consumer, ConsumerBusy, domain_lock
from research_transport.faults import ENV, EXIT_CODE
from research_transport.spool import Spool, SpoolConflict

REQUEST = {
    "schema_version": "crypto-research-request/1",
    "request_id": "crypto:REQ-T-0001",
    "request_type": "BACKTEST_EXISTING_HYPOTHESIS",
    "research_id": "crypto:RESEARCH-T",
    "hypothesis_id": "crypto:QUAL-T",
    "references": {
        k: {"name": "ref-" + k.replace("_", "-"), "version": "v1"}
        for k in ("protocol", "dataset", "baseline", "cost_model", "evidence")
    },
    "data_cutoff": "2026-08-31T00:00:00Z",
    "parameters": {
        "symbol": "BTCUSDT",
        "horizon_days": 7,
        "max_observations": 100,
        "fee_bps": 10,
        "slippage_bps": 5,
    },
    "priority_hint": "NORMAL",
}


def task_for(request=REQUEST, episode=1, previous=None, domain="crypto"):
    return v2.build_task(
        domain,
        copy.deepcopy(request),
        episode_id=v2.episode_id_for(domain, episode),
        proposal_id="cain:P-1",
        created_at="2026-09-27T00:00:00Z",
        previous_task_id=previous,
    )


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


class FakeCryptoDomain:
    """Minimal stand-in for Circuit: idempotent by request_id, optional scripted statuses."""

    DOMAIN = "crypto"

    def __init__(self, script=()):
        self.script = list(script)
        self.results = {}
        self.calls = []
        self.show_tamper = False
        self.bytes_tamper = False

    def identity(self):
        return {"distribution": "cripto-predictor", "version": "test", "module": "tests.fake"}

    def _result(self, request):
        return {
            "schema_version": "crypto-research-result/1",
            "result_id": "crypto:RESULT-" + sha(request["request_id"].encode())[:32],
            "request_id": request["request_id"],
            "admission_id": "crypto:ADM-" + "b" * 32,
            "experiment_id": "crypto:EXP-" + "c" * 32,
            "research_id": request["research_id"],
            "hypothesis_id": request["hypothesis_id"],
            "result_state": "NO_EDGE",
            "operational_state": "SUCCEEDED",
            "scientific_state": "INCONCLUSIVE",
            "economic_state": "NO_EDGE",
            "capital_permission": False,
            "produced_at": "2026-09-27T00:00:01Z",
            "core_facts": {"ci": [-0.25, 0.1 + 0.2]},
            "ops_facts": {"retry_count": 0},
            "domain_facts": {"texto": "ção"},
            "provenance": {"x": 1},
        }

    def submit_task(self, task, config):
        raw = v2.canonical(task["payload"]) if not self.bytes_tamper else b"{}"
        request = json.loads(raw) if not self.bytes_tamper else task["payload"]
        self.calls.append(task["task_id"])
        out = {
            "schema": "crypto-research-outcome/1",
            "submission_sha256": sha(raw),
            "request_id": request["request_id"],
            "client_ref": request["client_ref"],
        }
        status = self.script.pop(0) if self.script else None
        if status == "OPS_FAILED_RETRYABLE":
            return out | {"status": status, "exit_code": 3, "reason": "OPS_FAILED"}
        duplicate = request["request_id"] in self.results
        result = self.results.setdefault(request["request_id"], self._result(request))
        return out | {"status": "DUPLICATE" if duplicate else "RESULT", "exit_code": 0, "result": result}

    def reread(self, request_id, config):
        result = self.results[request_id]
        digest = sha(v2.domain_canonical(result)) if not self.show_tamper else "0" * 64
        return 0, {"status": "RESULT", "result_sha256": digest, "result": result}


@pytest.fixture
def env(tmp_path):
    domain = FakeCryptoDomain()
    spool = Spool(tmp_path / "spool")
    consumer = Consumer("crypto", spool, tmp_path / "ledger.sqlite", domain, {"state": "s"})
    return SimpleNamespace(domain=domain, spool=spool, consumer=consumer, tmp=tmp_path)


def test_put_task_is_write_once_and_idempotent(env):
    raw = v2.dumps_task(task_for())
    assert env.spool.put_task("crypto", raw)["status"] == "WRITTEN"
    assert env.spool.put_task("crypto", raw)["status"] == "EXISTS"
    target = env.spool.task_files("crypto")[0]
    target.write_bytes(b"tampered")
    with pytest.raises(SpoolConflict):
        env.spool.put_task("crypto", raw)
    assert target.read_bytes() == b"tampered"


def test_put_task_refuses_other_domain_and_non_canonical(env):
    raw = v2.dumps_task(task_for())
    with pytest.raises(v2.V2Error, match="DOMAIN_MISMATCH"):
        env.spool.put_task("stocks", raw)
    with pytest.raises(v2.V2Error, match="NON_CANONICAL"):
        env.spool.put_task("crypto", json.dumps(json.loads(raw), indent=1).encode())
    assert env.spool.task_files("crypto") == []


def test_task_is_delivered_once_and_result_is_byte_identical(env):
    task = task_for()
    env.spool.put_task("crypto", v2.dumps_task(task))
    first = env.consumer.run_once()
    assert [r["action"] for r in first] == ["delivered"] and first[0]["status"] == "RESULT"
    second = env.consumer.run_once()
    assert second[0]["action"] == "skipped" and env.domain.calls == [task["task_id"]]
    (result_file,) = env.spool.result_files("crypto")
    result = v2.loads_result(result_file.read_bytes(), task=task)
    assert result["result"]["payload_canonical"].encode() == v2.domain_canonical(
        env.domain.results[task["request_id"]]
    )
    assert result["client_ref"] == task["payload"]["client_ref"]
    assert result["adapter"]["distribution"] == "cripto-predictor"


def test_interrupted_delivery_is_resent_and_the_domain_answers_duplicate(env):
    task = task_for()
    env.spool.put_task("crypto", v2.dumps_task(task))
    env.consumer.run_once()
    with env.consumer._db() as db:
        db.execute("UPDATE deliveries SET state='IN_PROGRESS'")
    report = env.consumer.run_once()
    assert report[0]["status"] == "DUPLICATE"
    results = [v2.loads_result(p.read_bytes(), task=task) for p in env.spool.result_files("crypto")]
    assert {r["outcome"]["status"] for r in results} == {"RESULT", "DUPLICATE"}
    assert len({r["result"]["payload_sha256"] for r in results}) == 1
    assert len(env.domain.results) == 1


def test_retryable_waits_for_a_resend_requested_by_the_cain(env):
    env.domain.script = ["OPS_FAILED_RETRYABLE"]
    task = task_for()
    env.spool.put_task("crypto", v2.dumps_task(task))
    assert env.consumer.run_once()[0]["class"] == "RETRYABLE"
    assert env.consumer.run_once()[0]["action"] == "skipped"
    env.spool.request_retry("crypto", task["task_id"], 1)
    assert env.consumer.run_once()[0]["status"] == "RESULT"
    assert env.consumer.run_once()[0]["action"] == "skipped"
    assert len(env.domain.calls) == 2


def test_invalid_foreign_or_misnamed_task_files_are_rejected_without_calling_the_domain(env):
    tasks_dir = env.spool.root / "crypto" / "tasks"
    tasks_dir.mkdir(parents=True)
    stocks = v2.build_task(
        "stocks",
        {
            "schema_version": "stocks-research-request/1",
            "request_id": "stocks:REQ-1",
            "request_type": "BACKTEST_PIT_FACTOR",
            "research_id": "stocks:R",
            "hypothesis_id": "stocks:H9",
            "references": {
                k: {"name": "x", "version": "v1"}
                for k in ("dataset", "universe", "features", "model", "baseline", "cost_model", "readiness")
            },
            "as_of": "2026-09-24T03:00:00Z",
            "pit": {
                "availability_rule": "AVAILABLE_AT_LE_DECISION_TIME",
                "minimum_pit_class": "PIT_RECONSTRUCTED",
            },
            "parameters": {
                "target": "NEXT_REBALANCE_RETURN",
                "fee_bps": 10,
                "slippage_bps": 5,
                "max_securities": 50,
                "external_intelligence": {"mode": "NONE", "families": []},
            },
            "priority_hint": "NORMAL",
        },
        episode_id="stocks:episode-1",
        proposal_id="cain:P",
        created_at="2026-09-27T00:00:00Z",
    )
    crypto = task_for()
    (tasks_dir / ("TASK-" + stocks["task_id"].split("TASK-")[1] + ".json")).write_bytes(v2.dumps_task(stocks))
    (tasks_dir / ("TASK-" + "0" * 32 + ".json")).write_bytes(v2.dumps_task(crypto))
    wrong_version = json.loads(v2.dumps_task(crypto)) | {"schema": "research-task/3"}
    (tasks_dir / "v3.json").write_bytes(v2.canonical(wrong_version))
    report = env.consumer.run_once()
    assert sorted(r.get("code") for r in report) == [
        "DOMAIN_MISMATCH",
        "NAME_MISMATCH",
        "VERSION_UNSUPPORTED",
    ]
    assert env.domain.calls == [] and len(env.spool.rejection_files("crypto")) == 3
    assert all(r["action"] == "skipped" for r in env.consumer.run_once())


def test_domain_that_did_not_receive_request_bytes_is_held(env):
    env.domain.bytes_tamper = True
    env.spool.put_task("crypto", v2.dumps_task(task_for()))
    report = env.consumer.run_once()
    assert report[0]["action"] == "held" and report[0]["code"] == "ADAPTER_BYTES_MISMATCH"
    assert env.spool.result_files("crypto") == []
    assert env.consumer.run_once()[0]["action"] == "skipped"


def test_payload_not_identical_to_authoritative_reread_is_held(env):
    env.domain.show_tamper = True
    env.spool.put_task("crypto", v2.dumps_task(task_for()))
    report = env.consumer.run_once()
    assert report[0]["code"] == "BYTE_IDENTITY_MISMATCH" and env.spool.result_files("crypto") == []


def test_tasks_are_delivered_in_episode_order(env):
    first = task_for()
    second = task_for(REQUEST | {"request_id": "crypto:REQ-T-0002"}, episode=2, previous=first["task_id"])
    env.spool.put_task("crypto", v2.dumps_task(second))
    env.spool.put_task("crypto", v2.dumps_task(first))
    env.consumer.run_once()
    assert env.domain.calls == [first["task_id"], second["task_id"]]


def test_one_consumer_per_domain_at_a_time(env):
    # Stage B dispute tests (IC-F016, IC-F017, IS-F009): a second consumer of a domain never reaches it
    env.spool.put_task("crypto", v2.dumps_task(task_for()))
    other = Consumer("crypto", env.spool, env.tmp / "other-ledger.sqlite", env.domain, {"state": "s"})
    with domain_lock(env.spool, "crypto"):
        with pytest.raises(ConsumerBusy):
            other.run_once()
        with pytest.raises(ConsumerBusy):
            env.consumer.run_once()
    assert env.domain.calls == [] and not list((env.spool.root / "crypto" / "results").glob("*.json"))
    with other._db() as db:
        assert db.execute("SELECT count(*) FROM deliveries").fetchone()[0] == 0
    # released: the next pass delivers once
    assert [line["action"] for line in env.consumer.run_once()] == ["delivered"]
    assert [line["action"] for line in other.run_once()] == ["delivered"]  # its own ledger: the domain dedups
    assert env.domain.calls == [task_for()["task_id"]] * 2


def test_cli_reports_busy_and_publishes_nothing(tmp_path, capfd, monkeypatch):
    domain = FakeCryptoDomain()
    monkeypatch.setattr(cli, "load", lambda name: domain)
    spool = Spool(tmp_path / "spool")
    spool.put_task("crypto", v2.dumps_task(task_for()))
    argv = [
        "--domain",
        "crypto",
        "--spool",
        str(tmp_path / "spool"),
        "--ledger",
        str(tmp_path / "l.sqlite"),
        "--state",
        str(tmp_path),
        "--policy",
        str(tmp_path),
        "--objects",
        str(tmp_path),
    ]
    with domain_lock(spool, "crypto"):
        code = cli.main(argv)
    out, _err = capfd.readouterr()
    assert code == 6 and [json.loads(line) for line in out.splitlines()] == [
        {"action": "busy", "code": "CONSUMER_BUSY", "domain": "crypto"}
    ]
    assert domain.calls == [] and not list((tmp_path / "spool" / "crypto" / "results").glob("*.json"))
    assert cli.main(argv) == 0 and domain.calls == [task_for()["task_id"]]


def test_two_consumer_processes_on_the_same_task_deliver_once(tmp_path):
    script = tmp_path / "slow_consumer.py"
    script.write_text(
        "import json, sys, time\n"
        f"sys.path.insert(0, {str(Path(__file__).parent)!r})\n"
        "from test_transport import FakeCryptoDomain\n"
        "from research_transport.consumer import Consumer, ConsumerBusy\n"
        "from research_transport.spool import Spool\n"
        "class Slow(FakeCryptoDomain):\n"
        "    def submit_task(self, task, config):\n"
        "        time.sleep(1.5)\n"
        "        return super().submit_task(task, config)\n"
        "consumer = Consumer('crypto', Spool(sys.argv[1]), sys.argv[2], Slow(), {'state': 's'})\n"
        "try:\n"
        "    print(json.dumps([line['action'] for line in consumer.run_once()]))\n"
        "except ConsumerBusy:\n"
        "    print(json.dumps('busy'))\n",
        encoding="utf-8",
    )
    Spool(tmp_path / "spool").put_task("crypto", v2.dumps_task(task_for()))
    argv = [sys.executable, str(script), str(tmp_path / "spool"), str(tmp_path / "ledger.sqlite")]
    procs = [subprocess.Popen(argv, stdout=subprocess.PIPE, text=True) for _ in range(2)]
    outs = sorted(json.dumps(json.loads(p.communicate(timeout=60)[0])) for p in procs)
    assert outs == ['"busy"', '["delivered"]']
    assert len(list((tmp_path / "spool" / "crypto" / "results").glob("*.json"))) == 1


def test_the_lock_of_a_consumer_that_died_is_released_and_its_task_resumed(env):
    # the holder dies mid-delivery (fault point, os._exit 86): the OS releases the lock, the next pass resumes
    # the interrupted task through the adapter_api (SPEC V2 section 7)
    env.spool.put_task("crypto", v2.dumps_task(task_for()))
    code = (
        "import sys\n"
        f"sys.path.insert(0, {str(Path(__file__).parent)!r})\n"
        "from test_transport import FakeCryptoDomain\n"
        "from research_transport.consumer import Consumer\n"
        "from research_transport.spool import Spool\n"
        "Consumer('crypto', Spool(sys.argv[1]), sys.argv[2], FakeCryptoDomain(), {'state': 's'}).run_once()\n"
    )
    done = subprocess.run(
        [sys.executable, "-c", code, str(env.spool.root), str(env.tmp / "ledger.sqlite")],
        env=os.environ | {ENV: "after_domain_before_result_write"},
        capture_output=True,
        text=True,
    )
    assert done.returncode == EXIT_CODE
    lines = env.consumer.run_once()
    assert [line["action"] for line in lines] == ["delivered"] and lines[0]["attempt"] == 2


def test_fault_point_kills_the_process_with_86():
    code = "from research_transport.faults import fault; fault('before_domain'); print('alive')"
    done = subprocess.run(
        [sys.executable, "-c", code], env=os.environ | {ENV: "before_domain"}, capture_output=True, text=True
    )
    assert done.returncode == EXIT_CODE and "alive" not in done.stdout
    assert subprocess.run([sys.executable, "-c", code], capture_output=True, text=True).returncode == 0


def test_only_allowlisted_adapters_load():
    with pytest.raises(adapters.AdapterUnavailable):
        adapters.load("stocks")
    with pytest.raises(adapters.AdapterUnavailable):
        adapters.load("crypto")  # the domain is not installed in this package's own test environment
    assert dict(adapters.ADAPTERS["crypto"]) == {
        "distribution": "cripto-predictor",
        "module": "GarimpoInvestimentos.adapters.research_v2",
    }


def test_stocks_adapter_is_registered_by_module_name_only():
    assert set(adapters.ADAPTERS) == {"crypto", "stocks", "brasileirao"}
    assert dict(adapters.ADAPTERS["stocks"]) == {
        "distribution": "stocks-predictor",
        "module": "stocks_predictor.adapters.research_v2",
    }
    with pytest.raises(adapters.AdapterUnavailable, match="no adapter registered"):
        adapters.load("not-a-domain")  # an unregistered domain has no consumer
    with pytest.raises(adapters.AdapterUnavailable, match="not importable"):
        adapters.load("stocks")  # the domain is not installed in this package's own test environment


def test_brasileirao_adapter_is_registered_by_module_name_only():
    assert dict(adapters.ADAPTERS["brasileirao"]) == {
        "distribution": "brasileirao-predictor",
        "module": "brasileirao_predictor.adapters.research_v2",
    }
    with pytest.raises(adapters.AdapterUnavailable, match="not importable"):
        adapters.load("brasileirao")  # the domain is not installed in this package's own test environment


def test_cli_refuses_a_domain_without_adapter(tmp_path, capsys):
    code = cli.main(
        [
            "--domain",
            "brasileirao",
            "--spool",
            str(tmp_path),
            "--ledger",
            str(tmp_path / "l"),
            "--state",
            str(tmp_path),
            "--policy",
            str(tmp_path),
            "--objects",
            str(tmp_path),
        ]
    )
    assert code == 1 and "ADAPTER_UNAVAILABLE" in capsys.readouterr().err


def test_cli_stdout_carries_only_the_report_lines(tmp_path, capfd, monkeypatch):
    import logging

    class Noisy(FakeCryptoDomain):
        def submit_task(self, task, config):
            print("domain print to stdout")
            handler = logging.StreamHandler(sys.stdout)
            logging.getLogger("noisy-domain").addHandler(handler)
            logging.getLogger("noisy-domain").warning('{"event": "job_finished"}')
            logging.getLogger("noisy-domain").removeHandler(handler)
            os.system("echo child process stdout")
            return super().submit_task(task, config)

    monkeypatch.setattr(cli, "load", lambda domain: Noisy())
    Spool(tmp_path / "spool").put_task("crypto", v2.dumps_task(task_for()))
    spool, ledger = str(tmp_path / "spool"), str(tmp_path / "l.sqlite")
    code = cli.main(
        [
            "--domain",
            "crypto",
            "--spool",
            spool,
            "--ledger",
            ledger,
            "--state",
            str(tmp_path),
            "--policy",
            str(tmp_path),
            "--objects",
            str(tmp_path),
        ]
    )
    out, err = capfd.readouterr()
    assert code == 0
    lines = out.splitlines()
    assert len(lines) == 1 and json.loads(lines[0])["status"] == "RESULT"
    assert "domain print to stdout" in err and "job_finished" in err and "child process stdout" in err
    print("after main, stdout works again")
    assert capfd.readouterr().out.strip() == "after main, stdout works again"
