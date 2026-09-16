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


def _core1a_section_lineage(manuscript: dict[str, Any]) -> dict[str, Any]:
    """Close Core1A section identity against its declared learning-atom denominator."""
    total_atoms = 0
    total_sections = 0
    for bucket_index, bucket in enumerate(manuscript.get("buckets", []), 1):
        if not isinstance(bucket, dict):
            fail("CHEM_CORE_AUTH_CORE1A_BUCKET_INVALID", str(bucket_index))
        atoms = bucket.get("learning_atoms")
        sections = bucket.get("teaching_sections")
        if not isinstance(atoms, list) or not atoms:
            fail("CHEM_CORE_AUTH_CORE1A_LEARNING_ATOMS_REQUIRED", str(bucket_index))
        if not isinstance(sections, list) or not sections:
            fail("CHEM_CORE_AUTH_CORE1A_TEACHING_SECTIONS_REQUIRED", str(bucket_index))
        atom_ids = [str(row.get("atom_id", "")).strip() for row in atoms if isinstance(row, dict)]
        if len(atom_ids) != len(atoms) or any(not value for value in atom_ids):
            fail("CHEM_CORE_AUTH_CORE1A_LEARNING_ATOM_ID_INVALID", str(bucket_index))
        if len(atom_ids) != len(set(atom_ids)):
            fail("CHEM_CORE_AUTH_CORE1A_LEARNING_ATOM_DUPLICATE", str(bucket_index))
        if len(sections) != len(atoms):
            fail(
                "CHEM_CORE_AUTH_CORE1A_SECTION_ATOM_COUNT_MISMATCH",
                f"bucket={bucket_index}:sections={len(sections)}:atoms={len(atoms)}",
            )
        if any(not isinstance(section, dict) for section in sections):
            fail("CHEM_CORE_AUTH_CORE1A_TEACHING_SECTION_INVALID", str(bucket_index))
        total_atoms += len(atoms)
        total_sections += len(sections)
    if total_atoms < 1 or total_sections != total_atoms:
        fail("CHEM_CORE_AUTH_CORE1A_SECTION_LINEAGE_EMPTY")
    return {
        "status": "PASS",
        "lineage_mode": "ORDERED_LEARNING_ATOM",
        "learning_atom_count": total_atoms,
        "teaching_section_count": total_sections,
    }


def _mode_validation(product_mode: str, payload: dict[str, Any]) -> dict[str, Any]:
    if product_mode == "CORE1A":
        manuscript = payload.get("manuscript")
        representations = payload.get("representation_bundle")
        if not isinstance(manuscript, dict) or not manuscript.get("manuscript_id") or not isinstance(manuscript.get("buckets"), list):
            fail("CHEM_CORE_AUTH_CORE1A_MANUSCRIPT_REQUIRED")
        if not isinstance(representations, dict) or not representations.get("bundle_id"):
            fail("CHEM_CORE_AUTH_REPRESENTATION_BUNDLE_REQUIRED")
        lineage = _core1a_section_lineage(manuscript)
        return {
            "status": "PASS",
            "adapter": "CORE1A_MANUSCRIPT",
            "bucket_count": len(manuscript["buckets"]),
            "representation_bundle_ref": representations["bundle_id"],
            "section_lineage": lineage,
        }
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
        return {
            "status": "PASS",
            "adapter": "CORE2A_PLANS",
            "item_count": count,
            "representation_bundle_ref": representations["bundle_id"],
        }
    if product_mode == "CORE1B":
        return validate_core1b(payload)
    if product_mode == "CORE2B":
        return validate_core2b(payload)
    fail("CHEM_CORE_AUTH_MODE_INVALID", product_mode)


def _bundle_representation_refs(payload: dict[str, Any]) -> set[str]:
    bundle = payload.get("representation_bundle")
    if bundle is None:
        return set()
    if not isinstance(bundle, dict) or not str(bundle.get("bundle_id", "")).strip():
        fail("CHEM_CORE_AUTH_REPRESENTATION_BUNDLE_INVALID")
    rows = bundle.get("representations")
    if rows is None:
        rows = []
    if not isinstance(rows, list):
        fail("CHEM_CORE_AUTH_REPRESENTATION_BUNDLE_INVALID", "representations")
    refs: list[str] = []
    for row in rows:
        if not isinstance(row, dict) or not str(row.get("representation_id", "")).strip():
            fail("CHEM_CORE_AUTH_REPRESENTATION_BUNDLE_INVALID", "representation_id")
        refs.append(str(row["representation_id"]))
    if len(refs) != len(set(refs)):
        fail("CHEM_CORE_AUTH_REPRESENTATION_DUPLICATE")
    return set(refs)


