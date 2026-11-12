# Validation Proof

## Walkthrough & Validation

Command: `python -m pytest tests/test_scaffold.py -k 'first_minor' -q --tb=short`

Exit code: 1

```text
FF                                                                       [100%]
================================== FAILURES ===================================
_____________ test_reset_pyproject_version_starts_at_first_minor ______________
tests\test_scaffold.py:16: in test_reset_pyproject_version_starts_at_first_minor
    assert manifest.read_text(encoding="utf-8") == '[project]\nname = "demo"\nversion = "0.1.0-pre"\n'
E   assert '[project]\nn..."0.0.1-pre"\n' == '[project]\nn..."0.1.0-pre"\n'
E     
E       [project]
E       name = "demo"
E     - version = "0.1.0-pre"
E     ?               --
E     + version = "0.0.1-pre"
E     ?              ++
_____ test_fresh_changelog_starts_at_first_minor_with_area_prefixed_entry _____
tests\test_scaffold.py:21: in test_fresh_changelog_starts_at_first_minor_with_area_prefixed_entry
    assert changelog.split("\n## ")[1:] == [
E   AssertionError: assert ['v0.0.1-pre\...p project.\n'] == ['v0.1.0-pre\...p project.\n']
E     
E     At index 0 diff: 'v0.0.1-pre\n- Initial scaffold of the Sample App project.\n' != 'v0.1.0-pre\n- DevEx: Created the initial scaffold for the Sample App project.\n'
E     Use -v to get more diff
=========================== short test summary info ===========================
FAILED tests/test_scaffold.py::test_reset_pyproject_version_starts_at_first_minor
FAILED tests/test_scaffold.py::test_fresh_changelog_starts_at_first_minor_with_area_prefixed_entry
2 failed, 11 deselected in 0.40s
```

Command: `python -m pytest tests/test_cli.py -k test_create_scaffolds_renamed_project -q`

Exit code: 1

```text
[... 11 lines omitted ...]
        project_name = "sample-app"
        result = subprocess.run(
            [sys.executable, "-m", "myproject.cli", "create", project_name, "-o", str(tmp_path)],
            capture_output=True,
            text=True,
            env={
                **os.environ,
                "PYTHONPATH": str(Path(__file__).resolve().parents[1] / "src") + os.pathsep + os.environ.get("PYTHONPATH", ""),
            },
        )
        assert result.returncode == 0, result.stderr
    
        destination = tmp_path / project_name
        assert f"Created new project at {destination}" in result.stdout
        assert destination.is_dir()
        assert (destination / "src" / "sample_app" / "cli.py").is_file()
        package_init = (destination / "src" / "sample_app" / "__init__.py").read_text(encoding="utf-8")
        assert 'get_package_version("sample-app")' in package_init
        assert "template-python" not in package_init
        assert [p.name for p in (destination / "src").iterdir() if p.is_dir()] == ["sample_app"]
    
        pyproject = (destination / "pyproject.toml").read_text(encoding="utf-8")
        assert 'name = "sample-app"' in pyproject
>       assert 'version = "0.1.0-pre"' in pyproject
E       assert 'version = "0.1.0-pre"' in '[build-system]\nrequires = ["setuptools>=77"]\nbuild-backend = "setuptools.build_meta"\n\n[project]\nname = "sample-a...npythonpath = ["src"]\nmarkers = ["slow: integration tests that run git or subprocesses; run with pytest -m slow"]\n\n'

tests\test_cli.py:120: AssertionError
=========================== short test summary info ===========================
FAILED tests/test_cli.py::test_create_scaffolds_renamed_project - assert 'ver...
1 failed, 15 deselected in 4.08s
```

Command: `python -m pytest -m 'not slow' -q`

Exit code: 0

```text
.....................................                                    [100%]
37 passed, 13 deselected in 1.62s
```

Command: `python -m pytest tests/test_cli.py tests/test_scaffold.py -m slow -q`

Exit code: 0

```text
....                                                                     [100%]
4 passed, 25 deselected in 4.66s
```

Command: `python -m ruff check src/myproject/scaffold.py tests/test_cli.py tests/test_scaffold.py`

Exit code: 0

```text
All checks passed!
```

Command: `python -m ruff format --check src/myproject/scaffold.py tests/test_cli.py tests/test_scaffold.py`

Exit code: 0

```text
3 files already formatted
```

Command: `lint-markdown check AGENTS.md docs/requirements.md CHANGELOG.md`

Exit code: 1

```text
docs\requirements.md:7:1: MD015 [no-blank-line-after-subheading] Heading 'High-Level Goals' (H2) must not be followed by a blank line before content
docs\requirements.md:11:49: MD018 [valid-external-links] External link 'https://github.com/gpellicciotta/dev-guidelines' failed validation: HTTP 404
docs\requirements.md:49:1: MD015 [no-blank-line-after-subheading] Heading 'Technical Requirements' (H2) must not be followed by a blank line before content
docs\requirements.md:58:110: MD018 [valid-external-links] External link 'https://github.com/gpellicciotta/dev-guidelines/blob/main/guidelines/markdown-guidelines.md' failed validation: HTTP 404
**[WARN]**  Found 4 lint issues across 3 files.
**[ERROR]** Finished lint-markdown check in 14.6s with status: failed
```

All four Markdown issues exist in the unchanged requirements baseline, confirmed with `git show HEAD:docs/requirements.md`.

