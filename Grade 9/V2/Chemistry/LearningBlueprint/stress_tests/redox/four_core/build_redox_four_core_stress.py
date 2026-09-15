#!/usr/bin/env python3
"""Redox end-to-end stress fixture for the generic four-Core compiler.

This file is intentionally topic-specific fixture code. It is not generic Chemistry
policy and must not become a coding template. Every Chemistry-bearing learner string
and every representation fact is loaded from current repository authority at runtime.
Redox may falsify generic contracts; it may not define them.
"""
from __future__ import annotations

import argparse
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

from chemistry_notation import parse_equation  # noqa: E402
from compile_chemistry_blueprint_obligations import compile_blueprint_obligations  # noqa: E402
from compile_chemistry_core_authority import compile_core_authority  # noqa: E402
from compile_chemistry_core_product_custody import compile_core_product_custody  # noqa: E402
from compile_chemistry_core_representation_bundle import compile_core_representation_bundle  # noqa: E402
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
        "curriculum_scope": {"grades": [9, 10, 11], "curriculum": "CBSE/NCERT", "exam_family": "COMPETITIVE_FOUNDATION"},
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


def engineering_electron_state_records(gate: dict[str, Any]) -> tuple[str, list[dict[str, Any]]]:
    equations = list(gate.get("mandatory_equations") or [])
    if not equations:
        raise ValueError("REDOX_STRESS_ENGINEERING_EQUATION_REQUIRED")
    selected = None
    transitions = None
    for equation in equations:
        matches = re.findall(
            r"\b([A-Z][a-z]?)\s+(?:oxidized|reduced)\s+from\s+([+-]?\d+)\s+to\s+([+-]?\d+)",
            str(equation.get("meaning_of_symbols", "")),
            flags=re.IGNORECASE,
        )
        if matches:
            selected = equation
            transitions = matches
            break
    if selected is None or not transitions:
        raise ValueError("REDOX_STRESS_ENGINEERING_OXIDATION_STATE_TRANSITIONS_REQUIRED")
    parsed = parse_equation(selected["formula"])
    states = []
    for raw_element, raw_before, raw_after in transitions:
        element = raw_element[0].upper() + raw_element[1:].lower()
        before = int(raw_before)
        after = int(raw_after)
        reactants = [row for row in parsed["reactants"] if element in row["atoms"]]
        products = [row for row in parsed["products"] if element in row["atoms"]]
        if not reactants or not products:
            raise ValueError(f"REDOX_STRESS_ENGINEERING_STATE_SPECIES_UNRESOLVED:{element}")
        before_species = reactants[0]
        after_species = products[0]
        before_count = int(before_species["total_atoms"][element])
        after_count = int(after_species["total_atoms"][element])
        if before_count != after_count:
            raise ValueError(f"REDOX_STRESS_ENGINEERING_ELEMENT_COUNT_DRIFT:{element}")
        electron_count = abs(after - before) * before_count
        if electron_count < 1:
            raise ValueError(f"REDOX_STRESS_ENGINEERING_ZERO_ELECTRON_CHANGE:{element}")
        states.append({
            "element": element,
            "before": before,
            "after": after,
            "before_species": before_species["raw"],
            "after_species": after_species["raw"],
            "electron_count": electron_count,
        })
    lost = sum(row["electron_count"] for row in states if row["after"] > row["before"])
    gained = sum(row["electron_count"] for row in states if row["after"] < row["before"])
    if not lost or lost != gained:
        raise ValueError(f"REDOX_STRESS_ENGINEERING_ELECTRON_EXCHANGE_UNBALANCED:{lost}:{gained}")
    return selected["formula"], states


