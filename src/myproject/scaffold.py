"""Creates a new project as a renamed copy of this template project."""

from __future__ import annotations

import re
import shutil
from pathlib import Path

PACKAGE_NAME = "myproject"
PROJECT_SLUG = "template-python"
REPO_SLUG = "template.python"
TITLE_PLACEHOLDER = "Template Python"

_MARKER_FILES = ("pyproject.toml", "CHANGELOG.md")
# The template's plan data lives on a separate `plan` branch checked out at .plan/ (see .gitignore), so a clone
# has none of it; a new project gets fresh plan files instead and must track them.
_PLAN_STORE_NAMES = {".plan", "PLAN.md", "plan.code-workspace"}
_PLAN_STORE_IGNORES = {".plan/", "/PLAN.md", "/plan.code-workspace"}
_EXCLUDED_NAMES = {
    ".git",
    ".venv",
    "venv",
    "env",
    "__pycache__",
    "build",
    "dist",
    ".pytest_cache",
    ".ruff_cache",
    ".mypy_cache",
    "htmlcov",
    ".idea",
    ".vscode",
    "work",
    "logs",
}


class ScaffoldError(Exception):
    """Raised when a new project can't be scaffolded from this template."""


def find_template_root(start: Path) -> Path:
    """Walk up from `start` to find this template project's root directory."""
    for candidate in (start, *start.parents):
        has_markers = all((candidate / name).is_file() for name in _MARKER_FILES)
        if has_markers and (candidate / "src" / PACKAGE_NAME).is_dir():
            return candidate
    raise ScaffoldError(
        "Could not locate the template project root (expected pyproject.toml, CHANGELOG.md and "
        f"src/{PACKAGE_NAME}/ in a parent directory). `create` must be run against an editable install of "
        f"{REPO_SLUG}."
    )


def _to_package_name(project_name: str) -> str:
    package_name = re.sub(r"[^0-9a-zA-Z]+", "_", project_name).strip("_").lower()
    if not re.match(r"^[a-z_][a-z0-9_]*$", package_name):
        raise ScaffoldError(f"Cannot derive a valid Python package name from {project_name!r}.")
    return package_name


def _ignore(_dir: str, names: list[str]) -> set[str]:
    return {name for name in names if name in _EXCLUDED_NAMES or name.endswith(".egg-info") or name.startswith(".coverage")}


def _ignore_with_plan_store(template_root: Path):
    def ignore(directory: str, names: list[str]) -> set[str]:
        ignored = _ignore(directory, names)
        if Path(directory).resolve() == template_root.resolve():
            ignored |= {name for name in names if name in _PLAN_STORE_NAMES}
        return ignored

    return ignore


def _track_plan_files(gitignore_path: Path) -> None:
    if not gitignore_path.is_file():
        return
    lines = gitignore_path.read_text(encoding="utf-8").splitlines(keepends=True)
    gitignore_path.write_text("".join(line for line in lines if line.strip() not in _PLAN_STORE_IGNORES), encoding="utf-8")


def _rewrite_text_files(root: Path, replacements: list[tuple[str, str]]) -> None:
    for path in root.rglob("*"):
        if path.is_dir():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError, ValueError:
            continue
        new_text = text
        for old, new in replacements:
            new_text = new_text.replace(old, new)
        if new_text != text:
            path.write_text(new_text, encoding="utf-8")


def _fresh_changelog_md(title: str) -> str:
    return (
        "# Versioned Changes\n\n"
        "A summarized overview of all changes, per version of this project.\n\n"
        "> Entries will be added in reverse chronological order, so with the most recent at the top.\n"
        ">\n"
        "> Status codes used are:\n"
        "> - `vX.Y.Z-pre` - actively being developed (suffix on the heading itself, not a bracket tag)\n"
        "> - `[{{date}}]` - frozen/finalized on {{date}}\n"
        "> - `[released: {{date}}]` - released to package manager or production on {{date}}\n"
        "> - `[broken]` - considered broken and not be used\n\n"
        "---\n\n"
        "## v0.0.1-pre\n"
        f"- Initial scaffold of the {title} project.\n"
    )


def _fresh_plan_md() -> str:
    return (
        "# Project Planning\n"
        "An overview of all tasks and their planning.\n\n"
        "---\n\n"
        "## Next Milestone\n"
        "*(Currently no tasks)*\n\n"
        "---\n\n"
        "## Backlog\n"
        "*(Currently no tasks)*\n"
    )


def _reset_pyproject_version(pyproject_path: Path) -> None:
    text = pyproject_path.read_text(encoding="utf-8")
    new_text = re.sub(r'(?m)^version = ".*"$', 'version = "0.0.1-pre"', text, count=1)
    pyproject_path.write_text(new_text, encoding="utf-8")


def _create_tasks_dir(tasks_dir: Path) -> None:
    tasks_dir.mkdir(parents=True, exist_ok=True)
    (tasks_dir / ".gitkeep").write_text("\n", encoding="utf-8")


def create_project(project_name: str, output_dir: str = ".", template_root: Path | None = None) -> Path:
    """Create a new project at `output_dir/project_name`, as a renamed copy of this template.

    Automates the manual steps documented in this template's README under "Starting a new project
    from this template": copy the tree, rename the `myproject` package, replace the `template-python` /
    `template.python` name placeholders throughout, and reset `CHANGELOG.md`, `PLAN.md`, `.plan/tasks/`,
    and `pyproject.toml`'s `version` — the new project starts its own history rather than inheriting the
    template's.
    """
    if template_root is None:
        template_root = find_template_root(Path(__file__).resolve())

    destination = Path(output_dir).resolve() / project_name
    if destination.exists():
        raise ScaffoldError(f"Destination {destination} already exists.")

    package_name = _to_package_name(project_name)
    title = project_name.replace("-", " ").replace("_", " ").title()

    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(template_root, destination, ignore=_ignore_with_plan_store(template_root))

    if package_name != PACKAGE_NAME:
        (destination / "src" / PACKAGE_NAME).rename(destination / "src" / package_name)

    _rewrite_text_files(
        destination,
        [
            (REPO_SLUG, project_name),
            (PROJECT_SLUG, project_name),
            (TITLE_PLACEHOLDER, title),
            (PACKAGE_NAME, package_name),
        ],
    )

    (destination / "CHANGELOG.md").write_text(_fresh_changelog_md(title), encoding="utf-8")
    (destination / "PLAN.md").write_text(_fresh_plan_md(), encoding="utf-8")
    _create_tasks_dir(destination / ".plan" / "tasks")
    _reset_pyproject_version(destination / "pyproject.toml")
    _track_plan_files(destination / ".gitignore")

    return destination
