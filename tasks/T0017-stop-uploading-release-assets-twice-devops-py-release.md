---
id: T0017
owner: ~
needs: []
branch: —
worktree: —
status: ready
started_at: —
ended_at: —
review: agent
preview: none
protocol: standard
---
# T0017: Stop uploading release assets twice: devops.py release attaches the wheel and sdist, and publish.yml uploads them again

## Goals
`devops.py release` (support-python `ReleasePipeline`) builds from the frozen version and attaches `dist/*` to the GitHub release.
`.github/workflows/publish.yml` then rebuilds and uploads the same file names on `release: published`.
Delete `publish.yml`, so the release pipeline is the single source of release assets.
support.python's own `publish.yml` has the same duplication; auth and counters.server ship only `ci.yml`.
Update `README.md`, `docs/devops.md`, the scaffold test, and CHANGELOG.md to match.
Found in the T0014 review.

Specifications: [technical-spec.md](T0017-stop-uploading-release-assets-twice-devops-py-release/technical-spec.md).
Completion check: `pytest -q`, and `grep -rn publish.yml README.md docs` finds nothing
Size estimate: 5 files, 30 lines


## Task Execution Steps
- [ ] **[Implement]** Change the scaffold test to assert `publish.yml` is absent, and record its failure.
- [ ] **[Implement]** Delete `publish.yml`.
- [ ] **[Verify]**    Run lint and the full suite; record output.
- [ ] **[Doc]**       Update `README.md`, `docs/devops.md`, and CHANGELOG.md.
- [ ] **[Review]**    Obtain review approval of the finished work before completion.

## Execution Log
- [2026-11-10] **[Doc]**
  Companion task file scaffolded at task creation.
