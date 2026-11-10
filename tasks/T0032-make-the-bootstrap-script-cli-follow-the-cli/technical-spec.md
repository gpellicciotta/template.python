### Declared Files
- scripts/_cli_common.py
- scripts/bootstrap-dev-environment.py
- scripts/devops.py
- tests/test_scripts.py
- CHANGELOG.md

### Tests
- Unit: `-v` no longer prints the version, `--version` does, and `help --verbose` exits 0 with the exit codes listed.
- Unit: a failing bootstrap step writes its `**[ERROR]**` message to stderr.
- Integration: a subprocess run of `bootstrap-dev-environment.py help --verbose` exits 0 and prints the standard help sections.

Completion check: `python -m pytest tests/test_scripts.py` passes.

Size estimate: 5 files, 120 lines
