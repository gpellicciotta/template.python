## Walkthrough & Validation
Pin tests failed first (`2 failed, 26 passed`) with v2.0.0 still pinned; they pass after the bump.

```text
$ python scripts/devops.py check
All checks passed!
28 passed in 2.47s
collected 28 items / 27 deselected / 1 selected
1 passed, 27 deselected in 0.65s
Successfully built template_python-3.0.2rc0.tar.gz and template_python-3.0.2rc0-py3-none-any.whl
exit code: 0
```
