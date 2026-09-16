#!/usr/bin/env python3
"""Compile four-Core representation bundles from governed representation intents.

Scientific representation semantics are compiled upstream from Engineering authority.
Primitive/capability selection is compiled upstream from the C-H page-intent authority.
Structured primitive runtime facts are resolved from source-bound C-H fact authority.
This compiler accepts only a validated representation-intent packet and a set of intent
references selected for realization. It does not accept adapter-authored primitive IDs,
capabilities, scientific semantic payloads, or primitive runtime fact payloads.
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
    validate_notation,
    validate_registry,
)
from compile_chemistry_representation_intent import (  # noqa: E402
    compile_representation_intent,
    validate_representation_intent,
)
from compile_chemistry_representation_runtime_facts import (  # noqa: E402
    ChemistryRepresentationRuntimeFactsError,
    compile_runtime_fact_authority,
    resolve_runtime_fact_parameters,
)

PRIMITIVE_REGISTRY_REL = "../Representation/registry/chemistry-teaching-primitive-registry.json"
PAGE_INTENT_REL = "../Representation/registry/chemistry-page-intent-profile.json"
NOTATION_REL = "../Representation/registry/chemistry-notation-render-contract.json"
DEFAULT_EXTENSION_RELS = (
    "../Representation/registry/chemistry-electron-transfer-primitive-extension.v1.json",
)
DEFAULT_INTENT_EXTENSION_RELS = (
    "../Representation/registry/chemistry-electron-transfer-intent-extension.v1.json",
)


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


def _apply_extensions(
    primitive_registry: dict[str, Any],
    page_intent_profile: dict[str, Any],
    extensions: list[dict[str, Any]],
) -> tuple[dict[str, Any], dict[str, Any], list[str]]:
    registry = copy.deepcopy(primitive_registry)
    profile = copy.deepcopy(page_intent_profile)
    primitive_ids = {str(row.get("primitive_id")) for row in registry.get("primitives", [])}
    conditional = profile.setdefault("conditional_primitives", {})
    extension_refs: list[str] = []
    for extension in extensions:
        extension_id = str(extension.get("extension_id", "")).strip()
        if not extension_id or extension.get("subject") != "CHEMISTRY":
            fail("CHEM_CORE_REP_EXTENSION_INVALID", extension_id or "unnamed")
        if extension.get("extends_primitive_registry") != registry.get("registry_id"):
            fail("CHEM_CORE_REP_EXTENSION_REGISTRY_DRIFT", extension_id)
        if extension.get("extends_page_intent_profile") != profile.get("profile_id"):
            fail("CHEM_CORE_REP_EXTENSION_PAGE_INTENT_DRIFT", extension_id)
        if extension.get("renderer_selection_forbidden") is not True:
            fail("CHEM_CORE_REP_EXTENSION_RENDERER_SELECTION_FORBIDDEN", extension_id)
        rows = extension.get("primitives")
        additions = extension.get("conditional_primitives")
        if not isinstance(rows, list) or not isinstance(additions, dict):
            fail("CHEM_CORE_REP_EXTENSION_INVALID", extension_id)
        for primitive in rows:
            primitive_id = str(primitive.get("primitive_id", "")).strip() if isinstance(primitive, dict) else ""
            if not primitive_id:
                fail("CHEM_CORE_REP_EXTENSION_INVALID", extension_id)
            if primitive_id in primitive_ids:
                fail("CHEM_CORE_REP_EXTENSION_PRIMITIVE_OVERRIDE", primitive_id)
            registry.setdefault("primitives", []).append(copy.deepcopy(primitive))
            primitive_ids.add(primitive_id)
        for key, primitive_id in additions.items():
            if key in conditional:
                fail("CHEM_CORE_REP_EXTENSION_PAGE_INTENT_OVERRIDE", str(key))
            if primitive_id not in primitive_ids:
                fail("CHEM_CORE_REP_EXTENSION_PAGE_INTENT_UNKNOWN", str(primitive_id))
            conditional[str(key)] = str(primitive_id)
        extension_refs.append(extension_id)
    return registry, profile, extension_refs


def _resolved_authority(
    *,
    primitive_registry: dict[str, Any] | None = None,
    page_intent_profile: dict[str, Any] | None = None,
    notation_contract: dict[str, Any] | None = None,
    representation_extensions: list[dict[str, Any]] | None = None,
    representation_intent_extensions: list[dict[str, Any]] | None = None,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], list[str], list[dict[str, Any]]]:
    registry = primitive_registry or _load_chem_relative(PRIMITIVE_REGISTRY_REL)
    profile = page_intent_profile or _load_chem_relative(PAGE_INTENT_REL)
    notation = notation_contract or _load_chem_relative(NOTATION_REL)
    primitive_extensions = representation_extensions
    if primitive_extensions is None:
        primitive_extensions = [_load_chem_relative(rel) for rel in DEFAULT_EXTENSION_RELS]
    registry, profile, extension_refs = _apply_extensions(registry, profile, primitive_extensions)
    validate_registry(registry)
    validate_notation(notation)
    intent_extensions = representation_intent_extensions
    if intent_extensions is None:
        intent_extensions = [_load_chem_relative(rel) for rel in DEFAULT_INTENT_EXTENSION_RELS]
    return registry, profile, notation, extension_refs, intent_extensions


def compile_core_representation_intent(
    product_mode: str,
    obligation_packet: dict[str, Any],
    *,
    primitive_registry: dict[str, Any] | None = None,
    page_intent_profile: dict[str, Any] | None = None,
    notation_contract: dict[str, Any] | None = None,
    representation_extensions: list[dict[str, Any]] | None = None,
    representation_intent_extensions: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    registry, profile, _notation, _extension_refs, intent_extensions = _resolved_authority(
        primitive_registry=primitive_registry,
        page_intent_profile=page_intent_profile,
        notation_contract=notation_contract,
        representation_extensions=representation_extensions,
        representation_intent_extensions=representation_intent_extensions,
    )
    try:
        return compile_representation_intent(
            product_mode,
            obligation_packet,
            primitive_registry=registry,
            page_intent_profile=profile,
            representation_intent_extensions=intent_extensions,
        )
    except Exception as exc:
        fail("CHEM_CORE_REP_INTENT_COMPILE_FAILED", str(exc))


def _intent_map(intent_packet: dict[str, Any]) -> dict[str, dict[str, Any]]:
    rows = intent_packet.get("intents")
    if not isinstance(rows, list):
        fail("CHEM_CORE_REP_INTENT_PACKET_INVALID", "intents")
    out: dict[str, dict[str, Any]] = {}
    for row in rows:
        intent_id = str(row.get("intent_id", "")).strip() if isinstance(row, dict) else ""
        if not intent_id or intent_id in out:
            fail("CHEM_CORE_REP_INTENT_PACKET_INVALID", intent_id or "duplicate/unnamed")
        out[intent_id] = row
    return out


def compile_core_representation_bundle(
    product_mode: str,
    obligation_packet: dict[str, Any],
    intent_packet: dict[str, Any],
    realized_intent_ids: list[str],
    *,
    primitive_registry: dict[str, Any] | None = None,
    page_intent_profile: dict[str, Any] | None = None,
    notation_contract: dict[str, Any] | None = None,
    representation_extensions: list[dict[str, Any]] | None = None,
    representation_intent_extensions: list[dict[str, Any]] | None = None,
    bundle_id: str,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    if product_mode not in {"CORE1A", "CORE1B", "CORE2A", "CORE2B"}:
        fail("CHEM_CORE_REP_MODE_INVALID", product_mode)
    if obligation_packet.get("status") != "BLUEPRINT_OBLIGATIONS_READY":
        fail("CHEM_CORE_REP_OBLIGATION_PACKET_NOT_READY")

    registry, profile, notation, extension_refs, intent_extensions = _resolved_authority(
        primitive_registry=primitive_registry,
        page_intent_profile=page_intent_profile,
        notation_contract=notation_contract,
        representation_extensions=representation_extensions,
        representation_intent_extensions=representation_intent_extensions,
    )
    try:
        validate_representation_intent(
            product_mode,
            obligation_packet,
            intent_packet,
            primitive_registry=registry,
            page_intent_profile=profile,
            representation_intent_extensions=intent_extensions,
        )
    except Exception as exc:
        fail("CHEM_CORE_REP_INTENT_PACKET_INVALID", str(exc))

    intents = _intent_map(intent_packet)
    realized = [str(value).strip() for value in realized_intent_ids if str(value).strip()]
    if len(realized) != len(realized_intent_ids) or len(realized) != len(set(realized)):
        fail("CHEM_CORE_REP_REALIZATION_INVALID", "empty or duplicate intent ref")
    unknown = sorted(set(realized) - set(intents))
    if unknown:
        fail("CHEM_CORE_REP_INTENT_UNKNOWN", ",".join(unknown))
    required = {intent_id for intent_id, row in intents.items() if row.get("required_realization") is True}
    missing = sorted(required - set(realized))
    if missing:
        fail("CHEM_CORE_REP_REQUIRED_INTENT_MISSING", ",".join(missing))

    try:
        runtime_fact_authority = compile_runtime_fact_authority()
    except ChemistryRepresentationRuntimeFactsError as exc:
        fail(exc.code, exc.message)

    compiled: list[dict[str, Any]] = []
    bindings: list[dict[str, Any]] = []
    runtime_fact_count = 0
    for intent_id in realized:
        row = intents[intent_id]
        primitive_id = row["primitive_id"]
        primitive = next((item for item in registry["primitives"] if item["primitive_id"] == primitive_id), None)
        if primitive is None:
            fail("CHEM_CORE_REP_PRIMITIVE_UNKNOWN", primitive_id)
        try:
            runtime_fact = resolve_runtime_fact_parameters(
                row,
                obligation_packet,
                primitive,
                runtime_fact_authority,
            )
        except ChemistryRepresentationRuntimeFactsError as exc:
            fail(exc.code, exc.message)
        scientific = copy.deepcopy(row["scientific_semantics"])
        renderer_constraints = sorted(
            set(list(row["primitive_authority"]["renderer_constraints"]) + ["NOTATION_CONTRACT:" + notation["contract_id"]])
        )
        spec = {
            "representation_id": "REP-REALIZED-" + intent_id.removeprefix("CHEM-REP-INTENT-"),
            "intent_ref": intent_id,
            "primitive_id": primitive_id,
            "capability_ref": row["capability_ref"],
            "engineering_representation_refs": [row["source_representation_ref"]],
            "instructional_job": row["primitive_authority"]["instructional_job"],
            "attention_target": row["primitive_authority"]["attention_target"],
            "translation_obligation": row["primitive_authority"]["translation_obligation"],
            "scientific_semantics": scientific,
            "learner_action_expected": row["primitive_authority"]["learner_action"],
            "accessibility_text": primitive["accessibility_pattern"],
            "renderer_constraints": renderer_constraints,
            "decorative": False,
        }
        if runtime_fact is not None:
            spec["runtime_fact_ref"] = runtime_fact["fact_packet_ref"]
            spec["runtime_fact_digest"] = runtime_fact["fact_packet_digest"]
            spec["runtime_fact_kind"] = runtime_fact["fact_kind"]
            spec["runtime_fact_source_equation_refs"] = runtime_fact["source_equation_refs"]
            spec["runtime_parameters"] = runtime_fact["parameters"]
            runtime_fact_count += 1
        compiled.append(spec)
        bindings.append({
            "representation_ref": spec["representation_id"],
            "intent_ref": intent_id,
            "engineering_representation_refs": [row["source_representation_ref"]],
            "source_obligation_id": row["source_obligation_id"],
        })

    bundle = {
        "bundle_id": bundle_id,
        "schema_version": "2.0.0",
        "subject": "CHEMISTRY",
        "product_mode": product_mode,
        "obligation_packet_ref": obligation_packet["packet_id"],
        "representation_intent_ref": intent_packet["intent_packet_id"],
        "representation_intent_digest": intent_packet["intent_packet_digest"],
        "primitive_registry_ref": registry["registry_id"],
        "primitive_registry_extension_refs": extension_refs,
        "representation_intent_extension_refs": list(intent_packet.get("policy_extension_refs", [])),
        "runtime_fact_extension_refs": list(runtime_fact_authority["extension_refs"]),
        "page_intent_profile_ref": profile["profile_id"],
        "notation_contract_ref": notation["contract_id"],
        "representations": compiled,
        "summary": {
            "representation_count": len(compiled),
            "realized_intent_count": len(realized),
            "required_intent_count": len(required),
            "representation_extension_count": len(extension_refs),
            "representation_intent_extension_count": len(intent_packet.get("policy_extension_refs", [])),
            "runtime_fact_count": runtime_fact_count,
            "adapter_primitive_selection_allowed": False,
            "adapter_scientific_semantics_allowed": False,
            "adapter_runtime_facts_allowed": False,
            "renderer_selection_allowed": False,
        },
        "bundle_digest": "",
    }
    bundle["bundle_digest"] = digest(bundle, "bundle_digest")
    return bundle, bindings
