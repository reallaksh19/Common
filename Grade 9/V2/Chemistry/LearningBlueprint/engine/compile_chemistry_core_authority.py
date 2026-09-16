#!/usr/bin/env python3
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
sys.path.insert(0, str(ROOT / "engine"))

from compile_chemistry_engineering_closure import load  # noqa: E402
from compile_chemistry_learner_gate_projection import compile_learner_gate_projection  # noqa: E402
from compile_chemistry_semantic_projection import compile_semantic_projection  # noqa: E402
from validate_static_b_layer_boundary import validate_core1b, validate_core2b  # noqa: E402

SCHEMA_REL = "contracts/chemistry-core-authority.schema.json"
OBLIGATION_SCHEMA_REL = "contracts/chemistry-engineering-blueprint-obligations.schema.json"


class ChemistryCoreAuthorityError(ValueError):
    def __init__(self, code: str, message: str = ""):
        super().__init__(f"{code}: {message}" if message else code)
        self.code = code
        self.message = message


def fail(code: str, message: str = "") -> None:
    raise ChemistryCoreAuthorityError(code, message)


def canonical(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(obj: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical(obj).encode("utf-8")).hexdigest()


def _digest_without(obj: dict[str, Any], field: str) -> str:
    payload = copy.deepcopy(obj)
    payload.pop(field, None)
    return digest(payload)


def _validate_packet(packet: dict[str, Any]) -> None:
    try:
        jsonschema.validate(packet, load(OBLIGATION_SCHEMA_REL))
    except jsonschema.ValidationError as exc:
        fail("CHEM_CORE_AUTH_OBLIGATION_SCHEMA", exc.message)
    if packet.get("packet_digest") != _digest_without(packet, "packet_digest"):
        fail("CHEM_CORE_AUTH_OBLIGATION_DIGEST_MISMATCH")
    if packet.get("status") != "BLUEPRINT_OBLIGATIONS_READY":
        fail("CHEM_CORE_AUTH_OBLIGATION_NOT_READY")


def _scope_units(product_mode: str, payload: dict[str, Any]) -> list[dict[str, str]]:
    units: list[dict[str, str]] = []
    if product_mode == "CORE1A":
        manuscript = payload.get("manuscript")
        if not isinstance(manuscript, dict) or not isinstance(manuscript.get("buckets"), list):
            fail("CHEM_CORE_AUTH_CORE1A_MANUSCRIPT_REQUIRED")
        for bucket in manuscript["buckets"]:
            for atom in bucket.get("learning_atoms", []):
                atom_id = atom.get("atom_id")
                if atom_id:
                    units.append({"scope_unit_id": str(atom_id), "scope_unit_kind": "ATOM"})
    elif product_mode == "CORE2A":
        for key in ("source_plan", "challenge_plan"):
            plan = payload.get(key)
            if plan is None:
                continue
            if not isinstance(plan, dict) or not isinstance(plan.get("items"), list):
                fail("CHEM_CORE_AUTH_CORE2A_PLAN_INVALID", key)
            for item in plan["items"]:
                item_id = item.get("item_id")
                if item_id:
                    units.append({"scope_unit_id": str(item_id), "scope_unit_kind": "ITEM"})
    elif product_mode == "CORE1B":
        module_ref = payload.get("module_ref")
        if module_ref:
            units.append({"scope_unit_id": str(module_ref), "scope_unit_kind": "MODULE"})
    elif product_mode == "CORE2B":
        selected = payload.get("selected_item_id")
        if selected:
            units.append({"scope_unit_id": str(selected), "scope_unit_kind": "ITEM"})
    else:
        fail("CHEM_CORE_AUTH_MODE_INVALID", product_mode)

    keys = [(row["scope_unit_kind"], row["scope_unit_id"]) for row in units]
    if not units or len(keys) != len(set(keys)):
        fail("CHEM_CORE_AUTH_SCOPE_UNITS_INVALID")
    return units


def _surface_strings(value: Any, parent_key: str = "") -> list[str]:
    hidden_suffixes = ("_id", "_ids", "_ref", "_refs", "_digest", "_digests")
    hidden_keys = {
        "product_mode", "subject", "delivery_mode", "help_mode", "question_mode",
        "source_qc_status", "provenance_class", "primitive_id", "representation_type",
        "target_core_role", "scope_unit_kind",
    }
    out: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            if key in hidden_keys or key.endswith(hidden_suffixes):
                continue
            out.extend(_surface_strings(child, key))
    elif isinstance(value, list):
        for child in value:
            out.extend(_surface_strings(child, parent_key))
    elif isinstance(value, str) and value.strip():
        out.append(value.strip())
    return out


def _mode_validation(product_mode: str, payload: dict[str, Any]) -> dict[str, Any]:
    if product_mode == "CORE1A":
        manuscript = payload.get("manuscript")
        representations = payload.get("representation_bundle")
        if not isinstance(manuscript, dict) or not manuscript.get("manuscript_id") or not isinstance(manuscript.get("buckets"), list):
            fail("CHEM_CORE_AUTH_CORE1A_MANUSCRIPT_REQUIRED")
        if not isinstance(representations, dict) or not representations.get("bundle_id"):
            fail("CHEM_CORE_AUTH_REPRESENTATION_BUNDLE_REQUIRED")
        return {"status": "PASS", "adapter": "CORE1A_MANUSCRIPT", "bucket_count": len(manuscript["buckets"]), "representation_bundle_ref": representations["bundle_id"]}
    if product_mode == "CORE2A":
        source = payload.get("source_plan")
        challenge = payload.get("challenge_plan")
        representations = payload.get("representation_bundle")
        if source is None and challenge is None:
            fail("CHEM_CORE_AUTH_CORE2A_PLAN_REQUIRED")
        if not isinstance(representations, dict) or not representations.get("bundle_id"):
            fail("CHEM_CORE_AUTH_REPRESENTATION_BUNDLE_REQUIRED")
        count = sum(len(plan.get("items", [])) for plan in (source, challenge) if isinstance(plan, dict))
        if count < 1:
            fail("CHEM_CORE_AUTH_CORE2A_ITEMS_REQUIRED")
        return {"status": "PASS", "adapter": "CORE2A_PLANS", "item_count": count, "representation_bundle_ref": representations["bundle_id"]}
    if product_mode == "CORE1B":
        return validate_core1b(payload)
    if product_mode == "CORE2B":
        return validate_core2b(payload)
    fail("CHEM_CORE_AUTH_MODE_INVALID", product_mode)


def _semantic_closure(
    product_mode: str,
    obligation_packet: dict[str, Any],
    realized_obligation_ids: list[str],
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Bind claimed obligation realization to deterministic semantic-role lineage."""
    projection = compile_semantic_projection(obligation_packet)
    realized_obligations = set(realized_obligation_ids)
    authorized_atoms = [
        row for row in projection["semantic_atoms"]
        if product_mode in row["authorized_modes"]
    ]
    required_atoms = [
        row for row in authorized_atoms
        if row["direct"] and product_mode in row["required_realization_modes"]
    ]
    realized_atoms = [
        row for row in authorized_atoms
        if row["source_obligation_id"] in realized_obligations
    ]

    required_ids = {row["semantic_id"] for row in required_atoms}
    realized_ids = {row["semantic_id"] for row in realized_atoms}
    missing_required = sorted(required_ids - realized_ids)
    if missing_required:
        fail("CHEM_CORE_AUTH_REQUIRED_SEMANTIC_MISSING", ",".join(missing_required))

    realized_sources = {row["source_obligation_id"] for row in realized_atoms}
    missing_semantic_lineage = sorted(realized_obligations - realized_sources)
    if missing_semantic_lineage:
        fail(
            "CHEM_CORE_AUTH_REALIZED_OBLIGATION_WITHOUT_SEMANTICS",
            ",".join(missing_semantic_lineage),
        )

    closure = {
        "status": "PASS",
        "authorized_semantic_ids": sorted(row["semantic_id"] for row in authorized_atoms),
        "required_semantic_ids": sorted(required_ids),
        "realized_semantic_ids": sorted(realized_ids),
        "realized_source_obligation_ids": sorted(realized_sources),
        "semantic_atom_count": len(realized_atoms),
    }
    return projection, closure


def _learner_gate_closure(
    product_mode: str,
    obligation_packet: dict[str, Any],
    semantic_projection: dict[str, Any],
    realized_obligation_ids: list[str],
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Bind Core realization to direct learner jobs without promoting prerequisite context."""
    projection = compile_learner_gate_projection(
        obligation_packet,
        semantic_projection=semantic_projection,
    )
    realized_obligations = set(realized_obligation_ids)
    authorized_gates = [
        row for row in projection["learner_gates"]
        if product_mode in row["authorized_modes"]
    ]
    required_gates = [
        row for row in authorized_gates
        if product_mode in row["required_realization_modes"]
    ]
    realized_gates = [
        row for row in authorized_gates
        if row["source_obligation_id"] in realized_obligations
    ]
    required_ids = {row["learner_gate_id"] for row in required_gates}
    realized_ids = {row["learner_gate_id"] for row in realized_gates}
    missing_required = sorted(required_ids - realized_ids)
    if missing_required:
        fail("CHEM_CORE_AUTH_REQUIRED_LEARNER_GATE_MISSING", ",".join(missing_required))

    semantic_by_id = {
        row["semantic_id"]: row for row in semantic_projection["semantic_atoms"]
    }
    context_ids = sorted(
        semantic_id for semantic_id in projection["context_semantic_ids"]
        if product_mode in semantic_by_id[semantic_id]["authorized_modes"]
    )
    metadata_ids = sorted(
        semantic_id for semantic_id in projection["metadata_semantic_ids"]
        if product_mode in semantic_by_id[semantic_id]["authorized_modes"]
    )
    if set(context_ids) & set(realized_ids):
        fail("CHEM_CORE_AUTH_CONTEXT_PROMOTED_TO_LEARNER_GATE")

    closure = {
        "status": "PASS",
        "authorized_learner_gate_ids": sorted(row["learner_gate_id"] for row in authorized_gates),
        "required_learner_gate_ids": sorted(required_ids),
        "realized_learner_gate_ids": sorted(realized_ids),
        "context_semantic_ids": context_ids,
        "metadata_semantic_ids": metadata_ids,
        "learner_gate_count": len(realized_gates),
    }
    return projection, closure


def compile_core_authority(
    product_mode: str,
    subtopic_id: str,
    payload: dict[str, Any],
    obligation_packet: dict[str, Any],
    realized_obligation_ids: list[str],
    *,
    authority_id: str,
    payload_ref: str,
) -> dict[str, Any]:
    _validate_packet(obligation_packet)
    if product_mode not in {"CORE1A", "CORE1B", "CORE2A", "CORE2B"}:
        fail("CHEM_CORE_AUTH_MODE_INVALID", product_mode)
    if subtopic_id != obligation_packet["scope_ref"]:
        fail("CHEM_CORE_AUTH_SUBTOPIC_MISMATCH", f"{subtopic_id}!={obligation_packet['scope_ref']}")

    validation = _mode_validation(product_mode, payload)
    obligations = {row["obligation_id"]: row for row in obligation_packet["obligations"]}
    realized = list(realized_obligation_ids)
    if len(realized) != len(set(realized)):
        fail("CHEM_CORE_AUTH_REALIZATION_DUPLICATE")
    unknown = sorted(set(realized) - set(obligations))
    if unknown:
        fail("CHEM_CORE_AUTH_REALIZATION_UNKNOWN", ",".join(unknown))
    unauthorized = sorted(
        oid for oid in realized if product_mode not in obligations[oid]["authorized_modes"]
    )
    if unauthorized:
        fail("CHEM_CORE_AUTH_REALIZATION_UNAUTHORIZED", ",".join(unauthorized))

    required = {
        row["obligation_id"]
        for row in obligation_packet["obligations"]
        if row["direct"] and product_mode in row["required_realization_modes"]
    }
    missing = sorted(required - set(realized))
    if missing:
        fail("CHEM_CORE_AUTH_REQUIRED_OBLIGATION_MISSING", ",".join(missing))

    semantic_projection, semantic_closure = _semantic_closure(
        product_mode,
        obligation_packet,
        realized,
    )
    learner_gate_projection, learner_gate_closure = _learner_gate_closure(
        product_mode,
        obligation_packet,
        semantic_projection,
        realized,
    )

    authority = {
        "schema_version": "1.0.0",
        "authority_id": authority_id,
        "subject": "CHEMISTRY",
        "product_mode": product_mode,
        "subtopic_id": subtopic_id,
        "obligation_packet_id": obligation_packet["packet_id"],
        "obligation_packet_digest": obligation_packet["packet_digest"],
        "semantic_projection_id": semantic_projection["projection_id"],
        "semantic_projection_digest": semantic_projection["projection_digest"],
        "semantic_closure": semantic_closure,
        "learner_gate_projection_id": learner_gate_projection["projection_id"],
        "learner_gate_projection_digest": learner_gate_projection["projection_digest"],
        "learner_gate_closure": learner_gate_closure,
        "payload_ref": payload_ref,
        "payload_digest": digest(payload),
        "scope_units": _scope_units(product_mode, payload),
        "realized_obligation_ids": realized,
        "learner_surface_strings": _surface_strings(payload),
        "validation_evidence": validation,
        "status": "CORE_AUTHORITY_READY",
        "authority_digest": "",
    }
    authority["authority_digest"] = _digest_without(authority, "authority_digest")
    try:
        jsonschema.validate(authority, load(SCHEMA_REL))
    except jsonschema.ValidationError as exc:
        fail("CHEM_CORE_AUTH_SCHEMA", exc.message)
    return authority


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["CORE1A", "CORE1B", "CORE2A", "CORE2B"])
    parser.add_argument("subtopic_id")
    parser.add_argument("payload")
    parser.add_argument("obligation_packet")
    parser.add_argument("realized_obligations")
    parser.add_argument("--authority-id", required=True)
    parser.add_argument("--payload-ref", required=True)
    parser.add_argument("--out")
    args = parser.parse_args()
    payload = json.loads(Path(args.payload).read_text(encoding="utf-8"))
    packet = json.loads(Path(args.obligation_packet).read_text(encoding="utf-8"))
    realized = json.loads(Path(args.realized_obligations).read_text(encoding="utf-8"))
    authority = compile_core_authority(
        args.mode, args.subtopic_id, payload, packet, realized,
        authority_id=args.authority_id, payload_ref=args.payload_ref,
    )
    text = json.dumps(authority, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
