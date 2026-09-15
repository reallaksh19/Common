#!/usr/bin/env python3
"""Compile four-Core representation plans through the existing Chemistry C-H authority.

The renderer never chooses a visual. A product adapter must provide an explicit plan
that names the Engineering representation obligation, Chemistry capability and C-H
primitive. This compiler validates that plan against the Engineering obligation
packet, the existing primitive registry, page-intent profile and notation contract,
then emits the governed representation bundle consumed by learner-product renderers.
"""
from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CHEM_ROOT = ROOT.parent
sys.path.insert(0, str(CHEM_ROOT / "Representation" / "engine"))
sys.path.insert(0, str(ROOT / "engine"))

from build_chemistry_representations import (  # noqa: E402
    primitive_supports_capability,
    validate_notation,
    validate_registry,
)
from compile_chemistry_engineering_closure import load  # noqa: E402

PRIMITIVE_REGISTRY_REL = "../Representation/registry/chemistry-teaching-primitive-registry.json"
PAGE_INTENT_REL = "../Representation/registry/chemistry-page-intent-profile.json"
NOTATION_REL = "../Representation/registry/chemistry-notation-render-contract.json"


class ChemistryCoreRepresentationError(ValueError):
    def __init__(self, code: str, message: str = ""):
        super().__init__(f"{code}: {message}" if message else code)
        self.code = code
        self.message = message


def fail(code: str, message: str = "") -> None:
    raise ChemistryCoreRepresentationError(code, message)


