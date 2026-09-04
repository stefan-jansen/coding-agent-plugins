#!/usr/bin/env python3
"""Instructions-audit evidence collection.

Deterministic, bounded, read-only. Emits JSON on stdout; the SKILL.md that
calls this does the judging. Nothing here decides whether a rule earns its
place - it only gathers what a judgment would need to cite.

Two modes:
  (default)  one project: its instruction files, its auto-memory directory,
             its feedback memories, and - only where those are thin - a
             bounded transcript grep.
  --user     every project on the machine: feedback evidence grouped by the
             user-level instruction file's sections.

Never writes. Never edits. The only side effect is stdout.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

# --------------------------------------------------------------------------
# Constants

INSTRUCTION_NAMES = ("AGENTS.md", "CLAUDE.md")
RULES_GLOB = ".claude/rules/*.md"
TYPED_PREFIXES = ("user_", "feedback_", "project_", "reference_")
VALID_TYPES = ("user", "feedback", "project", "reference")

# Cap on extracted transcript text entering the model's context (AC-8).
EXTRACT_CAP_BYTES = 200 * 1024

# A turn is only evidence of a correction if a person typed it. Peer messages,
# task notifications, hook injections and tool results all arrive as
# type:"user" records and match the same wording.
HUMAN_ORIGIN_KIND = "human"

# Shape-based exclusion, used only when a transcript predates the origin field.
DEGRADED_EXCLUDE_PREFIXES = (
    "<command-name>", "<local-command-", "<cross-session-message",
    "<system-reminder>", "<task-notification>", "<user-prompt-submit-hook>",
)

CORRECTION_PATTERNS = [
    r"\bi (?:already )?(?:told|asked|said)\b",
    r"\bwhy (?:are|would|did|do) you\b",
    r"\byou (?:were supposed to|should have|keep|always|never)\b",
    r"\b(?:stop|don't|do not|never) (?:doing|adding|asking|creating|writing|using)\b",
    r"\bno[,.]? (?:i|that|this|it)\b",
    r"\bthat(?:'s| is) (?:not|wrong|incorrect)\b",
    r"\bagain[,.]",
    r"\binstead of\b",
    r"\bas i (?:said|told you|asked)\b",
]
CORRECTION_RE = re.compile("|".join(CORRECTION_PATTERNS), re.I)
# Sustained capitals read as emphasis, which is how a repeated instruction
# usually arrives after the plain version was missed.
SHOUT_RE = re.compile(r"\b[A-Z][A-Z ]{9,}[A-Z]\b")

HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*$")
FRONTMATTER_TYPE_RE = re.compile(r"^\s*type:\s*(\S+)\s*$", re.M)
FRONTMATTER_SESSION_RE = re.compile(r"^\s*originSessionId:\s*(\S+)\s*$", re.M)
FRONTMATTER_NAME_RE = re.compile(r"^\s*name:\s*(.+?)\s*$", re.M)
FRONTMATTER_DESC_RE = re.compile(r"^\s*description:\s*(.+?)\s*$", re.M)


# --------------------------------------------------------------------------
# Helpers

def project_slug(project_root: Path) -> str:
    """Claude Code's auto-memory path mangle: '/' and '.' both become '-'."""
    s = str(project_root)
    return "".join("-" if c in "/." else c for c in s)


def auto_memory_dir(project_root: Path) -> Path:
    return Path.home() / ".claude" / "projects" / project_slug(project_root) / "memory"


