#!/usr/bin/env python3
"""Redox end-to-end stress through governed four-Core representation authority.

This is topic-specific fixture orchestration only. It reuses the existing Redox semantic
payload adapters, but representation realization is compiled directly from Engineering
obligations plus generic C-H authority. The fixture nominates only the existing Blueprint
semantic authority; it does not select a primitive, author scientific representation
semantics, select a fact packet, or inject primitive runtime facts.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import build_redox_four_core_stress as fixture
from compile_chemistry_core_representation_bundle import (  # noqa: E402
    compile_core_representation_bundle,
    compile_core_representation_intent,
)

REP_INTENT_POLICY_REL = "policies/chemistry-representation-intent.v1.json"
RUNTIME_FACT_SCHEMA_REL = "contracts/chemistry-representation-runtime-facts.schema.json"
PRIMITIVE_REGISTRY_REL = "../Representation/registry/chemistry-teaching-primitive-registry.json"
PAGE_INTENT_REL = "../Representation/registry/chemistry-page-intent-profile.json"
NOTATION_REL = "../Representation/registry/chemistry-notation-render-contract.json"
REP_INTENT_EXTENSION_REL = "../Representation/registry/chemistry-electron-transfer-intent-extension.v1.json"
RUNTIME_FACT_EXTENSION_REL = "../Representation/registry/chemistry-electron-transfer-runtime-facts.v1.json"


def _governed_representation(
    mode: str,
    packet: dict[str, Any],
    semantic_authority: dict[str, Any],
) -> tuple[dict[str, Any], list[dict[str, Any]], str]:
    intent_packet = compile_core_representation_intent(mode, packet)
    direct = [row for row in intent_packet["intents"] if row.get("direct") is True]
    if not direct:
        raise ValueError(f"REDOX_STRESS_GOVERNED_DIRECT_REPRESENTATION_REQUIRED:{mode}")

    ordered = sorted(
        direct,
        key=lambda row: (not bool(row.get("required_realization")), row["intent_id"]),
    )
    realized_intent_ids = [row["intent_id"] for row in ordered]
    authority_ref = semantic_authority["authority_id"]
    bundle, bindings = compile_core_representation_bundle(
        mode,
        packet,
        intent_packet,
        realized_intent_ids,
        semantic_instance_authorities={authority_ref: semantic_authority},
        semantic_instance_authority_refs=[authority_ref],
        bundle_id=f"CHEM-REDOX-FOUR-CORE-STRESS-REP-BUNDLE-{mode}",
    )
    rows = bundle.get("representations") or []
    if not rows:
        raise ValueError(f"REDOX_STRESS_GOVERNED_REPRESENTATION_BUNDLE_EMPTY:{mode}")
    summary = bundle["summary"]
    if summary.get("adapter_primitive_selection_allowed") is not False:
        raise ValueError("REDOX_STRESS_ADAPTER_PRIMITIVE_AUTHORITY_REOPENED")
    if summary.get("adapter_scientific_semantics_allowed") is not False:
        raise ValueError("REDOX_STRESS_ADAPTER_SCIENCE_AUTHORITY_REOPENED")
    if summary.get("adapter_runtime_facts_allowed") is not False:
        raise ValueError("REDOX_STRESS_ADAPTER_RUNTIME_FACT_AUTHORITY_REOPENED")
    runtime_rows = [row for row in rows if row.get("runtime_fact_ref")]
    if not runtime_rows:
        raise ValueError(f"REDOX_STRESS_GOVERNED_RUNTIME_FACT_REQUIRED:{mode}")
    for row in runtime_rows:
        if row.get("runtime_fact_source_authority_kind") != "BLUEPRINT_CONTENT_AUTHORITY":
            raise ValueError(f"REDOX_STRESS_LOCAL_SEMANTIC_AUTHORITY_REQUIRED:{mode}")
        if row.get("runtime_fact_source_authority_ref") != authority_ref:
            raise ValueError(f"REDOX_STRESS_LOCAL_SEMANTIC_AUTHORITY_DRIFT:{mode}")
        if not row.get("semantic_instance_ref"):
            raise ValueError(f"REDOX_STRESS_LOCAL_SEMANTIC_INSTANCE_REQUIRED:{mode}")
    return bundle, bindings, rows[0]["capability_ref"]


def build_stress(out_dir: Path, *, render: bool = False) -> dict[str, Any]:
    out_dir.mkdir(parents=True, exist_ok=True)
    registry = fixture.load(fixture.REGISTRY_REL)
    audit = fixture.load(fixture.AUDIT_REL)
    scope_fixture = fixture.load(fixture.SCOPE_FIXTURE_REL)
    authority_v7 = fixture.load(fixture.AUTHORITY_REL)
    hard_bucket = fixture.load(fixture.HARD_BUCKET_REL)
    c1a_ttu = fixture.load(fixture.C1A_TTU_REL)
    c1b_ttu = fixture.load(fixture.C1B_TTU_REL)
    c1b_dialogue = fixture.load(fixture.C1B_DIALOGUE_REL)
    c2a_ttu = fixture.load(fixture.C2A_TTU_REL)
    c2b_ttu = fixture.load(fixture.C2B_TTU_REL)
    c2b_dialogue = fixture.load(fixture.C2B_DIALOGUE_REL)
    lau = fixture.load(fixture.LAU_REL)
    c2a_product = fixture.load(fixture.C2A_PRODUCT_REL)
    c2b_product = fixture.load(fixture.C2B_PRODUCT_REL)

    if scope_fixture.get("stress_only") is not True:
        raise ValueError("REDOX_STRESS_FIXTURE_MUST_BE_STRESS_ONLY")
    if audit["audit_role"] != "PRODUCTION_SOURCE_AUDIT":
        raise ValueError("REDOX_STRESS_PRODUCTION_AUDIT_REQUIRED")
    gate = fixture.gate_map(registry)[audit["gate_id"]]
    if gate["technical_readiness"] != "ENGINEERING_GATE_READY":
        raise ValueError("REDOX_STRESS_ENGINEERING_GATE_NOT_READY")

    request = fixture.make_request()
    manifest = fixture.make_manifest(registry, audit, authority_v7)
    dossier = fixture.make_research_dossier(
        audit,
        authority_v7,
        hard_bucket,
        c1a_ttu,
        c1b_ttu,
        c1b_dialogue,
        c2a_ttu,
        c2b_ttu,
        c2b_dialogue,
    )
    claims = fixture.make_claim_ledger(audit, scope_fixture)
    audit_payloads = {fixture.AUDIT_REL: audit}
    packet = fixture.compile_blueprint_obligations(
        request,
        manifest,
        registry=registry,
        source_audit_payloads=audit_payloads,
        research_dossier=dossier,
        claim_ledger=claims,
    )

    representation_bundles: dict[str, dict[str, Any]] = {}
    representation_bindings: dict[str, list[dict[str, Any]]] = {}
    representation_capabilities: dict[str, str] = {}
    for mode in fixture.MODES:
        bundle, bindings, capability = _governed_representation(mode, packet, authority_v7)
        representation_bundles[mode] = bundle
        representation_bindings[mode] = bindings
        representation_capabilities[mode] = capability

    payloads = {
        "CORE1A": fixture.build_core1a_payload(
            authority_v7,
            c1a_ttu,
            gate,
            representation_bundles["CORE1A"],
            representation_bindings["CORE1A"],
            representation_capabilities["CORE1A"],
        ),
        "CORE1B": fixture.build_core1b_payload(
            hard_bucket,
            c1b_ttu,
            c1b_dialogue,
            gate,
            representation_bundles["CORE1B"],
            representation_bindings["CORE1B"],
        ),
        "CORE2A": fixture.build_core2a_payload(
            c2a_ttu,
            c2a_product,
            representation_bundles["CORE2A"],
            representation_bindings["CORE2A"],
        ),
        "CORE2B": fixture.build_core2b_payload(
            c2b_ttu,
            c2b_dialogue,
            lau,
            c2b_product,
            representation_bundles["CORE2B"],
            representation_bindings["CORE2B"],
        ),
    }

    authorities: dict[str, dict[str, Any]] = {}
    scopes: dict[str, dict[str, Any]] = {}
    custodies: dict[str, dict[str, Any]] = {}
    renders: dict[str, Any] = {}
    preflights: dict[str, Any] = {}
    pngs: dict[str, list[str]] = {}

    for mode in fixture.MODES:
        realized = fixture.realized_obligations(packet, mode, audit, scope_fixture, payloads[mode])
        authority = fixture.compile_core_authority(
            mode,
            authority_v7["subtopic_id"],
            payloads[mode],
            packet,
            realized,
            authority_id=f"CHEM-CORE-AUTH-REDOX-FOUR-CORE-STRESS-{mode}",
            payload_ref=f"stress_tests/redox/four_core/generated/{mode.lower()}-payload.json",
        )
        scope = fixture.make_source_scope(mode, authority, audit, scope_fixture)
        custody = fixture.compile_core_product_custody(
            request,
            manifest,
            packet,
            scope,
            authority,
            registry=registry,
            source_audit_payloads=audit_payloads,
            research_dossier=dossier,
            claim_ledger=claims,
        )
        authorities[mode] = authority
        scopes[mode] = scope
        custodies[mode] = custody
        mode_dir = out_dir / mode.lower()
        fixture.write_json(mode_dir / "payload.json", payloads[mode])
        fixture.write_json(mode_dir / "authority.json", authority)
        fixture.write_json(mode_dir / "source-scope.json", scope)
        fixture.write_json(mode_dir / "custody.json", custody)
        if render:
            from run_chemistry_core_product import run_core_product

            render_manifest, preflight = run_core_product(custody, authority, payloads[mode], mode_dir)
            renders[mode] = render_manifest
            preflights[mode] = preflight
            if preflight["status"] != "PASS":
                raise ValueError(f"REDOX_STRESS_PREFLIGHT_FAILED:{mode}")
            pdf_path = mode_dir / render_manifest["artifact"]["path"]
            pngs[mode] = fixture.render_pngs(pdf_path, mode_dir / "pages")

    fixture.write_json(out_dir / "engineering-request.json", request)
    fixture.write_json(out_dir / "engineering-manifest.json", manifest)
    fixture.write_json(out_dir / "research-dossier.json", dossier)
    fixture.write_json(out_dir / "claim-ledger.json", claims)
    fixture.write_json(out_dir / "blueprint-obligations.json", packet)

    input_paths = [
        fixture.AUDIT_REL,
        fixture.SCOPE_FIXTURE_REL,
        fixture.REGISTRY_REL,
        fixture.AUTHORITY_REL,
        fixture.HARD_BUCKET_REL,
        fixture.C1A_TTU_REL,
        fixture.C1B_TTU_REL,
        fixture.C1B_DIALOGUE_REL,
        fixture.C2A_TTU_REL,
        fixture.C2B_TTU_REL,
        fixture.C2B_DIALOGUE_REL,
        fixture.LAU_REL,
        fixture.C2A_PRODUCT_REL,
        fixture.C2B_PRODUCT_REL,
        fixture.REP_EXTENSION_REL,
        REP_INTENT_POLICY_REL,
        RUNTIME_FACT_SCHEMA_REL,
        PRIMITIVE_REGISTRY_REL,
        PAGE_INTENT_REL,
        NOTATION_REL,
        REP_INTENT_EXTENSION_REL,
        RUNTIME_FACT_EXTENSION_REL,
    ]
    held_fingerprints = {
        row["fingerprint"] for row in scope_fixture["held_transformation_guards"]
    }
    realized_transform_refs = {
        mode: [
            row["asset_ref"]
            for row in packet["obligations"]
            if row["obligation_id"] in set(authorities[mode]["realized_obligation_ids"])
            and row["kind"] == "TRANSFORMATION"
        ]
        for mode in fixture.MODES
    }
    problem_projection = fixture.project_problem_family(gate["problem_families"][0])
    summary = {
        "schema_version": "2.1.0",
        "stress_id": "CHEM-REDOX-FOUR-CORE-STRESS-v4",
        "subject": "CHEMISTRY",
        "stress_only": True,
        "generic_compiler_changed_for_topic": False,
        "representation_authority_mode": "GOVERNED_INTENT_PLUS_LOCAL_SEMANTIC_INSTANCE_FACTS",
        "representation_semantic_authority_ref": authority_v7["authority_id"],
        "fixture_authored_representation_semantics": False,
        "engineering_gate_id": audit["gate_id"],
        "subtopic_id": authority_v7["subtopic_id"],
        "input_digests": {rel: fixture.sha256(fixture.load(rel)) for rel in input_paths},
        "obligation_packet_id": packet["packet_id"],
        "obligation_packet_digest": packet["packet_digest"],
        "problem_family_projection": {
            "problem_family_ref": problem_projection["problem_family_ref"],
            "method_steps": problem_projection["method_steps"],
            "common_fatal_errors": problem_projection["common_fatal_errors"],
            "semantic_role_trace": problem_projection["semantic_role_trace"],
        },
        "products": {
            mode: {
                "authority_id": authorities[mode]["authority_id"],
                "authority_digest": authorities[mode]["authority_digest"],
                "source_scope_id": scopes[mode]["scope_contract_id"],
                "custody_id": custodies[mode]["custody_id"],
                "custody_digest": custodies[mode]["custody_digest"],
                "scope_units": authorities[mode]["scope_units"],
                "representation_closure": authorities[mode]["representation_closure"],
                "representation_bundle_summary": representation_bundles[mode]["summary"],
                "representation_semantic_instance_refs": sorted({
                    row["semantic_instance_ref"]
                    for row in representation_bundles[mode]["representations"]
                    if row.get("semantic_instance_ref")
                }),
                "realized_transformations": realized_transform_refs[mode],
                "render_status": preflights.get(mode, {}).get("status", "NOT_RENDERED"),
                "artifact": renders.get(mode, {}).get("artifact"),
                "page_images": pngs.get(mode, []),
            }
            for mode in fixture.MODES
        },
        "held_transformation_fingerprints": sorted(held_fingerprints),
        "held_transform_realized_by_any_core": any(
            held_fingerprints & set(realized_transform_refs[mode]) for mode in fixture.MODES
        ),
        "status": "PASS",
        "stress_digest": "",
    }
    if summary["held_transform_realized_by_any_core"]:
        raise ValueError("REDOX_STRESS_HELD_TRANSFORMATION_REALIZED")
    summary["stress_digest"] = fixture.sha256(
        {key: value for key, value in summary.items() if key != "stress_digest"}
    )
    fixture.write_json(out_dir / "redox-four-core-stress-manifest.json", summary)
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--render", action="store_true")
    args = parser.parse_args()
    result = build_stress(args.out_dir, render=args.render)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
