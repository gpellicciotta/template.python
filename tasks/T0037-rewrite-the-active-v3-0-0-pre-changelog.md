---
id: T0037
owner: "@codex"
session: codex-20261112-1bba55
needs: []
branch: task/T0037-rewrite-the-active-v3-0-0-pre-changelog
worktree: .plan/work/T0037-rewrite-the-active-v3-0-0-pre-changelog
status: active
started_at: "2026-11-12T09:39:20Z"
ended_at: —
review: none
preview: none
protocol: adhoc
---
# T0037: Rewrite the active -pre CHANGELOG entries to follow the changelog entry style rules.

## Goals
Rewrite the active `-pre` CHANGELOG.md entries to follow the change management entry style rules.
Move `**[breaking]**` after the area in the six affected entries.
Replace the four `devops.py` sub-bullets with single-sentence entries of at most 20 words.
Consolidate the three `devops.py` entries and the two release-asset entries.
Link existing files, use code spans for removed files, and leave finalized versions untouched.

Completion check: `lint-markdown check CHANGELOG.md` reports no issue in the active -pre section.

### Declared Files
- CHANGELOG.md

Size estimate: 1 file, 30 lines

## Task Execution Steps
- [x] **[Doc]**       Rewrite the active -pre entries.
- [x] **[Verify]**    Run lint-markdown check on CHANGELOG.md.

## Execution Log
- [2026-11-10] **[Doc]**
  Companion task file scaffolded at task creation.

- [2026-11-12] **[Decided]**
  Consolidated active entries while preserving migration guidance and finalized versions.

- [2026-11-12] **[Verify]**
  Markdown lint and diff checks passed; active entries met word limits, and local links resolved.
  Evidence: [validation-proof.md](T0037-rewrite-the-active-v3-0-0-pre-changelog/validation-proof.md).

- [2026-11-12] **[Complete]**
  Rewrote the active changelog entries and preserved finalized history.
  - Files touched: 1; counted files: 0.
  - Lines touched: 30; counted lines: 0.
  - Reopenings: 0.
