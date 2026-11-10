### Declared Files
- scripts/devops.py
- tests/test_scripts.py
- .github/workflows/ci.yml
- docs/devops.md
- CHANGELOG.md

### Tests
- Unit: the project built by `build_cli(tmp_path)` fails `lint()` on a Markdown file with a lint issue and passes once it is fixed.
- Integration: `python scripts/devops.py check` passes on the repository and fails after seeding a Markdown violation.

Completion check: `python scripts/devops.py check` exits 0, and exits 1 with a seeded Markdown violation.

Size estimate: 5 files, 70 lines
