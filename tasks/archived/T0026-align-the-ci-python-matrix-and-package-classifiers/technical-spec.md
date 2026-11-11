### Declared Files
- pyproject.toml
- .github/workflows/ci.yml
- docs/devops.md
- docs/requirements.md
- README.md
- CHANGELOG.md

### Tests
- Unit test: none (configuration only; no code changes)
- Integration: `python scripts/bootstrap-dev-environment.py` passes in a fresh `.venv` created with Python 3.15.

Completion check: the bootstrap passes on Python 3.15 locally, and CI passes once the user pushes.

Size estimate: 6 files, 30 lines
