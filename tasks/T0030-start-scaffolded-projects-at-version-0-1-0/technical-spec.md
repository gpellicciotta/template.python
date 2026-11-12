### Declared Files
- src/myproject/scaffold.py
- tests/test_cli.py
- tests/test_scaffold.py
- docs/requirements.md
- AGENTS.md
- CHANGELOG.md

### Tests
- Unit: Verify manifest reset preserves other fields and sets `0.1.0-pre`; verify the fresh changelog heading and first entry.
- Integration: Run the actual CLI create entry point against a real template copy and verify both generated files.

Completion check: `python -m pytest tests/test_cli.py tests/test_scaffold.py` passes.

Size estimate: 4 files, 20 lines
