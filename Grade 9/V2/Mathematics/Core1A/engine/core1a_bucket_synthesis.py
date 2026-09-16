#!/usr/bin/env python3
"""Core1A bucket synthesis.

This module fixes the semantic boundary between capability-level Core1 planning and
textbook realization. It does not invent learner knowledge. Learner readiness,
confidence, observations, treatment and priority are copied from the exact M-F
MathLearnerStudyModel that Core1 was authored from.

Bucket grouping is deliberately conservative:
- directly assessed capabilities are grouped only when they share a governed
  problem family;
- prerequisite-only capabilities are attached to a single dependent bucket when
  the StudyModel makes that dependency unambiguous;
- shared prerequisites feeding multiple buckets remain their own bridge bucket;
- every capability appears in exactly one bucket.

The bucket invariant must be grounded in either a canonical problem-family target
job or a bound PCK anchor. No free-form model inference is accepted here.
"""
from __future__ import annotations

import copy
import hashlib
import json
from collections import defaultdict
from typing import Any


DIRECT_ROLES = {"DIRECT_ASSESSED", "DIRECT_AND_PREREQUISITE"}
SUPPORT_ROLE = "PREREQUISITE_SUPPORT"


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(value: Any, omit: str | None = None) -> str:
    item = copy.deepcopy(value)
    if omit and isinstance(item, dict):
        item.pop(omit, None)
    return hashlib.sha256(canonical(item).encode("utf-8")).hexdigest()


def fail(code: str, detail: str = "") -> None:
    raise ValueError(f"{code}:{detail}" if detail else code)


def _family_refs(lesson: dict) -> list[str]:
    return sorted({
        p.get("problem_family_ref")
        for p in lesson.get("problem_authoring_plans", [])
        if p.get("problem_family_ref")
    })


def _index_core1(core1: dict) -> dict[str, dict]:
    out = {}
    for lesson in core1.get("lessons", []):
        cap = lesson.get("capability_ref")
        if not cap or cap in out:
            fail("CORE1A_CORE1_CAPABILITY_DUPLICATE_OR_MISSING", str(cap))
        out[cap] = lesson
    return out


def _index_study_model(study_model: dict) -> dict[str, dict]:
    out = {}
    for plan in study_model.get("capability_plans", []):
        cap = plan.get("capability_ref")
        if not cap or cap in out:
            fail("CORE1A_STUDY_MODEL_CAPABILITY_DUPLICATE_OR_MISSING", str(cap))
        out[cap] = plan
    return out


def _validate_binding(core1: dict, study_model: dict) -> tuple[dict[str, dict], dict[str, dict]]:
    if core1.get("study_model_ref") != study_model.get("study_model_id"):
        fail("CORE1A_STUDY_MODEL_REF_MISMATCH")
    if core1.get("study_model_digest") != study_model.get("study_model_digest"):
        fail("CORE1A_STUDY_MODEL_DIGEST_BINDING_MISMATCH")
    if study_model.get("study_model_digest") != digest(study_model, "study_model_digest"):
        fail("CORE1A_STUDY_MODEL_DIGEST_INVALID")

    lessons = _index_core1(core1)
    plans = _index_study_model(study_model)
    expected = set(core1.get("scope_completeness", {}).get("required_capability_refs", []))
    if set(lessons) != expected:
        fail("CORE1A_CORE1_SCOPE_COVERAGE_DRIFT")
    if set(plans) != expected:
        fail("CORE1A_STUDY_MODEL_SCOPE_COVERAGE_DRIFT")

    for cap in sorted(expected):
        lesson = lessons[cap]
        plan = plans[cap]
        # M-G is downstream of M-F: treatment and scope role must survive unchanged.
        if lesson.get("treatment") != plan.get("treatment"):
            fail("CORE1A_TREATMENT_DRIFT", cap)
        if lesson.get("scope_role") != plan.get("scope_role"):
            fail("CORE1A_SCOPE_ROLE_DRIFT", cap)
        if set(lesson.get("assessment_question_refs", [])) != set(plan.get("assessment_question_refs", [])):
            fail("CORE1A_ASSESSMENT_BINDING_DRIFT", cap)
    return lessons, plans


def _direct_components(lessons: dict[str, dict], plans: dict[str, dict]) -> list[set[str]]:
    direct = sorted(cap for cap, p in plans.items() if p.get("scope_role") in DIRECT_ROLES)
    parent = {cap: cap for cap in direct}

    def find(x: str) -> str:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a: str, b: str) -> None:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[max(ra, rb)] = min(ra, rb)

    families = {cap: set(_family_refs(lessons[cap])) for cap in direct}
    for i, a in enumerate(direct):
        for b in direct[i + 1:]:
            if families[a] & families[b]:
                union(a, b)

    groups: dict[str, set[str]] = defaultdict(set)
    for cap in direct:
        groups[find(cap)].add(cap)
    return [groups[k] for k in sorted(groups)]


