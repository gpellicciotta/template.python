### Declared Files
- docs/tutorials/.gitkeep
- docs/index.md
- README.md
- tests/test_cli.py
- CHANGELOG.md

### Tests
- Unit: `test_create_scaffolds_renamed_project` asserts `docs/tutorials/.gitkeep` exists in the new project.
- Integration test: none (that test already runs the full `create` action against a real copy of the template)

Completion check: `python -m pytest tests/test_cli.py` passes and `lint-markdown check docs/index.md` reports no new issues.

Size estimate: 5 files, 15 lines
