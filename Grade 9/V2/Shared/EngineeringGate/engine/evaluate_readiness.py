#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import jsonschema

ROOT = Path(__file__).resolve().parents[1]


class EngineeringGateError(Exception):
    def __init__(self, code: str, message: str):
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_policy() -> dict[str, Any]:
    return _load_json(ROOT / "policy" / "readiness-policy.v1.json")


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical(value)).hexdigest()


def _research_state(request: dict[str, Any], engineering_receipt: dict[str, Any], policy: dict[str, Any]) -> str:
    if request.get("engineering_depth") != policy["research_depth_value"]:
        return "NOT_REQUIRED"
    research_codes = set(policy["research_blocker_codes"])
    return "BLOCKED" if any(row.get("code") in research_codes for row in engineering_receipt.get("blockers", [])) else "READY"


def _source_state(source_item_status: str) -> str:
    states = {
        "SOURCE_READY": "READY",
        "SOURCE_HELD": "HELD",
        "INDEPENDENT_OF_TECHNICAL_GATE": "NOT_APPLICABLE",
    }
    try:
        return states[source_item_status]
    except KeyError as exc:
        raise EngineeringGateError("E_ENG_GATE_SOURCE_STATE_UNKNOWN", source_item_status) from exc


def build_envelope(
    request: dict[str, Any],
    manifest: dict[str, Any],
    engineering_receipt: dict[str, Any],
    domain_receipt: dict[str, Any],
    *,
    policy: dict[str, Any] | None = None,
) -> dict[str, Any]:
    policy = policy or load_policy()

    if request.get("request_id") != manifest.get("request_id"):
        raise EngineeringGateError("E_ENG_GATE_REQUEST_MANIFEST_MISMATCH", "manifest belongs to another request")
    if request.get("request_id") != engineering_receipt.get("request_id"):
        raise EngineeringGateError("E_ENG_GATE_REQUEST_RECEIPT_MISMATCH", "engineering receipt belongs to another request")
    if manifest.get("manifest_id") != engineering_receipt.get("manifest_id"):
        raise EngineeringGateError("E_ENG_GATE_MANIFEST_RECEIPT_MISMATCH", "engineering receipt belongs to another manifest")
    if engineering_receipt.get("manifest_digest") != digest(manifest):
        raise EngineeringGateError("E_ENG_GATE_MANIFEST_DRIFT", "manifest content no longer matches the engineering closure receipt")
    if domain_receipt.get("engineering_receipt_ref") != engineering_receipt.get("receipt_id"):
        raise EngineeringGateError("E_ENG_GATE_DOMAIN_MISMATCH", "domain closure is not bound to the engineering receipt")

    research_codes = set(policy["research_blocker_codes"])
    blockers: list[dict[str, Any]] = []
    for row in engineering_receipt.get("blockers", []):
        blockers.append({
            "code": row["code"],
            "dimension": "RESEARCH_PROVENANCE" if row["code"] in research_codes else "TECHNICAL",
            "ref": row.get("gate_id"),
            "message": row["message"],
        })

    authoritative_status = policy["authoritative_prerequisite_status"]
    for row in domain_receipt.get("prerequisites", []):
        if row.get("status") != authoritative_status:
            blockers.append({
                "code": "E_ENG_EXTERNAL_PREREQUISITE_HELD",
                "dimension": "EXTERNAL_PREREQUISITES",
                "ref": row.get("prerequisite_id"),
                "message": f"{row.get('prerequisite_id')} has no provider-owned authoritative-domain receipt",
            })

    technical_ready = engineering_receipt.get("closure_status") == policy["technical_ready_status"]
    external_ready = domain_receipt.get("closure_status") == policy["domain_ready_status"]
    consumable = technical_ready and external_ready
    reason_codes = sorted({row["code"] for row in blockers})

    declared_consumers = manifest.get("downstream_consumers", [])
    if len(declared_consumers) != len(set(declared_consumers)):
        raise EngineeringGateError("E_ENG_GATE_DUPLICATE_CONSUMER", "manifest downstream_consumers must be unique")

    permissions: dict[str, dict[str, Any]] = {}
    non_authorizing = policy["non_authorizing_consumers"]
    for consumer in declared_consumers:
        if consumer in non_authorizing:
            permissions[consumer] = {
                "status": "NOT_AUTHORIZED",
                "reason_codes": [non_authorizing[consumer]],
            }
        else:
            permissions[consumer] = {
                "status": "ALLOWED" if consumable else "BLOCKED",
                "reason_codes": [] if consumable else reason_codes,
            }

    if consumable:
        next_action = "Declared technical consumers may proceed; non-engineering authorities remain independently governed."
    elif blockers:
        next_action = blockers[0]["message"]
    else:
        next_action = "Resolve Engineering Gate readiness blockers and recompile."

    envelope: dict[str, Any] = {
        "schema_version": "1.0.0",
        "policy_id": policy["policy_id"],
        "authority_layer": policy["authority_layer"],
        "envelope_id": engineering_receipt["receipt_id"].replace("ENG-CLOSURE-", "ENG-READY-", 1),
        "request_id": request["request_id"],
        "manifest_id": manifest["manifest_id"],
        "engineering_receipt": {
            "receipt_id": engineering_receipt["receipt_id"],
            "manifest_digest": engineering_receipt["manifest_digest"],
            "closure_digest": engineering_receipt["closure_digest"],
            "closure_status": engineering_receipt["closure_status"],
            "source_item_status": engineering_receipt["source_item_status"],
        },
        "domain_receipt": {
            "receipt_id": domain_receipt["receipt_id"],
            "closure_digest": domain_receipt["closure_digest"],
            "closure_status": domain_receipt["closure_status"],
            "prerequisite_count": len(domain_receipt.get("prerequisites", [])),
            "held_count": sum(1 for row in domain_receipt.get("prerequisites", []) if row.get("status") != authoritative_status),
        },
        "dimensions": {
            "technical": "READY" if technical_ready else "BLOCKED",
            "research_provenance": _research_state(request, engineering_receipt, policy),
            "external_prerequisites": "READY" if external_ready else "HELD",
            "source_authority": _source_state(engineering_receipt["source_item_status"]),
        },
        "consumer_permissions": permissions,
        "overall_state": policy["ready_state"] if consumable else policy["blocked_state"],
        "publication_authorization": "NOT_IMPLIED",
        "blockers": blockers,
        "next_action": next_action,
        "envelope_digest": "",
    }
    envelope["envelope_digest"] = digest({k: v for k, v in envelope.items() if k != "envelope_digest"})
    jsonschema.validate(envelope, _load_json(ROOT / "contracts" / "engineering-readiness-envelope.schema.json"))
    return envelope


