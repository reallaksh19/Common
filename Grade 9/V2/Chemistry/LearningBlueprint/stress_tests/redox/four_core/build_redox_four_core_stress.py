#!/usr/bin/env python3
"""Support utilities for the Redox four-Core stress fixture.

This module is intentionally topic-specific fixture support. It may translate current
repository Redox authority into generic Core payload contracts, but it does not own
representation selection, scientific representation semantics, runtime-fact selection,
or primitive runtime parameters. The only executable stress entrypoint is
``build_redox_four_core_governed.py``.
"""
from __future__ import annotations

import copy
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve()
ROOT = HERE.parents[3]
CHEM_ROOT = ROOT.parent
ENGINE = ROOT / "engine"
LP_ENGINE = CHEM_ROOT / "LearnerProduct" / "engine"
EXACT_ENGINE = CHEM_ROOT / "ExactProduct" / "engine"
sys.path.insert(0, str(ENGINE))
sys.path.insert(0, str(LP_ENGINE))
sys.path.insert(0, str(EXACT_ENGINE))

from compile_chemistry_blueprint_obligations import compile_blueprint_obligations  # noqa: E402
from compile_chemistry_core_authority import compile_core_authority  # noqa: E402
from compile_chemistry_core_product_custody import compile_core_product_custody  # noqa: E402
from compile_chemistry_engineering_closure import digest as engineering_digest  # noqa: E402
from project_chemistry_problem_family import project_problem_family  # noqa: E402

AUDIT_REL = "source_audits/redox/production-source-audit.v2.json"
SCOPE_FIXTURE_REL = "stress_tests/redox/four_core/source-scope-fixture.v1.json"
REGISTRY_REL = "policies/chemistry-technical-engineering-gates.v1.json"
AUTHORITY_REL = "golden/v7/core1a-study-note-redox-authority.json"
HARD_BUCKET_REL = "golden/v4/hard-bucket.json"
C1A_TTU_REL = "golden/v6/concept-ttu-core1a-redox.json"
C1B_TTU_REL = "golden/v6/concept-ttu-core1b-redox.json"
C1B_DIALOGUE_REL = "golden/v6/dialogue-core1b-redox.json"
C2A_TTU_REL = "golden/v6/problem-ttu-core2a-redox.json"
C2B_TTU_REL = "golden/v6/problem-ttu-core2b-redox.json"
C2B_DIALOGUE_REL = "golden/v6/dialogue-core2b-redox.json"
LAU_REL = "golden/v6/lau-knowledge-redox.json"
C2A_PRODUCT_REL = "golden/v5/core2a-owner-question-product.json"
C2B_PRODUCT_REL = "golden/v5/core2b-owner-question-product.json"
REP_EXTENSION_REL = "../Representation/registry/chemistry-electron-transfer-primitive-extension.v1.json"

MODES = ("CORE1A", "CORE1B", "CORE2A", "CORE2B")
REQUEST_ID = "CHEM-ENG-REQ-REDOX-FOUR-CORE-STRESS"
MANIFEST_ID = "CHEM-ENG-MAN-REDOX-FOUR-CORE-STRESS"


def load(rel: str) -> dict[str, Any]:
    return json.loads((ROOT / rel).resolve().read_text(encoding="utf-8"))


