#!/usr/bin/env python3
"""Compile Engineering representation obligations into governed C-H representation intents.

Scientific meaning comes only from Engineering obligations / semantic projection.
Pedagogical primitive selection comes only from declarative representation-intent
policy plus the existing C-H primitive/page-intent authority. Product adapters do
not provide primitive IDs or scientific representation payloads at this boundary.

The base policy must cover the complete Engineering representation-type enum. A type
may be RESOLVED or explicitly BLOCKED_C_H_PRIMITIVE_REQUIRED. Additive extensions may
resolve a blocked type, but may not override an already-resolved type, introduce a
new Engineering type, or alter scientific semantics.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
CHEM_ROOT = ROOT.parent
sys.path.insert(0, str(ROOT / "engine"))
sys.path.insert(0, str(CHEM_ROOT / "Representation" / "engine"))

from compile_chemistry_semantic_projection import (  # noqa: E402
    compile_semantic_projection,
    validate_semantic_projection,
)
from build_chemistry_representations import (  # noqa: E402
    primitive_supports_capability,
    validate_registry,
)

POLICY_REL = "policies/chemistry-representation-intent.v1.json"
SCHEMA_REL = "contracts/chemistry-representation-intent.schema.json"
ENGINEERING_GATE_SCHEMA_REL = "contracts/chemistry-technical-engineering-gate.schema.json"
PRIMITIVE_REGISTRY_PATH = CHEM_ROOT / "Representation/registry/chemistry-teaching-primitive-registry.json"
PAGE_INTENT_PATH = CHEM_ROOT / "Representation/registry/chemistry-page-intent-profile.json"
RESOLVED = "RESOLVED"
BLOCKED = "BLOCKED_C_H_PRIMITIVE_REQUIRED"


class ChemistryRepresentationIntentError(ValueError):
    def __init__(self, code: str, message: str = ""):
        super().__init__(f"{code}: {message}" if message else code)
        self.code = code
        self.message = message


def fail(code: str, message: str = "") -> None:
    raise ChemistryRepresentationIntentError(code, message)


def load(rel: str) -> dict[str, Any]:
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def load_path(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def canonical(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(obj: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical(obj).encode("utf-8")).hexdigest()


def digest_without(obj: dict[str, Any], field: str) -> str:
    value = copy.deepcopy(obj)
    value.pop(field, None)
    return digest(value)


def _intent_id(obligation_id: str, product_mode: str) -> str:
    seed = f"{obligation_id}|{product_mode}".encode("utf-8")
    return "CHEM-REP-INTENT-" + hashlib.sha256(seed).hexdigest()[:24].upper()


def _engineering_representation_types() -> set[str]:
    schema = load(ENGINEERING_GATE_SCHEMA_REL)
    try:
        values = schema["$defs"]["subtopic_gate"]["properties"]["representations"]["items"]["properties"]["representation_type"]["enum"]
    except (KeyError, TypeError) as exc:
        fail("CHEM_REP_INTENT_ENGINEERING_TYPE_SCHEMA_INVALID", str(exc))
    if not isinstance(values, list) or not values or any(not isinstance(value, str) or not value for value in values):
        fail("CHEM_REP_INTENT_ENGINEERING_TYPE_SCHEMA_INVALID", "representation_type enum")
    if len(values) != len(set(values)):
        fail("CHEM_REP_INTENT_ENGINEERING_TYPE_SCHEMA_INVALID", "duplicate representation types")
    return set(values)


def _allowed_primitives(capability_ref: str, primitive_by_id: dict[str, Any], profile: dict[str, Any]) -> set[str]:
    allowed = set(profile.get("primary_primitives_by_capability", {}).get(capability_ref, []))
    for primitive_id in profile.get("conditional_primitives", {}).values():
        primitive = primitive_by_id.get(primitive_id)
        if primitive and primitive_supports_capability(primitive, capability_ref):
            allowed.add(primitive_id)
    return allowed


def _validate_resolved_rule(
    representation_type: str,
    rule: dict[str, Any],
    primitive_by_id: dict[str, Any],
    page_intent_profile: dict[str, Any],
) -> None:
    capability_ref = rule.get("capability_ref")
    primitive_id = rule.get("primitive_id")
    if not isinstance(capability_ref, str) or not capability_ref or not isinstance(primitive_id, str) or not primitive_id:
        fail("CHEM_REP_INTENT_POLICY_INVALID", representation_type)
    primitive = primitive_by_id.get(primitive_id)
    if primitive is None:
        fail("CHEM_REP_INTENT_POLICY_PRIMITIVE_UNKNOWN", f"{representation_type}:{primitive_id}")
    if not primitive_supports_capability(primitive, capability_ref):
        fail("CHEM_REP_INTENT_POLICY_CAPABILITY_MISMATCH", f"{representation_type}:{capability_ref}:{primitive_id}")
    if primitive_id not in _allowed_primitives(capability_ref, primitive_by_id, page_intent_profile):
        fail("CHEM_REP_INTENT_POLICY_PAGE_INTENT_REJECTED", f"{representation_type}:{capability_ref}:{primitive_id}")


def _validate_policy(
    policy: dict[str, Any],
    primitive_by_id: dict[str, Any],
    page_intent_profile: dict[str, Any],
) -> None:
    if policy.get("policy_id") != "CHEM-ENGINEERING-REPRESENTATION-INTENT-v1":
        fail("CHEM_REP_INTENT_POLICY_INVALID", "policy_id")
    if policy.get("subject") != "CHEMISTRY" or policy.get("status") != "ACTIVE":
        fail("CHEM_REP_INTENT_POLICY_INVALID", "subject/status")
    if policy.get("engineering_type_schema_ref") != ENGINEERING_GATE_SCHEMA_REL:
        fail("CHEM_REP_INTENT_POLICY_INVALID", "engineering_type_schema_ref")
    if policy.get("selection_rule") != "EXACT_REPRESENTATION_TYPE_TO_GOVERNED_CAPABILITY_AND_PRIMITIVE":
        fail("CHEM_REP_INTENT_POLICY_INVALID", "selection_rule")
    rules = policy.get("representation_type_rules")
    if not isinstance(rules, dict) or not rules:
        fail("CHEM_REP_INTENT_POLICY_INVALID", "representation_type_rules")
    engineering_types = _engineering_representation_types()
    if set(rules) != engineering_types:
        missing = sorted(engineering_types - set(rules))
        extra = sorted(set(rules) - engineering_types)
        fail("CHEM_REP_INTENT_POLICY_TYPE_COVERAGE", f"missing={missing};extra={extra}")
    for representation_type, rule in rules.items():
        if not isinstance(rule, dict):
            fail("CHEM_REP_INTENT_POLICY_INVALID", representation_type)
        status = rule.get("status")
        if status == RESOLVED:
            _validate_resolved_rule(representation_type, rule, primitive_by_id, page_intent_profile)
        elif status == BLOCKED:
            reason = rule.get("reason")
            if not isinstance(reason, str) or not reason.strip():
                fail("CHEM_REP_INTENT_POLICY_INVALID", f"{representation_type}:blocked reason")
            if "capability_ref" in rule or "primitive_id" in rule:
                fail("CHEM_REP_INTENT_POLICY_INVALID", f"{representation_type}:blocked mapping")
        else:
            fail("CHEM_REP_INTENT_POLICY_INVALID", f"{representation_type}:status")


def _apply_intent_extensions(
    base_policy: dict[str, Any],
    extensions: list[dict[str, Any]],
    primitive_by_id: dict[str, Any],
    page_intent_profile: dict[str, Any],
) -> tuple[dict[str, Any], list[str]]:
    effective = copy.deepcopy(base_policy)
    extension_refs: list[str] = []
    seen: set[str] = set()
    engineering_types = _engineering_representation_types()
    for extension in extensions:
        if not isinstance(extension, dict):
            fail("CHEM_REP_INTENT_EXTENSION_INVALID", "not object")
        extension_id = extension.get("extension_id")
        if not isinstance(extension_id, str) or not extension_id or extension_id in seen:
            fail("CHEM_REP_INTENT_EXTENSION_INVALID", str(extension_id))
        seen.add(extension_id)
        if extension.get("schema_version") != "1.0.0" or extension.get("subject") != "CHEMISTRY":
            fail("CHEM_REP_INTENT_EXTENSION_INVALID", extension_id)
        if extension.get("extends_policy") != base_policy["policy_id"] or extension.get("additive_only") is not True:
            fail("CHEM_REP_INTENT_EXTENSION_AUTHORITY_INVALID", extension_id)
        rows = extension.get("representation_type_rules")
        if not isinstance(rows, dict) or not rows:
            fail("CHEM_REP_INTENT_EXTENSION_INVALID", extension_id)
        for representation_type, rule in rows.items():
            if representation_type not in engineering_types:
                fail("CHEM_REP_INTENT_EXTENSION_TYPE_UNKNOWN", representation_type)
            current = effective["representation_type_rules"][representation_type]
            if current.get("status") != BLOCKED:
                fail("CHEM_REP_INTENT_EXTENSION_OVERRIDE_FORBIDDEN", representation_type)
            if not isinstance(rule, dict) or rule.get("status") != RESOLVED:
                fail("CHEM_REP_INTENT_EXTENSION_INVALID", f"{extension_id}:{representation_type}")
            _validate_resolved_rule(representation_type, rule, primitive_by_id, page_intent_profile)
            effective["representation_type_rules"][representation_type] = copy.deepcopy(rule)
        extension_refs.append(extension_id)
    effective["applied_extension_refs"] = list(extension_refs)
    _validate_policy(effective, primitive_by_id, page_intent_profile)
    return effective, extension_refs


def _scientific_semantics(
    obligation: dict[str, Any],
    semantic_atoms: list[dict[str, Any]],
) -> dict[str, Any]:
    payload = obligation.get("payload")
    if not isinstance(payload, dict):
        fail("CHEM_REP_INTENT_ENGINEERING_PAYLOAD_INVALID", obligation["obligation_id"])
    required_strings = [
        "name", "chemistry_encoded", "what_cannot_be_omitted",
        "common_incorrect_version", "verification_method",
    ]
    for field in required_strings:
        value = payload.get(field)
        if not isinstance(value, str) or not value.strip():
            fail("CHEM_REP_INTENT_ENGINEERING_FIELD_MISSING", f"{obligation['obligation_id']}:{field}")
    labels = payload.get("mandatory_labels")
    if not isinstance(labels, list) or not labels or any(not isinstance(x, str) or not x.strip() for x in labels):
        fail("CHEM_REP_INTENT_ENGINEERING_FIELD_MISSING", f"{obligation['obligation_id']}:mandatory_labels")
    atoms = [row for row in semantic_atoms if row["source_obligation_id"] == obligation["obligation_id"]]
    if not atoms or "REPRESENTATION_REQUIREMENT" not in {row["semantic_role"] for row in atoms}:
        fail("CHEM_REP_INTENT_SEMANTIC_LINEAGE_MISSING", obligation["obligation_id"])
    return {
        "name": payload["name"].strip(),
        "chemistry_encoded": payload["chemistry_encoded"].strip(),
        "mandatory_labels": [x.strip() for x in labels],
        "what_cannot_be_omitted": payload["what_cannot_be_omitted"].strip(),
        "common_incorrect_version": payload["common_incorrect_version"].strip(),
        "verification_method": payload["verification_method"].strip(),
        "semantic_atom_refs": [row["semantic_id"] for row in atoms],
        "semantic_roles": sorted({row["semantic_role"] for row in atoms}),
    }


def compile_representation_intent(
    product_mode: str,
    obligation_packet: dict[str, Any],
    *,
    semantic_projection: dict[str, Any] | None = None,
    policy: dict[str, Any] | None = None,
    primitive_registry: dict[str, Any] | None = None,
    page_intent_profile: dict[str, Any] | None = None,
    representation_intent_extensions: list[dict[str, Any]] | None = None,
    intent_packet_id: str | None = None,
) -> dict[str, Any]:
    if product_mode not in {"CORE1A", "CORE1B", "CORE2A", "CORE2B"}:
        fail("CHEM_REP_INTENT_MODE_INVALID", product_mode)
    if obligation_packet.get("status") != "BLUEPRINT_OBLIGATIONS_READY":
        fail("CHEM_REP_INTENT_OBLIGATION_PACKET_NOT_READY")

    semantic_projection = semantic_projection or compile_semantic_projection(obligation_packet)
    try:
        validate_semantic_projection(obligation_packet, semantic_projection)
    except Exception as exc:
        fail("CHEM_REP_INTENT_SEMANTIC_PROJECTION_INVALID", str(exc))

    primitive_registry = copy.deepcopy(primitive_registry) if primitive_registry is not None else load_path(PRIMITIVE_REGISTRY_PATH)
    page_intent_profile = copy.deepcopy(page_intent_profile) if page_intent_profile is not None else load_path(PAGE_INTENT_PATH)
    primitive_by_id = validate_registry(primitive_registry)
    if page_intent_profile.get("subject") != "CHEMISTRY" or page_intent_profile.get("renderer_selection_forbidden") is not True:
        fail("CHEM_REP_INTENT_PAGE_INTENT_INVALID")

    base_policy = copy.deepcopy(policy) if policy is not None else load(POLICY_REL)
    _validate_policy(base_policy, primitive_by_id, page_intent_profile)
    effective_policy, extension_refs = _apply_intent_extensions(
        base_policy,
        list(representation_intent_extensions or []),
        primitive_by_id,
        page_intent_profile,
    )
    rules = effective_policy["representation_type_rules"]

    authorized_rows = [
        row for row in obligation_packet.get("obligations", [])
        if row.get("kind") == "REPRESENTATION" and product_mode in row.get("authorized_modes", [])
    ]
    intents: list[dict[str, Any]] = []
    for obligation in authorized_rows:
        payload = obligation.get("payload")
        representation_type = payload.get("representation_type") if isinstance(payload, dict) else None
        if not isinstance(representation_type, str) or not representation_type.strip():
            fail("CHEM_REP_INTENT_TYPE_MISSING", obligation["obligation_id"])
        representation_type = representation_type.strip()
        rule = rules.get(representation_type)
        if rule is None:
            fail("CHEM_REP_INTENT_TYPE_UNMAPPED", representation_type)
        if rule.get("status") == BLOCKED:
            fail("CHEM_REP_INTENT_C_H_SUPPORT_MISSING", f"{representation_type}:{rule['reason']}")
        capability_ref = rule["capability_ref"]
        primitive_id = rule["primitive_id"]
        primitive = primitive_by_id[primitive_id]
        required_realization = bool(obligation.get("direct") and product_mode in obligation.get("required_realization_modes", []))
        intents.append({
            "intent_id": _intent_id(obligation["obligation_id"], product_mode),
            "source_gate_id": obligation["gate_id"],
            "source_obligation_id": obligation["obligation_id"],
            "source_representation_ref": obligation["asset_ref"],
            "direct": obligation["direct"],
            "required_realization": required_realization,
            "representation_type": representation_type,
            "capability_ref": capability_ref,
            "primitive_id": primitive_id,
            "selection_authority": "ENGINEERING_REPRESENTATION_TYPE_PLUS_C_H_PAGE_INTENT",
            "scientific_semantics": _scientific_semantics(
                obligation,
                semantic_projection["semantic_atoms"],
            ),
            "primitive_authority": {
                "instructional_job": primitive["instructional_job"],
                "attention_target": primitive["attention_target"],
                "translation_obligation": primitive["translation_obligation"],
                "learner_action": primitive["learner_action"],
                "renderer_constraints": sorted(set(primitive["renderer_constraints"])),
            },
        })

    suffix = obligation_packet["packet_id"].removeprefix("CHEM-BP-OBL-")
    packet = {
        "schema_version": "1.0.0",
        "intent_packet_id": intent_packet_id or f"CHEM-REP-INT-{suffix}-{product_mode}",
        "subject": "CHEMISTRY",
        "product_mode": product_mode,
        "obligation_packet_id": obligation_packet["packet_id"],
        "obligation_packet_digest": obligation_packet["packet_digest"],
        "semantic_projection_id": semantic_projection["projection_id"],
        "semantic_projection_digest": semantic_projection["projection_digest"],
        "policy_ref": POLICY_REL,
        "policy_digest": digest(effective_policy),
        "policy_extension_refs": extension_refs,
        "primitive_registry_ref": primitive_registry["registry_id"],
        "page_intent_profile_ref": page_intent_profile["profile_id"],
        "intents": intents,
        "counts": {
            "authorized_representation_count": len(authorized_rows),
            "required_representation_count": sum(row["required_realization"] for row in intents),
            "intent_count": len(intents),
        },
        "status": "REPRESENTATION_INTENT_READY",
        "intent_packet_digest": "",
    }
    packet["intent_packet_digest"] = digest_without(packet, "intent_packet_digest")
    try:
        jsonschema.validate(packet, load(SCHEMA_REL))
    except jsonschema.ValidationError as exc:
        fail("CHEM_REP_INTENT_SCHEMA", exc.message)
    return packet


def validate_representation_intent(
    product_mode: str,
    obligation_packet: dict[str, Any],
    intent_packet: dict[str, Any],
    *,
    semantic_projection: dict[str, Any] | None = None,
    policy: dict[str, Any] | None = None,
    primitive_registry: dict[str, Any] | None = None,
    page_intent_profile: dict[str, Any] | None = None,
    representation_intent_extensions: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    try:
        jsonschema.validate(intent_packet, load(SCHEMA_REL))
    except jsonschema.ValidationError as exc:
        fail("CHEM_REP_INTENT_SCHEMA", exc.message)
    if intent_packet.get("intent_packet_digest") != digest_without(intent_packet, "intent_packet_digest"):
        fail("CHEM_REP_INTENT_DIGEST_MISMATCH")
    expected = compile_representation_intent(
        product_mode,
        obligation_packet,
        semantic_projection=semantic_projection,
        policy=policy,
        primitive_registry=primitive_registry,
        page_intent_profile=page_intent_profile,
        representation_intent_extensions=representation_intent_extensions,
        intent_packet_id=intent_packet["intent_packet_id"],
    )
    if canonical(expected) != canonical(intent_packet):
        fail("CHEM_REP_INTENT_DRIFT")
    return {"status": "PASS", "intent_count": intent_packet["counts"]["intent_count"]}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("product_mode", choices=["CORE1A", "CORE1B", "CORE2A", "CORE2B"])
    parser.add_argument("obligation_packet")
    parser.add_argument("--semantic-projection")
    parser.add_argument("--out")
    args = parser.parse_args()
    packet = json.loads(Path(args.obligation_packet).read_text(encoding="utf-8"))
    projection = None
    if args.semantic_projection:
        projection = json.loads(Path(args.semantic_projection).read_text(encoding="utf-8"))
    intent = compile_representation_intent(args.product_mode, packet, semantic_projection=projection)
    text = json.dumps(intent, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
