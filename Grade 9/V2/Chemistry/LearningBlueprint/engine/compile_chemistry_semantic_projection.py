#!/usr/bin/env python3
"""Compile Engineering->Blueprint obligations into typed Chemistry semantic atoms.

This boundary is deliberately topic-neutral. It does not recognize gate names or
Chemistry topics. Semantic roles are projected only from the typed Engineering
obligation kind plus a declarative field-to-role policy. Downstream adapters may
consume these atoms, but they may not reclassify their semantic polarity.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
POLICY_REL = "policies/chemistry-semantic-projection.v1.json"
SCHEMA_REL = "contracts/chemistry-semantic-projection.schema.json"
OBLIGATION_SCHEMA_REL = "contracts/chemistry-engineering-blueprint-obligations.schema.json"


class ChemistrySemanticProjectionError(ValueError):
    def __init__(self, code: str, message: str = ""):
        super().__init__(f"{code}: {message}" if message else code)
        self.code = code
        self.message = message


def fail(code: str, message: str = "") -> None:
    raise ChemistrySemanticProjectionError(code, message)


def load(rel: str) -> dict[str, Any]:
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def canonical(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(obj: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical(obj).encode("utf-8")).hexdigest()


def digest_without(obj: dict[str, Any], field: str) -> str:
    value = copy.deepcopy(obj)
    value.pop(field, None)
    return digest(value)


def semantic_id(obligation_id: str, semantic_role: str, source_field: str) -> str:
    seed = f"{obligation_id}|{semantic_role}|{source_field}".encode("utf-8")
    return "CHEM-SEM-" + hashlib.sha256(seed).hexdigest()[:24].upper()


def _validate_obligation_packet(packet: dict[str, Any]) -> None:
    try:
        jsonschema.validate(packet, load(OBLIGATION_SCHEMA_REL))
    except jsonschema.ValidationError as exc:
        fail("CHEM_SEMANTIC_PROJECTION_OBLIGATION_SCHEMA", exc.message)
    if packet.get("packet_digest") != digest_without(packet, "packet_digest"):
        fail("CHEM_SEMANTIC_PROJECTION_OBLIGATION_DIGEST_MISMATCH")
    if packet.get("status") != "BLUEPRINT_OBLIGATIONS_READY":
        fail("CHEM_SEMANTIC_PROJECTION_OBLIGATION_NOT_READY")


def _validate_policy(policy: dict[str, Any]) -> None:
    if policy.get("policy_id") != "CHEM-ENGINEERING-SEMANTIC-PROJECTION-v1":
        fail("CHEM_SEMANTIC_PROJECTION_POLICY_INVALID", "policy_id")
    if policy.get("subject") != "CHEMISTRY" or policy.get("status") != "ACTIVE":
        fail("CHEM_SEMANTIC_PROJECTION_POLICY_INVALID", "subject/status")
    kind_rules = policy.get("kind_rules")
    roles = policy.get("semantic_roles")
    if not isinstance(kind_rules, dict) or not kind_rules:
        fail("CHEM_SEMANTIC_PROJECTION_POLICY_INVALID", "kind_rules")
    if not isinstance(roles, list) or not roles or len(roles) != len(set(roles)):
        fail("CHEM_SEMANTIC_PROJECTION_POLICY_INVALID", "semantic_roles")
    allowed_roles = set(roles)
    seen_pairs: set[tuple[str, str, str]] = set()
    for kind, rules in kind_rules.items():
        if not isinstance(kind, str) or not isinstance(rules, list) or not rules:
            fail("CHEM_SEMANTIC_PROJECTION_POLICY_INVALID", str(kind))
        for rule in rules:
            if not isinstance(rule, dict):
                fail("CHEM_SEMANTIC_PROJECTION_POLICY_INVALID", kind)
            field = rule.get("source_field")
            role = rule.get("semantic_role")
            required = rule.get("required")
            if not isinstance(field, str) or not field or role not in allowed_roles or not isinstance(required, bool):
                fail("CHEM_SEMANTIC_PROJECTION_POLICY_INVALID", f"{kind}:{field}:{role}")
            key = (kind, field, role)
            if key in seen_pairs:
                fail("CHEM_SEMANTIC_PROJECTION_POLICY_DUPLICATE_RULE", ":".join(key))
            seen_pairs.add(key)


def _content(payload: dict[str, Any], field: str, *, required: bool, obligation_id: str) -> str | None:
    if field not in payload or payload[field] is None:
        if required:
            fail("CHEM_SEMANTIC_PROJECTION_SOURCE_FIELD_MISSING", f"{obligation_id}:{field}")
        return None
    value = payload[field]
    if not isinstance(value, str) or not value.strip():
        if required:
            fail("CHEM_SEMANTIC_PROJECTION_SOURCE_FIELD_INVALID", f"{obligation_id}:{field}")
        return None
    return value.strip()


def compile_semantic_projection(
    obligation_packet: dict[str, Any],
    *,
    policy: dict[str, Any] | None = None,
    projection_id: str | None = None,
) -> dict[str, Any]:
    _validate_obligation_packet(obligation_packet)
    policy = copy.deepcopy(policy) if policy is not None else load(POLICY_REL)
    _validate_policy(policy)

    kind_rules = policy["kind_rules"]
    atoms: list[dict[str, Any]] = []
    for obligation in obligation_packet["obligations"]:
        kind = obligation["kind"]
        rules = kind_rules.get(kind)
        if not rules:
            fail("CHEM_SEMANTIC_PROJECTION_KIND_UNMAPPED", kind)
        payload = obligation.get("payload")
        if not isinstance(payload, dict):
            fail("CHEM_SEMANTIC_PROJECTION_SOURCE_PAYLOAD_INVALID", obligation["obligation_id"])
        payload_digest = digest(payload)
        for rule in rules:
            field = rule["source_field"]
            value = _content(
                payload,
                field,
                required=rule["required"],
                obligation_id=obligation["obligation_id"],
            )
            if value is None:
                continue
            atoms.append({
                "semantic_id": semantic_id(obligation["obligation_id"], rule["semantic_role"], field),
                "source_gate_id": obligation["gate_id"],
                "source_obligation_id": obligation["obligation_id"],
                "source_asset_ref": obligation["asset_ref"],
                "source_kind": kind,
                "source_field": field,
                "semantic_role": rule["semantic_role"],
                "content": value,
                "direct": obligation["direct"],
                "authorized_modes": list(obligation["authorized_modes"]),
                "required_realization_modes": list(obligation["required_realization_modes"]),
                "source_authority_tier": obligation["source_authority_tier"],
                "source_payload_digest": payload_digest,
            })

    if not atoms:
        fail("CHEM_SEMANTIC_PROJECTION_EMPTY")
    ids = [row["semantic_id"] for row in atoms]
    if len(ids) != len(set(ids)):
        fail("CHEM_SEMANTIC_PROJECTION_ID_COLLISION")

    role_counts = dict(sorted(Counter(row["semantic_role"] for row in atoms).items()))
    resolved_projection_id = projection_id or obligation_packet["packet_id"].replace(
        "CHEM-BP-OBL-", "CHEM-BP-SEM-", 1
    )
    projection = {
        "schema_version": "1.0.0",
        "projection_id": resolved_projection_id,
        "subject": "CHEMISTRY",
        "obligation_packet_id": obligation_packet["packet_id"],
        "obligation_packet_digest": obligation_packet["packet_digest"],
        "policy_ref": POLICY_REL,
        "policy_digest": digest(policy),
        "semantic_atoms": atoms,
        "counts": {
            "source_obligation_count": len(obligation_packet["obligations"]),
            "semantic_atom_count": len(atoms),
            "role_counts": role_counts,
        },
        "status": "SEMANTIC_PROJECTION_READY",
        "projection_digest": "",
    }
    projection["projection_digest"] = digest_without(projection, "projection_digest")
    try:
        jsonschema.validate(projection, load(SCHEMA_REL))
    except jsonschema.ValidationError as exc:
        fail("CHEM_SEMANTIC_PROJECTION_SCHEMA", exc.message)
    return projection


def validate_semantic_projection(
    obligation_packet: dict[str, Any],
    projection: dict[str, Any],
    *,
    policy: dict[str, Any] | None = None,
) -> dict[str, Any]:
    _validate_obligation_packet(obligation_packet)
    policy = copy.deepcopy(policy) if policy is not None else load(POLICY_REL)
    _validate_policy(policy)
    try:
        jsonschema.validate(projection, load(SCHEMA_REL))
    except jsonschema.ValidationError as exc:
        fail("CHEM_SEMANTIC_PROJECTION_SCHEMA", exc.message)
    if projection.get("projection_digest") != digest_without(projection, "projection_digest"):
        fail("CHEM_SEMANTIC_PROJECTION_DIGEST_MISMATCH")
    if projection.get("obligation_packet_id") != obligation_packet.get("packet_id"):
        fail("CHEM_SEMANTIC_PROJECTION_PACKET_MISMATCH", "packet_id")
    if projection.get("obligation_packet_digest") != obligation_packet.get("packet_digest"):
        fail("CHEM_SEMANTIC_PROJECTION_PACKET_MISMATCH", "packet_digest")
    if projection.get("policy_digest") != digest(policy):
        fail("CHEM_SEMANTIC_PROJECTION_POLICY_DRIFT")

    expected = compile_semantic_projection(
        obligation_packet,
        policy=policy,
        projection_id=projection["projection_id"],
    )
    if canonical(expected) != canonical(projection):
        fail("CHEM_SEMANTIC_PROJECTION_DRIFT")
    return {
        "status": "PASS",
        "projection_id": projection["projection_id"],
        "semantic_atom_count": projection["counts"]["semantic_atom_count"],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("obligation_packet")
    parser.add_argument("--out")
    args = parser.parse_args()
    packet = json.loads(Path(args.obligation_packet).read_text(encoding="utf-8"))
    projection = compile_semantic_projection(packet)
    text = json.dumps(projection, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
