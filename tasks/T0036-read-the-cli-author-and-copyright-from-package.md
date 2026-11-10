---
id: T0036
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
# T0036: Read the CLI author and copyright from package metadata instead of hardcoding them in cli.py and _cli_common.py

## Goals
Derive the CLI copyright holder in src/myproject/cli.py from the installed package's author metadata through `importlib.metadata`, keeping pyproject.toml the single source of vendor metadata.
Fall back sensibly when metadata is missing, as the `0.0.0+unknown` version fallback does.
Make scripts/_cli_common.py read the author from pyproject.toml with the standard library instead of the `APP_AUTHOR` constant.
Record whether the copyright year stays a literal or moves into configuration.

## Task Execution Steps
- [ ] **[Implement]** Write the tests listed in the technical spec.
- [ ] **[Verify]**    Run the new tests and capture the expected failures.
- [ ] **[Implement]** Implement the change until the new tests pass.
- [ ] **[Verify]**    Run the fast suite and the completion check; record output in validation-proof.md.
- [ ] **[Doc]**       Update the affected documentation and add a CHANGELOG.md entry.

## Execution Log
- [2026-11-10] **[Doc]**
  Companion task file scaffolded at task creation.
