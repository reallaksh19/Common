#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))

from build_physics_engineering_gate_registry_v3 import build_registry  # noqa: E402
from validate_engineering_gates_v3 import validate as validate_v3_registry  # noqa: E402
from validate_engineering_mapping_review import MappingReviewError, validate as validate_mapping_review  # noqa: E402


class DiscoveryCatalogError(Exception):
    def __init__(self, code: str, message: str):
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message


def fail(code: str, message: str) -> None:
    raise DiscoveryCatalogError(code, message)


def load(rel: str) -> dict:
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def validate(catalog: dict) -> dict:
    schema = load("contracts/physics-engineering-discovery-catalog.schema.json")
    try:
        jsonschema.validate(catalog, schema)
    except jsonschema.ValidationError as exc:
        fail("E_ENG_DISCOVERY_SCHEMA", exc.message)

    source = catalog["source_snapshot"]
    if len(catalog["discovered_subtopics"]) != source["declared_subtopic_count"]:
        fail("E_ENG_DISCOVERY_COUNT_MISMATCH", f"declared {source['declared_subtopic_count']} subtopics but catalog has {len(catalog['discovered_subtopics'])}")

    registry = build_registry()
    validate_v3_registry(registry)
    current_ids = {gate["subtopic_id"] for gate in registry["gates"]}

    entries = catalog["discovered_subtopics"]
    discovery_ids = [entry["discovery_gate_id"] for entry in entries]
    if len(set(discovery_ids)) != len(discovery_ids):
        fail("E_ENG_DISCOVERY_DUPLICATE_ID", "duplicate discovery_gate_id")

    exact_targets: set[str] = set()
    mapped_targets: set[str] = set()
    migration_required = 0

    for entry in entries:
        discovery_id = entry["discovery_gate_id"]
        disposition = entry["disposition"]
        targets = entry["v3_gate_ids"]
        review_ref = entry.get("mapping_review_ref")

        if disposition == "EXACT_V3_ID":
            if review_ref is not None:
                fail("E_ENG_DISCOVERY_MAPPING_REVIEW_UNEXPECTED", discovery_id)
            if targets != [discovery_id]:
                fail("E_ENG_DISCOVERY_EXACT_ID_MISMATCH", f"{discovery_id} exact disposition must bind only itself")
            if discovery_id not in current_ids:
                fail("E_ENG_DISCOVERY_EXACT_ID_MISSING", f"{discovery_id} is marked exact but is absent from canonical v3")
            exact_targets.add(discovery_id)
        elif disposition == "MAPPED_V3":
            missing = sorted(set(targets) - current_ids)
            if missing:
                fail("E_ENG_DISCOVERY_MAPPING_TARGET_MISSING", f"{discovery_id} maps to unknown v3 gates {missing}")
            try:
                review = load(review_ref)
                review_result = validate_mapping_review(
                    review,
                    expected_discovery_id=discovery_id,
                    expected_targets=targets,
                )
            except (FileNotFoundError, json.JSONDecodeError, MappingReviewError) as exc:
                fail("E_ENG_DISCOVERY_MAPPING_REVIEW_INVALID", f"{discovery_id}: {exc}")
            if review_result["decision"] != "APPROVED":
                fail("E_ENG_DISCOVERY_MAPPING_REVIEW_NOT_APPROVED", discovery_id)
            mapped_targets.update(targets)
        elif disposition == "MIGRATION_REQUIRED":
            if review_ref is not None:
                fail("E_ENG_DISCOVERY_MAPPING_REVIEW_UNEXPECTED", discovery_id)
            migration_required += 1
            if discovery_id in current_ids:
                fail("E_ENG_DISCOVERY_STALE_MIGRATION_HOLD", f"{discovery_id} now exists in v3 and must be reconciled explicitly")
        else:
            fail("E_ENG_DISCOVERY_UNKNOWN_DISPOSITION", disposition)

    native = set(catalog["v3_native_or_refined_gate_ids"])
    unknown_native = sorted(native - current_ids)
    if unknown_native:
        fail("E_ENG_DISCOVERY_NATIVE_GATE_MISSING", f"native/refined list contains unknown v3 gates {unknown_native}")

    covered_current = exact_targets | mapped_targets | native
    missing_current = sorted(current_ids - covered_current)
    if missing_current:
        fail("E_ENG_DISCOVERY_V3_UNRECONCILED", f"canonical v3 gates are absent from discovery reconciliation {missing_current}")

    # Exact source identity and broader reviewed source mappings are independent
    # provenance roles and may legitimately converge on the same canonical gate.
    # Native/refined means there is no source-backed reconciliation role, so it
    # remains strictly disjoint from both exact and mapped target sets.
    overlap = (exact_targets | mapped_targets) & native
    if overlap:
        fail("E_ENG_DISCOVERY_DOUBLE_CLASSIFIED", f"native/refined v3 gates are also source-backed {sorted(overlap)}")

    return {
        "status": "PASS",
        "catalog_id": catalog["catalog_id"],
        "discovered_subtopic_count": len(entries),
        "exact_v3_count": len(exact_targets),
        "mapped_v3_target_count": len(mapped_targets),
        "migration_required_count": migration_required,
        "v3_native_or_refined_count": len(native),
        "canonical_v3_gate_count": len(current_ids),
        "case_artifacts_role": catalog["stress_test_policy"]["case_artifacts_role"],
        "readiness_rule": catalog["control_plane"]["readiness_rule"]
    }


def main() -> None:
    rel = sys.argv[1] if len(sys.argv) > 1 else "policy/physics-engineering-discovery-catalog.pr383.v1.json"
    print(json.dumps(validate(load(rel)), indent=2))


if __name__ == "__main__":
    main()
