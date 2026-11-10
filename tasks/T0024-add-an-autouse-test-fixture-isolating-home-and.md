---
id: T0024
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
# T0024: Add an autouse test fixture isolating HOME and configuration directories and failing on writes to real user state

## Goals
Add tests/conftest.py with an autouse fixture that redirects `HOME`, `USERPROFILE`, `APPDATA`, `LOCALAPPDATA`, and `XDG_CONFIG_HOME` to per-test `tmp_path` directories through `monkeypatch`.
Fail the session when a test writes into the real home directory or the repository working tree, for example by comparing `git status --porcelain` before and after the run.
Keep the fixture safe under pytest-xdist parallel runs.

## Task Execution Steps
- [ ] **[Implement]** Write the tests listed in the technical spec.
- [ ] **[Verify]**    Run the new tests and capture the expected failures.
- [ ] **[Implement]** Implement the change until the new tests pass.
- [ ] **[Verify]**    Run the fast suite and the completion check; record output in validation-proof.md.
- [ ] **[Doc]**       Update the affected documentation and add a CHANGELOG.md entry.

## Execution Log
- [2026-11-10] **[Doc]**
  Companion task file scaffolded at task creation.
