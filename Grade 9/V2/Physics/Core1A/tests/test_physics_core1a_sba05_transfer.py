#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
INDEX_SCHEMA = ROOT / "contracts" / "physics-core1a-sba-publication-index.schema.json"
INDEX = ROOT / "registry" / "physics-core1a-motion-in-a-plane-sba-publication-index-v1.json"
SBA_SCHEMA = ROOT / "contracts" / "physics-core1a-subtopic-bucket.schema.json"
SBA05_TRANSFER = ROOT / "registry" / "physics-core1a-motion-in-a-plane-sba05-transfer-v1.json"

index_schema = json.loads(INDEX_SCHEMA.read_text(encoding="utf-8"))
index = json.loads(INDEX.read_text(encoding="utf-8"))
sba_schema = json.loads(SBA_SCHEMA.read_text(encoding="utf-8"))
transfer = json.loads(SBA05_TRANSFER.read_text(encoding="utf-8"))

Draft202012Validator.check_schema(index_schema)
Draft202012Validator(index_schema).validate(index)

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
assert all(row["state"] == "BUILT" for row in index["rows"])

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

print("Core1A SBA05 publication-index and transfer-routine checks passed.")
