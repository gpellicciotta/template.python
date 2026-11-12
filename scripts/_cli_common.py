"""Shared CLI boilerplate for the standalone dev scripts under scripts/ - keeps their
version/help/error output consistent with each other and with myproject's `ToolHarness`
template, per the CLI guideline, using the standard library only.
"""

from __future__ import annotations

import argparse
import sys
import tomllib
from pathlib import Path
from typing import NoReturn, Optional, Sequence

#: Project manifest supplying the copyright holder.
PYPROJECT = Path(__file__).resolve().parent.parent / "pyproject.toml"
#: First publication year in the copyright notice; matches myproject.cli.COPYRIGHT_YEAR.
COPYRIGHT_YEAR = 2026
#: Copyright holder named when the manifest has no authors; matches myproject.cli.FALLBACK_AUTHOR.
FALLBACK_AUTHOR = "the template-python authors"
#: Severity tag prefixing error messages on stderr.
ERROR_TAG = "**[ERROR]** "
#: Width of the name column in help listings.
NAME_WIDTH = 23


def print_error(message: str, *details: str) -> None:
    """Print a tagged error message to stderr, indenting each detail line under the message."""
    print(ERROR_TAG + message, file=sys.stderr, flush=True)
    for detail in details:
        print(" " * len(ERROR_TAG) + detail, file=sys.stderr, flush=True)


class ActionParser(argparse.ArgumentParser):
    """Argument parser reporting syntax errors as tagged stderr messages with exit code 2."""

    def error(self, message: str) -> NoReturn:
        print_error(message, f"Usage: {self.prog} {{{'|'.join(self.action_names)}}} [options]")
        sys.exit(2)


def build_action_parser(prog: str, actions: Sequence[str], default_action: str) -> ActionParser:
    """Build an action-oriented parser with -h/--help, --version, and -v/--verbose, so the caller
    can print the shared version/help template instead of argparse's default output."""
    parser = ActionParser(prog=prog, add_help=False)
    parser.action_names = list(actions)
    parser.add_argument("action", nargs="?", default=default_action, choices=parser.action_names)
    parser.add_argument("-h", "--help", action="store_true")
    parser.add_argument("--version", action="store_true")
    parser.add_argument("-v", "--verbose", action="store_true")
    return parser


def read_author(pyproject: Path = PYPROJECT) -> str:
    """Return the author names from pyproject.toml, or `FALLBACK_AUTHOR` when it is missing or unreadable."""
    try:
        manifest = tomllib.loads(pyproject.read_text(encoding="utf-8"))
    except OSError, tomllib.TOMLDecodeError:
        return FALLBACK_AUTHOR
    authors = manifest.get("project", {}).get("authors", [])
    return ", ".join(author.get("name") or author.get("email", "") for author in authors) or FALLBACK_AUTHOR


def copyright_notice(pyproject: Path = PYPROJECT) -> str:
    """Return the copyright notice displayed in version banners."""
    return f"Copyright (c) {COPYRIGHT_YEAR} {read_author(pyproject)}"


def print_version(prog: str, version: str) -> None:
    """Print the program name, version, and shared copyright notice."""
    print(f"{prog} v{version} - {copyright_notice()}")


def _print_section(title: str, rows: Sequence[tuple], width: int = NAME_WIDTH) -> None:
    print(f"\n{title}:")
    for name, text in rows:
        print(f"  {str(name):<{width}}{text}")


def print_help(
    prog: str,
    version: str,
    description: str,
    usage: Sequence[str],
    actions: Sequence[tuple],
    options: Sequence[tuple],
    exit_codes: Sequence[tuple],
    details: Optional[Sequence[tuple]] = None,
) -> None:
    """Print the version header, description, usage, actions, options, and exit codes, plus the
    detailed action descriptions when `details` is given (`help --verbose`)."""
    print_version(prog, version)
    print(f"\n{description}\n\nUsage:")
    for line in usage:
        print(f"  {prog} {line}")
    _print_section("Actions", actions)
    _print_section("Options", options)
    _print_section("Exit codes", exit_codes, width=4)
    if details:
        print("\nDetailed Action Descriptions:")
        for name, lines in details:
            print(f"  {name}")
            for line in lines:
                print(f"      {line}")
