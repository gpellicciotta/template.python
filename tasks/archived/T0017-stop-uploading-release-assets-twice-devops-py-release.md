---
id: T0017
owner: "@claude-code"
needs: []
branch: —
worktree: —
status: completed
started_at: "2026-11-10T15:14:01Z"
ended_at: "2026-11-10T15:17:32Z"
review: agent
preview: none
protocol: standard
review_status: approved
review_round: 2
reviewed_by: "@claude-code-subagent"
completion-commit: b87682d53ed95cb6ec6ae25676044f24fc27316b
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
- [x] **[Implement]** Change the scaffold test to assert `publish.yml` is absent, and record its failure.
- [x] **[Implement]** Delete `publish.yml`.
- [x] **[Verify]**    Run lint and the full suite; record output.
- [x] **[Doc]**       Update `README.md`, `docs/devops.md`, and CHANGELOG.md.
- [x] **[Review]**    Obtain review approval of the finished work before completion.

## Execution Log
- [2026-11-10] **[Doc]**
  Companion task file scaffolded at task creation.

- [2026-11-10] **[Review]**
  Round 1 requested (mode: agent).

- [2026-11-10] **[Review]**
  Round 1 rejected by @claude-code-subagent: Manual release steps upload stale dist files and never push the tag before gh release create.

- [2026-11-10] **[Doc]**
  Rewrote manual release steps to build cleanly, push the tag, and attach only this version's packages with --verify-tag.

- [2026-11-10] **[Review]**
  Round 2 requested (mode: agent).

- [2026-11-10] **[Review]**
  Round 2 approved by @claude-code-subagent.
  - Round 2 approved; added the git commit line it noted as missing.

- [2026-11-10] **[Verify]**
  Recorded task outcomes.
  - Files touched: 5.
  - Lines touched: 55.
  - Reopenings: 0.

- [2026-11-10] **[Complete]**
  Task completed successfully.

