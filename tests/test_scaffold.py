from pathlib import Path

from myproject.scaffold import _ignore, create_project, find_template_root


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


def test_create_project_skips_template_plan_store(tmp_path):
    root = _fake_template_root(tmp_path / "template")
    (root / ".plan" / "config").mkdir(parents=True)
    (root / ".plan" / "config" / "store.json").write_text('{"format": 1}\n', encoding="utf-8")
    (root / ".plan" / "PLAN.md").write_text("- [ ] T0001 Template task.\n", encoding="utf-8")
    (root / ".plan" / "tasks").mkdir()
    (root / ".plan" / "tasks" / "T0001-template-task.md").write_text("# T0001\n", encoding="utf-8")
    (root / "plan.code-workspace").write_text("{}\n", encoding="utf-8")
    (root / "docs" / ".plan").mkdir(parents=True)
    (root / "docs" / ".plan" / "notes.md").write_text("Nested, not the plan store.\n", encoding="utf-8")

    destination = create_project("new-app", str(tmp_path / "out"), template_root=root)

    assert not (destination / "plan.code-workspace").exists()
    assert not (destination / ".plan" / "PLAN.md").exists()
    assert not (destination / ".plan" / "config").exists()
    assert [p.name for p in (destination / ".plan" / "tasks").iterdir()] == [".gitkeep"]
    assert "## Next Milestone" in (destination / "PLAN.md").read_text(encoding="utf-8")
    assert (destination / "docs" / ".plan" / "notes.md").is_file()
    assert (destination / ".gitignore").read_text(encoding="utf-8").splitlines() == [".venv/", "logs/"]
