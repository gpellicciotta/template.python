#!/usr/bin/env python3
"""Runs the typical operations of this project on support-python's DevopsCli over a PythonProject.

Run `python scripts/bootstrap-dev-environment.py` first: it creates `.venv` and installs `scripts/requirements.txt`
into it. This script re-runs itself with the `.venv` interpreter, so `python scripts/devops.py ...` works from any shell.

Usage:
  python scripts/devops.py help [--verbose]
  python scripts/devops.py check
  python scripts/devops.py release --dry-run
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Optional, Sequence

REPO_ROOT = Path(__file__).resolve().parent.parent
VENV_DIR = REPO_ROOT / ".venv"
DESCRIPTION = "Runs the lint, format, test, build, check, clean, versions, and release operations of this project."
COPYRIGHT = "Copyright (c) 2026 Giovanni Pellicciotta"
REEXEC_ENV = "DEVOPS_REEXECUTED"
BOOTSTRAP_HINT = "run `python scripts/bootstrap-dev-environment.py` first."


def venv_python() -> Path:
    """Return the venv's own python executable, cross-platform."""
    return VENV_DIR / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")


def build_cli(root: Path = REPO_ROOT) -> Any:
    """Build the devops command line: the standard DevopsCli actions."""
    from support_python.devops import DevopsCli, PythonProject

    return DevopsCli(PythonProject(root), description=DESCRIPTION, copyright=COPYRIGHT)


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Run the devops command line, re-running once with the .venv interpreter when it exists."""
    args = list(sys.argv[1:] if argv is None else argv)
    python = venv_python()
    in_venv = Path(sys.prefix).resolve() == VENV_DIR.resolve()
    reexecuted = os.environ.pop(REEXEC_ENV, None) is not None  # keep the guard out of child processes
    if python.is_file() and not in_venv and not reexecuted:
        try:
            return subprocess.call([str(python), str(Path(__file__).resolve()), *args], env={**os.environ, REEXEC_ENV: "1"})
        except OSError as exc:
            print(f"**[ERROR]** Cannot run {python}: {exc}; {BOOTSTRAP_HINT}", file=sys.stderr)
            return 1
    try:
        cli = build_cli()
    except ImportError as exc:
        print(f"**[ERROR]** {exc}; {BOOTSTRAP_HINT}", file=sys.stderr)
        return 1
    return cli.run(args)


if __name__ == "__main__":
    sys.exit(main())
