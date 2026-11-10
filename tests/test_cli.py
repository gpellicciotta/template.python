from myproject import __version__
from myproject.cli import main

VERSION_PREFIX = f"myproject v{__version__}"
COPYRIGHT_SUFFIX = " - Copyright (c) 2026 Giovanni Pellicciotta"


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
    assert "NAME defaults to 'wereld'" in out


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
    assert capsys.readouterr().out.strip() == "Hello, wereld"


def test_greet_verbose(capsys):
    for flag in ("--verbose", "-v"):
        assert main(["greet", "Gio", flag]) == 0
        out = capsys.readouterr().out
        assert "Starting myproject v" in out
        assert "Greeting target: Gio" in out
        assert "Hello, Gio" in out


def test_create_scaffolds_renamed_project(tmp_path, capsys):
    project_name = "sample-app"
    assert main(["create", project_name, "-o", str(tmp_path)]) == 0

    destination = tmp_path / project_name
    assert f"Created new project at {destination}" in capsys.readouterr().out
    assert destination.is_dir()
    assert (destination / "src" / "sample_app" / "cli.py").is_file()
    assert [p.name for p in (destination / "src").iterdir() if p.is_dir()] == ["sample_app"]

    pyproject = (destination / "pyproject.toml").read_text(encoding="utf-8")
    assert 'name = "sample-app"' in pyproject
    assert 'version = "0.0.1-pre"' in pyproject
    assert 'sample_app = "sample_app.cli:main"' in pyproject
    assert "[tool.ruff.lint]" in pyproject
    assert 'select = ["E4", "E7", "E9", "F"]' in pyproject
    assert 'license = "MIT"' in pyproject
    assert "https://github.com/gpellicciotta/sample-app" in pyproject
    assert "template.python" not in pyproject and "template-python" not in pyproject
    assert "support.python.git@v2.0.0" in pyproject

    readme = (destination / "README.md").read_text(encoding="utf-8")
    assert "Sample App" in readme

    license_file = destination / "LICENSE.md"
    assert license_file.is_file()

    changelog = (destination / "CHANGELOG.md").read_text(encoding="utf-8")
    assert "Initial scaffold of the Sample App project." in changelog
    assert "## v0.0.1-pre" in changelog
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
    assert (destination / ".plan" / "tasks" / ".gitkeep").is_file()
    assert [p.name for p in (destination / ".plan" / "tasks").iterdir()] == [".gitkeep"]
    assert (destination / ".github" / "workflows" / "ci.yml").is_file()
    assert not (destination / ".github" / "workflows" / "publish.yml").exists()
    gitignore = {line.strip() for line in (destination / ".gitignore").read_text(encoding="utf-8").splitlines()}
    assert ".venv/" in gitignore
    assert not gitignore & {".plan/", ".plan", "/.plan/", "/PLAN.md", "PLAN.md", "/plan.code-workspace"}
    assert "Installing from a release" in readme


def test_create_refuses_existing_destination(tmp_path, capsys):
    project_name = "dup-app"
    (tmp_path / project_name).mkdir()

    assert main(["create", project_name, "-o", str(tmp_path)]) == 1
    assert "already exists" in capsys.readouterr().err


def test_create_missing_project_name(capsys):
    assert main(["create"]) == 2
    assert "PROJECT_NAME" in capsys.readouterr().err


def test_invalid_args():
    assert main(["--invalid-option"]) == 2
    assert main(["unknown-action"]) == 2
    assert main(["greet", "--invalid-option"]) == 2
