"""Shared CLI boilerplate for the standalone dev scripts under scripts/ - keeps their
version/help/error output consistent with each other and with myproject's `ToolHarness`
template, per the CLI guideline, using the standard library only.
"""

from __future__ import annotations

import argparse
import sys
from typing import NoReturn, Optional, Sequence

#: Copyright notice displayed in version banners; matches myproject.cli.COPYRIGHT.
COPYRIGHT = "Copyright (c) 2026 Giovanni Pellicciotta"
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


def print_version(prog: str, version: str) -> None:
    """Print the program name, version, and shared copyright notice."""
    print(f"{prog} v{version} - {COPYRIGHT}")


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
