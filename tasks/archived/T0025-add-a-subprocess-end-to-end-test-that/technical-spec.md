### Declared Files
- tests/test_cli_e2e.py

### Tests
- Unit test: none (tests/test_cli.py already covers the actions in-process; this task adds end-to-end coverage only)
- Integration: subprocess runs of `myproject --version`, `help`, `greet Gio`, `create demo -o {{tmp}}`, a repeated `create`, and `--bogus`.

Completion check: `python -m pytest -m slow tests/test_cli_e2e.py` passes.

Size estimate: 1 file, 80 lines
