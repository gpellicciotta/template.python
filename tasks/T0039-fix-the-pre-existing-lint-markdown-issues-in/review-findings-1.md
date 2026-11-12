---
task: T0039
round: 1
verdict: rejected
reviewer: "@claude"
reviewed_at: 2026-11-12T09:20:33Z
reviewed_commit: "3422bf4"
base_commit: "6b139f8"
branch: task/T0039-fix-the-pre-existing-lint-markdown-issues-in
---
# Review Findings: Task T0039 (Round 1)

## Summary
Rejected; the mechanical lint fixes are correct, but two released changelog entries now misstate history.
- `lint-markdown check README.md CHANGELOG.md` exits 0: "All 2 markdown files passed linting."
- `pytest -q` passed 45 tests; `ruff check .` passed.
- The first pytest run had one transient real-state guard error; an immediate rerun passed.
- The error is unrelated to this documentation-only diff.
- The README heading, code-fence, and file-link fixes are correct and scaffold-safe.
- All linked repository files exist in scaffolded projects.

## Defects
1. `CHANGELOG.md:73` rewrites the released v1.2.0 entry to "Aligned project with latest [AGENTS.md](AGENTS.md)".
   That is false: `AGENTS.md` was first added in 6fb599d on 2026-10-31, long after v1.2.0 (2026-08-24).
   v1.2.0 aligned with the external development guidelines, not with `AGENTS.md`.
   MD018 required only the dead link to go, not a new claim.
2. `CHANGELOG.md:91` replaces the v1.0.0 published repository name `python-project-template` with `template.python`.
   v1.0.0 was published as `python-project-template`; the rename happened in v2.0.0.
   The old URL still resolves (HTTP 200, redirects to `template.python`), so MD008 needed only a link wrapper.
3. Minor: `README.md:61` adds `[AGENTS.md](AGENTS.md)` to "Useful Resources" about Python layouts.
   It duplicates the intro link at `README.md:7` and is not a layout resource; dropping the bullet is cleaner.

## Process Gaps
- The Execution Log records a TF020 completion-validation failure but no later Verify entry confirming the fix.
- The first Verify entry precedes the Implement and Doc entries, so the log order does not match execution.

## Required Rework
1. Restore the v1.2.0 meaning without a dead link, e.g. "Aligned project with the latest development guidelines:".
2. Restore the v1.0.0 name, e.g. "([python-project-template](https://github.com/gpellicciotta/python-project-template))".
3. Optional: remove the duplicate `AGENTS.md` bullet from README "Useful Resources".
4. Re-run `lint-markdown check README.md CHANGELOG.md` and record the verbatim output in validation-proof.md.