def canonical(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(obj: Any, field: str | None = None) -> str:
    value = copy.deepcopy(obj)
    if field:
        value.pop(field, None)
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def _load_chem_relative(rel: str) -> dict[str, Any]:
    return json.loads((ROOT / rel).resolve().read_text(encoding="utf-8"))


def _authorized_representation_rows(packet: dict[str, Any], product_mode: str) -> list[dict[str, Any]]:
    return [
        row for row in packet.get("obligations", [])
        if row.get("kind") == "REPRESENTATION"
        and product_mode in row.get("authorized_modes", [])
    ]


def _allowed_primitives(capability_ref: str, primitive_by_id: dict[str, Any], profile: dict[str, Any]) -> set[str]:
    allowed = set(profile.get("primary_primitives_by_capability", {}).get(capability_ref, []))
    for primitive_id in profile.get("conditional_primitives", {}).values():
        primitive = primitive_by_id.get(primitive_id)
        if primitive and primitive_supports_capability(primitive, capability_ref):
            allowed.add(primitive_id)
    return allowed


def compile_core_representation_bundle(
    product_mode: str,
    obligation_packet: dict[str, Any],
    representation_plan: dict[str, Any],
    *,
    primitive_registry: dict[str, Any] | None = None,
    page_intent_profile: dict[str, Any] | None = None,
    notation_contract: dict[str, Any] | None = None,
    bundle_id: str,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    if product_mode not in {"CORE1A", "CORE1B", "CORE2A", "CORE2B"}:
        fail("CHEM_CORE_REP_MODE_INVALID", product_mode)
    if obligation_packet.get("status") != "BLUEPRINT_OBLIGATIONS_READY":
        fail("CHEM_CORE_REP_OBLIGATION_PACKET_NOT_READY")
    rows = representation_plan.get("representations")
    if not isinstance(rows, list):
        fail("CHEM_CORE_REP_PLAN_INVALID", "representations")

    primitive_registry = primitive_registry or _load_chem_relative(PRIMITIVE_REGISTRY_REL)
    page_intent_profile = page_intent_profile or _load_chem_relative(PAGE_INTENT_REL)
    notation_contract = notation_contract or _load_chem_relative(NOTATION_REL)
    primitive_by_id = validate_registry(primitive_registry)
    validate_notation(notation_contract)

    obligation_rows = _authorized_representation_rows(obligation_packet, product_mode)
    authorized = {str(row["asset_ref"]) for row in obligation_rows}
    required = {
        str(row["asset_ref"])
        for row in obligation_rows
        if row.get("direct") and product_mode in row.get("required_realization_modes", [])
    }

    compiled: list[dict[str, Any]] = []
    bindings: list[dict[str, Any]] = []
    covered: set[str] = set()
    seen_rep_ids: set[str] = set()
    for row in rows:
        if not isinstance(row, dict):
            fail("CHEM_CORE_REP_PLAN_INVALID", "row")
        rep_id = str(row.get("representation_id", "")).strip()
        capability_ref = str(row.get("capability_ref", "")).strip()
        primitive_id = str(row.get("primitive_id", "")).strip()
        engineering_refs = row.get("engineering_representation_refs")
        if not rep_id or not capability_ref or not primitive_id or not isinstance(engineering_refs, list) or not engineering_refs:
            fail("CHEM_CORE_REP_PLAN_INVALID", rep_id or "unnamed")
        if rep_id in seen_rep_ids:
            fail("CHEM_CORE_REP_ID_DUPLICATE", rep_id)
        seen_rep_ids.add(rep_id)
        engineering_refs = {str(value).strip() for value in engineering_refs if str(value).strip()}
        if not engineering_refs:
            fail("CHEM_CORE_REP_PLAN_INVALID", rep_id)
        unauthorized = sorted(engineering_refs - authorized)
        if unauthorized:
            fail("CHEM_CORE_REP_ENGINEERING_REF_UNAUTHORIZED", ",".join(unauthorized))

        primitive = primitive_by_id.get(primitive_id)
        if primitive is None:
            fail("CHEM_CORE_REP_PRIMITIVE_UNKNOWN", primitive_id)
        if not primitive_supports_capability(primitive, capability_ref):
            fail("CHEM_CORE_REP_CAPABILITY_PRIMITIVE_MISMATCH", f"{capability_ref}:{primitive_id}")
        allowed = _allowed_primitives(capability_ref, primitive_by_id, page_intent_profile)
        if primitive_id not in allowed:
            fail("CHEM_CORE_REP_PAGE_INTENT_REJECTED", f"{capability_ref}:{primitive_id}")

        semantic = row.get("source_semantic_data")
        if not isinstance(semantic, dict):
            fail("CHEM_CORE_REP_SEMANTIC_DATA_REQUIRED", rep_id)
        chemical_entities = list(row.get("chemical_entities") or semantic.get("chemical_entities") or [])
        condition_context = list(row.get("condition_exception_context") or semantic.get("condition_exception_context") or [])
        notation_tokens = list(row.get("notation_tokens") or chemical_entities)
        species_roles = list(row.get("species_roles") or [])
        renderer_constraints = sorted(set(list(primitive.get("renderer_constraints") or []) + ["NOTATION_CONTRACT:" + notation_contract["contract_id"]]))
        spec = {
            "representation_id": rep_id,
            "primitive_id": primitive_id,
            "capability_ref": capability_ref,
            "problem_family_ref": row.get("problem_family_ref"),
            "engineering_representation_refs": sorted(engineering_refs),
            "instructional_job": primitive["instructional_job"],
            "attention_target": primitive["attention_target"],
            "translation_obligation": primitive["translation_obligation"],
            "chemical_entities": chemical_entities,
            "species_roles": species_roles,
            "representation_level_from": primitive["representation_level_from"],
            "representation_level_to": primitive["representation_level_to"],
            "condition_exception_context": condition_context,
            "source_semantic_data": semantic,
            "learner_action_expected": primitive["learner_action"],
            "misconception_or_contrast_ref": row.get("misconception_or_contrast_ref"),
            "accessibility_text": row.get("accessibility_text") or primitive["accessibility_pattern"],
            "renderer_constraints": renderer_constraints,
            "notation_tokens": notation_tokens,
            "decorative": False,
        }
        compiled.append(spec)
        bindings.append({
            "representation_ref": rep_id,
            "engineering_representation_refs": sorted(engineering_refs),
        })
        covered.update(engineering_refs)

    missing = sorted(required - covered)
    if missing:
        fail("CHEM_CORE_REP_REQUIRED_ENGINEERING_REPRESENTATION_MISSING", ",".join(missing))

    bundle = {
        "bundle_id": bundle_id,
        "schema_version": "1.0.0",
        "subject": "CHEMISTRY",
        "product_mode": product_mode,
        "obligation_packet_ref": obligation_packet["packet_id"],
        "primitive_registry_ref": primitive_registry["registry_id"],
        "page_intent_profile_ref": page_intent_profile["profile_id"],
        "notation_contract_ref": notation_contract["contract_id"],
        "representations": compiled,
        "summary": {
            "representation_count": len(compiled),
            "engineering_representation_count": len(covered),
            "required_engineering_representation_count": len(required),
            "renderer_selection_allowed": False,
        },
        "bundle_digest": "",
    }
    bundle["bundle_digest"] = digest(bundle, "bundle_digest")
    return bundle, bindings
