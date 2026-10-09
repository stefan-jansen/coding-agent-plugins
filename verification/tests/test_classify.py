"""Independent classification: one family's answers never reach the other's prompt."""
import json
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))

from verification import classify  # noqa: E402


def rows(path):
    return [json.loads(x) for x in (path / "causes.jsonl").read_text().splitlines()]


@pytest.fixture
def store(tmp_path):
    causes = [
        {
            "id": "crypto-gap",
            "summary": "features across 49-73 hour gaps",
            "sources": ["audit:r2p"],
            "classification": {"claude": "premise"},
        },
        {
            "id": "digest",
            "summary": "run digest ignores code",
            "sources": ["commit:dbeaeb2"],
            "classification": {"gpt": "term"},
        },
    ]
    (tmp_path / "causes.jsonl").write_text("".join(json.dumps(c) + "\n" for c in causes))
    return tmp_path


def test_other_family_answer_not_in_prompt(store):
    # Prevents: the second family anchoring on the first family's classification.
    prompts = []

    def ask(family, prompt):
        prompts.append(prompt)
        return '{"crypto-gap": {"category": "premise"}}'

    assert classify.classify(str(store), "gpt", ask=ask) == 1
    assert "crypto-gap" in prompts[0] and "digest" not in prompts[0]
    assert "claude" not in prompts[0]
    assert rows(store)[0]["classification"] == {"claude": "premise", "gpt": "premise"}


def test_invalid_category_writes_nothing(store):
    # Prevents: a malformed reply leaving the corpus half-classified.
    before = (store / "causes.jsonl").read_text()

    def ask(family, prompt):
        return '```json\n{"crypto-gap": {"category": "lookahead"}}\n```'

    with pytest.raises(ValueError, match="crypto-gap"):
        classify.classify(str(store), "gpt", ask=ask)
    assert (store / "causes.jsonl").read_text() == before


def test_existing_classification_is_not_redone(store):
    # Prevents: a rerun overwriting a family's earlier answer.
    seen = []

    def ask(family, prompt):
        seen.append(prompt)
        return '{"digest": {"category": "other", "other_description": "identity of a run"}}'

    classify.classify(str(store), "claude", ask=ask)
    assert "crypto-gap" not in seen[0]
    got = rows(store)[1]
    assert got["classification"] == {"gpt": "term", "claude": "other"}
    assert got["other_description"] == "claude: identity of a run"
