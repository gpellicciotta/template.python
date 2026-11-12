"""Run the installed `myproject` console script end to end with realistic arguments."""

from pathlib import Path
import shutil
import subprocess
import sys

import pytest
from support_python import get_package_version

from test_scaffold import installed_plan as installed_plan

pytestmark = [pytest.mark.slow, pytest.mark.timeout(120)]

SCRIPTS_DIR = Path(sys.executable).parent
VERSION_PREFIX = f"myproject v{get_package_version('template-python')}"
COPYRIGHT_SUFFIX = " - Copyright (c) 2026 Giovanni Pellicciotta"


@pytest.fixture
def myproject():
    """Return the console script installed next to the running interpreter."""
    executable = shutil.which("myproject", path=str(SCRIPTS_DIR))
    if executable is None:
        pytest.fail(f"The myproject console script is not installed in {SCRIPTS_DIR}")
    return executable


def run(executable, *args, cwd=None):
    return subprocess.run([executable, *args], capture_output=True, text=True, cwd=cwd, timeout=100)


def test_version(myproject):
    result = run(myproject, "--version")
    assert result.returncode == 0, result.stderr
    assert result.stdout.startswith(VERSION_PREFIX)
    assert result.stdout.strip().endswith(COPYRIGHT_SUFFIX)
    assert result.stderr == ""


def test_help(myproject):
    result = run(myproject, "help")
    assert result.returncode == 0, result.stderr
    assert result.stdout.startswith(VERSION_PREFIX)
    for text in ("Usage:", "Actions:", "Exit codes:", "greet", "create", "myproject create PROJECT_NAME [-o DIR]"):
        assert text in result.stdout


def test_greet(myproject):
    result = run(myproject, "greet", "Gio")
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == "Hello, Gio"
    assert result.stderr == ""


@pytest.mark.skipif(shutil.which("plan") is None, reason="plan is not installed")
def test_create_then_repeat(myproject, tmp_path, installed_plan):
    destination = tmp_path / "demo"

    result = run(myproject, "create", "demo", "-o", str(tmp_path), cwd=tmp_path)
    assert result.returncode == 0, result.stderr
    assert f"Created new project at {destination}" in result.stdout
    assert (destination / "src" / "demo" / "cli.py").is_file()
    assert 'name = "demo"' in (destination / "pyproject.toml").read_text(encoding="utf-8")

    repeated = run(myproject, "create", "demo", "-o", str(tmp_path), cwd=tmp_path)
    assert repeated.returncode == 1
    assert "already exists" in repeated.stderr
    assert "Created new project" not in repeated.stdout


def test_invalid_option(myproject):
    result = run(myproject, "--bogus")
    assert result.returncode == 2
    assert result.stdout == ""
    assert "Unknown subcommand: '--bogus'" in result.stderr
    assert "Usage: myproject" in result.stderr
