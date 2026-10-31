# DevOps and Operations

Practical guidance on development environment setup, testing, validation, builds, and operations for `template.python`.

---

## Prerequisites and Environment

- **Python**: Python 3.10+
- **Git**: Git 2.30+ supporting worktrees (`git worktree`)
- **Shell**: PowerShell (Windows) or POSIX shell (Linux/macOS)

---

## Setup and Development Workflows

### Initial Bootstrap (Windows/Linux/macOS)
To initialize git, create the virtual environment, install in editable mode with dev tools, lint, run tests, and build:

```bash
python scripts/bootstrap-dev-environment.py
```

### Manual Setup
```bash
# Create and activate virtual environment
python -m venv .venv

# Windows activation
.venv\Scripts\Activate.ps1

# Linux/macOS activation
source .venv/bin/activate

# Install in editable mode with dev dependencies
pip install -e ".[dev]"
```

### Task Coordination
All planned and active work is tracked in `PLAN.md` and `.plan/tasks/`, changed only through the `plan` CLI.
See `AGENTS.md` and the `plan-task-usage-guidelines` skill for the workflow.

### Common Operations
After bootstrapping, `scripts/devops.py` runs the typical operations through the virtual environment:

```bash
python scripts/devops.py lint    # ruff check + ruff format --check
python scripts/devops.py test    # pytest
python scripts/devops.py build   # sdist + wheel into dist/
python scripts/devops.py check   # lint + test + build
python scripts/devops.py clean   # remove dist/ and build/
python scripts/devops.py release # finalize, tag, push, and publish a GitHub release
python scripts/devops.py deploy  # example production deployment
```

---

## Testing and Code Quality

### Running Tests
```bash
.venv\Scripts\python -m pytest
```

### Linting and Formatting
```bash
.venv\Scripts\ruff check .
.venv\Scripts\ruff format --check .

# To automatically apply formatting and safe fixes:
.venv\Scripts\ruff check --fix .
.venv\Scripts\ruff format .
```

---

## Development and Maintenance Scripts

The root `scripts/` directory houses non-packaged development and maintenance tooling, including the
`bootstrap-dev-environment.py` and `devops.py` scripts used above. These standalone scripts remain separate from the
installable package and automated test suites. Projects such as `mail-utils` use this convention for
bootstrap scripts, roundtrip testing, and migrations.

The `deploy` action of `devops.py` is scaffolded as an example for projects derived from this template that
deploy a running service. This template itself has no deployment target, so its `deploy` action only
validates preconditions (clean git tree, finalized release version) and reports what it would do;
replace the marked section with the project's actual deployment mechanism:

```bash
python scripts/devops.py deploy --dry-run
```

### Creating a Release with `devops.py release`

The `release` action of `scripts/devops.py` automates the complete release process end-to-end:

1. Validates preconditions (clean working tree, branch is `main`, `gh` CLI installed and authenticated, no existing remote tag or release).
2. Runs pre-flight quality checks (`ruff check`, `ruff format --check`, `pytest`, `python -m build`).
3. Extracts release notes for the target version from `CHANGELOG.md`.
4. Finalizes the version in `pyproject.toml` and `CHANGELOG.md` (removing `-pre` and stamping the release date).
5. Commits the finalized release files and creates the git tag (`v<version>`).
6. Pushes the commit and tag to GitHub and creates the GitHub release.
7. Opens the next patch development version (`-pre`) in `pyproject.toml` and `CHANGELOG.md` in a follow-up commit.

```shell
# Preview the release actions without making changes
python scripts/devops.py release --dry-run

# Create and publish the release
python scripts/devops.py release

# Create and publish while skipping pre-flight checks
python scripts/devops.py release --skip-checks
```

### Purpose and Scope
Use `scripts/` for operational tasks that support developers rather than packaged library users:
- Environment bootstrapping and dev setup automation.
- Specialized test harnesses and roundtrip verification suites.
- Adhoc data migrations, database maintenance, and repair utilities.
- Test fixture generation and synthetic benchmark data creation.
- Shared internal CLI utilities supporting standalone scripts.

### Script Conventions
Follow standard project conventions when adding tools under `scripts/`:
- Keep scripts standalone and executable directly with Python.
- Structure command-line interfaces around action-oriented subcommands.
- Standardize version and help output per cross-project [CLI guidelines](https://github.com/gpellicciotta/dev-guidelines/blob/main/guidelines/general-guidelines.md#cli).
- Return explicit exit codes indicating success or failure.
- Prefix non-executable shared modules with an underscore, such as `_cli_common.py`.
- Lint and format scripts with `ruff` alongside application code.

### Execution
Run scripts directly using the virtual environment interpreter:

```bash
python scripts/<script-name>.py --help
```

---

## Build and Distribution

To build source distributions (`sdist`) and wheels (`bdist_wheel`):

```bash
python -m build
```

Built packages are written to `dist/` — `scripts/bootstrap-dev-environment.py`'s build step uses the same location.

---

## Release Process

Ongoing work accumulates under the top `CHANGELOG.md` heading while it carries a `-pre` SemVer suffix (e.g.
`## v1.3.1-pre`), which must always match `version` in `pyproject.toml` (the single source of truth) exactly,
`-pre` included.

### Automated Release
Use `scripts/devops.py release` to automate the complete release flow:

```bash
# Validate and preview release actions
python scripts/devops.py release --dry-run

# Run automated release
python scripts/devops.py release
```

The script performs the following operations:
- Verifies a clean working tree and checks that the `gh` CLI is available.
- Extracts release notes from `CHANGELOG.md` for the current version.
- Finalizes the `-pre` heading in `CHANGELOG.md` and strips `-pre` in `pyproject.toml`.
- Commits the finalized files and tags the release.
- Pushes the mainline branch and tag to `origin`.
- Creates a GitHub release using `gh release create` with the extracted release notes.
- Opens the next development version in `CHANGELOG.md` and `pyproject.toml`, then commits and pushes.

### Manual Release Steps
If releasing manually without the script:
1. Confirm the top `CHANGELOG.md` heading's version and `pyproject.toml`'s `version` already agree.
2. Freeze: replace the heading's `-pre` suffix with `[{{date}}]`, and drop `-pre` from `pyproject.toml`'s
   `version` so both again match exactly. In the same commit, add the next patch version's `## vX.Y.Z-pre`
   heading above it, but leave `pyproject.toml`'s `version` at the bare frozen version — bumping it to the next
   `-pre` now would make the following publish step publish the wrong version. Only bump `pyproject.toml` to the next
   `-pre` in the first real commit of the next dev cycle.
3. Perform a clean verification build:
   ```powershell
   .venv\Scripts\python -m pytest && .venv\Scripts\python -m build
   ```
4. Commit the changes and tag the release commit.
5. Publish a GitHub Release for the tag; `.github/workflows/publish.yml` builds distribution packages and attaches them to the release.

---

## Continuous Integration

The GitHub Actions workflow in `.github/workflows/ci.yml` runs on every push and pull request to validate:
- Python environment setup.
- Editable installation with dev dependencies.
- Code linting and formatting via `ruff`.
- Automated test suite execution via `pytest`.
- Package build via `build`.

When a release is published on GitHub, `.github/workflows/publish.yml` triggers to build sdist and wheel packages and attach them as downloadable release assets.
