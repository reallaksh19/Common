#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
INDEX_SCHEMA = ROOT / "contracts" / "physics-core1a-sba-publication-index.schema.json"
INDEX = ROOT / "registry" / "physics-core1a-motion-in-a-plane-sba-publication-index-v1.json"
SBA_SCHEMA = ROOT / "contracts" / "physics-core1a-subtopic-bucket.schema.json"
BUILD_SCHEMA = ROOT / "contracts" / "physics-core1a-sba-build-manifest.schema.json"
SBA04_MANIFEST = ROOT / "registry" / "build-manifests" / "M2D-SBA-04-v1.json"
SBA05_MANIFEST = ROOT / "registry" / "build-manifests" / "M2D-SBA-05-v1.json"
SBA05_TRANSFER = ROOT / "registry" / "physics-core1a-motion-in-a-plane-sba05-transfer-v1.json"
MIGRATION_AUDIT = ROOT.parent / "Blueprint" / "topics" / "m2d-sba04-core1a-migration-audit.v1.json"

index_schema = json.loads(INDEX_SCHEMA.read_text(encoding="utf-8"))
index = json.loads(INDEX.read_text(encoding="utf-8"))
sba_schema = json.loads(SBA_SCHEMA.read_text(encoding="utf-8"))
build_schema = json.loads(BUILD_SCHEMA.read_text(encoding="utf-8"))
sba04_manifest = json.loads(SBA04_MANIFEST.read_text(encoding="utf-8"))
sba05_manifest = json.loads(SBA05_MANIFEST.read_text(encoding="utf-8"))
transfer = json.loads(SBA05_TRANSFER.read_text(encoding="utf-8"))
migration_audit = json.loads(MIGRATION_AUDIT.read_text(encoding="utf-8"))

Draft202012Validator.check_schema(index_schema)
Draft202012Validator(index_schema).validate(index)
Draft202012Validator.check_schema(build_schema)
Draft202012Validator(build_schema).validate(sba04_manifest)
Draft202012Validator(build_schema).validate(sba05_manifest)

assert index["render_as_first_step"] is True
assert index["columns"] == [
    "SBA index", "Subtopic bucket", "Origin", "Core (1A) teaching home", "Core (2) primary questions", "State"
]
rows = {row["bucket_id"]: row for row in index["rows"]}
# SBA05 regression checks must remain valid as the publication index grows.
assert list(rows)[:5] == [f"M2D-SBA-{i:02d}" for i in range(1, 6)]
assert rows["M2D-SBA-03"]["core2_primary_questions"] == ["Q10", "Q43"]
assert rows["M2D-SBA-04"]["core2_primary_questions"] == ["Q01", "Q11", "Q13", "Q14", "Q17", "Q27", "Q40"]
assert rows["M2D-SBA-05"]["core2_primary_questions"] == [
    "Q02", "Q06", "Q07", "Q12", "Q16", "Q18", "Q19", "Q20", "Q22", "Q24", "Q25", "Q44", "Q52"
]
assert all(rows[f"M2D-SBA-{i:02d}"]["state"] == "BUILT" for i in range(1, 6))

routine_schema = {"type": "array", "items": sba_schema["$defs"]["transferRoutine"]}
Draft202012Validator(routine_schema).validate(transfer["transfer_routines"])
assert transfer["bucket_id"] == "M2D-SBA-05"
assert transfer["prior_knowledge_pct"] == 20
routines = {r["routine_id"]: r for r in transfer["transfer_routines"]}
assert set(routines) == {f"M2D-SBA-05-R{i}" for i in range(1, 9)}

primary = []
for i in range(1, 8):
    r = routines[f"M2D-SBA-05-R{i}"]
    primary.extend(r["core2_questions"])
    assert len(r["method_steps"]) >= 4
    assert [h["rung"] for h in r["hint_ladder"]] == ["H1", "H2", "H3"]
    assert r["independent_practice"]["prompt"]
    assert r["independent_practice"]["answer_check"]
    assert len(r["readiness_checks"]) >= 4

expected_primary = ["Q02", "Q06", "Q07", "Q12", "Q16", "Q18", "Q19", "Q20", "Q22", "Q24", "Q25", "Q44", "Q52"]
assert sorted(primary) == sorted(expected_primary)
assert len(primary) == len(set(primary)) == 13

cross = routines["M2D-SBA-05-R8"]
assert cross["core2_questions"] == ["Q14", "Q27"]
assert cross["release_prerequisite_buckets"] == ["M2D-SBA-04"]
assert "both SBA-04 and SBA-05" in cross["release_rule"]
assert len(cross["method_steps"]) >= 4
assert [h["rung"] for h in cross["hint_ladder"]] == ["H1", "H2", "H3"]
assert len(cross["readiness_checks"]) >= 4

# Cross-bucket release authority: both authored products are complete before Q14/Q27 can leave HELD.
for manifest in (sba04_manifest, sba05_manifest):
    assert manifest["handoff"]["status"] == "COMPLETE"
    assert all(gate["status"] == "PASS" for gate in manifest["phase_gates"])
    assert all(manifest["qa"].values())

release04 = {row["question_id"]: row for row in sba04_manifest["question_release"]}
for qid in ("Q14", "Q27"):
    assert release04[qid]["status"] == "RELEASED"
    assert release04[qid]["routine_id"] == "M2D-SBA-04-R4"
    assert release04[qid]["release_prerequisite_buckets"] == []

# The operational release does not erase pedagogical provenance: R8 remains the explicit cross-bucket bridge.
assert cross["core2_questions"] == ["Q14", "Q27"]
assert migration_audit["release_authorized"] is True
assert migration_audit["block_reasons"] == []
assert all(row["evidence_state"] == "PRESENT" for row in migration_audit["stage_audit"])

print("Core1A SBA05 publication-index, transfer-routine, and SBA04 Q14/Q27 cross-bucket release checks passed.")
