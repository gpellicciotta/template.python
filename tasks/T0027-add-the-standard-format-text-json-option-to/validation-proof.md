## Walkthrough & Validation

### Summary
- `greet` and `create` register `--format text|json` with `ToolHarness.add_format_option`.
- `json` mode prints one object through `CliLogger.emit_json`; the harness routes log entries to stderr.
- `greet` fields: `name`, `greeting`. `create` fields: `project_name`, `path`.
- **[Decided]** A failed `create` prints no JSON document; the error stays on stderr with exit code 1.
- `text` output is unchanged and remains the default.

### Failing tests before implementation
Command: `.venv/Scripts/python -m pytest tests/test_cli.py -p no:randomly -q --tb=line -k "json or format" -m "slow or not slow"`
Exit code: 1. `test_invalid_format_exits_two` passed already, since argparse rejected the unknown `--format` with exit code 2.

```text
[... 11 traceback lines omitted ...]
=========================== short test summary info ===========================
FAILED tests/test_cli.py::test_greet_json_verbose_logs_to_stderr - AssertionE...
FAILED tests/test_cli.py::test_create_json - AssertionError: assert 2 == 0
FAILED tests/test_cli.py::test_greet_json - AssertionError: assert 2 == 0
FAILED tests/test_cli.py::test_create_json_failure_prints_no_document - Asser...
FAILED tests/test_cli.py::test_action_help_lists_format_option - assert '--fo...
FAILED tests/test_cli.py::test_create_json_verbose_keeps_stdout_machine_readable
6 failed, 1 passed in 5.44s
exit=1
```

### Completion check
Command: `.venv/Scripts/python -m pytest tests/test_cli.py -m "slow or not slow" -p no:randomly -q`
Exit code: 0. Includes the slow `create --format json --verbose` subprocess scenario.

```text
bringing up nodes...

.......................                                                  [100%]
23 passed in 4.64s
exit=0
```

### Full checks: lint, fast suite, slow suite, build
Command: `python scripts/devops.py check`
Exit code: 0.

```text
Command: ...\.venv\Scripts\python.exe -m ruff check .
All checks passed!
Command: ...\.venv\Scripts\python.exe -m ruff format --check .
22 files already formatted
Command: ...\.venv\Scripts\python.exe -m pytest -q
.......................................                                  [100%]
39 passed in 2.38s
Command: ...\.venv\Scripts\python.exe -m pytest -m slow --timeout=120
8 workers [25 items]
.........................                                                [100%]
============================= 25 passed in 8.05s ==============================
Command: ...\.venv\Scripts\python.exe -m build -o dist
[... build log lines omitted ...]
Successfully built template_python-3.0.16rc0.tar.gz and template_python-3.0.16rc0-py3-none-any.whl
exit=0
```

### Manual CLI run
Command: `.venv/Scripts/myproject greet Gio --format json -v 2>err.txt`, then `cat err.txt`.
Exit code: 0. Stdout holds only the JSON document; the verbose log goes to stderr.

```text
{"name": "Gio", "greeting": "Hello, Gio"}
exit=0
--- stderr:
Starting myproject v3.0.16-pre+e35716a with configuration:
- Command: greet
- Log file: none
- Log level: INFO
- Verbose: true
Greeting target: Gio
Finished myproject greet in 0.0s with status: succeeded
```

### Markdown lint
Command: `.venv/Scripts/lint-markdown check README.md CHANGELOG.md`
Exit code: 0.

```text
All 2 markdown files passed linting.
exit=0
```

`docs/requirements.md` reports four issues (MD015 twice, MD018 twice).
The same four occur on `main` before this change, so they are out of scope.
