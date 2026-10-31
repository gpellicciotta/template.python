#!/usr/bin/env python3
"""Runs the typical operations of this project: lint, test, build, clean, release, and deploy.

Run `python scripts/bootstrap-dev-environment.py` first to create the virtual environment used by
lint, test, build, and check. The release and deploy actions run with the current interpreter.

Usage:
  python scripts/devops.py lint
  python scripts/devops.py test
  python scripts/devops.py build
  python scripts/devops.py check
  python scripts/devops.py clean
  python scripts/devops.py release [--dry-run] [--skip-checks]
  python scripts/devops.py deploy [--dry-run]
  python scripts/devops.py --version

`release` reads the version from pyproject.toml, extracts release notes from CHANGELOG.md, runs pre-flight
quality checks, finalizes version files if still at -pre, tags, pushes, creates the GitHub release, and opens
the next development version.

`deploy` is an example for projects derived from this template that deploy a running service. This template
has no deployment target, so it only validates preconditions and reports what it would do; replace the marked
section in `deploy()` with the project's actual deployment mechanism.
"""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

from _cli_common import build_action_parser, print_help, print_version

PROG = "devops"
DESCRIPTION = "Runs the lint, test, build, clean, release, and deploy operations of this project."
ACTIONS = ["lint", "test", "build", "check", "clean", "release", "deploy", "version", "help"]
VENV_ACTIONS = {"lint", "test", "build", "check"}
EXIT_CODES = [
    (0, "Success"),
    (1, "An operation or precondition failed, or the virtual environment is missing"),
    (2, "A release step failed"),
]
REPO_ROOT = Path(__file__).resolve().parent.parent
VENV_DIR = REPO_ROOT / ".venv"
DIST_DIR = REPO_ROOT / "dist"


