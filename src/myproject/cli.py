"""Register and run the greeting and project scaffolding CLI actions."""

from __future__ import annotations

import argparse
from typing import Optional, Sequence

from support_python import CliLogger
from support_python.cli import ToolHarness

from . import __version__
from .core import greet
from .scaffold import ScaffoldError, create_project

#: Command name used in CLI help, examples, and version output.
TOOL_NAME = "myproject"
#: Copyright notice displayed by the CLI harness.
COPYRIGHT = "Copyright (c) 2026 Giovanni Pellicciotta"
#: Summary displayed in CLI help.
DESCRIPTION = "Sample CLI for template.python providing greeting and project scaffolding."


def _configure_greet(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("name", nargs="?", default="world", help="name to greet (default: world)")
    ToolHarness.add_format_option(parser)


def _configure_create(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("project_name", metavar="PROJECT_NAME", help="name of the new project")
    parser.add_argument(
        "-o",
        "--output-dir",
        default=".",
        metavar="DIR",
        help="directory to create the new project under (default: .)",
    )
    ToolHarness.add_format_option(parser)


def run_greet(args: argparse.Namespace, logger: CliLogger) -> int:
    """Print a greeting for the given name."""
    logger.progress(f"Greeting target: {args.name}")
    greeting = greet(args.name)
    if args.format == "json":
        logger.emit_json({"name": args.name, "greeting": greeting})
    else:
        logger.emit(greeting)
    return 0


def run_create(args: argparse.Namespace, logger: CliLogger) -> int:
    """Scaffold a new project as a renamed copy of this template."""
    logger.progress(f"Scaffolding project '{args.project_name}' into '{args.output_dir}'...")
    try:
        destination = create_project(args.project_name, args.output_dir)
    except ScaffoldError as exc:
        logger.error(str(exc))
        return 1
    if args.format == "json":
        logger.emit_json({"project_name": args.project_name, "path": str(destination)})
    else:
        logger.emit(f"Created new project at {destination}")
    return 0


def build_harness() -> ToolHarness:
    """Build the CLI on the shared support-python action, help, version, and logging harness."""
    harness = ToolHarness(TOOL_NAME, DESCRIPTION, version=__version__, copyright=COPYRIGHT)
    harness.add_action(
        "greet",
        "print a greeting",
        run_greet,
        detail="Prints 'Hello, NAME'; NAME defaults to 'world'.\n"
        "With --verbose, also prints the greeting target.\n"
        "With --format json, prints the name and greeting as one JSON object.",
        usage_suffix="[NAME] [--format FORMAT]",
        configure_parser=_configure_greet,
    )
    harness.add_action(
        "create",
        "scaffold a new project from this template",
        run_create,
        detail="Copies this template into DIR/PROJECT_NAME, renaming the package, project, and title.\n"
        "PROJECT_NAME is the new project's name; DIR defaults to the current directory.\n"
        "With --format json, prints the project name and path as one JSON object.\n"
        "Needs an editable install of template.python.",
        usage_suffix="PROJECT_NAME [-o DIR] [--format FORMAT]",
        configure_parser=_configure_create,
    )
    harness.set_examples([f"{TOOL_NAME} greet Gio", f"{TOOL_NAME} create my-app -o ../", f"{TOOL_NAME} greet Gio --format json"])
    return harness


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Entry point for the CLI."""
    return build_harness().run(argv)


if __name__ == "__main__":
    raise SystemExit(main())
