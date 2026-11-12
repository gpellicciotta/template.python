---
id: T0024
owner: "@codex"
session: codex-20261112-b82ce9
needs: []
branch: task/T0024-add-an-autouse-test-fixture-isolating-home-and
worktree: .plan/work/T0024-add-an-autouse-test-fixture-isolating-home-and
status: active
started_at: "2026-11-12T08:48:51Z"
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
Model it on the session fixture in support.python v3.0.0, tests/conftest.py.

## Task Execution Steps
- [x] **[Implement]** Write the tests listed in the technical spec.
- [x] **[Verify]**    Run the new tests and capture the expected failures.
- [x] **[Implement]** Implement the change until the new tests pass.
- [x] **[Verify]**    Run the fast suite and the completion check; record output in validation-proof.md.
- [x] **[Doc]**       Update the affected documentation and add a CHANGELOG.md entry.

## Execution Log
- [2026-11-10] **[Doc]**
  Companion task file scaffolded at task creation.

- [2026-11-12] **[Decided]**
  Adapted support.python v3.0.0's session guard with per-test monkeypatch isolation, Python audit enforcement, and metadata snapshots.

- [2026-11-12] **[Verify]**
  Recorded five expected initial failures, then 37 passing tests serially and with two xdist workers. Ruff checks passed.

- [2026-11-12] **[Doc]**
  Updated fixture documentation, regression scenarios, validation evidence, and the changelog.
  Size note: Audit enforcement and subprocess regression scenarios exceeded the original 90-line estimate.

- [2026-11-12] **[Verify]**
  Recorded execution outcomes.
  - Files touched: 3
  - Lines touched: 191
  - Reopenings: 0

- [2026-11-12] **[Verify]**
  Task Markdown passed linting. Existing changelog entries retain four offline lint findings and one online broken-link finding.

- [2026-11-12] **[Complete]**
  Committed isolation fixtures, regression tests, and changelog as 75cb4f7. Recorded subprocess snapshot coverage limits in validation evidence.