def read_text(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def split_frontmatter(text: str) -> tuple[str, str]:
    """Return (frontmatter, body). Empty frontmatter when the file has none."""
    if not text.startswith("---"):
        return "", text
    end = text.find("\n---", 3)
    if end == -1:
        return "", text
    return text[3:end], text[end + 4:]


def headings(text: str) -> list[dict]:
    out = []
    for n, line in enumerate(text.splitlines(), 1):
        m = HEADING_RE.match(line)
        if m:
            out.append({"line": n, "level": len(m.group(1)), "title": m.group(2)})
    return out


# --------------------------------------------------------------------------
# I1 - target resolution

def resolve_instruction_file(p: Path, scope: str) -> dict | None:
    if not p.exists():
        return None
    text = read_text(p)
    real = p.resolve()
    return {
        "path": str(p),
        "realpath": str(real),
        "is_symlink": p.is_symlink(),
        "symlink_chain": symlink_chain(p),
        "scope": scope,
        "bytes": len(text.encode("utf-8")),
        "lines": text.count("\n") + 1 if text else 0,
        "words": len(text.split()),
        "headings": headings(text),
        "imports": sorted(set(re.findall(r"^@(\S+)", text, re.M))),
    }


def symlink_chain(p: Path) -> list[str]:
    """Every hop from p to its real path. M3 needs the whole chain: an edit
    must land on the real file without replacing any link along the way."""
    chain, seen, cur = [], set(), p
    while cur.is_symlink() and str(cur) not in seen:
        seen.add(str(cur))
        nxt = Path(os.readlink(cur))
        if not nxt.is_absolute():
            nxt = cur.parent / nxt
        chain.append(str(nxt))
        cur = nxt
    return chain


def collect_targets(project_root: Path) -> list[dict]:
    targets = []
    for name in INSTRUCTION_NAMES:
        t = resolve_instruction_file(project_root / name, "project")
        if t:
            targets.append(t)
    for rule in sorted(project_root.glob(RULES_GLOB)):
        t = resolve_instruction_file(rule, "project-rule")
        if t:
            targets.append(t)
    for name in INSTRUCTION_NAMES:
        t = resolve_instruction_file(Path.home() / ".claude" / name, "user")
        if t:
            targets.append(t)
    # ~/AGENTS.md is the same file through a different link on Codex hosts;
    # report it once, by real path.
    seen, deduped = set(), []
    for t in targets:
        if t["realpath"] in seen:
            continue
        seen.add(t["realpath"])
        deduped.append(t)
    return deduped


# --------------------------------------------------------------------------
# I2 - auto-memory inventory, with mirror detection

def detect_population(project_root: Path, mem_dir: Path) -> dict:
    """Distinguish a directory an agent authored from one a hook mirrors.

    A mirrored directory whose source is already reachable another way is not
    inert when its index is missing - the content still loads. Reporting the
    two as the same defect sends the fix to the wrong owner.
    """
    evidence = []

    settings = project_root / ".claude" / "settings.json"
    if settings.exists():
        try:
            cfg = json.loads(read_text(settings))
        except json.JSONDecodeError:
            cfg = {}
        for event in ("SessionStart", "SessionEnd"):
            for group in cfg.get("hooks", {}).get(event, []):
                for hook in group.get("hooks", []):
                    cmd = str(hook.get("command", ""))
                    if not cmd:
                        continue
                    script = Path(cmd.split()[0])
                    body = read_text(script) if script.exists() else ""
                    if "projects/" in body and "memory" in body:
                        evidence.append({
                            "kind": "hook",
                            "event": event,
                            "command": cmd,
                            "note": "references the auto-memory store",
                        })

    # An @-include reaching the same content is the other way the material
    # stays loaded without the auto-memory index.
    for name in INSTRUCTION_NAMES:
        f = project_root / name
        if not f.exists():
            continue
        for imp in re.findall(r"^@(\S+)", read_text(f), re.M):
            evidence.append({"kind": "import", "file": name, "target": imp})

    if any(e["kind"] == "hook" for e in evidence):
        classification = "mirrored"
    elif mem_dir.exists() and any(mem_dir.iterdir()):
        classification = "authored"
    else:
        classification = "unknown"
    return {"classification": classification, "evidence": evidence}


def collect_auto_memory(project_root: Path) -> dict:
    mem_dir = auto_memory_dir(project_root)
    out = {
        "dir": str(mem_dir),
        "exists": mem_dir.is_dir(),
        "index_present": False,
        "file_count": 0,
        "total_bytes": 0,
        "typed_conforming": [],
        "typed_nonconforming": [],
        "unindexed": [],
    }
    if not mem_dir.is_dir():
        out["population"] = detect_population(project_root, mem_dir)
        return out

    files = sorted(p for p in mem_dir.rglob("*.md") if p.is_file())
    index = mem_dir / "MEMORY.md"
    out["index_present"] = index.exists()
    out["file_count"] = len(files)
    out["total_bytes"] = sum(p.stat().st_size for p in files)

    index_text = read_text(index) if index.exists() else ""
    for p in files:
        if p.name == "MEMORY.md":
            continue
        fm, _ = split_frontmatter(read_text(p))
        m = FRONTMATTER_TYPE_RE.search(fm)
        typed = bool(m and m.group(1) in VALID_TYPES)
        prefixed = p.name.startswith(TYPED_PREFIXES)
        rel = str(p.relative_to(mem_dir))
        entry = {"file": rel, "frontmatter_type": m.group(1) if m else None,
                 "prefixed": prefixed}
        (out["typed_conforming"] if typed and prefixed
         else out["typed_nonconforming"]).append(entry)
        if index_text and rel not in index_text and p.name not in index_text:
            out["unindexed"].append(rel)

    out["population"] = detect_population(project_root, mem_dir)
    return out


# --------------------------------------------------------------------------
# I3 - feedback memories (primary evidence source)

def collect_feedback(mem_dir: Path) -> list[dict]:
    if not mem_dir.is_dir():
        return []
    out = []
    for p in sorted(mem_dir.rglob("*.md")):
        if p.name == "MEMORY.md":
            continue
        text = read_text(p)
        fm, body = split_frontmatter(text)
        m = FRONTMATTER_TYPE_RE.search(fm)
        if not m or m.group(1) != "feedback":
            continue
        sess = FRONTMATTER_SESSION_RE.search(fm)
        name = FRONTMATTER_NAME_RE.search(fm)
        desc = FRONTMATTER_DESC_RE.search(fm)
        out.append({
            "path": str(p),
            "name": name.group(1) if name else p.stem,
            "description": desc.group(1).strip('"') if desc else "",
            "originSessionId": sess.group(1) if sess else None,
            "body": body.strip(),
        })
    return out


# --------------------------------------------------------------------------
# I4 - transcript fallback, bounded

def transcript_dir(project_root: Path) -> Path:
    return Path.home() / ".claude" / "projects" / project_slug(project_root)


def record_is_human(rec: dict, degraded: bool) -> bool:
    """Accept only turns a person typed.

    Peer messages, task notifications, hook injections, slash-command echoes
    and tool results all arrive as type:"user" and match the same correction
    wording, so a regex-only filter cannot separate them.
    """
    origin = rec.get("origin")
    if isinstance(origin, dict):
        return origin.get("kind") == HUMAN_ORIGIN_KIND
    if origin is None and not degraded:
        # The field exists in this file, and this record does not carry it -
        # a hook injection, a command echo, or a tool result.
        return False
    # Degraded: the file predates the field. Fall back to shape.
    if rec.get("toolUseResult") is not None or rec.get("isMeta"):
        return False
    text = message_text(rec).lstrip()
    return not text.startswith(DEGRADED_EXCLUDE_PREFIXES)


def message_text(rec: dict) -> str:
    msg = rec.get("message") or {}
    content = msg.get("content")
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(
            c.get("text", "") for c in content
            if isinstance(c, dict) and c.get("type") == "text"
        )
    return ""


def file_has_origin(path: Path) -> bool:
    """Whether this transcript is new enough to carry the origin field."""
    try:
        with path.open(encoding="utf-8", errors="replace") as fh:
            for i, line in enumerate(fh):
                if i > 2000:
                    break
                if '"origin"' in line and '"origin":null' not in line.replace(" ", ""):
                    return True
    except OSError:
        pass
    return False


def collect_transcripts(project_root: Path, days: int) -> dict:
    tdir = transcript_dir(project_root)
    out = {"dir": str(tdir), "used": True, "cap_bound": False,
           "scanned_files": 0, "corpus_bytes": 0, "extracted_bytes": 0,
           "hits": []}
    if not tdir.is_dir():
        out["used"] = False
        out["reason"] = "no transcript directory"
        return out

    cutoff = datetime.now(timezone.utc).timestamp() - days * 86400
    files = sorted(
        (p for p in tdir.glob("*.jsonl") if p.stat().st_mtime >= cutoff),
        key=lambda p: p.stat().st_mtime, reverse=True,
    )
    out["corpus_bytes"] = sum(p.stat().st_size for p in files)

    extracted = 0
    for path in files:
        if extracted >= EXTRACT_CAP_BYTES:
            out["cap_bound"] = True
            break
        out["scanned_files"] += 1
        degraded = not file_has_origin(path)
        try:
            fh = path.open(encoding="utf-8", errors="replace")
        except OSError:
            continue
        with fh:
            for line in fh:
                if extracted >= EXTRACT_CAP_BYTES:
                    out["cap_bound"] = True
                    break
                if '"type":"user"' not in line and '"type": "user"' not in line:
                    continue
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if rec.get("type") != "user":
                    continue
                if not record_is_human(rec, degraded):
                    continue
                text = message_text(rec).strip()
                if not text or len(text) > 4000:
                    continue
                if not (CORRECTION_RE.search(text) or SHOUT_RE.search(text)):
                    continue
                hit = {
                    "session": path.stem,
                    "timestamp": rec.get("timestamp"),
                    "filter": "degraded" if degraded else "structural",
                    "text": text,
                }
                out["hits"].append(hit)
                extracted += len(text.encode("utf-8"))
    out["extracted_bytes"] = extracted
    return out


# --------------------------------------------------------------------------
# I5 - --user aggregation

def all_project_dirs() -> list[Path]:
    base = Path.home() / ".claude" / "projects"
    if not base.is_dir():
        return []
    return sorted(p for p in base.iterdir() if p.is_dir())


def collect_user_mode() -> dict:
    user_file = None
    for name in INSTRUCTION_NAMES:
        t = resolve_instruction_file(Path.home() / ".claude" / name, "user")
        if t:
            user_file = t
            break

    sections = []
    if user_file:
        text = read_text(Path(user_file["realpath"]))
        lines = text.splitlines()
        marks = [h for h in headings(text) if h["level"] == 2]
        for i, h in enumerate(marks):
            end = marks[i + 1]["line"] - 1 if i + 1 < len(marks) else len(lines)
            sections.append({
                "title": h["title"],
                "start_line": h["line"],
                "end_line": end,
                "words": len("\n".join(lines[h["line"]:end]).split()),
                "projects_with_evidence": [],
            })

    per_project = []
    for pdir in all_project_dirs():
        mem = pdir / "memory"
        fb = collect_feedback(mem)
        if not fb:
            continue
        per_project.append({
            "project_dir": pdir.name,
            "feedback_count": len(fb),
            "feedback": fb,
        })
        # Bind each feedback memory to the sections whose words it echoes.
        # Deliberately loose: this narrows what the judgment step reads, and
        # never decides anything on its own.
        for f in fb:
            blob = (f["name"] + " " + f["description"] + " " + f["body"]).lower()
            for s in sections:
                key = [w for w in re.findall(r"[a-z]{5,}", s["title"].lower())]
                if key and any(w in blob for w in key):
                    if pdir.name not in s["projects_with_evidence"]:
                        s["projects_with_evidence"].append(pdir.name)

    return {
        "user_instruction_file": user_file,
        "sections": sections,
        "projects": per_project,
        "project_dirs_scanned": len(all_project_dirs()),
    }


# --------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--project", default=".", help="project root (default: cwd)")
    ap.add_argument("--user", action="store_true",
                    help="cross-project mode: judge the user-level file only")
    ap.add_argument("--days", type=int, default=30,
                    help="transcript lookback window (default: 30)")
    ap.add_argument("--no-transcripts", action="store_true",
                    help="skip the transcript fallback entirely")
    ap.add_argument("--json", action="store_true",
                    help="accepted for symmetry; output is always JSON")
    args = ap.parse_args()

    payload = {
        "generated": datetime.now(timezone.utc).isoformat(),
        "mode": "user" if args.user else "project",
        "extract_cap_bytes": EXTRACT_CAP_BYTES,
    }

    if args.user:
        payload.update(collect_user_mode())
        json.dump(payload, sys.stdout, indent=1)
        sys.stdout.write("\n")
        return 0

    root = Path(args.project).expanduser().resolve()
    if not root.is_dir():
        print(f"collect: no such project root: {root}", file=sys.stderr)
        return 2

    mem_dir = auto_memory_dir(root)
    feedback = collect_feedback(mem_dir)

    payload["project_root"] = str(root)
    payload["instruction_files"] = collect_targets(root)
    payload["auto_memory"] = collect_auto_memory(root)
    payload["feedback_memories"] = feedback

    # The transcript grep is a fallback, not a default input: where a typed
    # feedback corpus exists it is already the better citation, and reading
    # transcripts costs orders of magnitude more.
    if args.no_transcripts:
        payload["transcript"] = {"used": False, "reason": "--no-transcripts"}
    elif len(feedback) >= 5:
        payload["transcript"] = {
            "used": False,
            "reason": f"feedback corpus sufficient ({len(feedback)} typed memories)",
        }
    else:
        payload["transcript"] = collect_transcripts(root, args.days)

    json.dump(payload, sys.stdout, indent=1)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
