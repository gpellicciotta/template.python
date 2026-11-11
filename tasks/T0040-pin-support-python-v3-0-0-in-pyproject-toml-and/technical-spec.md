### Declared Files
- pyproject.toml
- scripts/requirements.txt
- scripts/devops.py
- docs/devops.md
- tests/test_cli.py
- tests/test_scripts.py
- CHANGELOG.md

### Tests
- Unit: the pin tests expect `support.python.git@v3.0.0` in pyproject.toml and scripts/requirements.txt.
- Unit: `devops.py --version` prints the Giovanni Pellicciotta copyright banner.
- Integration: `python scripts/bootstrap-dev-environment.py` installs v3.0.0 and `python scripts/devops.py check` passes.

Completion check: `python scripts/devops.py check` exits 0 after a fresh bootstrap.

Size estimate: 7 files, 30 lines
