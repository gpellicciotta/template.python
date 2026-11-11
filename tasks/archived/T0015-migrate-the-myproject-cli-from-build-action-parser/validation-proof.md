# T0015 Validation Proof

## Walkthrough & Validation
### Failing tests before the implementation (v1 CLI, support-python v1.0.0)
```text
$ .venv/Scripts/python -m pytest -q tests/test_cli.py
FFFF..FF.F.                                                              [100%]
[... 103 lines omitted ...]
FAILED tests/test_cli.py::test_help_exits_zero - AssertionError: assert 'Usag...
FAILED tests/test_cli.py::test_help_flags - assert 'Usage:' in 'myproject v2....
FAILED tests/test_cli.py::test_no_args_shows_help - AssertionError: assert 'U...
FAILED tests/test_cli.py::test_action_help_lists_create_options - AssertionEr...
FAILED tests/test_cli.py::test_greet_verbose - AssertionError: assert 'Starti...
FAILED tests/test_cli.py::test_create_scaffolds_renamed_project - assert 'sup...
FAILED tests/test_cli.py::test_create_missing_project_name - AssertionError: ...
7 failed, 4 passed in 0.46s
exit 1
```

Review round 1 asked for documented positional arguments; `test_action_help_describes_greet_argument` was added with that fix.

### Lint after review rework
```text
$ .venv/Scripts/python -m ruff check . ; ruff format --check .
All checks passed!
19 files already formatted
exit 0
```

### Full suite after review rework (support-python v2.0.0 installed)
```text
$ .venv/Scripts/python -m pytest -q
........................                                                 [100%]
24 passed in 0.88s
exit 0
```

### Installed console script: help (integration scenario)
```text
$ .venv/Scripts/myproject help
myproject v3.0.0rc0+6da116c - Copyright (c) 2026 Giovanni Pellicciotta

Sample CLI for template.python providing greeting and project scaffolding.

Usage:
  myproject greet [NAME]
  myproject create PROJECT_NAME [-o DIR]
  myproject version
  myproject help [--verbose]

Actions:
  greet                  print a greeting
  create                 scaffold a new project from this template
  version                show version information and exit
  help                   show help message and exit (use --verbose for details)

Options:
  -h, --help             show help message and exit
  --version              show version information and exit
  -v, --verbose          enable verbose output logging
  --debug                enable debug output logging (implies --verbose)
[... 6 lines omitted ...]
  2   invalid arguments or syntax errors
exit 0
```

```text
$ .venv/Scripts/myproject help greet
myproject v3.0.0rc0+6da116c - Copyright (c) 2026 Giovanni Pellicciotta

Detailed Action Description: greet
  Prints 'Hello, NAME'; NAME defaults to 'wereld'.
  With --verbose, also prints the greeting target.

Examples:
  myproject greet Gio

Usage:
  myproject greet [NAME]

Options:
  -h, --help             show help message and exit
  --version              show version information and exit
  -v, --verbose          enable verbose output logging
  --debug                enable debug output logging (implies --verbose)
  --log-file PATH        append operational logs to specified file
  --log-level LEVEL      logging severity threshold (DEBUG, INFO, WARN, ERROR; default: INFO)

Exit codes:
  0   success
  1   operational or runtime execution error
  2   invalid arguments or syntax errors
exit 0
```

### Installed console script: actions and errors (integration scenario)
```text
$ .venv/Scripts/myproject version
myproject v3.0.0rc0+6da116c - Copyright (c) 2026 Giovanni Pellicciotta
exit 0
$ .venv/Scripts/myproject greet Gio
Hello, Gio
exit 0
$ .venv/Scripts/myproject greet Gio --verbose
Starting myproject v3.0.0rc0+6da116c with configuration:
- Command: greet
- Log file: none
- Log level: INFO
- Verbose: true
Greeting target: Gio
Hello, Gio
Finished myproject greet in 0.0s with status: succeeded
exit 0
$ .venv/Scripts/myproject create
**[ERROR]** the following arguments are required: PROJECT_NAME
            Usage: myproject create PROJECT_NAME [-o DIR]
exit 2
$ .venv/Scripts/myproject bogus
**[ERROR]** Unknown subcommand: 'bogus'
            Usage: myproject {help|version|greet|create} [options]
exit 2
```
