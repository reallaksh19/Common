from __future__ import annotations

import argparse
from copy import deepcopy
from pathlib import Path
from typing import Any

from common import BlueprintError, digest, load_json, load_routing_policy, write_json


DECISIONS = {"CORE1_FIRST", "CORE2_FIRST", "BLOCK_INSUFFICIENT_EVIDENCE", "BLOCK_CONFLICT"}


def _decide(metrics: dict[str, int], policy: dict[str, Any]) -> tuple[str, list[str]]:
    t = policy["thresholds"]
    if metrics["CI"] >= t["material_conflict_min"]:
        return "BLOCK_CONFLICT", ["MATERIAL_CONFLICT"]
    if metrics["UA"] >= t["high_uncertainty_min"]:
        return "BLOCK_INSUFFICIENT_EVIDENCE", ["HIGH_UNCERTAINTY"]
    if metrics["SA"] >= t["strong_scope_min"] and metrics["SS"] >= t["strong_semantic_source_min"]:
        return "CORE1_FIRST", ["STRONG_SCOPE_AUTHORITY", "STRONG_SEMANTIC_SOURCE"]
    if (
        metrics["QE"] >= t["rich_question_evidence_min"]
        and metrics["QR"] >= t["resolved_questions_min"]
        and (metrics["SA"] <= t["coarse_semantic_max"] or metrics["SS"] <= t["coarse_semantic_max"])
    ):
        return "CORE2_FIRST", ["RICH_RESOLVED_QUESTION_EVIDENCE", "SEMANTIC_AUTHORITY_WEAK_OR_COARSE"]
    if metrics["QE"] >= t["rich_question_evidence_min"] and metrics["QR"] >= t["resolved_questions_min"]:
        return "CORE2_FIRST", ["RICH_RESOLVED_QUESTION_EVIDENCE_FALLBACK"]
    return "BLOCK_INSUFFICIENT_EVIDENCE", ["INSUFFICIENT_ROUTING_EVIDENCE"]


def route_evidence(
    ground_truth: dict[str, Any],
    routing_input: dict[str, Any],
    policy: dict[str, Any] | None = None,
) -> dict[str, Any]:
    policy = policy or load_routing_policy()
    manifest_id = ground_truth.get("manifest_id")
    if routing_input.get("ground_truth_manifest_id") != manifest_id:
        raise BlueprintError("ROUTING_GROUND_TRUTH_BINDING_MISMATCH", str(manifest_id))

    subtopics = list(routing_input.get("subtopic_refs") or [])
    if not 1 <= len(subtopics) <= 3 or len(set(subtopics)) != len(subtopics):
        raise BlueprintError("HANDOFF_SUBTOPIC_BOUND_INVALID", repr(subtopics))

    metrics = deepcopy(routing_input.get("metrics") or {})
    if set(metrics) != {"SA", "SS", "QE", "QR", "UA", "CI"}:
        raise BlueprintError("ROUTING_METRICS_INCOMPLETE")
    if any(not isinstance(value, int) or not 0 <= value <= 4 for value in metrics.values()):
        raise BlueprintError("ROUTING_METRIC_OUT_OF_RANGE")

    decision, reason_codes = _decide(metrics, policy)
    if decision not in DECISIONS:
        raise BlueprintError("ROUTING_POLICY_RETURNED_UNKNOWN_DECISION", decision)

    unresolved = list(routing_input.get("unresolved") or [])
    if decision == "BLOCK_CONFLICT" and "MATERIAL_CONFLICT" not in unresolved:
        unresolved.append("MATERIAL_CONFLICT")
    if decision == "BLOCK_INSUFFICIENT_EVIDENCE" and not unresolved:
        unresolved.append("INSUFFICIENT_EVIDENCE_FOR_SAFE_FIRST_ROLE_SELECTION")

    confidence = "HIGH" if metrics["UA"] <= 1 and metrics["CI"] <= 1 and not decision.startswith("BLOCK") else "MEDIUM"
    if metrics["UA"] >= 3 or metrics["CI"] >= 3:
        confidence = "LOW"

    packet = {
        "packet_id": f"R-{routing_input['routing_request_id']}",
        "packet_type": "R",
        "schema_version": "1.0.0",
        "scope": {
            "subject": ground_truth["subject"],
            "grade": ground_truth["grade"],
            "topic_id": ground_truth["topic_id"],
            "subtopic_refs": subtopics
        },
        "provenance": {"ground_truth_refs": [manifest_id]},
        "dependencies": [],
        "confidence": {"level": confidence, "rationale": "; ".join(reason_codes)},
        "validation": {"status": "VALIDATED", "validator_refs": [policy["policy_id"]]},
        "unresolved": unresolved,
        "created_by": {"role": "CORE0", "instance_id": "CORE0-EVIDENCE-ROUTER-v0"},
        "system_decision": decision,
        "final_decision": decision,
        "reason_codes": reason_codes,
        "metrics": metrics,
        "evidence_notes": list(routing_input.get("evidence_notes") or []),
        "owner_override_ref": None,
        "execution_blocked": decision.startswith("BLOCK")
    }
    packet["digest"] = digest(packet)
    return packet


def main() -> int:
    parser = argparse.ArgumentParser(description="Route a Learning Blueprint bundle from evidence state")
    parser.add_argument("--ground-truth", required=True)
    parser.add_argument("--routing-input", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    packet = route_evidence(load_json(args.ground_truth), load_json(args.routing_input))
    write_json(Path(args.out), packet)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
