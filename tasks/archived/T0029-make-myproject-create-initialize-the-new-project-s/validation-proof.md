# Validation Proof

## Walkthrough & Validation

### Review rework verification
The following results supersede the earlier runs using a machine-specific PYTHONPATH override.
No external PYTHONPATH override was used for these commands.
The regression first reproduced PermissionError while removing committed Git objects on Windows.
One fast run detected changed real-home metadata; the subsequent fast run and full suite passed.

Command: `python -m pytest tests/test_scaffold.py -k 'missing_git or failed_plan_after_commit' -q --tb=short`; exit code: 1.

```text
.F                                                                       [100%]
================================== FAILURES ===================================
_________ test_failed_plan_after_commit_removes_readonly_git_objects __________
src\myproject\scaffold.py:122: in _initialize_plan_store
    subprocess.run([plan, "init", "--store", "branch"], cwd=destination, check=True, capture_output=True, text=True)
C:\Users\giova\AppData\Local\Programs\Python\Python315\Lib\subprocess.py:692: in run
    raise CalledProcessError(retcode, process.args,
E   subprocess.CalledProcessError: Command ['C:\\Users\\giova\\AppData\\Local\\Temp\\pytest-of-giova\\pytest-8457\\test_failed_plan_after_commit_0\\tools\\plan.CMD', 'init', '--store', 'branch'] returned non-zero exit status 1.

During handling of the above exception, another exception occurred:
tests\test_scaffold.py:113: in test_failed_plan_after_commit_removes_readonly_git_objects
    create_project("demo", str(tmp_path / "out"), template_root=root)
src\myproject\scaffold.py:171: in create_project
    _initialize_plan_store(destination, git, plan)
src\myproject\scaffold.py:125: in _initialize_plan_store
    shutil.rmtree(destination)
C:\Users\giova\AppData\Local\Programs\Python\Python315\Lib\shutil.py:859: in rmtree
    _rmtree_impl(path, dir_fd, onexc)
C:\Users\giova\AppData\Local\Programs\Python\Python315\Lib\shutil.py:705: in _rmtree_unsafe
    onexc(os.unlink, fullname, err)
C:\Users\giova\AppData\Local\Programs\Python\Python315\Lib\shutil.py:701: in _rmtree_unsafe
    os.unlink(fullname)
E   PermissionError: [WinError 5] Access is denied: 'C:\\Users\\giova\\AppData\\Local\\Temp\\pytest-of-giova\\pytest-8457\\test_failed_plan_after_commit_0\\out\\demo\\.git\\objects\\09\\69ee7b5ad280582389551f84e52ec0b16d163c'
=========================== short test summary info ===========================
FAILED tests/test_scaffold.py::test_failed_plan_after_commit_removes_readonly_git_objects
1 failed, 1 passed, 9 deselected in 1.78s
```

Command: `python -m pytest tests/test_scaffold.py tests/test_cli.py -q`; exit code: 0.

```text
........................                                                 [100%]
24 passed in 10.67s
```

Command: `python -m pytest -m 'not slow' -q`; exit code: 1.

```text
................................E                                        [100%]
=================================== ERRORS ====================================
_ ERROR at teardown of test_scripts_are_ascii_only_for_legacy_windows_consoles _
Real-state write guard failed:
real home entries changed
=========================== short test summary info ===========================
ERROR tests/test_scripts.py::test_scripts_are_ascii_only_for_legacy_windows_consoles
32 passed, 13 deselected, 1 error in 4.46s
```

Command: `python -m pytest -q`; exit code: 0.

```text
.............................................                            [100%]
45 passed in 20.82s
```

Command: `python -m ruff check .`; exit code: 0.

```text
All checks passed!
```

Command: `python -m ruff format --check .`; exit code: 0.

```text
21 files already formatted
```

Command: `git diff --check`; exit code: 0.

```text

```

