#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "contracts" / "physics-core1a-subtopic-bucket.schema.json"
REGISTRY = ROOT / "registry" / "physics-core1a-motion-in-a-plane-sba-v1.json"
SBA04_PROFILE = ROOT / "registry" / "physics-core1a-motion-in-a-plane-sba04-20pct-v1.json"
SBA05_PROFILE = ROOT / "registry" / "physics-core1a-motion-in-a-plane-sba05-20pct-v1.json"
SBA06_PROFILE = ROOT / "registry" / "physics-core1a-motion-in-a-plane-sba06-20pct-v1.json"

schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
sba04_profile = json.loads(SBA04_PROFILE.read_text(encoding="utf-8"))
sba05_profile = json.loads(SBA05_PROFILE.read_text(encoding="utf-8"))
sba06_profile = json.loads(SBA06_PROFILE.read_text(encoding="utf-8"))
validator = Draft202012Validator(schema)
Draft202012Validator.check_schema(schema)
validator.validate(registry)
validator.validate(sba04_profile)
validator.validate(sba05_profile)
validator.validate(sba06_profile)

buckets = registry["buckets"]
assert len(buckets) == 31, f"expected 31 indexed SBA buckets, found {len(buckets)}"

ids = [b["bucket_id"] for b in buckets]
assert len(ids) == len(set(ids)), "duplicate SBA bucket IDs"
assert ids == [f"M2D-SBA-{i:02d}" for i in range(1, 32)], "SBA index must be contiguous 01..31"

all_q = []
for bucket in buckets:
    qs = bucket["core2_primary_questions"]
    all_q.extend(qs)
    if not qs:
        assert bucket["production_status"] == "SKIP_NO_PRIMARY_CORE2"
    else:
        assert bucket["production_status"] == "ACTIVE"

expected_q = [f"Q{i:02d}" for i in range(1, 60)]
assert sorted(all_q) == expected_q, "every Revised Core (2) v2 Q01..Q59 must appear exactly once as primary"
assert len(all_q) == len(set(all_q)) == 59

by_id = {b["bucket_id"]: b for b in buckets}
assert by_id["M2D-SBA-03"]["core2_primary_questions"] == ["Q10", "Q43"]
assert by_id["M2D-SBA-04"]["core2_primary_questions"] == ["Q01", "Q11", "Q13", "Q14", "Q17", "Q27", "Q40"]
assert by_id["M2D-SBA-05"]["core2_primary_questions"] == [
    "Q02", "Q06", "Q07", "Q12", "Q16", "Q18", "Q19", "Q20", "Q22", "Q24", "Q25", "Q44", "Q52"
]
assert by_id["M2D-SBA-06"]["core2_primary_questions"] == ["Q38", "Q47"]

policy = registry["policy"]
assert policy["target_prior_knowledge_pct"] == [20, 50]
assert "Skip dedicated SBA PDFs" in policy["production_selection_rule"]
assert "H1/H2/H3" in policy["core2_hint_preteach_rule"]

# Detailed SBA04: 20%-knowledge D3 bucket must teach all primary hint rungs.
b04 = sba04_profile["buckets"][0]
assert b04["bucket_id"] == "M2D-SBA-04"
assert b04["intrinsic_difficulty"] == "D3"
assert b04["core2_primary_questions"] == by_id["M2D-SBA-04"]["core2_primary_questions"]
profile04 = next(p for p in b04["profiles"] if p["prior_knowledge_pct"] == 20)
assert profile04["pathway"] == "FOUNDATION_PATH"
assert len(profile04["learning_atoms"]) >= 7
assert max(a["visual_stage_count"] for a in profile04["learning_atoms"]) >= 5

coverage04 = {q["question_id"]: q for q in profile04["core2_hint_coverage"]}
assert set(coverage04) == set(b04["core2_primary_questions"])
for qid, q in coverage04.items():
    assert [r["rung"] for r in q["hint_rungs"]] == ["H1", "H2", "H3"]
    assert all(r["pre_taught"] is True for r in q["hint_rungs"])

