### Declared Files
- pyproject.toml
- .github/workflows/ci.yml
- tests/test_scripts.py
- tests/test_cli.py
- docs/devops.md
- README.md
- CHANGELOG.md

### Tests
- Unit: Verify the dev extra declares parallel execution and timeout plugins.
- Integration: Collect temporary fast and slow examples using project defaults and an explicit slow override.
- Unit: `pytest --collect-only -q` excludes the tests marked `slow`, and `pytest -m slow --collect-only -q` selects only them.
- Integration: `pytest` and `pytest -m slow --timeout=120` both pass, and the fast suite stays under 2 minutes.

Completion check: `python -m pytest` and `python -m pytest -m slow --timeout=120` both exit 0.

Size estimate: 8 files, 120 lines

### Scope Notes
Existing CLI, scaffold, and isolation integration tests already have slow markers.
Only script subprocess tests need additional markers; no CLI or devops runner change is required.
