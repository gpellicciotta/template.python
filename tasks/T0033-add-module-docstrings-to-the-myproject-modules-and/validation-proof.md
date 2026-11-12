# Validation Evidence

## Walkthrough & Validation
Command: `& '{{primary-checkout}}/.venv/Scripts/python.exe' -m ruff check .`

Exit code: 0

```text
All checks passed!
```

Command: `& '{{primary-checkout}}/.venv/Scripts/python.exe' -m ruff format --check .`

Exit code: 0

```text
21 files already formatted
```

Command: `& '{{primary-checkout}}/.venv/Scripts/python.exe' -m pytest -m 'not slow' -q`

Exit code: 0

```text
................................                                         [100%]
32 passed, 13 deselected in 2.30s
```

Command: `& '{{primary-checkout}}/.venv/Scripts/lint-markdown.exe' check CHANGELOG.md`

Exit code: 0

```text
All 1 markdown files passed linting.
```