# Q14 and Q27 use same-height range/height relations beyond SBA04; do not release early.
assert coverage04["Q14"]["release_prerequisite_buckets"] == ["M2D-SBA-05"]
assert coverage04["Q27"]["release_prerequisite_buckets"] == ["M2D-SBA-05"]
for qid in ["Q01", "Q11", "Q13", "Q17", "Q40"]:
    assert coverage04[qid]["release_prerequisite_buckets"] == []

# Detailed SBA05: 20%-knowledge D2 bucket must teach all 13 primary question hint ladders.
b05 = sba05_profile["buckets"][0]
assert b05["bucket_id"] == "M2D-SBA-05"
assert b05["intrinsic_difficulty"] == "D2"
assert b05["core2_primary_questions"] == by_id["M2D-SBA-05"]["core2_primary_questions"]
assert b05["prerequisite_buckets"] == ["M2D-SBA-03", "M2D-SBA-04"]
profile05 = next(p for p in b05["profiles"] if p["prior_knowledge_pct"] == 20)
assert profile05["pathway"] == "FOUNDATION_PATH"
assert len(profile05["learning_atoms"]) >= 9
assert all(a["visual_stage_count"] >= 4 for a in profile05["learning_atoms"])
assert max(a["visual_stage_count"] for a in profile05["learning_atoms"]) >= 5

coverage05 = {q["question_id"]: q for q in profile05["core2_hint_coverage"]}
assert set(coverage05) == set(b05["core2_primary_questions"])
for qid, q in coverage05.items():
    assert [r["rung"] for r in q["hint_rungs"]] == ["H1", "H2", "H3"]
    assert all(r["pre_taught"] is True for r in q["hint_rungs"])
    assert q["release_prerequisite_buckets"] == [], f"SBA05 primary {qid} should release after SBA03/SBA04 prerequisites"

# SBA05 closes the explicit release dependency from SBA04 for Q14/Q27.
assert by_id["M2D-SBA-05"]["production_status"] == "ACTIVE"
assert any(
    "release Q14 and Q27" in check
    for atom in profile05["learning_atoms"]
    for check in atom["checks"]
), "SBA05 should explicitly close Q14/Q27 same-height dependency"

# Detailed SBA06: 20%-knowledge D3 trajectory bucket must pre-teach Q38 and Q47 hint ladders.
b06 = sba06_profile["buckets"][0]
assert b06["bucket_id"] == "M2D-SBA-06"
assert b06["intrinsic_difficulty"] == "D3"
assert b06["core2_primary_questions"] == by_id["M2D-SBA-06"]["core2_primary_questions"]
assert b06["prerequisite_buckets"] == ["M2D-SBA-03"]
profile06 = next(p for p in b06["profiles"] if p["prior_knowledge_pct"] == 20)
assert profile06["pathway"] == "FOUNDATION_PATH"
assert len(profile06["learning_atoms"]) >= 8
assert max(a["visual_stage_count"] for a in profile06["learning_atoms"]) >= 6

coverage06 = {q["question_id"]: q for q in profile06["core2_hint_coverage"]}
assert set(coverage06) == {"Q38", "Q47"}
for qid, q in coverage06.items():
    assert [r["rung"] for r in q["hint_rungs"]] == ["H1", "H2", "H3"]
    assert all(r["pre_taught"] is True for r in q["hint_rungs"])
    assert q["release_prerequisite_buckets"] == []

atom_ids = {a["atom_id"] for a in profile06["learning_atoms"]}
assert {"M2D-SBA-06C", "M2D-SBA-06E", "M2D-SBA-06F", "M2D-SBA-06H"}.issubset(atom_ids)
assert coverage06["Q38"]["hint_rungs"][0]["core1a_learning_atom"] == "M2D-SBA-06F"
assert coverage06["Q47"]["hint_rungs"][0]["core1a_learning_atom"] == "M2D-SBA-06E"

print("Core1A SBA schema/index/profile checks passed.")
