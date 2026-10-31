from __future__ import annotations

import sys

from support_python.cli import build_action_parser, print_help, print_version

from . import __version__
from .core import greet
from .scaffold import ScaffoldError, create_project

TOOL_NAME = "myproject"
AUTHOR = "2026 Giovanni Pellicciotta"
DESCRIPTION = "Sample CLI for template.python providing greeting and project scaffolding."
ACTIONS = ["help", "version", "greet", "create"]
EXIT_CODES = [
    (0, "Success"),
    (1, "Application or command execution error"),
    (2, "Invalid command-line arguments"),
]


def build_parser():
    """Build the argument parser on top of the shared support-python action/help/version template."""
    parser = build_action_parser(TOOL_NAME, DESCRIPTION, ACTIONS, default_action="help")
    parser.add_argument("target", nargs="?", default=None, help="Name to greet ('greet'), or project name ('create')")
    parser.add_argument(
        "-o", "--output-dir", default=".", help="Directory to create the new project under (default: current directory)"
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """Entry point for the CLI."""
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return int(exc.code) if isinstance(exc.code, int) else 2

    if args.version or args.action == "version":
        print_version(TOOL_NAME, __version__, author=AUTHOR)
        return 0

    if args.help or args.action == "help":
        print_help(TOOL_NAME, __version__, DESCRIPTION, parser, exit_codes=EXIT_CODES, author=AUTHOR)
        return 0

    if args.action == "greet":
        name = args.target or "wereld"
        if args.verbose:
            print(f"Greeting target: {name}")
        print(greet(name))
        return 0

    # only "create" remains, since args.action is constrained to ACTIONS
    if not args.target:
        print("error: project_name is required for create action", file=sys.stderr)
        return 2
    if args.verbose:
        print(f"Scaffolding project '{args.target}' into '{args.output_dir}'...")
    try:
        destination = create_project(args.target, args.output_dir)
    except ScaffoldError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(f"Created new project at {destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
