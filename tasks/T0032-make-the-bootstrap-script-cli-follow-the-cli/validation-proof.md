## Walkthrough & Validation

Interpreter: the main checkout's `.venv` Python, run from the task worktree, which has no `.venv`.

### Red Run Before Implementation
`python -m pytest tests/test_scripts.py -m "" -n 0 -q` exited 1 with 10 failed, 12 passed.

```text
E       TypeError: main() takes 0 positional arguments but 1 was given
E       AssertionError: assert '**[ERROR]** Linting failed (exit code 3)' in ''
E       TypeError: run_step() got an unexpected keyword argument 'verbose'
E       AssertionError: assert not True
E       AssertionError: usage: bootstrap-dev-environment [-h] [-v] [{setup,version,help}]
E         bootstrap-dev-environment: error: unrecognized arguments: --verbose
E       assert False
10 failed, 12 passed in 2.45s
```

### Green Runs

```text
$ python -m pytest tests/test_scripts.py
...............                                                          [100%]
============================= 15 passed in 2.05s ==============================
exit code: 0

$ python -m pytest tests/test_scripts.py -m "" -n 0 -q
......................                                                   [100%]
22 passed in 3.76s
exit code: 0

$ python -m pytest -q
.............................................................            [100%]
61 passed in 2.66s
exit code: 0

$ ruff check . && ruff format --check .
All checks passed!
22 files already formatted
exit code: 0
```

### CLI Checks

```text
$ python scripts/bootstrap-dev-environment.py -x
**[ERROR]** unrecognized arguments: -x
            Usage: bootstrap-dev-environment {setup|version|help} [options]
exit code: 2

$ python scripts/bootstrap-dev-environment.py --version
bootstrap-dev-environment v3.0.18-pre - Copyright (c) 2026 Giovanni Pellicciotta
exit code: 0

$ python scripts/bootstrap-dev-environment.py help --verbose
bootstrap-dev-environment v3.0.18-pre - Copyright (c) 2026 Giovanni Pellicciotta

Creates the virtual environment, installs scripts/requirements.txt and the project in editable mode, lints, tests, and builds distributable artifacts.

Usage:
  bootstrap-dev-environment [setup] [-v]
  bootstrap-dev-environment version
  bootstrap-dev-environment help [--verbose]

Actions:
  setup                  bootstrap the development environment (default)
  version                show version information and exit
  help                   show help message and exit (use --verbose for details)

Options:
  -h, --help             show help message and exit
  --version              show version information and exit
  -v, --verbose          print each step's command line; with help, print the detailed action descriptions

Exit codes:
  0   success
  1   one or more bootstrap steps failed
  2   invalid arguments or syntax errors

Detailed Action Descriptions:
  setup
[... 7 lines omitted ...]
exit code: 0
```

### Markdown Lint

```text
$ lint-markdown check docs/devops.md README.md CHANGELOG.md
docs\devops.md:66:20: MD018 [valid-external-links] External link 'https://github.com/gpellicciotta/support.python/blob/v3.0.0/docs/tutorials/devops-scripts.md' failed validation: HTTP 429
**[WARN]**  Found 1 lint issue across 3 files.
**[ERROR]** Finished lint-markdown check in 2.7s with status: failed
```

The only issue is an HTTP 429 rate limit on an existing link that this task did not touch.
