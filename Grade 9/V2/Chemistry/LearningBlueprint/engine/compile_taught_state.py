from __future__ import annotations

from typing import Any

from common import BlueprintError, digest

FLAGS = ["taught", "represented", "worked", "faded", "independent", "checked"]


def compile_taught_state(assimilation: dict[str, Any], realization: dict[str, Any]) -> dict[str, Any]:
    if assimilation.get("validation_status") != "PASS" or not assimilation.get("manuscript_ready"):
        raise BlueprintError("TAUGHT_STATE_ASSIMILATION_NOT_READY")
    treatments = {r["capability_ref"]: r for r in assimilation.get("capability_treatments", [])}
    rows = realization.get("capabilities") or []
    if {r.get("capability_ref") for r in rows} != set(treatments):
        raise BlueprintError("TAUGHT_STATE_CAPABILITY_COVERAGE_MISMATCH")

    receipts = []
    for row in rows:
        cap = row["capability_ref"]
        evidence = row.get("evidence_refs") or {}
        for flag in FLAGS:
            value = row.get(flag)
            if not isinstance(value, bool):
                raise BlueprintError("TAUGHT_STATE_FLAG_INVALID", f"{cap}:{flag}")
            if value and not evidence.get(flag):
                raise BlueprintError("TAUGHT_STATE_POSITIVE_WITHOUT_EVIDENCE", f"{cap}:{flag}")
        if row.get("independent") and not row.get("checked"):
            raise BlueprintError("TAUGHT_STATE_INDEPENDENT_WITHOUT_CHECK", cap)
        if row.get("checked") and not row.get("independent"):
            raise BlueprintError("TAUGHT_STATE_CHECK_WITHOUT_INDEPENDENT", cap)
        receipts.append({"capability_ref": cap, **{f: row[f] for f in FLAGS}, "evidence_refs": evidence})

    packet = {
        "packet_id": f"T-{realization['realization_id']}",
        "packet_type": "T",
        "assimilation_packet_ref": assimilation["packet_id"],
        "assimilation_digest": assimilation["digest"],
        "purpose_mode": assimilation["purpose_mode"],
        "capabilities": receipts,
        "release_state": "TAUGHT_STATE_EVIDENCE_RECORDED"
    }
    packet["digest"] = digest(packet)
    return packet
