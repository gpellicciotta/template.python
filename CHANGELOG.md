# Versioned Changes

A summarized overview of all changes, per version of this project.

> Entries will be added in reverse chronological order, so with the most recent at the top.
> 
> Status codes used are:
> - `vX.Y.Z-pre` - actively being developed (suffix on the heading itself, not a bracket tag)
> - `[{{date}}]` - frozen/finalized on {{date}}
> - `[released: {{date}}]` - released to package manager or production on {{date}}
> - `[broken]` - considered broken and not be used

---

## v3.0.11-pre
- CLI: Changed the default greeting target to `world`; pass `wereld` explicitly to retain the previous greeting.
- CLI: **[breaking]** Scaffolded `0.1.0-pre` projects with area-prefixed changelogs, Git, and branch-backed plan stores, requiring `git` and `plan`.
- CLI: Removed partially initialized projects even when Git object files were read-only.
- CLI: Restored the `-pre` suffix in the public package version using the shared version resolver.
- Docs: Documented module responsibilities, public constants, and development script helpers.
- Docs: Corrected Markdown formatting and repaired links in [README.md](README.md) and [CHANGELOG.md](CHANGELOG.md).
- DevEx: Isolated test home and configuration directories and added guards against writes to persistent user and repository state.
- Docs: Moved project instructions into [AGENTS.md](AGENTS.md) and reduced [CLAUDE.md](CLAUDE.md) to an `@AGENTS.md` import.
- Build: **[breaking]** Required Python 3.15, raising `requires-python` from 3.10 and running CI on 3.15 only.
- CLI: **[breaking]** Rebuilt `myproject` on `support-python`'s `ToolHarness`; `-v` now means `--verbose`, so use `--version`.
- Build: Upgraded `support-python` from v1.0.0 to v3.0.0 and explicitly supplied the copyright banner in [devops.py](scripts/devops.py).
- DevEx: Added `pytest-timeout` and a `slow` marker; `check` now requires slow tests passing `pytest -m slow --timeout=120`.
- DevEx: **[breaking]** Replaced `scripts/create-github-release.py` and `scripts/deploy-to-production.py` with [devops.py](scripts/devops.py)'s `DevopsCli` actions, automatically using `.venv`.
- DevEx: **[breaking]** Changed [devops.py](scripts/devops.py) flags: `-v` means `--verbose`; use `--version`; exit code 2 indicates invalid arguments.
- Build: **[breaking]** Replaced `.github/workflows/publish.yml` with [devops.py](scripts/devops.py)'s `release` action, attaching wheel and sdist assets.
- DevEx: Required typed `release v{{version}}` confirmation for `release`; `--yes` skips confirmation.
- DevEx: Made `release --dry-run` validate all preconditions, including authenticated `gh` and fresh tags.
- DevEx: Required deployment tags on `origin` at HEAD, green CI, and typed confirmation; `--skip-ci-check` bypasses CI checks.
- DevEx: Added `format` and `versions` actions and bootstrap installation of [requirements.txt](scripts/requirements.txt) into `.venv`.
- DevEx: **[breaking]** Removed `scripts/install-from-github-release.py`; install releases with `pip` from the release wheel or Git tag.

## v2.0.0 [released: 2026-10-31]
- **[breaking]** DevEx: Renamed the distribution to `template-python` and the repository to `template.python`; update install URLs and pins.
- **[breaking]** DevEx: Replaced the `hinolugi-support` dependency with `support-python` (`support_python`).
- DevEx: Fixed `create` failing to find the template root, and made it scaffold `PLAN.md` and `.plan/tasks/` instead of `TODO.md` and `tasks/`.
- DevEx: Added [devops.py](scripts/devops.py) with lint, test, build, check, and clean actions.
- Build: Declared the license as an SPDX expression and raised the setuptools floor to 77.
- Docs: Replaced `TODO.md` references with `PLAN.md` and dropped `hinolugi` from project prose.
- DevEx: Improved `scripts/create-github-release.py` with pre-flight quality and state checks, and fixed its crash on Windows cp1252 consoles.

## v1.4.0 [released: 2026-09-10]
- DevEx: Added scaffolded `scripts/deploy-to-production.py` example for services deployed from this template.
- DevEx: Ignored coverage files and tool caches in `.gitignore`, and excluded logs and caches when scaffolding.
- DevEx: Upgraded CI to setup-python v5, added read-only permissions, and archived build artifacts.
- DevEx: Refactored sample CLI to build on `hinolugi-support`'s shared argparse version/help helpers.
- DevEx: Replaced Windows-only `setup.ps1` with a cross-platform `scripts/bootstrap-dev-environment.py`.
- Build: Declared license file and project URLs in `pyproject.toml`, rewritten automatically when scaffolding.
- DevEx: Standardized `setup.ps1`'s build step to output into `dist/`, matching `python -m build` and CI.
- DevEx: Added `src` to pytest's `pythonpath` so tests run without a prior editable install.