def make_representation_plan(mode: str, gate: dict[str, Any], c1a_ttu: dict[str, Any]) -> tuple[dict[str, Any], str]:
    engineering_rows = [
        row for row in gate.get("representations", [])
        if row.get("representation_type") == "ELECTRON_TRANSFER_DIAGRAM"
    ]
    if len(engineering_rows) != 1:
        raise ValueError("REDOX_STRESS_ENGINEERING_ELECTRON_TRANSFER_REPRESENTATION_REQUIRED")
    engineering = engineering_rows[0]
    extension = load(REP_EXTENSION_REL)
    primitive_id = extension["conditional_primitives"]["ELECTRON_TRANSFER_EVIDENCE"]
    primitive = next(row for row in extension["primitives"] if row["primitive_id"] == primitive_id)
    allowed_caps = set(primitive["capability_refs"])
    capability = next((cap for cap in c1a_ttu["identity"]["capability_ids"] if cap in allowed_caps), None)
    if capability is None:
        raise ValueError("REDOX_STRESS_BLUEPRINT_CAPABILITY_NOT_SUPPORTED_BY_ENGINEERING_REPRESENTATION")
    equation, states = engineering_electron_state_records(gate)
    representation_id = f"REP-REDOX-FOUR-CORE-STRESS-{mode}-ELECTRON-TRANSFER"
    plan = {
        "plan_id": f"CHEM-REP-PLAN-REDOX-FOUR-CORE-STRESS-{mode}",
        "representations": [{
            "representation_id": representation_id,
            "engineering_representation_refs": [engineering["representation_id"]],
            "capability_ref": capability,
            "primitive_id": primitive_id,
            "problem_family_ref": gate["problem_families"][0]["family_id"],
            "chemical_entities": [equation],
            "source_semantic_data": {
                "chemical_entities": [equation],
                "oxidation_states": states,
                "verification_requirements": list(gate["mandatory_verifications"]),
                "engineering_representation_name": engineering["name"],
                "engineering_verification_method": engineering["verification_method"],
            },
            "notation_tokens": [equation],
            "accessibility_text": engineering["name"] + ". " + engineering["verification_method"],
        }],
    }
    return plan, capability


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
                watch = " ".join(part for part in [f"Common wrong model: {wrong}" if wrong else "", f"Repair: {repair}" if repair else ""] if part)
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
                "verification_steps": verification or flatten_strings(c1a_ttu["canonical_expert_state"].get("verification", {})),
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
    manuscript["manuscript_digest"] = bare_sha256({k: v for k, v in manuscript.items() if k != "manuscript_digest"})
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
            for level, row in zip(("H1_ORIENT", "H2_REPRESENT", "H3_PRINCIPLE", "H4_FIRST_MOVE"), stages)
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
            "citations": [{"label": "Governed Blueprint problem authority", "locator": "Current repository Blueprint"}],
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
    plan["plan_digest"] = bare_sha256({k: v for k, v in plan.items() if k != "plan_digest"})
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
        {"level": "H7_FULL_SOLUTION", "text": " ".join(expert.get("equations", []) + [expert["result"]])},
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
        "full_solution": " ".join(expert["reasoning_steps"] + expert.get("equations", []) + [expert["result"]]),
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
                refs.update(((item.get("learner_support") or {}).get("see_the_idea") or {}).get("pre_taught_representation_refs") or [])
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
                raise ValueError(f"REDOX_STRESS_TRANSFORMATION_TIER_UNRESOLVED:{row['asset_ref']}:{tier}")
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
        row for row in audit["scope_tiers"]
        if row["tier_id"] in set(scope_fixture["authorized_scope_tiers"])
        and row["minimum_learner_grade"] > scope_fixture["learner_grade"]
    ]
    reason = "Authorized higher-grade source tiers: " + " | ".join(row["description"] for row in higher)
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


