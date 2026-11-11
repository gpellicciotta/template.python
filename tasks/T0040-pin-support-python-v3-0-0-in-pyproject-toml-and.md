---
id: T0040
owner: "@claude-code"
needs: []
branch: —
worktree: —
status: completed
started_at: "2026-11-11T09:13:40Z"
ended_at: "2026-11-11T09:17:00Z"
review: none
preview: none
protocol: adhoc
completion-commit: 7f08f067fc5ee16d579c0dc74b16dbf2e7ed09c5
---
# T0040: Pin support-python v3.0.0 in pyproject.toml and scripts/requirements.txt, and set the DevopsCli banner copyright it no longer defaults

## Goals
Needs the released support-python v3.0.0; see `docs/migration-v3.md` in support.python for the full mapping.
Pin `support-python` v3.0.0 in pyproject.toml, scripts/requirements.txt, the docs/devops.md link, and the pin tests.
Pass `copyright="Copyright (c) 2026 Giovanni Pellicciotta"` to `DevopsCli` in scripts/devops.py, since `APP_AUTHOR` and `COPYRIGHT` now default to empty.
No other v3 breaking change affects this template: it uses no `agent-files`, `lint-markdown`, crypto, or SQL APIs.

Specifications: [technical-spec.md](T0040-pin-support-python-v3-0-0-in-pyproject-toml-and/technical-spec.md).

## Task Execution Steps
- [x] **[Implement]** Write the tests listed in the technical spec.
- [x] **[Verify]**    Run the new tests and capture the expected failures.
- [x] **[Implement]** Implement the change until the new tests pass.
- [x] **[Verify]**    Run the fast suite and the completion check; record output in validation-proof.md.
- [x] **[Doc]**       Update docs/devops.md and add a CHANGELOG.md entry.

## Execution Log
- [2026-11-11] **[Doc]**
  Task file created after reading the support-python v3.0.0 changelog and migration guide.

- [2026-11-11] **[Verify]**
  Pinned v3.0.0, set the devops banner copyright, added pytest-timeout and a slow marker; check passes.
  - Files touched: 7.
  - Lines touched: 32.
  - Reopenings: 0.

- [2026-11-11] **[Implement]**
  Undeclared scope: v3 check needs pytest-timeout and one slow test; T0023 keeps the rest.

- [2026-11-11] **[Doc]**
  Updated docs link and CHANGELOG entry.

- [2026-11-11] **[Complete]**
  Task completed successfully.

