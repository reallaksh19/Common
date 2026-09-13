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
SBA07_PROFILE = ROOT / "registry" / "physics-core1a-motion-in-a-plane-sba07-20pct-v1.json"
TRANSFER = ROOT / "registry" / "physics-core1a-motion-in-a-plane-transfer-routines-v1.json"

schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
sba04_profile = json.loads(SBA04_PROFILE.read_text(encoding="utf-8"))
sba05_profile = json.loads(SBA05_PROFILE.read_text(encoding="utf-8"))
sba06_profile = json.loads(SBA06_PROFILE.read_text(encoding="utf-8"))
sba07_profile = json.loads(SBA07_PROFILE.read_text(encoding="utf-8"))
transfer = json.loads(TRANSFER.read_text(encoding="utf-8"))
validator = Draft202012Validator(schema)
Draft202012Validator.check_schema(schema)
for doc in [registry, sba04_profile, sba05_profile, sba06_profile, sba07_profile]:
    validator.validate(doc)

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
assert sorted(all_q) == expected_q
assert len(all_q) == len(set(all_q)) == 59

by_id = {b["bucket_id"]: b for b in buckets}
assert by_id["M2D-SBA-03"]["core2_primary_questions"] == ["Q10", "Q43"]
assert by_id["M2D-SBA-04"]["core2_primary_questions"] == ["Q01", "Q11", "Q13", "Q14", "Q17", "Q27", "Q40"]
assert by_id["M2D-SBA-05"]["core2_primary_questions"] == [
    "Q02", "Q06", "Q07", "Q12", "Q16", "Q18", "Q19", "Q20", "Q22", "Q24", "Q25", "Q44", "Q52"
]
assert by_id["M2D-SBA-06"]["core2_primary_questions"] == ["Q38", "Q47"]
assert by_id["M2D-SBA-07"]["core2_primary_questions"] == ["Q03", "Q04", "Q08", "Q09", "Q29", "Q30", "Q34", "Q36", "Q42"]

policy = registry["policy"]
assert policy["target_prior_knowledge_pct"] == [20, 50]
assert "Skip dedicated SBA PDFs" in policy["production_selection_rule"]
assert "H1/H2/H3" in policy["core2_hint_preteach_rule"]

# Transfer-routine registry is validated against the schema's transferRoutine definition.
routine_schema = {"type": "array", "items": schema["$defs"]["transferRoutine"]}
routine_validator = Draft202012Validator(routine_schema)
transfer_by_bucket = {b["bucket_id"]: b for b in transfer["buckets"]}
assert set(transfer_by_bucket) == {"M2D-SBA-03", "M2D-SBA-04"}
for tb in transfer["buckets"]:
    assert tb["prior_knowledge_pct"] == 20
    routine_validator.validate(tb["transfer_routines"])

# SBA03 transfer contract: Q10 gets a full problem-family routine; Q43 stays held for SBA04.
r03 = transfer_by_bucket["M2D-SBA-03"]["transfer_routines"]
assert len(r03) == 1
assert r03[0]["routine_id"] == "M2D-SBA-03-R1"
assert r03[0]["core2_questions"] == ["Q10"]
assert len(r03[0]["method_steps"]) >= 4
assert [h["rung"] for h in r03[0]["hint_ladder"]] == ["H1", "H2", "H3"]
assert len(r03[0]["readiness_checks"]) >= 4
assert "hold Q43" in r03[0]["release_rule"]

# SBA04: D3/20% must contain concept build plus problem-family transfer routines.
b04 = sba04_profile["buckets"][0]
assert b04["bucket_id"] == "M2D-SBA-04"
assert b04["intrinsic_difficulty"] == "D3"
assert b04["core2_primary_questions"] == by_id["M2D-SBA-04"]["core2_primary_questions"]
p04 = next(p for p in b04["profiles"] if p["prior_knowledge_pct"] == 20)
assert p04["pathway"] == "FOUNDATION_PATH"
assert len(p04["learning_atoms"]) >= 7
assert max(a["visual_stage_count"] for a in p04["learning_atoms"]) >= 5
coverage04 = {q["question_id"]: q for q in p04["core2_hint_coverage"]}
assert set(coverage04) == set(b04["core2_primary_questions"])
for qid, q in coverage04.items():
    assert [r["rung"] for r in q["hint_rungs"]] == ["H1", "H2", "H3"]
    assert all(r["pre_taught"] is True for r in q["hint_rungs"])
