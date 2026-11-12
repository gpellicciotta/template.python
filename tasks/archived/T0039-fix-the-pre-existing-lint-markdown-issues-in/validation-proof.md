# Validation Proof

## Walkthrough & Validation
### Review Round 1 Rework
Restored historical changelog meaning and removed the duplicate resource link.
Command: `lint-markdown check README.md CHANGELOG.md` (exit code 0).

```text
All 2 markdown files passed linting.
```

Documentation-only changes require no unit tests; the Markdown linter checks formatting and link validity.
The linter uses a modern browser User-Agent for external requests.

### Before Changes
Command: `lint-markdown check README.md CHANGELOG.md` (exit code 1).

```text
CHANGELOG.md:24:34: MD019 [file-references-as-links] Repository file reference 'scripts/devops.py' in prose must be formatted as markdown link [filename](path)
CHANGELOG.md:31:110: MD019 [file-references-as-links] Repository file reference 'scripts/devops.py' in prose must be formatted as markdown link [filename](path)
CHANGELOG.md:38:16: MD019 [file-references-as-links] Repository file reference 'scripts/devops.py' in prose must be formatted as markdown link [filename](path)
CHANGELOG.md:72:56: MD018 [valid-external-links] External link 'https://github.com/gpellicciotta/dev-guidelines' failed validation: HTTP 404
CHANGELOG.md:90:4: MD008 [no-raw-urls] Raw URL found in prose: 'https://github.com/gpellicciotta/python-project-template'; enclose in markdown link
README.md:7:26: MD018 [valid-external-links] External link 'https://github.com/gpellicciotta/dev-guidelines' failed validation: HTTP 404
README.md:9:1: MD015 [no-blank-line-after-subheading] Heading 'Directory Layout' (H2) must not be followed by a blank line before content
README.md:11:1: MD007 [code-block-language] Fenced code block lacks a language identifier
README.md:62:28: MD018 [valid-external-links] External link 'https://github.com/gpellicciotta/dev-guidelines' failed validation: HTTP 404
README.md:82:1: MD015 [no-blank-line-after-subheading] Heading 'Running Tests' (H2) must not be followed by a blank line before content
README.md:88:1: MD015 [no-blank-line-after-subheading] Heading 'Linting' (H2) must not be followed by a blank line before content
README.md:95:1: MD015 [no-blank-line-after-subheading] Heading 'CLI' (H2) must not be followed by a blank line before content
README.md:116:1: MD015 [no-blank-line-after-subheading] Heading 'Building the Packages' (H2) must not be followed by a blank line before content
README.md:124:73: MD019 [file-references-as-links] Repository file reference 'scripts/bootstrap-dev-environment.py' in prose must be formatted as markdown link [filename](path)
README.md:126:1: MD015 [no-blank-line-after-subheading] Heading 'Installation and Releases' (H2) must not be followed by a blank line before content
README.md:131:1: MD015 [no-blank-line-after-subheading] Heading 'Installing from a release' (H3) must not be followed by a blank line before content
README.md:153:1: MD015 [no-blank-line-after-subheading] Heading 'Starting a new project from this template' (H2) must not be followed by a blank line before content
README.md:161:1: MD016 [no-blank-line-before-list] Sentence introducing a list must not be followed by a blank line
README.md:165:3: MD019 [file-references-as-links] Repository file reference 'tests/test_core.py' in prose must be formatted as markdown link [filename](path)
**[WARN]**  Found 19 lint issues across 2 files.
**[ERROR]** Finished lint-markdown check in 0.9s with status: failed
```

### After Changes
Command: `lint-markdown check README.md CHANGELOG.md` (exit code 0).

```text
All 2 markdown files passed linting.
```