def _assign_supports(components: list[set[str]], plans: dict[str, dict]) -> list[set[str]]:
    comps = [set(c) for c in components]
    direct_to_bucket = {cap: i for i, comp in enumerate(comps) for cap in comp}
    supports = sorted(cap for cap, p in plans.items() if p.get("scope_role") == SUPPORT_ROLE)

    for support in supports:
        target_buckets = set()
        for dependent, plan in plans.items():
            if support in set(plan.get("prerequisite_refs", [])) and dependent in direct_to_bucket:
                target_buckets.add(direct_to_bucket[dependent])
        if len(target_buckets) == 1:
            idx = next(iter(target_buckets))
            comps[idx].add(support)
        else:
            # Shared or unattached prerequisite: teach once as its own bridge bucket.
            comps.append({support})

    assigned = {cap for comp in comps for cap in comp}
    for cap in sorted(set(plans) - assigned):
        comps.append({cap})
    return comps


def _choose_pck_asset(lesson: dict, assets: dict[str, dict]) -> tuple[str, dict] | None:
    cap = lesson.get("capability_ref")
    # Prefer an asset explicitly claiming this capability where available.
    for ref in lesson.get("pck_asset_refs", []):
        asset = assets.get(ref)
        if asset and cap in set(asset.get("capability_refs", [])):
            return ref, asset
    for ref in lesson.get("pck_asset_refs", []):
        if ref in assets:
            return ref, assets[ref]
    return None


def _atoms_for_capability(cap: str, lesson: dict, assets: dict[str, dict]) -> list[dict]:
    chosen = _choose_pck_asset(lesson, assets)
    if not chosen:
        fail("CORE1A_BUCKET_PCK_BINDING_MISSING", cap)
    ref, asset = chosen
    rows: list[tuple[str, str]] = []
    anchor = str(asset.get("anchor") or asset.get("ordinary_language_bridge") or "").strip()
    if anchor:
        rows.append(("ANCHOR", anchor))
    for step in asset.get("reconstruction_route", []):
        text = str(step).strip()
        if text:
            rows.append(("RECONSTRUCTION_STEP", text))
    if not rows:
        fail("CORE1A_BUCKET_LEARNING_ATOMS_MISSING", cap)

    out = []
    for i, (role, text) in enumerate(rows):
        atom_id = "MATH-C1A-ATOM-" + digest({"capability": cap, "pck": ref, "role": role, "index": i, "text": text})[:16]
        out.append({
            "atom_id": atom_id,
            "capability_ref": cap,
            "role": role,
            "text": text,
            "source_ref": ref,
        })
    return out


def _invariant_for_bucket(member_caps: set[str], primary_caps: list[str], lessons: dict[str, dict], assets: dict[str, dict], families: dict[str, dict]) -> dict:
    family_sets = [set(_family_refs(lessons[c])) for c in primary_caps]
    common = set.intersection(*family_sets) if family_sets and all(family_sets) else set()
    for ref in sorted(common):
        family = families.get(ref, {})
        text = str(family.get("problem_signature", {}).get("target_job", "")).strip()
        if text:
            return {"text": text, "source_type": "PROBLEM_FAMILY_TARGET_JOB", "source_ref": ref}

    # Singleton / bridge bucket: the bound PCK anchor is the governing teaching invariant.
    seed = primary_caps[0] if primary_caps else sorted(member_caps)[0]
    chosen = _choose_pck_asset(lessons[seed], assets)
    if chosen:
        ref, asset = chosen
        text = str(asset.get("anchor") or asset.get("ordinary_language_bridge") or "").strip()
        if text:
            return {"text": text, "source_type": "PCK_ANCHOR", "source_ref": ref}
    fail("CORE1A_BUCKET_INVARIANT_UNGROUNDED", seed)


def _bucket_title(primary_caps: list[str], member_caps: set[str], lessons: dict[str, dict]) -> str:
    seeds = primary_caps or sorted(member_caps)
    titles = []
    for cap in seeds:
        title = str(lessons[cap].get("learner_title") or "").strip()
        if title and title not in titles:
            titles.append(title)
    if not titles:
        fail("CORE1A_BUCKET_TITLE_MISSING")
    return titles[0] if len(titles) == 1 else " · ".join(titles)


