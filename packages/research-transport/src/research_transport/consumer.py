"""Per-domain consumer: spool task → domain adapter (adapter_api) → ResearchResultV2 back to the spool.

For each task file of its domain, in episode order, the consumer:
  1. parses it fail-closed (``loads_task``: canonical bytes, schema, IDs, hashes); the file name must be the
     task's own name and the task must belong to this consumer's domain; anything else is rejected and
     recorded, never executed;
  2. decides from its delivery ledger whether the task needs the domain: new, interrupted (``IN_PROGRESS``
     after a crash, SPEC V2 §7: the same task is sent again through the adapter_api), or ``RETRYABLE`` with a
     resend requested by the CAIN; terminal tasks are never sent again;
  3. calls the adapter, checks that the domain received exactly ``request_bytes(task)``
     (``submission_sha256``), wraps the outcome with the normative ``build_result`` of the frozen protocol,
     and for RESULT/DUPLICATE checks that the payload is byte-identical to the domain's authoritative re-read
     (``payload_sha256 == show().result_sha256``);
  4. publishes the result file and records the outcome class.

The consumer never chooses a handler, a budget, a priority or capital, and never interprets the domain's
states.

One consumer per domain at a time: ``run_once`` holds an exclusive, non-blocking lock of the domain's
spool directory (``<spool>/<domain>/.consumer.lock``; ``flock`` on POSIX, ``msvcrt.locking`` on Windows)
for the whole pass. A second consumer of the same domain raises ``ConsumerBusy`` before reading the ledger
or calling the adapter, so it publishes nothing and changes nothing. Before, two consumers on the same task
both reached the domain: the loser published a false ``OPS_FAILED_RETRYABLE`` (the Ops lock it lost) or a
false ``RECONCILIATION_REQUIRED`` (the domain materializes references before the Ops lock), and on Windows
it could die on a read-only file (Stage B dispute tests, 2026-09-28: IC-F016, IC-F017, IS-F009). The lock
is released when the pass ends or the process dies.
"""

from __future__ import annotations

import os
import sqlite3
from contextlib import contextmanager
from datetime import UTC, datetime
from pathlib import Path
from types import ModuleType

from research_protocol import v2

from research_transport import faults
from research_transport.spool import Spool, SpoolConflict, sha256, task_file_name

STATES = ("IN_PROGRESS", "TERMINAL_RESULT", "TERMINAL_REFUSAL", "RETRYABLE", "REQUIRES_HUMAN")
LOCK_NAME = ".consumer.lock"


class ConsumerBusy(RuntimeError):
    """Another consumer holds this domain's spool: nothing was read from the ledger or sent to the domain."""

    code = "CONSUMER_BUSY"


if os.name == "nt":
    import msvcrt

    def _try_lock(handle) -> None:
        handle.seek(0)
        msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)

    def _unlock(handle) -> None:
        handle.seek(0)
        msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
else:
    import fcntl

    def _try_lock(handle) -> None:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)

    def _unlock(handle) -> None:
        fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


@contextmanager
def domain_lock(spool: Spool, domain: str):
    """Exclusive, non-blocking lock of one domain's spool directory (``ConsumerBusy`` if another holds it)."""
    directory = spool.domain_dir(domain)
    handle = open(directory / LOCK_NAME, "a+b")  # noqa: SIM115 - held for the whole pass, closed below
    try:
        try:
            _try_lock(handle)
        except OSError as exc:
            raise ConsumerBusy(f"another consumer holds the {domain} spool") from exc
        try:
            yield
        finally:
            _unlock(handle)
    finally:
        handle.close()


def utc_now() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


