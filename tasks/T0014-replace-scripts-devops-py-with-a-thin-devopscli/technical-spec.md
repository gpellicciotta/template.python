# Thin DevopsCli script for template.python

## Technical Specifications
### Context
- The dev-guidelines project setup guidelines require scripts built on support.python, with `devops.py` a thin runner on `support_python.devops`.
- support.python v2.0.0 provides `DevopsCli` and `PythonProject`; its `docs/migration-v2.md` maps the migration.
- Today `scripts/devops.py` is a 415-line hand-written CLI with `lint`, `test`, `build`, `check`, `clean`, `release`, `deploy`, `version`, and `help`.
- It carries its own release pipeline: changelog finalization, version bumps, preconditions, and GitHub release creation.
- `scripts/bootstrap-dev-environment.py` creates `.venv` and installs the project with its `[dev]` extra.
- `tests/test_scripts.py` unit-tests release helpers such as `_release_version` and `_finalize_changelog_heading`.

### Required Behavior
- `scripts/requirements.txt` pins `support-python @ git+https://github.com/gpellicciotta/support.python.git@v2.0.0`.
- `bootstrap-dev-environment.py` stays stdlib-only and installs `scripts/requirements.txt`.
- `scripts/devops.py` runs `DevopsCli(PythonProject(REPO_ROOT)).run()`, plus the placeholder `deploy` described below.
- `lint`, `test`, `build`, `check`, `clean`, `release`, `version`, and `help` keep working with equivalent results.
- `release --dry-run` prints every step without changing anything, as today.
- `deploy` keeps refusing pre-release versions and a dirty tree, and keeps failing with the "no production deployment target" message.

### Design Decisions
- **[Decided]** Install `scripts/requirements.txt` into the interpreter running the bootstrap script, as counters.server does.
- **[Decided]** Register the placeholder `deploy` with `DevopsCli.set_deploy` if it supports an empty step list, otherwise with `add_action`.
- **[Decided]** Keep `_cli_common.py` while the bootstrap script still imports it.
- **[Decided]** Keep `support-python` out of `pyproject.toml`; scripts pin it only in `scripts/requirements.txt`.

### Out of Scope
- The `ci.yml` and `publish.yml` workflows, which call `ruff`, `pytest`, and `build` directly.
- Moving the bootstrap script onto support.python, which ADR-0001 rules out.

### Tests
Author these before changing the scripts, and record their failing output:
- Unit: `tests/test_scripts.py` loads `scripts/devops.py` and asserts it builds a `DevopsCli` over a `PythonProject` rooted at the repository.
- Unit: `python scripts/devops.py help` lists `lint`, `test`, `build`, `check`, `clean`, `release`, and `deploy`.
- Unit: `python scripts/devops.py deploy` exits non-zero for a `-pre` version.
- Unit: Delete the tests of release helpers that no longer exist in the template; support.python covers them.
- Integration: On a fresh clone, `python scripts/bootstrap-dev-environment.py` creates `.venv` and installs support.python.
- Integration: `python scripts/devops.py check` passes, and `python scripts/devops.py release --dry-run` prints the steps without changes.

### Declared Files
- `scripts/devops.py`
- `scripts/bootstrap-dev-environment.py`
- `scripts/requirements.txt` (new)
- `tests/test_scripts.py`
- `docs/devops.md`
- `README.md`
- `CHANGELOG.md`
