# T0017 Validation Proof

## Walkthrough & Validation
### Failing scaffold test before deleting publish.yml
```text
$ .venv/Scripts/python -m pytest -q tests/test_cli.py
[... non-matching lines omitted ...]
E       AssertionError: assert not True
E        +  where True = exists()
E        +    where exists = (((WindowsPath('C:/Users/giova/AppData/Local/Temp/pytest-of-giova/pytest-7479/test_create_scaffolds_renamed_0/sample-app') / '.github') / 'workflows') / 'publish.yml').exists
FAILED tests/test_cli.py::test_create_scaffolds_renamed_project - AssertionEr...
1 failed, 11 passed in 0.37s
exit 1
```

### Completion check after the change
```text
$ grep -rn publish.yml README.md docs
exit 1
$ .venv/Scripts/python -m ruff check . ; ruff format --check .
All checks passed!
19 files already formatted
exit 0
$ .venv/Scripts/python -m pytest -q
............................                                             [100%]
28 passed in 1.35s
exit 0
```

### Review round 1 rework

Rewrote manual release steps 3-5: `devops.py check` empties `dist/`, the tag is pushed, and `gh release create --verify-tag` attaches only this version.

```text
$ .venv/Scripts/python -m pytest -q
............................                                             [100%]
28 passed in 1.18s
exit 0
```
