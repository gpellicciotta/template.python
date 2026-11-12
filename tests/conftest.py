"""Isolate each test's home and detect writes to persistent state.

Python writes are blocked before mutation. Session snapshots also detect subprocess
writes to repository files and home entries, following support.python's guard pattern.
Temporary storage and pytest's own caches are excluded from snapshots.
"""

import os
from pathlib import Path
import sys

import pytest

REAL_HOME = Path.home().resolve()
REPO_ROOT = Path(__file__).resolve().parents[1]
_CACHE_NAMES = {".git", ".venv", "__pycache__", ".pytest_cache", ".ruff_cache"}


def _snapshot(root, excluded, recursive=True):
    """Record metadata without reading file contents or following directory links."""
    result = {}
    if not root.is_dir():
        return result
    for directory, names, files in os.walk(root):
        parent = Path(directory)
        names[:] = [
            name
            for name in names
            if name not in _CACHE_NAMES
            and not (parent / name).is_symlink()
            and not any((parent / name).resolve().is_relative_to(path) for path in excluded)
        ]
        if recursive:
            for name in names:
                result[str(parent / name)] = ("directory",)
        for name in files:
            path = parent / name
            if any(path.resolve().is_relative_to(item) for item in excluded):
                continue
            stat = path.lstat()
            result[str(path)] = (stat.st_mtime_ns, stat.st_size)
        if not recursive:
            for name in names:
                path = parent / name
                result[str(path)] = path.stat().st_mtime_ns
            break
    return result


@pytest.fixture(scope="session", autouse=True)
def guard_against_real_state_writes(tmp_path_factory, request):
    """Fail even when a blocked write's exception was caught by application code."""
    temporary = tmp_path_factory.getbasetemp().resolve()
    # xdist workers share a parent temporary directory; exclude every worker's tree.
    if hasattr(request.config, "workerinput"):
        temporary = temporary.parent
    excluded = (temporary,)
    before_repo = _snapshot(REPO_ROOT, excluded)
    before_home = _snapshot(REAL_HOME, excluded, recursive=False)
    violations = []
    active = True

    def audit(event, args):
        if not active:
            return
        paths = ()
        if event == "open":
            if args[2] & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND):
                paths = args[:1]
        elif event in {"os.remove", "os.rmdir", "os.mkdir", "os.chmod", "os.truncate", "os.utime"}:
            paths = args[:1]
        elif event in {"os.rename", "os.link"}:
            paths = args[:2]
        elif event == "os.symlink":
            paths = args[1:2]
        for value in paths:
            if not isinstance(value, (str, bytes, os.PathLike)):
                continue
            path = Path(os.fsdecode(value)).resolve()
            if path.is_relative_to(temporary):
                continue
            if path.is_relative_to(REPO_ROOT) and any(
                name in {"__pycache__", ".pytest_cache", ".ruff_cache"} for name in path.relative_to(REPO_ROOT).parts
            ):
                continue
            if path.is_relative_to(REAL_HOME) or path.is_relative_to(REPO_ROOT):
                violations.append(str(path))
                raise PermissionError(f"Real-state write guard blocked: {path}")

    sys.addaudithook(audit)
    try:
        yield
    finally:
        active = False
        if before_repo != _snapshot(REPO_ROOT, excluded):
            violations.append("repository working tree changed")
        if before_home != _snapshot(REAL_HOME, excluded, recursive=False):
            violations.append("real home entries changed")
        if violations:
            pytest.fail("Real-state write guard failed:\n" + "\n".join(sorted(set(violations))), pytrace=False)


@pytest.fixture(autouse=True)
def isolated_home(tmp_path, monkeypatch, guard_against_real_state_writes):
    """Give every test separate home, roaming, local, and XDG configuration paths."""
    home = tmp_path / "home"
    for name, directory in {
        "HOME": home,
        "USERPROFILE": home,
        "APPDATA": home / "AppData" / "Roaming",
        "LOCALAPPDATA": home / "AppData" / "Local",
        "XDG_CONFIG_HOME": home / ".config",
    }.items():
        directory.mkdir(parents=True, exist_ok=True)
        monkeypatch.setenv(name, str(directory))
