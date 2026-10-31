"""Smoke tests for the standalone dev scripts under scripts/ - only exercises their version/help
actions, since setup() and deploy() run real subprocesses (pip, ruff, pytest, git) that are
exercised in `bootstrap-dev-environment.py` and `deploy-to-production.py` themselves, not here.
"""

import subprocess
import sys
from pathlib import Path

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


def test_bootstrap_version():
    result = run_script("bootstrap-dev-environment.py", "--version")
    assert result.returncode == 0
    assert "bootstrap-dev-environment v" in result.stdout


def test_bootstrap_help():
    result = run_script("bootstrap-dev-environment.py", "help")
    assert result.returncode == 0
    assert "usage:" in result.stdout
    assert "Exit codes:" in result.stdout


def test_deploy_version():
    result = run_script("deploy-to-production.py", "--version")
    assert result.returncode == 0
    assert "deploy-to-production v" in result.stdout


def test_deploy_help():
    result = run_script("deploy-to-production.py", "help")
    assert result.returncode == 0
    assert "usage:" in result.stdout
    assert "--dry-run" in result.stdout
    assert "Exit codes:" in result.stdout


def test_devops_version():
    result = run_script("devops.py", "--version")
    assert result.returncode == 0
    assert "devops v" in result.stdout


def test_devops_help():
    result = run_script("devops.py", "help")
    assert result.returncode == 0
    assert "lint" in result.stdout
    assert "Exit codes:" in result.stdout


def test_scripts_are_ascii_only_for_legacy_windows_consoles():
    offenders = [p.name for p in SCRIPTS_DIR.glob("*.py") if not p.read_text(encoding="utf-8").isascii()]
    assert offenders == []
