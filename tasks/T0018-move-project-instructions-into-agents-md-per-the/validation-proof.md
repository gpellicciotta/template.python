# T0018: Validation Proof

## Walkthrough & Validation
`AGENTS.md` now holds the plan block, a title and summary, and the `Commands`, `Architecture`, `Project Conventions`, and `Boundaries` sections in 50 lines.
`CLAUDE.md` contains only `@AGENTS.md`.
`README.md` references and `CHANGELOG.md` were updated to match.

Command: `.venv\Scripts\lint-markdown check AGENTS.md CLAUDE.md` (exit code 0)

```text
All 2 markdown files passed linting.
```

Command: `python scripts/devops.py test` (exit code 0)

```text
Command: C:\Dev-Projects\template.python\.venv\Scripts\python.exe -m pytest -q
Process ID: 24920
............................                                             [100%]
28 passed in 1.52s
```
