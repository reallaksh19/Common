#!/usr/bin/env python3
"""P-K — Physics cold-start runner.

Drives the whole merged chain from repository artifacts alone:

    P-A intake fixtures -> P-B review -> P-C scope authority -> P-D problem semantics
    -> P-E learner evidence -> P-F study scope/model -> P-G Core1 -> P-H representations
    -> P-I Core2 transfer -> P-J coverage closure -> two learner PDFs

It runs twice over the *same* assessment, once with no AttemptSet and once with one,
and proves that the assessment-derived scope and the Physics truth are identical in
both. A fresh agent with no chat or issue history can execute this from
``GENERATION_AUTHORITY_MANIFEST.json`` alone.
"""
import argparse, copy, hashlib, json, sys
from pathlib import Path

HERE = Path(__file__).resolve()
COLD = HERE.parents[1]
PHYS = HERE.parents[2]
REPO = HERE.parents[5]
sys.path[:0] = [
    str(HERE.parent),
    str(PHYS / "ProblemSemantics" / "engine"),
    str(PHYS / "LearnerEvidence" / "engine"),
    str(PHYS / "StudySynthesis" / "engine"),
    str(PHYS / "CoreAuthoring" / "engine"),
    str(PHYS / "Representation" / "engine"),
    str(PHYS / "Core2Transfer" / "engine"),
    str(PHYS / "CoverageClosure" / "engine"),
]

import importlib.util  # noqa: E402


def _module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


from study_scope import derive_study_scope  # noqa: E402
from study_treatment_core import build_model  # noqa: E402
from build_physics_core1 import build_plan as build_core1, load_pck_registry  # noqa: E402
from build_physics_representations import build_bundle as build_representations  # noqa: E402
from realize_physics_representations import realize as realize_representations  # noqa: E402
from build_physics_core2_transfer import build_plan as build_core2  # noqa: E402
from build_physics_coverage_closure import build_closure  # noqa: E402
from physics_product_renderer import (  # noqa: E402
    render_core_study_guide, render_transfer_book, audit_product,
)


