### Declared Files
- src/myproject/cli.py
- tests/test_cli.py
- README.md
- docs/requirements.md
- CHANGELOG.md

### Tests
- Unit: `main(["greet"])` prints `Hello, world`, and `help greet` mentions the `world` default.
- Integration: `myproject greet` prints `Hello, world` and exits 0.

Completion check: `python -m pytest tests/test_cli.py` passes.

Size estimate: 4 files, 15 lines
