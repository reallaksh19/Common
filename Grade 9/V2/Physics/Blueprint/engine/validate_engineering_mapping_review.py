#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))

from build_physics_engineering_gate_registry_v3 import GATE_FILES, build_registry  # noqa: E402
from validate_engineering_gates_v3 import validate as validate_v3_registry  # noqa: E402

SCHEMA_REL = "contracts/physics-engineering-discovery-mapping-review.schema.json"
MANIFEST_REL = "provenance/pr383/source-snapshot.manifest.json"
SOURCE_OBLIGATION_FIELDS = [
    "prerequisite_ids",
    "technical_core",
    "mandatory_equations",
    "representations",
    "model_conditions",
    "reasoning_sequence",
    "required_transformations",
    "misconceptions",
    "mandatory_verifications",
    "problem_families",
    "falsification_cases",
]
ALLOWED_TARGET_ROOTS = {
    "prerequisites",
    "required_invariants",
    "concepts",
    "relations",
    "model_conditions",
    "representations",
    "reasoning_sequence",
    "required_transformations",
    "misconceptions",
    "verifications",
    "problem_families",
    "falsification_cases",
}


class MappingReviewError(Exception):
    def __init__(self, code: str, message: str):
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message


def fail(code: str, message: str) -> None:
    raise MappingReviewError(code, message)


def load(rel: str) -> dict:
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def git_blob_sha(path: Path) -> str:
    raw = path.read_bytes()
    framed = f"blob {len(raw)}\0".encode("ascii") + raw
    return hashlib.sha1(framed).hexdigest()


def pointer_get(doc: object, pointer: str) -> object:
    if not pointer.startswith("/"):
        fail("E_ENG_MAPPING_POINTER_INVALID", pointer)
    current = doc
    for raw_part in pointer.split("/")[1:]:
        part = raw_part.replace("~1", "/").replace("~0", "~")
        try:
            if isinstance(current, list):
                current = current[int(part)]
            elif isinstance(current, dict):
                current = current[part]
            else:
                raise KeyError(part)
        except (KeyError, IndexError, ValueError, TypeError):
            fail("E_ENG_MAPPING_POINTER_INVALID", pointer)
    return current


def source_obligation_pointers(source_gate: dict) -> list[str]:
    pointers: list[str] = []
    for field in SOURCE_OBLIGATION_FIELDS:
        values = source_gate.get(field, [])
        if not isinstance(values, list):
            fail("E_ENG_MAPPING_SOURCE_SHAPE", f"{field} is not an array")
        pointers.extend(f"/{field}/{idx}" for idx in range(len(values)))
    return pointers


def _validate_source_snapshot(review: dict) -> dict:
    manifest = load(MANIFEST_REL)
    source = review["source_snapshot"]
    if source["registry_ref"] != manifest["local"]["registry_ref"]:
        fail("E_ENG_MAPPING_SOURCE_REF_MISMATCH", source["registry_ref"])
    if source["registry_git_blob_sha"] != manifest["source"]["registry_git_blob_sha"]:
        fail("E_ENG_MAPPING_SOURCE_SHA_MISMATCH", source["registry_git_blob_sha"])

    registry_path = ROOT / source["registry_ref"]
    actual = git_blob_sha(registry_path)
    if actual != source["registry_git_blob_sha"]:
        fail("E_ENG_MAPPING_SOURCE_BLOB_DRIFT", f"expected {source['registry_git_blob_sha']} got {actual}")

    registry = load(source["registry_ref"])
    source_schema = load(manifest["local"]["schema_ref"])
    try:
        jsonschema.validate(registry, source_schema)
    except jsonschema.ValidationError as exc:
        fail("E_ENG_MAPPING_SOURCE_SCHEMA", exc.message)

    rows = [g for g in registry["subtopic_gates"] if g["subtopic_id"] == source["discovery_gate_id"]]
    if len(rows) != 1:
        fail("E_ENG_MAPPING_SOURCE_GATE_MISSING", source["discovery_gate_id"])
    return rows[0]


