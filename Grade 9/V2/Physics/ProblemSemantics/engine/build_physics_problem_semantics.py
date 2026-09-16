#!/usr/bin/env python3
import argparse, copy, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import physics_problem_semantics_core as _core
from physics_problem_semantics_core import *  # noqa: F401,F403,E402


def _consume_scope_bundle(precomputed_scope, scope_authority, scope_bindings):
    if not isinstance(precomputed_scope, (tuple, list)) or len(precomputed_scope) != 4:
        fail("P_D_PRECOMPUTED_SCOPE_SHAPE")
    scope_model, coverage, report, prereq = copy.deepcopy(precomputed_scope)
    if scope_model.get("scope_model_digest") != dwo(scope_model, "scope_model_digest"):
        fail("P_D_PRECOMPUTED_SCOPE_DIGEST")
    if coverage.get("matrix_digest") != dwo(coverage, "matrix_digest"):
        fail("P_D_PRECOMPUTED_COVERAGE_DIGEST")
    if report.get("report_digest") != dwo(report, "report_digest"):
        fail("P_D_PRECOMPUTED_RECONCILIATION_DIGEST")
    if prereq.get("closure_digest") != dwo(prereq, "closure_digest"):
        fail("P_D_PRECOMPUTED_PREREQUISITE_DIGEST")
    if scope_model.get("authority_ref") != scope_authority["authority_id"] or report.get("authority_ref") != scope_authority["authority_id"]:
        fail("P_D_PRECOMPUTED_SCOPE_AUTHORITY_MISMATCH")
    if scope_model.get("binding_registry_ref") != scope_bindings["binding_registry_id"] or report.get("binding_registry_ref") != scope_bindings["binding_registry_id"]:
        fail("P_D_PRECOMPUTED_SCOPE_BINDING_MISMATCH")
    if coverage.get("scope_model_ref") != scope_model["scope_model_id"]:
        fail("P_D_PRECOMPUTED_COVERAGE_SCOPE_MISMATCH")
    if scope_model.get("attempt_data_consumed") or report.get("attempt_data_consumed"):
        fail("P_D_CONSUMES_LEARNER_DATA")
    return scope_model, coverage, report, prereq


def build_package(q, s, review_reg, review_policy, canonical_caps, scope_authority, scope_bindings,
                  role_reg, family_reg, verification_reg, item_reg, badge_policy, precomputed_scope=None):
    if precomputed_scope is None:
        return _core.build_package(
            q, s, review_reg, review_policy, canonical_caps, scope_authority, scope_bindings,
            role_reg, family_reg, verification_reg, item_reg, badge_policy,
        )

    scope_model, coverage, report, prereq = _consume_scope_bundle(
        precomputed_scope, scope_authority, scope_bindings)
    if scope_model["attempt_data_consumed"] or report["attempt_data_consumed"]:
        fail("P_D_CONSUMES_LEARNER_DATA")
    if item_reg["upstream_question_set_ref"] != q["question_set_id"] or item_reg["upstream_scope_binding_registry_ref"] != scope_bindings["binding_registry_id"]:
        fail("ITEM_SEMANTIC_PROFILE_UPSTREAM_MISMATCH")
    roles, aliases = _core.validate_role_registry(role_reg, scope_authority)
    families = _core.validate_family_registry(family_reg, scope_authority, roles)
    verification = _core.validate_verification_registry(verification_reg, families, scope_authority)
    profiles, mapped = _core.validate_item_registry(item_reg, coverage, families)
    _core.validate_policy(badge_policy)
    items = []
    for item in sorted(mapped):
        cov = mapped[item]; p = profiles[item]; f = families[p["primary_family_ref"]]
        route = _core.instantiate_route(item, cov, p, f, aliases)
        _core.validate_frame_and_phase(item, cov, f, route)
        mv = _core.build_validity_binding(item, cov, f, route)
        vr = [verification[families[x]["verification_route_ref"]] for x in p["family_refs"]]
        covered = {c["obligation_ref"] for r in vr for c in r["checks"]}
        if not set(cov["verification_obligations"]) <= covered:
            fail("VERIFICATION_ROUTE_MISSING", f"{item}:{sorted(set(cov['verification_obligations'])-covered)}")
        vector = _core.build_vector(item, p, badge_policy, route)
        badge = _core.derive_badge(item, cov, vector, route, vr, badge_policy)
        items.append({
            "item_ref": item, "question_ref": cov["question_ref"], "part_ref": cov["part_ref"],
            "mapping_state": cov["mapping_state"], "resolution_status": cov["resolution_status"],
            "source_integrity_state": cov["source_integrity_state"], "validity_state": cov["validity_state"],
            "diagnostic_use": cov["diagnostic_use"], "family_refs": p["family_refs"],
            "primary_family_ref": p["primary_family_ref"], "graph_operations": p["graph_operations"],
            "reference_frame": cov["reference_frame"], "phase_structure": cov["phase_structure"],
            "reasoning_route": route, "model_validity_binding": mv,
            "verification_route_refs": [r["verification_route_id"] for r in vr],
            "demand_vector": vector, "guide_demand_badge": badge,
        })
    summary = {
        "item_count": len(items),
        "blocked_count": sum(1 for x in items if x["resolution_status"] == "BLOCKED"),
        "family_count": len(families),
        "badge_counts": dict(sorted(_core.Counter((x["guide_demand_badge"]["label"] or "WITHHELD") for x in items).items())),
    }
    pkg = {
        "package_id": "PHY-G9-MOTION-PD-PROBLEM-SEMANTICS-v1", "schema_version": "1.0.0", "subject": "PHYSICS",
        "question_set_ref": q["question_set_id"], "scope_model_ref": scope_model["scope_model_id"],
        "scope_coverage_ref": coverage["coverage_matrix_id"], "scope_reconciliation_ref": report["reconciliation_id"],
        "role_registry_ref": role_reg["registry_id"], "family_registry_ref": family_reg["registry_id"],
        "verification_registry_ref": verification_reg["registry_id"], "badge_policy_ref": badge_policy["policy_id"],
        "learner_support_independent": True, "attempt_data_consumed": False, "items": items, "summary": summary,
        "package_digest": "",
    }
    pkg["package_digest"] = dwo(pkg, "package_digest")
    return pkg


def main():
    ap = argparse.ArgumentParser()
    for x in ["questions", "topic-scope", "review-registry", "review-policy", "canonical-capabilities",
              "scope-authority", "scope-bindings", "role-registry", "family-registry", "verification-registry",
              "item-registry", "badge-policy", "out"]:
        ap.add_argument("--" + x, required=True)
    a = ap.parse_args()
    pkg = build_package(load(a.questions), load(a.topic_scope), load(a.review_registry), load(a.review_policy),
                        load(a.canonical_capabilities), load(a.scope_authority), load(a.scope_bindings),
                        load(a.role_registry), load(a.family_registry), load(a.verification_registry),
                        load(a.item_registry), load(a.badge_policy))
    write(a.out, pkg)


if __name__ == "__main__":
    main()
