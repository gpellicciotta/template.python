# Single source of release assets

## Technical Specifications
### Design Decisions
- **[Decided]** Keep the `ReleasePipeline` assets and drop `publish.yml`.
  The pipeline builds after the version freeze and attaches the outputs before anyone can see the release.
  support-python and the other sibling projects publish this way, too.

### Tests
- Unit: the `create` scaffold test asserts the new project has no `.github/workflows/publish.yml` but keeps `ci.yml`.
- Integration test: none (a real release would publish to GitHub; `release --dry-run` already lists the asset upload)

### Declared Files
- `.github/workflows/publish.yml` (deleted)
- `tests/test_cli.py`
- `README.md`
- `docs/devops.md`
- `CHANGELOG.md`

Completion check: `pytest -q`, and `grep -rn publish.yml README.md docs` finds nothing
