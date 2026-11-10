<!-- BEGIN plan (managed by plan init) -->
This project tracks its work with plan in `PLAN.md` and `.plan/tasks/`.
Load the `plan-task-usage-guidelines` skill before creating, starting, or changing tasks.
Change `PLAN.md` and task frontmatter only through `plan` commands.
<!-- END plan -->

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

<Fill in: what this project does, who/what it's for (personal tool, library, service, ...), and any hard
invariants that must not be silently changed — e.g. "read-only, never sends/writes", "no network calls",
"single-user, no auth". State them as deliberate design decisions, not just current behavior, so a future
change doesn't casually cross them.>

## Commands

All commands use the project's venv (`.venv`, created via `python -m venv .venv` — or run
`python scripts/bootstrap-dev-environment.py` for a one-shot, cross-platform bootstrap: creates the venv,
installs editable + dev extras, runs tests, builds sdist/wheel).

- Install in editable mode, with the `dev` extra (pytest, ruff, build):
  `.venv\Scripts\pip install -e ".[dev]"`
- Lint: `.venv\Scripts\ruff check .` / `.venv\Scripts\ruff format --check .`
- Run the test suite: `.venv\Scripts\python -m pytest`
- <Add the project's actual run command(s) here, e.g. `python -m mypackage.cli <command>`, or
  `mypackage <command>` once installed — see `pyproject.toml`'s `[project.scripts]`.>

Dependencies are declared once, in `pyproject.toml` — there is no separate `requirements.txt` to keep in sync.

## Architecture

<Describe the modules/packages and what each one owns — one paragraph per module is usually enough. Name it,
state its one job, and flag anything a future change needs to respect (e.g. "the only place that parses X",
"must stay pure/dependency-free so it's testable without live credentials").>

## Development Guidelines

This repository and all projects scaffolded from this template follow the cross-project [Development Guidelines](https://github.com/gpellicciotta/dev-guidelines):

- Use semver (`MAJOR.MINOR.PATCH`). Projects scaffolded from this template start pre-1.0 (`0.x.y` — see
  `scaffold.py`'s version reset), so breaking changes are still expected early on but must be called out
  explicitly in `CHANGELOG.md` rather than reading as routine. Once a project reaches `1.0.0`, a breaking
  change requires a major version bump instead.
- Favour simplicity over ingenuity. Keep things as simple as possible for what's actually needed today — don't
  design for hypothetical future requirements.
- Minimize third-party dependencies. Reach for the standard library first; add a dependency only when it earns
  its ongoing maintenance cost.
- Make it easy to get started: a clone + `python scripts/bootstrap-dev-environment.py` (or the three commands
  under Commands above) should be enough to get a working venv, passing tests, and a build — no undocumented
  setup steps.
- Use the same tools and techniques the rest of the Python ecosystem is using (src-layout, `pyproject.toml`,
  pytest, ruff, GitHub Actions) unless there's a concrete reason to deviate — and if you deviate, say why in
  this file rather than leaving it implicit.
- CLI design: prefer action-oriented, subcommand-based CLIs (`tool action [options]`) built on `support-python`'s
  `support_python.cli.ToolHarness` (see `src/myproject/cli.py`). It provides the `help` action / `-h` / `--help`,
  `version` action / `--version`, `-v`/`--verbose`, `--debug`, `--log-file`, the standardized
  `{name} v{version} - {copyright}` header, and exit codes. Register actions with `add_action(name, summary, handler)`,
  where `handler(args, logger)` returns the exit code and writes output through the `CliLogger` it receives.
- Logging: direct operational logging to a log file and standard streams per cross-project guidelines using
  `support-python`'s `support_python.logging.CliLogger` and `LogLevel` (dual destination, `--log-file`,
  startup/completion lifecycle banners, padded severity tags, and `--debug` filtering)
  instead of reimplementing a local starter module — see `## Logging` below. `ToolHarness` already prints the
  banners for CLI actions; call `log_start`/`log_end` only in code that runs without the harness.

## Logging

Operational and CLI logging follows the cross-project [Development Guidelines](https://github.com/gpellicciotta/dev-guidelines) (`general-guidelines.md`'s Logging section). Projects scaffolded from this template inherit the `support-python` dependency (declared in `pyproject.toml`) and use `support_python.logging.CliLogger` and `LogLevel` instead of reimplementing a local starter module:

```python
import sys
from pathlib import Path
from support_python.logging import CliLogger, LogLevel

logger = CliLogger(log_path=Path("logs/app.log"), verbose=True, debug=False, origin="myproject")
logger.log_start("myproject", __version__, sys.argv, config={"output_dir": "."})
logger.info("Informational message to file and stdout")
logger.warning("Warning message to file and stderr")
logger.error("Error message to file and stderr")
logger.debug("Debug message written to file only when debug=True")
logger.log_end("Success summary")
```

Key conventions:
- Direct operational logging to a log file (`--log-file <path>`) and standard streams (`stdout`/`stderr`).
- Log startup details via `logger.log_start(name, version, argv, config)` in a standardized multi-line banner.
- Log completion summary and elapsed duration via `logger.log_end(summary)` upon exit.
- Pad severity tags to 5 characters enclosed in double asterisks and brackets (`**[ERROR]**`, `**[WARN]** `, `**[INFO]** `, `**[DEBUG]**`).
- Suppress timestamps and `INFO` severity tags when emitting to stdout.
- Discard `DEBUG` messages unless `--debug` is explicitly enabled.

## Conventions

- `CHANGELOG.md` (top-level) tracks version history: active in-development versions use a `-pre` suffix
  (`vX.Y.Z-pre`), replaced on release with a status tag (`[YYYY-MM-DD]`, `[released: YYYY-MM-DD]`, `[broken]`).
  Bump `pyproject.toml`'s `version` for every user-facing change and add a matching entry to `CHANGELOG.md`.
- `PLAN.md` (top-level) is the task index, changed only through the `plan` CLI (see `AGENTS.md`). Task files live
  under `.plan/tasks/` and are retained with `status: completed`.
- Mandatory docs: `docs/index.md`, `docs/requirements.md`, and `docs/devops.md`. Other documentation
  (design notes, ADRs, detailed specs) also lives under `docs/`.
- Keep `README.md`'s setup/usage/layout sections in sync with the code as it evolves — treat drift there as a
  bug, not a documentation nice-to-have.
- Style guide: spaces for indentation (never tabs), 4-space indent width, 132-character line length, UTF-8
  everywhere. Enforced by `.editorconfig` (editor-level) and `ruff` (`pyproject.toml`'s `[tool.ruff]`, run via
  `ruff check .` / `ruff format --check .`, wired into `scripts/bootstrap-dev-environment.py` and CI) — don't
  let either drift from these numbers.
- The package's `__version__` (`src/myproject/__init__.py`) is read from installed package metadata
  (`importlib.metadata.version(...)`) rather than hardcoded, so `pyproject.toml`'s `version` stays the single
  source of truth.
- <Add project-specific invariants/conventions here as they emerge — things a future change must not casually
  break.>

