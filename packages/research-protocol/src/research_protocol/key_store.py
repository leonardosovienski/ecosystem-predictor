"""Operator-owned HMAC key lifecycle for research message publishers.

The store is deliberately local and small: SQLite supplies atomic rotation and
backup, while the containing directory is restricted to the current Windows
identity and SYSTEM (or mode 0700 on POSIX).  Secrets never appear in receipts
or audit events.
"""

from __future__ import annotations

import csv
import hashlib
import io
import os
import re
import secrets
import sqlite3
import subprocess
from contextlib import contextmanager
from datetime import UTC, datetime, timedelta
from pathlib import Path

_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:-]{0,127}\Z")
_STATES = {"ACTIVE", "VERIFY_ONLY", "REVOKED"}


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


def _current_windows_sid() -> str:
    result = subprocess.run(
        ["whoami", "/user", "/fo", "csv", "/nh"],
        check=True,
        capture_output=True,
        text=True,
        timeout=15,
    )
    row = next(csv.reader(io.StringIO(result.stdout.strip())))
    sid = row[-1].strip()
    if not re.fullmatch(r"S-1-[0-9-]+", sid):
        raise RuntimeError("unable to resolve current Windows SID")
    return sid


def _protect_root(root: Path) -> dict:
    root.mkdir(parents=True, exist_ok=True)
    if os.name != "nt":
        root.chmod(0o700)
        return {"method": "POSIX_MODE", "mode": "0700", "protected": True}
    sid = _current_windows_sid()
    result = subprocess.run(
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
    if result.returncode:
        raise PermissionError(f"unable to protect key store ACL: {result.stderr.strip()}")
    return {
        "method": "WINDOWS_DACL",
        "identity_sid": sid,
        "system_sid": "S-1-5-18",
        "inheritance": "REMOVED",
        "protected": True,
    }


class HmacKeyStore:
    """Durable operator key store with rotation, revocation and safe receipts."""

    def __init__(self, root: str | Path):
        self.root = Path(root).resolve()
        self._acl = _protect_root(self.root)
        self.path = self.root / "research-hmac-keys.sqlite"
        with self.connection() as db:
            db.executescript(
                """
                PRAGMA journal_mode=DELETE;
                PRAGMA synchronous=FULL;
                CREATE TABLE IF NOT EXISTS keys(
                  key_id TEXT PRIMARY KEY,
                  publisher_identity TEXT NOT NULL,
                  scope TEXT NOT NULL,
                  state TEXT NOT NULL CHECK(state IN ('ACTIVE','VERIFY_ONLY','REVOKED')),
                  secret BLOB NOT NULL,
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

    def provision(
        self,
        publisher_identity: str,
        scope: str,
        key_id: str,
        *,
        secret: bytes | None = None,
        at: datetime | None = None,
    ) -> dict:
        identities = (
            (publisher_identity, "publisher identity"),
            (scope, "scope"),
            (key_id, "key id"),
        )
        for value, label in identities:
            _check_id(value, label)
        created = _stamp(_at(at))
        secret = self._secret(secret)
        with self.connection() as db:
            db.execute("BEGIN IMMEDIATE")
            if db.execute(
                "SELECT 1 FROM keys WHERE publisher_identity=? AND scope=? AND state='ACTIVE'",
                (publisher_identity, scope),
            ).fetchone():
                raise ValueError("active key already exists; use rotate")
            db.execute(
                "INSERT INTO keys VALUES(?,?,?,?,?,?,?,?,?)",
                (key_id, publisher_identity, scope, "ACTIVE", secret, created, None, None, None),
            )
            row = db.execute("SELECT * FROM keys WHERE key_id=?", (key_id,)).fetchone()
            self._event(db, "PROVISIONED", row, created)
        return self.receipt(key_id)

    def rotate(
        self,
        publisher_identity: str,
        scope: str,
        new_key_id: str,
        *,
        grace_seconds: int,
        secret: bytes | None = None,
        at: datetime | None = None,
    ) -> dict:
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
        with self.connection() as db:
            db.execute("BEGIN IMMEDIATE")
            old = db.execute(
                "SELECT * FROM keys WHERE publisher_identity=? AND scope=? AND state='ACTIVE'",
                (publisher_identity, scope),
            ).fetchone()
            if old is None:
                raise ValueError("active key not found")
            db.execute(
                "UPDATE keys SET state='VERIFY_ONLY',verify_until=?,replaced_by=? WHERE key_id=?",
                (verify_until, new_key_id, old["key_id"]),
            )
            self._event(db, "ROTATED_FROM", old, recorded, f"replaced_by={new_key_id}")
            db.execute(
                "INSERT INTO keys VALUES(?,?,?,?,?,?,?,?,?)",
                (new_key_id, publisher_identity, scope, "ACTIVE", secret, recorded, None, None, None),
            )
            new = db.execute("SELECT * FROM keys WHERE key_id=?", (new_key_id,)).fetchone()
            self._event(db, "ROTATED_TO", new, recorded, f"replaces={old['key_id']}")
        return {"previous": self.receipt(old["key_id"]), "active": self.receipt(new_key_id)}

    def revoke(self, key_id: str, *, at: datetime | None = None) -> dict:
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
                "SELECT key_id,secret FROM keys WHERE publisher_identity=? AND scope=? AND state='ACTIVE'",
                (publisher_identity, scope),
            ).fetchone()
        if row is None:
            raise PermissionError("no active signing key")
        return row["key_id"], bytes(row["secret"])

    def resolve(
        self,
        publisher_identity: str,
        key_id: str,
        scope: str,
        *,
        at: datetime | None = None,
    ) -> bytes | None:
        moment = _at(at)
        with self.connection() as db:
            row = db.execute(
                "SELECT * FROM keys WHERE key_id=? AND publisher_identity=? AND scope=?",
                (key_id, publisher_identity, scope),
            ).fetchone()
        if row is None or row["state"] == "REVOKED":
            return None
        if row["state"] == "VERIFY_ONLY":
            verify_until = (
                datetime.fromisoformat(row["verify_until"].replace("Z", "+00:00"))
                if row["verify_until"] is not None
                else None
            )
            if verify_until is None or moment > verify_until:
                return None
        return bytes(row["secret"])

    def receipt(self, key_id: str) -> dict:
        with self.connection() as db:
            row = db.execute("SELECT * FROM keys WHERE key_id=?", (key_id,)).fetchone()
        if row is None:
            raise KeyError(key_id)
        return {
            "key_id": row["key_id"],
            "publisher_identity": row["publisher_identity"],
            "scope": row["scope"],
            "state": row["state"],
            "created_at": row["created_at"],
            "verify_until": row["verify_until"],
            "revoked_at": row["revoked_at"],
            "replaced_by": row["replaced_by"],
            "secret_fingerprint": hashlib.sha256(bytes(row["secret"])).hexdigest(),
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
        _protect_root(destination.parent)
        if destination.exists():
            raise FileExistsError(destination)
        source = sqlite3.connect(self.path)
        target = sqlite3.connect(destination)
        try:
            source.backup(target)
        finally:
            target.close()
            source.close()
        if os.name != "nt":
            destination.chmod(0o600)
        return {
            "path": str(destination),
            "sha256": hashlib.sha256(destination.read_bytes()).hexdigest(),
            "created_at": _stamp(_at()),
        }


__all__ = ["HmacKeyStore"]
