"""Row formats for the store. Each store file is JSONL, one row per line.

A format maps field name -> (required, check). A check returns None or a reason.
Cross-field rules live in the `rules` function of each format.
"""

import datetime
import re

CATEGORIES = ("term", "premise", "claim", "retrieval", "test")
ENFORCEMENT_LEVELS = ("unrepresentable", "check", "test", "prose")
ADMISSION_TESTS = (
    "durability",
    "specificity",
    "decision-changing",
    "no-stronger-mechanism",
    "no-duplicate",
)
SOURCE_PREFIXES = ("errata:", "issue:", "audit:", "quarantine:", "commit:")

_SLUG = re.compile(r"^[a-z0-9][a-z0-9-]*$")


def _str(v):
    return None if isinstance(v, str) and v.strip() else "must be a non-empty string"


def _one_line(v):
    return _str(v) or ("must be one line" if "\n" in v else None)


def _slug(v):
    return _str(v) or (None if _SLUG.match(v) else "must be a lowercase slug")


def _str_list(v):
    if not isinstance(v, list) or not v or not all(isinstance(x, str) and x for x in v):
        return "must be a non-empty list of strings"
    return None


def _bool(v):
    return None if isinstance(v, bool) else "must be true or false"


def _date(v):
    try:
        datetime.date.fromisoformat(v)
        return None
    except (TypeError, ValueError):
        return "must be an ISO date"


def _one_of(choices):
    def check(v):
        return None if v in choices else f"must be one of {', '.join(choices)}"

    return check


def _subset_of(choices):
    def check(v):
        if not isinstance(v, list) or any(x not in choices for x in v):
            return f"must be a list drawn from {', '.join(choices)}"
        return None

    return check


def _entry_rules(row):
    enf = row.get("enforcement")
    if not isinstance(enf, dict):
        return ["enforcement: must be an object with a level"]
    errors = []
    level = enf.get("level")
    if level not in ENFORCEMENT_LEVELS:
        errors.append(f"enforcement.level: must be one of {', '.join(ENFORCEMENT_LEVELS)}")
    if level == "prose" and _str(enf.get("reason")):
        errors.append("enforcement.reason: a prose entry must say why stronger levels failed")
    if level in ("unrepresentable", "check") and _str(enf.get("where")):
        errors.append(f"enforcement.where: a {level} entry must point to the enforcing code")
    if level in ("check", "test"):
        for field in ("test", "violated_variant"):
            if _str(row.get(field)):
                errors.append(f"{field}: required at enforcement level {level}")
    if row.get("institutional") is True and _str(row.get("source")):
        errors.append("source: an institutional entry must cite an authoritative source")
    return errors


def _cause_rules(row):
    errors = []
    if _str(row.get("pre_defect_commit")) and _str(row.get("unrecoverable_reason")):
        errors.append("pre_defect_commit: give the commit or an unrecoverable_reason")
    cls = row.get("classification")
    if not isinstance(cls, dict) or not cls:
        return errors + ["classification: must map each model family to a category"]
    for family, cat in cls.items():
        if cat not in CATEGORIES + ("other",):
            errors.append(f"classification.{family}: unknown category {cat!r}")
    if "other" in cls.values() and _str(row.get("other_description")):
        errors.append("other_description: required when a family classified as other")
    for src in row.get("sources") or []:
        if not src.startswith(SOURCE_PREFIXES):
            errors.append(f"sources: {src!r} lacks a known prefix {SOURCE_PREFIXES}")
    return errors


FORMATS = {
    "entries.jsonl": {
        "fields": {
            "id": (True, _slug),
            "shape": (True, _str_list),
            "context": (True, _str_list),
            "violation": (True, _one_line),
            "test": (False, None),
            "violated_variant": (False, None),
            "enforcement": (True, None),
            "institutional": (True, _bool),
            "source": (False, _str),
            "fired": (True, lambda v: None if isinstance(v, list) else "must be a list"),
            "admission": (True, _subset_of(ADMISSION_TESTS)),
        },
        "pointers": ("test", "violated_variant", "enforcement.where", "source"),
        "rules": _entry_rules,
        "token_limit": 120,
    },
    "definitions.jsonl": {
        "fields": {
            "id": (True, _slug),
            "term": (True, _one_line),
            "context": (True, _str_list),
            "definition": (True, _str),
            "decided_by": (True, _str),
            "decided_on": (True, _date),
            "origin": (True, _str),
        },
        "pointers": ("origin",),
        "rules": lambda row: [],
    },
    "causes.jsonl": {
        "fields": {
            "id": (True, _slug),
            "summary": (True, _one_line),
            "sources": (True, _str_list),
            "spec": (False, _str),
            "pre_defect_commit": (False, _str),
            "unrecoverable_reason": (False, _str),
            "reproduction": (False, _str),
            "classification": (True, None),
            "other_description": (False, _str),
        },
        "pointers": ("spec", "pre_defect_commit", "reproduction"),
        "rules": _cause_rules,
    },
    "misses.jsonl": {
        "fields": {
            "id": (True, _slug),
            "date": (True, _date),
            "reported_by": (True, _str),
            "defect": (True, _one_line),
            "classification": (True, _one_of(CATEGORIES)),
            "pointer": (False, _str),
        },
        "pointers": ("pointer",),
        "rules": lambda row: [],
    },
    "replays.jsonl": {
        "fields": {
            "run_id": (True, _str),
            "cause_id": (True, _slug),
            "date": (True, _date),
            "surfaced_by": (True, _one_of(CATEGORIES + ("none",))),
            "transcript": (True, _str),
            "blind": (True, _bool),
        },
        "pointers": ("transcript",),
        "rules": lambda row: [],
    },
}


def validate_row(name, row):
    """Return a list of reasons the row does not match its format."""
    fmt = FORMATS[name]
    if not isinstance(row, dict):
        return ["row must be a JSON object"]
    errors = []
    for field, (required, check) in fmt["fields"].items():
        if field not in row or row[field] is None:
            if required:
                errors.append(f"{field}: missing")
            continue
        if check:
            reason = check(row[field])
            if reason:
                errors.append(f"{field}: {reason}")
    unknown = sorted(set(row) - set(fmt["fields"]))
    if unknown:
        errors.append(f"unknown fields: {', '.join(unknown)}")
    return errors + fmt["rules"](row)


def pointer_values(name, row):
    """Yield (field, value) for every pointer-valued field present in the row."""
    for field in FORMATS[name]["pointers"]:
        value = row
        for part in field.split("."):
            value = value.get(part) if isinstance(value, dict) else None
        if isinstance(value, str) and value:
            yield field, value
