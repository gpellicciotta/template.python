"""Smoke and unit tests for the standalone dev scripts under scripts/.

They exercise help, version, and the precondition paths only; lint, test, build, and release run real
subprocesses (pip, ruff, pytest, git, gh) that `bootstrap-dev-environment.py` and `devops.py check` exercise.
"""

import importlib.util
import subprocess
import sys
import tomllib
from pathlib import Path

import pytest
from support_python.devops import DevopsCli, PythonProject

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"


def test_parallel_test_dependencies():
    manifest = tomllib.loads((REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    dependencies = manifest["project"]["optional-dependencies"]["dev"]
    assert any(item.startswith("pytest-xdist>=") for item in dependencies)
    assert any(item.startswith("pytest-timeout>=") for item in dependencies)


@pytest.mark.slow
@pytest.mark.parametrize(
    "selection, expected, excluded", [((), "test_fast", "test_slow"), (("-m", "slow"), "test_slow", "test_fast")]
)
def test_suite_collection_selection(tmp_path, selection, expected, excluded):
    manifest = tomllib.loads((REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    options = manifest["tool"]["pytest"]["ini_options"]
    (tmp_path / "pytest.ini").write_text(
        "[pytest]\naddopts = " + options.get("addopts", "") + "\nmarkers = slow: integration tests\n", encoding="utf-8"
    )
    (tmp_path / "test_selection.py").write_text(
        "import pytest\ndef test_fast(): pass\n@pytest.mark.slow\ndef test_slow(): pass\n", encoding="utf-8"
    )
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "--collect-only", "-q", "-n", "0", *selection],
        cwd=tmp_path,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert f"test_selection.py::{expected}" in result.stdout
    assert f"test_selection.py::{excluded}" not in result.stdout


def run_script(name: str, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / name), *args],
        cwd=str(REPO_ROOT),
        check=False,
        capture_output=True,
        text=True,
    )


def load_devops():
    spec = importlib.util.spec_from_file_location("devops", SCRIPTS_DIR / "devops.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_bootstrap(monkeypatch):
    monkeypatch.syspath_prepend(str(SCRIPTS_DIR))
    spec = importlib.util.spec_from_file_location("bootstrap", SCRIPTS_DIR / "bootstrap-dev-environment.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def bootstrap(monkeypatch):
    module = load_bootstrap(monkeypatch)
    calls = []
    monkeypatch.setattr(module, "setup", lambda verbose=False: calls.append(verbose) or 0)
    module.setup_calls = calls
    return module


def test_bootstrap_short_v_means_verbose_not_version(bootstrap, capsys):
    assert bootstrap.main(["-v"]) == 0
    assert bootstrap.setup_calls == [True]
    assert " v" not in capsys.readouterr().out


def test_bootstrap_version_uses_myproject_copyright(bootstrap, capsys):
    from myproject.cli import COPYRIGHT

    assert bootstrap.main(["--version"]) == 0
    assert bootstrap.main(["version"]) == 0
    expected = f"bootstrap-dev-environment v{bootstrap.get_project_version()} - {COPYRIGHT}\n"
    assert capsys.readouterr().out == expected * 2
    assert bootstrap.setup_calls == []


def test_bootstrap_help_lists_standard_sections(bootstrap, capsys):
    assert bootstrap.main(["help"]) == 0
    out = capsys.readouterr().out
    assert out.startswith("bootstrap-dev-environment v")
    for section in ("Usage:", "Actions:", "Options:", "Exit codes:"):
        assert f"\n{section}\n" in out
    assert "-v, --verbose" in out
    assert "Detailed Action Descriptions:" not in out


def test_bootstrap_help_verbose_adds_details_and_exit_codes(bootstrap, capsys):
    assert bootstrap.main(["help", "--verbose"]) == 0
    assert bootstrap.main(["--help", "-v"]) == 0
    out = capsys.readouterr().out
    first, second = out[: len(out) // 2], out[len(out) // 2 :]
    assert first == second
    assert "Detailed Action Descriptions:" in first
    exit_codes = first.split("Exit codes:\n")[1].split("\n\n")[0]
    assert [line.split()[0] for line in exit_codes.splitlines()] == ["0", "1", "2"]
    assert bootstrap.setup_calls == []


def test_bootstrap_invalid_arguments_exit_2_on_stderr(bootstrap, capsys):
    with pytest.raises(SystemExit) as exc:
        bootstrap.main(["unknown"])
    assert exc.value.code == 2
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err.startswith("**[ERROR]** ")
    assert "Usage: bootstrap-dev-environment" in captured.err


def test_bootstrap_failed_step_reports_error_on_stderr(monkeypatch, capsys):
    module = load_bootstrap(monkeypatch)
    monkeypatch.setattr(module.subprocess, "run", lambda *args, **kwargs: subprocess.CompletedProcess(args, 3))
    assert module.run_step("Linting", ["ruff", "check", "."]) is False
    captured = capsys.readouterr()
    assert "**[ERROR]** Linting failed (exit code 3)" in captured.err
    assert "failed" not in captured.out


def test_bootstrap_verbose_step_prints_command_line(monkeypatch, capsys):
    module = load_bootstrap(monkeypatch)
    monkeypatch.setattr(module.subprocess, "run", lambda *args, **kwargs: subprocess.CompletedProcess(args, 0))
    assert module.run_step("Linting", ["ruff", "check", "."]) is True
    assert "ruff check ." not in capsys.readouterr().out
    assert module.run_step("Linting", ["ruff", "check", "."], verbose=True) is True
    assert "$ ruff check ." in capsys.readouterr().out


def test_cli_common_has_no_duplicate_version_reader(monkeypatch):
    monkeypatch.syspath_prepend(str(SCRIPTS_DIR))
    import _cli_common

    assert not hasattr(_cli_common, "get_project_version")


@pytest.mark.slow
def test_bootstrap_version():
    result = run_script("bootstrap-dev-environment.py", "--version")
    assert result.returncode == 0
    assert "bootstrap-dev-environment v" in result.stdout


@pytest.mark.slow
def test_bootstrap_help_verbose_subprocess():
    result = run_script("bootstrap-dev-environment.py", "help", "--verbose")
    assert result.returncode == 0, result.stderr
    for section in ("Usage:", "Actions:", "Options:", "Exit codes:", "Detailed Action Descriptions:"):
        assert f"\n{section}\n" in result.stdout
    assert result.stderr == ""


def test_requirements_pin_support_python_v3():
    requirements = (SCRIPTS_DIR / "requirements.txt").read_text(encoding="utf-8")
    assert "support-python @ git+https://github.com/gpellicciotta/support.python.git@v3.0.0" in requirements


def test_devops_builds_devops_cli_over_python_project():
    cli = load_devops().build_cli()
    assert isinstance(cli, DevopsCli)
    assert isinstance(cli.project, PythonProject)
    assert Path(cli.project.root).resolve() == REPO_ROOT
    assert cli.run(["deploy"]) == 2


@pytest.mark.slow
def test_devops_help_lists_actions():
    result = run_script("devops.py", "help")
    assert result.returncode == 0
    action_lines = {line.split()[0] for line in result.stdout.splitlines() if line.startswith("  ") and line.strip()}
    assert {"lint", "format", "test", "build", "check", "clean", "versions", "release"} <= action_lines
    assert "deploy" not in action_lines
    assert "deploy" not in result.stdout


@pytest.mark.slow
def test_devops_version():
    result = run_script("devops.py", "--version")
    assert result.returncode == 0
    assert result.stdout.startswith("devops v")


@pytest.mark.slow
def test_devops_rejects_unconfigured_deploy():
    result = run_script("devops.py", "deploy")
    assert result.returncode == 2
    assert "deploy" in result.stderr


def _fake_call(calls):
    def call(command, env):
        calls.append((command, env))
        return 7

    return call


def test_devops_main_reexecutes_once_with_venv_python(tmp_path, monkeypatch):
    devops = load_devops()
    fake_python = tmp_path / "python.exe"
    fake_python.write_text("", encoding="utf-8")
    calls = []
    monkeypatch.setattr(devops, "venv_python", lambda: fake_python)
    monkeypatch.setattr(devops.sys, "prefix", str(tmp_path / "other-env"))
    monkeypatch.delenv(devops.REEXEC_ENV, raising=False)
    monkeypatch.setattr(devops.subprocess, "call", _fake_call(calls))

    assert devops.main(["versions", "--verbose"]) == 7
    [(command, env)] = calls
    assert command[0] == str(fake_python)
    assert command[2:] == ["versions", "--verbose"]
    assert env[devops.REEXEC_ENV] == "1"


def test_devops_main_runs_in_process_when_reexecuted_or_without_venv(tmp_path, monkeypatch, capsys):
    devops = load_devops()
    calls = []
    monkeypatch.setattr(devops.subprocess, "call", _fake_call(calls))
    monkeypatch.setattr(devops.sys, "prefix", str(tmp_path / "other-env"))

    monkeypatch.setattr(devops, "venv_python", lambda: tmp_path / "missing-python.exe")
    assert devops.main(["--version"]) == 0

    fake_python = tmp_path / "python.exe"
    fake_python.write_text("", encoding="utf-8")
    monkeypatch.setattr(devops, "venv_python", lambda: fake_python)
    monkeypatch.setenv(devops.REEXEC_ENV, "1")
    assert devops.main(["--version"]) == 0

    assert calls == []
    assert devops.REEXEC_ENV not in devops.os.environ
    assert capsys.readouterr().out.count("devops v") == 2


def test_devops_fallback_errors_on_stderr(tmp_path, monkeypatch, capsys):
    devops = load_devops()
    monkeypatch.setattr(devops, "venv_python", lambda: tmp_path / "missing-python.exe")

    def missing():
        raise ImportError("No module named 'support_python'")

    monkeypatch.setattr(devops, "build_cli", missing)
    assert devops.main(["check"]) == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err.startswith("**[ERROR]** No module named 'support_python'")


def test_scripts_are_ascii_only_for_legacy_windows_consoles():
    offenders = [p.name for p in SCRIPTS_DIR.glob("*.py") if not p.read_text(encoding="utf-8").isascii()]
    assert offenders == []