def _used_representation_refs(product_mode: str, payload: dict[str, Any]) -> set[str]:
    refs: set[str] = set()
    if product_mode == "CORE1A":
        manuscript = payload.get("manuscript") or {}
        for bucket in manuscript.get("buckets", []):
            for section in bucket.get("teaching_sections", []):
                values = section.get("representation_refs", [])
                if not isinstance(values, list):
                    fail("CHEM_CORE_AUTH_REPRESENTATION_USAGE_INVALID", "CORE1A")
                refs.update(str(value) for value in values if str(value).strip())
    elif product_mode == "CORE1B":
        values = payload.get("used_representation_refs", [])
        if not isinstance(values, list):
            fail("CHEM_CORE_AUTH_REPRESENTATION_USAGE_INVALID", "CORE1B")
        refs.update(str(value) for value in values if str(value).strip())
    elif product_mode == "CORE2A":
        for key in ("source_plan", "challenge_plan"):
            plan = payload.get(key)
            if not isinstance(plan, dict):
                continue
            for item in plan.get("items", []):
                support = item.get("learner_support") or {}
                see = support.get("see_the_idea") or {}
                values = see.get("pre_taught_representation_refs", [])
                if not isinstance(values, list):
                    fail("CHEM_CORE_AUTH_REPRESENTATION_USAGE_INVALID", "CORE2A:see_the_idea")
                refs.update(str(value) for value in values if str(value).strip())
                binding = item.get("core1a_binding") or {}
                values = binding.get("h2_evidence_refs", [])
                if not isinstance(values, list):
                    fail("CHEM_CORE_AUTH_REPRESENTATION_USAGE_INVALID", "CORE2A:core1a_binding")
                refs.update(str(value) for value in values if str(value).strip())
    elif product_mode == "CORE2B":
        values = payload.get("used_representation_refs", [])
        if values is None:
            values = []
        if not isinstance(values, list):
            fail("CHEM_CORE_AUTH_REPRESENTATION_USAGE_INVALID", "CORE2B")
        refs.update(str(value) for value in values if str(value).strip())
    else:
        fail("CHEM_CORE_AUTH_MODE_INVALID", product_mode)
    return refs


def _representation_closure(
    product_mode: str,
    payload: dict[str, Any],
    obligation_packet: dict[str, Any],
    realized_obligation_ids: list[str],
) -> dict[str, Any]:
    authorized_rows = [
        row for row in obligation_packet["obligations"]
        if row["kind"] == "REPRESENTATION" and product_mode in row["authorized_modes"]
    ]
    direct_rows = [row for row in authorized_rows if row["direct"]]
    authorized_assets = {str(row["asset_ref"]) for row in authorized_rows}
    required_assets = {
        str(row["asset_ref"]) for row in direct_rows
        if product_mode in row["required_realization_modes"]
    }
    claimed_assets = {
        str(row["asset_ref"]) for row in direct_rows
        if row["obligation_id"] in set(realized_obligation_ids)
    }

    defined_refs = _bundle_representation_refs(payload)
    used_refs = _used_representation_refs(product_mode, payload)
    bindings = payload.get("representation_bindings", [])
    if bindings is None:
        bindings = []
    if not isinstance(bindings, list):
        fail("CHEM_CORE_AUTH_REPRESENTATION_BINDINGS_INVALID")

    by_rep: dict[str, set[str]] = {}
    for row in bindings:
        if not isinstance(row, dict):
            fail("CHEM_CORE_AUTH_REPRESENTATION_BINDINGS_INVALID")
        rep_ref = str(row.get("representation_ref", "")).strip()
        engineering_refs = row.get("engineering_representation_refs")
        if not rep_ref or not isinstance(engineering_refs, list) or not engineering_refs:
            fail("CHEM_CORE_AUTH_REPRESENTATION_BINDINGS_INVALID")
        refs = {str(value).strip() for value in engineering_refs if str(value).strip()}
        if not refs:
            fail("CHEM_CORE_AUTH_REPRESENTATION_BINDINGS_INVALID")
        if rep_ref in by_rep:
            fail("CHEM_CORE_AUTH_REPRESENTATION_BINDING_DUPLICATE", rep_ref)
        unauthorized = sorted(refs - authorized_assets)
        if unauthorized:
            fail("CHEM_CORE_AUTH_REPRESENTATION_ASSET_UNAUTHORIZED", ",".join(unauthorized))
        by_rep[rep_ref] = refs

    undefined = sorted(used_refs - defined_refs)
    if undefined:
        fail("CHEM_CORE_AUTH_REPRESENTATION_UNDEFINED", ",".join(undefined))
    unbound = sorted(used_refs - set(by_rep))
    if unbound:
        fail("CHEM_CORE_AUTH_REPRESENTATION_USE_UNBOUND", ",".join(unbound))

    realized_assets: set[str] = set()
    for rep_ref in used_refs:
        realized_assets.update(by_rep[rep_ref])

    missing_required = sorted(required_assets - realized_assets)
    if missing_required:
        fail("CHEM_CORE_AUTH_REQUIRED_REPRESENTATION_UNREALIZED", ",".join(missing_required))
    overclaimed = sorted(claimed_assets - realized_assets)
    if overclaimed:
        fail("CHEM_CORE_AUTH_REPRESENTATION_REALIZATION_OVERCLAIM", ",".join(overclaimed))
    if (required_assets or used_refs or claimed_assets) and not defined_refs:
        fail("CHEM_CORE_AUTH_REPRESENTATION_BUNDLE_EMPTY")

    return {
        "status": "PASS",
        "authorized_engineering_representation_refs": sorted(authorized_assets),
        "required_engineering_representation_refs": sorted(required_assets),
        "realized_engineering_representation_refs": sorted(realized_assets),
        "defined_representation_refs": sorted(defined_refs),
        "used_representation_refs": sorted(used_refs),
        "binding_count": len(bindings),
    }


