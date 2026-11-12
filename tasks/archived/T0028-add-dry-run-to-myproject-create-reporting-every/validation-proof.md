## Walkthrough & Validation

### Summary
- `scaffold.plan_project()` checks `create_project`'s preconditions and returns a `ScaffoldPlan` without writing.
- `create_project()` now calls `plan_project()` first and runs that plan, so a dry run fails exactly as the real run does.
- `ScaffoldPlan` lists `copied` (template-relative), `renamed`, `rewritten`, `reset` (destination-relative), and `commands`.
- `myproject create --dry-run` prints one `Would <change>: <item>` line per change, or one JSON object with `--format json`.
- **[Decided]** The dry run lives in a separate `plan_project()` function instead of a `dry_run` flag on `create_project()`.
  This keeps `create_project()` returning a `Path`.
- **[Decided]** The real run now rewrites `AGENTS.md` only when it holds a plan block, so the plan matches the files written.
- `test_plan_project_matches_created_files` compares the plan with the files a real (subprocess-mocked) run writes.

### Failing tests before implementation
Command: `C:/Dev-Projects/template.python/.venv/Scripts/python -m pytest tests/test_scaffold.py tests/test_cli.py -p no:randomly -q --tb=line -k "plan_project or dry_run" -m "slow or not slow"`
Exit code: 1. Run from the worktree with the main checkout's venv; `pythonpath = ["src"]` puts the worktree sources first.

```text
[... 12 traceback lines omitted ...]
=========================== short test summary info ===========================
FAILED tests/test_scaffold.py::test_plan_project_keeps_package_name_without_rename
FAILED tests/test_scaffold.py::test_plan_project_matches_created_files - Attr...
FAILED tests/test_scaffold.py::test_plan_project_fails_like_real_run[demo-plan-plan.*PATH]
FAILED tests/test_scaffold.py::test_plan_project_fails_like_real_run[dup-app-None-already exists]
FAILED tests/test_scaffold.py::test_plan_project_fails_like_real_run[123-None-package name]
FAILED tests/test_scaffold.py::test_plan_project_fails_like_real_run[demo-git-git.*PATH]
FAILED tests/test_scaffold.py::test_plan_project_reports_changes_without_writing
FAILED tests/test_cli.py::test_create_dry_run_json - AssertionError: assert 2...
FAILED tests/test_cli.py::test_create_dry_run_missing_plan_exits_one - Assert...
FAILED tests/test_cli.py::test_create_dry_run_fails_like_real_run[dup-app-already exists]
FAILED tests/test_cli.py::test_create_dry_run_fails_like_real_run[123-package name]
FAILED tests/test_cli.py::test_create_dry_run_reports_changes_without_writing
FAILED tests/test_cli.py::test_action_help_lists_dry_run_option - AssertionEr...
FAILED tests/test_cli.py::test_create_dry_run_entry_point_writes_nothing - As...
14 failed in 2.75s
exit=1
```

### Completion check
Command: `.venv/Scripts/python -m pytest tests/test_scaffold.py tests/test_cli.py -m "slow or not slow" -p no:randomly -q`
Exit code: 0. Includes the slow `create demo -o {{tmp}} --dry-run` entry-point scenario.

```text
bringing up nodes...
bringing up nodes...

..................................................                       [100%]
50 passed in 4.93s
```

### Fast suite
Command: `python scripts/devops.py test`
Exit code: 0.

```text
bringing up nodes...
bringing up nodes...
....................................................                     [100%]
52 passed in 2.18s
```

### Full check (lint, fast and slow suites, build)
Command: `python scripts/devops.py check`
Exit code: 0. `[...]` replaces the worktree path prefix; the five `Process ID:` lines are omitted.

```text
Command: [...]\.venv\Scripts\python.exe -m ruff check .
All checks passed!
Command: [...]\.venv\Scripts\python.exe -m ruff format --check .
22 files already formatted
Command: [...]\.venv\Scripts\python.exe -m pytest -q
....................................................                     [100%]
52 passed in 2.18s
Command: [...]\.venv\Scripts\python.exe -m pytest -m slow --timeout=120
[... 11 lines omitted ...]
..........................                                               [100%]
============================= 26 passed in 7.46s ==============================
[... 116 build lines omitted ...]
Successfully built template_python-3.0.17rc0.tar.gz and template_python-3.0.17rc0-py3-none-any.whl
```

### Transient guard failures
Two earlier runs (`devops.py check`, then `devops.py test`) passed every test but failed the session teardown guard.
The guard flagged `real home entries changed`, caused by Claude Code's atomic `~/.claude.json` writes during the run.
The tests did not write those files. Reruns passed with exit code 0 (above).

```text
E       FileNotFoundError: [WinError 2] The system cannot find the file specified: 'C:\\Users\\giova\\.claude.json.tmp.3852.572be492609c'
[... 3 lines omitted ...]
52 passed, 8 errors in 3.09s
**[ERROR]** Finished devops test in 3.8s with status: failed
```

### Manual dry run against the real template
Command: `PYTHONPATH=src .venv/Scripts/python -m myproject.cli create demo -o ../dry-run-check --dry-run`
Exit code: 0. Prints 52 lines; `Would copy:` lines are filtered out below. `../dry-run-check` still does not exist afterwards.

```text
Would create new project at C:\Dev-Projects\template.python\.plan\work\dry-run-check\demo
Would rename: src/myproject -> src/demo
Would rewrite: AGENTS.md
Would rewrite: CHANGELOG.md
Would rewrite: README.md
[... 9 rewrite lines omitted ...]
Would rewrite: tests/test_scaffold.py
Would reset: AGENTS.md
Would reset: CHANGELOG.md
Would reset: pyproject.toml
Would run: git init
Would run: plan init --store branch
ls: cannot access '../dry-run-check': No such file or directory
```

### Markdown lint
Command: `.venv/Scripts/lint-markdown check README.md CHANGELOG.md`
Exit code: 0.

```text
All 2 markdown files passed linting.
```

### Review round 1 rework
The "Initialization failures ..." sentence moved back to the end of the real-run `create` paragraph in README.md.
Command: `.venv/Scripts/lint-markdown check README.md`
Exit code: 0. The change is documentation-only, so no test inputs changed.

```text
All 1 markdown files passed linting.
```

`docs/requirements.md` reports four issues (MD015 at lines 7 and 60, MD018 at lines 11 and 69).
All four are in unchanged lines; `HEAD`'s copy of the file reports the same four.
