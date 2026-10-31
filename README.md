# Template Python

A minimal example project to get Python development started quickly using the src-layout.

Includes pytest for testing, ruff for linting/formatting, build support with build/wheel, a GitHub Actions CI
workflow, and the docs/versioning conventions (`CHANGELOG.md`, `PLAN.md`, `CLAUDE.md`) following the cross-project
[Development Guidelines](https://github.com/gpellicciotta/dev-guidelines) — see `CLAUDE.md` for the details Claude Code reads to follow them automatically.

## Directory Layout

```
template.python/
  src/
    myproject/
      __init__.py
      core.py          # business logic
      cli.py           # entry point (registered in pyproject.toml's [project.scripts])
      scaffold.py      # `create` subcommand: copies + renames this template into a new project
  scripts/
    bootstrap-dev-environment.py  # one-shot bootstrap: git init, venv, editable install, lint, tests, build
    devops.py          # lint, test, build, check, and clean actions through the venv
    _cli_common.py     # shared version/help boilerplate for scripts/
  tests/
    test_core.py
    test_cli.py
  .plan/
    tasks/             # task files, Tnnnn-slug.md (retained upon completion)
  docs/
    index.md           # documentation index
    requirements.md    # high-level goals, functional & technical requirements
    devops.md          # environment prerequisites, build/test/deploy procedures
    specs/             # interface, format, and protocol specifications
    adrs/              # architectural decision records
    issues/            # root cause analysis and resolution records
  .github/
    workflows/
      ci.yml           # editable install + ruff + pytest + build, on push/PR
      publish.yml      # build and attach sdist/wheel to GitHub releases
  LICENSE.md           # MIT license
  pyproject.toml       # project metadata, dependencies, dev extra, CLI entry point, ruff config
  .gitignore 
  .editorconfig        # indent/charset/line-length, mirrors the ruff config for non-Python files/editors
  CLAUDE.md
  CHANGELOG.md         # version history with status tags - top-level
  PLAN.md              # task index (Next Milestone, Backlog) - top-level, managed with the `plan` CLI
```

The "src" layout places your package code under `src/{{package name}}/`. This prevents tests from accidentally
importing the local source tree instead of the installed package.

Benefits:
- Avoids import conflicts when running tests.
- Encourages installing the package (editable or wheel) during development.
- Widely adopted by PyPA projects and recommended for libraries.

Alternatives:
- Flat layout (package at project root): simpler for small scripts/apps but more prone to import issues during testing.
- App-specific layouts: can vary depending on project type (CLI, web app, library).

### Useful Resources
- [Development Guidelines](https://github.com/gpellicciotta/dev-guidelines)
- [Python Packaging User Guide — Packaging Projects](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
- [PyPA sampleproject (src-layout example)](https://github.com/pypa/sampleproject)
- [Real Python — Python application layouts](https://realpython.com/python-application-layouts/)
- [pytest — Good practices (tests outside application code)](https://docs.pytest.org/en/stable/goodpractices.html#tests-outside-application-code)
- [The Hitchhiker's Guide to Python — Project structure](https://docs.python-guide.org/writing/structure/)

## Quick Start (Windows/Linux/macOS)
Open a terminal in the project root and run:

```bash
python scripts/bootstrap-dev-environment.py
```

This initializes a git repo (if one doesn't already exist), creates a virtual environment, installs the
project in editable mode with the `dev` extra (pytest), runs the test suite, and builds a wheel/sdist into
`dist/`.

## Running Tests

```powershell
.venv\Scripts\python -m pytest
```

## Linting

```powershell
.venv\Scripts\ruff check .
.venv\Scripts\ruff format --check .
```

## CLI

```powershell
myproject help                 # or -h / --help (add --verbose for full option details)
myproject version              # or --version
myproject greet <name>         # sample business logic
myproject create <project-name> [-o <output-dir>]
```

`create` scaffolds a new project as a copy of this template at `<output-dir>/<project-name>` (current directory
if `-o` is omitted), automating the renames described below in **Starting a new project from this template**.
Run it from an editable install of this template (i.e. after `python scripts/bootstrap-dev-environment.py` or
`pip install -e ".[dev]"` in this repo).

## Building the Packages

For building the source and binary (i.e. wheel) distribution packages:

```powershell
python -m build
```

The built packages will be in the `dist/` directory — the same location `scripts/bootstrap-dev-environment.py`'s build step uses.

## Installation and Releases

When a release is published on GitHub, `.github/workflows/publish.yml` builds source and wheel packages,
attaching them as downloadable release assets.

### Installing from a release

Install directly from a published GitHub release wheel asset:

```bash
python -m pip install https://github.com/gpellicciotta/template.python/releases/download/vX.Y.Z/template_python-X.Y.Z-py3-none-any.whl
```

Or install directly from the Git release tag:

```bash
python -m pip install git+https://github.com/gpellicciotta/template.python.git@vX.Y.Z
```

Or declare it in downstream `pyproject.toml` dependencies:

```toml
dependencies = [
    "template-python @ git+https://github.com/gpellicciotta/template.python.git@vX.Y.Z",
]
```

## Starting a new project from this template

Preferred: run `myproject create <project-name> [-o <output-dir>]` (see **CLI** above) — it does the copy and
every rename below for you.

To do it by hand instead: copy this folder, then rename every occurrence of the placeholder names below —
they're easy to miss because nothing enforces consistency between them, and a leftover mismatch (e.g.
`pyproject.toml`'s `name` not matching the actual `src/` package directory) breaks the build/install step
silently rather than loudly:

- `src/myproject/` → `src/<your_package_name>/`
- `pyproject.toml`: `name = "template-python"` and `[project.scripts]`'s `myproject = "myproject.cli:main"`
- `tests/test_core.py`'s `from myproject...` imports
- This README's title, and `CLAUDE.md`'s placeholder sections
- `CHANGELOG.md` — replace the placeholder with your project's actual first entry once there's something real to release

Then follow **Quick Start** above to verify the rename didn't break anything before writing real code.
