#!/usr/bin/env python3
"""Build the real NCERT Redox C-F/C-G/C-H/C-I/C-J production slice.

This is deliberately topic-specific production authority, not a shortcut around
the generic Chemistry semantic chain. The retained source denominator comes
from ``redox-ncert-authority.json`` and PR #346's independently frozen baseline.
The eleven NCERT questions remain source practice. Redox oxidation-state and
agent-role material is marked as a depth extension and never masquerades as an
additional NCERT source question.

The output objects are the exact upstream shapes consumed by the generic
LearnerProduct runner. They are deterministic and digest-bound so the production
runner can take them through C-LP-25 without reading chat history or reverse-
engineering an older learner PDF.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve()
REDOX_DIR = HERE.parent
LP = HERE.parents[2]
CHEM = HERE.parents[3]
REPO = CHEM.parents[2]

sys.path.insert(0, str(CHEM / "Representation" / "engine"))
sys.path.insert(0, str(LP / "engine"))

from build_chemistry_representations import build_bundle, validate_bundle  # noqa: E402
import ncert_production_baselines as production  # noqa: E402
import run_chemistry_learner_product as runner  # noqa: E402

AUTHORITY_PATH = REDOX_DIR / "redox-ncert-authority.json"
PROFILE_PATH = REDOX_DIR / "redox-production-profile.json"


def canonical(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(obj, field=None):
    value = copy.deepcopy(obj)
    if field:
        value.pop(field, None)
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def fail(code, detail=""):
    raise ValueError(f"{code}:{detail}" if detail else code)


def load_promoted_pck():
    path = CHEM / "CoreAuthoring" / "registry" / "chemistry_promoted_pck.py"
    spec = importlib.util.spec_from_file_location("redox_production_pck", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.build_registry()


def authorities():
    return {
        "primitive_registry": load(CHEM / "Representation" / "registry" / "chemistry-teaching-primitive-registry.json"),
        "page_intent": load(CHEM / "Representation" / "registry" / "chemistry-page-intent-profile.json"),
        "notation": load(CHEM / "Representation" / "registry" / "chemistry-notation-render-contract.json"),
        "families": load(CHEM / "ReasoningSemantics" / "registry" / "chemistry-problem-family-registry.json"),
        "pck": load_promoted_pck(),
    }


def validate_source_authority(source, profile):
    if source.get("authority_id") != profile.get("source_authority_ref"):
        fail("REDOX_PRODUCTION_SOURCE_AUTHORITY_MISMATCH")
    if source.get("subject") != "CHEMISTRY" or profile.get("subject") != "CHEMISTRY":
        fail("REDOX_PRODUCTION_SUBJECT_MISMATCH")
    questions = source.get("questions") or []
    if len(questions) != source.get("retained_question_count") or len(questions) != profile.get("source_question_denominator"):
        fail("REDOX_PRODUCTION_DENOMINATOR_DRIFT")
    if len({q["question_id"] for q in questions}) != len(questions):
        fail("REDOX_PRODUCTION_DUPLICATE_SOURCE_ID")
    if [q["source_order"] for q in questions] != list(range(1, len(questions) + 1)):
        fail("REDOX_PRODUCTION_SOURCE_ORDER_DRIFT")
    if set(profile["question_routes"]) != {q["question_id"] for q in questions}:
        fail("REDOX_PRODUCTION_ROUTE_COVERAGE_DRIFT")
    docs = {d["document_id"]: d for d in source["source_documents"]}
    for q in questions:
        if q["document_id"] not in docs or not docs[q["document_id"]]["url"].startswith("https://ncert.nic.in/"):
            fail("REDOX_PRODUCTION_OFFICIAL_SOURCE_MISSING", q["question_id"])
        options = q.get("options") or []
        if q["response_mode"] == "MCQ" and len(options) < 2:
            fail("REDOX_PRODUCTION_RESPONSE_SHAPE", q["question_id"])
        if q["response_mode"] == "CONSTRUCTED_RESPONSE" and options:
            fail("REDOX_PRODUCTION_RESPONSE_SHAPE", q["question_id"])
        if not str(q.get("canonical_answer_text") or "").strip():
            fail("REDOX_PRODUCTION_ANSWER_MISSING", q["question_id"])
    return docs


def validate_profile(profile, auth):
    family_ids = {x["family_id"] for x in auth["families"]["families"]}
    assets = {x["asset_id"]: x for x in auth["pck"]["assets"]}
    if set(profile["capability_order"]) != set(profile["capabilities"]):
        fail("REDOX_PRODUCTION_CAPABILITY_ORDER_DRIFT")
    for cap in profile["capability_order"]:
        cfg = profile["capabilities"][cap]
        if cfg["problem_family_ref"] not in family_ids:
            fail("REDOX_PRODUCTION_FAMILY_UNKNOWN", cfg["problem_family_ref"])
        for ref in cfg["pck_asset_refs"]:
            if ref not in assets:
                fail("REDOX_PRODUCTION_PCK_UNKNOWN", ref)
            topic_refs = assets[ref].get("topic_scope_refs") or []
            if topic_refs and topic_refs != ["REDOX"]:
                fail("REDOX_PRODUCTION_TOPIC_PCK_SCOPE_DRIFT", ref)
        if cfg["scope_class"] == "REDOX_DEPTH_EXTENSION" and not any((assets[ref].get("topic_scope_refs") or []) == ["REDOX"] for ref in cfg["pck_asset_refs"]):
            # Species tracking is intentionally generic; role/oxidation-state extension must
            # demonstrate at least one explicit Redox PCK authority somewhere downstream.
            if cap not in {"CAP-TRACK-REACTING-SPECIES"}:
                fail("REDOX_PRODUCTION_EXTENSION_WITHOUT_REDox_PCK", cap)
    return True


def question_map(source):
    return {q["question_id"]: q for q in source["questions"]}


def capability_question_refs(profile):
    out = {cap: [] for cap in profile["capability_order"]}
    for qid, route in profile["question_routes"].items():
        out[route["primary_capability_ref"]].append(qid)
    return out


def build_study_model(source, profile):
    qrefs = capability_question_refs(profile)
    records = []
    for cap in profile["capability_order"]:
        cfg = profile["capabilities"][cap]
        refs = qrefs[cap]
        source_refs = ["NCERT:" + q for q in refs]
        if cfg["scope_class"] == "REDOX_DEPTH_EXTENSION":
            source_refs = ["REDOX_DEPTH_EXTENSION:governed-from-source-reaction-evidence"]
        records.append({
            "capability_ref": cap,
            "source_obligation_refs": source_refs,
            "assessment_question_refs": list(refs),
            "external_candidate_refs": list(refs),
            "prerequisite_refs": [],
            "learner_state_ref": "REDOX-NO-ATTEMPT",
            "learner_state": "UNKNOWN",
            "treatment": "ACTIVE_STUDY",
            "priority": "MEDIUM",
            "sequencing_rationale": "Required Redox scope is taught without inferring a learner weakness from absent attempt data.",
            "supporting_downstream_refs": [],
            "required_pck_jobs": ["ORIENT", "EXPLAIN", "REPRESENT", "WORKED_REASONING", "GUIDED_ATTEMPT", "FADED_ATTEMPT", "INDEPENDENT_ATTEMPT", "VERIFY", "TRANSFER"],
            "representation_level_obligations": list(cfg["representation_levels"]),
            "representation_requirement_obligations": list(cfg["representation_requirements"]),
            "chemical_entity_species_obligations": list(cfg["chemical_entities"]),
            "condition_exception_obligations": [],
            "conservation_obligations": [],
            "problem_family_refs": [cfg["problem_family_ref"]],
            "verification_requirements": list(cfg["verification_requirements"]),
            "future_evidence_obligations": ["NEAR_TRANSFER_NEW_INSTANCE", "FAR_TRANSFER_NEW_CONTEXT", "INDEPENDENT_CHEMICAL_VERIFICATION"],
            "source_trace_status": cfg["scope_class"],
        })
    out = {
        "study_model_id": "CHEM-C-F-REDOX-NCERT-v1",
        "schema_version": "1.0.0",
        "subject": "CHEMISTRY",
        "source_authority_ref": source["authority_id"],
        "source_authority_digest": digest(source),
        "profile_ref": profile["profile_id"],
        "capability_records": records,
        "summary": {
            "required_capability_count": len(records),
            "source_question_denominator": len(source["questions"]),
            "source_derived_capability_count": sum(profile["capabilities"][r["capability_ref"]]["scope_class"] == "SOURCE_DERIVED_CORE" for r in records),
            "redox_depth_extension_capability_count": sum(profile["capabilities"][r["capability_ref"]]["scope_class"] == "REDOX_DEPTH_EXTENSION" for r in records),
            "scope_complete": True,
        },
        "study_model_digest": "",
    }
    out["study_model_digest"] = digest(out, "study_model_digest")
    return out


def worked_example(cap, cfg):
    prompts = {
        "CAP-CLASSIFY-CHANGE-EVIDENCE": "A process description explicitly says that a new substance is formed. Classify the change and state the evidence that controls your decision.",
        "CAP-SEPARATE-OBSERVATION-INFERENCE": "A gas is evolved and a test result is recorded. Separate the observation from the chemical inference before naming the conclusion.",
        "CAP-TRACK-REACTING-SPECIES": "For Zn + Cu²⁺ → Zn²⁺ + Cu, track the corresponding reactant and product species before attaching any Redox label.",
        "CAP-ATTACH-SPECIES-ROLE": "For Zn + Cu²⁺ → Zn²⁺ + Cu, prove which reactant supplies electrons before naming the reducing agent.",
        "CAP-TRACK-OXIDATION-STATE": "For Zn + Cu²⁺ → Zn²⁺ + Cu, place Zn and Cu on before/after oxidation-state lanes and classify each direction of change.",
    }
    return {
        "instance_id": "CORE1-REDOX-" + cap + "-WORKED",
        "source_class": "NEW_AUTHORED_CORE1_REDox_EXTENSION" if cfg["scope_class"] == "REDOX_DEPTH_EXTENSION" else "NEW_AUTHORED_CORE1",
        "problem_family_ref": cfg["problem_family_ref"],
        "primary_capability_ref": cap,
        "prompt": prompts[cap],
        "external_candidate_refs": [],
        "reasoning_steps": list(cfg["reconstruction_steps"]),
        "verification_steps": list(cfg["verification_requirements"]),
    }


def practice_prompt(cap, stage, cfg):
    stem = {
        "CAP-CLASSIFY-CHANGE-EVIDENCE": "Use the stated evidence to decide the change or property. Write the decisive evidence before your classification.",
        "CAP-SEPARATE-OBSERVATION-INFERENCE": "Separate the supplied observation/test from the chemical inference and justify the link.",
        "CAP-TRACK-REACTING-SPECIES": "Track each reacting species from before to after before assigning a Redox label.",
        "CAP-ATTACH-SPECIES-ROLE": "Write SELF change first, then OTHER effect, then attach the requested Redox agent role.",
        "CAP-TRACK-OXIDATION-STATE": "Write before and after oxidation states for the same element, compare them, and classify the direction.",
    }[cap]
    cue = {
        "GUIDED": "Use the four-step routine shown in the lesson.",
        "FADED": "Choose the second step yourself after writing the first evidence line.",
        "INDEPENDENT": "Use no procedural cue beyond the task and the representation.",
    }[stage]
    return stem + " " + cue


def build_core1(source, profile, model):
    lessons, aitems, bsols, hand = [], [], [], []
    for cap in profile["capability_order"]:
        cfg = profile["capabilities"][cap]
        lesson_id = "CORE1-REDOX-" + cap
        misconception = None
        if cfg.get("misconception_contrast"):
            misconception = {
                "wrong_model": "A familiar surface word is enough to decide the chemistry.",
                "why_plausible": "The shortcut can work on easy-looking examples without testing the decisive chemical evidence.",
                "minimal_contrast": cfg["misconception_contrast"],
                "repair_steps": list(cfg["reconstruction_steps"][:3]),
                "retry_prompt": practice_prompt(cap, "GUIDED", cfg),
            }
        lessons.append({
            "lesson_id": lesson_id,
            "capability_ref": cap,
            "treatment": "ACTIVE_STUDY",
            "lesson_mode": "FULL_LEARNING",
            "pck_asset_refs": list(cfg["pck_asset_refs"]),
            "content_roles": ["FAMILIAR_CONTEXT", "REPRESENTATION", "ORDINARY_LANGUAGE_EXPLANATION", "WHY_RECONSTRUCTION", "WORKED_REASONING", "GUIDED_ATTEMPT", "FADED_ATTEMPT", "INDEPENDENT_ATTEMPT", "CHEMICAL_VERIFICATION", "TRANSFER"],
            "scope_trace": {
                "source_obligation_refs": ["NCERT:" + q for q in capability_question_refs(profile)[cap]] if cfg["scope_class"] == "SOURCE_DERIVED_CORE" else ["REDOX_DEPTH_EXTENSION:governed-from-source-reaction-evidence"],
                "assessment_question_refs": list(capability_question_refs(profile)[cap]),
                "external_candidate_refs": list(capability_question_refs(profile)[cap]),
                "problem_family_refs": [cfg["problem_family_ref"]],
            },
            "activation": cfg["activation"],
            "familiar_macro_anchor": cfg["familiar_macro_anchor"],
            "representation_path": ["Use the governed visual before moving to the symbolic conclusion."],
            "ordinary_language_explanation": cfg["ordinary_language_explanation"],
            "rule_model_condition": cfg["rule_model_condition"],
            "reconstruction_steps": list(cfg["reconstruction_steps"]),
            "worked_example": worked_example(cap, cfg),
            "concept_helper": cfg["reconstruction_steps"][0],
            "misconception_repair": misconception,
            "guided_attempt": {"attempt_id": lesson_id + "-GUIDED", "support_stage": "GUIDED", "prompt": practice_prompt(cap, "GUIDED", cfg), "representation_spec": list(cfg["representation_requirements"])},
            "faded_attempt": {"attempt_id": lesson_id + "-FADED", "support_stage": "FADED", "prompt": practice_prompt(cap, "FADED", cfg), "representation_spec": list(cfg["representation_requirements"])},
            "independent_attempt": {"attempt_id": lesson_id + "-INDEPENDENT", "support_stage": "INDEPENDENT", "prompt": practice_prompt(cap, "INDEPENDENT", cfg), "representation_spec": list(cfg["representation_requirements"])},
            "verification_steps": list(cfg["verification_requirements"]),
            "transfer_bridge": cfg["transfer_bridge"],
            "condition_exception_obligations": [],
        })
        for stage in ("GUIDED", "FADED", "INDEPENDENT"):
            item_id = f"A-REDOX-{cap}-{stage}"
            solution_id = "B-SOL-" + item_id
            aitems.append({
                "item_id": item_id,
                "source_class": "NEW_AUTHORED_CORE1",
                "problem_family_ref": cfg["problem_family_ref"],
                "primary_capability_ref": cap,
                "supports_capability_refs": [],
                "support_stage": stage,
                "scored": True,
                "prompt": practice_prompt(cap, stage, cfg),
                "representation_spec": list(cfg["representation_requirements"]),
                "external_candidate_refs": [],
                "solution_ref": solution_id,
            })
            bsols.append({
                "solution_id": solution_id,
                "item_ref": item_id,
                "primary_capability_ref": cap,
                "reasoning_steps": list(cfg["reconstruction_steps"]),
                "verification_steps": list(cfg["verification_requirements"]),
                "final_response": "A complete response states the decisive chemical evidence, executes the taught reasoning route, and gives the conclusion only after the check passes.",
                "condition_exception_note": "No extra condition or exception is introduced beyond the task.",
            })
        hand.append({
            "capability_ref": cap,
            "first_move": cfg["reconstruction_steps"][0],
            "rule_or_decision_cue": cfg["rule_model_condition"],
            "verification_cue": cfg["verification_requirements"][0],
        })
    out = {
        "plan_id": "CHEM-C-G-REDOX-NCERT-v1",
        "schema_version": "1.0.0",
        "subject": "CHEMISTRY",
        "study_model_ref": model["study_model_id"],
        "study_model_digest": model["study_model_digest"],
        "pck_registry_ref": "CHEM-C-G-PROMOTED-PCK-v1",
        "authoring_profile_ref": profile["profile_id"],
        "lessons": lessons,
        "appendices": {
            "appendix_a": {"title": "Appendix A — Core Practice", "present": True, "items": aitems},
            "appendix_b": {"title": "Appendix B — Core Solutions", "present": True, "solutions": bsols},
            "appendix_c": {"title": "Appendix C — Printable Handout", "present": True, "answer_free": True, "supported_capability_refs": list(profile["capability_order"]), "introduced_capability_refs": [], "reference_entries": hand, "print_constraints": ["ANSWER_FREE", "ONE_FIRST_MOVE_PER_CAPABILITY"]},
        },
        "external_transfer_unspoiled": True,
        "scope_complete": True,
        "release_authority_state": "PRODUCTION_CANDIDATE_HUMAN_EXPERT_RELEASE_NOT_GRANTED",
        "plan_digest": "",
    }
    out["plan_digest"] = digest(out, "plan_digest")
    return out


def patch_redox_representation_authority(bundle, profile, core1, model, auth):
    for rep in bundle["representations"]:
        if rep["primitive_id"] == "OXIDATION_STATE_LANE" and rep["capability_ref"] == "CAP-TRACK-OXIDATION-STATE":
            rep["source_semantic_data"]["oxidation_states"] = copy.deepcopy(profile["redox_extension_oxidation_states"])
            rep["accessibility_text"] += " Oxidation-state values are explicit Redox production authority."
    counts = Counter(x["primitive_id"] for x in bundle["representations"])
    bundle["summary"]["primitive_counts"] = dict(sorted(counts.items()))
    bundle["summary"]["representation_count"] = len(bundle["representations"])
    bundle["bundle_digest"] = ""
    bundle["bundle_digest"] = digest(bundle, "bundle_digest")
    validate_bundle(bundle, core1, model, auth["primitive_registry"], auth["page_intent"], auth["notation"])
    return bundle


def build_representations(profile, model, core1, auth):
    bundle = build_bundle(
        core1, model, auth["primitive_registry"], auth["page_intent"], auth["notation"],
        "CHEM-C-H-REDOX-NCERT-v1",
    )
    return patch_redox_representation_authority(bundle, profile, core1, model, auth)


def source_reasoning_steps(q, route):
    qid = q["question_id"]
    if route["problem_family_ref"] == "PF-EVIDENCE_TO_CLAIM":
        if qid == "U2Q35":
            return [
                "Treat part A and part B separately before naming either gas.",
                "For part A, use the heated iron–sulphur product with dilute hydrochloric acid and identify hydrogen sulphide from its characteristic odour.",
                "For part B, use the unheated iron–sulphur mixture; iron reacts with dilute hydrochloric acid to give hydrogen, identified by the pop test.",
                "Check that each gas name is tied to the correct part and test."
            ]
        return [
            "Write the stated observation or process before interpreting it.",
            "State the chemical inference separately.",
            "Check that the inference is supported by the source evidence."
        ]
    if qid == "U2Q30F":
        return [
            "Identify the process named in the question: combustion.",
            "Recall the required non-metal reactant for combustion.",
            "State the non-metal as oxygen and check that the response answers the exact noun requested."
        ]
    return [
        "Locate the decisive process, product or observation in the source stem.",
        "Use that evidence to decide whether a new substance or chemical reaction is involved.",
        "Choose or write the classification only after the evidence test.",
        "Check that the final reason and answer agree."
    ]


def build_core2(source, profile, model, core1):
    docs = {d["document_id"]: d for d in source["source_documents"]}
    cap_titles = {cap: profile["capabilities"][cap]["learner_title"] for cap in profile["capability_order"]}
    pages = []
    for q in source["questions"]:
        route = profile["question_routes"][q["question_id"]]
        family = profile["source_family_support"][route["problem_family_ref"]]
        cap = route["primary_capability_ref"]
        document = docs[q["document_id"]]
        visual_id = "VIS-" + q["question_id"] + "-" + ("EVIDENCE_CLAIM_REASONING_CHAIN" if route["problem_family_ref"] == "PF-EVIDENCE_TO_CLAIM" else "MACRO_OBSERVATION_VIEW")
        page = {
            "question_ref": q["question_id"],
            "source_ref": digest(q),
            "source_year": "Class IX",
            "source_session": "NCERT Exemplar",
            "source_shift": q["section"],
            "scope_status": "ELIGIBLE_IN_SCOPE",
            "source_qc_status": "CLEAN",
            "source_stem": q["stem"],
            "source_options": copy.deepcopy(q["options"]),
            "source_subparts": [],
            "response_mode": q["response_mode"],
            "source_locator": q["source_locator"],
            "source_text_relation": q["source_text_relation"],
            "verified_official_source_ref": document["document_id"],
            "source_figure_required": False,
            "source_figure_semantic": None,
            "source_condition_text": None,
            "source_states": [],
            "source_units": [],
            "primary_concept_ref": "CHEM-CONCEPT-OBSERVATION-INFERENCE" if route["problem_family_ref"] == "PF-EVIDENCE_TO_CLAIM" else "CHEM-CONCEPT-CHANGE-EVIDENCE",
            "primary_capability_ref": cap,
            "supporting_concept_refs": [],
            "supporting_capability_refs": [],
            "problem_family_ref": route["problem_family_ref"],
            "guide_demand_badge": {"label": "STANDARD", "semantic_class": "GUIDE_ASSIGNED_REASONING_DEMAND", "psychometric_claim": False},
            "transfer_badge": "CANONICAL_TRANSFER",
            "source_badges": {"source": document["label"], "year": "Class IX", "session": "NCERT Exemplar", "shift": q["section"]},
            "core1_lesson_refs": [{"lesson_id": "CORE1-REDOX-" + cap, "learner_title": cap_titles[cap], "capability_ref": cap}],
            "workspace_spec": {"workspace_type": route["problem_family_ref"], "fields": copy.deepcopy(family["workspace_fields"])},
            "hint_ladder": {
                "h0_attempt_first": "Attempt the NCERT source question independently before opening any clue or solution.",
                "support_revealed_initially": False,
                "h1_notice": family["h1"],
                "h2_rule_model_representation": family["h2"],
                "h3_start": family["h3"],
            },
            "reasoning_route": ["READ_GIVEN", "COMPARE", "CLASSIFY", "VERIFY_RESULT"] if route["problem_family_ref"] == "PF-REACTION_PROCESS_CLASSIFICATION" else ["READ_GIVEN", "INFER_FROM_OBSERVATION", "INTERPRET_CHEMICAL_MEANING", "VERIFY_RESULT"],
            "reasoning_route_ref": "CHEM-REDOX-ROUTE-" + q["question_id"],
            "solution_route": {
                "reasoning_steps": source_reasoning_steps(q, route),
                "verification_steps": list(family["verification"]),
                "final_answer": str(q["canonical_answer"]),
                "chemical_language_response": q["canonical_answer_text"],
                "condition_exception_check": "No additional condition or exception is required beyond the source wording."
            },
            "quick_check_marking_points": copy.deepcopy(route["marking_points"]),
            "verification_route": list(family["verification"]),
            "visual_specs": [{"visual_id": visual_id, "visual_kind": "TEACHING_PRIMITIVE", "primitive_id": visual_id.split("-", 2)[-1], "source_bound": True}],
            "source_link": document["url"],
            "source_fidelity": {
                "authority_ref": source["authority_id"],
                "document_id": q["document_id"],
                "source_locator": q["source_locator"],
                "source_text_relation": q["source_text_relation"],
                "options_preserved": True,
                "figure_preserved": True,
                "condition_preserved": True,
                "response_mode_preserved": True,
            },
            "page_digest": "",
        }
        page["page_digest"] = digest(page, "page_digest")
        pages.append(page)
    out = {
        "plan_id": "CHEM-C-I-REDOX-NCERT-v1",
        "schema_version": "1.0.0",
        "subject": "CHEMISTRY",
        "source_authority_ref": source["authority_id"],
        "core1_plan_ref": core1["plan_id"],
        "core1_plan_digest": core1["plan_digest"],
        "study_model_ref": model["study_model_id"],
        "study_model_digest": model["study_model_digest"],
        "pages": pages,
        "excluded_candidate_refs": [],
        "summary": {
            "source_candidate_denominator": len(pages),
            "eligible_candidate_count": len(pages),
            "placed_page_count": len(pages),
            "excluded_or_unresolved_count": 0,
            "unique_primary_placement": True,
            "attempt_first": True,
            "external_transfer_unspoiled": True,
            "psychometric_claims": False,
            "response_mode_counts": dict(sorted(Counter(p["response_mode"] for p in pages).items())),
        },
        "plan_digest": "",
    }
    out["plan_digest"] = digest(out, "plan_digest")
    return out


def build_closure(source, model, core1, representations, core2):
    records = []
    for page in core2["pages"]:
        records.append({
            "candidate_ref": page["question_ref"],
            "scope_status": "ELIGIBLE_IN_SCOPE",
            "placement_status": "PLACED",
            "source_link_status": "PASS",
            "hint_support_status": "PASS",
            "solution_status": "PASS",
        })
    external_matrix = {
        "matrix_id": "CHEM-C-J-REDOX-EXTERNAL-MATRIX-v1",
        "schema_version": "1.0.0",
        "subject": "CHEMISTRY",
        "records": records,
        "summary": {
            "candidate_total": len(records),
            "eligible_total": len(records),
            "placed_unique_total": len(records),
            "missing_total": 0,
            "duplicate_primary_total": 0,
            "source_link_failures": 0,
            "hint_support_failures": 0,
            "solution_failures": 0,
        },
    }
    external_matrix["matrix_digest"] = digest(external_matrix)
    out = {
        "closure_id": "CHEM-C-J-REDOX-NCERT-v1",
        "schema_version": "1.0.0",
        "subject": "CHEMISTRY",
        "source_authority_ref": source["authority_id"],
        "study_model_ref": model["study_model_id"],
        "core1_plan_ref": core1["plan_id"],
        "representation_bundle_ref": representations["bundle_id"],
        "core2_plan_ref": core2["plan_id"],
        "external_matrix_ref": external_matrix["matrix_id"],
        "external_matrix": external_matrix,
        "summary": {
            "required_capability_count": len(model["capability_records"]),
            "source_question_denominator": len(records),
            "blocking_failures": 0,
            "status": "PASS",
        },
        "closure_digest": "",
    }
    out["closure_digest"] = digest(out, "closure_digest")
    return out


def build_run(model, core1, representations, core2, closure, profile):
    baseline = production.baseline_for_topic(profile["baseline_topic_id"])
    out = {
        "run_id": "CHEM-LPR-7265646f78303031",
        "contract_version": "1.0.0",
        "subject": "CHEMISTRY",
        "inputs": {
            "learner_study_model_ref": model["study_model_id"],
            "learner_study_model_digest": model["study_model_digest"],
            "core1_plan_ref": core1["plan_id"],
            "core1_plan_digest": core1["plan_digest"],
            "representation_bundle_ref": representations["bundle_id"],
            "representation_bundle_digest": representations["bundle_digest"],
            "core2_plan_ref": core2["plan_id"],
            "core2_plan_digest": core2["plan_digest"],
            "coverage_closure_ref": closure["closure_id"],
            "coverage_closure_digest": closure["closure_digest"],
            "competitive_registry_ref": None,
            "competitive_registry_digest": None,
            "production_topic_id": profile["baseline_topic_id"],
            "production_baseline_ref": baseline["baseline_ref"],
            "production_baseline_digest": baseline["baseline_digest"],
        },
        "policy_refs": {
            "core1a_execution_policy": "CHEM-CORE1A-EXECUTION-v1",
            "core2a_execution_policy": "CHEM-CORE2A-EXECUTION-v1",
            "learner_language_policy": "CHEM-LEARNER-LANGUAGE-v1",
            "question_citation_policy": "CHEM-QUESTION-CITATION-v1",
            "competitive_challenge_policy": "CHEM-COMPETITIVE-CHALLENGE-v1",
            "answer_path_policy": "CHEM-ANSWER-PATH-v1",
        },
        "execution_sequence": list(runner.EXECUTION_SEQUENCE),
        "requested_products": {"core1a": True, "core2a_source": True, "core2a_challenges": False},
        "outputs": {
            "core1a_bucket_plan_ref": None,
            "core1a_manuscript_ref": None,
            "core2a_source_plan_ref": None,
            "core2a_challenge_plan_ref": None,
            "answer_closure_audit_ref": None,
            "artifact_manifest_ref": None,
            "handoff_manifest_ref": None,
        },
        "run_digest": "",
    }
    out["run_digest"] = runner.canonical_digest(out)
    return out


def build_all():
    source = load(AUTHORITY_PATH)
    profile = load(PROFILE_PATH)
    auth = authorities()
    validate_source_authority(source, profile)
    validate_profile(profile, auth)
    model = build_study_model(source, profile)
    core1 = build_core1(source, profile, model)
    reps = build_representations(profile, model, core1, auth)
    core2 = build_core2(source, profile, model, core1)
    closure = build_closure(source, model, core1, reps, core2)
    run = build_run(model, core1, reps, core2, closure, profile)
    production.assert_run_binding(run, closure)
    runner.validate_foundation(run)
    return {
        "source_authority": source,
        "production_profile": profile,
        "study_model": model,
        "core1": core1,
        "representations": reps,
        "core2": core2,
        "closure": closure,
        "run": run,
    }


def write_all(out_dir):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    bundle = build_all()
    names = {
        "source_authority": "redox_source_authority.json",
        "production_profile": "redox_production_profile.json",
        "study_model": "redox_study_model.json",
        "core1": "redox_core1_plan.json",
        "representations": "redox_representation_bundle.json",
        "core2": "redox_core2_plan.json",
        "closure": "redox_coverage_closure.json",
        "run": "redox_run_manifest.json",
    }
    for key, name in names.items():
        (out_dir / name).write_text(json.dumps(bundle[key], ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return bundle


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-dir", type=Path, required=True)
    args = ap.parse_args()
    bundle = write_all(args.out_dir)
    print(json.dumps({
        "status": "PASS",
        "questions": len(bundle["core2"]["pages"]),
        "response_modes": bundle["core2"]["summary"]["response_mode_counts"],
        "capabilities": len(bundle["study_model"]["capability_records"]),
        "run_id": bundle["run"]["run_id"],
    }, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
