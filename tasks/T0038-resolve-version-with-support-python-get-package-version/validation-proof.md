# Validation Proof

## Walkthrough & Validation
Command: `C:/Dev-Projects/template.python/.venv/Scripts/python.exe -m pytest tests/test_cli.py -k package_version --timeout=30 -q`

Exit code: 1

```text
F..                                                                      [100%]
================================== FAILURES ===================================
__________________ test_package_version[3.0.0rc0-3.0.0-pre] ___________________

installed = '3.0.0rc0', expected = '3.0.0-pre'
monkeypatch = <_pytest.monkeypatch.MonkeyPatch object at 0x0000019841386190>

    @pytest.mark.parametrize("installed, expected", [("3.0.0rc0", "3.0.0-pre"), ("3.0.0", "3.0.0"), (None, "0.0.0+unknown")])
    def test_package_version(installed, expected, monkeypatch):
        def metadata_version(distribution):
            assert distribution == "template-python"
            if installed is None:
                raise importlib.metadata.PackageNotFoundError(distribution)
            return installed
[... 1 lines omitted ...]
        monkeypatch.setattr(importlib.metadata, "version", metadata_version)
>       assert runpy.run_module("myproject.__init__")["__version__"] == expected
E       AssertionError: assert '3.0.0rc0' == '3.0.0-pre'
[... 1 lines omitted ...]
E         - 3.0.0-pre
E         + 3.0.0rc0

tests\test_cli.py:28: AssertionError
=========================== short test summary info ===========================
FAILED tests/test_cli.py::test_package_version[3.0.0rc0-3.0.0-pre] - Assertio...
1 failed, 2 passed, 13 deselected in 0.58s
```

Command: `C:/Dev-Projects/template.python/.venv/Scripts/python.exe -m pytest tests/test_cli.py --timeout=120 -q`

Exit code: 1

```text
................E                                                        [100%]
=================================== ERRORS ====================================
___________________ ERROR at teardown of test_invalid_args ____________________
Real-state write guard failed:
real home entries changed
---------------------------- Captured stderr call -----------------------------
**[ERROR]** Unknown subcommand: '--invalid-option'
            Usage: myproject {help|version|greet|create} [options]
**[ERROR]** Unknown subcommand: 'unknown-action'
            Usage: myproject {help|version|greet|create} [options]
**[ERROR]** unrecognized arguments: --invalid-option
            Usage: myproject greet [NAME]
=========================== short test summary info ===========================
ERROR tests/test_cli.py::test_invalid_args - Failed: Real-state write guard f...
16 passed, 1 error in 3.33s
```

Command: `C:/Dev-Projects/template.python/.venv/Scripts/python.exe -m pytest -m 'not slow' --timeout=30 -q`

Exit code: 0

```text
...................................                                      [100%]
35 passed, 13 deselected in 1.86s
```

Command: `C:/Dev-Projects/template.python/.venv/Scripts/python.exe -m pytest tests/test_cli.py --timeout=120 -q`

Exit code: 0

```text
................                                                         [100%]
16 passed in 3.19s
```

Command: `C:/Dev-Projects/template.python/.venv/Scripts/python.exe -c "import runpy,sys; sys.path.insert(0, 'src'); sys.argv = ['myproject', '--version']; runpy.run_module('myproject.cli', run_name='__main__')"`

Exit code: 0

```text
myproject v3.0.2-pre+ad31d2d - Copyright (c) 2026 Giovanni Pellicciotta
```

Command: `C:/Dev-Projects/template.python/.venv/Scripts/python.exe -m ruff check src/myproject/__init__.py tests/test_cli.py`

Exit code: 0

```text
All checks passed!
```

Command: `C:/Dev-Projects/template.python/.venv/Scripts/python.exe -m ruff format --check src/myproject/__init__.py tests/test_cli.py`

Exit code: 0

```text
2 files already formatted
```

The first CLI suite run detected changed real-home entries; the repeated run passed without code changes.
The shared environment contains older installed template metadata; source execution confirmed normalization without changing that environment.

Command: `plan tasks validate --completion C:/Dev-Projects/template.python/.plan/tasks/T0038-resolve-version-with-support-python-get-package-version.md --project C:/Dev-Projects/template.python`

Exit code: 0

```text
All 1 task file passed validation.
```

