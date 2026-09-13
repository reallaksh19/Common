from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from common import BlueprintError, digest, load_json, write_json


ROLE_PACKET = {"CORE1": "K", "CORE2": "D"}
ROLE_DOMAIN = {"CORE1": "SEMANTIC", "CORE2": "ASSESSMENT"}


def freeze_specialist_pass(packet: dict[str, Any]) -> dict[str, Any]:
    role = packet.get("role")
    if role not in ROLE_PACKET:
        raise BlueprintError("SPECIALIST_ROLE_INVALID", repr(role))
    if packet.get("packet_type") != ROLE_PACKET[role]:
        raise BlueprintError("SPECIALIST_ROLE_PACKET_TYPE_MISMATCH", f"{role} -> {packet.get('packet_type')}")
    if packet.get("grounding_phase") != "BLIND_GROUNDING" or packet.get("access_state") != "ORIGINAL_EVIDENCE_ONLY":
        raise BlueprintError("SPECIALIST_BLIND_PASS_HAS_UPSTREAM_ACCESS", packet.get("pass_id", ""))
    if packet.get("upstream_packet_refs"):
        raise BlueprintError("SPECIALIST_BLIND_PASS_HAS_UPSTREAM_ACCESS", packet.get("pass_id", ""))
    if packet.get("sequence_role") not in {"FIRST_SPECIALIST", "SECOND_SPECIALIST"}:
        raise BlueprintError("SPECIALIST_SEQUENCE_ROLE_INVALID", repr(packet.get("sequence_role")))

    claims = list(packet.get("claims") or [])
    if not claims:
        raise BlueprintError("SPECIALIST_PASS_HAS_NO_CLAIMS", packet.get("pass_id", ""))
    ids = [str(row.get("claim_id")) for row in claims]
    if len(ids) != len(set(ids)):
        raise BlueprintError("SPECIALIST_CLAIM_ID_DUPLICATED", packet.get("pass_id", ""))
    for row in claims:
        if row.get("claim_domain") != ROLE_DOMAIN[role]:
            raise BlueprintError("SPECIALIST_CLAIM_DOMAIN_MISMATCH", str(row.get("claim_id")))
        if not row.get("capability_refs") or not row.get("evidence_refs"):
            raise BlueprintError("SPECIALIST_CLAIM_GROUNDING_INCOMPLETE", str(row.get("claim_id")))
        if role == "CORE1" and row.get("required_for_assessment"):
            raise BlueprintError("SEMANTIC_CLAIM_CANNOT_ASSERT_ASSESSMENT_REQUIREMENT", str(row.get("claim_id")))

    frozen_digest = digest(packet)
    return {
        "pass_id": packet["pass_id"],
        "packet_id": packet["packet_id"],
        "role": role,
        "instance_id": packet["instance_id"],
        "sequence_role": packet["sequence_role"],
        "access_state": packet["access_state"],
        "claim_ids": ids,
        "freeze_digest": frozen_digest,
        "frozen_before_reveal": True,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Freeze a blind-grounded Core1/Core2 specialist pass")
    parser.add_argument("--pass-packet", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    write_json(Path(args.out), freeze_specialist_pass(load_json(args.pass_packet)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
