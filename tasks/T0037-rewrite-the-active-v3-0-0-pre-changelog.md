---
id: T0037
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
- [ ] **[Doc]**       Rewrite the active -pre entries.
- [ ] **[Verify]**    Run lint-markdown check on CHANGELOG.md.

## Execution Log
- [2026-11-10] **[Doc]**
  Companion task file scaffolded at task creation.
