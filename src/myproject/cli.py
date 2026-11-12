"""Register and run the greeting and project scaffolding CLI actions."""

from __future__ import annotations

import argparse
from email.utils import getaddresses
import importlib.metadata
from typing import Optional, Sequence

from support_python import CliLogger
from support_python.cli import ToolHarness

from . import __version__
from .core import greet
from .scaffold import ScaffoldError, ScaffoldPlan, create_project, plan_project

#: Command name used in CLI help, examples, and version output.
TOOL_NAME = "myproject"
#: Distribution whose metadata supplies the copyright holder.
DISTRIBUTION = "template-python"
#: First publication year in the copyright notice, matching LICENSE.md.
COPYRIGHT_YEAR = 2026
#: Copyright holder named when package metadata has no author.
FALLBACK_AUTHOR = f"the {DISTRIBUTION} authors"
#: Summary displayed in CLI help.
DESCRIPTION = "Sample CLI for template.python providing greeting and project scaffolding."


def read_author() -> str:
    """Return the installed distribution's author names, or `FALLBACK_AUTHOR` when metadata is unavailable."""
    try:
        metadata = importlib.metadata.metadata(DISTRIBUTION)
    except importlib.metadata.PackageNotFoundError:
        return FALLBACK_AUTHOR
    names = [metadata.get("Author") or ""]
    names += [name or address for name, address in getaddresses([metadata.get("Author-email") or ""])]
    return ", ".join(name for name in names if name) or FALLBACK_AUTHOR


def copyright_notice() -> str:
    """Return the copyright notice displayed by the CLI harness."""
    return f"Copyright (c) {COPYRIGHT_YEAR} {read_author()}"


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
    parser.add_argument("--dry-run", action="store_true", help="report the planned changes without writing anything")
    ToolHarness.add_format_option(parser)


def _emit_plan(project_name: str, plan: ScaffoldPlan, output_format: str, logger: CliLogger) -> None:
    if output_format == "json":
        logger.emit_json(
            {
                "project_name": project_name,
                "path": str(plan.destination),
                "dry_run": True,
                "template": str(plan.template_root),
                "copied": plan.copied,
                "renamed": [{"from": old, "to": new} for old, new in plan.renamed],
                "rewritten": plan.rewritten,
                "reset": plan.reset,
                "commands": plan.commands,
            }
        )
        return
    logger.emit(f"Would create new project at {plan.destination}")
    for path in plan.copied:
        logger.emit(f"Would copy: {path}")
    for old, new in plan.renamed:
        logger.emit(f"Would rename: {old} -> {new}")
    for path in plan.rewritten:
        logger.emit(f"Would rewrite: {path}")
    for path in plan.reset:
        logger.emit(f"Would reset: {path}")
    for command in plan.commands:
        logger.emit(f"Would run: {command}")


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
    """Scaffold a new project as a renamed copy of this template, or only report the planned changes."""
    logger.progress(f"Scaffolding project '{args.project_name}' into '{args.output_dir}'...")
    try:
        if args.dry_run:
            plan = plan_project(args.project_name, args.output_dir)
        else:
            destination = create_project(args.project_name, args.output_dir)
    except ScaffoldError as exc:
        logger.error(str(exc))
        return 1
    if args.dry_run:
        _emit_plan(args.project_name, plan, args.format, logger)
    elif args.format == "json":
        logger.emit_json({"project_name": args.project_name, "path": str(destination)})
    else:
        logger.emit(f"Created new project at {destination}")
    return 0


def build_harness() -> ToolHarness:
    """Build the CLI on the shared support-python action, help, version, and logging harness."""
    harness = ToolHarness(TOOL_NAME, DESCRIPTION, version=__version__, copyright=copyright_notice())
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
        "With --dry-run, lists every planned copy, rename, rewrite, reset, and command, and writes nothing.\n"
        "With --format json, prints the project name and path, or the dry-run plan, as one JSON object.\n"
        "Needs an editable install of template.python.",
        usage_suffix="PROJECT_NAME [-o DIR] [--dry-run] [--format FORMAT]",
        configure_parser=_configure_create,
    )
    harness.set_examples(
        [
            f"{TOOL_NAME} greet Gio",
            f"{TOOL_NAME} create my-app -o ../",
            f"{TOOL_NAME} create my-app -o ../ --dry-run",
            f"{TOOL_NAME} greet Gio --format json",
        ]
    )
    return harness


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Entry point for the CLI."""
    return build_harness().run(argv)


if __name__ == "__main__":
    raise SystemExit(main())
