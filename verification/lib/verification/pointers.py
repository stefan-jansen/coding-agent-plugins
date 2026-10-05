"""Pointers from store rows to evidence elsewhere on disk.

Forms:
  <repo>:<path>               a file inside a repository
  <repo>:<path>::<symbol>     a function or class defined in that file
  <repo>@<sha>                a commit in that repository
  http(s)://...               an external document (format-checked only)

<repo> may start with `~`. A pointer resolves when the file exists, the symbol is
defined in it, or the commit exists in the repository.
"""

import os
import re
import subprocess

_COMMIT = re.compile(r"^(?P<repo>[^:@]+)@(?P<sha>[0-9a-f]{7,40})$")
_FILE = re.compile(r"^(?P<repo>[^:@]+):(?P<path>[^:]+)(?:::(?P<symbol>[A-Za-z_][\w.]*))?$")


def is_url(value):
    return value.startswith("https://") or value.startswith("http://")


def resolve(pointer):
    """Return None when the pointer resolves, else a one-line reason."""
    if not isinstance(pointer, str) or not pointer:
        return "pointer is empty"
    if is_url(pointer):
        return None
    m = _COMMIT.match(pointer)
    if m:
        repo = os.path.expanduser(m["repo"])
        if not os.path.isdir(repo):
            return f"repository {m['repo']} not found"
        r = subprocess.run(
            ["git", "-C", repo, "cat-file", "-e", f"{m['sha']}^{{commit}}"],
            capture_output=True,
        )
        return None if r.returncode == 0 else f"commit {m['sha']} not in {m['repo']}"
    m = _FILE.match(pointer)
    if not m:
        return f"not a pointer: {pointer!r}"
    path = os.path.join(os.path.expanduser(m["repo"]), m["path"])
    if not os.path.isfile(path):
        return f"file {m['path']} not found in {m['repo']}"
    if m["symbol"]:
        name = m["symbol"].split(".")[-1]
        with open(path, encoding="utf-8", errors="replace") as fh:
            text = fh.read()
        if not re.search(rf"^\s*(?:async\s+def|def|class)\s+{re.escape(name)}\b", text, re.M):
            return f"{m['symbol']} not defined in {m['path']}"
    return None
