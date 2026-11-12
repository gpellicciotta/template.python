# T0036 Validation Proof

The worktree has no `.venv`, so every command used the main checkout's interpreter at `../../../.venv/Scripts/`.
`devops.py check` refused to run there: `Virtual environment missing at {{worktree}}/.venv`.
Its lint and test steps ran directly instead; the build step was skipped because packaging is unchanged.

## Expected Failures Before Implementation
`python -m pytest tests/test_cli.py tests/test_scripts.py -q -n 0`:

```text
E       AssertionError: assert False   (x6, version line still named Giovanni Pellicciotta)
E       ImportError: cannot import name 'copyright_notice' from 'myproject.cli'
E       AttributeError: module '_cli_common' has no attribute 'read_author'   (x4)
11 failed, 41 passed, 10 deselected in 2.27s
```

## After Implementation
- `ruff check .`: `All checks passed!`
- `ruff format --check .`: `22 files already formatted`
- Fast suite, `python -m pytest`: `71 passed in 4.70s`
- Completion check, `python -m pytest tests/test_cli.py tests/test_scripts.py`: `52 passed in 4.39s`
- Slow suite, `python -m pytest -m slow`: `26 passed in 14.78s`
- `python scripts/bootstrap-dev-environment.py --version`:
  `bootstrap-dev-environment v3.0.20-pre - Copyright (c) 2026 Giovanni Pellicciotta`
- `main(["--version"])` with `PYTHONPATH=src`:
  `myproject v3.0.2-pre+462228a - Copyright (c) 2026 Giovanni Pellicciotta`

## Limits
The e2e test runs the console script installed from the main checkout, so it still runs the pre-change code.
It confirms that the `pyproject.toml` authors match the installed metadata output, not the new code path.
The in-process unit tests exercise the new code path with monkeypatched metadata.
