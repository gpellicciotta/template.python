---
id: T0020
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
# T0020: Remove the always-failing placeholder deploy action from scripts/devops.py, its tests, and its docs

## Goals
Remove `no_deployment_target` and the `set_deploy` call from scripts/devops.py, since the CLI guidelines enable `deploy` only in projects that deploy.
Remove the deploy tests from tests/test_scripts.py and assert that `devops.py help` no longer lists `deploy`.
Remove the deploy documentation from scripts/devops.py, docs/devops.md, and README.md, noting that deploying projects enable it with `DevopsCli.set_deploy`.

## Task Execution Steps
- [ ] **[Implement]** Write the tests listed in the technical spec.
- [ ] **[Verify]**    Run the new tests and capture the expected failures.
- [ ] **[Implement]** Implement the change until the new tests pass.
- [ ] **[Verify]**    Run the fast suite and the completion check; record output in validation-proof.md.
- [ ] **[Doc]**       Update the affected documentation and add a CHANGELOG.md entry.

## Execution Log
- [2026-11-10] **[Doc]**
  Companion task file scaffolded at task creation.
