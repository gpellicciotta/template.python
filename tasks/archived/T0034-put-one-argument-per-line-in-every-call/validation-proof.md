# Validation Proof

## Walkthrough & Validation
Command: `ruff check .`

Exit code: 0

```text
All checks passed!
```

Command: `ruff format --check .`

Exit code: 0

```text
21 files already formatted
```

Command: `python -m pytest tests/test_cli.py -m slow -q`

Exit code: 0

```text
.                                                                        [100%]
1 passed, 15 deselected in 3.90s
```

Command: `lint-markdown check CHANGELOG.md`

Exit code: 0

```text
All 1 markdown files passed linting.
```

Command:

```powershell
python -c 'import ast,pathlib,subprocess; paths=subprocess.check_output(["git","ls-files","*.py"],text=True).splitlines(); changed=[]; [(changed.append(p)) for p in paths if ast.dump(ast.parse(subprocess.check_output(["git","show",f"HEAD:{p}"],text=True))) != ast.dump(ast.parse(pathlib.Path(p).read_text(encoding="utf-8")))]; print(f"Checked {len(paths)} tracked Python files; AST changes: {changed}"); assert not changed'
```

Exit code: 0

```text
Checked 13 tracked Python files; AST changes: []
```

Command: `python -m pytest -m "not slow" -q`

Exit code: 0

```text
.....................................                                    [100%]
37 passed, 13 deselected in 37.59s
```

Command: `git diff --check`

Exit code: 0 (no output).

