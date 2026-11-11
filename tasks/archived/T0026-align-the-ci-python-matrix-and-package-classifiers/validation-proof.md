## Walkthrough & Validation
- Raised `requires-python` to `>=3.15`, added the 3.15 classifiers, and set the CI matrix to 3.15.
- Rebuilt `.venv` with Python 3.15.2; ruff then removed the parentheses from a multi-exception `except` in scaffold.py (PEP 758).

Command: `rm -rf .venv && py -3.15 scripts/bootstrap-dev-environment.py > bootstrap-315.txt 2>&1` (first run, exit code 1)

Summary command over that output: `grep -E "^\[|passed|All checks|Successfully built template" bootstrap-315.txt` (exit code 0)

```text
[*] Creating virtual environment
[*] Upgrading pip
[*] Installing script requirements
[*] Installing project (editable, dev extra)
Successfully built template-python
[*] Linting (ruff check)
All checks passed!
[*] Checking formatting (ruff format --check)
[!] Checking formatting (ruff format --check) failed (exit code 1)
[*] Running unit tests (pytest)
28 passed in 1.56s
[*] Building sdist + wheel
Successfully built template_python-3.0.0rc0.tar.gz and template_python-3.0.0rc0-py3-none-any.whl
```

Command: `.venv/Scripts/ruff format --diff .` (exit code 1)

```text
--- src\myproject\scaffold.py
+++ src\myproject\scaffold.py
@@ -86,7 +86,7 @@
             continue
         try:
             text = path.read_text(encoding="utf-8")
-        except (UnicodeDecodeError, ValueError):
+        except UnicodeDecodeError, ValueError:
             continue
         new_text = text
         for old, new in replacements:

1 file would be reformatted, 18 files already formatted
```

Command: `py -3.15 scripts/bootstrap-dev-environment.py` (second run, exit code 0)

```text

[*] Upgrading pip
============================================================
Requirement already satisfied: pip in .\.venv\Lib\site-packages (26.3)

[... 58 lines omitted ...]
[*] Linting (ruff check)
============================================================
All checks passed!

[*] Checking formatting (ruff format --check)
============================================================
19 files already formatted

[*] Running unit tests (pytest)
============================================================
............................                                             [100%]
28 passed in 1.31s

[*] Building sdist + wheel
============================================================
* Creating isolated environment: venv+pip...
* Installing packages in isolated environment:
[... 108 lines omitted ...]
removing build\bdist.win-amd64\wheel
Successfully built template_python-3.0.0rc0.tar.gz and template_python-3.0.0rc0-py3-none-any.whl
```

Command: `.venv/Scripts/python --version && .venv/Scripts/myproject --version` (exit code 0)

```text
Python 3.15.2
myproject v3.0.0rc0+0a59a6f - Copyright (c) 2026 Giovanni Pellicciotta
```
