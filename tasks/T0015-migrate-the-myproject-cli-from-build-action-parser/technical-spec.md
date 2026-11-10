# myproject CLI on ToolHarness

## Technical Specifications
### Context
- `pyproject.toml` pins `support-python @ git+https://github.com/gpellicciotta/support.python.git@v1.0.0`.
- `src/myproject/cli.py` imports `build_action_parser`, `print_help`, and `print_version`, which v2.0.0 removed.
- support.python `docs/migration-v2.md` maps them to `ToolHarness` with `add_action`.
- Scaffolded projects copy `cli.py`, so the template's CLI is the starting point of every new project.

### Required Behavior
- `myproject`, `myproject help`, `-h`, and `--help` print the harness help and exit 0.
- `myproject help greet` prints the action help, listing `greet`'s arguments.
- `myproject version` and `--version` print `myproject v{{version}}[+{{commit}}] - Copyright (c) 2026 Giovanni Pellicciotta`.
- `myproject greet [NAME]` prints `Hello, {{NAME}}`, defaulting to `wereld`.
- `myproject greet NAME --verbose` also prints `Greeting target: {{NAME}}` and the harness startup banner.
- `myproject create PROJECT_NAME [-o DIR]` scaffolds the project and prints `Created new project at {{path}}`.
- `create` without a project name exits 2 with an error on `stderr`.
- `create` into an existing destination exits 1 with an error on `stderr`.
- An unknown action or option exits 2.

### Design Decisions
- **[Decided]** Keep `main(argv)` returning an exit code, so the console script and tests stay unchanged.
- **[Decided]** Pass `version=__version__` and the 2026 copyright notice to `ToolHarness`.
- **[Decided]** Keep `support-python` in `pyproject.toml`: the `myproject` package imports it at runtime.
- **[Decided]** Leave `scripts/` to T0014; `_cli_common.py` is a local stdlib module, not support-python.

### Tests
- Unit: `tests/test_cli.py` covers help, action help, version, greet, verbose greet, create, and every error exit code.
- Integration: after `pip install -e ".[dev]"`, `.venv/Scripts/myproject help`, `version`, and `greet Gio` behave as specified.

### Declared Files
- `pyproject.toml`
- `src/myproject/cli.py`
- `tests/test_cli.py`
- `README.md`
- `CLAUDE.md`
- `docs/requirements.md`
- `CHANGELOG.md`