def build_stress(out_dir: Path, *, render: bool = False) -> dict[str, Any]:
    out_dir.mkdir(parents=True, exist_ok=True)
    registry = load(REGISTRY_REL)
    audit = load(AUDIT_REL)
    scope_fixture = load(SCOPE_FIXTURE_REL)
    authority_v7 = load(AUTHORITY_REL)
    hard_bucket = load(HARD_BUCKET_REL)
    c1a_ttu = load(C1A_TTU_REL)
    c1b_ttu = load(C1B_TTU_REL)
    c1b_dialogue = load(C1B_DIALOGUE_REL)
    c2a_ttu = load(C2A_TTU_REL)
    c2b_ttu = load(C2B_TTU_REL)
    c2b_dialogue = load(C2B_DIALOGUE_REL)
    lau = load(LAU_REL)
    c2a_product = load(C2A_PRODUCT_REL)
    c2b_product = load(C2B_PRODUCT_REL)

    if scope_fixture.get("stress_only") is not True:
        raise ValueError("REDOX_STRESS_FIXTURE_MUST_BE_STRESS_ONLY")
    if audit["audit_role"] != "PRODUCTION_SOURCE_AUDIT":
        raise ValueError("REDOX_STRESS_PRODUCTION_AUDIT_REQUIRED")
    gate = gate_map(registry)[audit["gate_id"]]
    if gate["technical_readiness"] != "ENGINEERING_GATE_READY":
        raise ValueError("REDOX_STRESS_ENGINEERING_GATE_NOT_READY")

    request = make_request()
    manifest = make_manifest(registry, audit, authority_v7)
    dossier = make_research_dossier(
        audit, authority_v7, hard_bucket, c1a_ttu, c1b_ttu, c1b_dialogue,
        c2a_ttu, c2b_ttu, c2b_dialogue,
    )
    claims = make_claim_ledger(audit, scope_fixture)
    audit_payloads = {AUDIT_REL: audit}
    packet = compile_blueprint_obligations(
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
    for mode in MODES:
        rep_plan, rep_capability = make_representation_plan(mode, gate, c1a_ttu)
        bundle, bindings = compile_core_representation_bundle(
            mode,
            packet,
            rep_plan,
            bundle_id=f"CHEM-REDOX-FOUR-CORE-STRESS-REP-BUNDLE-{mode}",
        )
        representation_bundles[mode] = bundle
        representation_bindings[mode] = bindings
        representation_capabilities[mode] = rep_capability

    payloads = {
        "CORE1A": build_core1a_payload(
            authority_v7, c1a_ttu, gate,
            representation_bundles["CORE1A"], representation_bindings["CORE1A"], representation_capabilities["CORE1A"],
        ),
        "CORE1B": build_core1b_payload(
            hard_bucket, c1b_ttu, c1b_dialogue, gate,
            representation_bundles["CORE1B"], representation_bindings["CORE1B"],
        ),
        "CORE2A": build_core2a_payload(
            c2a_ttu, c2a_product,
            representation_bundles["CORE2A"], representation_bindings["CORE2A"],
        ),
        "CORE2B": build_core2b_payload(
            c2b_ttu, c2b_dialogue, lau, c2b_product,
            representation_bundles["CORE2B"], representation_bindings["CORE2B"],
        ),
    }
    authorities: dict[str, dict[str, Any]] = {}
    scopes: dict[str, dict[str, Any]] = {}
    custodies: dict[str, dict[str, Any]] = {}
    renders: dict[str, Any] = {}
    preflights: dict[str, Any] = {}
    pngs: dict[str, list[str]] = {}

    for mode in MODES:
        realized = realized_obligations(packet, mode, audit, scope_fixture, payloads[mode])
        authority = compile_core_authority(
            mode,
            authority_v7["subtopic_id"],
            payloads[mode],
            packet,
            realized,
            authority_id=f"CHEM-CORE-AUTH-REDOX-FOUR-CORE-STRESS-{mode}",
            payload_ref=f"stress_tests/redox/four_core/generated/{mode.lower()}-payload.json",
        )
        scope = make_source_scope(mode, authority, audit, scope_fixture)
        custody = compile_core_product_custody(
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
        write_json(mode_dir / "payload.json", payloads[mode])
        write_json(mode_dir / "authority.json", authority)
        write_json(mode_dir / "source-scope.json", scope)
        write_json(mode_dir / "custody.json", custody)
        if render:
            from run_chemistry_core_product import run_core_product

            render_manifest, preflight = run_core_product(custody, authority, payloads[mode], mode_dir)
            renders[mode] = render_manifest
            preflights[mode] = preflight
            if preflight["status"] != "PASS":
                raise ValueError(f"REDOX_STRESS_PREFLIGHT_FAILED:{mode}")
            pdf_path = mode_dir / render_manifest["artifact"]["path"]
            pngs[mode] = render_pngs(pdf_path, mode_dir / "pages")

    write_json(out_dir / "engineering-request.json", request)
    write_json(out_dir / "engineering-manifest.json", manifest)
    write_json(out_dir / "research-dossier.json", dossier)
    write_json(out_dir / "claim-ledger.json", claims)
    write_json(out_dir / "blueprint-obligations.json", packet)

    input_paths = [
        AUDIT_REL, SCOPE_FIXTURE_REL, REGISTRY_REL, AUTHORITY_REL, HARD_BUCKET_REL,
        C1A_TTU_REL, C1B_TTU_REL, C1B_DIALOGUE_REL, C2A_TTU_REL, C2B_TTU_REL,
        C2B_DIALOGUE_REL, LAU_REL, C2A_PRODUCT_REL, C2B_PRODUCT_REL, REP_EXTENSION_REL,
    ]
    held_fingerprints = {row["fingerprint"] for row in scope_fixture["held_transformation_guards"]}
    realized_transform_refs = {
        mode: [
            row["asset_ref"] for row in packet["obligations"]
            if row["obligation_id"] in set(authorities[mode]["realized_obligation_ids"])
            and row["kind"] == "TRANSFORMATION"
        ]
        for mode in MODES
    }
    problem_projection = project_problem_family(gate["problem_families"][0])
    summary = {
        "schema_version": "2.0.0",
        "stress_id": "CHEM-REDOX-FOUR-CORE-STRESS-v2",
        "subject": "CHEMISTRY",
        "stress_only": True,
        "generic_compiler_changed_for_topic": False,
        "engineering_gate_id": audit["gate_id"],
        "subtopic_id": authority_v7["subtopic_id"],
        "input_digests": {rel: sha256(load(rel)) for rel in input_paths},
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
                "realized_transformations": realized_transform_refs[mode],
                "render_status": preflights.get(mode, {}).get("status", "NOT_RENDERED"),
                "artifact": renders.get(mode, {}).get("artifact"),
                "page_images": pngs.get(mode, []),
            }
            for mode in MODES
        },
        "held_transformation_fingerprints": sorted(held_fingerprints),
        "held_transform_realized_by_any_core": any(
            held_fingerprints & set(realized_transform_refs[mode]) for mode in MODES
        ),
        "status": "PASS",
        "stress_digest": "",
    }
    if summary["held_transform_realized_by_any_core"]:
        raise ValueError("REDOX_STRESS_HELD_TRANSFORMATION_REALIZED")
    summary["stress_digest"] = sha256({k: v for k, v in summary.items() if k != "stress_digest"})
    write_json(out_dir / "redox-four-core-stress-manifest.json", summary)
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