Command: `lint-markdown check --offline AGENTS.md`; exit code: 0.

```text
All 1 markdown files passed linting.
```

Command: `python -m pytest -m 'not slow' -q`; exit code: 0.

```text
................................                                         [100%]
32 passed, 13 deselected in 3.31s
```

### Earlier evidence (superseded)


Command: `python -m pytest tests/test_scaffold.py tests/test_cli.py -m 'not slow' -q`; exit code: 1.

```text
...FFFF..........F.                                                      [100%]
================================== FAILURES ===================================
________________ test_create_runs_git_and_plan_in_destination _________________

tmp_path = WindowsPath('C:/Users/giova/AppData/Local/Temp/pytest-of-giova/pytest-8442/test_create_runs_git_and_plan_0')
monkeypatch = <_pytest.monkeypatch.MonkeyPatch object at 0x000002AEB8131370>

    def test_create_runs_git_and_plan_in_destination(tmp_path, monkeypatch):
        root = _fake_template_root(tmp_path / "template")
        calls = []
        monkeypatch.setattr(scaffold.shutil, "which", lambda name: name)
>       monkeypatch.setattr(scaffold.subprocess, "run", lambda args, **kwargs: calls.append((args, kwargs)))
                            ^^^^^^^^^^^^^^^^^^^
E       AttributeError: module 'myproject.scaffold' has no attribute 'subprocess'

tests\test_scaffold.py:66: AttributeError
_______________ test_create_missing_plan_leaves_no_destination ________________

tmp_path = WindowsPath('C:/Users/giova/AppData/Local/Temp/pytest-of-giova/pytest-8442/test_create_missing_plan_leave0')
monkeypatch = <_pytest.monkeypatch.MonkeyPatch object at 0x000002AEB8131260>

    def test_create_missing_plan_leaves_no_destination(tmp_path, monkeypatch):
        root = _fake_template_root(tmp_path / "template")
        monkeypatch.setattr(scaffold.shutil, "which", lambda name: None if name == "plan" else name)
>       with pytest.raises(scaffold.ScaffoldError, match="plan.*PATH"):
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E       Failed: DID NOT RAISE ScaffoldError

tests\test_scaffold.py:75: Failed
___________ test_initialization_failure_cleans_destination[error0] ____________

tmp_path = WindowsPath('C:/Users/giova/AppData/Local/Temp/pytest-of-giova/pytest-8442/test_initialization_failure_cl0')
monkeypatch = <_pytest.monkeypatch.MonkeyPatch object at 0x000002AEB817AE50>
error = OSError('cannot start')

    @pytest.mark.parametrize("error", [OSError("cannot start"), subprocess.CalledProcessError(1, "plan", stderr="init failed")])
    def test_initialization_failure_cleans_destination(tmp_path, monkeypatch, error):
        root = _fake_template_root(tmp_path / "template")
        monkeypatch.setattr(scaffold.shutil, "which", lambda name: name)
    
```

