# Scaffold from a clone without plan data

## Technical Specifications
### Context
- `src/myproject/scaffold.py` `find_template_root` requires `pyproject.toml`, `PLAN.md`, `CHANGELOG.md`, and `src/myproject/`.
- The plan branch store keeps `PLAN.md` and `.plan/` out of the code branch; a clone has neither.
- GitHub CI run 41516752208 for 6da116c failed on `test_create_scaffolds_renamed_project`.
- In a checkout with the store, `copytree` copies `.plan/`, including the template's own `.plan/PLAN.md`, config, and protocols.
- The copied `.gitignore` ignores `.plan/` and `/PLAN.md`, so a new project would not track its fresh plan files.

### Required Behavior
- `find_template_root` accepts a directory with `pyproject.toml`, `CHANGELOG.md`, and `src/myproject/`, with or without `PLAN.md`.
- `create_project` never copies the template's `.plan/` or `plan.code-workspace`.
- The new project gets a fresh `PLAN.md` and `.plan/tasks/.gitkeep`, as today.
- The new project's `.gitignore` keeps every other line but drops `.plan/`, `/PLAN.md`, and `/plan.code-workspace`.

### Tests
- Unit: `find_template_root` finds a temporary template root that has no `PLAN.md`.
- Unit: `create_project` from a temporary root with a stale `.plan/PLAN.md`, `.plan/config/`, and `plan.code-workspace` copies none of them.
- Unit: the scaffolded `.gitignore` keeps `.venv/` and drops the three plan lines.
- Integration: on a fresh clone, `python scripts/bootstrap-dev-environment.py` passes, including `tests/test_cli.py`.

### Declared Files
- `src/myproject/scaffold.py`
- `tests/test_scaffold.py`
- `docs/requirements.md`
- `CHANGELOG.md`
