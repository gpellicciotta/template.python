---
id: T0030
owner: ~
needs: []
branch: —
worktree: —
status: ready
started_at: —
ended_at: —
review: none
preview: none
protocol: adhoc
---
# T0030: Start scaffolded projects at version 0.1.0-pre with an area-prefixed first CHANGELOG entry

## Goals
Reset the scaffolded pyproject.toml version to `0.1.0-pre` instead of `0.0.1-pre`, since semantic versioning starts at `0.1.0`.
Scaffold the first CHANGELOG.md heading as `## v0.1.0-pre`, with an entry in the `{{area}}: {{past-tense-outcome}}` format.
Update docs/requirements.md to match.

## Task Execution Steps
- [ ] **[Implement]** Write the tests listed in the technical spec.
- [ ] **[Verify]**    Run the new tests and capture the expected failures.
- [ ] **[Implement]** Implement the change until the new tests pass.
- [ ] **[Verify]**    Run the fast suite and the completion check; record output in validation-proof.md.
- [ ] **[Doc]**       Update the affected documentation and add a CHANGELOG.md entry.

## Execution Log
- [2026-11-10] **[Doc]**
  Companion task file scaffolded at task creation.
