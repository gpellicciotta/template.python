### Declared Files
- src/myproject/__init__.py
- tests/test_cli.py
- CHANGELOG.md

### Tests
- Unit: with the version `3.0.0-pre` in pyproject.toml, `myproject.__version__` equals `3.0.0-pre`, not `3.0.0rc0`.
- Unit: Preserve release versions and return `0.0.0+unknown` when distribution metadata is missing.
- Integration: Scaffold creation rewrites the shared resolver's distribution argument to the new project name.
- Integration: `myproject --version` prints `myproject v3.0.0-pre+{{hash}}` after an editable install.

Completion check: `python -m pytest tests/test_cli.py` passes and `myproject --version` shows the `-pre` form.

Size estimate: 3 files, 15 lines
