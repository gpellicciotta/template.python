# T0016 Validation Proof

## Walkthrough & Validation

### Failing tests before the fix

```text
$ .venv/Scripts/python -m pytest -q tests/test_scaffold.py
[... 50 non-matching lines omitted ...]
E       myproject.scaffold.ScaffoldError: Could not locate the template project root (expected pyproject.toml, PLAN.md, CHANGELOG.md and src/myproject/ in a parent directory). `create` must be run against an editable install of template.python.
E       AssertionError: assert not True
FAILED tests/test_scaffold.py::test_find_template_root_without_plan_md - mypr...
FAILED tests/test_scaffold.py::test_create_project_skips_template_plan_store
2 failed, 2 passed in 0.22s
exit 1
```

### Lint and full suite after the fix

```text
$ .venv/Scripts/python -m ruff check . ; ruff format --check .
All checks passed!
19 files already formatted
exit 0
$ .venv/Scripts/python -m pytest -q
............................                                             [100%]
28 passed in 1.30s
exit 0
```

### Integration: bootstrap on a fresh clone with the T0016 diff

The clone has no `PLAN.md` or `.plan/`, as on GitHub; before the fix, two `create` tests failed there (see T0014's proof).


```text
$ python scripts/bootstrap-dev-environment.py   # fresh clone with the T0016 diff
[... 212 non-matching lines omitted ...]
[*] Creating virtual environment
[*] Upgrading pip
[*] Installing script requirements
Successfully built support-python
[*] Installing project (editable, dev extra)
Successfully built template-python
[*] Linting (ruff check)
All checks passed!
[*] Checking formatting (ruff format --check)
[*] Running unit tests (pytest)
28 passed in 1.59s
[*] Building sdist + wheel
Successfully built template_python-3.0.0rc0.tar.gz and template_python-3.0.0rc0-py3-none-any.whl
exit 0
```

### Integration: scaffold from the fresh clone; git tracks the new plan files

```text
$ .venv/Scripts/myproject create demo-app -o ../t16-out
Created new project at C:\Users\giova\AppData\Local\Temp\claude\7cea8c64eae46762\06e26aed-76a0-4418-bcd5-3bab1733df95\scratchpad\t16-out\demo-app
exit 0
$ git init -q && git add -A && git status --short | grep -i plan
A  .plan/tasks/.gitkeep
A  PLAN.md
$ python scripts/devops.py --version   # no .venv yet; global python has support-python 1.0.0
[!] cannot import name 'DeployStep' from 'support_python.devops' (C:\Users\giova\AppData\Roaming\Python\Python312\site-packages\support_python\devops.py); run `python scripts/bootstrap-dev-environment.py` first.
exit 1
```

### Review round 1 follow-ups

Added nested `.plan` and CRLF cases, a real-template `.gitignore` check, and doc fixes; simplified the tasks dir helper.

```text
$ .venv/Scripts/python -m ruff check . ; ruff format --check .
All checks passed!
19 files already formatted
exit 0
$ .venv/Scripts/python -m pytest -q
............................                                             [100%]
28 passed in 1.48s
exit 0
```
