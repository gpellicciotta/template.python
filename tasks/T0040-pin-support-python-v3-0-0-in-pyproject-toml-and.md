---
id: T0040
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
# T0040: Pin support-python v3.0.0 in pyproject.toml and scripts/requirements.txt, and set the DevopsCli banner copyright it no longer defaults

## Goals
Needs the released support-python v3.0.0; see `docs/migration-v3.md` in support.python for the full mapping.
Pin `support-python` v3.0.0 in pyproject.toml, scripts/requirements.txt, the docs/devops.md link, and the pin tests.
Pass `copyright="Copyright (c) 2026 Giovanni Pellicciotta"` to `DevopsCli` in scripts/devops.py, since `APP_AUTHOR` and `COPYRIGHT` now default to empty.
No other v3 breaking change affects this template: it uses no `agent-files`, `lint-markdown`, crypto, or SQL APIs.

Specifications: [technical-spec.md](T0040-pin-support-python-v3-0-0-in-pyproject-toml-and/technical-spec.md).

## Task Execution Steps
- [ ] **[Implement]** Write the tests listed in the technical spec.
- [ ] **[Verify]**    Run the new tests and capture the expected failures.
- [ ] **[Implement]** Implement the change until the new tests pass.
- [ ] **[Verify]**    Run the fast suite and the completion check; record output in validation-proof.md.
- [ ] **[Doc]**       Update docs/devops.md and add a CHANGELOG.md entry.

## Execution Log
- [2026-11-11] **[Doc]**
  Task file created after reading the support-python v3.0.0 changelog and migration guide.
