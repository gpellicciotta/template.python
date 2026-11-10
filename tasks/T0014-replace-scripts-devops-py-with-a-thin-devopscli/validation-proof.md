# T0014 Validation Proof

## Walkthrough & Validation

### Baseline: old `devops.py help`

```text
$ python scripts/devops.py help
devops v3.0.0-pre - Copyright (c) Giovanni Pellicciotta

Runs the lint, test, build, clean, release, and deploy operations of this project.

usage: devops [-h] [-v] [--dry-run] [--skip-checks]
              [{lint,test,build,check,clean,release,deploy,version,help}]

Runs the lint, test, build, clean, release, and deploy operations of this
project.

positional arguments:
  {lint,test,build,check,clean,release,deploy,version,help}
                        Action to perform

options:
  -h, --help            Show this help message and exit
  -v, --version         Show version information and exit
  --dry-run             release/deploy: print every step without making any
                        changes
  --skip-checks         release: skip pre-flight quality checks

Exit codes:
  0  Success
  1  An operation or precondition failed, or the virtual environment is missing
  2  A release step failed
exit 0
```

### Baseline: old `devops.py release --dry-run --skip-checks`

```text
$ python scripts/devops.py release --dry-run --skip-checks
Release version : v3.0.0
Next dev version: v3.0.1-pre
Dry run         : True

GitHub repo     : gpellicciotta/template.python
Release notes   : 4 lines
  - **[breaking]** CLI: Rebuilt `myproject` on the `support-python` v2.0.0 `ToolHarness`; `-v` now means `--verbose`, so use `--version`.
  - Build: Upgraded the `support-python` dependency from v1.0.0 to v2.0.0.
  - **[breaking]** DevEx: Merged `scripts/create-github-release.py` and `scripts/deploy-to-production.py` into `scripts/devops.py` as `release` and `deploy` actions.
  - **[breaking]** DevEx: Removed `scripts/install-from-github-release.py`; install releases with `pip` from the release wheel or Git tag.

--- Step 1: Finalize version ---
  [edit] CHANGELOG.md: heading -> '## v3.0.0 [released: 2026-11-10]'
  [edit] pyproject.toml: version = "3.0.0"
  $ git add CHANGELOG.md pyproject.toml
  $ git commit -m Released v3.0.0.

--- Step 2: Tag and push v3.0.0 ---
  $ git tag -f v3.0.0
  $ git push origin main
  $ git push origin v3.0.0

--- Step 3: Create GitHub release v3.0.0 ---
  $ gh release create v3.0.0 --title v3.0.0 --notes - **[breaking]** CLI: Rebuilt `myproject` on the `support-python` v2.0.0 `ToolHarness`; `-v` now means `--verbose`, so use `--version`.
- Build: Upgraded the `support-python` dependency from v1.0.0 to v2.0.0.
- **[breaking]** DevEx: Merged `scripts/create-github-release.py` and `scripts/deploy-to-production.py` into `scripts/devops.py` as `release` and `deploy` actions.
- **[breaking]** DevEx: Removed `scripts/install-from-github-release.py`; install releases with `pip` from the release wheel or Git tag.

--- Step 4: Open v3.0.1-pre ---
  [edit] CHANGELOG.md: inserted '## v3.0.1-pre' heading
  [edit] pyproject.toml: version = "3.0.1-pre"
  $ git add CHANGELOG.md pyproject.toml
  $ git commit -m Opened v3.0.1-pre development after releasing v3.0.0.
  $ git push origin main

[DRY RUN] No changes were made.
exit 0
```

### Failing tests before the implementation

```text
$ .venv/Scripts/python -m pytest -q tests/test_scripts.py
[... 214 non-matching lines omitted ...]
E           AssertionError: assert 'versions' in 'devops v3.0.0-pre - Copyright (c) Giovanni Pellicciotta\n\nRuns the lint, test, build, clean, release, and deploy ope...Success\n  1  An operation or precondition failed, or the virtual environment is missing\n  2  A release step failed\n'
E            +  where 'devops v3.0.0-pre - Copyright (c) Giovanni Pellicciotta\n\nRuns the lint, test, build, clean, release, and deploy ope...Success\n  1  An operation or precondition failed, or the virtual environment is missing\n  2  A release step failed\n' = CompletedProcess(args=['C:\\Dev-Projects\\template.python\\.venv\\Scripts\\python.exe', 'C:\\Dev-Projects\\template.py...  An operation or precondition failed, or the virtual environment is missing\n  2  A release step failed\n', stderr='').stdout
FAILED tests/test_scripts.py::test_requirements_pin_support_python_v2 - FileN...
FAILED tests/test_scripts.py::test_devops_builds_devops_cli_over_python_project
FAILED tests/test_scripts.py::test_devops_help_lists_actions - AssertionError...
FAILED tests/test_scripts.py::test_devops_deploy_refuses_pre_release_version
FAILED tests/test_scripts.py::test_devops_deploy_step_reports_missing_target
5 failed, 4 passed in 1.01s
exit 1
```

### Lint after the implementation

```text
$ .venv/Scripts/python -m ruff check . ; ruff format --check .
All checks passed!
19 files already formatted
exit 0
```

### Full suite after the implementation

