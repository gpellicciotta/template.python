# Validation Proof

## Walkthrough & Validation
No automated code tests apply because this task changes changelog prose only.

Command: `& '../../../.venv/Scripts/lint-markdown.exe' check CHANGELOG.md`

Exit code: 0

```text
All 1 markdown files passed linting.
```

Command: `git diff --check`

Exit code: 0

```text
```

The active entries passed word-count, bullet-structure, and local-link checks.
The finalized section matched HEAD after line-ending normalization.

Command from the primary checkout: `plan tasks validate .plan/tasks/T0037-rewrite-the-active-v3-0-0-pre-changelog.md`

Exit code: 0

```text
All 1 task file passed validation.
```
