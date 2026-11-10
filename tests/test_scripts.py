"""Smoke and unit tests for the standalone dev scripts under scripts/.

They exercise help, version, and the precondition paths only; lint, test, build, and release run real
subprocesses (pip, ruff, pytest, git, gh) that `bootstrap-dev-environment.py` and `devops.py check` exercise.
"""

import importlib.util
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

from support_python import CliLogger
from support_python.devops import DevopsCli, PythonProject

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"


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


def test_bootstrap_version():
    result = run_script("bootstrap-dev-environment.py", "--version")
    assert result.returncode == 0
    assert "bootstrap-dev-environment v" in result.stdout


def test_bootstrap_help():
    result = run_script("bootstrap-dev-environment.py", "help")
    assert result.returncode == 0
    assert "usage:" in result.stdout
    assert "Exit codes:" in result.stdout


def test_requirements_pin_support_python_v2():
    requirements = (SCRIPTS_DIR / "requirements.txt").read_text(encoding="utf-8")
    assert "support-python @ git+https://github.com/gpellicciotta/support.python.git@v2.0.0" in requirements


def test_devops_builds_devops_cli_over_python_project():
    cli = load_devops().build_cli()
    assert isinstance(cli, DevopsCli)
    assert isinstance(cli.project, PythonProject)
    assert Path(cli.project.root).resolve() == REPO_ROOT


def test_devops_help_lists_actions():
    result = run_script("devops.py", "help")
    assert result.returncode == 0
    action_lines = {line.split()[0] for line in result.stdout.splitlines() if line.startswith("  ") and line.strip()}
    assert {"lint", "format", "test", "build", "check", "clean", "versions", "release", "deploy"} <= action_lines
    assert "deploy operations of this project" in result.stdout


def test_devops_version():
    result = run_script("devops.py", "--version")
    assert result.returncode == 0
    assert result.stdout.startswith("devops v")


def test_devops_deploy_refuses_pre_release_version(tmp_path, capsys):
    (tmp_path / "pyproject.toml").write_text('[project]\nname = "demo"\nversion = "1.0.0-pre"\n', encoding="utf-8")
    git = [
        "git",
        "-c",
        "user.name=test",
        "-c",
        "user.email=test@example.com",
        "-c",
        "commit.gpgsign=false",
        "-c",
        "core.hooksPath=",
    ]
    for args in (["init", "-q"], ["add", "."], ["commit", "-q", "-m", "init"]):
        subprocess.run([*git, *args], cwd=tmp_path, check=True)

    assert load_devops().build_cli(tmp_path).run(["deploy", "--dry-run"]) == 1
    assert "1.0.0-pre is still in development" in capsys.readouterr().err


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


def test_devops_deploy_step_reports_missing_target(capsys):
    context = SimpleNamespace(logger=CliLogger(), dry_run=False)
    assert load_devops().no_deployment_target(context) is False
    assert "No production deployment target" in capsys.readouterr().err


def test_scripts_are_ascii_only_for_legacy_windows_consoles():
    offenders = [p.name for p in SCRIPTS_DIR.glob("*.py") if not p.read_text(encoding="utf-8").isascii()]
    assert offenders == []
