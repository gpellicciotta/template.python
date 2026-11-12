# T0025 Validation Proof

## Walkthrough & Validation
- Red phase: not applicable; the task adds end-to-end coverage of existing behavior without production changes.
- First run failed on two wrong expectations: the runtime build hash in the version line and examples hidden without `--verbose`.

`python -m pytest -m slow tests/test_cli_e2e.py` (exit code 0)

```text
============================= test session starts =============================
platform win32 -- Python 3.15.2, pytest-9.2.0, pluggy-1.7.0
rootdir: C:\Dev-Projects\template.python\.plan\work\T0025-add-a-subprocess-end-to-end-test-that
configfile: pyproject.toml
plugins: timeout-2.4.0, xdist-3.8.0
timeout: 30.0s
timeout method: thread
timeout func_only: False
created: 8/8 workers
8 workers [5 items]

.....                                                                    [100%]
============================== 5 passed in 7.80s ==============================
```

`python -m pytest` (exit code 0)

```text
============================= test session starts =============================
platform win32 -- Python 3.15.2, pytest-9.2.0, pluggy-1.7.0
rootdir: C:\Dev-Projects\template.python\.plan\work\T0025-add-a-subprocess-end-to-end-test-that
configfile: pyproject.toml
testpaths: tests
plugins: timeout-2.4.0, xdist-3.8.0
timeout: 30.0s
timeout method: thread
timeout func_only: False
created: 8/8 workers
8 workers [33 items]

.................................                                        [100%]
============================= 33 passed in 4.19s ==============================
```