```text
$ .venv/Scripts/python -m pytest -q
........................                                                 [100%]
24 passed in 1.18s
exit 0
```

### `devops.py check` in the working checkout

```text
$ python scripts/devops.py check
Command: C:\Dev-Projects\template.python\.venv\Scripts\python.exe -m ruff check .
Process ID: 28916
All checks passed!
Command: C:\Dev-Projects\template.python\.venv\Scripts\python.exe -m ruff format --check .
Process ID: 9752
19 files already formatted
Command: C:\Dev-Projects\template.python\.venv\Scripts\python.exe -m pytest -q
Process ID: 75960
........................                                                 [100%]
24 passed in 1.48s
Removing dist
[... 103 lines omitted ...]
adding 'myproject/cli.py'
adding 'myproject/core.py'
adding 'myproject/scaffold.py'
adding 'template_python-3.0.0rc0.dist-info/licenses/LICENSE.md'
adding 'template_python-3.0.0rc0.dist-info/METADATA'
adding 'template_python-3.0.0rc0.dist-info/WHEEL'
adding 'template_python-3.0.0rc0.dist-info/entry_points.txt'
adding 'template_python-3.0.0rc0.dist-info/top_level.txt'
adding 'template_python-3.0.0rc0.dist-info/RECORD'
removing build\bdist.win-amd64\wheel
Successfully built template_python-3.0.0rc0.tar.gz and template_python-3.0.0rc0-py3-none-any.whl
exit 0
```

### Integration: bootstrap on a fresh clone of the changes

The clone carried the T0014 diff as one local commit, with `origin` set to the GitHub URL.

Two `create` tests fail there because the plan branch store leaves no `PLAN.md` in a clone; T0016 tracks that pre-existing failure.

GitHub CI on `main` has failed the same way since commit 6da116c.


```text
$ python scripts/bootstrap-dev-environment.py
[... 246 non-matching lines omitted ...]
[*] Creating virtual environment
[*] Upgrading pip
Successfully installed pip-26.3
[*] Installing script requirements
Successfully installed support-python-2.0.0
[*] Installing project (editable, dev extra)
Successfully installed build-1.6.1 colorama-0.4.6 iniconfig-2.3.1 packaging-26.3 pluggy-1.7.0 pygments-2.21.0 pyproject_hooks-1.3.3 pytest-9.2.0 ruff-0.17.4 template-python-3.0.0rc0
[*] Linting (ruff check)
All checks passed!
[*] Checking formatting (ruff format --check)
[*] Running unit tests (pytest)
FAILED tests/test_cli.py::test_create_scaffolds_renamed_project - AssertionEr...
FAILED tests/test_cli.py::test_create_refuses_existing_destination - Assertio...
2 failed, 22 passed in 1.21s
[!] Running unit tests (pytest) failed (exit code 1)
[*] Building sdist + wheel
exit 1
```

### Integration: `version`, `release --dry-run`, and `deploy --dry-run` on the fresh clone

```text
$ python scripts/devops.py version
devops v3.0.0-pre+53e366e - Copyright (c) Giovanni Pellicciotta
exit 0
$ python scripts/devops.py release --dry-run --skip-checks
Release version: v3.0.0
Next version: v3.0.1-pre
Dry run: True
[dry-run] edit CHANGELOG.md: ## v3.0.0 [released: 2026-11-10]
[dry-run] edit pyproject.toml: version = "3.0.0"
[dry-run] git add CHANGELOG.md pyproject.toml
[dry-run] git commit -m "Released version 3.0.0."
[dry-run] build release assets from the frozen version
[dry-run] git tag v3.0.0
[dry-run] git push origin main
[dry-run] git push origin v3.0.0
[dry-run] gh release create v3.0.0 --title v3.0.0 --notes-file <notes-file> <built-assets>
[dry-run] edit CHANGELOG.md: ## v3.0.1-pre
[dry-run] edit pyproject.toml: version = "3.0.1-pre"
[dry-run] git add CHANGELOG.md pyproject.toml
[dry-run] git commit -m "Started version 3.0.1-pre after the 3.0.0 release."
[dry-run] git push origin main
[dry-run] No changes were made.
exit 0
$ python scripts/devops.py deploy --dry-run
Deploy version: v3.0.0-pre
Environment: production
Dry run: True
**[ERROR]** Version 3.0.0-pre is still in development; release it before deploying.
**[ERROR]** Finished devops deploy in 0.0s with status: failed
exit 1
```

### Review round 1 follow-ups: lint, suite, and help

Added the re-exec guard, the `main()` re-exec tests, git config isolation, and doc fixes.
The `main()` tests were written together with the guard, so no failing run of them was recorded.
Round 2 then made the venv child drop the guard variable before running actions.

```text
$ .venv/Scripts/python -m ruff check . ; ruff format --check .
All checks passed!
19 files already formatted
exit 0
$ .venv/Scripts/python -m pytest -q
..........................                                               [100%]
26 passed in 1.11s
exit 0
$ python scripts/devops.py help
devops v3.0.0-pre+a0d84f6 - Copyright (c) Giovanni Pellicciotta

Runs the lint, format, test, build, check, clean, versions, release, and deploy operations of this project.

[... remaining help lines omitted ...]
```
