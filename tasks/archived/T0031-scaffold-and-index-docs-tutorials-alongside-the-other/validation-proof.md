# Walkthrough & Validation

## Regression
Command: `python -m pytest tests/test_cli.py -k test_create_scaffolds_renamed_project -m slow --timeout=120 -q`

Exit code: 1. The new assertion failed before adding the tutorial placeholder.

```text
[... earlier failure output omitted ...]
>       assert (destination / "docs" / "tutorials" / ".gitkeep").is_file()
E       AssertionError: assert False
[... path details omitted ...]
tests\test_cli.py:151: AssertionError
=========================== short test summary info ===========================
FAILED tests/test_cli.py::test_create_scaffolds_renamed_project - AssertionEr...
1 failed, 15 deselected in 2.01s
```

## Final Checks

Command: `python -m pytest -m 'not slow' --timeout=30 -q`

Exit code: 0.

```text
.....................................                                    [100%]
37 passed, 13 deselected in 1.74s
```

Command: `python -m pytest tests/test_cli.py --timeout=120 -q`

Exit code: 0.

```text
................                                                         [100%]
16 passed in 4.12s
```

Command: `lint-markdown check README.md docs/index.md CHANGELOG.md`

Exit code: 1.

```text
docs\index.md:7:1: MD015 [no-blank-line-after-subheading] Heading 'Core Documentation' (H2) must not be followed by a blank line before content
docs\index.md:13:10: MD014 [valid-relative-links] Relative link '../PLAN.md' does not resolve to an existing file on disk
docs\index.md:18:1: MD015 [no-blank-line-after-subheading] Heading 'Specialized Documentation' (H2) must not be followed by a blank line before content
docs\index.md:27:1: MD015 [no-blank-line-after-subheading] Heading 'Guidelines' (H2) must not be followed by a blank line before content
docs\index.md:30:26: MD018 [valid-external-links] External link 'https://github.com/gpellicciotta/dev-guidelines' failed validation: HTTP 404
docs\index.md:31:22: MD018 [valid-external-links] External link 'https://github.com/gpellicciotta/dev-guidelines/blob/main/guidelines/general-guidelines.md' failed validation: HTTP 429
docs\index.md:32:21: MD018 [valid-external-links] External link 'https://github.com/gpellicciotta/dev-guidelines/blob/main/guidelines/python-guidelines.md' failed validation: HTTP 404
docs\index.md:33:32: MD018 [valid-external-links] External link 'https://github.com/gpellicciotta/dev-guidelines/blob/main/guidelines/coordinating-work-guidelines.md' failed validation: HTTP 404
docs\index.md:35:23: MD018 [valid-external-links] External link 'https://github.com/gpellicciotta/dev-guidelines/blob/main/guidelines/markdown-guidelines.md' failed validation: HTTP 404
**[WARN]**  Found 9 lint issues across 3 files.
**[ERROR]** Finished lint-markdown check in 4.2s with status: failed
```

Command: `lint-markdown check --offline README.md docs/index.md CHANGELOG.md`

Exit code: 1.

```text
docs\index.md:7:1: MD015 [no-blank-line-after-subheading] Heading 'Core Documentation' (H2) must not be followed by a blank line before content
docs\index.md:13:10: MD014 [valid-relative-links] Relative link '../PLAN.md' does not resolve to an existing file on disk
docs\index.md:18:1: MD015 [no-blank-line-after-subheading] Heading 'Specialized Documentation' (H2) must not be followed by a blank line before content
docs\index.md:27:1: MD015 [no-blank-line-after-subheading] Heading 'Guidelines' (H2) must not be followed by a blank line before content
**[WARN]**  Found 4 lint issues across 3 files.
**[ERROR]** Finished lint-markdown check in 0.0s with status: failed
```

Command: `python -m ruff check tests/test_cli.py`

Exit code: 0.

```text
All checks passed!
```

Command: `python -m ruff format --check tests/test_cli.py`

Exit code: 0.

```text
1 file already formatted
```

## Baseline Comparison
The baseline index reports the same four offline issues. The added tutorial link introduces no lint violations.
External failures concern unchanged guideline URLs. The isolated worktree lacks the existing plan convenience link.

Command: `lint-markdown check --offline docs/.baseline-index.md`

The temporary file contained `git show HEAD:docs/index.md` and was removed after verification.
The linter exited 1; its enclosing cleanup command exited 0.

```text
docs\.baseline-index.md:7:1: MD015 [no-blank-line-after-subheading] Heading 'Core Documentation' (H2) must not be followed by a blank line before content
docs\.baseline-index.md:13:10: MD014 [valid-relative-links] Relative link '../PLAN.md' does not resolve to an existing file on disk
docs\.baseline-index.md:18:1: MD015 [no-blank-line-after-subheading] Heading 'Specialized Documentation' (H2) must not be followed by a blank line before content
docs\.baseline-index.md:26:1: MD015 [no-blank-line-after-subheading] Heading 'Guidelines' (H2) must not be followed by a blank line before content
**[WARN]**  Found 4 lint issues across 1 files.
**[ERROR]** Finished lint-markdown check in 0.0s with status: failed
```

