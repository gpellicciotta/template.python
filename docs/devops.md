# DevOps and Operations

Practical guidance on development environment setup, testing, validation, builds, and operations for `template.python`.

---

## Development Environment
### Prerequisites
- Python 3.15 or later, the latest stable release required by the Python guidelines.
- Git 2.30 or later, supporting worktrees (`git worktree`).
- PowerShell on Windows, or a POSIX shell on Linux and macOS.
- The GitHub CLI (`gh`), authenticated, for publishing releases.

### Setup
To initialize git, create the virtual environment, install in editable mode with dev tools, lint, run tests, and build:

```bash
python scripts/bootstrap-dev-environment.py
```

Add `-v`/`--verbose` to print each step's command line; failed steps report `**[ERROR]**` lines on stderr.
Run `help --verbose` for the full help, and `--version` for the version.
The bootstrap has no `--debug`: it writes no operational logs, so it has no logging threshold to lower.

To set up the environment manually instead:

```bash
# Create and activate virtual environment
python -m venv .venv

# Windows (PowerShell) activation
.venv/Scripts/Activate.ps1

# Linux/macOS activation
source .venv/bin/activate

# Install in editable mode with dev dependencies
pip install -e ".[dev]"
```

---

## Versioning and Releasing
### Updating Versions
`version` in [pyproject.toml](../pyproject.toml) is the single source of truth for the project version.
The package reads `__version__` from the installed metadata, so no source file repeats it.
The top [CHANGELOG.md](../CHANGELOG.md) heading must match it exactly, `-pre` suffix included (e.g. `## v1.3.1-pre`).
Ongoing work accumulates under that heading until the next release.

- Patch: `plan` task completion raises the patch in both files; never edit it by hand.
- Minor or major: rename the `-pre` heading and `pyproject.toml`'s `version` together, in the same commit as the change.

Check that both versions agree:

```bash
python scripts/devops.py versions
```

### Making a Release
The `release` action of [devops.py](../scripts/devops.py) automates the complete release process end-to-end:
1. Validates preconditions: clean working tree, branch `main`, `gh` authenticated, fresh tags, no existing tag or release,
   and non-empty release notes.
2. Runs `check` (lint, test, build) as the quality check, unless `--skip-checks` is given.
3. Asks for the typed confirmation `release v{{version}}`, unless `--yes` is given.
4. Finalizes the version in `pyproject.toml` and `CHANGELOG.md` (removing `-pre` and stamping the release date) and commits.
5. Rebuilds `dist/` from the frozen version, then tags `v{{version}}`.
6. Pushes the commit and tag and creates the GitHub release with the wheel and sdist attached.
7. Opens the next patch development version (`-pre`) in `pyproject.toml` and `CHANGELOG.md`, commits, and pushes it.

```bash
# Preview the release actions without making changes
python scripts/devops.py release --dry-run

# Create and publish the release
python scripts/devops.py release

# Create and publish while skipping pre-flight checks and the confirmation
python scripts/devops.py release --skip-checks --yes
```

To release manually without the script:
1. Confirm the top `CHANGELOG.md` heading's version and `pyproject.toml`'s `version` agree:
   ```bash
   python scripts/devops.py versions
   ```
2. Freeze the version: replace the heading's `-pre` suffix with `[released: {{date}}]` (`YYYY-MM-DD`),
   and drop `-pre` from `pyproject.toml`'s `version`. Add no new `-pre` heading yet.
3. Run lint, tests, and a clean build; `build` empties `dist/` first, so it holds only this version's packages:
   ```bash
   python scripts/devops.py check
   ```
4. Commit the release on its own, tag the release commit, and push both:
   ```bash
   git commit -am "Released version {{version}}."
   git tag v{{version}}
   git push origin main v{{version}}
   ```
5. Publish a GitHub Release for the pushed tag, attaching the wheel and sdist built in step 3:
   ```bash
   gh release create v{{version}} --verify-tag dist/*-{{version}}-py3-none-any.whl dist/*-{{version}}.tar.gz
   ```
6. Reopen development in a separate commit: add the next patch `## v{{next-version}}-pre` heading above the release,
   set `pyproject.toml`'s `version` to `{{next-version}}-pre`, then commit and push:
   ```bash
   git commit -am "Started version {{next-version}}-pre after the {{version}} release."
   git push origin main
   ```