class Consumer:
    def __init__(self, domain: str, spool: Spool, ledger: Path, adapter: ModuleType, config: dict):
        if getattr(adapter, "DOMAIN", None) != domain:
            raise ValueError("adapter of another domain")
        self.domain, self.spool, self.adapter, self.config = domain, spool, adapter, dict(config)
        self.ledger = Path(ledger)
        self.ledger.parent.mkdir(parents=True, exist_ok=True)
        with self._db() as db:
            db.executescript(
                """
                CREATE TABLE IF NOT EXISTS deliveries(
                  task_id TEXT PRIMARY KEY, domain TEXT NOT NULL, episode INTEGER NOT NULL,
                  task_sha256 TEXT NOT NULL,
                  state TEXT NOT NULL CHECK(state IN ('IN_PROGRESS','TERMINAL_RESULT','TERMINAL_REFUSAL',
                                                      'RETRYABLE','REQUIRES_HUMAN')),
                  attempts INTEGER NOT NULL, retries_honored INTEGER NOT NULL,
                  last_status TEXT, last_result_file TEXT, reason TEXT, updated_at TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS rejections(
                  file TEXT NOT NULL, sha256 TEXT NOT NULL, code TEXT NOT NULL, reason TEXT NOT NULL,
                  at TEXT NOT NULL, PRIMARY KEY(file, sha256));
                """
            )

    @contextmanager
    def _db(self):
        db = sqlite3.connect(self.ledger, timeout=30)
        db.row_factory = sqlite3.Row
        try:
            with db:
                yield db
        finally:
            db.close()

    def _reject(self, path: Path, raw: bytes, code: str, reason: str) -> dict:
        self.spool.put_rejection(self.domain, path, raw, code, reason)
        with self._db() as db:
            db.execute(
                "INSERT OR IGNORE INTO rejections VALUES(?,?,?,?,?)",
                (path.name, sha256(raw), code, reason[:300], utc_now()),
            )
        return {"file": path.name, "action": "rejected", "code": code, "reason": reason[:300]}

    def _load(self, path: Path) -> tuple[dict | None, bytes, dict | None]:
        raw = path.read_bytes() if path.stat().st_size <= v2.MAX_TASK_BYTES else b""
        if not raw:
            return (
                None,
                raw,
                self._reject(path, raw, "SIZE_LIMIT", "task file empty or larger than MAX_TASK_BYTES"),
            )
        try:
            task = v2.loads_task(raw)
        except v2.V2Error as exc:
            return None, raw, self._reject(path, raw, exc.code, str(exc))
        if task["domain"] != self.domain:
            return None, raw, self._reject(path, raw, "DOMAIN_MISMATCH", f"task of domain {task['domain']}")
        if task_file_name(task["task_id"]) != path.name:
            return None, raw, self._reject(path, raw, "NAME_MISMATCH", "file name is not the task's own name")
        return task, raw, None

    def run_once(self) -> list[dict]:
        with domain_lock(self.spool, self.domain):
            return self._run_once()

    def _run_once(self) -> list[dict]:
        loaded = []
        report = []
        for path in self.spool.task_files(self.domain):
            current = path.read_bytes() if path.stat().st_size <= v2.MAX_TASK_BYTES else b""
            with self._db() as db:
                seen = db.execute(
                    "SELECT code FROM rejections WHERE file=? AND sha256=?", (path.name, sha256(current))
                ).fetchone()
            if seen is not None:
                report.append(
                    {"file": path.name, "action": "skipped", "state": "REJECTED", "code": seen["code"]}
                )
                continue
            task, raw, rejected = self._load(path)
            if rejected is not None:
                report.append(rejected)
                continue
            loaded.append((v2.episode_number(task["episode_id"]), task["task_id"], task, raw))
        for _episode, _task_id, task, raw in sorted(loaded, key=lambda item: (item[0], item[1])):
            report.append(self._deliver(task, raw))
        return report

    def _deliver(self, task: dict, raw: bytes) -> dict:
        task_id, task_sha = task["task_id"], sha256(raw)
        with self._db() as db:
            row = db.execute("SELECT * FROM deliveries WHERE task_id=?", (task_id,)).fetchone()
        requested = self.spool.retries_requested(self.domain, task_id)
        base = {"task_id": task_id, "episode_id": task["episode_id"]}
        if row is not None and row["task_sha256"] != task_sha:
            return base | {
                "action": "rejected",
                "code": "CONFLICT",
                "reason": "task_id seen with other bytes",
            }
        if row is not None and row["state"] not in ("IN_PROGRESS", "RETRYABLE"):
            return base | {"action": "skipped", "state": row["state"], "status": row["last_status"]}
        if row is not None and row["state"] == "RETRYABLE" and requested <= row["retries_honored"]:
            return base | {
                "action": "skipped",
                "state": "RETRYABLE",
                "status": row["last_status"],
                "reason": "waiting for a resend requested by the CAIN",
            }
        attempts = (row["attempts"] if row else 0) + 1
        honored = max(requested, row["retries_honored"] if row else 0)
        with self._db() as db:
            db.execute(
                "INSERT INTO deliveries VALUES(?,?,?,?,'IN_PROGRESS',?,?,NULL,NULL,NULL,?) "
                "ON CONFLICT(task_id) DO UPDATE SET state='IN_PROGRESS', attempts=excluded.attempts, "
                "retries_honored=excluded.retries_honored, updated_at=excluded.updated_at",
                (
                    task_id,
                    self.domain,
                    v2.episode_number(task["episode_id"]),
                    task_sha,
                    attempts,
                    honored,
                    utc_now(),
                ),
            )
        faults.fault("before_domain")
        outcome = self.adapter.submit_task(task, self.config)
        if outcome.get("submission_sha256") != sha256(v2.request_bytes(task)):
            return self._hold(
                base, "ADAPTER_BYTES_MISMATCH", "the domain did not receive request_bytes(task)"
            )
        faults.fault("after_domain_before_result_write")
        try:
            result = v2.build_result(task, outcome, adapter=self.adapter.identity(), produced_at=utc_now())
        except v2.V2Error as exc:
            return self._hold(base, exc.code, str(exc))
        if result["outcome"]["status"] in v2.RESULT_STATUSES:
            code, shown = self.adapter.reread(task["request_id"], self.config)
            if code != 0 or shown.get("result_sha256") != result["result"]["payload_sha256"]:
                return self._hold(
                    base, "BYTE_IDENTITY_MISMATCH", "payload differs from the domain's authoritative re-read"
                )
        written = self.spool.put_result(self.domain, task_id, v2.dumps_result(result, task=task))
        faults.fault("after_result_write")
        klass = v2.OUTCOME_CLASSES[result["outcome"]["status"]]
        with self._db() as db:
            db.execute(
                "UPDATE deliveries SET state=?, last_status=?, last_result_file=?, reason=?, updated_at=? "
                "WHERE task_id=?",
                (
                    klass,
                    result["outcome"]["status"],
                    written["file"],
                    result["outcome"]["reason"],
                    utc_now(),
                    task_id,
                ),
            )
        return base | {
            "action": "delivered",
            "attempt": attempts,
            "status": result["outcome"]["status"],
            "class": klass,
            "result_file": written["file"],
            "result_write": written["status"],
        }

    def _hold(self, base: dict, code: str, reason: str) -> dict:
        with self._db() as db:
            db.execute(
                "UPDATE deliveries SET state='REQUIRES_HUMAN', last_status=?, reason=?, updated_at=? "
                "WHERE task_id=?",
                (code, reason[:300], utc_now(), base["task_id"]),
            )
        return base | {"action": "held", "class": "REQUIRES_HUMAN", "code": code, "reason": reason[:300]}


__all__ = ["Consumer", "ConsumerBusy", "SpoolConflict", "STATES", "domain_lock"]
