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

from compile_chemistry_engineering_authorization_binding import compile_binding  # noqa: E402
from compile_chemistry_engineering_closure import compile_closure, digest, load  # noqa: E402
from validate_chemistry_gate_source_audit import transformation_ref  # noqa: E402

POLICY_REL = "policies/engineering-blueprint-compilation.v1.json"
SCHEMA_REL = "contracts/chemistry-engineering-blueprint-obligations.schema.json"
TOPOLOGY_LINEAGE_FIELDS = (
    "topology_id",
    "topology_digest",
    "topology_extension_id",
    "topology_extension_digest",
)


class ChemistryBlueprintObligationError(ValueError):
    def __init__(self, code: str, message: str = ""):
        super().__init__(f"{code}: {message}" if message else code)
        self.code = code
        self.message = message


def fail(code: str, message: str = "") -> None:
    raise ChemistryBlueprintObligationError(code, message)


def _canonical(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _packet_digest(packet: dict[str, Any]) -> str:
    payload = copy.deepcopy(packet)
    payload.pop("packet_digest", None)
    return "sha256:" + hashlib.sha256(_canonical(payload).encode("utf-8")).hexdigest()


def _obligation_id(gate_id: str, kind: str, asset_ref: str) -> str:
    seed = f"{gate_id}|{kind}|{asset_ref}".encode("utf-8")
    return "CHEM-OBL-" + hashlib.sha256(seed).hexdigest()[:24].upper()


def _row(
    gate: dict[str, Any],
    direct: bool,
    kind: str,
    asset_ref: str,
    payload: dict[str, Any],
    policy: dict[str, Any],
    *,
    target_mode: str | None = None,
) -> dict[str, Any]:
    defaults = policy["kind_defaults"][kind]
    authorized = list(defaults["authorized_modes"])
    required = list(defaults["required_direct_modes"]) if direct else []
    if kind == "TRANSFORMATION":
        if target_mode is None:
            fail("CHEM_BP_OBL_TRANSFORMATION_TARGET_MISSING", asset_ref)
        authorized = [target_mode]
        required = []
    return {
        "obligation_id": _obligation_id(gate["subtopic_id"], kind, asset_ref),
        "gate_id": gate["subtopic_id"],
        "direct": direct,
        "kind": kind,
        "asset_ref": asset_ref,
        "authorized_modes": authorized,
        "required_realization_modes": required,
        "source_authority_tier": gate["authority_tier"],
        "payload": copy.deepcopy(payload),
    }


def _gate_obligations(gate: dict[str, Any], direct: bool, policy: dict[str, Any]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for item in gate["technical_core"]:
        out.append(_row(gate, direct, "CONCEPT", item["concept_id"], item, policy))
    for item in gate["mandatory_equations"]:
        out.append(_row(gate, direct, "EQUATION", item["equation_id"], item, policy))
    for item in gate["representations"]:
        out.append(_row(gate, direct, "REPRESENTATION", item["representation_id"], item, policy))
    for index, item in enumerate(gate["model_conditions"], 1):
        out.append(_row(gate, direct, "MODEL_CONDITION", f"MODEL-CONDITION-{index:02d}", item, policy))
    for item in gate["reasoning_sequence"]:
        out.append(_row(gate, direct, "REASONING_STEP", f"REASONING-{int(item['step']):02d}", item, policy))
    role_map = policy["core_role_map"]
    for item in gate["required_transformations"]:
        role = item["target_core_role"]
        if role not in role_map:
            fail("CHEM_BP_OBL_UNKNOWN_CORE_ROLE", role)
        out.append(_row(gate, direct, "TRANSFORMATION", transformation_ref(item), item, policy, target_mode=role_map[role]))
    for item in gate["misconceptions"]:
        out.append(_row(gate, direct, "MISCONCEPTION", item["misconception_id"], item, policy))
    for index, statement in enumerate(gate["mandatory_verifications"], 1):
        out.append(_row(gate, direct, "VERIFICATION", f"VERIFICATION-{index:02d}", {"statement": statement}, policy))
    for item in gate["problem_families"]:
        out.append(_row(gate, direct, "PROBLEM_FAMILY", item["family_id"], item, policy))
    out.append(_row(gate, direct, "DIFFICULTY_PROFILE", "DIFFICULTY-PROFILE", gate["difficulty_profile"], policy))
    return out


def compile_blueprint_obligations(
    request: dict[str, Any],
    manifest: dict[str, Any],
    *,
    registry: dict[str, Any] | None = None,
    topology_extension: dict[str, Any] | None = None,
    source_audit_payloads: dict[str, dict[str, Any]] | None = None,
    research_dossier: dict[str, Any] | None = None,
    claim_ledger: dict[str, Any] | None = None,
) -> dict[str, Any]:
    closure_kwargs = {
        "registry": registry,
        "topology_extension": topology_extension,
        "source_audit_payloads": source_audit_payloads,
        "research_dossier": research_dossier,
        "claim_ledger": claim_ledger,
    }
    receipt = compile_closure(request, manifest, **closure_kwargs)
    if receipt["closure_status"] != "READY":
        fail("CHEM_BP_OBL_ENGINEERING_NOT_READY", ",".join(row["code"] for row in receipt["blockers"]))
    binding = compile_binding(request, manifest, **closure_kwargs)
    if binding["closure_digest"] != receipt["closure_digest"]:
        fail("CHEM_BP_OBL_CLOSURE_BINDING_DRIFT")
    if any(field in receipt for field in TOPOLOGY_LINEAGE_FIELDS):
        if any(binding.get(field) != receipt.get(field) for field in TOPOLOGY_LINEAGE_FIELDS):
            fail("CHEM_BP_OBL_TOPOLOGY_BINDING_DRIFT")

    current_registry = registry if registry is not None else load(manifest["registry_ref"])
    if digest(current_registry) != receipt["registry_digest"]:
        fail("CHEM_BP_OBL_REGISTRY_DRIFT")
    gate_map = {row["subtopic_id"]: row for row in current_registry["subtopic_gates"]}
    policy = load(POLICY_REL)
    if policy.get("policy_id") != "CHEM-ENGINEERING-BLUEPRINT-COMPILATION-v1":
        fail("CHEM_BP_OBL_POLICY_INVALID")

    direct = set(receipt["direct_gate_ids"])
    obligations: list[dict[str, Any]] = []
    for gate_id in receipt["closure_gate_ids"]:
        gate = gate_map.get(gate_id)
        if gate is None:
            fail("CHEM_BP_OBL_GATE_MISSING", gate_id)
        obligations.extend(_gate_obligations(gate, gate_id in direct, policy))

    ids = [row["obligation_id"] for row in obligations]
    if len(ids) != len(set(ids)):
        fail("CHEM_BP_OBL_ID_COLLISION")

    modes = policy["product_modes"]
    required_by_mode = {
        mode: sum(mode in row["required_realization_modes"] for row in obligations)
        for mode in modes
    }
    packet = {
        "schema_version": "1.0.0",
        "packet_id": manifest["manifest_id"].replace("CHEM-ENG-MAN-", "CHEM-BP-OBL-", 1),
        "subject": "CHEMISTRY",
        "request_id": request["request_id"],
        "manifest_id": manifest["manifest_id"],
        "scope_ref": manifest["scope_ref"],
        "engineering_binding_id": binding["binding_id"],
        "engineering_binding_digest": digest(binding),
        "closure_receipt_id": receipt["receipt_id"],
        "closure_digest": receipt["closure_digest"],
        "registry_ref": receipt["registry_ref"],
        "registry_digest": receipt["registry_digest"],
        "direct_gate_ids": receipt["direct_gate_ids"],
        "closure_gate_ids": receipt["closure_gate_ids"],
        "obligations": obligations,
        "counts": {
            "gate_count": len(receipt["closure_gate_ids"]),
            "direct_gate_count": len(receipt["direct_gate_ids"]),
            "obligation_count": len(obligations),
            "required_by_mode": required_by_mode,
        },
        "status": "BLUEPRINT_OBLIGATIONS_READY",
        "packet_digest": "",
    }
    if "topology_id" in receipt:
        packet.update({field: receipt[field] for field in TOPOLOGY_LINEAGE_FIELDS})
    packet["packet_digest"] = _packet_digest(packet)
    try:
        jsonschema.validate(packet, load(SCHEMA_REL))
    except jsonschema.ValidationError as exc:
        fail("CHEM_BP_OBL_SCHEMA", exc.message)
    return packet


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("request")
    parser.add_argument("manifest")
    parser.add_argument("--out")
    args = parser.parse_args()
    packet = compile_blueprint_obligations(load(args.request), load(args.manifest))
    text = json.dumps(packet, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
