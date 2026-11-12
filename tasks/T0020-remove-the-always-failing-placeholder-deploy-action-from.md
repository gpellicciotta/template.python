---
id: T0020
owner: "@codex"
session: codex-20261112-847011
needs: []
branch: task/T0020-remove-the-always-failing-placeholder-deploy-action-from
worktree: .plan/work/T0020-remove-the-always-failing-placeholder-deploy-action-from
status: completed
started_at: "2026-11-12T09:50:06Z"
ended_at: "2026-11-12T09:53:01Z"
review: none
preview: none
protocol: adhoc
usage:
  worker: {turns: 2, duration_s: 319.8, input: 89140, output: 8404, cache_read: 1040640, cache_write: 0}
work_duration: 174.8
completion-commit: 4b7ef6a7f8bc750e16400ac2c3762a465f1c3b42
---
# T0020: Remove the always-failing placeholder deploy action from scripts/devops.py, its tests, and its docs

## Goals
Remove `no_deployment_target` and the `set_deploy` call from scripts/devops.py, since the CLI guidelines enable `deploy` only in projects that deploy.
Remove the deploy tests from tests/test_scripts.py and assert that `devops.py help` no longer lists `deploy`.
Remove the deploy documentation from scripts/devops.py, docs/devops.md, and README.md, noting that deploying projects enable it with `DevopsCli.set_deploy`.

## Task Execution Steps
- [x] **[Implement]** Write the tests listed in the technical spec.
- [x] **[Verify]**    Run the new tests and capture the expected failures.
- [x] **[Implement]** Implement the change until the new tests pass.
- [x] **[Verify]**    Run the fast suite and the completion check; record output in validation-proof.md.
- [x] **[Doc]**       Update the affected documentation and add a CHANGELOG.md entry.

## Execution Log
- [2026-11-10] **[Doc]**
  Companion task file scaffolded at task creation.

- [2026-11-12] **[Implement]**
  Removed placeholder deployment registration, implementation, obsolete tests, and advertised commands.

- [2026-11-12] **[Verify]**
  Captured three expected failures, then 37 passing fast tests and 10 passing completion tests.
  Evidence: [validation-proof.md](T0020-remove-the-always-failing-placeholder-deploy-action-from/validation-proof.md).

- [2026-11-12] **[Doc]**
  Updated deployment opt-in guidance and breaking changelog entry; repaired operations guide lint issues.

- [2026-11-12] **[Verify]**
  Python lint, formatting, Markdown lint, and help checks passed.
  Files touched: 5; lines touched: 99; reopenings: 0.

- [2026-11-12] **[Complete]**
  Task completed successfully.

