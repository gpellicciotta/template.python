"""Regression coverage for the test suite's state isolation."""

import os
from pathlib import Path

import pytest

pytest_plugins = ["pytester"]


def test_home_and_configuration_are_temporary(tmp_path):
    assert Path.home() == tmp_path / "home"
    for name in ("HOME", "USERPROFILE", "APPDATA", "LOCALAPPDATA", "XDG_CONFIG_HOME"):
        directory = Path(os.environ[name])
        assert directory.is_relative_to(tmp_path)
        assert directory.is_dir()


@pytest.mark.slow
@pytest.mark.parametrize("target", ["home", "repository", "subprocess", "home-subprocess", "caught", "delete", "rename"])
def test_nested_session_rejects_real_state_writes(pytester, target):
    """Exercise the actual fixtures against disposable protected directories."""
    source = Path(__file__).with_name("conftest.py")
    assert source.exists(), "The isolation fixture has not been implemented"
    home = pytester.path / "real-home"
    repo = pytester.path / "repository"
    home.mkdir()
    repo.mkdir()
    pytester.makeconftest(
        source.read_text(encoding="utf-8") + f"\nREAL_HOME = Path({str(home)!r})\nREPO_ROOT = Path({str(repo)!r})\n"
    )
    destination = (home if target in {"home", "home-subprocess"} else repo) / "leaked.txt"
    if target in {"delete", "rename"}:
        destination.write_text("existing", encoding="utf-8")
    operation = f"Path({str(destination)!r}).write_text('leaked', encoding='utf-8')"
    if target in {"subprocess", "home-subprocess"}:
        operation = f"subprocess.run([sys.executable, '-c', {('from pathlib import Path; ' + operation)!r}], check=True)"
    elif target == "caught":
        operation = f"\n    try:\n        {operation}\n    except OSError:\n        pass"
    elif target == "delete":
        operation = f"Path({str(destination)!r}).unlink()"
    elif target == "rename":
        operation = f"Path({str(destination)!r}).rename({str(destination.with_suffix('.moved'))!r})"
    pytester.makepyfile(f"import subprocess, sys\nfrom pathlib import Path\ndef test_leak():\n    {operation}\n")
    result = pytester.runpytest_subprocess("-q", "-p", "no:cacheprovider", "--basetemp", str(pytester.path / "temp"))
    assert result.ret != 0
    assert "Real-state write guard" in result.stdout.str()


@pytest.mark.slow
def test_nested_session_isolates_tests_and_restores_environment(pytester):
    home = pytester.path / "real-home"
    repo = pytester.path / "repository"
    home.mkdir()
    repo.mkdir()
    pytester.makeconftest(
        Path(__file__).with_name("conftest.py").read_text(encoding="utf-8")
        + f"\nREAL_HOME = Path({str(home)!r})\nREPO_ROOT = Path({str(repo)!r})\n"
        + """
ORIGINAL = {key: os.environ.get(key) for key in ("HOME", "USERPROFILE", "APPDATA", "LOCALAPPDATA", "XDG_CONFIG_HOME")}
@pytest.fixture(scope="session", autouse=True)
def verify_restoration():
    yield
    assert ORIGINAL == {key: os.environ.get(key) for key in ORIGINAL}
"""
    )
    pytester.makepyfile("""
from pathlib import Path
def test_first():
    (Path.home() / "marker").write_text("first", encoding="utf-8")
def test_second():
    assert not (Path.home() / "marker").exists()
""")
    result = pytester.runpytest_subprocess("-q", "-p", "no:cacheprovider")
    result.assert_outcomes(passed=2)
