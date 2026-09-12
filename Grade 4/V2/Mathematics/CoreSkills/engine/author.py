"""Primary Math V2 deterministic authoring/concept engine.

This module intentionally does not parse arbitrary mathematics prose heuristically.
A semantic extraction layer (agent/model/source parser) supplies normalized
QuestionEvidence under each question's ``evidence`` field.  This engine validates
those claims against canonical registries and deterministically assembles the
#329 SkillModel / Core1 / Core2 / RepresentationPlan seams.

It imports no publication or rendering code.
"""
from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping

CORE_SKILLS_ROOT = Path(__file__).resolve().parents[1]
REGISTRY_ROOT = CORE_SKILLS_ROOT / "registry"

SCOPE_BASES = {
    "CURRICULUM_CONFIRMED",
    "QUESTION_SET_OBSERVED",
    "SCHOOL_CLASSWORK_OBSERVED",
    "COMMON_G4_5_CAPABILITY",
    "CURRICULUM_OVERLAY",
    "EXTENSION",
    "STRETCH",
    "MAPPING_PENDING",
    "SOURCE_NOT_PROVIDED",
}
CONCEPT_MODES = {
    "INTRODUCE", "CONNECT", "REPAIR", "PROBE", "PRACTISE",
    "RETRIEVE", "TRANSFER", "VERIFY", "REFERENCE",
}