```text
        def fail(*args, **kwargs):
            raise error
    
>       monkeypatch.setattr(scaffold.subprocess, "run", fail)
                            ^^^^^^^^^^^^^^^^^^^
E       AttributeError: module 'myproject.scaffold' has no attribute 'subprocess'

tests\test_scaffold.py:88: AttributeError
___________ test_initialization_failure_cleans_destination[error1] ____________

tmp_path = WindowsPath('C:/Users/giova/AppData/Local/Temp/pytest-of-giova/pytest-8442/test_initialization_failure_cl1')
monkeypatch = <_pytest.monkeypatch.MonkeyPatch object at 0x000002AEB817B750>
error = CalledProcessError(1, 'plan')

    @pytest.mark.parametrize("error", [OSError("cannot start"), subprocess.CalledProcessError(1, "plan", stderr="init failed")])
    def test_initialization_failure_cleans_destination(tmp_path, monkeypatch, error):
        root = _fake_template_root(tmp_path / "template")
        monkeypatch.setattr(scaffold.shutil, "which", lambda name: name)
    
        def fail(*args, **kwargs):
            raise error
    
>       monkeypatch.setattr(scaffold.subprocess, "run", fail)
                            ^^^^^^^^^^^^^^^^^^^
E       AttributeError: module 'myproject.scaffold' has no attribute 'subprocess'

tests\test_scaffold.py:88: AttributeError
_____________________ test_create_missing_plan_exits_one ______________________

tmp_path = WindowsPath('C:/Users/giova/AppData/Local/Temp/pytest-of-giova/pytest-8442/test_create_missing_plan_exits0')
monkeypatch = <_pytest.monkeypatch.MonkeyPatch object at 0x000002AEB81D09B0>
capsys = <_pytest.capture.CaptureFixture object at 0x000002AEB81D8320>

    def test_create_missing_plan_exits_one(tmp_path, monkeypatch, capsys):
        monkeypatch.setenv("PATH", "")
>       assert main(["create", "demo", "-o", str(tmp_path)]) == 1
E       AssertionError: assert 0 == 1
E        +  where 0 = main(['create', 'demo', '-o', 'C:\\Users\\giova\\AppData\\Local\\Temp\\pytest-of-giova\\pytest-8442\\test_create_missing_plan_exits0'])

tests\test_cli.py:156: AssertionError
```

```text
---------------------------- Captured stdout call -----------------------------
Created new project at C:\Users\giova\AppData\Local\Temp\pytest-of-giova\pytest-8442\test_create_missing_plan_exits0\demo
=========================== short test summary info ===========================
FAILED tests/test_scaffold.py::test_create_runs_git_and_plan_in_destination
FAILED tests/test_scaffold.py::test_create_missing_plan_leaves_no_destination
FAILED tests/test_scaffold.py::test_initialization_failure_cleans_destination[error0]
FAILED tests/test_scaffold.py::test_initialization_failure_cleans_destination[error1]
FAILED tests/test_cli.py::test_create_missing_plan_exits_one - AssertionError...
5 failed, 14 passed, 2 deselected in 2.75s
```


Command: `$env:PYTHONPATH='C:/Dev-Projects/plan/src'; python -m pytest tests/test_scaffold.py tests/test_cli.py -q`; exit code: 0.

```text
......................                                                   [100%]
22 passed in 8.80s
```


Command: `python -m pytest -m 'not slow' -q`; exit code: 0.

```text
...............................                                          [100%]
31 passed, 12 deselected in 2.04s
```


Command: `$env:PYTHONPATH='C:/Dev-Projects/plan/src'; python -m pytest -q`; exit code: 0.

```text
...........................................                              [100%]
43 passed in 15.21s
```


Command: `python -m ruff check .`; exit code: 0.

```text
All checks passed!
```


Command: `python -m ruff format --check .`; exit code: 0.

```text
21 files already formatted
```


Command: `lint-markdown check README.md docs/requirements.md CHANGELOG.md`; exit code: 1.

