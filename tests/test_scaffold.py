import os
from pathlib import Path
import shutil
import subprocess

import pytest

from myproject import scaffold
from myproject.scaffold import _ignore, create_project, find_template_root


def test_reset_pyproject_version_starts_at_first_minor(tmp_path):
    manifest = tmp_path / "pyproject.toml"
    manifest.write_text('[project]\nname = "demo"\nversion = "3.0.0-pre"\n', encoding="utf-8")
    scaffold._reset_pyproject_version(manifest)
    assert manifest.read_text(encoding="utf-8") == '[project]\nname = "demo"\nversion = "0.1.0-pre"\n'


def test_fresh_changelog_starts_at_first_minor_with_area_prefixed_entry():
    changelog = scaffold._fresh_changelog_md("Sample App")
    assert changelog.split("\n## ")[1:] == ["v0.1.0-pre\n- DevEx: Created the initial scaffold for the Sample App project.\n"]


@pytest.fixture
def installed_plan(monkeypatch):
    """Select an installed launcher that works with the isolated test home."""
    for directory in os.get_exec_path():
        executable = shutil.which("plan", path=directory)
        if executable and subprocess.run([executable, "--version"], capture_output=True).returncode == 0:
            monkeypatch.setenv("PATH", directory + os.pathsep + os.environ["PATH"])
            return executable
    pytest.fail("No installed plan launcher works with the isolated test home")


def test_ignore_excludes_logs_and_tool_caches():
    names = ["logs", ".pytest_cache", ".ruff_cache", ".mypy_cache", "src", "pyproject.toml"]
    assert _ignore(".", names) == {"logs", ".pytest_cache", ".ruff_cache", ".mypy_cache"}


def test_ignore_excludes_coverage_files():
    names = [".coverage", ".coverage.host.12345", "htmlcov", "README.md"]
    assert _ignore(".", names) == {".coverage", ".coverage.host.12345", "htmlcov"}


def _fake_template_root(root: Path) -> Path:
    (root / "src" / "myproject").mkdir(parents=True)
    (root / "src" / "myproject" / "cli.py").write_text("# myproject\n", encoding="utf-8")
    (root / "pyproject.toml").write_text('[project]\nname = "template-python"\nversion = "3.0.0-pre"\n', encoding="utf-8")
    (root / "CHANGELOG.md").write_text("## v3.0.0-pre\n- Template change.\n", encoding="utf-8")
    (root / ".gitignore").write_bytes(b".venv/\r\n.plan/\r\n/PLAN.md  \r\n/plan.code-workspace\r\nlogs/")
    return root


def test_find_template_root_without_plan_md(tmp_path):
    root = _fake_template_root(tmp_path / "template")
    assert find_template_root(root / "src" / "myproject") == root


@pytest.mark.slow
@pytest.mark.skipif(shutil.which("plan") is None, reason="plan is not installed")
def test_create_project_skips_template_plan_store(tmp_path, installed_plan):
    root = _fake_template_root(tmp_path / "template")
    (root / ".plan" / "config").mkdir(parents=True)
    (root / ".plan" / "config" / "store.json").write_text('{"format": 1}\n', encoding="utf-8")
    (root / ".plan" / "config" / "template-only.txt").write_text("inherited", encoding="utf-8")
    (root / ".plan" / "PLAN.md").write_text("- [ ] T0001 Template task.\n", encoding="utf-8")
    (root / ".plan" / "tasks").mkdir()
    (root / ".plan" / "tasks" / "T0001-template-task.md").write_text("# T0001\n", encoding="utf-8")
    (root / "plan.code-workspace").write_text("{}\n", encoding="utf-8")
    (root / "docs" / ".plan").mkdir(parents=True)
    (root / "docs" / ".plan" / "notes.md").write_text("Nested, not the plan store.\n", encoding="utf-8")

    destination = create_project("new-app", str(tmp_path / "out"), template_root=root)

    assert (destination / "plan.code-workspace").exists()
    assert (destination / ".plan" / "PLAN.md").exists()
    assert not (destination / ".plan" / "config" / "template-only.txt").exists()
    assert not (destination / ".plan" / "tasks" / "T0001-template-task.md").exists()
    assert "## Next Milestone" in (destination / "PLAN.md").read_text(encoding="utf-8")
    assert (destination / "docs" / ".plan" / "notes.md").is_file()
    assert (destination / ".gitignore").read_text(encoding="utf-8").splitlines() == [
        ".venv/",
        ".plan/",
        "/PLAN.md  ",
        "/plan.code-workspace",
        "logs/",
    ]


