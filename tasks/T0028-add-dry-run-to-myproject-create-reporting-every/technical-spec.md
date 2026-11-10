### Declared Files
- src/myproject/scaffold.py
- src/myproject/cli.py
- tests/test_scaffold.py
- tests/test_cli.py
- README.md
- docs/requirements.md
- CHANGELOG.md

### Tests
- Unit: a dry run of `create_project` returns the planned changes and leaves the destination absent.
- Unit: a dry run against an existing destination or an invalid project name fails as the real run does.
- Integration: `myproject create demo -o {{tmp}} --dry-run` exits 0, lists the planned changes, and leaves `{{tmp}}` empty.

Completion check: `python -m pytest tests/test_scaffold.py tests/test_cli.py` passes, including the dry-run scenarios.

Size estimate: 7 files, 200 lines
