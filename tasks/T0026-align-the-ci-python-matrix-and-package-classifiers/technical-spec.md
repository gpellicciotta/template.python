### Declared Files
- .github/workflows/ci.yml
- pyproject.toml
- docs/devops.md
- README.md
- CHANGELOG.md

### Tests
- Unit test: none (configuration only; no code changes)
- Integration test: none (the CI run on every matrix version is the check, after the user pushes)

Completion check: `python -m build` succeeds locally, and CI passes on every matrix version once the user pushes.

Size estimate: 5 files, 30 lines
