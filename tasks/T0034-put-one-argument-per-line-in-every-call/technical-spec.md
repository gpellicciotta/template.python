### Declared Files
- src/myproject/cli.py
- scripts/bootstrap-dev-environment.py
- tests/test_cli.py

### Tests
- Unit test: none (formatting only; no behavior changes)
- Integration test: none (formatting only; no behavior changes)

Mechanical command: `ruff format .` after adding the trailing commas

Completion check: `ruff check .`, `ruff format --check .`, and `python -m pytest -m "not slow"` pass.

Size estimate: 3 files, 30 lines
