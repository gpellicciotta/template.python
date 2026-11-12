---
task: T0028
round: 1
verdict: rejected
reviewer: "@claude-2"
reviewed_at: 2026-11-12T10:26:40Z
reviewed_commit: "cbc14c8"
base_commit: "d60d432"
branch: task/T0028-add-dry-run-to-myproject-create-reporting-every
---
# Review Findings: Task T0028 (Round 1)

## Summary
The implementation meets every functional goal and the CLI guidelines' dry-run rule.
One README regression blocks approval; it is a one-line fix.

Verified by the reviewer:
- `pytest tests/test_scaffold.py tests/test_cli.py -m "slow or not slow"`: 50 passed, exit 0.
- `python scripts/devops.py check`: ruff, fast suite, slow suite (26 passed), and build all passed, exit 0.
- Ad hoc script against the real template, with `subprocess.run` mocked:
  `plan_project("new-app")` matched the 31 files `create_project` wrote.
  It also matched the exact set of files whose bytes changed.
- `create '' --dry-run` and `create src --dry-run` exit 1 with the destination error on stderr.
- `create demo --dry-run --format json` prints one JSON object with the documented fields.

Design notes:
- `create_project` now runs the plan from `plan_project`, so both share preconditions by construction.
- Rewriting `AGENTS.md` only when it holds a plan block is a sound change; the plan and real run agree.
- `test_plan_project_matches_created_files` guards the plan against drift from the real run.

## Defects
1. README.md:150 — the change moved "Initialization failures remove the generated directory and return exit code `1`."
   It now follows the `create --dry-run` example block instead of the real-run paragraph (main's line 136).
   It now reads as dry-run behavior, though a dry run never generates a directory.
   It also sits directly after the closing code fence with no blank line.

## Process Gaps
- Non-blocking: the spec's integration scenario names the `myproject` entry point.
  `test_create_dry_run_entry_point_writes_nothing` runs `python -m myproject.cli` instead.
  This is functionally equivalent; T0025's tests already cover the console-script binding.
- Non-blocking: the change exceeded the 200-line size estimate (370 insertions); the Execution Log records the reason.

## Required Rework
1. Move the "Initialization failures ..." sentence back to the end of the real-run `create` paragraph in README.md.
   Put it after "Its plan store lives on the `plan` branch ...", as on `main`.
   Leave a blank line after the dry-run example's closing fence.
2. Re-run `.venv/Scripts/lint-markdown check README.md` and record the result in validation-proof.md.
