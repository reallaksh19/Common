from __future__ import annotations

import argparse
from copy import deepcopy
from pathlib import Path
from typing import Any

from common import BlueprintError, digest, load_json, write_json


ROUTE_VALUES = {"CORE1_FIRST", "CORE2_FIRST", "BLOCK_INSUFFICIENT_EVIDENCE", "BLOCK_CONFLICT"}


def apply_owner_override(route_packet: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    if override.get("target_domain") != "ROUTING" or override.get("target_field") != "final_decision":
        raise BlueprintError("V0_OVERRIDE_TARGET_UNSUPPORTED")
    if override.get("target_packet_id") != route_packet.get("packet_id"):
        raise BlueprintError("OVERRIDE_TARGET_PACKET_MISMATCH")
    if override.get("system_value") != route_packet.get("system_decision"):
        raise BlueprintError("OVERRIDE_SYSTEM_FINDING_MISMATCH")
    owner_value = override.get("owner_value")
    if owner_value not in ROUTE_VALUES:
        raise BlueprintError("OWNER_ROUTE_VALUE_INVALID", repr(owner_value))

    result = deepcopy(route_packet)
    blocked = str(route_packet["system_decision"]).startswith("BLOCK")
    applied = True
    if override.get("mode") == "SOFT" and blocked:
        computed_final = route_packet["system_decision"]
        applied = False
        result["unresolved"] = list(result.get("unresolved") or []) + ["SOFT_OVERRIDE_DID_NOT_BYPASS_SYSTEM_BLOCK"]
    else:
        computed_final = owner_value

    if override.get("final_action") != computed_final:
        raise BlueprintError("OVERRIDE_FINAL_ACTION_INCONSISTENT", f"expected {computed_final}")

    result["final_decision"] = computed_final
    result["owner_override_ref"] = override["override_id"]
    result["execution_blocked"] = str(computed_final).startswith("BLOCK")
    result["override_audit"] = {
        "override_id": override["override_id"],
        "mode": override["mode"],
        "system_finding": route_packet["system_decision"],
        "owner_value": owner_value,
        "applied": applied,
        "final_action": computed_final,
        "rationale": override["rationale"]
    }
    result["digest"] = digest({k: v for k, v in result.items() if k != "digest"})
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Apply an owner operational override without erasing the system finding")
    parser.add_argument("--route", required=True)
    parser.add_argument("--override", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    write_json(Path(args.out), apply_owner_override(load_json(args.route), load_json(args.override)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
