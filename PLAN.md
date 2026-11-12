# Project Planning
An overview of all tasks and their planning.

---

## Next Milestone
- [x] T0024 Add an autouse test fixture isolating HOME and configuration directories and failing on writes to real user state.
- [x] T0029 Make myproject create initialize the new project's plan store with plan init --store branch.
- [x] T0039 Fix the pre-existing lint-markdown issues in README.md and CHANGELOG.md.
- [x] T0033 Add module docstrings to the myproject modules and docstrings to the public script helper functions.
- [x] T0038 Resolve __version__ with support_python.get_package_version so the CLI shows -pre instead of the rc0 form.
- [x] T0030 Start scaffolded projects at version 0.1.0-pre with an area-prefixed first CHANGELOG entry.
- [x] T0035 Change the greet default name from the Dutch wereld to the US English world.
- [x] T0037 Rewrite the active -pre CHANGELOG entries to follow the changelog entry style rules.
- [x] T0034 Put one argument per line in every call or signature split across lines.
- [x] T0031 Scaffold and index docs/tutorials/ alongside the other standard documentation subdirectories.
- [x] T0020 Remove the always-failing placeholder deploy action from scripts/devops.py, its tests, and its docs.
- [x] T0023 Split the tests into fast and slow suites with pytest-xdist, pytest-timeout, a slow marker, and a CI slow run.
- [x] T0025 Add a subprocess end-to-end test that runs the installed myproject entry point with realistic arguments.
- [x] T0027 Add the standard --format text|json option to the myproject greet and create actions.
- [x] T0028 Add --dry-run to myproject create, reporting every planned change without writing anything.
- [x] T0032 Make the bootstrap script CLI follow the CLI guidelines: -v as --verbose, help --verbose, errors on stderr.
- [x] T0019 Restructure docs/devops.md into the required guideline sections and fix the manual release commit order.
- [ ] T0036 Read the CLI author and copyright from package metadata instead of hardcoding them in cli.py and _cli_common.py.
- [ ] T0021 Fix all lint-markdown issues, bold lead-ins, placeholder syntax, backslash paths, and stale references in the docs.
- [ ] T0022 [needs: T0021] Run lint-markdown check in CI and in devops.py check so Markdown violations fail the build.

---

## Backlog
*(Currently no tasks)*
