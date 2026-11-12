# T0019 Validation Proof

## Walkthrough & Validation
The worktree has no `.venv`, so these commands use the primary checkout's `.venv` interpreter.
`PYTHONPATH=src` makes pytest import the worktree's `myproject` package.

### Markdown lint

```text
$ lint-markdown check docs/devops.md CHANGELOG.md
All 2 markdown files passed linting.
exit 0
```

### Fast test suite

```text
$ PYTHONPATH=src python -m pytest -q
bringing up nodes...
bringing up nodes...

.............................................................            [100%]
61 passed in 2.84s
exit 0
```
