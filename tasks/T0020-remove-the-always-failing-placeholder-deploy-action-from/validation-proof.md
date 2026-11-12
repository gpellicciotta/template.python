# Validation Proof

## Walkthrough & Validation

### Failing regression tests
Command: `{{project-root}}/.venv/Scripts/python.exe -m pytest tests/test_scripts.py -q --timeout=30`

Exit code: 1

```text
...FF.F...                                                               [100%]
================================== FAILURES ===================================
______________ test_devops_builds_devops_cli_over_python_project ______________

    def test_devops_builds_devops_cli_over_python_project():
        cli = load_devops().build_cli()
        assert isinstance(cli, DevopsCli)
        assert isinstance(cli.project, PythonProject)
        assert Path(cli.project.root).resolve() == REPO_ROOT
>       assert cli.run(["deploy"]) == 2
E       AssertionError: assert 1 == 2
E        +  where 1 = run(['deploy'])
E        +    where run = <support_python.devops.cli.DevopsCli object at 0x000001401BE56CF0>.run

tests\test_scripts.py:58: AssertionError
---------------------------- Captured stdout call -----------------------------
Deploy version: v3.0.13-pre
Environment: production
Dry run: False
---------------------------- Captured stderr call -----------------------------
**[ERROR]** Uncommitted changes in: tests/test_scripts.py; commit or stash them before deploying.
**[ERROR]** Finished devops deploy in 0.1s with status: failed
_______________________ test_devops_help_lists_actions ________________________

    def test_devops_help_lists_actions():
        result = run_script("devops.py", "help")
        assert result.returncode == 0
        action_lines = {line.split()[0] for line in result.stdout.splitlines() if line.startswith("  ") and line.strip()}
        assert {"lint", "format", "test", "build", "check", "clean", "versions", "release"} <= action_lines
>       assert "deploy" not in action_lines
E       AssertionError: assert 'deploy' not in {'--debug', '--log-file', '--log-level', '--version', '-h,', '-v,', ...}

tests\test_scripts.py:66: AssertionError
___________________ test_devops_rejects_unconfigured_deploy ___________________

    def test_devops_rejects_unconfigured_deploy():
        result = run_script("devops.py", "deploy")
>       assert result.returncode == 2
E       AssertionError: assert 1 == 2
E        +  where 1 = CompletedProcess(args=['C:\\Dev-Projects\\template.python\\.venv\\Scripts\\python.exe', 'C:\\Dev-Projects\\template.py..._scripts.py; commit or stash them before deploying.\n**[ERROR]** Finished devops deploy in 0.1s with status: failed\n').returncode
```
```text

tests\test_scripts.py:78: AssertionError
=========================== short test summary info ===========================
FAILED tests/test_scripts.py::test_devops_builds_devops_cli_over_python_project
FAILED tests/test_scripts.py::test_devops_help_lists_actions - AssertionError...
FAILED tests/test_scripts.py::test_devops_rejects_unconfigured_deploy - Asser...
3 failed, 7 passed in 3.01s
```

### Fast suite
Command: `{{project-root}}/.venv/Scripts/python.exe -m pytest -m 'not slow' --timeout=30 -q`

Exit code: 0

```text
.....................................                                    [100%]
37 passed, 12 deselected in 3.43s
```

### Completion tests
Command: `{{project-root}}/.venv/Scripts/python.exe -m pytest tests/test_scripts.py -q --timeout=30`

Exit code: 0

```text
..........                                                               [100%]
10 passed in 2.23s
```

### Python lint
Command: `{{project-root}}/.venv/Scripts/python.exe -m ruff check scripts/devops.py tests/test_scripts.py`

Exit code: 0

```text
All checks passed!
```

### Python formatting
Command: `{{project-root}}/.venv/Scripts/python.exe -m ruff format --check scripts/devops.py tests/test_scripts.py`

Exit code: 0

```text
2 files already formatted
```

### Markdown lint
Command: `{{project-root}}/.venv/Scripts/lint-markdown.exe check README.md docs/devops.md CHANGELOG.md`

Exit code: 0

```text
All 3 markdown files passed linting.
```

### Help completion check
Command: `{{project-root}}/.venv/Scripts/python.exe scripts/devops.py help`

Exit code: 0

```text
devops v3.0.13-pre+d99d4d3 - Copyright (c) 2026 Giovanni Pellicciotta

Runs the lint, format, test, build, check, clean, versions, and release operations of this project.

Usage:
  devops lint
  devops format
  devops test [--slow] [SELECTION...] [-- RUNNER-OPTIONS...]
  devops build
  devops check
  devops clean
  devops versions
  devops release [--dry-run] [--skip-checks] [--yes]
  devops version
  devops help [--verbose]

Actions:
  lint                   check lint and formatting without changing files
  format                 reformat the sources in place
  test                   run the test suite, or a selection of it
  build                  build the distributable outputs from scratch
  check                  run lint, test, and build, stopping at the first failure
  clean                  remove build outputs
  versions               compare the version file with the CHANGELOG.md top heading
  release                freeze, tag, push, publish a GitHub release, and reopen development
  version                show version information and exit
  help                   show help message and exit (use --verbose for details)

Options:
  -h, --help             show help message and exit
  --version              show version information and exit
  -v, --verbose          enable verbose output logging
  --debug                enable debug output logging (implies --verbose)
  --log-file PATH        append operational logs to specified file
  --log-level LEVEL      logging severity threshold (DEBUG, INFO, WARN, ERROR; default: INFO)

Exit codes:
  0   success
  1   an operation failed, a prerequisite is missing, or versions drift
  2   invalid arguments or unknown action
```

