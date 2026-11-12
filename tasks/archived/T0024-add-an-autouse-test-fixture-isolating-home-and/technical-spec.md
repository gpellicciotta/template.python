### Declared Files
- tests/conftest.py
- tests/test_isolation.py
- CHANGELOG.md

### Tests
- Unit: inside a test, `Path.home()` and `os.environ["APPDATA"]` resolve under that test's `tmp_path`.
- Unit: all five redirected directories exist, remain per-test, and restore their original environment values.
- Integration: a `pytester` run of a test that writes into the repository working tree makes the session fail.
- Integration: sandboxed sessions reject home writes, subprocess leaks, caught violations, deletions, and renames.
- Integration: run the complete suite with two pytest-xdist workers.

Completion check: `python -m pytest` passes and the `pytester` leak scenario fails as intended.

Size estimate: 3 files, 90 lines
