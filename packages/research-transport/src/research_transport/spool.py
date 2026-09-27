"""Local file spool for V2 research envelopes: one directory per domain, write-once files.

Layout under the spool root (one orchestration per domain, D-22)::

    <domain>/tasks/TASK-<32 hex>.json               ResearchTaskV2, canonical bytes (written by the CAIN)
    <domain>/retries/TASK-<32 hex>.<n>.json         the CAIN asks for resend n of a RETRYABLE task
    <domain>/results/TASK-<32 hex>.<16 hex>.json    ResearchResultV2, canonical bytes (by the consumer);
                                                    the suffix is the sha256 prefix of the bytes
    <domain>/rejected/<file>.<16 hex>.json          why the consumer refused a task file

Every file is published atomically (temporary file + ``os.link``) and never overwritten: writing the same
bytes again is a no-op and different bytes under the same name are a ``SpoolConflict``. The spool only
carries bytes; the CAIN and the consumer decide what the envelopes mean.
"""

from __future__ import annotations

import hashlib
import os
import re
from pathlib import Path
from uuid import uuid4

from research_protocol import v2

_TASK_FILE = re.compile(r"TASK-[0-9a-f]{32}\.json\Z")
_RESULT_FILE = re.compile(r"(TASK-[0-9a-f]{32})\.([0-9a-f]{16})\.json\Z")
_RETRY_FILE = re.compile(r"(TASK-[0-9a-f]{32})\.([1-9][0-9]{0,5})\.json\Z")
RETRY_SCHEMA = "research-transport-retry/1"
REJECTION_SCHEMA = "research-transport-rejection/1"


class SpoolConflict(ValueError):
    """Different bytes under a name that already exists: nothing is overwritten."""

    code = "CONFLICT"


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def task_file_name(task_id: str) -> str:
    domain, _, local = task_id.partition(":")
    name = f"{local}.json"
    if domain not in v2.DOMAINS or not _TASK_FILE.fullmatch(name):
        raise v2.V2Error("ID_NOT_QUALIFIED", "task_id is not <domain>:TASK-<32 hex>")
    return name


class Spool:
    def __init__(self, root: str | os.PathLike[str]):
        self.root = Path(root)

    def _dir(self, domain: str, kind: str) -> Path:
        if domain not in v2.DOMAINS:
            raise v2.V2Error("DOMAIN_UNKNOWN", f"domain {domain[:40]!r}")
        path = self.root / domain / kind
        path.mkdir(parents=True, exist_ok=True)
        return path

    @staticmethod
    def _publish(directory: Path, name: str, raw: bytes) -> str:
        target = directory / name
        if target.exists():
            if target.read_bytes() == raw:
                return "EXISTS"
            raise SpoolConflict(f"CONFLICT: {directory.name}/{name} already has other bytes")
        tmp = directory / f".tmp-{uuid4().hex}"
        try:
            with open(tmp, "xb") as handle:
                handle.write(raw)
                handle.flush()
                os.fsync(handle.fileno())
            try:
                os.link(tmp, target)
            except FileExistsError:
                if target.read_bytes() != raw:
                    raise SpoolConflict(
                        f"CONFLICT: {directory.name}/{name} already has other bytes"
                    ) from None
                return "EXISTS"
        finally:
            tmp.unlink(missing_ok=True)
        return "WRITTEN"

    @staticmethod
    def _files(directory: Path, pattern: re.Pattern[str]) -> list[Path]:
        return sorted(p for p in directory.iterdir() if p.is_file() and pattern.fullmatch(p.name))

    # ------------------------------------------------------------------ tasks (CAIN side writes)
    def put_task(self, domain: str, raw: bytes) -> dict:
        task = v2.loads_task(raw)
        if task["domain"] != domain:
            raise v2.V2Error("DOMAIN_MISMATCH", "task of another domain")
        name = task_file_name(task["task_id"])
        status = self._publish(self._dir(domain, "tasks"), name, bytes(raw))
        return {"status": status, "file": f"{domain}/tasks/{name}", "sha256": sha256(raw)}

    def task_files(self, domain: str) -> list[Path]:
        return self._files(self._dir(domain, "tasks"), re.compile(r".+\.json\Z"))

    def request_retry(self, domain: str, task_id: str, attempt: int) -> dict:
        if type(attempt) is not int or not 1 <= attempt <= 999_999:
            raise ValueError("retry attempt must be 1..999999")
        local = task_file_name(task_id)[: -len(".json")]
        if not task_id.startswith(domain + ":"):
            raise v2.V2Error("DOMAIN_MISMATCH", "retry of a task of another domain")
        raw = v2.canonical({"schema": RETRY_SCHEMA, "task_id": task_id, "attempt": attempt})
        status = self._publish(self._dir(domain, "retries"), f"{local}.{attempt}.json", raw)
        return {"status": status, "file": f"{domain}/retries/{local}.{attempt}.json"}

    def retries_requested(self, domain: str, task_id: str) -> int:
        local = task_file_name(task_id)[: -len(".json")]
        attempts = [
            int(m.group(2))
            for p in self._files(self._dir(domain, "retries"), _RETRY_FILE)
            if (m := _RETRY_FILE.fullmatch(p.name)) and m.group(1) == local
        ]
        return max(attempts, default=0)

    # ------------------------------------------------------------------ results (consumer side writes)
    def put_result(self, domain: str, task_id: str, raw: bytes) -> dict:
        local = task_file_name(task_id)[: -len(".json")]
        if not task_id.startswith(domain + ":"):
            raise v2.V2Error("DOMAIN_MISMATCH", "result of a task of another domain")
        name = f"{local}.{sha256(raw)[:16]}.json"
        status = self._publish(self._dir(domain, "results"), name, bytes(raw))
        return {"status": status, "file": f"{domain}/results/{name}", "sha256": sha256(raw)}

    def result_files(self, domain: str) -> list[Path]:
        return self._files(self._dir(domain, "results"), re.compile(r".+\.json\Z"))

    # ------------------------------------------------------------------ rejections (consumer side writes)
    def put_rejection(self, domain: str, source: Path, raw: bytes, code: str, reason: str) -> dict:
        body = v2.canonical(
            {
                "schema": REJECTION_SCHEMA,
                "file": source.name,
                "sha256": sha256(raw),
                "code": code,
                "reason": reason[: v2.MAX_REASON_CHARS],
            }
        )
        name = f"{source.name}.{sha256(raw)[:16]}.json"
        status = self._publish(self._dir(domain, "rejected"), name, body)
        return {"status": status, "file": f"{domain}/rejected/{name}"}

    def rejection_files(self, domain: str) -> list[Path]:
        return self._files(self._dir(domain, "rejected"), re.compile(r".+\.json\Z"))
