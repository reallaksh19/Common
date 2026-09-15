#!/usr/bin/env python3
"""Redox Core1A stress-boundary proof for Chemistry Workbench v2.

This is intentionally NOT a learner-product renderer while the only current Redox
source audit is STRESS_TEST_SOURCE_AUDIT. It re-reads current Blueprint authority,
validates the stress audit, attempts product source-scope authorization, and
requires the Workbench v2 firewall to block before any PDF is emitted.

A future learner-product build requires a separately authorized
PRODUCTION_SOURCE_AUDIT. This stress harness must never manufacture that authority.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[5]
BP = ROOT / "Grade 9" / "V2" / "Chemistry" / "LearningBlueprint"
sys.path.insert(0, str(BP / "engine"))

from validate_chemistry_gate_source_audit import validate as validate_source_audit  # noqa: E402
from validate_product_source_scope import (  # noqa: E402
    ChemistryProductSourceScopeError,
    digest,
    validate_product_source_scope,
)

AUTHORITY_REL = "golden/v7/core1a-study-note-redox-authority.json"
CCBOM_REL = "golden/v7/ccbom-redox.json"
TTU_REL = "golden/v5/core1a-hard-study-product.json"
SDU_REL = "golden/v6/sdu-hard-redox.json"
CONCEPT_TTU_REL = "golden/v6/concept-ttu-core1a-redox.json"
SELF_HELP_REL = "golden/v6/self-help-core1a-redox.json"
STUDY_POLICY_REL = "policies/v7-core1a-study-note-sufficiency-policy.json"
REGISTRY_REL = "policies/chemistry-technical-engineering-gates.v1.json"
STRESS_AUDIT_REL = "stress_tests/redox/source-audit.v2.json"
EXPECTED_BLOCKER = "CHEM_PRODUCT_SCOPE_STRESS_AUDIT_NOT_AUTHORITY"


def load(rel: str) -> dict[str, Any]:
    return json.loads((BP / rel).read_text(encoding="utf-8"))


def sha(obj: Any) -> str:
    raw = json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return "sha256:" + hashlib.sha256(raw).hexdigest()


def scope_attempt(authority: dict[str, Any], audit: dict[str, Any]) -> dict[str, Any]:
    """Construct a schema-valid request to exercise the product-authority firewall.

    The values below do not grant authority. They merely make the attempted
    contract structurally complete so failure occurs for the correct reason:
    a stress audit cannot authorize a learner product.
    """
    tiers = [row["tier_id"] for row in audit["scope_tiers"]]
    held = [row["tier_id"] for row in audit["scope_tiers"] if row["tier_id"] == "EXTENDED_G11"]
    authorized = [tier for tier in tiers if tier not in held]
    if not authorized:
        authorized = tiers[:1]
        held = tiers[1:]

    atom_ids = [row["atom_id"] for row in authority["learning_atoms"]]
    assignments = []
    for index, atom_id in enumerate(atom_ids):
        tier = authorized[0] if index == 0 else authorized[-1]
        assignments.append({"learning_atom_id": atom_id, "scope_tier": tier})

    guards = []
    for row in audit["asset_bindings"]:
        if row["asset_kind"] == "TRANSFORMATION" and row["scope_tier_id"] in set(held):
            guards.append({
                "fingerprint": row["asset_ref"],
                "detection_tokens": ["permanganate", "MnO4", "acidic medium"],
            })

    return {
        "schema_version": "2.0.0",
        "scope_contract_id": "CHEM-PRODUCT-SCOPE-REDOX-STRESS-ATTEMPT-V2",
        "gate_id": audit["gate_id"],
        "subtopic_id": authority["subtopic_id"],
        "source_audit_ref": STRESS_AUDIT_REL,
        "source_audit_digest": digest(audit),
        "learner_grade": 9,
        "program_context": "COMPETITIVE_FOUNDATION_EXTENSION",
        "authorized_scope_tiers": authorized,
        "held_scope_tiers": held,
        "extension_authority_ref": "STRESS_ATTEMPT_ONLY_NO_AUTHORITY_EFFECT",
        "extension_reason": "Schema-complete negative proof only; no source or product authority is granted.",
        "learning_atom_scope_assignments": assignments,
        "held_transformation_guards": guards,
        "status": "SCOPE_CONTRACT_READY",
    }


def build_receipt(out_receipt: Path) -> dict[str, Any]:
    authority = load(AUTHORITY_REL)
    ccbom = load(CCBOM_REL)
    ttu_doc = load(TTU_REL)
    sdu = load(SDU_REL)
    concept_ttu = load(CONCEPT_TTU_REL)
    self_help = load(SELF_HELP_REL)
    study_policy = load(STUDY_POLICY_REL)
    registry = load(REGISTRY_REL)
    audit = load(STRESS_AUDIT_REL)

    audit_result = validate_source_audit(audit, registry)
    if audit_result["status"] != "PASS":
        raise RuntimeError("Redox stress source audit did not validate")
    if audit_result["audit_role"] != "STRESS_TEST_SOURCE_AUDIT":
        raise RuntimeError("Redox fixture unexpectedly carries production source authority")
    if audit_result["authority_effect"] != "NONE_STRESS_TEST_ONLY":
        raise RuntimeError("Redox stress audit authority effect drifted")

    required_ttu_ids = set(authority["reconstructable_ttu_refs"])
    serialized_ttu_ids = {row["ttu_id"] for row in ttu_doc.get("reconstructable_ttus", [])}
    missing_ttus = sorted(required_ttu_ids - serialized_ttu_ids)
    if missing_ttus:
        raise RuntimeError(f"Current Blueprint reconstructable TTUs missing: {missing_ttus}")

    attempt = scope_attempt(authority, audit)
    blocker_code = None
    blocker_message = None
    try:
        validate_product_source_scope(attempt, audit, authority, registry)
    except ChemistryProductSourceScopeError as exc:
        blocker_code = exc.code
        blocker_message = exc.message
    else:
        raise RuntimeError("STRESS_AUDIT_UNEXPECTEDLY_AUTHORIZED_LEARNER_PRODUCT")

    if blocker_code != EXPECTED_BLOCKER:
        raise RuntimeError(f"Unexpected product-authority blocker: {blocker_code}: {blocker_message}")

    receipt = {
        "schema_version": "1.0.0",
        "proof_id": "CHEM-REDOX-CORE1A-STRESS-BOUNDARY-v2",
        "status": "EXPECTED_BLOCK_CONFIRMED",
        "product_mode": "CORE1A",
        "product_emitted": False,
        "pdf_emitted": False,
        "workbench_version": "V2",
        "stress_topic": "REDOX",
        "stress_authority_status": "NON_AUTHORITATIVE_FIXTURE",
        "source_audit": {
            "audit_id": audit["audit_id"],
            "audit_role": audit_result["audit_role"],
            "authority_effect": audit_result["authority_effect"],
            "audit_status": audit_result["audit_status"],
            "gate_id": audit_result["gate_id"],
            "digest": sha(audit),
        },
        "expected_blocker": EXPECTED_BLOCKER,
        "observed_blocker": blocker_code,
        "blocker_message": blocker_message,
        "scope_attempt_digest": sha(attempt),
        "current_blueprint": {
            "authority_id": authority["authority_id"],
            "authority_digest": sha(authority),
            "subtopic_id": authority["subtopic_id"],
            "difficulty_badge": authority["difficulty_badge"],
            "learning_atom_count": len(authority["learning_atoms"]),
            "content_object_count": len(authority["content_objects"]),
            "ccbom_id": ccbom["ccbom_id"],
            "ccbom_digest": sha(ccbom),
            "sdu_digest": sha(sdu),
            "concept_ttu_id": concept_ttu["ttu_id"],
            "concept_ttu_digest": sha(concept_ttu),
            "self_help_closure_id": self_help["closure_id"],
            "self_help_digest": sha(self_help),
            "study_policy_id": study_policy["policy_id"],
            "study_policy_digest": sha(study_policy),
            "required_reconstructable_ttu_ids": sorted(required_ttu_ids),
            "serialized_reconstructable_ttu_ids": sorted(serialized_ttu_ids),
        },
        "release_condition": "NO_LEARNER_PRODUCT_RENDER_UNTIL_EXPLICIT_PRODUCTION_SOURCE_AUDIT_EXISTS",
        "historical_v1_authority_used": False,
    }
    out_receipt.parent.mkdir(parents=True, exist_ok=True)
    out_receipt.write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return receipt


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", default=str(HERE / "out" / "core1a_redox_stress_receipt.json"))
    args = parser.parse_args()
    receipt = build_receipt(Path(args.receipt))
    print(json.dumps({
        "status": receipt["status"],
        "observed_blocker": receipt["observed_blocker"],
        "product_emitted": receipt["product_emitted"],
        "receipt": args.receipt,
    }, indent=2))


if __name__ == "__main__":
    main()