---

## Testing and Code Quality
### Running Tests
The default suite runs in parallel, excludes `slow` tests, and applies a 30-second timeout per test.

```bash
python scripts/devops.py test
# Or, with the virtual environment active:
python -m pytest
```

Run the slow suite with the virtual environment active:

```bash
python -m pytest -m slow --timeout=120
# Equivalent devops command:
python scripts/devops.py test --slow
```

Mark integration, end-to-end, subprocess, Git, browser, build, and tests exceeding five seconds with `@pytest.mark.slow`.
Keep unit tests isolated and safe for parallel execution. The fast suite should finish within two minutes.
`python scripts/devops.py check` and release checks run both suites before building.

### Linting and Formatting
With the virtual environment active:

```bash
ruff check .
ruff format --check .

# To automatically apply formatting and safe fixes:
ruff check --fix .
ruff format .
```

Lint Markdown with `lint-markdown`, configured by [.lint-markdown.json](../.lint-markdown.json):

```bash
lint-markdown check
# To fix safe formatting issues in place:
lint-markdown fix
```

---

## Common Operations
[devops.py](../scripts/devops.py) is a thin script over `support-python`'s `DevopsCli` and `PythonProject`.
`scripts/requirements.txt` pins `support-python`, and the bootstrap installs it into `.venv`.
The script re-runs itself with the `.venv` interpreter, so plain `python` works:

```bash
python scripts/devops.py help      # list every action; add --verbose for details
python scripts/devops.py lint      # ruff check + ruff format --check
python scripts/devops.py format    # ruff format
python scripts/devops.py test      # fast suite; selection: test tests/test_cli.py -- -k version
python scripts/devops.py test --slow # slow suite with 120-second per-test timeouts
python scripts/devops.py build     # sdist + wheel into dist/
python scripts/devops.py check     # lint + fast tests + slow tests + build
python scripts/devops.py clean     # remove dist/, build/, and src/*.egg-info
python scripts/devops.py versions  # compare pyproject.toml's version with the CHANGELOG.md top heading
python scripts/devops.py release   # freeze, tag, push, and publish a GitHub release
```

Add project-specific actions in `build_cli()` with `cli.add_action(name, summary, handler)`.
Projects that deploy enable deployment with `DevopsCli.set_deploy` in `build_cli()`, supplying project-local `DeployStep` actions.
The support-python [DevOps scripts tutorial][devops-tutorial] documents every option.

[devops-tutorial]: https://github.com/gpellicciotta/support.python/blob/v3.0.0/docs/tutorials/devops-scripts.md

### Task Coordination
All planned and active work is tracked in `PLAN.md` and `.plan/tasks/`, changed only through the `plan` CLI.
See [AGENTS.md](../AGENTS.md) and the `plan-task-usage-guidelines` skill for the workflow.

---

## Development and Maintenance Scripts
The root `scripts/` directory houses non-packaged development and maintenance tooling, including the
`bootstrap-dev-environment.py` and `devops.py` scripts used above. These standalone scripts remain separate from the
installable package and automated test suites.

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
- Standardize version and help output per cross-project [DevOps scripts tutorial][devops-tutorial].
- Return explicit exit codes indicating success or failure.
- Prefix non-executable shared modules with an underscore, such as `_cli_common.py`.
- Lint and format scripts with `ruff` alongside application code.

### Execution
Run scripts directly using the virtual environment interpreter:

```bash
python scripts/{{script-name}}.py --help
```

---

## Build and Distribution
To build source distributions (`sdist`) and wheels (`bdist_wheel`):

```bash
python -m build
```

Built packages are written to `dist/` — [bootstrap-dev-environment.py](../scripts/bootstrap-dev-environment.py)'s build step uses the same location.

---

## Continuous Integration
The GitHub Actions workflow in [ci.yml](../.github/workflows/ci.yml) runs on every push and pull request to validate:
- Python environment setup.
- Editable installation with dev dependencies.
- Code linting and formatting via `ruff`.
- Separate fast and slow suite execution via `pytest`, with 30-second and 120-second per-test timeouts.
- Package build via `build`.

No workflow runs on release: `devops.py release` attaches the wheel and sdist itself.
