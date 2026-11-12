---
task: T0029
round: 1
verdict: rejected
reviewer: "@claude"
reviewed_at: 2026-11-12T09:05:52Z
reviewed_commit: "10a9db5"
base_commit: "4c31af9"
branch: task/T0029-make-myproject-create-initialize-the-new-project-s
---
# Review Findings: Task T0029 (Round 1)

## Summary
The core change works.
`create` runs `git init` and `plan init --store branch`, keeps the ignore rules, and leaves one managed AGENTS.md block.
A manual `create demo` run confirmed the `plan` branch at `.plan/`, the ignored `PLAN.md`, and a single block.
Verification results:
- Fast suite: 31 passed.
- Ruff check and format: clean.
- Full suite with `PYTHONPATH` set to the plan source checkout: 43 passed.
- Completion check without that override: the CLI integration test fails.

Rejected for one failing completion check, one cleanup bug, and stale project instructions.

## Defects
1. The integration test fails on the task's own completion command.
   - `python -m pytest tests/test_scaffold.py tests/test_cli.py` gives 1 failed, 21 passed.
   - Failing test: `test_create_scaffolds_renamed_project`.
   - `tests/test_cli.py` calls `subprocess.run(["plan", "tasks", "list"], ...)` with the bare name.
   - On Windows, `CreateProcess` resolves that bare name to `AppData/Roaming/Python/Python312/Scripts/plan.exe`.
   - That launcher needs the user site, which the isolated `APPDATA` hides, so it fails with `ModuleNotFoundError: No module named 'plan'`.
   - `scaffold.py` resolves `plan` with `shutil.which`, which finds the working `~/bin/plan.cmd`.
   - So `create` passes while the test's own `plan` call fails.
   - The validation proof hid this by setting `PYTHONPATH=C:/Dev-Projects/plan/src`.
2. Cleanup after a failed init can crash and leave a half-created project, which breaks the "no half-created project" goal.
   - `_initialize_plan_store` calls `shutil.rmtree(destination)` once `git init` or `plan init` has failed.
   - On Windows, Git makes its object files read-only.
   - Reproduced on Python 3.15: `rmtree` on a repo with one commit raises `PermissionError: [WinError 5]`.
   - `plan init --store branch` commits to the `plan` branch before its later steps (worktree add, link, AGENTS.md).
   - If one of those later steps fails, cleanup raises an uncaught `PermissionError` instead of `ScaffoldError` and leaves the directory.
   - The unit tests miss this because they mock `subprocess.run`, so no Git objects exist.
3. AGENTS.md still describes the old behavior, and every scaffolded project inherits it.
   - Line 43 says "`create` skips that store and makes new projects track their own plan files".
   - New projects now ignore their plan files and keep them on a `plan` branch.
   - Line 39's "fresh `CHANGELOG.md`, `PLAN.md`, and `.plan/tasks/`" should say `plan init` creates them.

## Process Gaps
- The validation proof's green run depends on an undocumented, machine-specific `PYTHONPATH`.
  The "Completion check passed" log entry overstates the result without that override.
- No test covers the missing-`git` branch of `create_project`, only the missing-`plan` branch.
- Minor: `tests/test_cli.py` and `tests/test_scaffold.py` put stdlib imports after third-party imports, unsorted.

## Required Rework
1. Run every `plan` and `git` call in the tests through `shutil.which(...)`, like the production code.
   - The completion command must pass with no extra environment.
   - Re-record the validation proof without the `PYTHONPATH` override.
2. Make the failure cleanup remove read-only files.
   - For example, pass an `onexc` handler to `shutil.rmtree` that clears the read-only bit and retries.
   - Add a test where a real `git init` plus a commit is followed by a failing fake `plan`.
   - Assert that the result is `ScaffoldError` and that the destination is gone.
3. Update AGENTS.md's Project Conventions to describe the branch-backed plan store `create` now initializes.
4. Add a unit test for the missing-`git` error.
