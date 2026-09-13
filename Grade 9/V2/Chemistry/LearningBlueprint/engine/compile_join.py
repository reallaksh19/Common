from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path
from typing import Any

from common import BlueprintError, digest, load_json, write_json


INVALIDATED_FIRST_STATUSES = {"MISSING", "UNSUPPORTED", "CONTRADICTED", "OUT_OF_SCOPE"}


def _claim_status_map(validation: dict[str, Any]) -> dict[str, str]:
    return {row["upstream_claim_id"]: row["status"] for row in validation.get("comparisons") or []}


def _valid_claims(packet: dict[str, Any], validation: dict[str, Any], first_pass_id: str) -> list[dict[str, Any]]:
    status_map = _claim_status_map(validation) if packet.get("pass_id") == first_pass_id else {}
    out: list[dict[str, Any]] = []
    for claim in packet.get("claims") or []:
        if status_map.get(claim["claim_id"]) in INVALIDATED_FIRST_STATUSES:
            continue
        out.append(claim)
    return out


def compile_join(
    first_pass: dict[str, Any],
    second_pass: dict[str, Any],
    validation: dict[str, Any],
) -> dict[str, Any]:
    packets = {first_pass.get("packet_type"): first_pass, second_pass.get("packet_type"): second_pass}
    if set(packets) != {"K", "D"}:
        raise BlueprintError("JOIN_REQUIRES_ONE_K_AND_ONE_D_PACKET")
    semantic = packets["K"]
    assessment = packets["D"]

    comparison_statuses = [row.get("status") for row in validation.get("comparisons") or []]
    has_conflict = "CONTRADICTED" in comparison_statuses

    valid_k = _valid_claims(semantic, validation, validation.get("first_pass_id", ""))
    valid_d = _valid_claims(assessment, validation, validation.get("first_pass_id", ""))

    k_by_cap: dict[str, list[str]] = defaultdict(list)
    for claim in valid_k:
        for cap in claim.get("capability_refs") or []:
            k_by_cap[str(cap)].append(claim["claim_id"])

    d_required_by_cap: dict[str, list[str]] = defaultdict(list)
    d_any_by_cap: dict[str, list[str]] = defaultdict(list)
    for claim in valid_d:
        for cap in claim.get("capability_refs") or []:
            d_any_by_cap[str(cap)].append(claim["claim_id"])
            if claim.get("required_for_assessment"):
                d_required_by_cap[str(cap)].append(claim["claim_id"])

    obligations: list[dict[str, Any]] = []
    missing_support: list[dict[str, Any]] = []
    for index, cap in enumerate(sorted(d_required_by_cap), start=1):
        if k_by_cap.get(cap):
            obligations.append({
                "obligation_id": f"OBL-{index:03d}",
                "capability_ref": cap,
                "semantic_claim_refs": sorted(set(k_by_cap[cap])),
                "assessment_claim_refs": sorted(set(d_required_by_cap[cap])),
                "state": "SEMANTIC_AND_ASSESSMENT_ALIGNED",
            })
        else:
            missing_support.append({
                "capability_ref": cap,
                "assessment_claim_refs": sorted(set(d_required_by_cap[cap])),
            })

    semantic_without_assessment: list[dict[str, Any]] = []
    for cap in sorted(k_by_cap):
        if cap not in d_required_by_cap:
            semantic_without_assessment.append({
                "capability_ref": cap,
                "semantic_claim_refs": sorted(set(k_by_cap[cap])),
                "interpretation": "NO_ASSESSMENT_DEMAND_EVIDENCE_DOES_NOT_IMPLY_LOW_IMPORTANCE",
            })

    unresolved = list(validation.get("unresolved") or [])
    if has_conflict:
        join_state = "BLOCK_CONFLICT"
        if "MATERIAL_CORE1_CORE2_CONFLICT" not in unresolved:
            unresolved.append("MATERIAL_CORE1_CORE2_CONFLICT")
    elif missing_support:
        join_state = "BLOCK_MISSING_SEMANTIC_SUPPORT"
        for row in missing_support:
            issue = f"MISSING_SEMANTIC_SUPPORT:{row['capability_ref']}"
            if issue not in unresolved:
                unresolved.append(issue)
    else:
        join_state = "READY_FOR_LEARNER_STATE"

    packet = {
        "packet_id": f"J-{semantic['packet_id']}-{assessment['packet_id']}",
        "packet_type": "J",
        "ground_truth_manifest_id": semantic["ground_truth_manifest_id"],
        "semantic_packet_ref": semantic["packet_id"],
        "assessment_packet_ref": assessment["packet_id"],
        "validation_packet_ref": validation["packet_id"],
        "join_state": join_state,
        "obligations": obligations,
        "assessment_without_semantic_support": missing_support,
        "semantic_without_assessment_evidence": semantic_without_assessment,
        "unresolved": unresolved,
    }
    packet["digest"] = digest(packet)
    return packet


def main() -> int:
    parser = argparse.ArgumentParser(description="Compile Core1 x Core2 join obligations")
    parser.add_argument("--first-pass", required=True)
    parser.add_argument("--second-pass", required=True)
    parser.add_argument("--validation", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    packet = compile_join(load_json(args.first_pass), load_json(args.second_pass), load_json(args.validation))
    write_json(Path(args.out), packet)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
