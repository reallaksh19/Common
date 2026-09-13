#!/usr/bin/env python3
"""Build the governed Chemistry Core (1A) bucket plan from C-F/C-G/C-H/C-I.

This engine is deliberately semantic. It does not render pages and it does not
invent learner state, chemistry, source questions, problem families, or visual
meaning. It groups Core1 capabilities only through the canonical Chemistry
problem-family registry and closes Core2 H1/H2/H3 support against already-taught
Core1A atoms / C-H representations.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

STAGES = [
    "SEE_THE_PHENOMENON",
    "SEE_THE_PARTICLES",
    "SEE_THE_CHEMICAL_STRUCTURE",
    "SEE_THE_SYMBOLS",
    "CONNECT_THE_QUANTITIES",
    "DO_THE_CHEMISTRY",
    "VERIFY_THE_RESULT",
    "CONNECT_TO_CORE2",
]

FIRST_MOVE_KINDS = {
    "RECONSTRUCTION_STEP",
    "WORKED_REASONING",
    "RULE_MODEL_CONDITION",
    "TRANSFER_BRIDGE",
}


def canonical(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(obj, field=None):
    payload = copy.deepcopy(obj)
    if field:
        payload.pop(field, None)
    return hashlib.sha256(canonical(payload).encode("utf-8")).hexdigest()


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def uniq(values):
    out = []
    for value in values:
        if value not in out:
            out.append(value)
    return out


def fail(code, detail=""):
    raise ValueError(f"{code}: {detail}" if detail else code)


def family_tables(registry):
    by_id = {row["family_id"]: row for row in registry["families"]}
    aliases = registry.get("question_family_aliases", {})
    defaults = registry.get("capability_family_defaults", {})
    return by_id, aliases, defaults


def canonical_family(ref, by_id, aliases):
    if ref in by_id:
        return ref
    if ref in aliases and aliases[ref] in by_id:
        return aliases[ref]
    return None


def primary_family_for_capability(capability_ref, record, by_id, aliases, defaults):
    default = defaults.get(capability_ref)
    if default in by_id:
        family = by_id[default]
        if capability_ref not in family.get("canonical_capability_refs", []):
            fail("CORE1A_BUCKET_INVARIANT_UNGROUNDED", capability_ref + ": default family does not own capability")
        return default
    candidates = []
    for raw in record.get("problem_family_refs", []):
        resolved = canonical_family(raw, by_id, aliases)
        if resolved and capability_ref in by_id[resolved].get("canonical_capability_refs", []):
            candidates.append(resolved)
    candidates = uniq(candidates)
    if len(candidates) != 1:
        fail("CORE1A_BUCKET_INVARIANT_UNGROUNDED", capability_ref + ": no unique canonical problem family")
    return candidates[0]


def validate_upstream_bindings(study_model, core1, representations, core2):
    if core1.get("study_model_ref") != study_model.get("study_model_id"):
        fail("CORE1A_UPSTREAM_BINDING_MISMATCH", "Core1 study-model ref")
    if core1.get("study_model_digest") != study_model.get("study_model_digest"):
        fail("CORE1A_UPSTREAM_BINDING_MISMATCH", "Core1 study-model digest")
    if representations.get("study_model_ref") != study_model.get("study_model_id"):
        fail("CORE1A_UPSTREAM_BINDING_MISMATCH", "C-H study-model ref")
    if representations.get("study_model_digest") != study_model.get("study_model_digest"):
        fail("CORE1A_UPSTREAM_BINDING_MISMATCH", "C-H study-model digest")
    if representations.get("core1_plan_ref") != core1.get("plan_id"):
        fail("CORE1A_UPSTREAM_BINDING_MISMATCH", "C-H Core1 ref")
    if representations.get("core1_plan_digest") != core1.get("plan_digest"):
        fail("CORE1A_UPSTREAM_BINDING_MISMATCH", "C-H Core1 digest")
    if core2.get("study_model_ref") != study_model.get("study_model_id"):
        fail("CORE1A_UPSTREAM_BINDING_MISMATCH", "Core2 study-model ref")
    if core2.get("study_model_digest") != study_model.get("study_model_digest"):
        fail("CORE1A_UPSTREAM_BINDING_MISMATCH", "Core2 study-model digest")
    if core2.get("core1_plan_ref") != core1.get("plan_id"):
        fail("CORE1A_UPSTREAM_BINDING_MISMATCH", "Core2 Core1 ref")
    if core2.get("core1_plan_digest") != core1.get("plan_digest"):
        fail("CORE1A_UPSTREAM_BINDING_MISMATCH", "Core2 Core1 digest")


def make_atoms(bucket_id, lesson, record):
    source_refs = uniq(
        list(lesson.get("pck_asset_refs", []))
        + list(record.get("source_obligation_refs", []))
        + list(record.get("assessment_question_refs", []))
        + [lesson["lesson_id"]]
    )
    atoms = []

    def add(kind, text):
        text = (text or "").strip()
        if not text:
            return
        atoms.append(
            {
                "atom_id": f"CHEM-C1A-ATOM-{bucket_id.split('-')[-1]}-{len(atoms)+1:03d}",
                "capability_ref": lesson["capability_ref"],
                "atom_kind": kind,
                "text": text,
                "source_refs": source_refs,
            }
        )

    add("MEANING", lesson.get("ordinary_language_explanation"))
    add("RULE_MODEL_CONDITION", lesson.get("rule_model_condition"))
    for step in lesson.get("reconstruction_steps", []):
        add("RECONSTRUCTION_STEP", step)
    worked = lesson.get("worked_example")
    if worked:
        for step in worked.get("reasoning_steps", []):
            add("WORKED_REASONING", step)
    repair = lesson.get("misconception_repair")
    if repair:
        add("MISCONCEPTION_CONTRAST", repair.get("minimal_contrast"))
    add("TRANSFER_BRIDGE", lesson.get("transfer_bridge"))
    if not atoms:
        fail("CORE1A_LEARNING_ATOMS_MISSING", lesson["capability_ref"])
    return atoms


def rep_obligation(spec):
    return {
        "representation_ref": spec["representation_id"],
        "capability_ref": spec["capability_ref"],
        "primitive_id": spec["primitive_id"],
        "instructional_job": spec["instructional_job"],
        "learner_action_expected": spec["learner_action_expected"],
    }


def stage_row(stage, evidence, reason_required, reason_na):
    evidence = uniq(evidence)
    if evidence:
        return {"stage": stage, "status": "REQUIRED", "evidence_refs": evidence, "reason": reason_required}
    return {"stage": stage, "status": "NOT_APPLICABLE", "evidence_refs": [], "reason": reason_na}


def representation_sequence(reps, atoms, records, core2_refs):
    rep_ids = lambda rows: [row["representation_id"] for row in rows]
    macro = [r for r in reps if "MACROSCOPIC" in {r.get("representation_level_from"), r.get("representation_level_to")}]
    particle = [r for r in reps if "PARTICULATE" in {r.get("representation_level_from"), r.get("representation_level_to")}]
    structure = [
        r for r in reps
        if any(token in r.get("primitive_id", "") for token in ("STRUCTURE", "FORMULA", "CHARGE", "OXIDATION", "SPECIES_ROLE"))
    ]
    symbolic = [r for r in reps if "SYMBOLIC" in {r.get("representation_level_from"), r.get("representation_level_to")}]
    quantity = [
        r for r in reps
        if any(token in (r.get("primitive_id", "") + " " + r.get("instructional_job", "")).upper()
               for token in ("LEDGER", "COUNT", "QUANTITY", "MASS", "MOLE", "RATIO"))
    ]
    doing = [a["atom_id"] for a in atoms if a["atom_kind"] in FIRST_MOVE_KINDS]
    verification_required = any(r.get("verification_requirements") for r in records)
    verifying = [
        r for r in reps
        if any(token in (r.get("primitive_id", "") + " " + r.get("instructional_job", "")).upper()
               for token in ("CHECK", "VERIFY", "VERIFICATION", "CONSERVATION"))
    ]
    if verification_required and not verifying:
        verifying = reps[:1]
    return [
        stage_row("SEE_THE_PHENOMENON", rep_ids(macro), "Macroscopic evidence is part of the governed representation path.", "No macroscopic representation is required by C-H for this bucket."),
        stage_row("SEE_THE_PARTICLES", rep_ids(particle), "Particulate reasoning is explicitly represented before symbolic transfer.", "No particulate representation is required by C-H for this bucket."),
        stage_row("SEE_THE_CHEMICAL_STRUCTURE", rep_ids(structure), "Chemical structure/formula anatomy is explicitly represented.", "No separate structure/formula-anatomy stage is required beyond the other governed views."),
        stage_row("SEE_THE_SYMBOLS", rep_ids(symbolic), "Symbolic Chemistry is explicitly represented.", "No symbolic representation is required by C-H for this bucket."),
        stage_row("CONNECT_THE_QUANTITIES", rep_ids(quantity), "A governed representation connects chemical quantities or conservation counts.", "The governed problem family does not require a separate quantitative bridge."),
        stage_row("DO_THE_CHEMISTRY", doing, "Core1 teaching atoms supply executable Chemistry moves.", "No executable step is authorized for this bucket."),
        stage_row("VERIFY_THE_RESULT", rep_ids(verifying), "Verification is an explicit C-F/C-H obligation.", "No separate visual verification stage is required for this bucket."),
        stage_row("CONNECT_TO_CORE2", core2_refs, "The bucket explicitly releases governed Core2 transfer questions.", "This bucket has no primary Core2 question in the current source-transfer plan."),
    ]


def difficulty_for_pages(pages, policy):
    if not pages:
        return policy["intrinsic_difficulty_from_core2_badge"]["NO_PRIMARY_CORE2"]
    rank = {"D1": 1, "D2": 2, "D3": 3}
    mapped = []
    for page in pages:
        badge = page["guide_demand_badge"]["label"]
        mapped.append(policy["intrinsic_difficulty_from_core2_badge"][badge])
    return max(mapped, key=lambda x: rank[x])


def family_object(family_ref, family, page_refs):
    signals = uniq(list(family.get("allowed_variations", [])) + list(family.get("representation_requirements", [])))
    if not signals:
        signals = [family["chemical_signature"]]
    return {
        "problem_family_ref": family_ref,
        "chemical_signature": family["chemical_signature"],
        "recognition_signals": signals,
        "method_steps": list(family["reasoning_route_template"]),
        "core2_primary_question_refs": uniq(page_refs),
    }


def title_for_bucket(capabilities, core2_pages, family):
    titles = []
    caps = set(capabilities)
    for page in core2_pages:
        for ref in page.get("core1_lesson_refs", []):
            if ref.get("capability_ref") in caps and ref.get("learner_title"):
                titles.append(ref["learner_title"])
    titles = uniq(titles)
    if titles:
        return titles[0]
    signature = family["chemical_signature"].strip().rstrip(".")
    return signature[:110]


def choose_hint_evidence(capability_ref, atoms, reps):
    cap_atoms = [a for a in atoms if a["capability_ref"] == capability_ref]
    cap_reps = [r for r in reps if r["capability_ref"] == capability_ref]
    h1 = [a["atom_id"] for a in cap_atoms if a["atom_kind"] in {"MEANING", "RULE_MODEL_CONDITION"}][:1]
    h2 = [r["representation_id"] for r in cap_reps][:1]
    h3 = [a["atom_id"] for a in cap_atoms if a["atom_kind"] in FIRST_MOVE_KINDS][:1]
    if not h1 or not h2 or not h3:
        fail("CORE1A_HINT_NOT_PRETAUGHT", capability_ref)
    return h1, h2, h3


def build_bucket_plan(
    study_model,
    core1,
    representations,
    core2,
    problem_family_registry,
    synthesis_policy,
    plan_id="CHEM-C1A-BP-PILOT-v1",
):
    validate_upstream_bindings(study_model, core1, representations, core2)
    if synthesis_policy.get("policy_id") != "CHEM-CORE1A-BUCKET-SYNTHESIS-v1":
        fail("CORE1A_UPSTREAM_BINDING_MISMATCH", "unexpected synthesis policy")
    if problem_family_registry.get("registry_id") is None:
        fail("CORE1A_BUCKET_INVARIANT_UNGROUNDED", "problem-family registry missing id")

    by_family, aliases, defaults = family_tables(problem_family_registry)
    records = {r["capability_ref"]: r for r in study_model["capability_records"]}
    lessons = {l["capability_ref"]: l for l in core1["lessons"]}
    ordered_caps = [l["capability_ref"] for l in core1["lessons"]]
    if set(ordered_caps) != set(records) or len(ordered_caps) != len(records):
        fail("CORE1A_CAPABILITY_COVERAGE_FAILED", "Core1 and C-F capability sets differ")

    reps_by_cap = defaultdict(list)
    for rep in representations["representations"]:
        reps_by_cap[rep["capability_ref"]].append(rep)

    pages_by_cap = defaultdict(list)
    for page in core2["pages"]:
        pages_by_cap[page["primary_capability_ref"]].append(page)
        if page["primary_capability_ref"] not in records:
            fail("CORE1A_CORE2_MAPPING_INCOMPLETE", page["question_ref"] + ": unknown primary capability")

    group_order = []
    group_caps = defaultdict(list)
    cap_family = {}
    for cap in ordered_caps:
        family_ref = primary_family_for_capability(cap, records[cap], by_family, aliases, defaults)
        cap_family[cap] = family_ref
        if family_ref not in group_order:
            group_order.append(family_ref)
        group_caps[family_ref].append(cap)

    buckets = []
    cap_to_bucket = {}
    for index, family_ref in enumerate(group_order, 1):
        bucket_id = f"CHEM-C1A-SBA-{index:02d}"
        caps = group_caps[family_ref]
        family = by_family[family_ref]
        bucket_pages = [p for cap in caps for p in pages_by_cap.get(cap, [])]
        primary_caps = uniq([p["primary_capability_ref"] for p in bucket_pages])
        supporting_caps = [cap for cap in caps if cap not in primary_caps]
        bucket_records = [records[cap] for cap in caps]
        bucket_reps = [r for cap in caps for r in reps_by_cap.get(cap, [])]
        if not bucket_reps:
            fail("CORE1A_VISUAL_OBLIGATION_UNCLOSED", bucket_id)

        atoms = []
        for cap in caps:
            lesson = lessons.get(cap)
            if lesson is None:
                fail("CORE1A_CAPABILITY_COVERAGE_FAILED", cap + ": no Core1 lesson")
            if lesson["treatment"] != records[cap]["treatment"]:
                fail("CORE1A_TREATMENT_DRIFT", cap)
            atoms.extend(make_atoms(bucket_id, lesson, records[cap]))

        page_refs = uniq([p["question_ref"] for p in bucket_pages])
        hint_bindings = []
        for page in bucket_pages:
            h1, h2, h3 = choose_hint_evidence(page["primary_capability_ref"], atoms, bucket_reps)
            hint_bindings.append(
                {
                    "question_ref": page["question_ref"],
                    "h1_evidence_refs": h1,
                    "h2_evidence_refs": h2,
                    "h3_evidence_refs": h3,
                }
            )

        family_refs = [family_ref]
        for cap in caps:
            for raw in records[cap].get("problem_family_refs", []):
                resolved = canonical_family(raw, by_family, aliases)
                if resolved:
                    family_refs.append(resolved)
        for page in bucket_pages:
            resolved = canonical_family(page.get("problem_family_ref"), by_family, aliases)
            if resolved:
                family_refs.append(resolved)
        family_refs = uniq(family_refs)
        problem_families = []
        for ref in family_refs:
            related = [p["question_ref"] for p in bucket_pages if canonical_family(p.get("problem_family_ref"), by_family, aliases) == ref]
            problem_families.append(family_object(ref, by_family[ref], related))

        bucket = {
            "bucket_id": bucket_id,
            "learner_title": title_for_bucket(caps, bucket_pages, family),
            "bucket_invariant": family["chemical_signature"],
            "intrinsic_difficulty": difficulty_for_pages(bucket_pages, synthesis_policy),
            "primary_problem_family_ref": family_ref,
            "primary_capability_refs": primary_caps,
            "supporting_capability_refs": supporting_caps,
            "learner_treatment_by_capability": [
                {
                    "capability_ref": cap,
                    "learner_state": records[cap]["learner_state"],
                    "treatment": records[cap]["treatment"],
                    "priority": records[cap]["priority"],
                }
                for cap in caps
            ],
            "source_obligation_refs": uniq([x for cap in caps for x in records[cap]["source_obligation_refs"]]),
            "assessment_question_refs": uniq([x for cap in caps for x in records[cap]["assessment_question_refs"]]),
            "core2_primary_question_refs": page_refs,
            "learning_atoms": atoms,
            "representation_obligations": [rep_obligation(r) for r in bucket_reps],
            "representation_sequence": representation_sequence(bucket_reps, atoms, bucket_records, page_refs),
            "problem_families": problem_families,
            "core2_hint_bindings": hint_bindings,
            "readiness_gate": {
                "required_dimensions": ["RECOGNISE", "REPRESENT", "FIRST_MOVE", "FINISH_AND_VERIFY"],
                "release_rule": "4_OF_4_WITHOUT_H2_OR_H3",
                "remediation_target_kind": "LEARNING_ATOM_OR_PROBLEM_FAMILY_ROUTINE",
            },
        }
        buckets.append(bucket)
        for cap in caps:
            if cap in cap_to_bucket:
                fail("CORE1A_CAPABILITY_COVERAGE_FAILED", cap + ": duplicate bucket")
            cap_to_bucket[cap] = bucket_id

    required_caps = ordered_caps
    placed_caps = [cap for bucket in buckets for cap in bucket["primary_capability_refs"] + bucket["supporting_capability_refs"]]
    counts = Counter(placed_caps)
    duplicate_caps = sorted([cap for cap, count in counts.items() if count > 1])
    missing_caps = [cap for cap in required_caps if cap not in counts]

    required_questions = [p["question_ref"] for p in core2["pages"]]
    mapped_questions = [q for bucket in buckets for q in bucket["core2_primary_question_refs"]]
    question_counts = Counter(mapped_questions)
    missing_questions = [q for q in required_questions if q not in question_counts]
    duplicate_questions = [q for q, count in question_counts.items() if count > 1]
    if missing_caps or duplicate_caps:
        fail("CORE1A_CAPABILITY_COVERAGE_FAILED", f"missing={missing_caps}; duplicate={duplicate_caps}")
    if missing_questions or duplicate_questions:
        fail("CORE1A_CORE2_MAPPING_INCOMPLETE", f"missing={missing_questions}; duplicate={duplicate_questions}")

    required_rep_ids = {r["representation_id"] for r in representations["representations"]}
    placed_rep_ids = {
        r["representation_ref"]
        for bucket in buckets
        for r in bucket["representation_obligations"]
    }
    if required_rep_ids != placed_rep_ids:
        fail("CORE1A_VISUAL_OBLIGATION_UNCLOSED", "C-H representation custody mismatch")

    bound_reveals = 3 * sum(len(bucket["core2_hint_bindings"]) for bucket in buckets)
    required_reveals = 3 * len(core2["pages"])
    if bound_reveals != required_reveals:
        fail("CORE1A_HINT_NOT_PRETAUGHT", f"required={required_reveals}; bound={bound_reveals}")

    out = {
        "plan_id": plan_id,
        "schema_version": "1.0.0",
        "subject": "CHEMISTRY",
        "study_model_ref": study_model["study_model_id"],
        "study_model_digest": study_model["study_model_digest"],
        "core1_plan_ref": core1["plan_id"],
        "core1_plan_digest": core1["plan_digest"],
        "representation_bundle_ref": representations["bundle_id"],
        "representation_bundle_digest": representations["bundle_digest"],
        "core2_plan_ref": core2["plan_id"],
        "core2_plan_digest": core2["plan_digest"],
        "problem_family_registry_ref": problem_family_registry["registry_id"],
        "synthesis_policy_ref": synthesis_policy["policy_id"],
        "buckets": buckets,
        "coverage": {
            "required_capability_refs": required_caps,
            "placed_capability_refs": placed_caps,
            "missing_capability_refs": [],
            "duplicate_primary_capability_refs": [],
            "required_core2_question_refs": required_questions,
            "mapped_core2_question_refs": mapped_questions,
            "missing_core2_question_refs": [],
            "hint_reveals_required": required_reveals,
            "hint_reveals_bound": bound_reveals,
            "status": "PASS",
        },
        "plan_digest": "",
    }
    out["plan_digest"] = digest(out, "plan_digest")
    validate_bucket_plan(out, study_model, core1, representations, core2, problem_family_registry, synthesis_policy)
    return out


def validate_bucket_plan(plan, study_model, core1, representations, core2, problem_family_registry, synthesis_policy):
    validate_upstream_bindings(study_model, core1, representations, core2)
    if plan.get("plan_digest") != digest(plan, "plan_digest"):
        fail("CORE1A_UPSTREAM_BINDING_MISMATCH", "bucket-plan digest")
    expected_bindings = {
        "study_model_ref": study_model["study_model_id"],
        "study_model_digest": study_model["study_model_digest"],
        "core1_plan_ref": core1["plan_id"],
        "core1_plan_digest": core1["plan_digest"],
        "representation_bundle_ref": representations["bundle_id"],
        "representation_bundle_digest": representations["bundle_digest"],
        "core2_plan_ref": core2["plan_id"],
        "core2_plan_digest": core2["plan_digest"],
        "problem_family_registry_ref": problem_family_registry["registry_id"],
        "synthesis_policy_ref": synthesis_policy["policy_id"],
    }
    for key, value in expected_bindings.items():
        if plan.get(key) != value:
            fail("CORE1A_UPSTREAM_BINDING_MISMATCH", key)

    records = {r["capability_ref"]: r for r in study_model["capability_records"]}
    by_family, aliases, defaults = family_tables(problem_family_registry)
    placed = []
    mapped_questions = []
    placed_reps = []
    bound_reveals = 0
    for bucket in plan["buckets"]:
        family_ref = bucket["primary_problem_family_ref"]
        if family_ref not in by_family or bucket["bucket_invariant"] != by_family[family_ref]["chemical_signature"]:
            fail("CORE1A_BUCKET_INVARIANT_UNGROUNDED", bucket["bucket_id"])
        caps = bucket["primary_capability_refs"] + bucket["supporting_capability_refs"]
        placed.extend(caps)
        for row in bucket["learner_treatment_by_capability"]:
            if row["capability_ref"] not in records:
                fail("CORE1A_CAPABILITY_COVERAGE_FAILED", row["capability_ref"])
            record = records[row["capability_ref"]]
            if (row["learner_state"], row["treatment"], row["priority"]) != (
                record["learner_state"], record["treatment"], record["priority"]
            ):
                fail("CORE1A_TREATMENT_DRIFT", row["capability_ref"])
            expected_family = primary_family_for_capability(row["capability_ref"], record, by_family, aliases, defaults)
            if expected_family != family_ref:
                fail("CORE1A_BUCKET_INVARIANT_UNGROUNDED", row["capability_ref"])
        if not bucket["learning_atoms"]:
            fail("CORE1A_LEARNING_ATOMS_MISSING", bucket["bucket_id"])
        atom_refs = {a["atom_id"] for a in bucket["learning_atoms"]}
        rep_refs = {r["representation_ref"] for r in bucket["representation_obligations"]}
        if not rep_refs:
            fail("CORE1A_VISUAL_OBLIGATION_UNCLOSED", bucket["bucket_id"])
        placed_reps.extend(rep_refs)
        if [x["stage"] for x in bucket["representation_sequence"]] != STAGES:
            fail("CORE1A_VISUAL_OBLIGATION_UNCLOSED", bucket["bucket_id"] + ": stage order")
        for stage in bucket["representation_sequence"]:
            if stage["status"] == "REQUIRED" and not stage["evidence_refs"]:
                fail("CORE1A_VISUAL_OBLIGATION_UNCLOSED", bucket["bucket_id"] + ": " + stage["stage"])
            if stage["status"] == "NOT_APPLICABLE" and not stage["reason"].strip():
                fail("CORE1A_VISUAL_OBLIGATION_UNCLOSED", bucket["bucket_id"] + ": unexplained N/A")
        mapped_questions.extend(bucket["core2_primary_question_refs"])
        for binding in bucket["core2_hint_bindings"]:
            for key in ("h1_evidence_refs", "h2_evidence_refs", "h3_evidence_refs"):
                refs = binding[key]
                if not refs or any(ref not in atom_refs | rep_refs for ref in refs):
                    fail("CORE1A_HINT_NOT_PRETAUGHT", binding["question_ref"] + ": " + key)
                bound_reveals += 1

    required_caps = [l["capability_ref"] for l in core1["lessons"]]
    if Counter(placed) != Counter(required_caps):
        fail("CORE1A_CAPABILITY_COVERAGE_FAILED")
    required_questions = [p["question_ref"] for p in core2["pages"]]
    if Counter(mapped_questions) != Counter(required_questions):
        fail("CORE1A_CORE2_MAPPING_INCOMPLETE")
    required_rep_ids = [r["representation_id"] for r in representations["representations"]]
    if Counter(placed_reps) != Counter(required_rep_ids):
        fail("CORE1A_VISUAL_OBLIGATION_UNCLOSED", "representation custody")
    if bound_reveals != 3 * len(core2["pages"]):
        fail("CORE1A_HINT_NOT_PRETAUGHT", "hint denominator")
    if plan["coverage"]["status"] != "PASS":
        fail("CORE1A_CAPABILITY_COVERAGE_FAILED", "coverage status")
    if plan["coverage"]["hint_reveals_required"] != plan["coverage"]["hint_reveals_bound"]:
        fail("CORE1A_HINT_NOT_PRETAUGHT", "coverage counters")
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--study-model", required=True)
    parser.add_argument("--core1-plan", required=True)
    parser.add_argument("--representation-bundle", required=True)
    parser.add_argument("--core2-plan", required=True)
    parser.add_argument("--problem-family-registry", required=True)
    parser.add_argument("--synthesis-policy", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--plan-id", default="CHEM-C1A-BP-PILOT-v1")
    args = parser.parse_args()
    out = build_bucket_plan(
        load(args.study_model),
        load(args.core1_plan),
        load(args.representation_bundle),
        load(args.core2_plan),
        load(args.problem_family_registry),
        load(args.synthesis_policy),
        args.plan_id,
    )
    Path(args.out).write_text(json.dumps(out, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
