#!/usr/bin/env python3
from __future__ import annotations

import copy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KIT = ROOT / "production_kit"
sys.path.insert(0, str(KIT))

from build_learning_representation import build_from_fixture
from task_router import load_json, route
from validate_learning_representation import validate_fixture_and_lr

FIXTURES = ROOT / "fixtures" / "golden"
paths = sorted(FIXTURES.glob("M2D-SBA-*.json"))
assert [p.name for p in paths] == ["M2D-SBA-03.json", "M2D-SBA-05.json", "M2D-SBA-21.json"]

expected = {
    "M2D-SBA-03": {"class": "LOW", "families": 1, "source_mode": "THEORY_BACKED"},
    "M2D-SBA-05": {"class": "VERY_HIGH", "families": 7, "source_mode": "THEORY_BACKED"},
    "M2D-SBA-21": {"class": "MEDIUM", "families": 3, "source_mode": "SOURCE_VISIBLE_EXTENSION"},
}

for path in paths:
    fixture = load_json(path)
    task = route(fixture["bucket_id"], fixture["prior_knowledge_pct"])
    lr = build_from_fixture(fixture)
    report = validate_fixture_and_lr(fixture, lr)
    exp = expected[fixture["bucket_id"]]
    assert report["status"] == "PASS"
    assert task["question_load"]["class"] == exp["class"]
    assert len(lr["transfer_families"]) == exp["families"]
    assert lr["source_mode"] == exp["source_mode"]
    assert lr["scaffold_profile_id"] == task["scaffold_profile_id"]

# Default routing must agree with durable build state.
state = load_json(ROOT / "registry" / "physics-core1a-motion-in-a-plane-build-state-v1.json")
default_task = route()
assert default_task["bucket_id"] == state["next_active_bucket"]

# Zero-primary buckets must never produce a dedicated production task.
try:
    route("M2D-SBA-08", 20)
    raise AssertionError("Skipped bucket unexpectedly routed.")
except ValueError:
    pass

# Falsifier 1: non-clean source cannot be silently used.
fx = load_json(FIXTURES / "M2D-SBA-03.json")
mut = copy.deepcopy(fx)
mut["source_contract"]["source_items"][0]["integrity_class"] = "TYPOGRAPHIC_OCR_AMBIGUITY"
mut["source_contract"]["source_items"][0]["use_policy"] = "USE"
lr = build_from_fixture(mut)
try:
    validate_fixture_and_lr(mut, lr)
    raise AssertionError("Source-integrity falsifier did not fire.")
except ValueError as e:
    assert "non-clean source cannot be silently USE" in str(e)

# Falsifier 2: a Core2 hint cannot point to an un-taught atom.
mut = copy.deepcopy(fx)
mut["answer_contract"]["questions"][0]["hint_ladder"][2]["learning_atom"] = "M2D-SBA-03Z"
lr = build_from_fixture(mut)
try:
    validate_fixture_and_lr(mut, lr)
    raise AssertionError("Hint-preteach falsifier did not fire.")
except ValueError as e:
    assert "learning atom" in str(e)

# Falsifier 3: primary questions cannot be duplicated across transfer families.
fx21 = load_json(FIXTURES / "M2D-SBA-21.json")
mut = copy.deepcopy(fx21)
mut["authoring"]["transfer_families"][1]["core2_questions"].append("Q54")
lr = build_from_fixture(mut)
try:
    validate_fixture_and_lr(mut, lr)
    raise AssertionError("Transfer coverage falsifier did not fire.")
except ValueError as e:
    assert "more than one transfer family" in str(e)

print("Core1A production-kit contracts/router/builder/validator/golden-fixture checks passed.")
