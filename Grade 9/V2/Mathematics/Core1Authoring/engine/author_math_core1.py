#!/usr/bin/env python3
import argparse
import copy
import hashlib
import json
from pathlib import Path

FULL_TREATMENTS = {"ACTIVE_STUDY", "REPAIR_BEFORE", "REPAIR_IN_UNIT"}

# Release classes. `PROVISIONAL_PENDING_EXPERT_REVIEW` means the plan is
# authoring-legal (every full-teaching capability is bound to a PCK asset that
# cleared the M-G promotion pipeline) but not release-legal, because at least
# one bound asset carries only AI-assisted reference review and its
# SUBJECT/PEDAGOGY expert review is still PENDING.
RELEASE_CLASSES = ("PRODUCTION", "PROVISIONAL_PENDING_EXPERT_REVIEW", "TEST_ONLY")


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def canon(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(value, omit=None):
    value = copy.deepcopy(value)
    if omit and isinstance(value, dict):
        value.pop(omit, None)
    return hashlib.sha256(canon(value).encode("utf-8")).hexdigest()


def verify_digest(value, field, code):
    expected = value.get(field)
    if expected != digest(value, field):
        raise ValueError(code)


def load_candidate_bundle(path):
    path = Path(path)
    registry = load(path)
    assets = []
    for doc in registry["asset_documents"]:
        asset = load(path.parent / doc["path"])
        if asset["asset_id"] != doc["asset_id"] or asset["asset_digest"] != doc["asset_digest"]:
            raise ValueError(f"PCK_INDEX_BINDING_MISMATCH:{doc['asset_id']}")
        assets.append(asset)
    return registry, assets


def candidate_map(candidate_registry, candidate_assets):
    verify_digest(candidate_registry, "registry_digest", "PCK_CANDIDATE_REGISTRY_DIGEST_MISMATCH")
    out = {}
    for asset in candidate_assets:
        verify_digest(asset, "asset_digest", f"PCK_DIGEST_MISMATCH:{asset['asset_id']}")
        if asset["asset_id"] in out:
            raise ValueError(f"DUPLICATE_PCK_ASSET:{asset['asset_id']}")
        out[asset["asset_id"]] = asset
    return out


def validated_promotions(candidate_registry, candidate_assets, promotion_registry, test_mode=False):
    candidates = candidate_map(candidate_registry, candidate_assets)
    verify_digest(promotion_registry, "registry_digest", "PCK_PROMOTION_REGISTRY_DIGEST_MISMATCH")
    registry_class = promotion_registry["registry_class"]
    if registry_class == "TEST_ONLY" and not test_mode:
        raise ValueError("TEST_ONLY_PCK_REGISTRY_FORBIDDEN")

    by_capability = {}
    provisional_asset_ids = set()
    producer_legal_asset_ids = set()
    for rec in promotion_registry["promotions"]:
        verify_digest(rec, "promotion_digest", f"PCK_PROMOTION_DIGEST_MISMATCH:{rec['asset_id']}")
        if rec["asset_id"] not in candidates:
            raise ValueError(f"PCK_PROMOTION_UNKNOWN_ASSET:{rec['asset_id']}")
        asset = candidates[rec["asset_id"]]
        if rec["asset_digest"] != asset["asset_digest"]:
            raise ValueError(f"PCK_DIGEST_MISMATCH:{rec['asset_id']}")

        if registry_class == "PRODUCTION":
            status = rec["promotion_status"]
            shared = (
                {"SUBJECT", "PEDAGOGY"}.issubset(set(rec["review_dimensions"]))
                and len(rec["review_evidence_refs"]) >= 2
            )
            if status == "PROMOTED":
                good = (
                    shared
                    and rec["review_source"] == "HUMAN_REVIEW_INTAKE_RESULT"
                    and rec["review_registry_class"] == "REAL"
                    and rec["producer_legal"] is True
                    and rec.get("expert_review_state", {"SUBJECT_EXPERT_PASS": "PASS", "PEDAGOGY_EXPERT_PASS": "PASS"})
                    == {"SUBJECT_EXPERT_PASS": "PASS", "PEDAGOGY_EXPERT_PASS": "PASS"}
                )
                if not good:
                    raise ValueError(f"PCK_REVIEW_AUTHORITY_INVALID:{rec['asset_id']}")
                producer_legal_asset_ids.add(rec["asset_id"])
            elif status == "PROVISIONAL_PROMOTED":
                if rec.get("producer_legal") or rec.get("release_legal"):
                    raise ValueError(f"PROVISIONAL_PROMOTION_CLAIMED_PRODUCER_LEGAL:{rec['asset_id']}")
                good = (
                    shared
                    and rec.get("promotion_class") == "AI_ASSISTED_PROVISIONAL"
                    and rec["review_source"] == "AI_ASSISTED_REFERENCE_REVIEW"
                    and rec["review_registry_class"] == "AI_ASSISTED"
                    and rec.get("authoring_legal") is True
                    and rec.get("lifecycle_state") == "PROMOTED_INSTRUCTIONAL_KNOWLEDGE"
                    and len(rec.get("review_pipeline") or []) >= 4
                )
                if not good:
                    raise ValueError(f"PCK_PROVISIONAL_PROMOTION_INVALID:{rec['asset_id']}")
                provisional_asset_ids.add(rec["asset_id"])
            else:
                raise ValueError(f"PCK_REVIEW_AUTHORITY_INVALID:{rec['asset_id']}")
        else:
            good = (
                test_mode
                and rec["promotion_status"] == "TEST_PROMOTED"
                and rec["review_registry_class"] == "TEST_ONLY"
                and rec["producer_legal"] is False
            )
            if not good:
                raise ValueError(f"PCK_TEST_PROMOTION_INVALID:{rec['asset_id']}")

        for capability in asset["capability_refs"]:
            by_capability.setdefault(capability, []).append(asset)
    for assets in by_capability.values():
        assets.sort(key=lambda x: x["asset_id"])
    authority = {"provisional": provisional_asset_ids, "producer_legal": producer_legal_asset_ids}
    return candidates, by_capability, authority


def required_pck_for(plan):
    return plan["treatment"] in FULL_TREATMENTS


def choose_pck(plan, candidates, promoted_by_capability):
    cap = plan["capability_ref"]
    available_candidates = [a for a in candidates.values() if cap in a["capability_refs"]]
    promoted = promoted_by_capability.get(cap, [])
    if required_pck_for(plan):
        if not available_candidates:
            raise ValueError(f"PCK_COVERAGE_GAP:{cap}")
        if not promoted:
            raise ValueError(f"PCK_PROMOTION_REQUIRED:{cap}")
        return promoted
    return promoted


def problem_plan(capability_ref, family_ref, role, verification_requirements):
    seed = {"capability_ref": capability_ref, "problem_family_ref": family_ref, "instance_role": role}
    return {
        "plan_id": "MATH-PAP-" + digest(seed)[:16],
        "capability_ref": capability_ref,
        "problem_family_ref": family_ref,
        "instance_role": role,
        "must_be_new_instance": True,
        "source_question_reuse": False,
        "source_question_refs": [],
        "variation_requirements": [
            "author a new instructional instance rather than copying an original assessment question",
            "preserve the problem-family invariant while varying surface data or context",
            "preserve the capability and verification obligations named by the StudyModel",
        ],
        "verification_obligations": sorted(set(verification_requirements)),
    }


def lesson_title(capability_ref):
    return capability_ref.removeprefix("MATH-").replace("-", " ").title()


def build_lesson(plan, study_model, assets, profile):
    treatment = plan["treatment"]
    sequence = list(profile["treatment_sequences"][treatment])
    problem_plans = []
    families = sorted(set(plan["problem_family_refs"]))

    if treatment in FULL_TREATMENTS:
        if not families:
            raise ValueError(f"PROBLEM_FAMILY_REQUIRED:{plan['capability_ref']}")
        family = families[0]
        for role in profile["problem_authoring"]["required_instance_roles_for_full_teaching"]:
            problem_plans.append(problem_plan(plan["capability_ref"], family, role, plan["verification_requirements"]))
    elif treatment == "VERIFY_ONLY" and families:
        problem_plans.append(problem_plan(plan["capability_ref"], families[0], "VERIFY", plan["verification_requirements"]))

    seed = {"study_model_id": study_model["study_model_id"], "capability_ref": plan["capability_ref"], "treatment": treatment}
    return {
        "lesson_id": "MATH-C1L-" + digest(seed)[:16],
        "learner_title": lesson_title(plan["capability_ref"]),
        "capability_ref": plan["capability_ref"],
        "treatment": treatment,
        "scope_role": plan["scope_role"],
        "assessment_question_refs": sorted(set(plan["assessment_question_refs"])),
        "pck_asset_refs": [a["asset_id"] for a in assets],
        "required_pck_jobs": list(plan["required_pck_jobs"]),
        "instructional_sequence": sequence,
        "representation_requirements": sorted(set(plan["representation_requirements"])),
        "problem_authoring_plans": problem_plans,
        "verification_requirements": sorted(set(plan["verification_requirements"])),
        "future_evidence_obligations": plan["future_evidence_obligations"],
        "scope_trace": {"study_scope_ref": study_model["study_scope_ref"], "study_model_capability_ref": plan["capability_ref"]},
    }


def assert_pck_authority_invariants(plan):
    authority = plan.get("pck_authority")
    if authority is None:
        raise ValueError("PCK_AUTHORITY_BLOCK_MISSING")
    provisional = authority["provisional_asset_refs"]
    if plan["release_class"] == "PRODUCTION" and provisional:
        raise ValueError("PRODUCTION_RELEASE_CLASS_WITH_PROVISIONAL_PCK:" + ",".join(provisional))
    if provisional and authority["release_legal"]:
        raise ValueError("PROVISIONAL_PROMOTION_CLAIMED_PRODUCER_LEGAL:" + ",".join(provisional))
    if provisional and authority["expert_review_state"] != "PENDING":
        raise ValueError("FABRICATED_EXPERT_REVIEW_AUTHORITY:" + ",".join(provisional))
    if plan["release_class"] == "TEST_ONLY" and authority["release_legal"]:
        raise ValueError("TEST_ONLY_PLAN_CLAIMED_RELEASE_LEGAL")
    overlap = sorted(set(provisional) & set(authority["producer_legal_asset_refs"]))
    if overlap:
        raise ValueError("PCK_AUTHORITY_STATE_CONFLICT:" + ",".join(overlap))


def assert_plan_invariants(plan, study_model, profile):
    assert_pck_authority_invariants(plan)
    expected = [x["capability_ref"] for x in study_model["capability_plans"]]
    actual = [x["capability_ref"] for x in plan["lessons"]]
    if len(actual) != len(set(actual)):
        raise ValueError("CORE1_DUPLICATE_CAPABILITY_LESSON")
    if set(actual) != set(expected):
        missing = sorted(set(expected) - set(actual))
        extra = sorted(set(actual) - set(expected))
        raise ValueError("CORE1_SCOPE_GAP:missing=" + ",".join(missing) + ";extra=" + ",".join(extra))

    for lesson in plan["lessons"]:
        expected_seq = profile["treatment_sequences"][lesson["treatment"]]
        if lesson["instructional_sequence"] != expected_seq:
            raise ValueError(f"TREATMENT_SEQUENCE_DRIFT:{lesson['capability_ref']}")
        if lesson["treatment"] == "VERIFY_ONLY":
            forbidden = {"ANCHOR", "RECONSTRUCT", "WORKED", "GUIDED", "FADED", "INDEPENDENT", "TRANSFER"}
            if forbidden.intersection(lesson["instructional_sequence"]):
                raise ValueError(f"READY_CONTENT_PADDED_INTO_FULL_RETEACH:{lesson['capability_ref']}")
        if lesson["treatment"] == "PROBE_FIRST" and lesson["instructional_sequence"] != ["PROBE"]:
            raise ValueError(f"PROBE_FIRST_EXPLANATION_LEAK:{lesson['capability_ref']}")
        if lesson["treatment"] in FULL_TREATMENTS:
            required = {"ANCHOR", "REPRESENT", "EXPLAIN", "RECONSTRUCT", "CONTRAST", "WORKED", "GUIDED", "FADED", "INDEPENDENT", "VERIFY", "TRANSFER"}
            if not required.issubset(set(lesson["instructional_sequence"])):
                raise ValueError(f"FULL_LEARNING_TREATMENT_WITHOUT_RECONSTRUCTION:{lesson['capability_ref']}")
            if not lesson["pck_asset_refs"]:
                raise ValueError(f"PCK_PROMOTION_REQUIRED:{lesson['capability_ref']}")
        for pap in lesson["problem_authoring_plans"]:
            if not pap["problem_family_ref"]:
                raise ValueError(f"PROBLEM_FAMILY_REQUIRED:{lesson['capability_ref']}")
            if pap["source_question_reuse"] or pap["source_question_refs"]:
                raise ValueError(f"SOURCE_QUESTION_REUSE_FORBIDDEN:{lesson['capability_ref']}")
            if not pap["must_be_new_instance"]:
                raise ValueError(f"NEW_PROBLEM_INSTANCE_REQUIRED:{lesson['capability_ref']}")


def author(study_wrapper, candidate_registry, candidate_assets, promotion_registry, profile, scope_policy, test_mode=False):
    study_model = study_wrapper.get("learner_study_model", study_wrapper)
    if study_model.get("subject") != "MATHEMATICS":
        raise ValueError("NON_MATH_STUDY_MODEL")

    candidates, promoted_by_capability, pck_authority = validated_promotions(
        candidate_registry, candidate_assets, promotion_registry, test_mode
    )
    lessons = []
    bound_asset_ids = set()
    for capability_plan in study_model["capability_plans"]:
        assets = choose_pck(capability_plan, candidates, promoted_by_capability)
        bound_asset_ids.update(a["asset_id"] for a in assets)
        lessons.append(build_lesson(capability_plan, study_model, assets, profile))

    required = sorted(x["capability_ref"] for x in study_model["capability_plans"])
    covered = sorted(x["capability_ref"] for x in lessons)
    omitted = sorted(set(required) - set(covered))
    if omitted:
        raise ValueError("CORE1_SCOPE_GAP:" + ",".join(omitted))

    bound_provisional = sorted(bound_asset_ids & pck_authority["provisional"])
    bound_producer_legal = sorted(bound_asset_ids & pck_authority["producer_legal"])
    if test_mode:
        release_class = "TEST_ONLY"
    elif bound_provisional:
        release_class = "PROVISIONAL_PENDING_EXPERT_REVIEW"
    else:
        release_class = "PRODUCTION"

    input_payload = {
        "study_model_digest": study_model["study_model_digest"],
        "candidate_registry_digest": candidate_registry["registry_digest"],
        "promotion_registry_digest": promotion_registry["registry_digest"],
        "profile_digest": digest(profile),
        "scope_policy_digest": digest(scope_policy),
        "test_mode": bool(test_mode),
        "release_class": release_class,
    }
    plan = {
        "core1_study_plan_id": "MATH-C1SP-" + digest(input_payload)[:16],
        "schema_version": "1.0.0",
        "subject": "MATHEMATICS",
        "release_class": release_class,
        "pck_authority": {
            "promotion_registry_ref": promotion_registry["registry_id"],
            "promotion_registry_digest": promotion_registry["registry_digest"],
            "bound_asset_refs": sorted(bound_asset_ids),
            "provisional_asset_refs": bound_provisional,
            "producer_legal_asset_refs": bound_producer_legal,
            "expert_review_state": "PENDING" if bound_provisional else ("PASS" if bound_asset_ids else "NOT_REQUIRED"),
            "release_legal": bool(bound_asset_ids) and not bound_provisional and not test_mode,
        },
        "study_model_ref": study_model["study_model_id"],
        "study_model_digest": study_model["study_model_digest"],
        "pck_candidate_registry_ref": candidate_registry["registry_id"],
        "pck_promotion_registry_ref": promotion_registry["registry_id"],
        "lessons": lessons,
        "scope_completeness": {"required_capability_refs": required, "covered_capability_refs": covered, "omitted_capability_refs": [], "status": "PASS"},
        "input_digest": digest(input_payload),
    }
    plan["plan_digest"] = digest(plan, "plan_digest")
    assert_plan_invariants(plan, study_model, profile)
    return plan


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--study-model", required=True)
    ap.add_argument("--pck-candidates", required=True)
    ap.add_argument("--pck-promotions", required=True)
    ap.add_argument("--profile", required=True)
    ap.add_argument("--scope-policy", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--test-mode", action="store_true")
    args = ap.parse_args()
    candidate_registry, candidate_assets = load_candidate_bundle(args.pck_candidates)
    result = author(load(args.study_model), candidate_registry, candidate_assets, load(args.pck_promotions), load(args.profile), load(args.scope_policy), test_mode=args.test_mode)
    Path(args.out).write_text(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