def synthesize_bucket_plan(core1: dict, study_model: dict, assets: dict[str, dict], families: dict[str, dict]) -> dict:
    if core1.get("subject") != "MATHEMATICS" or study_model.get("subject") != "MATHEMATICS":
        fail("CORE1A_BUCKET_NON_MATH_INPUT")
    lessons, plans = _validate_binding(core1, study_model)

    components = _assign_supports(_direct_components(lessons, plans), plans)
    # Stable pedagogic order follows the earliest Core1 lesson position, never an invented difficulty score.
    order = {lesson["capability_ref"]: i for i, lesson in enumerate(core1.get("lessons", []))}
    components.sort(key=lambda c: min(order[x] for x in c))

    buckets = []
    seen: list[str] = []
    for comp in components:
        members = sorted(comp, key=lambda c: order[c])
        primary = [c for c in members if plans[c].get("scope_role") in DIRECT_ROLES]
        supporting = [c for c in members if c not in primary]
        lesson_refs = [lessons[c]["lesson_id"] for c in members]
        question_refs = sorted({q for c in members for q in plans[c].get("assessment_question_refs", [])})
        family_refs = sorted({f for c in members for f in _family_refs(lessons[c])})
        pck_refs = sorted({r for c in members for r in lessons[c].get("pck_asset_refs", [])})
        reps = sorted({r for c in members for r in plans[c].get("representation_requirements", [])})
        verification = sorted({r for c in members for r in plans[c].get("verification_requirements", [])})

        treatment_rows = []
        for c in members:
            p = plans[c]
            treatment_rows.append({
                "capability_ref": c,
                "learner_state_readiness": p["learner_state_readiness"],
                "learner_state_confidence": p["learner_state_confidence"],
                "learner_state_observation_refs": list(p.get("learner_state_observation_refs", [])),
                "treatment": p["treatment"],
                "priority_band": p["priority_band"],
            })

        edges = []
        member_set = set(members)
        for dependent in members:
            for prereq in plans[dependent].get("prerequisite_refs", []):
                if prereq in plans:
                    edges.append({
                        "prerequisite_ref": prereq,
                        "dependent_ref": dependent,
                        "inside_bucket": prereq in member_set,
                    })

        atoms = []
        for c in members:
            atoms.extend(_atoms_for_capability(c, lessons[c], assets))

        bucket_id = "MATH-C1AB-" + digest({
            "core1": core1["core1_study_plan_id"],
            "members": sorted(members),
            "families": family_refs,
        })[:16]
        buckets.append({
            "bucket_id": bucket_id,
            "title": _bucket_title(primary, comp, lessons),
            "bucket_invariant": _invariant_for_bucket(comp, primary, lessons, assets, families),
            "member_capability_refs": members,
            "primary_capability_refs": primary or members,
            "supporting_capability_refs": supporting,
            "source_core1_lesson_refs": lesson_refs,
            "assessment_question_refs": question_refs,
            # Core2 preserves the original assessment IDs; hint-to-atom binding is a later Core2-aware audit.
            "core2_question_refs": question_refs,
            "problem_family_refs": family_refs,
            "pck_asset_refs": pck_refs,
            "learner_treatment_by_capability": treatment_rows,
            "dependency_edges": edges,
            "learning_atoms": atoms,
            "representation_requirements": reps,
            "verification_requirements": verification,
        })
        seen.extend(members)

    required = sorted(lessons)
    duplicates = sorted({c for c in seen if seen.count(c) > 1})
    omitted = sorted(set(required) - set(seen))
    if duplicates or omitted or sorted(seen) != required:
        fail("CORE1A_BUCKET_COVERAGE_FAILED", f"duplicates={duplicates};omitted={omitted}")

    out = {
        "bucket_plan_id": "MATH-C1ABP-" + digest({
            "core1": core1["core1_study_plan_id"],
            "study_model": study_model["study_model_id"],
            "core1_digest": core1["plan_digest"],
            "study_digest": study_model["study_model_digest"],
        })[:16],
        "schema_version": "1.0.0",
        "subject": "MATHEMATICS",
        "source_core1_study_plan_ref": core1["core1_study_plan_id"],
        "source_core1_plan_digest": core1["plan_digest"],
        "source_study_model_ref": study_model["study_model_id"],
        "source_study_model_digest": study_model["study_model_digest"],
        "release_class": core1["release_class"],
        "buckets": buckets,
        "coverage": {
            "required_capability_refs": required,
            "bucketed_capability_refs": sorted(seen),
            "duplicate_capability_refs": duplicates,
            "omitted_capability_refs": omitted,
            "status": "PASS",
        },
        "plan_digest": "",
    }
    out["plan_digest"] = digest(out, "plan_digest")
    return out
