### Declared Files
- src/myproject/cli.py
- scripts/_cli_common.py
- tests/test_cli.py
- tests/test_scripts.py
- CHANGELOG.md

### Tests
- Unit: with monkeypatched package metadata, the version line names the metadata author.
- Unit: `_cli_common` reads the author from a temporary pyproject.toml.
- Integration: `myproject --version` prints `myproject v{{version}} - Copyright (c) {{year}} {{author}}` from the installed metadata.

Completion check: `python -m pytest tests/test_cli.py tests/test_scripts.py` passes.

Size estimate: 5 files, 60 lines