def canonical(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256(obj: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical(obj).encode("utf-8")).hexdigest()


def bare_sha256(obj: Any) -> str:
    return hashlib.sha256(canonical(obj).encode("utf-8")).hexdigest()


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def flatten_strings(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value] if value.strip() else []
    if isinstance(value, dict):
        out: list[str] = []
        for child in value.values():
            out.extend(flatten_strings(child))
        return out
    if isinstance(value, list):
        out: list[str] = []
        for child in value:
            out.extend(flatten_strings(child))
        return out
    return [str(value)]


def unique(values: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            out.append(value)
    return out


def gate_map(registry: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {row["subtopic_id"]: row for row in registry["subtopic_gates"]}


def external_prerequisites(registry: dict[str, Any], direct_gate_id: str) -> list[str]:
    gates = gate_map(registry)
    seen: set[str] = set()
    external: set[str] = set()

    def walk(gid: str) -> None:
        if gid in seen:
            return
        seen.add(gid)
        gate = gates.get(gid)
        if gate is None:
            return
        for prereq in gate.get("prerequisite_ids", []):
            if prereq.startswith("CHEM-"):
                walk(prereq)
            else:
                external.add(prereq)

    walk(direct_gate_id)
    return sorted(external)


def make_request() -> dict[str, Any]:
    return {
        "schema_version": "2.0.0",
        "request_id": REQUEST_ID,
        "subject": "CHEMISTRY",
        "requested_topic": "Redox four-Core compiler stress fixture",
        "requested_scope": "Current governed Redox species/state/electron/agent scope",
        "engineering_depth": "RESEARCH",
        "requested_action": "DECLARE_DIRECT_GATES",
        "curriculum_scope": {
            "grades": [9, 10, 11],
            "curriculum": "CBSE/NCERT",
            "exam_family": "COMPETITIVE_FOUNDATION",
        },
        "requested_for": ["CORE1A", "CORE1B", "CORE2A", "CORE2B", "CDAU", "SDU", "LAU", "TTU", "PAL"],
        "notes": "Stress fixture only; Redox may falsify the generic compiler but does not define generic policy.",
    }


def make_manifest(registry: dict[str, Any], audit: dict[str, Any], authority: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "2.0.0",
        "manifest_id": MANIFEST_ID,
        "request_id": REQUEST_ID,
        "scope_kind": "SUBTOPIC",
        "scope_ref": authority["subtopic_id"],
        "topic_id": "CHEM-REDOX-FOUR-CORE-STRESS",
        "title": "Redox four-Core stress compilation",
        "registry_ref": REGISTRY_REL,
        "required_gate_ids": [audit["gate_id"]],
        "optional_gate_ids": [],
        "out_of_scope_gate_ids": [],
        "source_audits": [{"gate_id": audit["gate_id"], "audit_ref": AUDIT_REL}],
        "external_prerequisite_resolutions": [
            {
                "dependency_id": dep,
                "status": "RESOLVED_BY_AUTHORITY",
                "evidence_ref": "ENGINEERING_REGISTRY_DECLARED_PREREQUISITE",
                "note": "Stress compilation preserves the current registry prerequisite declaration without inventing learner mastery.",
            }
            for dep in external_prerequisites(registry, audit["gate_id"])
        ],
        "research_dossier_ref": "stress_tests/redox/four_core/generated/research-dossier.json",
        "claim_ledger_ref": "stress_tests/redox/four_core/generated/claim-ledger.json",
        "source_item_status": "SOURCE_READY",
        "downstream_consumers": ["CDAU", "SDU", "LAU", "TTU", "PAL"],
        "notes": "Redox stress fixture only.",
    }


def research_class(layer_class: str) -> str:
    if layer_class == "STANDARD_CHEMISTRY_DERIVED":
        return "STANDARD_CHEMISTRY_DERIVED"
    if layer_class == "AUTHORING_RECOMMENDATION":
        return "AUTHORING_RECOMMENDATION"
    return "SOURCE_DEFINED"


def make_research_dossier(
    audit: dict[str, Any],
    authority: dict[str, Any],
    hard_bucket: dict[str, Any],
    c1a_ttu: dict[str, Any],
    c1b_ttu: dict[str, Any],
    c1b_dialogue: dict[str, Any],
    c2a_ttu: dict[str, Any],
    c2b_ttu: dict[str, Any],
    c2b_dialogue: dict[str, Any],
) -> dict[str, Any]:
    reps: list[str] = []
    reps.extend(hard_bucket["visual_plan"]["visual_jobs"])
    reps.extend(c1a_ttu["canonical_expert_state"].get("representations", []))
    reps.extend(c1b_ttu["canonical_expert_state"].get("representations", []))
    reps.extend(c2a_ttu["task_state"].get("representation_options", []))
    reps.extend(c2b_ttu["task_state"].get("representation_options", []))
    misconceptions: list[str] = []
    misconceptions.extend(c1a_ttu["canonical_expert_state"].get("misconception_contrasts", []))
    misconceptions.extend(c1b_ttu["canonical_expert_state"].get("misconception_contrasts", []))
    misconceptions.extend(row["misconception_ref"] for row in c1b_dialogue.get("misconception_branches", []))
    misconceptions.extend(row["misconception_ref"] for row in c2b_dialogue.get("misconception_branches", []))
    misconceptions.extend(c2a_ttu["expert_solution_state"].get("wrong_routes", []))
    misconceptions.extend(c2b_ttu["expert_solution_state"].get("wrong_routes", []))
    return {
        "schema_version": "2.0.0",
        "dossier_id": "CHEM-ENG-DOSSIER-REDOX-FOUR-CORE-STRESS",
        "request_id": REQUEST_ID,
        "engineering_depth": "RESEARCH",
        "scope_definition": authority["scope_statement"],
        "authoritative_source_set": [
            {
                "source_ref": row["source_ref"],
                "authority_class": research_class(row["authority_class"]),
                "scope": row["scope"],
            }
            for row in audit["source_layers"]
        ],
        "curriculum_boundaries": [row["description"] for row in audit["scope_tiers"]],
        "representation_evidence": unique(reps),
        "misconception_evidence": unique(misconceptions),
        "selected_design_decisions": unique([
            hard_bucket["research"]["mode"],
            c1a_ttu["learner_transformation"]["target_model"],
            c1b_ttu["learner_transformation"]["target_model"],
            c1b_dialogue["stage_selection_reason"],
            c2b_dialogue["stage_selection_reason"],
        ]),
        "rejected_alternatives": unique(
            c2a_ttu["expert_solution_state"].get("wrong_routes", [])
            + c2b_ttu["expert_solution_state"].get("wrong_routes", [])
        ),
        "status": "RESEARCH_DOSSIER_READY",
    }


def make_claim_ledger(audit: dict[str, Any], scope_fixture: dict[str, Any]) -> dict[str, Any]:
    held = set(scope_fixture["held_scope_tiers"])
    claims = []
    for index, row in enumerate(audit["asset_bindings"], 1):
        claims.append({
            "claim_id": f"REDOX-STRESS-CLAIM-{index:02d}",
            "statement": row["downstream_scope"],
            "authority_class": row["claim_class"],
            "evidence_ref": "+".join(row["authority_layer_ids"]),
            "scope_status": "HELD_SCOPE" if row["scope_tier_id"] in held else "IN_SCOPE",
        })
    return {
        "schema_version": "2.0.0",
        "ledger_id": "CHEM-ENG-CLAIMS-REDOX-FOUR-CORE-STRESS",
        "request_id": REQUEST_ID,
        "claims": claims,
        "status": "CLAIM_LEDGER_READY",
    }


def select_capability(atom_title: str, capability_ids: list[str]) -> str:
    words = set(re.findall(r"[a-z0-9]+", atom_title.lower()))
    scored = []
    for index, cap in enumerate(capability_ids):
        cap_words = set(re.findall(r"[a-z0-9]+", cap.lower().replace("cap-", "")))
        scored.append((len(words & cap_words), -index, cap))
    return max(scored)[2]


def build_core1a_payload(
    authority: dict[str, Any],
    c1a_ttu: dict[str, Any],
    gate: dict[str, Any],
    rep_bundle: dict[str, Any],
    rep_bindings: list[dict[str, Any]],
    rep_capability: str,
) -> dict[str, Any]:
    objects = authority["content_objects"]
    by_atom: dict[str, list[dict[str, Any]]] = {}
    by_id = {row["object_id"]: row for row in objects}
    for row in objects:
        by_atom.setdefault(row["learning_atom_id"], []).append(row)

    rep_ref = rep_bundle["representations"][0]["representation_id"]
    sections = []
    practice_items = []
    capabilities = c1a_ttu["identity"]["capability_ids"]
    rep_placed = False
    for atom in authority["learning_atoms"]:
        rows = by_atom[atom["atom_id"]]
        classes: dict[str, list[dict[str, Any]]] = {}
        for row in rows:
            classes.setdefault(row["object_class"], []).append(row)
        meaning = flatten_strings((classes.get("MEANING") or [{}])[0].get("learner_payload"))
        explain_rows: list[str] = []
        for cls in ("RULE", "EQUATION", "REPRESENTATION", "REASONING_CHAIN", "VERIFICATION"):
            for row in classes.get(cls, []):
                explain_rows.extend(flatten_strings(row.get("learner_payload")))
        misconceptions = classes.get("MISCONCEPTION_REPAIR", [])
        watch = None
        if misconceptions:
            payload = misconceptions[0]["learner_payload"]
            if isinstance(payload, dict):
                wrong = payload.get("wrong_model")
                repair = payload.get("repair")
                watch = " ".join(
                    part
                    for part in [
                        f"Common wrong model: {wrong}" if wrong else "",
                        f"Repair: {repair}" if repair else "",
                    ]
                    if part
                )
            else:
                watch = " ".join(flatten_strings(payload))
        worked_rows = classes.get("WORKED_EXAMPLE", [])
        verification: list[str] = []
        for row in classes.get("VERIFICATION", []):
            verification.extend(flatten_strings(row["learner_payload"]))
        worked = None
        if worked_rows:
            worked = {
                "prompt": atom["learner_title"],
                "reasoning_steps": flatten_strings(worked_rows[0]["learner_payload"]),
                "verification_steps": verification
                or flatten_strings(c1a_ttu["canonical_expert_state"].get("verification", {})),
            }
        has_electron_ledger = any(row.get("representation_type") == "ELECTRON_LEDGER" for row in rows)
        refs = [rep_ref] if has_electron_ledger else []
        rep_placed = rep_placed or bool(refs)
        section_capability = select_capability(atom["learner_title"], capabilities)
        if refs and section_capability != rep_capability:
            section_capability = rep_capability
        sections.append({
            "capability_ref": section_capability,
            "see": " ".join(meaning),
            "explain": unique(explain_rows),
            "representation_refs": refs,
            "watch_one": watch,
            "worked_example": worked,
            "verification_steps": verification,
        })
        for row in rows:
            if "PRACTICE" not in row["object_class"]:
                continue
            answer = by_id[row["answer_object_id"]]
            source_label = row.get("learner_source_display", "")
            prompt = "\n".join(part for part in [source_label, str(row["learner_payload"])] if part)
            practice_items.append({
                "question_id": row.get("question_id", row["object_id"]),
                "prompt": prompt,
                "answer_path": {
                    "expected_response_rubric": {
                        "learner_label": "Expected response",
                        "criteria": flatten_strings(answer["learner_payload"]),
                    }
                },
            })
    if not rep_placed:
        raise ValueError("REDOX_STRESS_CORE1A_ENGINEERING_REPRESENTATION_NOT_PLACED")

    projected = [project_problem_family(row) for row in gate["problem_families"]]
    routines = [
        {
            "problem_family_ref": row["problem_family_ref"],
            "chemical_signature": row["chemical_signature"],
            "recognition_signals": row["recognition_signals"],
            "method_steps": row["method_steps"],
            "common_fatal_errors": row["common_fatal_errors"],
            "typical_unknown": row["typical_unknown"],
        }
        for row in projected
    ]
    bucket = {
        "bucket_id": "REDOX-FOUR-CORE-STRESS-C1A",
        "learner_title": authority["subtopic_title"],
        "bucket_invariant": c1a_ttu["canonical_expert_state"]["concept_statement"],
        "learning_atoms": [
            {"atom_id": row["atom_id"], "learner_title": row["learner_title"]}
            for row in authority["learning_atoms"]
        ],
        "teaching_sections": sections,
        "problem_family_routines": routines,
        "practice_items": practice_items,
        "readiness_gate": {"required_dimensions": c1a_ttu["canonical_expert_state"]["reasoning_chain"]},
    }
    manuscript = {
        "manuscript_id": "CHEM-REDOX-FOUR-CORE-STRESS-C1A-MANUSCRIPT",
        "schema_version": "1.0.0",
        "buckets": [bucket],
        "manuscript_digest": "",
    }
    manuscript["manuscript_digest"] = bare_sha256(
        {key: value for key, value in manuscript.items() if key != "manuscript_digest"}
    )
    return {
        "manuscript": manuscript,
        "representation_bundle": rep_bundle,
        "representation_bindings": rep_bindings,
    }


def build_core1b_payload(
    hard_bucket: dict[str, Any],
    c1b_ttu: dict[str, Any],
    dialogue: dict[str, Any],
    gate: dict[str, Any],
    rep_bundle: dict[str, Any],
    rep_bindings: list[dict[str, Any]],
) -> dict[str, Any]:
    stages = dialogue["stages"]
    verification = flatten_strings(c1b_ttu["canonical_expert_state"]["verification"])
    capabilities = c1b_ttu["identity"]["capability_ids"]
    families = [row["family_id"] for row in gate["problem_families"]]
    rep_ref = rep_bundle["representations"][0]["representation_id"]
    return {
        "subject": "CHEMISTRY",
        "delivery_mode": "STATIC",
        "new_chemistry_refs": [],
        "module_ref": c1b_ttu["ttu_id"],
        "title": hard_bucket["title"],
        "instruction_bucket": hard_bucket,
        "capability_ref": select_capability(dialogue["target_change"], capabilities),
        "approved_capability_refs": capabilities,
        "problem_family_ref": families[0],
        "approved_problem_family_refs": families,
        "used_representation_refs": [rep_ref],
        "approved_representation_refs": [rep_ref],
        "representation_bundle": rep_bundle,
        "representation_bindings": rep_bindings,
        "task_prompt": " ".join(row["prompt"] for row in stages[:3]),
        "canonical_answer": c1b_ttu["canonical_expert_state"]["concept_statement"],
        "explanation": c1b_ttu["learner_transformation"]["target_model"],
        "check": " ".join(verification),
        "help_mode": "PROGRESSIVE_FIXED",
        "help": [
            {"level": level, "text": row["prompt"]}
            for level, row in zip(
                ("H1_ORIENT", "H2_REPRESENT", "H3_PRINCIPLE", "H4_FIRST_MOVE"),
                stages,
            )
        ],
        "workspace_lines": 10,
    }


def problem_prompt(problem_ttu: dict[str, Any]) -> str:
    givens = "; ".join(problem_ttu["task_state"].get("givens", []))
    unknown = problem_ttu["task_state"].get("unknown", "")
    return f"Given: {givens}. Task: {unknown}."


def build_core2a_payload(
    problem_ttu: dict[str, Any],
    product_golden: dict[str, Any],
    rep_bundle: dict[str, Any],
    rep_bindings: list[dict[str, Any]],
) -> dict[str, Any]:
    expert = problem_ttu["expert_solution_state"]
    rep_ref = rep_bundle["representations"][0]["representation_id"]
    item = {
        "item_id": problem_ttu["identity"]["question_id"],
        "prompt": problem_prompt(problem_ttu),
        "question_authority_ref": problem_ttu["identity"]["question_authority_ref"],
        "provenance": {
            "authority_ref": problem_ttu["identity"]["question_authority_ref"],
            "citations": [
                {
                    "label": "Governed Blueprint problem authority",
                    "locator": "Current repository Blueprint",
                }
            ],
        },
        "learner_support": {
            "write_this_first": expert["recognition"],
            "small_clue": expert["representation"],
            "bigger_clue": expert["model_selection"],
            "how_do_i_start": expert["first_move"],
            "watch_for_this": " / ".join(expert.get("wrong_routes", [])),
            "think_it_through": expert["reasoning_steps"],
            "check_your_chemistry": [expert["verification"]],
            "see_the_idea": {"pre_taught_representation_refs": [rep_ref]},
        },
        "core1a_binding": {"h2_evidence_refs": [rep_ref]},
        "answer_path": {
            "quick_check": {
                "answer_summary": expert["result"],
                "marking_points": [expert["verification"]],
            },
            "full_working": {
                "steps": expert["reasoning_steps"] + expert.get("equations", []) + [expert["result"]],
                "verification": expert["verification"],
            },
        },
        "blueprint_product_ref": product_golden["product_mode"],
    }
    plan = {
        "plan_id": "CHEM-REDOX-FOUR-CORE-STRESS-C2A-CHALLENGE",
        "items": [item],
        "plan_digest": "",
    }
    plan["plan_digest"] = bare_sha256({key: value for key, value in plan.items() if key != "plan_digest"})
    return {
        "source_plan": None,
        "challenge_plan": plan,
        "representation_bundle": rep_bundle,
        "representation_bindings": rep_bindings,
    }


def build_core2b_payload(
    problem_ttu: dict[str, Any],
    dialogue: dict[str, Any],
    lau: dict[str, Any],
    product_golden: dict[str, Any],
    rep_bundle: dict[str, Any],
    rep_bindings: list[dict[str, Any]],
) -> dict[str, Any]:
    expert = problem_ttu["expert_solution_state"]
    stages = dialogue["stages"]
    question_id = problem_ttu["identity"]["question_id"]
    rep_ref = rep_bundle["representations"][0]["representation_id"]
    help_rows = [
        {"level": "H1_ORIENT", "text": stages[0]["prompt"]},
        {"level": "H2_STRUCTURE", "text": stages[1]["prompt"]},
        {"level": "H3_REPRESENTATION", "text": expert["representation"]},
        {"level": "H4_PRINCIPLE", "text": expert["model_selection"]},
        {"level": "H5_FIRST_MOVE", "text": expert["first_move"]},
        {"level": "H6_PARTIAL_PATH", "text": " -> ".join(expert["reasoning_steps"])},
        {
            "level": "H7_FULL_SOLUTION",
            "text": " ".join(expert.get("equations", []) + [expert["result"]]),
        },
        {"level": "H8_VERIFY_REFLECT", "text": expert["verification"]},
    ]
    return {
        "subject": "CHEMISTRY",
        "delivery_mode": "STATIC",
        "new_chemistry_refs": [],
        "learner_conditioning": {
            "schema_version": "4.0.0",
            "mode": "KNOWLEDGE_PERCENT",
            "knowledge_percent": lau["conditioning"]["learner_state"]["knowledge_percent"],
        },
        "selected_item_id": question_id,
        "legal_core2a_item_ids": [question_id],
        "question_mode": "FROZEN_SOURCE_ITEM",
        "source_item": {
            "item_id": question_id,
            "source_locator": "Governed Blueprint question authority",
            "stem": problem_prompt(problem_ttu),
            "canonical_answer": expert["result"],
            "problem_family_ref": problem_ttu["identity"]["problem_family_id"],
            "provenance_class": product_golden["episodes"][0]["source_class"],
        },
        "used_representation_refs": [rep_ref],
        "approved_representation_refs": [rep_ref],
        "representation_bundle": rep_bundle,
        "representation_bindings": rep_bindings,
        "help_mode": "PROGRESSIVE_FIXED",
        "help": help_rows,
        "full_solution": " ".join(
            expert["reasoning_steps"] + expert.get("equations", []) + [expert["result"]]
        ),
        "verify_reflect": expert["verification"],
        "workspace_lines": 10,
    }


def _used_representation_refs(mode: str, payload: dict[str, Any]) -> set[str]:
    refs: set[str] = set()
    if mode == "CORE1A":
        for bucket in payload["manuscript"]["buckets"]:
            for section in bucket.get("teaching_sections", []):
                refs.update(section.get("representation_refs") or [])
    elif mode == "CORE1B":
        refs.update(payload.get("used_representation_refs") or [])
    elif mode == "CORE2A":
        for key in ("source_plan", "challenge_plan"):
            plan = payload.get(key)
            if not isinstance(plan, dict):
                continue
            for item in plan.get("items", []):
                refs.update(
                    ((item.get("learner_support") or {}).get("see_the_idea") or {}).get(
                        "pre_taught_representation_refs"
                    )
                    or []
                )
                refs.update((item.get("core1a_binding") or {}).get("h2_evidence_refs") or [])
    elif mode == "CORE2B":
        refs.update(payload.get("used_representation_refs") or [])
    return {str(ref) for ref in refs if str(ref).strip()}


def realized_engineering_representation_refs(mode: str, payload: dict[str, Any]) -> set[str]:
    used = _used_representation_refs(mode, payload)
    by_rep = {
        row["representation_ref"]: set(row["engineering_representation_refs"])
        for row in payload.get("representation_bindings", [])
    }
    missing = used - set(by_rep)
    if missing:
        raise ValueError("REDOX_STRESS_REPRESENTATION_USAGE_UNBOUND:" + ",".join(sorted(missing)))
    out: set[str] = set()
    for ref in used:
        out.update(by_rep[ref])
    return out


def realized_obligations(
    packet: dict[str, Any],
    mode: str,
    audit: dict[str, Any],
    scope_fixture: dict[str, Any],
    payload: dict[str, Any],
) -> list[str]:
    held = set(scope_fixture["held_scope_tiers"])
    authorized = set(scope_fixture["authorized_scope_tiers"])
    transform_tiers = {
        row["asset_ref"]: row["scope_tier_id"]
        for row in audit["asset_bindings"]
        if row["asset_kind"] == "TRANSFORMATION"
    }
    realized_reps = realized_engineering_representation_refs(mode, payload)
    out = []
    for row in packet["obligations"]:
        if not row["direct"] or mode not in row["authorized_modes"]:
            continue
        if row["kind"] == "TRANSFORMATION":
            tier = transform_tiers[row["asset_ref"]]
            if tier in held:
                continue
            if tier not in authorized:
                raise ValueError(
                    f"REDOX_STRESS_TRANSFORMATION_TIER_UNRESOLVED:{row['asset_ref']}:{tier}"
                )
        if row["kind"] == "REPRESENTATION" and row["asset_ref"] not in realized_reps:
            continue
        out.append(row["obligation_id"])
    return out


def highest_authorized_tier(audit: dict[str, Any], scope_fixture: dict[str, Any]) -> str:
    authorized = set(scope_fixture["authorized_scope_tiers"])
    rows = [row for row in audit["scope_tiers"] if row["tier_id"] in authorized]
    if not rows:
        raise ValueError("REDOX_STRESS_NO_AUTHORIZED_SOURCE_TIER")
    return max(rows, key=lambda row: (row["minimum_learner_grade"], row["tier_id"]))["tier_id"]


def make_source_scope(
    mode: str,
    authority: dict[str, Any],
    audit: dict[str, Any],
    scope_fixture: dict[str, Any],
) -> dict[str, Any]:
    default_tier = highest_authorized_tier(audit, scope_fixture)
    atom_map = scope_fixture["core1a_atom_scope_assignments"]
    assignments = []
    for row in authority["scope_units"]:
        tier = atom_map[row["scope_unit_id"]] if mode == "CORE1A" else default_tier
        assignments.append({**row, "scope_tier": tier})
    higher = [
        row
        for row in audit["scope_tiers"]
        if row["tier_id"] in set(scope_fixture["authorized_scope_tiers"])
        and row["minimum_learner_grade"] > scope_fixture["learner_grade"]
    ]
    reason = "Authorized higher-grade source tiers: " + " | ".join(
        row["description"] for row in higher
    )
    return {
        "schema_version": "1.0.0",
        "scope_contract_id": f"CHEM-CORE-SCOPE-REDOX-FOUR-CORE-STRESS-{mode}",
        "product_mode": mode,
        "gate_id": audit["gate_id"],
        "subtopic_id": authority["subtopic_id"],
        "source_audit_ref": AUDIT_REL,
        "source_audit_digest": engineering_digest(audit),
        "learner_grade": scope_fixture["learner_grade"],
        "program_context": scope_fixture["program_context"],
        "authorized_scope_tiers": scope_fixture["authorized_scope_tiers"],
        "held_scope_tiers": scope_fixture["held_scope_tiers"],
        "extension_authority_ref": authority["authority_id"],
        "extension_reason": reason,
        "scope_unit_assignments": assignments,
        "held_transformation_guards": copy.deepcopy(scope_fixture["held_transformation_guards"]),
        "status": "CORE_SCOPE_READY",
    }


def render_pngs(pdf_path: Path, out_dir: Path) -> list[str]:
    import pymupdf

    out_dir.mkdir(parents=True, exist_ok=True)
    doc = pymupdf.open(pdf_path)
    paths = []
    for index, page in enumerate(doc, 1):
        path = out_dir / f"page-{index:03d}.png"
        pix = page.get_pixmap(matrix=pymupdf.Matrix(1.5, 1.5), alpha=False)
        pix.save(path)
        paths.append(str(path.relative_to(out_dir.parent.parent)))
    doc.close()
    return paths
