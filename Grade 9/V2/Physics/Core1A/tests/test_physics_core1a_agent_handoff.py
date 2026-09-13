#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / "contracts" / "physics-core1a-sba-build-manifest.schema.json").read_text(encoding="utf-8"))
REGISTRY = json.loads((ROOT / "registry" / "physics-core1a-motion-in-a-plane-sba-v1.json").read_text(encoding="utf-8"))
INDEX = json.loads((ROOT / "registry" / "physics-core1a-motion-in-a-plane-sba-publication-index-v1.json").read_text(encoding="utf-8"))
STATE = json.loads((ROOT / "registry" / "physics-core1a-motion-in-a-plane-build-state-v1.json").read_text(encoding="utf-8"))
MANIFEST_DIR = ROOT / "registry" / "build-manifests"

validator = Draft202012Validator(SCHEMA)
Draft202012Validator.check_schema(SCHEMA)

by_id = {b["bucket_id"]: b for b in REGISTRY["buckets"]}
expected_gate_order = [
    "G0_INDEX_SYNC",
    "G1_SOURCE_AND_CORE2_AUDIT",
    "G2_DIFFICULTY_AND_READINESS",
    "G3_LEARNING_ATOM_DECOMPOSITION",
    "G4_CORE2_HINT_PRETEACH_AUDIT",
    "G5_PROBLEM_FAMILY_ASSIMILATION",
    "G6_PAGE_PLAN",
    "G7_RENDER_AND_VISUAL_AUDIT",
    "G8_READINESS_AND_TRANSFER_AUDIT",
    "G9_MACHINE_QA_AND_HANDOFF",
]


def load_class(n: int) -> str:
    if n <= 2:
        return "LOW"
    if n <= 5:
        return "MEDIUM"
    if n <= 9:
        return "HIGH"
    return "VERY_HIGH"


completed = STATE["completed_active_buckets"]
assert completed, "build state must include at least one completed active bucket"
active_ids = [b["bucket_id"] for b in REGISTRY["buckets"] if b["production_status"] == "ACTIVE"]
# Completed buckets must be an ordered prefix of the active queue, with zero-primary buckets absent by construction.
assert completed == active_ids[:len(completed)]
assert STATE["last_completed_bucket"] == completed[-1]

for bucket_id in completed:
    path = MANIFEST_DIR / f"{bucket_id}-v1.json"
    assert path.exists(), f"missing build manifest for {bucket_id}"
    manifest = json.loads(path.read_text(encoding="utf-8"))
    validator.validate(manifest)

    canonical = by_id[bucket_id]
    assert manifest["primary_questions"] == canonical["core2_primary_questions"]
    assert manifest["question_load"]["count"] == len(manifest["primary_questions"])
    assert manifest["question_load"]["class"] == load_class(len(manifest["primary_questions"]))
    assert len(manifest["transfer_routines"]) >= manifest["question_load"]["minimum_transfer_families"]

    gates = manifest["phase_gates"]
    assert [g["gate"] for g in gates] == expected_gate_order
    if manifest["handoff"]["status"] == "COMPLETE":
        assert all(g["status"] == "PASS" for g in gates)
        assert all(manifest["qa"].values())

    release = manifest["question_release"]
    assert {r["question_id"] for r in release} == set(manifest["primary_questions"])
    assert len({r["question_id"] for r in release}) == len(release)
    routines = set(manifest["transfer_routines"])
    for r in release:
        if r["status"] == "RELEASED":
            assert r["routine_id"] in routines
            assert r["release_prerequisite_buckets"] == []
        else:
            assert r["release_prerequisite_buckets"], f"held {r['question_id']} needs an explicit prerequisite"
            if r["routine_id"] is not None:
                assert r["routine_id"] in routines

    order = manifest["publication_plan"]["macro_order"]
    assert order[0] == "SBA_INDEX"
    for required in ["PROBLEM_FAMILY_ROUTINES", "INDEPENDENT_PRACTICE", "HINTS", "READINESS", "CORE2_TRANSFER_SUMMARY"]:
        assert required in order
    assert order.index("INDEPENDENT_PRACTICE") < order.index("HINTS") < order.index("READINESS") < order.index("CORE2_TRANSFER_SUMMARY")

# Publication index must agree with canonical SBA registry for all rows already published.
for row in INDEX["rows"]:
    canonical = by_id[row["bucket_id"]]
    assert row["core2_primary_questions"] == canonical["core2_primary_questions"]
    assert row["core1a_teaching_home"] == canonical["core1a_homes"]

# Build-state must derive the next active bucket, not rely on memory or page order.
remaining = [bid for bid in active_ids if bid not in set(completed)]
derived_next = remaining[0] if remaining else None
assert STATE["next_active_bucket"] == derived_next

# Reference cases preserve load scaling and professional-lossless behavior.
assert load_class(len(by_id["M2D-SBA-03"]["core2_primary_questions"])) == "LOW"
assert load_class(len(by_id["M2D-SBA-04"]["core2_primary_questions"])) == "HIGH"
assert load_class(len(by_id["M2D-SBA-05"]["core2_primary_questions"])) == "VERY_HIGH"
assert load_class(len(by_id["M2D-SBA-06"]["core2_primary_questions"])) == "LOW"
assert load_class(len(by_id["M2D-SBA-07"]["core2_primary_questions"])) == "HIGH"
assert "PROFESSIONAL_TEXTBOOK_SPEC.md" in STATE["required_start_files"]

print("Core1A agent handoff/build-state checks passed.")
