### Declared Files
- AGENTS.md
- src/myproject/scaffold.py
- tests/test_scaffold.py
- tests/test_cli.py
- README.md
- docs/requirements.md
- CHANGELOG.md

### Tests
- Unit: missing Git raises ScaffoldError before creating the destination.
- Integration: a failing fake plan commits real Git objects first; cleanup removes the destination and raises ScaffoldError.
- Integration: select a working installed plan launcher from PATH under the isolated home without changing PYTHONPATH.
- Unit: with a fake `plan` executable on `PATH`, `create_project` runs `plan init --store branch` in the destination.
- Unit: without `plan` on `PATH`, `create_project` raises `ScaffoldError` and removes the destination.
- Integration: with plan installed, `myproject create demo -o {{tmp}}` yields a `plan` branch at `.plan/`, an ignored PLAN.md link, and a working `plan tasks list`; mark it `slow` and skip it without plan.

Completion check: `python -m pytest tests/test_scaffold.py tests/test_cli.py` passes, and the integration scenario passes with plan installed.

Size estimate: 6 files, 200 lines
