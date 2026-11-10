### Declared Files
- src/myproject/scaffold.py
- tests/test_cli.py
- docs/requirements.md
- CHANGELOG.md

### Tests
- Unit: `test_create_scaffolds_renamed_project` expects `version = "0.1.0-pre"`, `## v0.1.0-pre`, and an area-prefixed first entry.
- Integration test: none (that test already runs the full `create` action against a real copy of the template)

Completion check: `python -m pytest tests/test_cli.py` passes.

Size estimate: 4 files, 20 lines
