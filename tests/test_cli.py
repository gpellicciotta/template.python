import importlib.metadata
import os
from pathlib import Path
import runpy
import shutil
import subprocess
import sys

import pytest
from support_python import get_package_version

from myproject.cli import main
from test_scaffold import installed_plan as installed_plan

VERSION_PREFIX = f"myproject v{get_package_version('template-python')}"
COPYRIGHT_SUFFIX = " - Copyright (c) 2026 Giovanni Pellicciotta"


@pytest.mark.parametrize("installed, expected", [("3.0.0rc0", "3.0.0-pre"), ("3.0.0", "3.0.0"), (None, "0.0.0+unknown")])
def test_package_version(installed, expected, monkeypatch):
    def metadata_version(distribution):
        assert distribution == "template-python"
        if installed is None:
            raise importlib.metadata.PackageNotFoundError(distribution)
        return installed

    monkeypatch.setattr(importlib.metadata, "version", metadata_version)
    assert runpy.run_module("myproject.__init__")["__version__"] == expected


def test_help_exits_zero(capsys):
    assert main(["help"]) == 0
    out = capsys.readouterr().out
    assert out.startswith(VERSION_PREFIX)
    for text in ("Usage:", "Actions:", "Options:", "Exit codes:", "greet", "create"):
        assert text in out


def test_help_flags(capsys):
    assert main(["-h"]) == 0
    assert "Usage:" in capsys.readouterr().out

    assert main(["--help"]) == 0
    assert "Usage:" in capsys.readouterr().out


def test_no_args_shows_help(capsys):
    assert main([]) == 0
    out = capsys.readouterr().out
    assert "Usage:" in out
    assert "Exit codes:" in out


def test_action_help_lists_create_options(capsys):
    assert main(["help", "create"]) == 0
    out = capsys.readouterr().out
    assert "myproject create PROJECT_NAME [-o DIR]" in out
    assert "-o, --output-dir" in out
    assert "PROJECT_NAME is the new project's name" in out


def test_action_help_describes_greet_argument(capsys):
    assert main(["help", "greet"]) == 0
    out = capsys.readouterr().out
    assert "myproject greet [NAME]" in out
    assert "NAME defaults to 'world'" in out


def test_version_action_and_flag(capsys):
    for argv in (["version"], ["--version"]):
        assert main(argv) == 0
        out = capsys.readouterr().out.strip()
        assert out.startswith(VERSION_PREFIX)
        assert out.endswith(COPYRIGHT_SUFFIX)


def test_greet(capsys):
    assert main(["greet", "Gio"]) == 0
    assert capsys.readouterr().out.strip() == "Hello, Gio"

    assert main(["greet"]) == 0
    assert capsys.readouterr().out.strip() == "Hello, world"


def test_greet_verbose(capsys):
    for flag in ("--verbose", "-v"):
        assert main(["greet", "Gio", flag]) == 0
        out = capsys.readouterr().out
        assert "Starting myproject v" in out
        assert "Greeting target: Gio" in out
        assert "Hello, Gio" in out


@pytest.mark.slow
@pytest.mark.skipif(shutil.which("plan") is None, reason="plan is not installed")
def test_create_scaffolds_renamed_project(tmp_path, capsys, installed_plan):
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
    assert 'version = "0.1.0-pre"' in pyproject
    assert 'sample_app = "sample_app.cli:main"' in pyproject
    assert "[tool.ruff.lint]" in pyproject
    assert 'select = ["E4", "E7", "E9", "F"]' in pyproject
    assert 'license = "MIT"' in pyproject
    assert "https://github.com/gpellicciotta/sample-app" in pyproject
    assert "template.python" not in pyproject and "template-python" not in pyproject
    assert "support.python.git@v3.0.0" in pyproject

    readme = (destination / "README.md").read_text(encoding="utf-8")
    assert "Sample App" in readme

    license_file = destination / "LICENSE.md"
    assert license_file.is_file()

    changelog = (destination / "CHANGELOG.md").read_text(encoding="utf-8")
    assert "- DevEx: Created the initial scaffold for the Sample App project." in changelog
    assert "## v0.1.0-pre" in changelog
    assert "in development" not in changelog
    assert "ruff" not in changelog

    plan = (destination / "PLAN.md").read_text(encoding="utf-8")
    assert "## Next Milestone" in plan
    assert "## Backlog" in plan

    assert (destination / "docs" / "requirements.md").is_file()
    assert (destination / "docs" / "devops.md").is_file()
    assert (destination / "docs" / "index.md").is_file()
    assert (destination / "docs" / "specs" / ".gitkeep").is_file()
    assert (destination / "docs" / "adrs" / ".gitkeep").is_file()
    assert (destination / "docs" / "issues" / ".gitkeep").is_file()
    assert (destination / ".plan" / "tasks").is_dir()
    assert (destination / "PLAN.md").samefile(destination / ".plan" / "PLAN.md")
    assert (
        subprocess.check_output(
            [shutil.which("git"), "branch", "--list", "plan", "--format=%(refname:short)"],
            cwd=destination,
            text=True,
        ).strip()
        == "plan"
    )
    subprocess.run([shutil.which("git"), "check-ignore", "PLAN.md"], cwd=destination, check=True, capture_output=True)
    subprocess.run([shutil.which("plan"), "tasks", "list"], cwd=destination, check=True, capture_output=True)
    agents = (destination / "AGENTS.md").read_text(encoding="utf-8")
    assert agents.count("<!-- BEGIN plan") == agents.count("<!-- END plan -->") == 1
    assert (destination / ".github" / "workflows" / "ci.yml").is_file()
    assert not (destination / ".github" / "workflows" / "publish.yml").exists()
    gitignore = {line.strip() for line in (destination / ".gitignore").read_text(encoding="utf-8").splitlines()}
    assert ".venv/" in gitignore
    assert {".plan/", "/PLAN.md", "/plan.code-workspace"} <= gitignore
    assert "Installing from a release" in readme


def test_create_refuses_existing_destination(tmp_path, capsys):
    project_name = "dup-app"
    (tmp_path / project_name).mkdir()

    assert main(["create", project_name, "-o", str(tmp_path)]) == 1
    assert "already exists" in capsys.readouterr().err


def test_create_missing_project_name(capsys):
    assert main(["create"]) == 2
    assert "PROJECT_NAME" in capsys.readouterr().err


def test_create_missing_plan_exits_one(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("PATH", "")
    assert main(["create", "demo", "-o", str(tmp_path)]) == 1
    assert "plan" in capsys.readouterr().err
    assert not (tmp_path / "demo").exists()


def test_invalid_args():
    assert main(["--invalid-option"]) == 2
    assert main(["unknown-action"]) == 2
    assert main(["greet", "--invalid-option"]) == 2
