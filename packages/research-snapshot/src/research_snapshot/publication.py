"""Immutable local publication; readers see either no file or complete bytes."""

from __future__ import annotations

import os
import tempfile
from pathlib import Path

from research_snapshot import canonical, digest, validate


def publish(package: dict, destination: Path) -> str:
    """Validate, fsync and atomically link bytes without replacing an existing file.

    Retrying the same bytes recovers the receipt after a process interruption.
    A conflicting destination is an error. Filesystems without hard links fail
    closed; no non-atomic copy fallback is used.
    """
    payload = canonical(validate(package))
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    descriptor, name = tempfile.mkstemp(prefix=".snapshot-", dir=destination.parent)
    temporary = Path(name)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        try:
            os.link(temporary, destination)
        except FileExistsError:
            if destination.is_symlink() or destination.read_bytes() != payload:
                raise FileExistsError("publication conflict") from None
        if os.name != "nt":
            directory = os.open(destination.parent, os.O_RDONLY)
            try:
                os.fsync(directory)
            finally:
                os.close(directory)
        return digest(payload)
    finally:
        temporary.unlink(missing_ok=True)