def require_consumer(envelope: dict[str, Any], consumer: str) -> None:
    permissions = envelope.get("consumer_permissions", {})
    if consumer not in permissions:
        raise EngineeringGateError("E_ENG_GATE_CONSUMER_UNDECLARED", f"{consumer} is not declared by the engineering manifest")
    if permissions[consumer]["status"] != "ALLOWED":
        raise EngineeringGateError(
            "E_ENG_GATE_CONSUMER_BLOCKED",
            f"{consumer} blocked by {permissions[consumer]['reason_codes']}",
        )


def render_markdown(envelope: dict[str, Any]) -> str:
    lines = [
        "# Engineering Gate Readiness",
        "",
        f"- **Authority layer:** {envelope['authority_layer']}",
        f"- **Policy:** {envelope['policy_id']}",
        f"- **Overall:** {envelope['overall_state']}",
        f"- **Technical:** {envelope['dimensions']['technical']}",
        f"- **Research provenance:** {envelope['dimensions']['research_provenance']}",
        f"- **External prerequisites:** {envelope['dimensions']['external_prerequisites']}",
        f"- **Source authority:** {envelope['dimensions']['source_authority']}",
        "",
        "## Declared consumer permissions",
        "",
    ]
    for consumer, row in envelope["consumer_permissions"].items():
        reasons = ", ".join(row["reason_codes"]) if row["reason_codes"] else "none"
        lines.append(f"- **{consumer}:** {row['status']} — {reasons}")
    lines.extend(["", "## Blockers", ""])
    if envelope["blockers"]:
        for row in envelope["blockers"]:
            ref = f" `{row['ref']}`" if row.get("ref") else ""
            lines.append(f"- **{row['dimension']} / {row['code']}**{ref}: {row['message']}")
    else:
        lines.append("- None.")
    lines.extend(["", "## Next action", "", envelope["next_action"], ""])
    return "\n".join(lines)
