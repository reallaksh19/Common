#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRANSFER = json.loads((ROOT / "registry" / "physics-core1a-motion-in-a-plane-sba06-transfer-v1.json").read_text(encoding="utf-8"))
PROFILE = json.loads((ROOT / "registry" / "physics-core1a-motion-in-a-plane-sba06-20pct-v1.json").read_text(encoding="utf-8"))
MANIFEST = json.loads((ROOT / "registry" / "build-manifests" / "M2D-SBA-06-v1.json").read_text(encoding="utf-8"))
POLICY = json.loads((ROOT / "registry" / "physics-core1a-publication-policy.json").read_text(encoding="utf-8"))

assert TRANSFER["bucket_id"] == "M2D-SBA-06"
routines = TRANSFER["transfer_routines"]
assert {r["routine_id"] for r in routines} == {"M2D-SBA-06-R1", "M2D-SBA-06-R2"}

mapped = []
for routine in routines:
    mapped.extend(routine["core2_questions"])
    assert len(routine["method_steps"]) >= 4
    assert routine["independent_practice"]["prompt"]
    assert routine["independent_practice"]["answer_check"]
    assert [h["rung"] for h in routine["hint_ladder"]] == ["H1", "H2", "H3"]
    assert len(routine["readiness_checks"]) == 4
    assert routine["release_rule"]

assert mapped == ["Q38", "Q47"]
assert len(set(mapped)) == 2

bucket = PROFILE["buckets"][0]
assert bucket["bucket_id"] == "M2D-SBA-06"
assert bucket["intrinsic_difficulty"] == "D3"
assert bucket["core2_primary_questions"] == ["Q38", "Q47"]
assert len(bucket["profiles"][0]["learning_atoms"]) == 8

assert MANIFEST["question_load"] == {"count": 2, "class": "LOW", "minimum_transfer_families": 1}
assert [q["question_id"] for q in MANIFEST["question_release"]] == ["Q38", "Q47"]
assert all(q["status"] == "RELEASED" for q in MANIFEST["question_release"])
assert set(MANIFEST["transfer_routines"]) == {"M2D-SBA-06-R1", "M2D-SBA-06-R2"}
assert MANIFEST["publication_plan"]["independent_practice_policy"] == "ATTEMPT_BEFORE_HINTS"
assert MANIFEST["publication_plan"]["hint_delivery_policy"] == "NEXT_PAGE"
assert MANIFEST["publication_plan"]["readiness_gate_policy"] == "RECOGNISE_REPRESENT_FIRST_MOVE_FINISH"

page = POLICY["page"]
assert page["page_section_heading_max_pt"] <= 16.0
assert page["long_page_heading_max_pt"] <= 14.5
assert POLICY["learner_ui"]["professionalisation_may_not_remove_instructional_functions"] is True

print("SBA06 transfer and professional-lossless checks passed.")