def _semantic_closure(
    product_mode: str,
    obligation_packet: dict[str, Any],
    realized_obligation_ids: list[str],
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Bind claimed obligation realization to deterministic semantic-role lineage."""
    projection = compile_semantic_projection(obligation_packet)
    realized_obligations = set(realized_obligation_ids)
    authorized_atoms = [row for row in projection["semantic_atoms"] if product_mode in row["authorized_modes"]]
    required_atoms = [row for row in authorized_atoms if row["direct"] and product_mode in row["required_realization_modes"]]
    realized_atoms = [row for row in authorized_atoms if row["source_obligation_id"] in realized_obligations]

    required_ids = {row["semantic_id"] for row in required_atoms}
    realized_ids = {row["semantic_id"] for row in realized_atoms}
    missing_required = sorted(required_ids - realized_ids)
    if missing_required:
        fail("CHEM_CORE_AUTH_REQUIRED_SEMANTIC_MISSING", ",".join(missing_required))
    realized_sources = {row["source_obligation_id"] for row in realized_atoms}
    missing_semantic_lineage = sorted(realized_obligations - realized_sources)
    if missing_semantic_lineage:
        fail("CHEM_CORE_AUTH_REALIZED_OBLIGATION_WITHOUT_SEMANTICS", ",".join(missing_semantic_lineage))

    return projection, {
        "status": "PASS",
        "authorized_semantic_ids": sorted(row["semantic_id"] for row in authorized_atoms),
        "required_semantic_ids": sorted(required_ids),
        "realized_semantic_ids": sorted(realized_ids),
        "realized_source_obligation_ids": sorted(realized_sources),
        "semantic_atom_count": len(realized_atoms),
    }


def _learner_gate_closure(
    product_mode: str,
    obligation_packet: dict[str, Any],
    semantic_projection: dict[str, Any],
    realized_obligation_ids: list[str],
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Bind Core realization to direct learner jobs without promoting prerequisite context."""
    projection = compile_learner_gate_projection(obligation_packet, semantic_projection=semantic_projection)
    realized_obligations = set(realized_obligation_ids)
    authorized_gates = [row for row in projection["learner_gates"] if product_mode in row["authorized_modes"]]
    required_gates = [row for row in authorized_gates if product_mode in row["required_realization_modes"]]
    realized_gates = [row for row in authorized_gates if row["source_obligation_id"] in realized_obligations]
    required_ids = {row["learner_gate_id"] for row in required_gates}
    realized_ids = {row["learner_gate_id"] for row in realized_gates}
    missing_required = sorted(required_ids - realized_ids)
    if missing_required:
        fail("CHEM_CORE_AUTH_REQUIRED_LEARNER_GATE_MISSING", ",".join(missing_required))

    semantic_by_id = {row["semantic_id"]: row for row in semantic_projection["semantic_atoms"]}
    context_ids = sorted(
        semantic_id for semantic_id in projection["context_semantic_ids"]
        if product_mode in semantic_by_id[semantic_id]["authorized_modes"]
    )
    metadata_ids = sorted(
        semantic_id for semantic_id in projection["metadata_semantic_ids"]
        if product_mode in semantic_by_id[semantic_id]["authorized_modes"]
    )
    realized_source_semantic_ids = {row["source_semantic_id"] for row in realized_gates}
    if set(context_ids) & realized_source_semantic_ids:
        fail("CHEM_CORE_AUTH_CONTEXT_PROMOTED_TO_LEARNER_GATE")

    return projection, {
        "status": "PASS",
        "authorized_learner_gate_ids": sorted(row["learner_gate_id"] for row in authorized_gates),
        "required_learner_gate_ids": sorted(required_ids),
        "realized_learner_gate_ids": sorted(realized_ids),
        "context_semantic_ids": context_ids,
        "metadata_semantic_ids": metadata_ids,
        "learner_gate_count": len(realized_gates),
    }


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
    unauthorized = sorted(oid for oid in realized if product_mode not in obligations[oid]["authorized_modes"])
    if unauthorized:
        fail("CHEM_CORE_AUTH_REALIZATION_UNAUTHORIZED", ",".join(unauthorized))

    required = {
        row["obligation_id"] for row in obligation_packet["obligations"]
        if row["direct"] and product_mode in row["required_realization_modes"]
    }
    missing = sorted(required - set(realized))
    if missing:
        fail("CHEM_CORE_AUTH_REQUIRED_OBLIGATION_MISSING", ",".join(missing))

    representation_closure = _representation_closure(product_mode, payload, obligation_packet, realized)
    semantic_projection, semantic_closure = _semantic_closure(product_mode, obligation_packet, realized)
    learner_gate_projection, learner_gate_closure = _learner_gate_closure(
        product_mode, obligation_packet, semantic_projection, realized
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
        "representation_closure": representation_closure,
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