assert coverage04["Q14"]["release_prerequisite_buckets"] == ["M2D-SBA-05"]
assert coverage04["Q27"]["release_prerequisite_buckets"] == ["M2D-SBA-05"]
for qid in ["Q01", "Q11", "Q13", "Q17", "Q40"]:
    assert coverage04[qid]["release_prerequisite_buckets"] == []

r04 = {r["routine_id"]: r for r in transfer_by_bucket["M2D-SBA-04"]["transfer_routines"]}
assert set(r04) == {"M2D-SBA-04-R1", "M2D-SBA-04-R2", "M2D-SBA-04-R3", "M2D-SBA-04-R4"}
assert r04["M2D-SBA-04-R1"]["core2_questions"] == ["Q11", "Q17"]
assert r04["M2D-SBA-04-R2"]["core2_questions"] == ["Q01", "Q13"]
assert r04["M2D-SBA-04-R3"]["core2_questions"] == ["Q40"]
assert r04["M2D-SBA-04-R4"]["core2_questions"] == ["Q14", "Q27"]
assert r04["M2D-SBA-04-R4"]["release_prerequisite_buckets"] == ["M2D-SBA-05"]
for routine in r04.values():
    assert len(routine["method_steps"]) >= 4
    assert [h["rung"] for h in routine["hint_ladder"]] == ["H1", "H2", "H3"]
    assert routine["independent_practice"]["prompt"]
    assert routine["independent_practice"]["answer_check"]
    assert len(routine["readiness_checks"]) >= 4

# Detailed SBA05: 20%-knowledge D2 bucket must teach all 13 primary question hint ladders.
b05 = sba05_profile["buckets"][0]
assert b05["bucket_id"] == "M2D-SBA-05"
assert b05["intrinsic_difficulty"] == "D2"
assert b05["core2_primary_questions"] == by_id["M2D-SBA-05"]["core2_primary_questions"]
p05 = next(p for p in b05["profiles"] if p["prior_knowledge_pct"] == 20)
assert len(p05["learning_atoms"]) >= 9
coverage05 = {q["question_id"]: q for q in p05["core2_hint_coverage"]}
assert set(coverage05) == set(b05["core2_primary_questions"])
for q in coverage05.values():
    assert [r["rung"] for r in q["hint_rungs"]] == ["H1", "H2", "H3"]
    assert all(r["pre_taught"] is True for r in q["hint_rungs"])

# Detailed SBA06: trajectory bucket remains source/hint complete.
b06 = sba06_profile["buckets"][0]
assert b06["bucket_id"] == "M2D-SBA-06"
p06 = next(p for p in b06["profiles"] if p["prior_knowledge_pct"] == 20)
assert len(p06["learning_atoms"]) >= 8
coverage06 = {q["question_id"]: q for q in p06["core2_hint_coverage"]}
assert set(coverage06) == {"Q38", "Q47"}

# Detailed SBA07: high-load D2 bucket must teach all nine primary hint ladders.
b07 = sba07_profile["buckets"][0]
assert b07["bucket_id"] == "M2D-SBA-07"
assert b07["intrinsic_difficulty"] == "D2"
assert b07["core2_primary_questions"] == by_id["M2D-SBA-07"]["core2_primary_questions"]
p07 = next(p for p in b07["profiles"] if p["prior_knowledge_pct"] == 20)
assert p07["pathway"] == "FOUNDATION_PATH"
assert len(p07["learning_atoms"]) >= 8
assert max(a["visual_stage_count"] for a in p07["learning_atoms"]) >= 5
coverage07 = {q["question_id"]: q for q in p07["core2_hint_coverage"]}
assert set(coverage07) == set(b07["core2_primary_questions"])
for q in coverage07.values():
    assert [r["rung"] for r in q["hint_rungs"]] == ["H1", "H2", "H3"]
    assert all(r["pre_taught"] is True for r in q["hint_rungs"])

print("Core1A SBA schema/index/profile/transfer checks passed.")
