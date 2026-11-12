"""Creates a new project as a renamed copy of this template project."""

from __future__ import annotations

import os
import re
import shutil
import stat
import subprocess
from dataclasses import dataclass
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
#: Commands run in a new project once its files are in place, as executable name and arguments.
_INIT_COMMANDS = (("git", "init"), ("plan", "init", "--store", "branch"))
_PLAN_BLOCK = re.compile(r"<!-- BEGIN plan(?:\s[^>]*?)? -->.*?<!-- END plan -->\s*", flags=re.DOTALL)


class ScaffoldError(Exception):
    """Raised when a new project can't be scaffolded from this template."""


@dataclass(frozen=True)
class ScaffoldPlan:
    """Changes that `create_project` makes; `copied` paths are template-relative, the others destination-relative."""

    destination: Path
    template_root: Path
    package_name: str
    title: str
    executables: dict[str, str]
    copied: list[str]
    renamed: list[tuple[str, str]]
    rewritten: list[str]
    reset: list[str]
    commands: list[str]


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


def _template_files(template_root: Path) -> list[str]:
    """List the files `shutil.copytree` copies under the same ignore rules, as sorted template-relative paths."""
    ignore = _ignore_with_plan_store(template_root)
    files = []
    for directory, names, file_names in os.walk(template_root, followlinks=True):
        ignored = ignore(directory, names + file_names)
        names[:] = [name for name in names if name not in ignored]
        files += [(Path(directory) / name).relative_to(template_root).as_posix() for name in file_names if name not in ignored]
    return sorted(files)


def _read_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError, ValueError:
        return None


def _replace_all(text: str, replacements: list[tuple[str, str]]) -> str:
    for old, new in replacements:
        text = text.replace(old, new)
    return text


def _rewrite_text_files(root: Path, paths: list[str], replacements: list[tuple[str, str]]) -> None:
    for relative_path in paths:
        path = root / relative_path
        path.write_text(_replace_all(path.read_text(encoding="utf-8"), replacements), encoding="utf-8")


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
        "## v0.1.0-pre\n"
        f"- DevEx: Created the initial scaffold for the {title} project.\n"
    )


def _reset_pyproject_version(pyproject_path: Path) -> None:
    text = pyproject_path.read_text(encoding="utf-8")
    new_text = re.sub(r'(?m)^version = ".*"$', 'version = "0.1.0-pre"', text, count=1)
    pyproject_path.write_text(new_text, encoding="utf-8")


def _initialize_plan_store(destination: Path, executables: dict[str, str]) -> None:
    agents = destination / "AGENTS.md"
    if agents.is_file():
        text = agents.read_text(encoding="utf-8")
        new_text = _PLAN_BLOCK.sub("", text)
        if new_text != text:
            agents.write_text(new_text, encoding="utf-8")
    try:
        for name, *arguments in _INIT_COMMANDS:
            subprocess.run([executables[name], *arguments], cwd=destination, check=True, capture_output=True, text=True)
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


def _replacements(project_name: str, package_name: str, title: str) -> list[tuple[str, str]]:
    return [
        (REPO_SLUG, project_name),
        (PROJECT_SLUG, project_name),
        (TITLE_PLACEHOLDER, title),
        (PACKAGE_NAME, package_name),
    ]


def plan_project(project_name: str, output_dir: str = ".", template_root: Path | None = None) -> ScaffoldPlan:
    """Check `create_project`'s preconditions and list the changes it would make, without writing anything.

    Raises `ScaffoldError` on the same failed preconditions as `create_project`.
    """
    if template_root is None:
        template_root = find_template_root(Path(__file__).resolve())

    destination = Path(output_dir).resolve() / project_name
    if destination.exists():
        raise ScaffoldError(f"Destination {destination} already exists.")

    package_name = _to_package_name(project_name)
    title = project_name.replace("-", " ").replace("_", " ").title()
    executables = {}
    for name in ("plan", "git"):
        executable = shutil.which(name)
        if executable is None:
            raise ScaffoldError(f"The {name} executable must be on PATH to create a project.")
        executables[name] = executable

    renamed = [] if package_name == PACKAGE_NAME else [(f"src/{PACKAGE_NAME}", f"src/{package_name}")]
    replacements = _replacements(project_name, package_name, title)
    copied = _template_files(template_root)
    rewritten = []
    reset = ["CHANGELOG.md", "pyproject.toml"]
    for path in copied:
        target = path
        for old, new in renamed:
            if path.startswith(old + "/"):
                target = new + path[len(old) :]
        text = _read_text(template_root / path)
        if text is None:
            continue
        new_text = _replace_all(text, replacements)
        if new_text != text:
            rewritten.append(target)
        if target == "AGENTS.md" and _PLAN_BLOCK.search(new_text):
            reset.append(target)

    return ScaffoldPlan(
        destination=destination,
        template_root=template_root,
        package_name=package_name,
        title=title,
        executables=executables,
        copied=copied,
        renamed=renamed,
        rewritten=sorted(rewritten),
        reset=sorted(reset),
        commands=[" ".join(command) for command in _INIT_COMMANDS],
    )


def create_project(project_name: str, output_dir: str = ".", template_root: Path | None = None) -> Path:
    """Create a new project at `output_dir/project_name`, as a renamed copy of this template.

    Automates the manual steps documented in this template's README under "Starting a new project
    from this template": copy the tree, rename the `myproject` package, replace the `template-python` /
    `template.python` name placeholders throughout, reset the changelog and version, and initialize
    Git and a fresh branch-backed plan store. `plan_project` lists these changes without making them.
    """
    plan = plan_project(project_name, output_dir, template_root)
    destination = plan.destination

    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(plan.template_root, destination, ignore=_ignore_with_plan_store(plan.template_root))

    for old, new in plan.renamed:
        (destination / old).rename(destination / new)

    _rewrite_text_files(destination, plan.rewritten, _replacements(project_name, plan.package_name, plan.title))

    (destination / "CHANGELOG.md").write_text(_fresh_changelog_md(plan.title), encoding="utf-8")
    _reset_pyproject_version(destination / "pyproject.toml")
    _initialize_plan_store(destination, plan.executables)

    return destination
