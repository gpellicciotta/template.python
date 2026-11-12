# Validation Proof

## Walkthrough & Validation
Red phase: `python -m pytest tests/test_isolation.py -q --tb=short` exited 1 before fixture implementation.

```text
FFFFF                                                                    [100%]
================================== FAILURES ===================================
__________________ test_home_and_configuration_are_temporary __________________
tests\test_isolation.py:12: in test_home_and_configuration_are_temporary
    assert Path.home() == tmp_path / "home"
E   AssertionError: assert WindowsPath('C:/Users/giova') == (WindowsPath('C:/Users/giova/AppData/Local/Temp/pytest-of-giova/pytest-8426/test_home_and_configuration_ar0') / 'home')
E    +  where WindowsPath('C:/Users/giova') = home()
E    +    where home = Path.home
[... 28 lines omitted ...]
=========================== short test summary info ===========================
FAILED tests/test_isolation.py::test_home_and_configuration_are_temporary - A...
FAILED tests/test_isolation.py::test_nested_session_rejects_real_state_writes[home]
FAILED tests/test_isolation.py::test_nested_session_rejects_real_state_writes[repository]
FAILED tests/test_isolation.py::test_nested_session_rejects_real_state_writes[subprocess]
FAILED tests/test_isolation.py::test_nested_session_rejects_real_state_writes[caught]
5 failed in 0.13s
```

Final commands each exited 0:

```text
python -m ruff check tests/conftest.py tests/test_isolation.py
All checks passed!
python -m ruff format --check tests/conftest.py tests/test_isolation.py
2 files already formatted
python -m pytest -q --tb=short -n 2
bringing up nodes...
bringing up nodes...

.....................................                                    [100%]
37 passed in 4.74s
```

Completion check: `python -m pytest -q --tb=short` exited 0.

```text
.....................................                                    [100%]
37 passed in 9.47s
```

Nested sessions use disposable protected directories and assert nonzero exits for attempted leaks.
Coverage includes home, repository, subprocess, caught exceptions, deletion, rename, environment restoration, and per-test separation.
Both serial and parallel runs include the affected slow tests.
Installed pytest-xdist 3.8.0 into the existing development environment for parallel verification.
No dependency manifest changed.

The audit hook guards Python mutations throughout fixture execution.
Snapshots detect repository file metadata changes and real-home top-level entry changes, including subprocess effects.
Snapshots exclude temporary storage and tool caches; they never read file contents.
Deep subprocess changes within existing home subdirectories are outside this guard's snapshot coverage.

`lint-markdown check --offline CHANGELOG.md` exited 1 for existing entries outside this change.

```text
**[WARN]**  Found 4 lint issues across 1 files.
**[ERROR]** Finished lint-markdown check in 0.0s with status: failed
CHANGELOG.md:22:34: MD019 [file-references-as-links] Repository file reference 'scripts/devops.py' in prose must be formatted as markdown link [filename](path)
CHANGELOG.md:30:110: MD019 [file-references-as-links] Repository file reference 'scripts/devops.py' in prose must be formatted as markdown link [filename](path)
CHANGELOG.md:37:16: MD019 [file-references-as-links] Repository file reference 'scripts/devops.py' in prose must be formatted as markdown link [filename](path)
CHANGELOG.md:89:4: MD008 [no-raw-urls] Raw URL found in prose: 'https://github.com/gpellicciotta/python-project-template'; enclose in markdown link
```

Online lint also reported an existing external link returning HTTP 404.
The added changelog entry introduced no lint findings.
Task specification, task log, and validation evidence passed offline Markdown linting.
