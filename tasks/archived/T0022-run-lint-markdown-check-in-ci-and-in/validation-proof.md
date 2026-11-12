# T0022 Validation Proof

## Expected Failure Before Implementation
Command: `.venv/Scripts/python -m pytest -q -m slow -n 0 tests/test_scripts.py -k markdown_violations`

```text
E       assert True is False
E        +  where True = lint()
E        +    where lint = <support_python.devops.projects.PythonProject object at 0x0000017EA401EBA0>.lint
1 failed, 26 deselected in 0.50s
```

## Passing After Implementation
Same command:

```text
1 passed, 26 deselected in 1.01s
```

## Completion Check: Clean Repository
Command: `python scripts/devops.py check`, exit code 0.

```text
Command: ...\.venv\Scripts\python.exe -m support_python.tools.lint_markdown check
All 8 markdown files passed linting.
Command: ...\.venv\Scripts\python.exe -m pytest -q
72 passed in 3.03s
Command: ...\.venv\Scripts\python.exe -m pytest -m slow --timeout=120
============================= 27 passed in 9.64s ==============================
Command: ...\.venv\Scripts\python.exe -m build -o dist
```

## Completion Check: Seeded Violation
Seeded `docs/seeded-violation.md` with a `*` bullet, ran `python scripts/devops.py check`, then removed the file.
Exit code 1:

```text
docs\seeded-violation.md:3:1: MD005 [dash-bullets] Non-dash bullet indicator '*' used; use '-' instead
**[WARN]**  Found 1 lint issue across 9 files.
**[ERROR]** Finished lint-markdown check in 0.8s with status: failed
**[ERROR]** Finished devops check in 1.4s with status: failed
```

## Not Verified Locally
The CI workflow change was not run on GitHub Actions; no push was made.
