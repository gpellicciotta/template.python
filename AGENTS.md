<!-- BEGIN plan (managed by plan init) -->
This project tracks its work with plan in `PLAN.md` and `.plan/tasks/`.
Load the `plan-task-usage-guidelines` skill before creating, starting, or changing tasks.
Change `PLAN.md` and task frontmatter only through `plan` commands.
<!-- END plan -->

# Template Python

Template Python is the starting point for new Python projects.
It ships a `src/`-layout package with pytest, ruff, build, and GitHub Actions CI.
Its CLI and devops scripts run on [support.python](https://github.com/gpellicciotta/support.python).
The `myproject create` action copies and renames the template into a new project.
See [README.md](README.md), [requirements.md](docs/requirements.md), and [devops.md](docs/devops.md).

## Commands
- Bootstrap the venv, dependencies, lint, tests, and build: `python scripts/bootstrap-dev-environment.py`
- Run the fast tests: `python scripts/devops.py test`
- Run all checks (lint, tests, build): `python scripts/devops.py check`
- Reformat the sources: `python scripts/devops.py format`
- Lint Markdown: `.venv/Scripts/lint-markdown check {{file}}` (`.venv/bin/` on Linux and macOS)
- Start the CLI: `.venv/Scripts/myproject help` (`.venv/bin/` on Linux and macOS)

The `devops.py` script re-runs itself with the `.venv` interpreter, so plain `python` works.

## Architecture
- [cli.py](src/myproject/cli.py): `ToolHarness` CLI registering the `greet` and `create` actions.
- [core.py](src/myproject/core.py): sample business logic behind `greet`.
- [scaffold.py](src/myproject/scaffold.py): `create` action; copies the template and rewrites its placeholder names.
- [\_\_init\_\_.py](src/myproject/__init__.py): `__version__`, read from installed package metadata.
- [tests/](tests/): pytest suite for the core logic, CLI, scaffolding, and scripts.
- [bootstrap-dev-environment.py](scripts/bootstrap-dev-environment.py): stdlib-only bootstrap, sharing [\_cli\_common.py](scripts/_cli_common.py).
- [devops.py](scripts/devops.py): thin support.python `DevopsCli` runner; [requirements.txt](scripts/requirements.txt) pins its dependency.
- [docs/](docs/index.md): requirements, devops guide, specs, ADRs, and issue records.
- [ci.yml](.github/workflows/ci.yml): ruff, pytest, and build on every push and pull request.

## Project Conventions
- Keep the placeholder names `myproject`, `template-python`, `template.python`, and `Template Python` intact.
  [scaffold.py](src/myproject/scaffold.py) rewrites them literally in every text file of a new project.
- Scaffolded projects start at `0.0.1-pre` with a fresh `CHANGELOG.md`, `PLAN.md`, and `.plan/tasks/`.
- Mark breaking changes `**[breaking]**` in [CHANGELOG.md](CHANGELOG.md), even before `1.0.0`.
- Keep `.editorconfig` and `pyproject.toml`'s `[tool.ruff]` in sync: 4-space indent, 132-character lines.
- This template keeps its plan store on the orphan `plan` branch checked out at `.plan/`.
  `create` skips that store and makes new projects track their own plan files.

## Boundaries
- Never commit `.plan/` or `PLAN.md` to `main`; the `plan` CLI owns the `plan` branch.
- Never add a GitHub workflow that publishes releases; `devops.py release` is the only source of release assets.
- Never run `devops.py release` or `devops.py deploy` without explicit user approval; both push and publish.
- Never add a runtime dependency without user approval; every scaffolded project inherits it.
- Never rename a placeholder without updating [scaffold.py](src/myproject/scaffold.py) and its tests in the same change.
