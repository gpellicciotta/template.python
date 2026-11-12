# Validation Evidence

Command: `python scripts/devops.py check`; exit code: 0.

```text
Command: C:\Dev-Projects\template.python\.plan\work\T0023-split-the-tests-into-fast-and-slow-suites\.venv\Scripts\python.exe -m ruff check .
Process ID: 20428
All checks passed!
Command: C:\Dev-Projects\template.python\.plan\work\T0023-split-the-tests-into-fast-and-slow-suites\.venv\Scripts\python.exe -m ruff format --check .
Process ID: 65224
21 files already formatted
Command: C:\Dev-Projects\template.python\.plan\work\T0023-split-the-tests-into-fast-and-slow-suites\.venv\Scripts\python.exe -m pytest -q
Process ID: 81988
bringing up nodes...
bringing up nodes...
.................................                                        [100%]
33 passed in 3.77s
Command: C:\Dev-Projects\template.python\.plan\work\T0023-split-the-tests-into-fast-and-slow-suites\.venv\Scripts\python.exe -m pytest -m slow --timeout=120
Process ID: 80640
============================= test session starts =============================
platform win32 -- Python 3.15.2, pytest-9.2.0, pluggy-1.7.0
rootdir: C:\Dev-Projects\template.python\.plan\work\T0023-split-the-tests-into-fast-and-slow-suites
configfile: pyproject.toml
testpaths: tests
plugins: timeout-2.4.0, xdist-3.8.0
timeout: 120.0s
timeout method: thread
timeout func_only: False
created: 8/8 workers
8 workers [19 items]
...................                                                      [100%]
============================= 19 passed in 14.06s =============================
Command: C:\Dev-Projects\template.python\.plan\work\T0023-split-the-tests-into-fast-and-slow-suites\.venv\Scripts\python.exe -m build -o dist
Process ID: 81768
* Creating isolated environment: venv+pip...
* Installing packages in isolated environment:
  - setuptools>=77
[... 103 lines omitted ...]
adding 'template_python-3.0.14rc0.dist-info/METADATA'
adding 'template_python-3.0.14rc0.dist-info/WHEEL'
adding 'template_python-3.0.14rc0.dist-info/entry_points.txt'
adding 'template_python-3.0.14rc0.dist-info/top_level.txt'
adding 'template_python-3.0.14rc0.dist-info/RECORD'
removing build\bdist.win-amd64\wheel
Successfully built template_python-3.0.14rc0.tar.gz and template_python-3.0.14rc0-py3-none-any.whl
```

Command: `python scripts/devops.py test --slow`; exit code: 0.

```text
Command: C:\Dev-Projects\template.python\.plan\work\T0023-split-the-tests-into-fast-and-slow-suites\.venv\Scripts\python.exe -m pytest -m slow --timeout=120
Process ID: 45200
============================= test session starts =============================
platform win32 -- Python 3.15.2, pytest-9.2.0, pluggy-1.7.0
rootdir: C:\Dev-Projects\template.python\.plan\work\T0023-split-the-tests-into-fast-and-slow-suites
configfile: pyproject.toml
testpaths: tests
plugins: timeout-2.4.0, xdist-3.8.0
timeout: 120.0s
timeout method: thread
timeout func_only: False
created: 8/8 workers
8 workers [19 items]
...................                                                      [100%]
============================= 19 passed in 11.24s =============================
```

Command: `lint-markdown check README.md docs/devops.md CHANGELOG.md`; exit code: 0.

```text
All 3 markdown files passed linting.
```

The first public devops attempts failed because the worktree had no local virtual environment.
An editable installation with declared development dependencies resolved this environment prerequisite.


## Walkthrough & Validation
Failing-first command: `python -m pytest tests/test_scripts.py -k 'parallel_test_dependencies or suite_collection_selection' -q`; exit code: 1.

```text
FAILED tests/test_scripts.py::test_parallel_test_dependencies - assert False
FAILED tests/test_scripts.py::test_suite_collection_selection[selection0-test_fast-test_slow]
2 failed, 1 passed, 10 deselected in 2.72s
```

Only the verbatim failure summary is retained above.

Command: `python -m pytest`; exit code: 0.

```text
============================= test session starts =============================
platform win32 -- Python 3.15.2, pytest-9.2.0, pluggy-1.7.0
rootdir: C:\Dev-Projects\template.python\.plan\work\T0023-split-the-tests-into-fast-and-slow-suites
configfile: pyproject.toml
testpaths: tests
plugins: timeout-2.4.0, xdist-3.8.0
timeout: 30.0s
timeout method: thread
timeout func_only: False
created: 8/8 workers
8 workers [33 items]

.................................                                        [100%]
============================= 33 passed in 4.09s ==============================
```

Command: `python -m pytest -m slow --timeout=120`; exit code: 0.

```text
============================= test session starts =============================
platform win32 -- Python 3.15.2, pytest-9.2.0, pluggy-1.7.0
rootdir: C:\Dev-Projects\template.python\.plan\work\T0023-split-the-tests-into-fast-and-slow-suites
configfile: pyproject.toml
testpaths: tests
plugins: timeout-2.4.0, xdist-3.8.0
timeout: 120.0s
timeout method: thread
timeout func_only: False
created: 8/8 workers
8 workers [19 items]

...................                                                      [100%]
============================= 19 passed in 10.96s =============================
```