def get_project_version() -> str:
    """Resolves the current project version from pyproject.toml."""
    content = (REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    match = re.search(r'^version\s*=\s*"([^"]+)"', content, re.MULTILINE)
    return match.group(1).strip() if match else "0.0.0+unknown"


def venv_python() -> Path:
    """Returns the path to the venv's own python executable, cross-platform."""
    return VENV_DIR / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")


def run(args: list) -> bool:
    """Runs one command in the repository root. Returns whether it succeeded."""
    print(f"[*] {' '.join(args)}", flush=True)
    return subprocess.run(args, cwd=str(REPO_ROOT), check=False).returncode == 0


def lint(python: str) -> bool:
    return run([python, "-m", "ruff", "check", "."]) and run([python, "-m", "ruff", "format", "--check", "."])


def test(python: str) -> bool:
    return run([python, "-m", "pytest", "-q"])


def build(python: str) -> bool:
    shutil.rmtree(DIST_DIR, ignore_errors=True)
    return run([python, "-m", "build", "-o", str(DIST_DIR)])


def clean(python: str) -> bool:
    shutil.rmtree(DIST_DIR, ignore_errors=True)
    shutil.rmtree(REPO_ROOT / "build", ignore_errors=True)
    return True


def _read_file(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _write_file(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8", newline="\n")


def _run_step(cmd: list[str], dry_run: bool) -> int:
    print(f"  $ {' '.join(cmd)}")
    if dry_run:
        return 0
    return subprocess.run(cmd, check=False, cwd=REPO_ROOT).returncode


def _run_capture(cmd: list[str]) -> str:
    return subprocess.run(cmd, capture_output=True, text=True, check=True, cwd=REPO_ROOT).stdout.strip()


def _set_version(pyproject: Path, new_version: str, dry_run: bool) -> None:
    new_text = re.sub(
        r'^(version\s*=\s*)"[^"]+"',
        f'\\1"{new_version}"',
        _read_file(pyproject),
        flags=re.MULTILINE,
    )
    print(f'  [edit] {pyproject.name}: version = "{new_version}"')
    if not dry_run:
        _write_file(pyproject, new_text)


def _release_version(ver: str) -> str:
    return ver.removesuffix("-pre")


def _next_dev_version(release_ver: str) -> str:
    parts = release_ver.split(".")
    parts[-1] = str(int(parts[-1]) + 1)
    return ".".join(parts) + "-pre"


def _extract_changelog_notes(changelog: Path, release_ver: str) -> str:
    text = _read_file(changelog)
    # Match the entire heading line: ## v3.1.2 or ## v3.1.2-pre or ## v3.1.2 [released: ...]
    m = re.search(rf"^## v{re.escape(release_ver)}[^\n]*\n?", text, re.MULTILINE)
    if not m:
        raise SystemExit(f"[ERROR] No '## v{release_ver}' section found in CHANGELOG.md\n        Add the heading before releasing.")
    start = m.end()
    next_h = re.search(r"^## ", text[start:], re.MULTILINE)
    end = start + next_h.start() if next_h else len(text)
    notes = text[start:end].strip()
    if not notes:
        raise SystemExit(f"[ERROR] Release notes for 'v{release_ver}' in CHANGELOG.md are empty.")
    return notes


def _finalize_changelog_heading(changelog: Path, release_ver: str, today: str, dry_run: bool) -> None:
    text = _read_file(changelog)
    replacement = f"## v{release_ver} [released: {today}]"
    new_text = re.sub(rf"^## v{re.escape(release_ver)}(?:-pre)?(?=\s*$)", replacement, text, flags=re.MULTILINE)
    if new_text == text:
        # Already finalized; verify the heading exists at all
        if not re.search(rf"^## v{re.escape(release_ver)}\b", text, re.MULTILINE):
            raise SystemExit(f"[ERROR] No '## v{release_ver}' or '## v{release_ver}-pre' in CHANGELOG.md")
        return
    print(f"  [edit] CHANGELOG.md: heading -> '{replacement}'")
    if not dry_run:
        _write_file(changelog, new_text)


def _prepend_dev_changelog_heading(changelog: Path, next_ver: str, dry_run: bool) -> None:
    text = _read_file(changelog)
    sep = "\n---\n"
    idx = text.find(sep)
    if idx == -1:
        raise SystemExit("[ERROR] Could not find '---' separator in CHANGELOG.md")
    insert_at = idx + len(sep)
    new_text = text[:insert_at] + f"\n## v{next_ver}\n" + text[insert_at:]
    print(f"  [edit] CHANGELOG.md: inserted '## v{next_ver}' heading")
    if not dry_run:
        _write_file(changelog, new_text)


def _get_github_repo() -> str:
    url = _run_capture(["git", "remote", "get-url", "origin"])
    m = re.search(r"github\.com[:/](.+?)(?:\.git)?$", url)
    if not m:
        raise SystemExit(f"[ERROR] Cannot parse GitHub repo from remote URL: {url}")
    return m.group(1)


def _get_dirty_files() -> set[str]:
    res = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True, check=True, cwd=REPO_ROOT)
    files = set()
    for line in res.stdout.splitlines():
        if not line:
            continue
        path_part = line[2:].strip()
        if " -> " in path_part:
            path_part = path_part.split(" -> ", 1)[1]
        if path_part:
            files.add(path_part)
    return files


def _validate_preconditions(release_ver: str, needs_finalize: bool) -> int:
    # 1. Check working tree
    dirty_files = _get_dirty_files()
    allowed = {"pyproject.toml", "CHANGELOG.md"} if needs_finalize else set()
    unexpected = dirty_files - allowed
    if unexpected:
        print(f"[ERROR] Uncommitted changes in: {', '.join(sorted(unexpected))}")
        print("        Commit or stash them before releasing.")
        return 1

    # 2. Check current branch
    try:
        branch = _run_capture(["git", "branch", "--show-current"])
        if branch != "main":
            print(f"[ERROR] Releases must be cut from branch 'main' (currently on '{branch}')")
            return 1
    except Exception as exc:
        print(f"[ERROR] Could not determine current git branch: {exc}")
        return 1

    # 3. Check gh CLI availability and authentication
    try:
        _run_capture(["gh", "--version"])
    except Exception:
        print("[ERROR] 'gh' CLI is not installed - see https://cli.github.com/")
        return 1

    auth_res = subprocess.run(["gh", "auth", "status"], capture_output=True, text=True, check=False)
    if auth_res.returncode != 0:
        print("[ERROR] 'gh' CLI is not authenticated - run 'gh auth login' before releasing.")
        return 1

    # 4. Check remote sync and tag existence
    try:
        _run_capture(["git", "fetch", "origin", "main", "--tags"])
    except Exception as exc:
        print(f"[ERROR] Failed to fetch origin: {exc}")
        return 1

    remote_tags = _run_capture(["git", "ls-remote", "--tags", "origin", f"refs/tags/v{release_ver}"])
    if remote_tags:
        print(f"[ERROR] Tag 'v{release_ver}' already exists on remote origin.")
        return 1

    # 5. Check if GitHub release already exists
    gh_view = subprocess.run(["gh", "release", "view", f"v{release_ver}"], capture_output=True, text=True, check=False)
    if gh_view.returncode == 0:
        print(f"[ERROR] GitHub release 'v{release_ver}' already exists.")
        return 1

    return 0


def _run_quality_checks() -> int:
    print("--- Pre-flight Quality Checks ---")
    checks = [
        ("Linter (ruff check)", [sys.executable, "-m", "ruff", "check", "."]),
        ("Formatter (ruff format)", [sys.executable, "-m", "ruff", "format", "--check", "."]),
        ("Test suite (pytest)", [sys.executable, "-m", "pytest"]),
        ("Package build (build)", [sys.executable, "-m", "build"]),
    ]
    for name, cmd in checks:
        print(f"  Running {name}...")
        res = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True, check=False)
        if res.returncode != 0:
            print(f"[ERROR] Quality check failed: {name}")
            if res.stdout:
                print(res.stdout.strip())
            if res.stderr:
                print(res.stderr.strip())
            return 1
        print(f"  [OK] {name} passed")
    print()
    return 0


def release(dry_run: bool, skip_checks: bool = False) -> int:
    pyproject = REPO_ROOT / "pyproject.toml"
    changelog = REPO_ROOT / "CHANGELOG.md"
    today = date.today().strftime("%Y-%m-%d")

    current_ver = get_project_version()
    release_ver = _release_version(current_ver)
    next_dev_ver = _next_dev_version(release_ver)
    needs_finalize = current_ver.endswith("-pre")

    print(f"Release version : v{release_ver}")
    print(f"Next dev version: v{next_dev_ver}")
    print(f"Dry run         : {dry_run}")
    print()

    # Precondition validation
    precondition_code = _validate_preconditions(release_ver, needs_finalize)
    if precondition_code != 0:
        return precondition_code

    # Quality checks (run early before modifying anything)
    if not skip_checks and not dry_run:
        quality_code = _run_quality_checks()
        if quality_code != 0:
            return quality_code

    repo = _get_github_repo()
    notes = _extract_changelog_notes(changelog, release_ver)
    note_lines = notes.splitlines()
    print(f"GitHub repo     : {repo}")
    print(f"Release notes   : {len(note_lines)} lines")
    for line in note_lines[:6]:
        print(f"  {line}")
    if len(note_lines) > 6:
        print(f"  ... ({len(note_lines) - 6} more lines)")
    print()

    # Step 1: finalize -pre if needed
    if needs_finalize:
        print("--- Step 1: Finalize version ---")
        _finalize_changelog_heading(changelog, release_ver, today, dry_run)
        _set_version(pyproject, release_ver, dry_run)
        if _run_step(["git", "add", "CHANGELOG.md", "pyproject.toml"], dry_run) != 0:
            return 2
        if _run_step(["git", "commit", "-m", f"Released v{release_ver}."], dry_run) != 0:
            return 2
        print()

    # Step 2: tag and push
    print(f"--- Step 2: Tag and push v{release_ver} ---")
    if _run_step(["git", "tag", "-f", f"v{release_ver}"], dry_run) != 0:
        return 2
    if _run_step(["git", "push", "origin", "main"], dry_run) != 0:
        return 2
    if _run_step(["git", "push", "origin", f"v{release_ver}"], dry_run) != 0:
        return 2
    print()

    # Step 3: GitHub release
    print(f"--- Step 3: Create GitHub release v{release_ver} ---")
    if _run_step(["gh", "release", "create", f"v{release_ver}", "--title", f"v{release_ver}", "--notes", notes], dry_run) != 0:
        return 2
    print()

    # Step 4: open next dev version
    print(f"--- Step 4: Open v{next_dev_ver} ---")
    _prepend_dev_changelog_heading(changelog, next_dev_ver, dry_run)
    _set_version(pyproject, next_dev_ver, dry_run)
    if _run_step(["git", "add", "CHANGELOG.md", "pyproject.toml"], dry_run) != 0:
        return 2
    if _run_step(["git", "commit", "-m", f"Opened v{next_dev_ver} development after releasing v{release_ver}."], dry_run) != 0:
        return 2
    if _run_step(["git", "push", "origin", "main"], dry_run) != 0:
        return 2
    print()

    if dry_run:
        print("[DRY RUN] No changes were made.")
    else:
        print(f"[OK] v{release_ver} released - https://github.com/{repo}/releases/tag/v{release_ver}")
    return 0


def check_clean_git_tree() -> bool:
    """Returns whether the working tree has no uncommitted changes."""
    result = subprocess.run(["git", "status", "--porcelain"], cwd=str(REPO_ROOT), check=False, capture_output=True, text=True)
    if result.stdout.strip():
        print("[!] Working tree has uncommitted changes - commit or stash before deploying.")
        return False
    return True


def check_not_pre_release(version: str) -> bool:
    """Returns whether the current version is a finalized release, not an in-development '-pre'."""
    if version.endswith("-pre"):
        print(f"[!] Version '{version}' is still in development ('-pre') - finalize the release first.")
        return False
    return True


def deploy(version: str, dry_run: bool) -> int:
    if not check_clean_git_tree():
        return 1
    if not check_not_pre_release(version):
        return 1

    print(f"\n[*] Deploying version {version} to production", flush=True)
    if dry_run:
        print("[dry-run] Skipping actual deployment step.")
        return 0

    # Project-specific deployment goes here, e.g. build+push a container image, rsync artifacts
    # to the target host and restart the service, or invoke a cloud provider's deploy CLI.
    print("[!] No production deployment target is configured for this template - nothing done.")
    print("    Replace this section in deploy() with the project's actual deployment mechanism.")
    return 1


def main() -> int:
    parser = build_action_parser(PROG, DESCRIPTION, ACTIONS, "help")
    parser.add_argument("--dry-run", action="store_true", help="release/deploy: print every step without making any changes")
    parser.add_argument("--skip-checks", action="store_true", help="release: skip pre-flight quality checks")
    args = parser.parse_args()
    version = get_project_version()

    if args.version or args.action == "version":
        print_version(PROG, version)
        return 0
    if args.help or args.action == "help":
        print_help(PROG, version, DESCRIPTION, parser, EXIT_CODES)
        return 0

    if args.action == "release":
        return release(dry_run=args.dry_run, skip_checks=args.skip_checks)
    if args.action == "deploy":
        return deploy(version, args.dry_run)

    if args.action in VENV_ACTIONS and not venv_python().exists():
        print("[!] Virtual environment missing; run scripts/bootstrap-dev-environment.py first.", file=sys.stderr)
        return 1
    python = str(venv_python())
    operations = {"lint": [lint], "test": [test], "build": [build], "clean": [clean], "check": [lint, test, build]}
    return 0 if all(operation(python) for operation in operations[args.action]) else 1


if __name__ == "__main__":
    sys.exit(main())
