"""Operator-owned HMAC key lifecycle without secrets in SQLite or receipts."""

from __future__ import annotations

import csv
import hashlib
import io
import json
import os
import re
import secrets
import shutil
import sqlite3
import subprocess
from contextlib import contextmanager
from datetime import UTC, datetime, timedelta
from pathlib import Path
from uuid import uuid4

_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:-]{0,127}\Z")


def _at(value: datetime | None = None) -> datetime:
    value = value or datetime.now(UTC)
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("key lifecycle timestamps require timezone")
    return value.astimezone(UTC)


def _stamp(value: datetime) -> str:
    return value.isoformat(timespec="microseconds").replace("+00:00", "Z")


def _check_id(value: str, label: str) -> None:
    if not isinstance(value, str) or _ID.fullmatch(value) is None:
        raise ValueError(f"invalid {label}")


def _sha(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def _current_windows_sid() -> str:
    result = subprocess.run(
        ["whoami", "/user", "/fo", "csv", "/nh"],
        check=True,
        capture_output=True,
        text=True,
        timeout=15,
    )
    sid = next(csv.reader(io.StringIO(result.stdout.strip())))[-1].strip()
    if not re.fullmatch(r"S-1-[0-9-]+", sid):
        raise RuntimeError("unable to resolve current Windows SID")
    return sid


def _protect_root(root: Path) -> dict:
    root.mkdir(parents=True, exist_ok=True)
    if os.name != "nt":
        root.chmod(0o700)
        return {"method": "POSIX_MODE", "mode": "0700", "protected": True}
    sid = _current_windows_sid()
    applied = subprocess.run(
        [
            "icacls",
            str(root),
            "/inheritance:r",
            "/grant:r",
            f"*{sid}:(OI)(CI)F",
            "*S-1-5-18:(OI)(CI)F",
        ],
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )
    if applied.returncode:
        raise PermissionError(f"unable to protect key store ACL: {applied.stderr.strip()}")
    observed = subprocess.run(
        ["icacls", str(root)], check=True, capture_output=True, text=True, timeout=30
    ).stdout
    return {
        "method": "WINDOWS_DACL",
        "identity_sid": sid,
        "system_sid": "S-1-5-18",
        "inheritance": "REMOVED",
        "acl_observation_sha256": hashlib.sha256(observed.encode()).hexdigest(),
        "protected": True,
    }


class HmacKeyStore:
    """Metadata in SQLite; secret bytes only in an ACL-protected file vault."""

    def __init__(self, root: str | Path):
        self.root = Path(root).resolve()
        self._acl = _protect_root(self.root)
        self.vault = self.root / "secrets"
        _protect_root(self.vault)
        self.path = self.root / "metadata.sqlite"
        with self.connection() as db:
            columns = {row[1] for row in db.execute("PRAGMA table_info(keys)")}
            if "secret" in columns:
                raise RuntimeError(
                    "legacy key store embeds secrets in SQLite; reprovision into OperatorHmacKeyStoreV2"
                )
            db.executescript(
                """
                PRAGMA journal_mode=DELETE;
                PRAGMA synchronous=FULL;
                CREATE TABLE IF NOT EXISTS keys(
                  key_id TEXT PRIMARY KEY,
                  publisher_identity TEXT NOT NULL,
                  scope TEXT NOT NULL,
                  state TEXT NOT NULL CHECK(state IN ('ACTIVE','VERIFY_ONLY','REVOKED')),
                  secret_ref TEXT NOT NULL UNIQUE,
                  secret_sha256 TEXT NOT NULL,
                  created_at TEXT NOT NULL,
                  verify_until TEXT,
                  revoked_at TEXT,
                  replaced_by TEXT
                );
                CREATE UNIQUE INDEX IF NOT EXISTS one_active_key
                  ON keys(publisher_identity,scope) WHERE state='ACTIVE';
                CREATE TABLE IF NOT EXISTS key_events(
                  sequence INTEGER PRIMARY KEY AUTOINCREMENT,
                  event TEXT NOT NULL,
                  key_id TEXT NOT NULL,
                  publisher_identity TEXT NOT NULL,
                  scope TEXT NOT NULL,
                  recorded_at TEXT NOT NULL,
                  detail TEXT
                );
                """
            )
        if os.name != "nt":
            self.path.chmod(0o600)

    @contextmanager
    def connection(self):
        db = sqlite3.connect(self.path, timeout=15)
        db.row_factory = sqlite3.Row
        try:
            with db:
                yield db
        finally:
            db.close()

    @staticmethod
    def _secret(value: bytes | None) -> bytes:
        value = secrets.token_bytes(32) if value is None else value
        if not isinstance(value, bytes) or len(value) < 32:
            raise ValueError("HMAC secret must contain at least 32 bytes")
        return value

    @staticmethod
    def _event(db, event, row, recorded_at, detail=None):
        db.execute(
            "INSERT INTO key_events(event,key_id,publisher_identity,scope,recorded_at,detail) "
            "VALUES(?,?,?,?,?,?)",
            (event, row["key_id"], row["publisher_identity"], row["scope"], recorded_at, detail),
        )

    @staticmethod
    def _ref(key_id: str) -> str:
        return hashlib.sha256(("research-hmac-key:" + key_id).encode()).hexdigest() + ".key"

    def _secret_path(self, secret_ref: str) -> Path:
        if not re.fullmatch(r"[0-9a-f]{64}\.key", secret_ref):
            raise ValueError("invalid secret reference")
        path = (self.vault / secret_ref).resolve()
        if path.parent != self.vault:
            raise PermissionError("secret reference escapes vault")
        return path

    def _write_secret(self, key_id: str, value: bytes) -> tuple[str, str]:
        secret_ref = self._ref(key_id)
        target = self._secret_path(secret_ref)
        if target.exists():
            raise FileExistsError("secret identity already exists")
        temp = self.vault / ("." + secret_ref + "." + uuid4().hex + ".tmp")
        try:
            flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
            if hasattr(os, "O_BINARY"):
                flags |= os.O_BINARY
            descriptor = os.open(temp, flags, 0o600)
            try:
                os.write(descriptor, value)
                os.fsync(descriptor)
            finally:
                os.close(descriptor)
            os.replace(temp, target)
            if os.name != "nt":
                target.chmod(0o600)
        finally:
            if temp.exists():
                temp.unlink()
        return secret_ref, hashlib.sha256(value).hexdigest()

    def _read_secret(self, secret_ref: str, expected_hash: str) -> bytes:
        path = self._secret_path(secret_ref)
        if not path.exists() or path.is_symlink() or getattr(path, "is_junction", lambda: False)():
            raise PermissionError("key material unavailable")
        value = path.read_bytes()
        if len(value) < 32 or hashlib.sha256(value).hexdigest() != expected_hash:
            raise PermissionError("key material integrity failure")
        return value

    def provision(self, publisher_identity, scope, key_id, *, secret=None, at=None) -> dict:
        identities = (
            (publisher_identity, "publisher identity"),
            (scope, "scope"),
            (key_id, "key id"),
        )
        for value, label in identities:
            _check_id(value, label)
        created, secret = _stamp(_at(at)), self._secret(secret)
        secret_ref = None
        try:
            with self.connection() as db:
                db.execute("BEGIN IMMEDIATE")
                if db.execute(
                    "SELECT 1 FROM keys WHERE publisher_identity=? AND scope=? AND state='ACTIVE'",
                    (publisher_identity, scope),
                ).fetchone():
                    raise ValueError("active key already exists; use rotate")
                secret_ref, fingerprint = self._write_secret(key_id, secret)
                db.execute(
                    "INSERT INTO keys VALUES(?,?,?,?,?,?,?,?,?,?)",
                    (
                        key_id, publisher_identity, scope, "ACTIVE", secret_ref,
                        fingerprint, created, None, None, None,
                    ),
                )
                row = db.execute("SELECT * FROM keys WHERE key_id=?", (key_id,)).fetchone()
                self._event(db, "PROVISIONED", row, created)
        except Exception:
            if secret_ref is not None:
                self._secret_path(secret_ref).unlink(missing_ok=True)
            raise
        return self.receipt(key_id)

    def rotate(self, publisher_identity, scope, new_key_id, *, grace_seconds, secret=None, at=None) -> dict:
        identities = (
            (publisher_identity, "publisher identity"),
            (scope, "scope"),
            (new_key_id, "key id"),
        )
        for value, label in identities:
            _check_id(value, label)
        if not isinstance(grace_seconds, int) or not 0 <= grace_seconds <= 31_536_000:
            raise ValueError("invalid rotation grace period")
        moment = _at(at)
        recorded = _stamp(moment)
        verify_until = _stamp(moment + timedelta(seconds=grace_seconds))
        secret = self._secret(secret)
        secret_ref = None
        try:
            with self.connection() as db:
                db.execute("BEGIN IMMEDIATE")
                old = db.execute(
                    "SELECT * FROM keys WHERE publisher_identity=? AND scope=? AND state='ACTIVE'",
                    (publisher_identity, scope),
                ).fetchone()
                if old is None:
                    raise ValueError("active key not found")
                secret_ref, fingerprint = self._write_secret(new_key_id, secret)
                db.execute(
                    "UPDATE keys SET state='VERIFY_ONLY',verify_until=?,replaced_by=? WHERE key_id=?",
                    (verify_until, new_key_id, old["key_id"]),
                )
                self._event(db, "ROTATED_FROM", old, recorded, f"replaced_by={new_key_id}")
                db.execute(
                    "INSERT INTO keys VALUES(?,?,?,?,?,?,?,?,?,?)",
                    (
                        new_key_id, publisher_identity, scope, "ACTIVE", secret_ref,
                        fingerprint, recorded, None, None, None,
                    ),
                )
                new = db.execute("SELECT * FROM keys WHERE key_id=?", (new_key_id,)).fetchone()
                self._event(db, "ROTATED_TO", new, recorded, f"replaces={old['key_id']}")
        except Exception:
            if secret_ref is not None:
                self._secret_path(secret_ref).unlink(missing_ok=True)
            raise
        return {"previous": self.receipt(old["key_id"]), "active": self.receipt(new_key_id)}

    def revoke(self, key_id: str, *, at=None) -> dict:
        _check_id(key_id, "key id")
        recorded = _stamp(_at(at))
        with self.connection() as db:
            db.execute("BEGIN IMMEDIATE")
            row = db.execute("SELECT * FROM keys WHERE key_id=?", (key_id,)).fetchone()
            if row is None:
                raise KeyError(key_id)
            if row["state"] != "REVOKED":
                db.execute(
                    "UPDATE keys SET state='REVOKED',revoked_at=?,verify_until=NULL WHERE key_id=?",
                    (recorded, key_id),
                )
                self._event(db, "REVOKED", row, recorded)
        return self.receipt(key_id)

    def signing_key(self, publisher_identity: str, scope: str) -> tuple[str, bytes]:
        with self.connection() as db:
            row = db.execute(
                "SELECT key_id,secret_ref,secret_sha256 FROM keys "
                "WHERE publisher_identity=? AND scope=? AND state='ACTIVE'",
                (publisher_identity, scope),
            ).fetchone()
        if row is None:
            raise PermissionError("no active signing key")
        return row["key_id"], self._read_secret(row["secret_ref"], row["secret_sha256"])

    def resolve(self, publisher_identity, key_id, scope, *, at=None) -> bytes | None:
        moment = _at(at)
        with self.connection() as db:
            row = db.execute(
                "SELECT * FROM keys WHERE key_id=? AND publisher_identity=? AND scope=?",
                (key_id, publisher_identity, scope),
            ).fetchone()
        if row is None or row["state"] == "REVOKED":
            return None
        if row["state"] == "VERIFY_ONLY":
            verify_until = datetime.fromisoformat(row["verify_until"].replace("Z", "+00:00"))
            if moment > verify_until:
                return None
        return self._read_secret(row["secret_ref"], row["secret_sha256"])

    def receipt(self, key_id: str) -> dict:
        with self.connection() as db:
            row = db.execute("SELECT * FROM keys WHERE key_id=?", (key_id,)).fetchone()
        if row is None:
            raise KeyError(key_id)
        return {
            "key_id": row["key_id"], "publisher_identity": row["publisher_identity"],
            "scope": row["scope"], "state": row["state"], "created_at": row["created_at"],
            "verify_until": row["verify_until"], "revoked_at": row["revoked_at"],
            "replaced_by": row["replaced_by"], "secret_fingerprint": row["secret_sha256"],
            "storage": "OS_ACL_FILE_VAULT",
        }

    def events(self) -> list[dict]:
        with self.connection() as db:
            rows = db.execute(
                "SELECT sequence,event,key_id,publisher_identity,scope,recorded_at,detail "
                "FROM key_events ORDER BY sequence"
            ).fetchall()
        return [dict(row) for row in rows]

    def acl_attestation(self) -> dict:
        return dict(self._acl)

    def backup(self, destination: str | Path) -> dict:
        destination = Path(destination).resolve()
        if destination.exists():
            raise FileExistsError(destination)
        destination.parent.mkdir(parents=True, exist_ok=True)
        temp = destination.parent / ("." + destination.name + "." + uuid4().hex + ".tmp")
        temp.mkdir()
        try:
            metadata = temp / "metadata.sqlite"
            source, target = sqlite3.connect(self.path), sqlite3.connect(metadata)
            try:
                source.backup(target)
            finally:
                target.close()
                source.close()
            vault = temp / "secrets"
            vault.mkdir()
            db = sqlite3.connect(metadata)
            try:
                rows = db.execute("SELECT secret_ref,secret_sha256 FROM keys ORDER BY key_id").fetchall()
            finally:
                db.close()
            secret_hashes = {}
            for secret_ref, expected in rows:
                value = self._read_secret(secret_ref, expected)
                target_secret = vault / secret_ref
                target_secret.write_bytes(value)
                if os.name != "nt":
                    target_secret.chmod(0o600)
                secret_hashes[secret_ref] = expected
            manifest = {
                "schema_version": "OperatorHmacKeyStoreBackupV1", "metadata_sha256": _sha(metadata),
                "secret_files": secret_hashes, "created_at": _stamp(_at()),
            }
            (temp / "manifest.json").write_text(
                json.dumps(manifest, sort_keys=True, separators=(",", ":")), encoding="utf-8"
            )
            temp.rename(destination)
            _protect_root(destination)
            _protect_root(destination / "secrets")
        except Exception:
            shutil.rmtree(temp, ignore_errors=True)
            raise
        return {
            "path": str(destination),
            "manifest_sha256": _sha(destination / "manifest.json"),
            "created_at": manifest["created_at"],
        }

    @classmethod
    def restore(cls, backup: str | Path, destination: str | Path) -> HmacKeyStore:
        backup, destination = Path(backup).resolve(), Path(destination).resolve()
        if destination.exists():
            raise FileExistsError(destination)
        if backup.is_symlink() or getattr(backup, "is_junction", lambda: False)():
            raise PermissionError("key backup indirection denied")
        manifest = json.loads((backup / "manifest.json").read_text(encoding="utf-8"))
        if set(manifest) != {"schema_version", "metadata_sha256", "secret_files", "created_at"}:
            raise ValueError("invalid key backup manifest")
        if (
            manifest["schema_version"] != "OperatorHmacKeyStoreBackupV1"
            or _sha(backup / "metadata.sqlite") != manifest["metadata_sha256"]
        ):
            raise ValueError("key backup metadata mismatch")
        for secret_ref, expected in manifest["secret_files"].items():
            if _sha(backup / "secrets" / secret_ref) != expected:
                raise ValueError("key backup secret mismatch")
        destination.parent.mkdir(parents=True, exist_ok=True)
        temp = destination.parent / ("." + destination.name + "." + uuid4().hex + ".tmp")
        try:
            shutil.copytree(backup, temp)
            (temp / "manifest.json").unlink()
            temp.rename(destination)
            _protect_root(destination)
            _protect_root(destination / "secrets")
            return cls(destination)
        except Exception:
            shutil.rmtree(temp, ignore_errors=True)
            raise


__all__ = ["HmacKeyStore"]
