"""Smoke tests for the standalone dev scripts under scripts/ - only exercises their version/help
actions, since setup() and deploy() run real subprocesses (pip, ruff, pytest, git) that are
exercised in `bootstrap-dev-environment.py` and `deploy-to-production.py` themselves, not here.
"""

import importlib.util
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


def load_devops():
    sys.path.insert(0, str(SCRIPTS_DIR))
    try:
        spec = importlib.util.spec_from_file_location("devops", SCRIPTS_DIR / "devops.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    finally:
        sys.path.remove(str(SCRIPTS_DIR))
    return module


def test_devops_help_lists_release_and_deploy_options():
    result = run_script("devops.py", "help")
    assert result.returncode == 0
    for text in ("release", "deploy", "--dry-run", "--skip-checks"):
        assert text in result.stdout


def test_devops_next_dev_version_bumps_patch():
    devops = load_devops()
    assert devops._release_version("2.0.1-pre") == "2.0.1"
    assert devops._next_dev_version("2.0.1") == "2.0.2-pre"


def test_devops_finalizes_and_extracts_changelog(tmp_path):
    devops = load_devops()
    changelog = tmp_path / "CHANGELOG.md"
    changelog.write_text(
        "# Changes\n\n---\n\n## v1.2.3-pre\n- DevEx: Did a thing.\n\n## v1.2.2 [2026-01-01]\n- Old.\n", encoding="utf-8"
    )
    assert devops._extract_changelog_notes(changelog, "1.2.3") == "- DevEx: Did a thing."
    devops._finalize_changelog_heading(changelog, "1.2.3", "2026-02-02", dry_run=False)
    assert "## v1.2.3 [released: 2026-02-02]" in changelog.read_text(encoding="utf-8")


def test_devops_deploy_refuses_pre_release_version():
    devops = load_devops()
    assert devops.check_not_pre_release("1.0.0-pre") is False
    assert devops.check_not_pre_release("1.0.0") is True


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
