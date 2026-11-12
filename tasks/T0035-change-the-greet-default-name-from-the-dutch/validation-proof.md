# Validation Proof

## Walkthrough & Validation
Commands ran in the task worktree with `PYTHONPATH` set to its `src` directory.
`{{python}}` denotes the primary checkout's `.venv/Scripts/python.exe`.
`{{lint-markdown}}` denotes its `.venv/Scripts/lint-markdown.exe`.

### Red phase
Command: `{{python}} -m pytest tests/test_cli.py -k 'test_greet or test_action_help_describes_greet_argument' -q`
Exit code: 1.

```text
[... 36 lines omitted ...]
=========================== short test summary info ===========================
FAILED tests/test_cli.py::test_action_help_describes_greet_argument - assert ...
FAILED tests/test_cli.py::test_greet - AssertionError: assert 'Hello, wereld'...
2 failed, 1 passed, 13 deselected in 1.19s
```

### Full suite
Command: `{{python}} -m pytest -q`
Exit code: 0. This includes fast and slow tests.

```text
..................................................                       [100%]
50 passed in 21.00s
```

### CLI entry point
Command: `{{python}} -m myproject.cli greet`
Exit code: 0.

```text
Hello, world
```

### Python lint
Command: `{{python}} -m ruff check src/myproject/cli.py tests/test_cli.py`
Exit code: 0.

```text
All checks passed!
```

Command: `{{python}} -m ruff format --check src/myproject/cli.py tests/test_cli.py`
Exit code: 0.

```text
2 files already formatted
```

### Markdown lint
Command: `{{lint-markdown}} check README.md docs/requirements.md CHANGELOG.md`
Exit code: 1.
Existing blank lines and external links caused the following failures; `git show HEAD:docs/requirements.md` confirmed unchanged content.

```text
docs\requirements.md:7:1: MD015 [no-blank-line-after-subheading] Heading 'High-Level Goals' (H2) must not be followed by a blank line before content
docs\requirements.md:11:49: MD018 [valid-external-links] External link 'https://github.com/gpellicciotta/dev-guidelines' failed validation: HTTP 404
docs\requirements.md:49:1: MD015 [no-blank-line-after-subheading] Heading 'Technical Requirements' (H2) must not be followed by a blank line before content
docs\requirements.md:58:110: MD018 [valid-external-links] External link 'https://github.com/gpellicciotta/dev-guidelines/blob/main/guidelines/markdown-guidelines.md' failed validation: HTTP 404
**[WARN]**  Found 4 lint issues across 3 files.
**[ERROR]** Finished lint-markdown check in 3.8s with status: failed
```

### Whitespace
Command: `git diff --check`
Exit code: 0. No output.
