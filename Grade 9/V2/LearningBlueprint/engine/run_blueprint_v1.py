from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from common import BlueprintError, digest, load_json, write_json
from compile_join import compile_join
from freeze_specialist_pass import freeze_specialist_pass
from validate_specialist_relay import validate_specialist_relay


ROUTE_TO_ROLE = {"CORE1_FIRST": "CORE1", "CORE2_FIRST": "CORE2"}


def run_v1(
    route: dict[str, Any],
    first_pass: dict[str, Any],
    second_pass: dict[str, Any],
    validation: dict[str, Any],
) -> dict[str, Any]:
    if route.get("execution_blocked") or route.get("final_decision") not in ROUTE_TO_ROLE:
        raise BlueprintError("BLUEPRINT_V1_ROUTE_BLOCKED", str(route.get("final_decision")))
    expected_first = ROUTE_TO_ROLE[route["final_decision"]]
    if first_pass.get("role") != expected_first:
        raise BlueprintError(
            "BLUEPRINT_V1_ROUTE_ORDER_MISMATCH",
            f"expected {expected_first}, got {first_pass.get('role')}",
        )
    expected_second = "CORE2" if expected_first == "CORE1" else "CORE1"
    if second_pass.get("role") != expected_second:
        raise BlueprintError(
            "BLUEPRINT_V1_ROUTE_ORDER_MISMATCH",
            f"expected second {expected_second}, got {second_pass.get('role')}",
        )

    first_receipt = freeze_specialist_pass(first_pass)
    second_receipt = freeze_specialist_pass(second_pass)
    relay_audit = validate_specialist_relay(first_pass, second_pass, validation)
    join_packet = compile_join(first_pass, second_pass, validation)

    manifest = {
        "blueprint_stage": "V1_INDEPENDENT_INTELLIGENCE_AND_JOIN",
        "route_packet_ref": route.get("packet_id"),
        "route_digest": route.get("digest"),
        "first_specialist": expected_first,
        "second_specialist": expected_second,
        "first_pass_freeze_digest": first_receipt["freeze_digest"],
        "second_pass_freeze_digest": second_receipt["freeze_digest"],
        "validation_packet_ref": validation["packet_id"],
        "relay_audit_digest": relay_audit["audit_digest"],
        "join_packet_ref": join_packet["packet_id"],
        "join_digest": join_packet["digest"],
        "join_state": join_packet["join_state"],
        "status": "PASS" if join_packet["join_state"] == "READY_FOR_LEARNER_STATE" else "BLOCKED",
    }
    manifest["manifest_digest"] = digest(manifest)
    return {
        "first_freeze_receipt": first_receipt,
        "second_freeze_receipt": second_receipt,
        "relay_audit": relay_audit,
        "join_packet": join_packet,
        "manifest": manifest,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Learning Blueprint v1 independent specialist relay and join")
    parser.add_argument("--route", required=True)
    parser.add_argument("--first-pass", required=True)
    parser.add_argument("--second-pass", required=True)
    parser.add_argument("--validation", required=True)
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()
    result = run_v1(load_json(args.route), load_json(args.first_pass), load_json(args.second_pass), load_json(args.validation))
    out = Path(args.out_dir)
    for name, payload in result.items():
        write_json(out / f"{name}.json", payload)
    return 0 if result["manifest"]["status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
