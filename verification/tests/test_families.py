"""`families.ask`: one headless call per family, read back as text."""

import os
import subprocess
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))

from verification import families  # noqa: E402

PROMPT = "Judge these items.\n" + "- item: " + "x" * 3000


def codex(results):
    """A stand-in for `codex exec` that echoes the prompt to stderr, as Codex does."""
    calls = []

    def run(argv, cwd, **kw):
        calls.append(argv)
        rc, reply, error = results[len(calls) - 1]
        if rc == 0:
            with open(argv[argv.index("-o") + 1], "w", encoding="utf-8") as fh:
                fh.write(reply)
        return subprocess.CompletedProcess(argv, rc, stdout=error, stderr="user\n" + argv[-1])

    return run, calls


def test_a_failed_call_is_retried(monkeypatch):
    # Prevents: one transient Codex failure discarding a replay whose two agent runs had
    # already finished (aw-fx-hmm-floor-ratio-wrong, 2026-10-13).
    run, calls = codex([(1, "", "ERROR: stream disconnected"), (0, '{"exposing": []}', "")])
    monkeypatch.setattr(families.subprocess, "run", run)
    assert families.ask("gpt", PROMPT) == '{"exposing": []}'
    assert len(calls) == 2


def test_a_failure_names_its_cause_not_the_echoed_prompt(monkeypatch):
    # Prevents: an error message that is the tail of the prompt Codex echoed, with the reason
    # for the failure cut off.
    run, _ = codex([(1, "", "ERROR: usage limit reached")] * 2)
    monkeypatch.setattr(families.subprocess, "run", run)
    with pytest.raises(RuntimeError) as e:
        families.ask("gpt", PROMPT)
    assert "usage limit reached" in str(e.value)
    assert "x" * 100 not in str(e.value)