```text
CHANGELOG.md:23:34: MD019 [file-references-as-links] Repository file reference 'scripts/devops.py' in prose must be formatted as markdown link [filename](path)
**[WARN]**  Found 23 lint issues across 3 files.
CHANGELOG.md:30:110: MD019 [file-references-as-links] Repository file reference 'scripts/devops.py' in prose must be formatted as markdown link [filename](path)
CHANGELOG.md:37:16: MD019 [file-references-as-links] Repository file reference 'scripts/devops.py' in prose must be formatted as markdown link [filename](path)
CHANGELOG.md:71:56: MD018 [valid-external-links] External link 'https://github.com/gpellicciotta/dev-guidelines' failed validation: HTTP 404
CHANGELOG.md:89:4: MD008 [no-raw-urls] Raw URL found in prose: 'https://github.com/gpellicciotta/python-project-template'; enclose in markdown link
docs\requirements.md:7:1: MD015 [no-blank-line-after-subheading] Heading 'High-Level Goals' (H2) must not be followed by a blank line before content
docs\requirements.md:11:49: MD018 [valid-external-links] External link 'https://github.com/gpellicciotta/dev-guidelines' failed validation: HTTP 404
docs\requirements.md:49:1: MD015 [no-blank-line-after-subheading] Heading 'Technical Requirements' (H2) must not be followed by a blank line before content
docs\requirements.md:58:110: MD018 [valid-external-links] External link 'https://github.com/gpellicciotta/dev-guidelines/blob/main/guidelines/markdown-guidelines.md' failed validation: HTTP 429
README.md:7:26: MD018 [valid-external-links] External link 'https://github.com/gpellicciotta/dev-guidelines' failed validation: HTTP 404
README.md:9:1: MD015 [no-blank-line-after-subheading] Heading 'Directory Layout' (H2) must not be followed by a blank line before content
README.md:11:1: MD007 [code-block-language] Fenced code block lacks a language identifier
README.md:62:28: MD018 [valid-external-links] External link 'https://github.com/gpellicciotta/dev-guidelines' failed validation: HTTP 404
README.md:82:1: MD015 [no-blank-line-after-subheading] Heading 'Running Tests' (H2) must not be followed by a blank line before content
README.md:88:1: MD015 [no-blank-line-after-subheading] Heading 'Linting' (H2) must not be followed by a blank line before content
README.md:95:1: MD015 [no-blank-line-after-subheading] Heading 'CLI' (H2) must not be followed by a blank line before content
README.md:116:1: MD015 [no-blank-line-after-subheading] Heading 'Building the Packages' (H2) must not be followed by a blank line before content
README.md:124:73: MD019 [file-references-as-links] Repository file reference 'scripts/bootstrap-dev-environment.py' in prose must be formatted as markdown link [filename](path)
README.md:126:1: MD015 [no-blank-line-after-subheading] Heading 'Installation and Releases' (H2) must not be followed by a blank line before content
README.md:131:1: MD015 [no-blank-line-after-subheading] Heading 'Installing from a release' (H3) must not be followed by a blank line before content
README.md:153:1: MD015 [no-blank-line-after-subheading] Heading 'Starting a new project from this template' (H2) must not be followed by a blank line before content
README.md:161:1: MD016 [no-blank-line-before-list] Sentence introducing a list must not be followed by a blank line
README.md:165:3: MD019 [file-references-as-links] Repository file reference 'tests/test_core.py' in prose must be formatted as markdown link [filename](path)
**[ERROR]** Finished lint-markdown check in 2.7s with status: failed
```


The installed plan launcher uses an editable Python 3.12 user-site installation.
The isolated test home hides that installation; PYTHONPATH exposes its existing source checkout for integration tests.
Windows plan initialization creates a hard link; samefile verifies the link without assuming symlink privileges.
Markdown lint reports existing formatting issues and inaccessible external links outside the changed lines.
The standard isolated build passed; the optional no-isolation build lacked setuptools.

Command: `python -m build`; exit code: 0.

```text
[... 103 lines omitted ...]
adding 'myproject/core.py'
adding 'myproject/scaffold.py'
adding 'template_python-3.0.4rc0.dist-info/licenses/LICENSE.md'
adding 'template_python-3.0.4rc0.dist-info/METADATA'
adding 'template_python-3.0.4rc0.dist-info/WHEEL'
adding 'template_python-3.0.4rc0.dist-info/entry_points.txt'
adding 'template_python-3.0.4rc0.dist-info/top_level.txt'
adding 'template_python-3.0.4rc0.dist-info/RECORD'
removing build\bdist.win-amd64\wheel
Successfully built template_python-3.0.4rc0.tar.gz and template_python-3.0.4rc0-py3-none-any.whl
```