def canonical(o):
    return json.dumps(o, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(o, field=None):
    x = copy.deepcopy(o)
    if field:
        x.pop(field, None)
    return hashlib.sha256(canonical(x).encode("utf-8")).hexdigest()


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def fail(code, detail=""):
    raise ValueError(f"{code}: {detail}" if detail else code)


# ------------------------------------------------------------------ manifest


def verify_manifest(manifest):
    if manifest.get("subject") != "PHYSICS":
        fail("COLD_START_REQUIRES_CHAT_OR_ISSUE_HISTORY", "manifest subject")
    if manifest.get("manifest_digest") != digest(manifest, "manifest_digest"):
        fail("COLD_START_REQUIRES_CHAT_OR_ISSUE_HISTORY", "manifest digest")
    forbidden = set(manifest["runtime_input_contract"]["forbidden"])
    required_forbidden = {
        "ISSUE_HISTORY", "CHAT_HISTORY", "RAW_PR156", "MANUAL_SCOPE_AUTHORITY",
        "PREFILTERED_ELIGIBLE_EXTERNAL_SET", "MANUAL_LEARNER_STUDY_MODEL",
        "MANUAL_PROBLEM_FAMILY_MAP", "MANUAL_TEACHING_PRIMITIVE_SELECTION",
    }
    if not required_forbidden <= forbidden:
        fail("COLD_START_REQUIRES_CHAT_OR_ISSUE_HISTORY", "forbidden boundary incomplete")
    derived = set(manifest["derived_not_runtime_inputs"])
    if not {"PhysicsAssessmentScopeModel", "PhysicsLearnerStudyModel",
            "PhysicsRepresentationBundle", "PhysicsCore2TransferPlan"} <= derived:
        fail("GENERATION_STARTS_AFTER_SCOPE_WAS_MANUALLY_DERIVED")
    if len(manifest["two_product_topology"]) != 2:
        fail("THIRD_PRODUCT_PDF_CREATED")
    core = next((p for p in manifest["two_product_topology"] if p["product_id"] == "CORE_STUDY_GUIDE"), None)
    if not core or "APPENDIX_C_PRINTABLE_HANDOUT" not in core["required_sections"]:
        fail("APPENDIX_C_MISSING_FROM_CORE1")
    return True


def resolve(manifest, key, repo_root=REPO):
    rel = manifest["authorities"][key]
    path = Path(repo_root) / rel
    if not path.exists():
        fail("AUTHORITY_ARTIFACT_MISSING", rel)
    return path, rel


# ------------------------------------------------------------------- the run


def run_cold_start(manifest, out_dir, with_attempts, repo_root=REPO, run_id=None):
    verify_manifest(manifest)
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    reads = []

    def get(key):
        path, rel = resolve(manifest, key, repo_root)
        reads.append(rel)
        return load(path)

    semantics_engine = _module(
        "phy_pd_runner", Path(repo_root) / manifest["engines"]["problem_semantics"])
    evidence_engine = _module(
        "phy_pe_runner", Path(repo_root) / manifest["engines"]["learner_evidence"])
    reads.extend([manifest["engines"]["problem_semantics"], manifest["engines"]["learner_evidence"]])

    questions = get("question_set")
    topic_scope = get("declared_topic_scope")
    review_registry = get("item_validity_registry")
    review_policy = get("diagnostic_use_policy")
    capabilities = get("canonical_capabilities")
    scope_authority = get("scope_authority")
    scope_bindings = get("scope_bindings")
    role_registry = get("reasoning_role_registry")
    family_registry = get("problem_family_registry")
    verification_registry = get("verification_route_registry")
    item_registry = get("item_semantics_registry")
    badge_policy = get("guide_demand_badge_policy")
    observation_registry = get("observation_code_registry")
    diagnostic_policy = get("diagnostic_policy")
    treatment_policy = get("treatment_policy")
    instructional_profile = get("instructional_authoring_profile")
    completeness_policy = get("core1_completeness_policy")
    problem_profile = get("problem_authoring_profile")
    primitive_registry = get("teaching_primitive_registry")
    page_intent_profile = get("page_intent_profile")
    render_contract = get("figure_render_contract")
    transfer_corpus = get("external_transfer_corpus")
    transfer_classification = get("external_corpus_classification")
    core2_profile = get("core2_authoring_profile")
    transfer_badges = get("transfer_badge_policy")
    concept_segregation = get("concept_segregation")
    evidence_policy = get("transfer_evidence_policy")

    attempts = None
    evidence_ledger = None
    transfer_evidence = None
    if with_attempts:
        attempts = get("attempt_set")
        evidence_ledger = get("learner_evidence_ledger")
        transfer_evidence = get("transfer_evidence_ledger")

    # ---- P-D problem semantics (learner independent)
    semantics = semantics_engine.build_package(
        copy.deepcopy(questions), copy.deepcopy(topic_scope), copy.deepcopy(review_registry),
        copy.deepcopy(review_policy), copy.deepcopy(capabilities), copy.deepcopy(scope_authority),
        copy.deepcopy(scope_bindings), copy.deepcopy(role_registry), copy.deepcopy(family_registry),
        copy.deepcopy(verification_registry), copy.deepcopy(item_registry), copy.deepcopy(badge_policy),
    )

    # ---- P-E learner evidence
    kwargs = {}
    if with_attempts:
        kwargs = {"attempts": copy.deepcopy(attempts), "ledger": copy.deepcopy(evidence_ledger)}
    snapshot = evidence_engine.build_snapshot(
        copy.deepcopy(semantics), copy.deepcopy(questions),
        copy.deepcopy(observation_registry), copy.deepcopy(diagnostic_policy), **kwargs,
    )

    # ---- P-F study scope / model
    study_scope = derive_study_scope(copy.deepcopy(scope_bindings), copy.deepcopy(scope_authority),
                                     copy.deepcopy(semantics))
    study_model = build_model(copy.deepcopy(study_scope), copy.deepcopy(snapshot),
                              copy.deepcopy(treatment_policy))

    # ---- P-G Core1
    core1 = build_core1(copy.deepcopy(study_model), copy.deepcopy(study_scope), load_pck_registry(),
                        copy.deepcopy(instructional_profile), copy.deepcopy(completeness_policy),
                        copy.deepcopy(problem_profile))

    # ---- P-H representations + realization proof
    bundle = build_representations(copy.deepcopy(core1), copy.deepcopy(study_model),
                                   copy.deepcopy(questions), copy.deepcopy(primitive_registry),
                                   copy.deepcopy(page_intent_profile), copy.deepcopy(render_contract))
    rep_map, _ = realize_representations(bundle, primitive_registry, render_contract,
                                         out / "representation-proof")

    # ---- P-I Core2 transfer
    core2 = build_core2(copy.deepcopy(transfer_corpus), copy.deepcopy(transfer_classification),
                        copy.deepcopy(core1), copy.deepcopy(study_model), copy.deepcopy(study_scope),
                        copy.deepcopy(core2_profile), copy.deepcopy(transfer_badges),
                        copy.deepcopy(concept_segregation))

    # ---- two learner products
    minimums = {p["primitive_id"]: p["minimum_vector_ops"] for p in primitive_registry["primitives"]}
    core1_pdf = out / "physics-core-study-guide.pdf"
    core2_pdf = out / "physics-transfer-solution-book.pdf"
    core1_bytes, core1_map, core1_sections = render_core_study_guide(core1, bundle, core1_pdf)
    core2_bytes, core2_map, core2_sections = render_transfer_book(core2, core2_pdf)
    audit_product(core1_map, core1_bytes, minimums)
    audit_product(core2_map, core2_bytes, minimums)

    # ---- P-J coverage closure over the realized product
    closure = build_closure(copy.deepcopy(questions), copy.deepcopy(review_registry),
                            copy.deepcopy(core1), copy.deepcopy(bundle), copy.deepcopy(core2),
                            copy.deepcopy(transfer_classification), copy.deepcopy(study_scope),
                            copy.deepcopy(study_model), copy.deepcopy(evidence_policy),
                            copy.deepcopy(transfer_evidence), copy.deepcopy(rep_map))

    package = {
        "package_id": "PHY-P-K-TWO-PRODUCT-" + ("ATTEMPT" if with_attempts else "NO-ATTEMPT"),
        "schema_version": "1.0.0",
        "subject": "PHYSICS",
        "product_count": 2,
        "third_product_created": False,
        "products": [
            {
                "product_id": "CORE_STUDY_GUIDE",
                "artifact_path": core1_pdf.name,
                "artifact_sha256": sha_bytes(core1_bytes),
                "artifact_bytes": len(core1_bytes),
                "page_count": core1_map["physical_page_count"],
                "required_sections": core1_sections,
                "figure_count": core1_map["realization_summary"]["figure_count"],
                "vector_ops": core1_map["realization_summary"]["total_vector_ops"],
            },
            {
                "product_id": "TRANSFER_SOLUTION_BOOK",
                "artifact_path": core2_pdf.name,
                "artifact_sha256": sha_bytes(core2_bytes),
                "artifact_bytes": len(core2_bytes),
                "page_count": core2_map["physical_page_count"],
                "required_sections": core2_sections,
                "figure_count": core2_map["realization_summary"]["figure_count"],
                "vector_ops": core2_map["realization_summary"]["total_vector_ops"],
            },
        ],
    }

    report = {
        "report_id": run_id or ("PHY-P-K-RUN-" + ("ATTEMPT" if with_attempts else "NO-ATTEMPT")),
        "schema_version": "1.0.0",
        "subject": "PHYSICS",
        "run_mode": "WITH_ATTEMPTS" if with_attempts else "NO_ATTEMPT",
        "manifest_ref": manifest["manifest_id"],
        "manifest_digest": manifest["manifest_digest"],
        "input_custody": {
            "question_set_digest": digest(questions),
            "declared_topic_scope_digest": digest(topic_scope),
            "scope_authority_digest": scope_authority["authority_digest"],
            "attempt_set_digest": digest(attempts) if attempts is not None else None,
            "external_corpus_digest": transfer_corpus["corpus_digest"],
        },
        "assessment_truth": {
            "problem_semantics_digest": semantics["package_digest"],
            "study_scope_ref": study_scope["study_scope_id"],
            "study_scope_digest": study_scope["study_scope_digest"],
            "required_capability_refs": sorted(
                r["capability_ref"] for r in study_scope["capability_scope_records"]),
            "required_item_refs": list(study_scope["required_item_refs"]),
            "problem_family_refs": sorted(
                {f for r in study_scope["capability_scope_records"] for f in r["problem_family_refs"]}),
            "physical_model_refs": sorted(
                {m for r in study_scope["capability_scope_records"] for m in r["physical_model_refs"]}),
            "law_refs": sorted(
                {x for r in study_scope["capability_scope_records"] for x in r["law_refs"]}),
            "eligible_external_candidate_refs": list(core2["eligible_candidate_refs"]),
        },
        "stage_digests": {
            "P_D_problem_semantics": semantics["package_digest"],
            "P_E_learner_snapshot": digest(snapshot),
            "P_F_study_scope": study_scope["study_scope_digest"],
            "P_F_study_model": study_model["study_model_digest"],
            "P_G_core1_plan": core1["plan_digest"],
            "P_H_representation_bundle": bundle["bundle_digest"],
            "P_H_physical_page_map": rep_map["page_map_digest"],
            "P_I_core2_plan": core2["plan_digest"],
            "P_J_coverage_closure": closure["closure_digest"],
        },
        "two_product_package": package,
        "runtime_dependency_audit": {
            "chat_or_issue_history_used": False,
            "raw_pr156_used": False,
            "manual_precomputed_inputs_used": [],
            "runtime_reads": sorted(set(reads)),
        },
        "authority_trace": [
            {"decision_class": "REQUIRED_SCOPE",
             "authority_refs": [scope_authority["authority_id"], study_scope["study_scope_id"]],
             "resolution": "Required capabilities were derived from the P-C scope authority and the "
                           "question/capability bindings, not chosen by the agent."},
            {"decision_class": "TREATMENT",
             "authority_refs": [treatment_policy["policy_id"], study_model["study_model_id"]],
             "resolution": "Treatment per capability came from the P-F treatment policy applied to the "
                           "P-E learner snapshot."},
            {"decision_class": "TEACHING_PRIMITIVE_SELECTION",
             "authority_refs": [primitive_registry["registry_id"], page_intent_profile["profile_id"]],
             "resolution": "Primitives were selected from the capability's own representation "
                           "requirements through the page-intent profile."},
            {"decision_class": "EXTERNAL_ELIGIBILITY",
             "authority_refs": [transfer_classification["registry_id"]],
             "resolution": "External eligibility was classified against the scope authority before any "
                           "learner evidence was read."},
            {"decision_class": "COVERAGE_CLOSURE",
             "authority_refs": [evidence_policy["policy_id"], closure["closure_id"]],
             "resolution": "Closure state was computed from the coverage matrices and the physical page "
                           "map, not asserted."},
            {"decision_class": "FINAL_PAGE_COMPOSITION",
             "authority_refs": [core1["plan_id"], bundle["bundle_id"], core2["plan_id"]],
             "resolution": "Page composition followed the Core1 lesson order and the P-H page-intent "
                           "phases; placement evidence was emitted while drawing."},
        ],
        "summary": {
            "capability_count": len(study_scope["capability_scope_records"]),
            "core1_lesson_count": len(core1["lessons"]),
            "representation_count": len(bundle["representations"]),
            "core2_page_count": len(core2["transfer_pages"]),
            "closure_state": closure["closure_state"],
            "appendix_c_present": bool(core1["appendices"]["appendix_c"]["present"]),
            "total_vector_ops": (core1_map["realization_summary"]["total_vector_ops"]
                                 + core2_map["realization_summary"]["total_vector_ops"]),
        },
        "human_expert_review_states": {
            "SUBJECT_EXPERT_PASS": "PENDING",
            "PEDAGOGY_EXPERT_PASS": "PENDING",
            "ASSESSMENT_EXPERT_PASS": "PENDING",
            "VISUAL_USABILITY_EXPERT_PASS": "PENDING",
        },
        "report_digest": "",
    }
    report["report_digest"] = digest(report, "report_digest")

    artifacts = {
        "problem_semantics": semantics, "learner_snapshot": snapshot,
        "study_scope": study_scope, "study_model": study_model, "core1": core1,
        "representation_bundle": bundle, "representation_page_map": rep_map,
        "core2": core2, "coverage_closure": closure,
        "core1_page_map": core1_map, "core2_page_map": core2_map,
    }
    for name, obj in artifacts.items():
        (out / f"{name}.json").write_text(
            json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (out / "run_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return report, artifacts


def compare_runs(no_attempt, with_attempts, comparison_id="PHY-P-K-COMPARISON-v1"):
    a, b = no_attempt["assessment_truth"], with_attempts["assessment_truth"]
    ia, ib = no_attempt["input_custody"], with_attempts["input_custody"]
    invariants = {
        "question_set_digest_identical": ia["question_set_digest"] == ib["question_set_digest"],
        "declared_topic_scope_digest_identical":
            ia["declared_topic_scope_digest"] == ib["declared_topic_scope_digest"],
        "scope_authority_digest_identical": ia["scope_authority_digest"] == ib["scope_authority_digest"],
        "external_corpus_digest_identical": ia["external_corpus_digest"] == ib["external_corpus_digest"],
        "problem_semantics_identical": a["problem_semantics_digest"] == b["problem_semantics_digest"],
        "study_scope_digest_identical": a["study_scope_digest"] == b["study_scope_digest"],
        "required_capability_set_identical": a["required_capability_refs"] == b["required_capability_refs"],
        "required_item_set_identical": a["required_item_refs"] == b["required_item_refs"],
        "problem_family_truth_identical": a["problem_family_refs"] == b["problem_family_refs"],
        "physical_model_truth_identical": a["physical_model_refs"] == b["physical_model_refs"],
        "law_truth_identical": a["law_refs"] == b["law_refs"],
        "external_eligibility_identical":
            a["eligible_external_candidate_refs"] == b["eligible_external_candidate_refs"],
        "two_product_topology_identical":
            [p["product_id"] for p in no_attempt["two_product_package"]["products"]]
            == [p["product_id"] for p in with_attempts["two_product_package"]["products"]],
    }
    differences = {
        "study_model_digest_differs":
            no_attempt["stage_digests"]["P_F_study_model"] != with_attempts["stage_digests"]["P_F_study_model"],
        "core1_plan_digest_differs":
            no_attempt["stage_digests"]["P_G_core1_plan"] != with_attempts["stage_digests"]["P_G_core1_plan"],
    }
    comparison = {
        "comparison_id": comparison_id,
        "schema_version": "1.0.0",
        "subject": "PHYSICS",
        "no_attempt_report_ref": no_attempt["report_id"],
        "with_attempts_report_ref": with_attempts["report_id"],
        "invariants": invariants,
        "expected_differences": differences,
        "comparison_digest": "",
    }
    comparison["comparison_digest"] = digest(comparison, "comparison_digest")
    return comparison


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", default=str(PHYS / "GENERATION_AUTHORITY_MANIFEST.json"))
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--repo-root", default=str(REPO))
    a = ap.parse_args()
    manifest = load(a.manifest)
    out = Path(a.out_dir)
    no_attempt, _ = run_cold_start(manifest, out / "no-attempt", False, a.repo_root)
    with_attempts, _ = run_cold_start(manifest, out / "with-attempts", True, a.repo_root)
    comparison = compare_runs(no_attempt, with_attempts)
    (out / "comparison.json").write_text(
        json.dumps(comparison, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    failed = [k for k, v in comparison["invariants"].items() if not v]
    if failed:
        fail("ATTEMPT_RUN_CHANGES_REQUIRED_SCOPE", ",".join(failed))
    print(
        "PHY P-K cold start: PASS "
        f"(no-attempt {no_attempt['summary']['core1_lesson_count']} lessons / "
        f"{no_attempt['summary']['core2_page_count']} transfer pages, "
        f"with-attempts {with_attempts['summary']['core1_lesson_count']} lessons / "
        f"{with_attempts['summary']['core2_page_count']} transfer pages, "
        f"scope digest identical, two products each run)"
    )


if __name__ == "__main__":
    main()
