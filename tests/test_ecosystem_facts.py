import copy
import json
from datetime import UTC, datetime

import pytest

from scripts import sync_ecosystem_facts as facts


def _repository(name="example-predictor"):
    return {
        "repository": name,
        "branch": "main",
        "head": "a" * 40,
        "source_ref": f"{name}@{'a' * 40}",
        "version": "1.0.0",
        "python": ">=3.13",
        "core": "==2.2.0 (v2.2.0)",
        "ops": "==3.0.0 (v3.0.0)",
        "workflow": ".github/workflows/ci.yml",
        "ci": "success",
        "ci_url": "https://example.invalid/run/1",
        "canonical": ["README.md", "pyproject.toml"],
    }


def _snapshot(*repositories):
    return facts.make_snapshot(list(repositories or [_repository()]), "2026-08-11T00:00:00Z")


def _assert_drift(expected, observed, field):
    with pytest.raises(facts.FactError, match=f"FACTUAL_DRIFT: .*{field}"):
        facts.compare(expected, observed)


def test_output_is_deterministic_and_sorted():
    snapshot = facts.make_snapshot([_repository("z"), _repository("a")], "2026-08-11T00:00:00Z")
    assert [item["repository"] for item in snapshot["repositories"]] == ["a", "z"]
    assert facts.render(snapshot) == facts.render(copy.deepcopy(snapshot))


def test_fixture_without_drift():
    snapshot = _snapshot()
    facts.compare(snapshot, copy.deepcopy(snapshot))


@pytest.mark.parametrize("field,value", [("head", "b" * 40), ("version", "2.0.0"), ("core", "==9")])
def test_mechanical_drift(field, value):
    expected, observed = _snapshot(), _snapshot()
    observed["repositories"][0][field] = value
    _assert_drift(expected, observed, field)


def test_ops_drift():
    expected, observed = _snapshot(), _snapshot()
    observed["repositories"][0]["ops"] = "==4"
    _assert_drift(expected, observed, "ops")


def test_missing_document_is_drift():
    expected, observed = _snapshot(), _snapshot()
    observed["repositories"][0]["canonical"].remove("README.md")
    _assert_drift(expected, observed, "canonical")


def test_ci_for_another_commit_is_not_accepted():
    expected, observed = _snapshot(), _snapshot()
    observed["repositories"][0]["ci"] = "UNKNOWN"
    observed["repositories"][0]["ci_url"] = ""
    _assert_drift(expected, observed, "ci")


def test_broken_internal_link(tmp_path):
    document = tmp_path / "ECOSYSTEM_CURRENT_STATE.md"
    document.write_text("[missing](missing.md)", encoding="utf-8")
    (tmp_path / "README.md").write_text("ok", encoding="utf-8")
    with pytest.raises(facts.FactError, match="FACTUAL_DRIFT: broken internal links"):
        facts.validate_links(document)


def test_external_source_unavailable(monkeypatch):
    monkeypatch.setattr(facts, "urlopen", lambda *args, **kwargs: (_ for _ in ()).throw(OSError("down")))
    with pytest.raises(facts.FactError, match="SOURCE_UNAVAILABLE"):
        facts._request("/test", None)


def test_external_timeout(monkeypatch):
    monkeypatch.setattr(facts, "urlopen", lambda *args, **kwargs: (_ for _ in ()).throw(TimeoutError("late")))
    with pytest.raises(facts.FactError, match="SOURCE_UNAVAILABLE"):
        facts._request("/test", None, timeout=0.01)


def test_invalid_schema():
    with pytest.raises(facts.FactError, match="INVALID_SCHEMA"):
        facts.validate_schema({"schema_version": "wrong"})


def test_human_fields_are_rejected_from_mechanical_schema():
    snapshot = _snapshot()
    snapshot["repositories"][0]["scientific_state"] = "GO"
    with pytest.raises(facts.FactError, match="INVALID_SCHEMA"):
        facts.validate_schema(snapshot)


def test_ecosystem_self_head_and_ci_are_derived():
    expected = _snapshot(_repository("ecosystem-predictor"))
    observed = copy.deepcopy(expected)
    observed["repositories"][0].update(head="b" * 40, ci="UNKNOWN", ci_url="")
    facts.compare(expected, observed)
    block = facts.render(expected)
    assert "HEAD derivado em execução" in block
    assert "aaaaaaaaaaaa" not in block


def test_offline_check_never_collects(monkeypatch, tmp_path):
    snapshot = _snapshot()
    snapshot_path = tmp_path / "facts.json"
    snapshot_path.write_text(json.dumps(snapshot), encoding="utf-8")
    document = tmp_path / "ECOSYSTEM_CURRENT_STATE.md"
    document.write_text("# State\n" + facts.render(snapshot) + "\n[readme](README.md)\n", encoding="utf-8")
    (tmp_path / "README.md").write_text("[state](ECOSYSTEM_CURRENT_STATE.md)", encoding="utf-8")
    monkeypatch.setattr(facts, "collect", lambda *args, **kwargs: pytest.fail("network used"))
    assert facts.main(["--offline-check", "--snapshot", str(snapshot_path), "--document", str(document)]) == 0


def test_diff_is_fail_fast(tmp_path):
    snapshot = _snapshot()
    snapshot_path = tmp_path / "facts.json"
    snapshot_path.write_text(json.dumps(snapshot), encoding="utf-8")
    document = tmp_path / "ECOSYSTEM_CURRENT_STATE.md"
    document.write_text(
        "# State\n<!-- mechanical-facts:start -->\nstale\n<!-- mechanical-facts:end -->\n", encoding="utf-8"
    )
    (tmp_path / "README.md").write_text("ok", encoding="utf-8")
    with pytest.raises(facts.FactError, match="FACTUAL_DRIFT"):
        facts.main(["--offline-check", "--snapshot", str(snapshot_path), "--document", str(document)])


def test_invalid_snapshot_file(tmp_path):
    path = tmp_path / "facts.json"
    path.write_text("not-json", encoding="utf-8")
    with pytest.raises(facts.FactError, match="INVALID_SCHEMA"):
        facts._load(path)


def test_expired_snapshot_requires_review():
    snapshot = _snapshot()
    with pytest.raises(facts.FactError, match="STALE_REVIEW_REQUIRED"):
        facts.validate_freshness(
            snapshot,
            now=datetime(2026, 8, 20, tzinfo=UTC),
            max_age_hours=24,
        )
