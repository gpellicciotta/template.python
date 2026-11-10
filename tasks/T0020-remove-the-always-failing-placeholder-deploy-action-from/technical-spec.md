### Declared Files
- scripts/devops.py
- tests/test_scripts.py
- docs/devops.md
- README.md
- CHANGELOG.md

### Tests
- Unit: `build_cli()` registers no `deploy` action, and `devops.py help` output lists no `deploy` line.
- Integration: `python scripts/devops.py deploy` exits with code 2 as an unknown action.

Completion check: `python -m pytest tests/test_scripts.py` passes and `python scripts/devops.py help` lists no `deploy` action.

Size estimate: 5 files, 80 lines
