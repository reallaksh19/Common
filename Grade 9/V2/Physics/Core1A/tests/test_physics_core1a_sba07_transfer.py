#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRANSFER = json.loads((ROOT / "registry" / "physics-core1a-motion-in-a-plane-sba07-transfer-v1.json").read_text(encoding="utf-8"))
PROFILE = json.loads((ROOT / "registry" / "physics-core1a-motion-in-a-plane-sba07-20pct-v1.json").read_text(encoding="utf-8"))
MANIFEST = json.loads((ROOT / "registry" / "build-manifests" / "M2D-SBA-07-v1.json").read_text(encoding="utf-8"))
INDEX = json.loads((ROOT / "registry" / "physics-core1a-motion-in-a-plane-sba-publication-index-v1.json").read_text(encoding="utf-8"))
POLICY = json.loads((ROOT / "registry" / "physics-core1a-publication-policy.json").read_text(encoding="utf-8"))

assert TRANSFER["bucket_id"] == "M2D-SBA-07"
routines = TRANSFER["transfer_routines"]
assert {r["routine_id"] for r in routines} == {f"M2D-SBA-07-R{i}" for i in range(1, 5)}

mapped = []
for routine in routines:
    mapped.extend(routine["core2_questions"])
    assert len(routine["method_steps"]) >= 4
    assert routine["independent_practice"]["prompt"]
    assert routine["independent_practice"]["answer_check"]
    assert [h["rung"] for h in routine["hint_ladder"]] == ["H1", "H2", "H3"]
    assert len(routine["readiness_checks"]) == 4
    assert routine["release_rule"]

expected = ["Q03", "Q04", "Q08", "Q09", "Q29", "Q30", "Q34", "Q36", "Q42"]
assert sorted(mapped) == sorted(expected)
assert len(mapped) == len(set(mapped)) == 9

bucket = PROFILE["buckets"][0]
assert bucket["bucket_id"] == "M2D-SBA-07"
assert bucket["intrinsic_difficulty"] == "D2"
assert bucket["core2_primary_questions"] == expected
profile = bucket["profiles"][0]
assert profile["prior_knowledge_pct"] == 20
assert len(profile["learning_atoms"]) == 8
assert {x["question_id"] for x in profile["core2_hint_coverage"]} == set(expected)
for q in profile["core2_hint_coverage"]:
    assert [h["rung"] for h in q["hint_rungs"]] == ["H1", "H2", "H3"]
    assert all(h["pre_taught"] for h in q["hint_rungs"])

assert MANIFEST["question_load"] == {"count": 9, "class": "HIGH", "minimum_transfer_families": 3}
assert set(q["question_id"] for q in MANIFEST["question_release"]) == set(expected)
assert all(q["status"] == "RELEASED" for q in MANIFEST["question_release"])
assert set(MANIFEST["transfer_routines"]) == {f"M2D-SBA-07-R{i}" for i in range(1, 5)}
assert MANIFEST["publication_plan"]["independent_practice_policy"] == "ATTEMPT_BEFORE_HINTS"
assert MANIFEST["publication_plan"]["hint_delivery_policy"] == "NEXT_PAGE"
assert MANIFEST["publication_plan"]["readiness_gate_policy"] == "RECOGNISE_REPRESENT_FIRST_MOVE_FINISH"
assert MANIFEST["handoff"]["next_active_bucket"] == "M2D-SBA-21"
assert MANIFEST["handoff"]["status"] in {"IN_PROGRESS", "COMPLETE"}
if MANIFEST["handoff"]["status"] == "COMPLETE":
    assert MANIFEST["qa"]["ci_passed"] is True

rows = {r["bucket_id"]: r for r in INDEX["rows"]}
assert rows["M2D-SBA-07"]["core2_primary_questions"] == expected
assert rows["M2D-SBA-07"]["state"] in {"IN_PROGRESS", "BUILT"}

page = POLICY["page"]
assert page["page_section_heading_max_pt"] <= 16.0
assert page["long_page_heading_max_pt"] <= 14.5
assert POLICY["learner_ui"]["professionalisation_may_not_remove_instructional_functions"] is True

print("SBA07 transfer and professional-lossless checks passed.")
