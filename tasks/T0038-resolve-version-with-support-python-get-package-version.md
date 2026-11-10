---
id: T0038
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
# T0038: Resolve __version__ with support_python.get_package_version so the CLI shows -pre instead of the rc0 form

## Goals
`myproject --version` prints `v3.0.0rc0+0a59a6f` because packaging normalizes `3.0.0-pre` to `3.0.0rc0` in installed metadata.
Resolve `__version__` in src/myproject/__init__.py with `support_python.get_package_version("template-python")`, which maps `rc0` back to `-pre` and falls back to `0.0.0+unknown`.
Make sure `create` still rewrites the distribution name in new projects.

## Task Execution Steps
- [ ] **[Implement]** Write the tests listed in the technical spec.
- [ ] **[Verify]**    Run the new tests and capture the expected failures.
- [ ] **[Implement]** Implement the change until the new tests pass.
- [ ] **[Verify]**    Run the fast suite and the completion check; record output in validation-proof.md.
- [ ] **[Doc]**       Add a CHANGELOG.md entry.

## Execution Log
- [2026-11-10] **[Doc]**
  Companion task file scaffolded at task creation.
