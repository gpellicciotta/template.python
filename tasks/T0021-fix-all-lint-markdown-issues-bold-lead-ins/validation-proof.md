# T0021 Validation Proof

## Walkthrough & Validation
Ran every command from the task worktree with the main checkout's `.venv` interpreter.
The worktree has no `.venv`, so `devops.py check` refused to run; its lint and test steps ran individually.

### Failing Test Before the Scaffold Fix
Command: `python -m pytest tests/test_scaffold.py -k preamble -p no:xdist -o addopts=""`, exit code 1.

```text
E       AssertionError: assert '# Versioned ...used\n\n---\n' == '# Versioned ...used\n\n---\n'
E         
E         Skipping 172 identical leading characters in diff, use -v to show
E           the top.
E         - > 
E         ?  -
E         + >
E           > Status codes used are:...
E         
E         ...Full output truncated, use '-vv' to show

tests\test_scaffold.py:27: AssertionError
=========================== short test summary info ===========================
FAILED tests/test_scaffold.py::test_fresh_changelog_keeps_the_template_preamble
====================== 1 failed, 20 deselected in 0.56s =======================
```

### Markdown Lint (Completion Check)
Command: `lint-markdown check`, with external link checks enabled, exit code 0.

```text
All 8 markdown files passed linting.
EXIT=0
```

### Ruff
Commands: `python -m ruff check .` and `python -m ruff format --check .`, both exit code 0.

```text
All checks passed!
EXIT=0
22 files already formatted
EXIT=0
```

### Fast Test Suite
Command: `python -m pytest`, exit code 0.

```text
============================= test session starts =============================
platform win32 -- Python 3.15.2, pytest-9.2.0, pluggy-1.7.0
[... 1 line omitted ...]
configfile: pyproject.toml
testpaths: tests
plugins: timeout-2.4.0, xdist-3.8.0
timeout: 30.0s
timeout method: thread
timeout func_only: False
created: 8/8 workers
8 workers [72 items]

........................................................................ [100%]
============================= 72 passed in 3.69s ==============================
EXIT=0
```

### Slow Test Suite
Command: `python -m pytest -m slow --timeout=120`, exit code 0.
A first run hit 3 teardown errors, "real home entries changed", from a concurrent write to the real home directory.
All 26 tests passed in that run too; the immediate rerun below was clean.

```text
============================= test session starts =============================
platform win32 -- Python 3.15.2, pytest-9.2.0, pluggy-1.7.0
[... 1 line omitted ...]
configfile: pyproject.toml
testpaths: tests
plugins: timeout-2.4.0, xdist-3.8.0
timeout: 120.0s
timeout method: thread
timeout func_only: False
created: 8/8 workers
8 workers [26 items]

..........................                                               [100%]
============================= 26 passed in 8.29s ==============================
EXIT=0
```
