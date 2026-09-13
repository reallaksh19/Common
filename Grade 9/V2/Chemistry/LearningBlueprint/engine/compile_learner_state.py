from __future__ import annotations

from typing import Any

from common import BlueprintError, digest, load_assimilation_policy


def compile_learner_state(join: dict[str, Any], learner_input: dict[str, Any], policy: dict[str, Any] | None = None) -> dict[str, Any]:
    policy = policy or load_assimilation_policy()
    if join.get("join_state") != "READY_FOR_LEARNER_STATE":
        raise BlueprintError("ASSIMILATION_JOIN_NOT_READY", str(join.get("join_state")))

    prior = learner_input.get("readiness_prior")
    if str(prior) not in policy["readiness_profiles"]:
        raise BlueprintError("LEARNER_READINESS_PRIOR_UNSUPPORTED", str(prior))

    obligation_caps = [row["capability_ref"] for row in join.get("obligations", [])]
    if len(set(obligation_caps)) != len(obligation_caps):
        raise BlueprintError("JOIN_DUPLICATE_CAPABILITY_OBLIGATION")

    evidence_rows = learner_input.get("capability_evidence") or []
    evidence_by_cap: dict[str, dict[str, Any]] = {}
    for row in evidence_rows:
        cap = row.get("capability_ref")
        if cap in evidence_by_cap:
            raise BlueprintError("LEARNER_CAPABILITY_EVIDENCE_DUPLICATE", str(cap))
        if row.get("state") not in policy["learner_states"]:
            raise BlueprintError("LEARNER_CAPABILITY_STATE_INVALID", str(row.get("state")))
        if not row.get("evidence_refs"):
            raise BlueprintError("LEARNER_CAPABILITY_EVIDENCE_REF_MISSING", str(cap))
        evidence_by_cap[cap] = row

    profile = policy["readiness_profiles"][str(prior)]
    states = []
    for cap in obligation_caps:
        evidence = evidence_by_cap.get(cap)
        if evidence:
            state = evidence["state"]
            origin = "CAPABILITY_EVIDENCE"
            refs = list(evidence["evidence_refs"])
        else:
            state = "UNKNOWN"
            origin = "READINESS_PRIOR_ONLY_NO_CAPABILITY_EVIDENCE"
            refs = []
        states.append({
            "capability_ref": cap,
            "state": state,
            "origin": origin,
            "evidence_refs": refs,
            "bridge_required_by_profile": state in profile["require_bridge_for_states"]
        })

    packet = {
        "packet_id": f"LS-{learner_input['learner_state_request_id']}",
        "packet_type": "LS",
        "join_packet_ref": join["packet_id"],
        "join_digest": join["digest"],
        "readiness_prior": prior,
        "prior_interpretation": "PRIOR_ONLY_NOT_DIAGNOSIS",
        "scaffold_depth": profile["scaffold_depth"],
        "secure_compression_span": profile["secure_compression_span"],
        "capabilities": states,
        "unresolved": [row["capability_ref"] for row in states if row["state"] == "UNKNOWN"]
    }
    packet["digest"] = digest(packet)
    return packet
