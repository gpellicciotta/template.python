---
task: T0029
round: 2
verdict: approved
reviewer: "@claude"
reviewed_at: 2026-11-12T09:14:00Z
reviewed_commit: "2820814"
base_commit: "4c31af9"
branch: task/T0029-make-myproject-create-initialize-the-new-project-s
---
# Review Findings: Task T0029 (Round 2)

## Summary
Approved.
The rework fixes all four required items from round 1.
- The completion command passes with no extra environment: `python -m pytest tests/test_scaffold.py tests/test_cli.py` gives 24 passed.
- The CLI test still sets `PYTHONPATH` for its child `python -m myproject.cli` process.
  That points the child at the worktree's `src`, not at plan, so the round 1 concern no longer applies.
- `rmtree` now uses an `onexc` handler that clears read-only bits.
  A real `git commit` followed by a failing fake `plan` now raises `ScaffoldError` and leaves no directory.
- AGENTS.md describes the branch-backed store; a missing-`git` unit test exists.

Independent verification:
- Fast suite, three runs: 32 passed each time.
- Slow suite, two runs: 13 passed each time.
- Full suite: 45 passed.
- Ruff check and format: clean.
- Manual `create demo` under an isolated home:
  - exit 0, with a `plan` branch holding one commit.
  - `PLAN.md` links to `.plan/PLAN.md`.
  - `.plan`, `PLAN.md`, and `plan.code-workspace` are git-ignored.
  - AGENTS.md has exactly one managed block.

## Defects
None.

## Process Gaps
- The real-home write guard failed intermittently: once in the full suite and once in a slow run.
  A before/after snapshot traced it to `~/.claude.json`, which concurrent Claude Code sessions rewrite.
  The cause is the T0024 guard's top-level home snapshot, not this change.
  The validation proof noted the failure but did not diagnose it.
  Consider a follow-up task to exclude agent-owned home files or tolerate concurrent writers.
- Minor: the CHANGELOG adds a separate "read-only Git objects" fix for a feature that is not released yet.
  It also deletes the earlier fresh-clone entry instead of folding it into the new breaking entry.
- Minor: on POSIX, `_remove_readonly` sets mode `0600`, which would drop a directory's execute bit.
  It only runs after a `PermissionError`, so the Windows path this targets still works.

## Required Rework
None.
