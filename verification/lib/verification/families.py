"""Run one prompt on a model family headlessly, from a directory that names nothing.

Families: `claude` (Claude Code, `claude -p`) and `gpt` (Codex, `codex exec`).
Each call runs read-only in a fresh empty directory so neither family sees the
other's output or the store.
"""

import json
import os
import re
import subprocess
import tempfile

COMMANDS = {
    "claude": lambda prompt, out: (["claude", "-p", "--output-format", "text", prompt], None),
    "gpt": lambda prompt, out: (
        [
            "codex",
            "exec",
            "--sandbox",
            "read-only",
            "--skip-git-repo-check",
            "--ephemeral",
            "-o",
            out,
            prompt,
        ],
        out,
    ),
}


def ask(family, prompt, timeout=1800):
    """Return the family's final text reply."""
    with tempfile.TemporaryDirectory(prefix="work-") as cwd:
        out = os.path.join(cwd, "reply.txt")
        argv, outfile = COMMANDS[family](prompt, out)
        r = subprocess.run(
            argv, cwd=cwd, capture_output=True, text=True, timeout=timeout, stdin=subprocess.DEVNULL
        )
        if r.returncode != 0:
            raise RuntimeError(f"{family} exited {r.returncode}: {r.stderr[-2000:]}")
        if outfile:
            with open(outfile, encoding="utf-8") as fh:
                return fh.read()
        return r.stdout


def parse_json_object(text):
    """The last JSON object in a reply, tolerating a fenced block or surrounding prose."""
    fenced = re.findall(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.S)
    candidates = fenced or [text[text.find("{") : text.rfind("}") + 1]]
    return json.loads(candidates[-1])
