#!/usr/bin/env python3
"""Bootstraps a fresh checkout of this template: creates the virtual environment, installs scripts/requirements.txt and the
project in editable mode with the dev extra, lints, tests, and builds distributable artifacts.

Cross-platform (Windows/Linux/macOS) - replaces the old Windows-only setup.ps1. Works on both
platforms since it only calls the venv's own python/pip executables, never assumes PowerShell.

Usage:
  python scripts/bootstrap-dev-environment.py [setup] [--verbose]
  python scripts/bootstrap-dev-environment.py help [--verbose]
  python scripts/bootstrap-dev-environment.py --version

It has no `--debug`, `--log-file`, or `--log-level`: it writes no operational logs, only step headers and the steps' own
output, so it has no logging threshold to lower. `--verbose` adds each step's command line.
"""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

from typing import Optional, Sequence

from _cli_common import build_action_parser, print_error, print_help, print_version

#: Program name displayed in help and version output.
PROG = "bootstrap-dev-environment"
#: Bootstrap summary displayed in help output.
DESCRIPTION = (
    "Creates the virtual environment, installs scripts/requirements.txt and the project in editable mode, lints, tests,"
    " and builds distributable artifacts."
)
#: Usage lines displayed in help output, after the program name.
USAGE = ["[setup] [-v]", "version", "help [--verbose]"]
#: Actions and their summaries for bootstrap help.
ACTIONS = [
    ("setup", "bootstrap the development environment (default)"),
    ("version", "show version information and exit"),
    ("help", "show help message and exit (use --verbose for details)"),
]
#: Options and their summaries for bootstrap help.
OPTIONS = [
    ("-h, --help", "show help message and exit"),
    ("--version", "show version information and exit"),
    ("-v, --verbose", "print each step's command line; with help, print the detailed action descriptions"),
]
#: Exit statuses and their meanings for bootstrap help.
EXIT_CODES = [
    (0, "success"),
    (1, "one or more bootstrap steps failed"),
    (2, "invalid arguments or syntax errors"),
]
#: Detailed action descriptions displayed by `help --verbose`.
DETAILS = [
    (
        "setup",
        [
            "Runs `git init` when the checkout has no repository, and creates .venv when it is missing.",
            "Upgrades pip, installs scripts/requirements.txt and the project in editable mode with the dev extra.",
            "Runs ruff check, ruff format --check, and the fast pytest suite, then builds the sdist and wheel into dist/.",
            "Runs every step even after a failure, and reports each failure on stderr.",
        ],
    ),
    ("version", ["Prints the name, the version from pyproject.toml, and the copyright notice."]),
    ("help", ["Prints this help; with --verbose, also prints these detailed action descriptions."]),
]
#: Checkout root containing the project configuration.
REPO_ROOT = Path(__file__).resolve().parent.parent
#: Directory containing standalone development scripts and their requirements.
SCRIPTS_DIR = REPO_ROOT / "scripts"
#: Virtual environment used for project dependencies and checks.
VENV_DIR = REPO_ROOT / ".venv"
#: Output directory for built source distributions and wheels.
DIST_DIR = REPO_ROOT / "dist"


def get_project_version() -> str:
    """Resolves the current project version from pyproject.toml."""
    pyproject = REPO_ROOT / "pyproject.toml"
    if pyproject.exists():
        content = pyproject.read_text(encoding="utf-8")
        match = re.search(r'^version\s*=\s*"([^"]+)"', content, re.MULTILINE)
        if match:
            return match.group(1).strip()
    return "0.0.0+unknown"


def venv_python() -> Path:
    """Returns the path to the venv's own python executable, cross-platform."""
    if sys.platform == "win32":
        return VENV_DIR / "Scripts" / "python.exe"
    return VENV_DIR / "bin" / "python"


def run_step(description: str, args: list, verbose: bool = False) -> bool:
    """Runs one bootstrap step, printing its header, its command line when verbose, and its failure on stderr.
    Returns whether it succeeded."""
    # flush=True keeps these headers in order relative to the child's own output when stdout
    # isn't a TTY (redirected to a file/pipe) - otherwise Python fully buffers stdout and the
    # child's directly-written output can appear before these headers.
    print(f"\n[*] {description}", flush=True)
    print("=" * 60, flush=True)
    if verbose:
        print("$ " + subprocess.list2cmdline([str(arg) for arg in args]), flush=True)
    result = subprocess.run(args, cwd=str(REPO_ROOT), check=False)
    if result.returncode != 0:
        print_error(f"{description} failed (exit code {result.returncode})")
    return result.returncode == 0


def setup(verbose: bool = False) -> int:
    """Prepare the development environment, run checks, and build artifacts; return zero when all steps succeed."""

    def step(description: str, args: list) -> bool:
        return run_step(description, args, verbose)

    if not (REPO_ROOT / ".git").exists():
        step("Initializing git repository", ["git", "init"])

    all_ok = True
    if not venv_python().exists():
        all_ok &= step("Creating virtual environment", [sys.executable, "-m", "venv", str(VENV_DIR)])

    python = str(venv_python())
    all_ok &= step("Upgrading pip", [python, "-m", "pip", "install", "--upgrade", "pip"])
    all_ok &= step(
        "Installing script requirements",
        [python, "-m", "pip", "install", "-r", str(SCRIPTS_DIR / "requirements.txt")],
    )
    all_ok &= step("Installing project (editable, dev extra)", [python, "-m", "pip", "install", "-e", ".[dev]"])
    all_ok &= step("Linting (ruff check)", [python, "-m", "ruff", "check", "."])
    all_ok &= step("Checking formatting (ruff format --check)", [python, "-m", "ruff", "format", "--check", "."])
    all_ok &= step("Running unit tests (pytest)", [python, "-m", "pytest", "-q"])

    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
    all_ok &= step("Building sdist + wheel", [python, "-m", "build", "-o", str(DIST_DIR)])

    return 0 if all_ok else 1


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Dispatch setup, help, or version requests and return the corresponding exit status."""
    version = get_project_version()
    parser = build_action_parser(PROG, [name for name, _ in ACTIONS], "setup")
    args = parser.parse_args(argv)

    if args.version or args.action == "version":
        print_version(PROG, version)
        return 0
    if args.help or args.action == "help":
        print_help(PROG, version, DESCRIPTION, USAGE, ACTIONS, OPTIONS, EXIT_CODES, DETAILS if args.verbose else None)
        return 0

    return setup(args.verbose)


if __name__ == "__main__":
    sys.exit(main())
