# Requirements

Functional and technical requirements for the `template.python` repository.

---

## High-Level Goals
- Provide a clean, modern template to start Python projects quickly using the standard `src/` layout.
- Include out-of-the-box support for testing (`pytest`), linting and formatting (`ruff`), packaging (`build`/`wheel`), and CI (`GitHub Actions`).
- Follow cross-project [Development Guidelines](https://github.com/gpellicciotta/dev-guidelines), including documentation standards and [CLI conventions](https://github.com/gpellicciotta/dev-guidelines/blob/main/guidelines/cli-guidelines.md).
- Coordinate tasks with the `plan` CLI, following the [Plan Task Usage Guidelines](https://github.com/gpellicciotta/plan/blob/main/src/plan/skills/plan-task-usage-guidelines/SKILL.md).
- Provide an automated scaffolding command (`myproject create {{project-name}}`) to clone and rename the template into a fresh, independent project with its own clean history and configuration.

---

## Functional Requirements

### Template Structure and Scaffolding
- Support the standard `src/{{package-name}}/` layout to avoid import conflicts during testing.
- Include a built-in `create` subcommand (`myproject create {{project-name}} [-o {{output-dir}}]`) that:
  - Validates and derives valid Python package names from project slugs.
  - Copies template files while excluding cache/build artifacts.
  - Rewrites placeholders (`template-python`, `template.python`, `myproject`, title) across documentation and configuration.
  - Resets the project version to `0.1.0-pre` and initializes a fresh changelog with an area-prefixed first entry.
  - Requires `git` and `plan` on `PATH`; runs `git init` followed by `plan init --store branch`.
  - Skips the template's plan store and preserves `.plan/`, `/PLAN.md`, and `/plan.code-workspace` ignore rules.
  - Creates a branch-backed plan store, an ignored root `PLAN.md` link, and exactly one plan-managed instructions block.
  - Returns exit code `1` for missing tools or initialization failures, leaving no generated project directory.
  - Refuses to overwrite existing target directories.
  - Accepts `--dry-run` to report every planned change without writing anything:
    - Reports the destination, copied files, renames, rewrites, reset files, and the `git init` and `plan init` steps.
    - Fails with exit code `1` on the same preconditions as the real run, such as an existing destination or an invalid name.

### Command Line Interface (CLI)
- Provide an action-oriented, subcommand-based CLI built on `support-python`'s `ToolHarness`:
  - `myproject help [{{action}}]` / `-h` / `--help`: displays standardized multi-line help with usage, subcommands, options, and exit codes (supports `--verbose` for detailed usage).
  - `myproject version` / `--version`: outputs `{{name}} v{{version}} - {{copyright}}` and exits with code 0.
    The copyright names the `pyproject.toml` authors through package metadata, after a literal first-publication year.
  - `myproject greet [{{name}}]`: sample business logic command; prints `Hello, world` when the name is omitted.
  - `myproject create {{project-name}}`: project scaffolding subcommand.
- Accept `--format text|json` on `greet` and `create`, defaulting to `text`:
  - `text`: prints the plain greeting or the `Created new project at {{path}}` line.
  - `json`: prints exactly one JSON object on stdout and writes all log entries to stderr.
  - `greet` JSON fields: `name` (greeting target) and `greeting` (greeting text).
  - `create` JSON fields: `project_name` (new project's name) and `path` (created project directory).
  - `create --dry-run` JSON fields: `project_name`, `path`, `dry_run` (`true`), `template`, `copied`, `renamed`, `rewritten`, `reset`, and `commands`.
  - Failures print no JSON document; the error goes to stderr with exit code `1`.
  - Renaming or removing a JSON field is a breaking change.
- Maintain consistent exit codes across all commands:
  - `0`: Success.
  - `1`: Application or command execution failure.
  - `2`: Invalid command-line arguments.

### Logging
- Support operational and CLI logging adhering to the cross-project [Logging Guidelines](https://github.com/gpellicciotta/dev-guidelines/blob/main/guidelines/logging-guidelines.md):
  - Utilize `support-python`'s `support_python.logging.CliLogger` and `LogLevel` rather than reimplementing local logging utilities.
  - Support `--log-file`, dual-destination output, startup and completion lifecycle banners, padded severity indicators, and debug filtering.

---

## Technical Requirements
- Require Python 3.15 or later.
- Package with a standard [pyproject.toml](../pyproject.toml) using the `setuptools.build_meta` backend.
- Enforce code quality with shared tool settings:
  - Format and lint code with `ruff` (132-character line length, rules pinned to `E4`, `E7`, `E9`, `F`).
  - Configure editors through [.editorconfig](../.editorconfig) (4 spaces, UTF-8, LF line endings).
- Test core logic, CLI actions, options, exit codes, and scaffolding behavior with `pytest`.
- Support Windows, Linux, and macOS.
- Write all documentation in US English Markdown, following the [Markdown Guidelines](https://github.com/gpellicciotta/dev-guidelines/blob/main/guidelines/markdown-guidelines.md).
- Validate Markdown with `lint-markdown check`, configured by [.lint-markdown.json](../.lint-markdown.json).
