"""Creates a new project as a renamed copy of this template project."""

from __future__ import annotations

import re
import shutil
import stat
import subprocess
from pathlib import Path

#: Python package placeholder replaced with the new project's import name.
PACKAGE_NAME = "myproject"
#: Distribution name placeholder replaced with the new project's slug.
PROJECT_SLUG = "template-python"
#: Repository name placeholder replaced with the new project's slug.
REPO_SLUG = "template.python"
#: Display title placeholder replaced with the new project's title.
TITLE_PLACEHOLDER = "Template Python"

_MARKER_FILES = ("pyproject.toml", "CHANGELOG.md")
# The template's plan data lives on a separate `plan` branch checked out at .plan/ (see .gitignore), so a clone
# has none of it; plan initializes a fresh branch-backed store in each new project.
_PLAN_STORE_NAMES = {".plan", "PLAN.md", "plan.code-workspace"}
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


def _reset_pyproject_version(pyproject_path: Path) -> None:
    text = pyproject_path.read_text(encoding="utf-8")
    new_text = re.sub(r'(?m)^version = ".*"$', 'version = "0.0.1-pre"', text, count=1)
    pyproject_path.write_text(new_text, encoding="utf-8")


def _initialize_plan_store(destination: Path, git: str, plan: str) -> None:
    agents = destination / "AGENTS.md"
    if agents.is_file():
        text = agents.read_text(encoding="utf-8")
        text = re.sub(r"<!-- BEGIN plan(?:\s[^>]*?)? -->.*?<!-- END plan -->\s*", "", text, flags=re.DOTALL)
        agents.write_text(text, encoding="utf-8")
    try:
        subprocess.run([git, "init"], cwd=destination, check=True, capture_output=True, text=True)
        subprocess.run([plan, "init", "--store", "branch"], cwd=destination, check=True, capture_output=True, text=True)
    except (OSError, subprocess.CalledProcessError) as exc:
        detail = exc.stderr if isinstance(exc, subprocess.CalledProcessError) else str(exc)
        shutil.rmtree(destination, onexc=_remove_readonly)
        raise ScaffoldError(f"Could not initialize the new project's plan store: {detail}") from exc


def _remove_readonly(function, path: str, exc: OSError) -> None:
    """Retry removal after clearing Git's read-only object-file attribute."""
    if not isinstance(exc, PermissionError):
        raise exc
    Path(path).chmod(stat.S_IRUSR | stat.S_IWUSR)
    function(path)


def create_project(project_name: str, output_dir: str = ".", template_root: Path | None = None) -> Path:
    """Create a new project at `output_dir/project_name`, as a renamed copy of this template.

    Automates the manual steps documented in this template's README under "Starting a new project
    from this template": copy the tree, rename the `myproject` package, replace the `template-python` /
    `template.python` name placeholders throughout, reset the changelog and version, and initialize
    Git and a fresh branch-backed plan store.
    """
    if template_root is None:
        template_root = find_template_root(Path(__file__).resolve())

    destination = Path(output_dir).resolve() / project_name
    if destination.exists():
        raise ScaffoldError(f"Destination {destination} already exists.")

    package_name = _to_package_name(project_name)
    title = project_name.replace("-", " ").replace("_", " ").title()
    plan = shutil.which("plan")
    if plan is None:
        raise ScaffoldError("The plan executable must be on PATH to create a project.")
    git = shutil.which("git")
    if git is None:
        raise ScaffoldError("The git executable must be on PATH to create a project.")

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
    _reset_pyproject_version(destination / "pyproject.toml")
    _initialize_plan_store(destination, git, plan)

    return destination