def test_create_runs_git_and_plan_in_destination(tmp_path, monkeypatch):
    root = _fake_template_root(tmp_path / "template")
    calls = []
    monkeypatch.setattr(scaffold.shutil, "which", lambda name: name)
    monkeypatch.setattr(scaffold.subprocess, "run", lambda args, **kwargs: calls.append((args, kwargs)))
    destination = create_project("demo", str(tmp_path / "out"), template_root=root)
    assert [args for args, _ in calls] == [["git", "init"], ["plan", "init", "--store", "branch"]]
    assert all(options["cwd"] == destination and options["check"] for _, options in calls)


def test_create_missing_plan_leaves_no_destination(tmp_path, monkeypatch):
    root = _fake_template_root(tmp_path / "template")
    monkeypatch.setattr(scaffold.shutil, "which", lambda name: None if name == "plan" else name)
    with pytest.raises(scaffold.ScaffoldError, match="plan.*PATH"):
        create_project("demo", str(tmp_path / "out"), template_root=root)
    assert not (tmp_path / "out" / "demo").exists()


def test_create_missing_git_leaves_no_destination(tmp_path, monkeypatch):
    root = _fake_template_root(tmp_path / "template")
    monkeypatch.setattr(scaffold.shutil, "which", lambda name: None if name == "git" else name)
    with pytest.raises(scaffold.ScaffoldError, match="git.*PATH"):
        create_project("demo", str(tmp_path / "out"), template_root=root)
    assert not (tmp_path / "out" / "demo").exists()


@pytest.mark.slow
def test_failed_plan_after_commit_removes_readonly_git_objects(tmp_path, monkeypatch):
    root = _fake_template_root(tmp_path / "template")
    tools = tmp_path / "tools"
    tools.mkdir()
    git = shutil.which("git")
    commit_proof = tmp_path / "commit-proof.txt"
    fake = tools / ("plan.cmd" if os.name == "nt" else "plan")
    commands = (
        f'"{git}" add .',
        f'"{git}" -c user.name=Test -c user.email=test@example.invalid commit -m initial',
        f'"{git}" rev-parse --verify HEAD > "{commit_proof}"',
    )
    fake.write_text(
        ("@echo off\n" if os.name == "nt" else "#!/bin/sh\n")
        + "\n".join(commands)
        + ("\nexit /b 1\n" if os.name == "nt" else "\nexit 1\n"),
        encoding="utf-8",
    )
    fake.chmod(0o755)
    monkeypatch.setenv("PATH", str(tools) + os.pathsep + os.environ["PATH"])
    with pytest.raises(scaffold.ScaffoldError, match="initialize"):
        create_project("demo", str(tmp_path / "out"), template_root=root)
    assert len(commit_proof.read_text().strip()) == 40
    assert not (tmp_path / "out" / "demo").exists()


@pytest.mark.slow
def test_create_with_fake_plan_on_path(tmp_path, monkeypatch):
    root = _fake_template_root(tmp_path / "template")
    tools = tmp_path / "tools"
    tools.mkdir()
    fake = tools / ("plan.cmd" if os.name == "nt" else "plan")
    fake.write_text(
        "@echo off\necho %* > plan-call.txt\ncd >> plan-call.txt\n"
        if os.name == "nt"
        else '#!/bin/sh\nprintf "%s\\n" "$*" "$PWD" > plan-call.txt\n',
        encoding="utf-8",
    )
    fake.chmod(0o755)
    monkeypatch.setenv("PATH", str(tools) + os.pathsep + os.environ["PATH"])
    destination = create_project("demo", str(tmp_path / "out"), template_root=root)
    lines = (destination / "plan-call.txt").read_text().splitlines()
    assert lines[0].strip() == "init --store branch"
    assert Path(lines[1]) == destination


@pytest.mark.parametrize("error", [OSError("cannot start"), subprocess.CalledProcessError(1, "plan", stderr="init failed")])
def test_initialization_failure_cleans_destination(tmp_path, monkeypatch, error):
    root = _fake_template_root(tmp_path / "template")
    monkeypatch.setattr(scaffold.shutil, "which", lambda name: name)

    def fail(*args, **kwargs):
        raise error

    monkeypatch.setattr(scaffold.subprocess, "run", fail)
    with pytest.raises(scaffold.ScaffoldError, match="initialize"):
        create_project("demo", str(tmp_path / "out"), template_root=root)
    assert not (tmp_path / "out" / "demo").exists()