class AuthoringError(ValueError):
    """Fail-closed authoring error with a stable falsifier code."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _slug(value: str) -> str:
    value = re.sub(r"[^A-Za-z0-9]+", "-", value.strip()).strip("-")
    return value.upper() or "UNNAMED"


class RegistryIndex:
    def __init__(self) -> None:
        cap = _load_json(REGISTRY_ROOT / "capability_registry.json")
        pf = _load_json(REGISTRY_ROOT / "problem_family_registry.json")
        rt = _load_json(REGISTRY_ROOT / "representation_translation_registry.json")
        self.capabilities = {x["id"]: x for x in cap["capabilities"]}
        self.problem_families = {x["id"]: x for x in pf["problem_families"]}
        self.translations = {x["id"]: x for x in rt["translations"]}


def _as_list(value: Any) -> List[Any]:
    if value is None:
        return []
    return list(value)


def _require_refs(refs: Iterable[str], allowed: Mapping[str, Any], code: str, owner: str) -> None:
    missing = sorted({r for r in refs if r not in allowed})
    if missing:
        raise AuthoringError(code, f"{owner} contains unknown refs: {missing}")


def validate_question_evidence(evidence: Mapping[str, Any], registry: RegistryIndex) -> None:
    required = [
        "question_ref", "concept_key", "concept_title", "scope_basis",
        "capability_refs", "problem_family_refs", "representation_requirements",
    ]
    missing_fields = [k for k in required if k not in evidence]
    if missing_fields:
        raise AuthoringError("QUESTION_EVIDENCE_INCOMPLETE", f"missing fields {missing_fields}")

    basis = evidence["scope_basis"]
    if basis not in SCOPE_BASES:
        raise AuthoringError("UNKNOWN_SCOPE_BASIS", f"{evidence['question_ref']}: {basis}")
    if basis == "CURRICULUM_CONFIRMED" and not evidence.get("authority_ref"):
        raise AuthoringError(
            "CURRICULUM_CONFIRMED_WITHOUT_AUTHORITY_REF",
            f"{evidence['question_ref']} claims curriculum authority without authority_ref",
        )
    if basis in {"QUESTION_SET_OBSERVED", "SCHOOL_CLASSWORK_OBSERVED"} and evidence.get("universal_grade_claim"):
        raise AuthoringError(
            "QUESTION_OBSERVED_SKILL_PROMOTED_TO_UNIVERSAL_GRADE_SCOPE",
            f"{evidence['question_ref']} promotes observed scope to universal grade truth",
        )

    capability_refs = _as_list(evidence.get("capability_refs"))
    prereq_refs = _as_list(evidence.get("prerequisite_refs"))
    problem_refs = _as_list(evidence.get("problem_family_refs"))
    translation_refs = _as_list(evidence.get("translation_refs"))
    _require_refs(capability_refs, registry.capabilities, "UNKNOWN_CAPABILITY_REF", evidence["question_ref"])
    _require_refs(prereq_refs, registry.capabilities, "UNKNOWN_CAPABILITY_REF", evidence["question_ref"])
    _require_refs(problem_refs, registry.problem_families, "UNKNOWN_PROBLEM_FAMILY_REF", evidence["question_ref"])
    _require_refs(translation_refs, registry.translations, "UNKNOWN_REPRESENTATION_TRANSLATION_REF", evidence["question_ref"])

    cap_set = set(capability_refs)
    for rt_ref in translation_refs:
        required_caps = set(registry.translations[rt_ref].get("capability_refs", []))
        if not required_caps.issubset(cap_set):
            raise AuthoringError(
                "REPRESENTATION_BRIDGE_CAPABILITY_GAP",
                f"{evidence['question_ref']} uses {rt_ref} without capabilities {sorted(required_caps - cap_set)}",
            )

    reps = _as_list(evidence.get("representation_requirements"))
    if not reps:
        raise AuthoringError("REPRESENTATION_REQUIREMENT_MISSING", evidence["question_ref"])
    for rep in reps:
        for field in ("representation_id", "role", "primitive_kind", "semantic_params", "validator_refs", "provenance"):
            if field not in rep:
                raise AuthoringError("REPRESENTATION_REQUIREMENT_INCOMPLETE", f"{evidence['question_ref']} missing {field}")
        if not rep.get("validator_refs"):
            raise AuthoringError("REPRESENTATION_WITHOUT_VALIDATOR", rep["representation_id"])


def _work_records(primary_input: Mapping[str, Any]) -> List[Dict[str, Any]]:
    workout = primary_input.get("student_workout")
    if not workout:
        return []
    return list(workout.get("work_evidence", []))


def _validate_work_record(work: Mapping[str, Any], concept_keys: set[str]) -> None:
    if "work_evidence_id" not in work or "concept_key" not in work:
        raise AuthoringError("WORK_EVIDENCE_INCOMPLETE", "work evidence requires work_evidence_id and concept_key")
    if work["concept_key"] not in concept_keys:
        raise AuthoringError("WORK_EVIDENCE_UNKNOWN_CONCEPT", work["concept_key"])
    if work.get("teacher_correction_as_child_original"):
        raise AuthoringError("TEACHER_CORRECTION_COUNTED_AS_CHILD_EVIDENCE", work["work_evidence_id"])
    if work.get("final_status") == "INCORRECT" and work.get("correct_substeps") and work.get("correct_substeps_preserved") is False:
        raise AuthoringError("INCORRECT_FINAL_ERASES_CORRECT_SUBSTEP", work["work_evidence_id"])
    if work.get("ambiguity_observed") and work.get("ambiguity_preserved") is False:
        raise AuthoringError("AMBIGUOUS_MAPPING_SILENTLY_FORCED", work["work_evidence_id"])

    diagnostic = work.get("diagnostic")
    if diagnostic:
        hypotheses = list(diagnostic.get("competing_hypotheses", []))
        probe = diagnostic.get("probe")
        if not (2 <= len(hypotheses) <= 3):
            raise AuthoringError("PROBE_MODE_WITHOUT_COMPETING_HYPOTHESES", work["work_evidence_id"])
        if not probe or not probe.get("outcome_rules"):
            raise AuthoringError("PROBE_MODE_WITHOUT_DIAGNOSTIC_PROBE", work["work_evidence_id"])
        if any(h.get("durable_trait") for h in hypotheses):
            raise AuthoringError("ERROR_SIGNATURE_PROMOTED_TO_DURABLE_LEARNER_TRAIT", work["work_evidence_id"])


def _choose_mode(work: Mapping[str, Any] | None, has_translation: bool) -> str:
    if work is None:
        return "CONNECT" if has_translation else "INTRODUCE"
    if work.get("diagnostic"):
        return "PROBE"
    if work.get("bounded_error_signature"):
        return "REPAIR"
    if work.get("final_status") == "CORRECT" and work.get("support_level", "H0") in {"H0", "NONE"}:
        return "VERIFY"
    return "CONNECT" if has_translation else "INTRODUCE"


def _topic_labels(primary_input: Mapping[str, Any]) -> set[str]:
    # #329 defines topic_hints as labels/strings. They are allowed to label scope,
    # never to add/override canonical capabilities.
    return {str(x).strip() for x in (primary_input.get("topic_hints") or []) if str(x).strip()}


def author(primary_input: Mapping[str, Any]) -> Dict[str, Any]:
    """Build canonical authoring outputs from normalized evidence.

    Questions must carry an ``evidence`` object.  This is deliberate: raw text may
    be retained for provenance, but semantic extraction is an upstream reasoning
    step and may not be replaced by keyword heuristics here.
    """
    if primary_input.get("schema_version") != "1.0.0" or not primary_input.get("input_id"):
        raise AuthoringError("PRIMARY_INPUT_INVALID", "schema_version=1.0.0 and input_id are required")
    question_set = primary_input.get("question_set") or {}
    questions = list(question_set.get("questions") or [])
    if not questions:
        raise AuthoringError("QUESTION_SET_REQUIRED", "question_set.questions must be non-empty")

    registry = RegistryIndex()
    evidence_rows: List[Dict[str, Any]] = []
    for q in questions:
        evidence = q.get("evidence")
        if not evidence:
            raise AuthoringError(
                "SEMANTIC_EVIDENCE_REQUIRED",
                f"question {q.get('question_ref', '<unknown>')} has raw content but no normalized QuestionEvidence",
            )
        validate_question_evidence(evidence, registry)
        evidence_rows.append(dict(evidence))

    grouped: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for row in evidence_rows:
        grouped[row["concept_key"]].append(row)
    concept_keys = set(grouped)

    works = _work_records(primary_input)
    for work in works:
        _validate_work_record(work, concept_keys)
    work_by_concept: Dict[str, Dict[str, Any]] = {w["concept_key"]: w for w in works}

    topic_labels = _topic_labels(primary_input)
    unresolved: List[Dict[str, Any]] = []
    concepts: List[Dict[str, Any]] = []
    concept_ref_by_key: Dict[str, str] = {}
    concept_source_refs: Dict[str, List[str]] = {}
    concept_translation_refs: Dict[str, List[str]] = {}

    for concept_key in sorted(grouped):
        rows = grouped[concept_key]
        concept_id = f"PMV2-CONCEPT-{_slug(concept_key)}"
        concept_ref_by_key[concept_key] = concept_id
        titles = {r["concept_title"] for r in rows}
        title = sorted(titles)[0]
        # Topic hints may label a concept only when they literally match its key/title;
        # they never mutate capabilities/scope.
        matching_labels = sorted(x for x in topic_labels if x.lower() in {concept_key.lower(), title.lower()})
        if matching_labels:
            title = matching_labels[0]

        bases = {r["scope_basis"] for r in rows}
        if len(bases) == 1:
            scope_basis = next(iter(bases))
        else:
            scope_basis = "MAPPING_PENDING"
            unresolved.append({
                "state": "MAPPING_PENDING",
                "description": f"{concept_key} has conflicting scope bases: {sorted(bases)}",
            })
        authorities = {r.get("authority_ref") for r in rows if r.get("authority_ref")}
        authority_ref = sorted(authorities)[0] if len(authorities) == 1 else None
        if scope_basis == "CURRICULUM_CONFIRMED" and authority_ref is None:
            raise AuthoringError("CURRICULUM_CONFIRMED_WITHOUT_AUTHORITY_REF", concept_key)

        capabilities = sorted({x for r in rows for x in r.get("capability_refs", [])})
        prereqs = sorted({x for r in rows for x in r.get("prerequisite_refs", [])})
        problem_refs = sorted({x for r in rows for x in r.get("problem_family_refs", [])})
        rep_refs = sorted({rep["representation_id"] for r in rows for rep in r.get("representation_requirements", [])})
        translation_refs = sorted({x for r in rows for x in r.get("translation_refs", [])})
        concept_translation_refs[concept_key] = translation_refs
        source_refs = sorted({
            ref for r in rows for ref in ([r.get("question_ref")] + list(r.get("source_refs", []))) if ref
        })
        concept_source_refs[concept_key] = source_refs

        work = work_by_concept.get(concept_key)
        error_refs = [work["bounded_error_signature"]] if work and work.get("bounded_error_signature") else []
        concepts.append({
            "concept_id": concept_id,
            "title": title,
            "description": f"Authoring concept assembled from grounded evidence for {title}.",
            "scope_basis": scope_basis,
            "authority_ref": authority_ref,
            "universal_grade_claim": False,
            "learning_object_refs": [],
            "capability_refs": capabilities,
            "prerequisite_refs": prereqs,
            "representation_refs": rep_refs,
            "problem_family_refs": problem_refs,
            "invariant_refs": sorted({x for r in rows for x in r.get("invariant_refs", [])}),
            "error_signature_refs": error_refs,
            "transfer_dimension_refs": sorted({x for r in rows for x in r.get("transfer_dimension_refs", [])}),
        })
        for r in rows:
            for amb in r.get("ambiguity", []):
                unresolved.append({"state": "AMBIGUOUS", "description": f"{r['question_ref']}: {amb}"})

    representation_requirements: List[str] = sorted({
        rep["representation_id"] for r in evidence_rows for rep in r.get("representation_requirements", [])
    })
    problem_family_refs = sorted({x for c in concepts for x in c["problem_family_refs"]})
    quantity_structures = [r["quantity_structure"] for r in evidence_rows if r.get("quantity_structure")]
    work_refs = sorted(w["work_evidence_id"] for w in works)
    diagnostic_refs = sorted(
        w["diagnostic"].get("diagnostic_id", f"DIAG-{_slug(w['work_evidence_id'])}")
        for w in works if w.get("diagnostic")
    )

    skill_model = {
        "schema_version": "1.0.0",
        "model_id": f"PMV2-SKILL-{_slug(primary_input['input_id'])}",
        "input_ref": primary_input["input_id"],
        "concepts": concepts,
        "prerequisite_edges": [],
        "problem_family_refs": problem_family_refs,
        "representation_requirements": representation_requirements,
        "quantity_structures": quantity_structures,
        "reasoning_requirements": ["EXPLAIN_RELATIONSHIPS", "CHECK_REASONABLENESS"],
        "practice_obligations": ["CONTROLLED_VARIATION", "NO_NUMBER_SUBSTITUTION_ONLY"],
        "retrieval_obligations": ["FRESH_RETRIEVAL"],
        "transfer_obligations": ["CHANGE_CONTEXT_OR_REPRESENTATION"],
        "work_evidence_refs": work_refs,
        "diagnostic_refs": diagnostic_refs,
        "unresolved": unresolved,
    }

    core1_modules: List[Dict[str, Any]] = []
    core2_modules: List[Dict[str, Any]] = []
    mode_by_concept: Dict[str, str] = {}
    for concept_key in sorted(grouped):
        cid = concept_ref_by_key[concept_key]
        concept = next(c for c in concepts if c["concept_id"] == cid)
        work = work_by_concept.get(concept_key)
        mode = _choose_mode(work, bool(concept_translation_refs[concept_key]))
        if mode not in CONCEPT_MODES:
            raise AuthoringError("UNKNOWN_CONCEPT_MODE", mode)
        mode_by_concept[concept_key] = mode
        evidence_refs = [work["work_evidence_id"]] if work else []
        module_id = f"C1-{_slug(concept_key)}"
        support_level = "H1" if mode == "REPAIR" else "H0"
        fade_mode = "PARTIAL" if mode == "REPAIR" else "NONE"
        core1_modules.append({
            "module_id": module_id,
            "concept_ref": cid,
            "concept_mode": mode,
            "objective": f"Build, connect, and check {concept['title']} using grounded representations.",
            "prerequisite_refs": concept["prerequisite_refs"],
            "representation_refs": concept["representation_refs"],
            "learner_action": "Represent the relationship, solve or explain it, then check the result.",
            "support_level": support_level,
            "fade_mode": fade_mode,
            "independent_check_required": mode != "PROBE",
            "core1_module_ref": None,
            "hint_ref": None,
            "practice_batch_type": "NOT_APPLICABLE",
            "source_refs": concept_source_refs[concept_key],
            "evidence_refs": evidence_refs,
        })

        if mode == "PROBE":
            core2_modules.append({
                "module_id": f"C2-{_slug(concept_key)}-PROBE",
                "concept_ref": cid,
                "concept_mode": "PROBE",
                "objective": "Run the smallest discriminating probe before choosing repair practice.",
                "prerequisite_refs": concept["prerequisite_refs"],
                "representation_refs": concept["representation_refs"],
                "learner_action": "Attempt the diagnostic probe independently.",
                "support_level": "H0",
                "fade_mode": "NONE",
                "independent_check_required": False,
                "core1_module_ref": module_id,
                "hint_ref": None,
                "practice_batch_type": "NOT_APPLICABLE",
                "source_refs": concept_source_refs[concept_key],
                "evidence_refs": evidence_refs,
            })
        else:
            core2_modules.extend([
                {
                    "module_id": f"C2-{_slug(concept_key)}-BUILD",
                    "concept_ref": cid,
                    "concept_mode": "PRACTISE",
                    "objective": f"Build reliable use of {concept['title']} with controlled variation.",
                    "prerequisite_refs": concept["prerequisite_refs"],
                    "representation_refs": concept["representation_refs"],
                    "learner_action": "Try independently; use H1→H2→H3 only if needed, then complete a fresh H0 item.",
                    "support_level": "H0",
                    "fade_mode": "FULL",
                    "independent_check_required": True,
                    "core1_module_ref": module_id,
                    "hint_ref": f"HINT-{_slug(concept_key)}",
                    "practice_batch_type": "BUILD",
                    "source_refs": concept_source_refs[concept_key],
                    "evidence_refs": evidence_refs,
                },
                {
                    "module_id": f"C2-{_slug(concept_key)}-TRANSFER",
                    "concept_ref": cid,
                    "concept_mode": "TRANSFER",
                    "objective": f"Transfer {concept['title']} under a changed context or representation.",
                    "prerequisite_refs": concept["prerequisite_refs"],
                    "representation_refs": concept["representation_refs"],
                    "learner_action": "Choose a useful representation and solve a non-number-substitution transfer item.",
                    "support_level": "H0",
                    "fade_mode": "NONE",
                    "independent_check_required": True,
                    "core1_module_ref": module_id,
                    "hint_ref": f"HINT-{_slug(concept_key)}",
                    "practice_batch_type": "TRANSFER",
                    "source_refs": concept_source_refs[concept_key],
                    "evidence_refs": evidence_refs,
                },
            ])

    core1_plan = {
        "schema_version": "1.0.0",
        "plan_id": f"PMV2-C1-{_slug(primary_input['input_id'])}",
        "product": "CORE1_STUDY_GUIDE",
        "skill_model_ref": skill_model["model_id"],
        "modules": core1_modules,
    }
    core2_plan = {
        "schema_version": "1.0.0",
        "plan_id": f"PMV2-C2-{_slug(primary_input['input_id'])}",
        "product": "CORE2_COMPANION",
        "skill_model_ref": skill_model["model_id"],
        "modules": core2_modules,
    }

    reps_by_id: Dict[str, Dict[str, Any]] = {}
    rep_concept: Dict[str, str] = {}
    for row in evidence_rows:
        cid = concept_ref_by_key[row["concept_key"]]
        for rep in row["representation_requirements"]:
            rid = rep["representation_id"]
            candidate = {
                "representation_id": rid,
                "concept_ref": cid,
                "role": rep["role"],
                "primitive_kind": rep["primitive_kind"],
                "semantic_params": rep["semantic_params"],
                "validator_refs": list(rep["validator_refs"]),
                "fade_modes": list(rep.get("fade_modes", ["NONE"])),
                "provenance": rep["provenance"],
            }
            if rid in reps_by_id and reps_by_id[rid] != candidate:
                raise AuthoringError("REPRESENTATION_ID_CONFLICT", rid)
            reps_by_id[rid] = candidate
            rep_concept[rid] = cid

    representation_plan = {
        "schema_version": "1.0.0",
        "plan_id": f"PMV2-REP-{_slug(primary_input['input_id'])}",
        "skill_model_ref": skill_model["model_id"],
        "representations": [reps_by_id[k] for k in sorted(reps_by_id)],
    }

    diagnostic_objects = [w["diagnostic"] for w in works if w.get("diagnostic")]
    return {
        "schema_version": "1.0.0",
        "input_ref": primary_input["input_id"],
        "skill_model": skill_model,
        "core1_plan": core1_plan,
        "core2_plan": core2_plan,
        "representation_plan": representation_plan,
        "diagnostic_objects": diagnostic_objects,
        "authoring_trace": {
            "question_refs": [r["question_ref"] for r in evidence_rows],
            "work_evidence_refs": work_refs,
            "topic_hints": sorted(topic_labels),
            "concept_modes": {concept_ref_by_key[k]: v for k, v in mode_by_concept.items()},
            "publisher_dependency": False,
        },
    }


def author_file(input_path: Path, output_path: Path) -> None:
    result = author(_load_json(input_path))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
