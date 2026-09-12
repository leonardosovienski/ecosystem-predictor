"""Bounded local transport I/O. No fetch, unpack or domain lookup.

POSIX uses descriptor-relative O_NOFOLLOW on every path component. Windows
opens with sharing restricted to readers, rejects reparse points, and checks
the opened handle's final path. Storage parents must be administrator-owned.
"""

import errno
import hashlib
import os
import stat
from contextlib import contextmanager
from pathlib import Path

from research_bundle import safe_path


def no_links(path):
    path = Path(path).absolute()
    for part in [*reversed(path.parents), path]:
        info = part.lstat()
        if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & 0x400:
            raise ValueError("UNSAFE_PATH: link/reparse point")
    return path


def safe_mkdirs(path):
    """Create and durably link each directory beneath trusted parents on POSIX.

    Sync existing entries too: another writer may have created them without yet
    syncing, or a previous failed attempt may have left an unsynced directory.
    Windows fsync_dir deliberately provides no directory durability guarantee.
    """
    path = Path(path).absolute()
    for part in [*reversed(path.parents), path]:
        if not part.exists():
            part.mkdir(exist_ok=True)
        no_links(part)
        if not part.is_dir():
            raise ValueError("UNSAFE_PATH: expected directory")
        if part != part.parent:
            fsync_dir(part.parent)
    return path


def _posix_open(path, flags, *, dir_fd=None):
    try:
        return os.open(path, flags, dir_fd=dir_fd)
    except OSError as exc:
        if exc.errno in (errno.ELOOP, errno.ENOTDIR):
            raise ValueError("UNSAFE_PATH: symlink or non-directory component") from exc
        raise


@contextmanager
def safe_open(root, relative):
    safe_path(relative)
    root = no_links(root)
    candidate = root / relative
    if os.name == "nt":
        import ctypes
        import msvcrt
        from ctypes import wintypes

        no_links(candidate)
        kernel = ctypes.WinDLL("kernel32", use_last_error=True)
        create = kernel.CreateFileW
        create.argtypes = [
            wintypes.LPCWSTR,
            wintypes.DWORD,
            wintypes.DWORD,
            wintypes.LPVOID,
            wintypes.DWORD,
            wintypes.DWORD,
            wintypes.HANDLE,
        ]
        create.restype = wintypes.HANDLE
        handle = create(str(candidate), 0x80000000, 1, None, 3, 0x08200000, None)
        if handle == ctypes.c_void_p(-1).value:
            raise OSError(ctypes.get_last_error(), "Safe read open failed")
        try:
            final = kernel.GetFinalPathNameByHandleW
            final.argtypes = [wintypes.HANDLE, wintypes.LPWSTR, wintypes.DWORD, wintypes.DWORD]
            final.restype = wintypes.DWORD
            buf = ctypes.create_unicode_buffer(32768)
            length = final(handle, buf, len(buf), 0)
            actual = buf.value
            if actual.startswith("\\\\?\\UNC\\"):
                actual = "\\\\" + actual[8:]
            elif actual.startswith("\\\\?\\"):
                actual = actual[4:]
            if (
                not length
                or length >= len(buf)
                or os.path.normcase(actual) != os.path.normcase(str(candidate))
            ):
                raise ValueError("UNSAFE_PATH: handle escaped path")
            no_links(candidate)
            fd = msvcrt.open_osfhandle(handle, os.O_RDONLY | os.O_BINARY)
            handle = None
        finally:
            if handle is not None:
                close = kernel.CloseHandle
                close.argtypes = [wintypes.HANDLE]
                close(handle)
    else:
        directory = _posix_open(root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        try:
            parts = relative.split("/")
            for part in parts[:-1]:
                child = _posix_open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=directory)
                os.close(directory)
                directory = child
            fd = _posix_open(parts[-1], os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=directory)
        finally:
            os.close(directory)
    with os.fdopen(fd, "rb") as stream:
        if not stat.S_ISREG(os.fstat(stream.fileno()).st_mode):
            raise ValueError("UNSAFE_PATH: nonregular file")
        yield stream


def transfer(source, destination=None, *, limit, expected_sha=None, expected_size=None):
    before = os.fstat(source.fileno())
    if before.st_size > limit:
        raise ValueError("RESOURCE_LIMIT")
    total, hasher = 0, hashlib.sha256()
    while chunk := source.read(min(65536, limit - total + 1)):
        total += len(chunk)
        if total > limit:
            raise ValueError("RESOURCE_LIMIT")
        hasher.update(chunk)
        if destination is not None:
            destination.write(chunk)
    after = os.fstat(source.fileno())
    if (before.st_size, before.st_mtime_ns, before.st_ctime_ns) != (
        after.st_size,
        after.st_mtime_ns,
        after.st_ctime_ns,
    ):
        raise ValueError("SOURCE_CHANGED")
    if expected_size is not None and total != expected_size:
        raise ValueError("CORRUPTION: size mismatch")
    if expected_sha is not None and hasher.hexdigest() != expected_sha:
        raise ValueError("CORRUPTION: hash mismatch")
    return hasher.hexdigest(), total


def fsync_dir(path):
    if os.name != "nt":
        fd = os.open(path, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(fd)
        finally:
            os.close(fd)
