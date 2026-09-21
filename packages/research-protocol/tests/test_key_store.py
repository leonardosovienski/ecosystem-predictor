import json
import sqlite3
from datetime import UTC, datetime, timedelta

import pytest
from research_protocol import HmacKeyStore, sign_task, verify_task

SCOPE = "crypto.research.propose"
IDENTITY = "cain-operator"
T0 = datetime(2026, 9, 20, 12, 0, tzinfo=UTC)


def task():
    return {
        "schema_version": "ResearchTaskV1",
        "task_id": "TASK-KEY-001",
        "research_id": "RESEARCH-KEY-001",
        "parent_task_id": None,
        "hypothesis_id": "HYPOTHESIS-KEY-001",
        "domain": "crypto",
        "request_type": "BACKTEST_EXISTING_HYPOTHESIS",
        "protocol_ref": {"kind": "protocol", "name": "safe", "version": "1"},
        "dataset_constraint_ref": {"kind": "dataset", "name": "frozen", "version": "1"},
        "baseline_refs": [{"kind": "baseline", "name": "base", "version": "1"}],
        "cost_model_ref": {"kind": "cost_model", "name": "cost", "version": "1"},
        "evidence_refs": [{"kind": "evidence", "name": "prior", "version": "1"}],
        "bounded_parameters": {
            "symbol": "BTCUSDT",
            "horizon_days": 1,
            "max_observations": 30,
            "fee_bps": 2,
            "slippage_bps": 3,
        },
        "priority_hint": "NORMAL",
        "created_at": "2026-09-20T12:00:00Z",
        "expires_at": "2026-09-20T13:00:00Z",
        "requested_by": "cain-session",
        "provenance": {
            "cain_source_sha": "a" * 40,
            "retrieval_receipt_ids": ["RECEIPT-1"],
            "proposal_model": None,
        },
    }


def test_rotation_grace_revocation_backup_and_no_secret_leak(tmp_path):
    store = HmacKeyStore(tmp_path / "keys")
    old_secret = b"o" * 32
    new_secret = b"n" * 32
    provisioned = store.provision(IDENTITY, SCOPE, "key-1", secret=old_secret, at=T0)
    assert provisioned["state"] == "ACTIVE"
    assert provisioned["secret_fingerprint"]
    assert old_secret.hex() not in json.dumps(provisioned)
    assert store.acl_attestation()["protected"] is True

    key_id, secret = store.signing_key(IDENTITY, SCOPE)
    envelope = sign_task(
        task(), producer="CAIN", publisher_identity=IDENTITY, consumer="CRIPTO",
        scope=SCOPE, key_id=key_id, secret=secret,
    )
    verify_task(envelope, lambda identity, key: store.resolve(identity, key, SCOPE, at=T0))

    rotation = store.rotate(
        IDENTITY, SCOPE, "key-2", grace_seconds=60, secret=new_secret, at=T0 + timedelta(seconds=10)
    )
    assert rotation["previous"]["state"] == "VERIFY_ONLY"
    assert store.signing_key(IDENTITY, SCOPE) == ("key-2", new_secret)
    verify_task(
        envelope,
        lambda identity, key: store.resolve(identity, key, SCOPE, at=T0 + timedelta(seconds=30)),
    )
    with pytest.raises(PermissionError, match="unknown or revoked"):
        verify_task(
            envelope,
            lambda identity, key: store.resolve(identity, key, SCOPE, at=T0 + timedelta(seconds=71)),
        )

    store.revoke("key-2", at=T0 + timedelta(seconds=40))
    with pytest.raises(PermissionError, match="no active signing key"):
        store.signing_key(IDENTITY, SCOPE)
    assert store.resolve(IDENTITY, "key-2", SCOPE, at=T0 + timedelta(seconds=41)) is None

    public_evidence = json.dumps({
        "receipts": [store.receipt("key-1"), store.receipt("key-2")],
        "events": store.events(),
    })
    assert old_secret.hex() not in public_evidence
    assert new_secret.hex() not in public_evidence
    assert old_secret not in store.path.read_bytes()
    assert new_secret not in store.path.read_bytes()
    db = sqlite3.connect(store.path)
    try:
        assert "secret" not in {row[1] for row in db.execute("PRAGMA table_info(keys)")}
    finally:
        db.close()

    backup = store.backup(tmp_path / "backup" / "keys")
    assert len(backup["manifest_sha256"]) == 64
    db = sqlite3.connect(tmp_path / "backup" / "keys" / "metadata.sqlite")
    try:
        assert db.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
    finally:
        db.close()
    restored = HmacKeyStore.restore(backup["path"], tmp_path / "restored")
    assert restored.resolve(IDENTITY, "key-1", SCOPE, at=T0 + timedelta(seconds=30)) == old_secret
    assert restored.resolve(IDENTITY, "key-2", SCOPE, at=T0 + timedelta(seconds=41)) is None


def test_secret_corruption_and_legacy_secret_database_fail_closed(tmp_path):
    store = HmacKeyStore(tmp_path / "keys")
    store.provision(IDENTITY, SCOPE, "key-1", secret=b"x" * 32, at=T0)
    secret_file = next(store.vault.glob("*.key"))
    secret_file.write_bytes(b"tampered")
    with pytest.raises(PermissionError, match="integrity failure"):
        store.signing_key(IDENTITY, SCOPE)

    legacy = tmp_path / "legacy"
    legacy.mkdir()
    db = sqlite3.connect(legacy / "metadata.sqlite")
    try:
        db.execute("CREATE TABLE keys(key_id TEXT, secret BLOB)")
    finally:
        db.close()
    with pytest.raises(RuntimeError, match="embeds secrets"):
        HmacKeyStore(legacy)


def test_rotation_is_atomic_and_wrong_identity_scope_fail_closed(tmp_path):
    store = HmacKeyStore(tmp_path / "keys")
    store.provision(IDENTITY, SCOPE, "key-1", secret=b"x" * 32, at=T0)
    assert store.resolve("other", "key-1", SCOPE, at=T0) is None
    assert store.resolve(IDENTITY, "key-1", "wrong.scope", at=T0) is None
    with pytest.raises(ValueError, match="active key already exists"):
        store.provision(IDENTITY, SCOPE, "key-other", secret=b"y" * 32, at=T0)
    assert store.signing_key(IDENTITY, SCOPE) == ("key-1", b"x" * 32)
