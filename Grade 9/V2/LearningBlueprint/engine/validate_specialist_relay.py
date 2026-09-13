from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from common import BlueprintError, digest, load_json, write_json
from freeze_specialist_pass import freeze_specialist_pass


COMPARATIVE_STATUSES = {"CONFIRMED", "REFINED", "CONTRADICTED", "OUT_OF_SCOPE"}


def validate_specialist_relay(
    first_pass: dict[str, Any],
    second_pass: dict[str, Any],
    validation: dict[str, Any],
) -> dict[str, Any]:
    first_receipt = freeze_specialist_pass(first_pass)
    second_receipt = freeze_specialist_pass(second_pass)

    if first_pass.get("sequence_role") != "FIRST_SPECIALIST" or second_pass.get("sequence_role") != "SECOND_SPECIALIST":
        raise BlueprintError("SPECIALIST_SEQUENCE_ROLE_INVALID")
    if first_pass.get("role") == second_pass.get("role"):
        raise BlueprintError("SPECIALIST_ROLES_NOT_COMPLEMENTARY")
    if first_pass.get("instance_id") == second_pass.get("instance_id"):
        raise BlueprintError("SPECIALIST_INSTANCE_REUSED", first_pass.get("instance_id", ""))
    if first_pass.get("ground_truth_manifest_id") != second_pass.get("ground_truth_manifest_id"):
        raise BlueprintError("SPECIALIST_GROUND_TRUTH_BINDING_MISMATCH")
    if first_pass.get("ground_truth_manifest_digest") != second_pass.get("ground_truth_manifest_digest"):
        raise BlueprintError("SPECIALIST_GROUND_TRUTH_BINDING_MISMATCH")
    if list(first_pass.get("subtopic_refs") or []) != list(second_pass.get("subtopic_refs") or []):
        raise BlueprintError("SPECIALIST_SUBTOPIC_SCOPE_MISMATCH")

    if validation.get("packet_type") != "V":
        raise BlueprintError("VALIDATION_PACKET_TYPE_INVALID")
    if validation.get("first_pass_id") != first_pass.get("pass_id") or validation.get("second_pass_id") != second_pass.get("pass_id"):
        raise BlueprintError("VALIDATION_PASS_BINDING_MISMATCH")
    if validation.get("first_role") != first_pass.get("role") or validation.get("second_role") != second_pass.get("role"):
        raise BlueprintError("VALIDATION_ROLE_BINDING_MISMATCH")
    if validation.get("first_pass_freeze_digest") != first_receipt["freeze_digest"]:
        raise BlueprintError("VALIDATION_FREEZE_DIGEST_MISMATCH", "first")
    if validation.get("second_pass_freeze_digest") != second_receipt["freeze_digest"]:
        raise BlueprintError("VALIDATION_FREEZE_DIGEST_MISMATCH", "second")
    if validation.get("reveal_after_second_freeze") is not True:
        raise BlueprintError("VALIDATION_REVEAL_BEFORE_SECOND_FREEZE")

    first_claims = {row["claim_id"]: row for row in first_pass["claims"]}
    second_claims = {row["claim_id"]: row for row in second_pass["claims"]}
    comparisons = list(validation.get("comparisons") or [])
    by_upstream: dict[str, list[dict[str, Any]]] = {}
    material_conflicts: list[str] = []

    for row in comparisons:
        upstream_id = row.get("upstream_claim_id")
        if upstream_id not in first_claims:
            raise BlueprintError("VALIDATION_REFERENCES_UNKNOWN_CLAIM", str(upstream_id))
        by_upstream.setdefault(str(upstream_id), []).append(row)
        validator_refs = list(row.get("validator_claim_refs") or [])
        for claim_id in validator_refs:
            if claim_id not in second_claims:
                raise BlueprintError("VALIDATION_REFERENCES_UNKNOWN_CLAIM", str(claim_id))
        if row.get("status") in COMPARATIVE_STATUSES:
            if not validator_refs:
                raise BlueprintError("VALIDATION_COMPARATIVE_STATUS_WITHOUT_SECOND_CLAIM", str(upstream_id))
            upstream_caps = set(first_claims[upstream_id].get("capability_refs") or [])
            downstream_caps: set[str] = set()
            for claim_id in validator_refs:
                downstream_caps.update(second_claims[claim_id].get("capability_refs") or [])
            if not upstream_caps.intersection(downstream_caps):
                raise BlueprintError("VALIDATION_CAPABILITY_MISMATCH", str(upstream_id))
        if not row.get("evidence_refs"):
            raise BlueprintError("VALIDATION_EVIDENCE_MISSING", str(upstream_id))
        if row.get("status") == "CONTRADICTED":
            material_conflicts.append(str(upstream_id))

    missing = [claim_id for claim_id in first_claims if claim_id not in by_upstream]
    duplicated = [claim_id for claim_id, rows in by_upstream.items() if len(rows) != 1]
    if missing or duplicated:
        raise BlueprintError(
            "VALIDATION_UPSTREAM_CLAIM_COVERAGE_INCOMPLETE",
            f"missing={missing}; duplicated={duplicated}",
        )

    audit = {
        "validation_packet_ref": validation["packet_id"],
        "first_pass_ref": first_pass["pass_id"],
        "second_pass_ref": second_pass["pass_id"],
        "first_freeze_digest": first_receipt["freeze_digest"],
        "second_freeze_digest": second_receipt["freeze_digest"],
        "validated_upstream_claim_total": len(first_claims),
        "material_conflict_claim_refs": material_conflicts,
        "fresh_instance_verified": True,
        "blind_grounding_verified": True,
        "reveal_after_freeze_verified": True,
        "status": "PASS",
    }
    audit["audit_digest"] = digest(audit)
    return audit


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate blind Core1/Core2 relay and claim-level comparison")
    parser.add_argument("--first-pass", required=True)
    parser.add_argument("--second-pass", required=True)
    parser.add_argument("--validation", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    audit = validate_specialist_relay(load_json(args.first_pass), load_json(args.second_pass), load_json(args.validation))
    write_json(Path(args.out), audit)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
