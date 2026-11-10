### Declared Files
- src/myproject/cli.py
- tests/test_cli.py
- README.md
- docs/requirements.md
- CHANGELOG.md

### Tests
- Unit: `main(["greet", "Gio", "--format", "json"])` prints one parsable JSON document holding the greeting.
- Unit: `create --format json` prints one JSON document holding the destination path; `--format xml` exits with code 2.
- Integration: `myproject create demo -o {{tmp}} --format json --verbose` prints only JSON on stdout and the log entries on stderr.

Completion check: `python -m pytest tests/test_cli.py` passes, including the `--format json` scenarios.

Size estimate: 5 files, 120 lines
