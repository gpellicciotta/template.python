# Project Planning
An overview of all tasks and their planning.

---

## Next Milestone
- [x] T0017 Stop uploading release assets twice: devops.py release attaches the wheel and sdist, and publish.yml uploads them again.
- [x] T0016 Make myproject create and its tests work on a fresh clone, where the plan branch store leaves no PLAN.md.
- [x] T0014 Replace scripts/devops.py with a thin DevopsCli script on the PythonProject adapter, pinning the released support-python v2.0.0.
- [x] T0015 Migrate the myproject CLI from build_action_parser, print_help, and print_version to the support-python v2.0.0 ToolHarness.
- [x] T0018 Move project instructions into AGENTS.md per the agent-file layout, reducing CLAUDE.md to an @AGENTS.md import.
- [ ] T0019 [needs: T0020] Restructure docs/devops.md into the required guideline sections and fix the manual release commit order.
- [ ] T0020 Remove the always-failing placeholder deploy action from scripts/devops.py, its tests, and its docs.
- [ ] T0021 [needs: T0019] Fix all lint-markdown issues, bold lead-ins, placeholder syntax, backslash paths, and stale references in the docs.
- [ ] T0022 [needs: T0021] Run lint-markdown check in CI and in devops.py check so Markdown violations fail the build.
- [ ] T0023 Split the tests into fast and slow suites with pytest-xdist, pytest-timeout, a slow marker, and a CI slow run.
- [ ] T0024 Add an autouse test fixture isolating HOME and configuration directories and failing on writes to real user state.
- [ ] T0025 [needs: T0023] Add a subprocess end-to-end test that runs the installed myproject entry point with realistic arguments.
- [x] T0026 Move to Python 3.15 per the Python guidelines: requires-python >=3.15, the CI matrix, classifiers, and docs.
- [ ] T0027 Add the standard --format text|json option to the myproject greet and create actions.
- [ ] T0028 [needs: T0027, T0029] Add --dry-run to myproject create, reporting every planned change without writing anything.
- [ ] T0029 Make myproject create initialize the new project's plan store with plan init --store branch.
- [ ] T0030 Start scaffolded projects at version 0.1.0-pre with an area-prefixed first CHANGELOG entry.
- [ ] T0031 Scaffold and index docs/tutorials/ alongside the other standard documentation subdirectories.
- [ ] T0032 Make the bootstrap script CLI follow the CLI guidelines: -v as --verbose, help --verbose, errors on stderr.
- [ ] T0033 Add module docstrings to the myproject modules and docstrings to the public script helper functions.
- [ ] T0034 Put one argument per line in every call or signature split across lines.
- [ ] T0035 Change the greet default name from the Dutch wereld to the US English world.
- [ ] T0036 Read the CLI author and copyright from package metadata instead of hardcoding them in cli.py and _cli_common.py.
- [ ] T0037 Rewrite the active -pre CHANGELOG entries to follow the changelog entry style rules.
- [ ] T0038 Resolve __version__ with support_python.get_package_version so the CLI shows -pre instead of the rc0 form.

---

## Backlog
- [ ] T0039 Fix the pre-existing lint-markdown issues in README.md and CHANGELOG.md.