## v1.3.0 [2026-09-06]
- Docs: Document optional scripts convention for non-packaged dev and maintenance tooling in devops.md.
- Config: Pin ruff default lint rules explicitly in pyproject.toml.
- DevEx: Reset pyproject.toml version to 0.0.1-pre when scaffolding new projects.
- DevEx: Scaffold a tracked tasks/ directory with a placeholder file for new projects.
- Docs: Scaffold docs/specs/, docs/adrs/, and docs/issues/ placeholder directories and link them from docs/index.md.
- Build: Add release publish workflow and document installing packages from GitHub releases.
- Docs: Wire CLAUDE.md logging guidance to hinolugi-support's CliLogger and LogLevel instead of local modules.
- DevEx: Add hinolugi-support dependency so derived projects inherit shared support utilities.
- DevEx: Add all log files to .gitignore.
- Docs: Align task and documentation files with latest dev-guidelines and hinolugi-support.python conventions.

## v1.2.1 [2026-09-06]
- Docs: Align TODO.md, CHANGELOG.md, and CLAUDE.md with the `-pre` versioning and Backlog heading conventions.
- DevEx: Document the adhoc-task and review-tier workflow in devops.md, and fix scaffolded projects' TODO.md/CHANGELOG.md to match.

## v1.2.0 [2026-08-24]
- DevEx: Scope pytest to `tests/` so it no longer collides with sibling task worktrees under `work/`.
- DevEx: Add Python 3.10 to the CI test matrix so it matches what `requires-python` actually allows.
- Aligned project with the latest development guidelines:
  - Renamed `LICENSE` to `LICENSE.md` and `RELEASES.md` to `CHANGELOG.md` with version status tags.
  - Restructured `TODO.md` with milestone sections (`## Next Milestone`, `### Backlog`) per coordinating work guidelines, and added `work/` to `.gitignore`.
  - Added mandatory documentation files `docs/requirements.md` and `docs/devops.md`, and updated `docs/index.md`, `README.md`, and `CLAUDE.md`.
  - Aligned CLI in `src/myproject/cli.py` to support action-oriented subcommands, `{name} v{version} - {copyright}` version output, standardized multi-line help with exit codes, and `-h`/`--help`/`--version`/`--verbose` options.
  - Updated `scaffold.py` and test suite to verify the updated layout, docs, and CLI options.

## v1.1.0 [released: 2026-08-19]
- Renamed `docs/README.md` to `docs/index.md`.
- Fixed `test_create_scaffolds_renamed_project` (`tests/test_cli.py`): its assertions hardcoded the
  template's own placeholder name (`myproject`) to check that the *old* package/name references were gone,
  but the test file itself is text-rewritten by `create`/`scaffold.py` when copied into a scaffolded
  project, so those literals got swept up in the very rewrite pass they were meant to validate. Replaced
  them with structural checks that survive being copied into their own test subject: exactly one directory
  under `src/`, and the scripts entry matching the new project's own name.

## v1.0.0 [released: 2026-08-19]
- First stable release. Published the repo to GitHub
  ([python-project-template](https://github.com/gpellicciotta/python-project-template)).
- Added a `docs/` folder (with a short explainer) so it exists from the start rather than only being
  documented as "created as needed".
- Fixed `setup.ps1`'s build step: the `dev` extra never included the `build` package, so `python -m build`
  always failed with "No module named build" despite the editable install succeeding.

## v0.1.0 [released: 2026-08-19]
- Added `myproject create <project-name> [-o <output-dir>]`, which scaffolds a new project as a renamed copy
  of this template (package rename, `pyproject.toml` name, and all `template-project` / `python-template-project`
  placeholder references), automating the manual steps previously described in the README.
- Restructured the CLI into subcommands: `help`, `version`, `greet <name>` (the previous top-level sample
  action), and `create`. **Breaking:** `myproject <name>` no longer greets directly — use `myproject greet <name>`.
- `__version__` is now read from installed package metadata instead of being hardcoded, so it can't drift
  from `pyproject.toml`'s `version`.
- Added `ruff` (lint + format check) as a dev-extra tool, wired into `setup.ps1` and CI, with a 132-character
  line length. Added a matching `.editorconfig` (4-space indent, spaces only, UTF-8, 132-char lines).
- Added the project's `LICENSE.md` file (MIT), matching the classifier already declared in `pyproject.toml`.
- Trimmed `[build-system].requires` to just `setuptools>=68` (removed `wheel` and `build`, neither of which
  is a build-backend dependency).
- Documented general development guidelines and the style guide in `CLAUDE.md`.
