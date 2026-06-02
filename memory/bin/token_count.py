#!/usr/bin/env python3
"""Stdlib token-counting helper — the single source of truth for memory tooling.

Every memory script (measure_memory.sh and, downstream, verify_index.sh,
check_anchors.sh, the PreToolUse reference hook, and the upgraded /memory-gc)
estimates token counts through this module so all consumers agree on one number.

Estimate: ~4 characters per token, the well-known rule of thumb for the
Claude / GPT-family BPE tokenizers on mixed prose + code. This is deliberately a
heuristic: it needs no third-party tokenizer (pure Python 3 stdlib) and stays
deterministic and consistent across the whole toolchain. Absolute accuracy
matters less than every script producing the same count for the same bytes.
Override the divisor with the CHARS_PER_TOKEN environment variable if a project
wants to calibrate against a measured ratio.

Use as a module:
    from token_count import count_tokens, count_file
    n = count_tokens("some text")
    n = count_file("path/to/file.md")   # 0 if missing / unreadable

Use as a CLI:
    python3 token_count.py FILE [FILE ...]    # prints summed token count
    python3 token_count.py --per-file FILE…   # prints "<tokens>\t<path>" lines
    echo "text" | python3 token_count.py      # counts stdin
"""
import os
import sys


def _chars_per_token():
    """Characters-per-token divisor (default 4, overridable via env)."""
    raw = os.environ.get("CHARS_PER_TOKEN", "4")
    try:
        value = int(raw)
    except ValueError:
        value = 4
    return value if value > 0 else 4


CHARS_PER_TOKEN = _chars_per_token()


def count_tokens(text):
    """Estimate the number of tokens in a string (~4 chars/token, rounded up)."""
    if not text:
        return 0
    return (len(text) + CHARS_PER_TOKEN - 1) // CHARS_PER_TOKEN


def count_file(path):
    """Estimate tokens in a file. Returns 0 if the file is missing/unreadable."""
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            return count_tokens(fh.read())
    except (OSError, IOError):
        return 0


def _main(argv):
    args = argv[1:]
    per_file = False
    if args and args[0] == "--per-file":
        per_file = True
        args = args[1:]

    if not args:
        # No paths given: count stdin.
        print(count_tokens(sys.stdin.read()))
        return 0

    total = 0
    for path in args:
        n = count_file(path)
        total += n
        if per_file:
            print("%d\t%s" % (n, path))
    if not per_file:
        print(total)
    return 0


if __name__ == "__main__":
    sys.exit(_main(sys.argv))
