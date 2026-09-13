#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "contracts" / "physics-core1a-subtopic-bucket.schema.json"
REGISTRY = ROOT / "registry" / "physics-core1a-motion-in-a-plane-sba-v1.json"
SBA04_PROFILE = ROOT / "registry" / "physics-core1a-motion-in-a-plane-sba04-20pct-v1.json"

schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
sba04_profile = json.loads(SBA04_PROFILE.read_text(encoding="utf-8"))
validator = Draft202012Validator(schema)
Draft202012Validator.check_schema(schema)
validator.validate(registry)
validator.validate(sba04_profile)

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

policy = registry["policy"]
assert policy["target_prior_knowledge_pct"] == [20, 50]
assert "Skip dedicated SBA PDFs" in policy["production_selection_rule"]
assert "H1/H2/H3" in policy["core2_hint_preteach_rule"]

# Detailed SBA04: 20%-knowledge D3 bucket must teach all primary hint rungs.
b04 = sba04_profile["buckets"][0]
assert b04["bucket_id"] == "M2D-SBA-04"
assert b04["intrinsic_difficulty"] == "D3"
assert b04["core2_primary_questions"] == by_id["M2D-SBA-04"]["core2_primary_questions"]
profile20 = next(p for p in b04["profiles"] if p["prior_knowledge_pct"] == 20)
assert profile20["pathway"] == "FOUNDATION_PATH"
assert len(profile20["learning_atoms"]) >= 7
assert max(a["visual_stage_count"] for a in profile20["learning_atoms"]) >= 5

coverage = {q["question_id"]: q for q in profile20["core2_hint_coverage"]}
assert set(coverage) == set(b04["core2_primary_questions"])
for qid, q in coverage.items():
    assert [r["rung"] for r in q["hint_rungs"]] == ["H1", "H2", "H3"]
    assert all(r["pre_taught"] is True for r in q["hint_rungs"])

# Q14 and Q27 use same-height range/height relations beyond SBA04; do not release early.
assert coverage["Q14"]["release_prerequisite_buckets"] == ["M2D-SBA-05"]
assert coverage["Q27"]["release_prerequisite_buckets"] == ["M2D-SBA-05"]
for qid in ["Q01", "Q11", "Q13", "Q17", "Q40"]:
    assert coverage[qid]["release_prerequisite_buckets"] == []

print("Core1A SBA schema/index/profile checks passed.")