def _validate_targets(review: dict) -> tuple[dict[str, dict], list[str]]:
    registry = build_registry()
    validate_v3_registry(registry)
    current = {g["subtopic_id"]: g for g in registry["gates"]}
    target_docs: dict[str, dict] = {}
    ordered_ids: list[str] = []

    for snapshot in review["target_snapshot"]:
        gid = snapshot["gate_id"]
        if gid in target_docs:
            fail("E_ENG_MAPPING_DUPLICATE_TARGET", gid)
        if gid not in current:
            fail("E_ENG_MAPPING_TARGET_MISSING", gid)
        if snapshot["gate_ref"] not in GATE_FILES:
            fail("E_ENG_MAPPING_TARGET_REF_NOT_CANONICAL", snapshot["gate_ref"])
        path = ROOT / snapshot["gate_ref"]
        actual_sha = git_blob_sha(path)
        if actual_sha != snapshot["gate_git_blob_sha"]:
            fail("E_ENG_MAPPING_TARGET_BLOB_DRIFT", f"{gid}: expected {snapshot['gate_git_blob_sha']} got {actual_sha}")
        doc = load(snapshot["gate_ref"])
        if doc.get("subtopic_id") != gid:
            fail("E_ENG_MAPPING_TARGET_ID_MISMATCH", gid)
        if doc != current[gid]:
            fail("E_ENG_MAPPING_TARGET_REGISTRY_DRIFT", gid)
        target_docs[gid] = doc
        ordered_ids.append(gid)
    return target_docs, ordered_ids


def validate(review: dict, *, expected_discovery_id: str | None = None, expected_targets: list[str] | None = None) -> dict:
    try:
        jsonschema.validate(review, load(SCHEMA_REL))
    except jsonschema.ValidationError as exc:
        fail("E_ENG_MAPPING_REVIEW_SCHEMA", exc.message)

    source_gate = _validate_source_snapshot(review)
    discovery_id = review["source_snapshot"]["discovery_gate_id"]
    if expected_discovery_id is not None and discovery_id != expected_discovery_id:
        fail("E_ENG_MAPPING_DISCOVERY_ID_MISMATCH", f"expected {expected_discovery_id} got {discovery_id}")

    target_docs, target_ids = _validate_targets(review)
    if expected_targets is not None and target_ids != expected_targets:
        fail("E_ENG_MAPPING_TARGET_SET_MISMATCH", f"expected {expected_targets} got {target_ids}")

    required_pointers = source_obligation_pointers(source_gate)
    coverage = review["coverage"]
    coverage_pointers = [row["source_pointer"] for row in coverage]
    if len(set(coverage_pointers)) != len(coverage_pointers):
        fail("E_ENG_MAPPING_DUPLICATE_SOURCE_POINTER", "duplicate source_pointer")
    if set(coverage_pointers) != set(required_pointers):
        missing = sorted(set(required_pointers) - set(coverage_pointers))
        extra = sorted(set(coverage_pointers) - set(required_pointers))
        fail("E_ENG_MAPPING_SOURCE_COVERAGE_MISMATCH", f"missing={missing} extra={extra}")

    for row in coverage:
        pointer_get(source_gate, row["source_pointer"])
        for target_ref in row["target_refs"]:
            gid = target_ref["gate_id"]
            if gid not in target_docs:
                fail("E_ENG_MAPPING_COVERAGE_TARGET_OUTSIDE_REVIEW", gid)
            root = target_ref["target_pointer"].split("/")[1]
            if root not in ALLOWED_TARGET_ROOTS:
                fail("E_ENG_MAPPING_TARGET_POINTER_SCOPE", target_ref["target_pointer"])
            pointer_get(target_docs[gid], target_ref["target_pointer"])

    uncovered = sorted(row["source_pointer"] for row in coverage if row["status"] == "UNCOVERED")
    declared_uncovered = sorted(review["decision"]["uncovered_source_pointers"])
    if uncovered != declared_uncovered:
        fail("E_ENG_MAPPING_UNCOVERED_LIST_MISMATCH", f"derived={uncovered} declared={declared_uncovered}")

    decision = review["decision"]["status"]
    if decision == "APPROVED" and uncovered:
        fail("E_ENG_MAPPING_APPROVAL_HAS_GAPS", str(uncovered))
    if decision == "BLOCKED" and not uncovered:
        fail("E_ENG_MAPPING_BLOCKED_WITHOUT_GAP", "blocked review must identify at least one uncovered source obligation")

    return {
        "status": "PASS",
        "review_id": review["review_id"],
        "decision": decision,
        "discovery_gate_id": discovery_id,
        "target_gate_ids": target_ids,
        "source_obligation_count": len(required_pointers),
        "covered_obligation_count": len(required_pointers) - len(uncovered),
        "uncovered_obligation_count": len(uncovered),
        "readiness_authorized": False,
        "source_custody_promoted": False,
    }


def main() -> None:
    rel = sys.argv[1] if len(sys.argv) > 1 else "provenance/pr383/mapping-reviews/PHY-GRAV-UNIVERSAL-LAW.v1.json"
    print(json.dumps(validate(load(rel)), indent=2))


if __name__ == "__main__":
    main()
