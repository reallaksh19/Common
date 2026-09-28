#!/usr/bin/env python3
"""Independent validation of a P-K cold-start run report and two-run comparison."""
import json, sys, warnings
from pathlib import Path

warnings.filterwarnings("ignore", category=DeprecationWarning)
from jsonschema import Draft202012Validator  # noqa: E402
from referencing import Registry, Resource  # noqa: E402

HERE = Path(__file__).resolve()
COLD = HERE.parents[1]
PHYS = HERE.parents[2]
sys.path.insert(0, str(HERE.parent))

from physics_cold_start_runner import digest, fail, verify_manifest  # noqa: E402


def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def schema(name):
    return load(COLD / "contracts" / name)


def _registry():
    names = [p.name for p in (COLD / "contracts").glob("*.schema.json")]
    return Registry().with_resources(
        [(n, Resource.from_contents(schema(n))) for n in names]
    )


def check(name, instance):
    Draft202012Validator(schema(name), registry=_registry()).validate(instance)


def validate_report(report, manifest, artifacts=None):
    verify_manifest(manifest)
    if report["report_digest"] != digest(report, "report_digest"):
        fail("FINAL_PAGE_DECISION_WITHOUT_AUTHORITY_TRACE", "report digest")
    if report["manifest_digest"] != manifest["manifest_digest"]:
        fail("COLD_START_REQUIRES_CHAT_OR_ISSUE_HISTORY", "manifest drift")

    audit = report["runtime_dependency_audit"]
    reads = audit["runtime_reads"]
    if audit["chat_or_issue_history_used"]:
        fail("COLD_START_REQUIRES_CHAT_OR_ISSUE_HISTORY")
    for token in ("issue", "chat", "conversation", "transcript"):
        if any(token in r.lower() for r in reads):
            fail("COLD_START_REQUIRES_CHAT_OR_ISSUE_HISTORY", token)
    if audit["raw_pr156_used"] or any("pull/156" in r.lower() or "pr156" in r.lower() for r in reads):
        fail("PR156_USED_AS_PRODUCER_INPUT_BEFORE_FINAL_COMPARISON")
    manual = set(audit["manual_precomputed_inputs_used"])
    for banned, code in (
        ("ScopeAuthority", "GENERATION_STARTS_AFTER_SCOPE_WAS_MANUALLY_DERIVED"),
        ("LearnerStudyModel", "MANUAL_STUDYMODEL_REQUIRED"),
        ("ProblemFamilyMap", "MANUAL_PROBLEM_FAMILY_MAP_REQUIRED"),
        ("PrefilteredEligibleExternalSet", "GENERATION_STARTS_FROM_PREFILTERED_ELIGIBLE_SET"),
    ):
        if banned in manual:
            fail(code)
    # every runtime read must be an artifact the manifest actually declares
    declared = set(manifest["authorities"].values()) | set(manifest["engines"].values())
    undeclared = [r for r in reads if r not in declared]
    if undeclared:
        fail("RUNTIME_READ_OUTSIDE_AUTHORITY_MANIFEST", ",".join(sorted(undeclared)[:3]))

    required = set(manifest["required_authority_trace_decisions"])
    traces = report["authority_trace"]
    got = {t["decision_class"] for t in traces}
    if not required <= got:
        fail("FINAL_PAGE_DECISION_WITHOUT_AUTHORITY_TRACE", ",".join(sorted(required - got)))
    for t in traces:
        if not t["authority_refs"] or not t["resolution"].strip():
            fail("FINAL_PAGE_DECISION_WITHOUT_AUTHORITY_TRACE", t["decision_class"])
        if t["resolution"].strip().lower() in {"agent decided", "by judgement", "chosen by the agent"}:
            fail("FINAL_PAGE_DECISION_WITHOUT_AUTHORITY_TRACE", t["decision_class"])

    pkg = report["two_product_package"]
    if pkg["product_count"] != 2 or len(pkg["products"]) != 2 or pkg["third_product_created"]:
        fail("THIRD_PRODUCT_PDF_CREATED")
    core = next((p for p in pkg["products"] if p["product_id"] == "CORE_STUDY_GUIDE"), None)
    if not core or "APPENDIX_C_PRINTABLE_HANDOUT" not in core["required_sections"]:
        fail("APPENDIX_C_MISSING_FROM_CORE1")
    if not report["summary"]["appendix_c_present"]:
        fail("APPENDIX_C_MISSING_FROM_CORE1", "summary")
    for product in pkg["products"]:
        if product["page_count"] < 1 or product["artifact_bytes"] < 1:
            fail("PRODUCT_ARTIFACT_EMPTY", product["product_id"])
    if pkg["products"][0]["vector_ops"] < 1:
        fail("TEACHING_PRIMITIVE_LABEL_ONLY_NOT_REALIZED", "core study guide has no vector graphics")

    if report["run_mode"] == "NO_ATTEMPT":
        if report["input_custody"]["attempt_set_digest"] is not None:
            fail("NO_ATTEMPT_RUN_INVENTS_PHYSICS_WEAKNESS", "attempt digest present")
        if artifacts is not None:
            states = [r["learner_state"] for r in artifacts["study_model"]["capability_records"]]
            if any(s != "UNKNOWN" for s in states):
                fail("NO_ATTEMPT_RUN_INVENTS_PHYSICS_WEAKNESS")
            modes = {l["lesson_mode"] for l in artifacts["core1"]["lessons"]}
            if modes != {"FULL_LEARNING"}:
                fail("NO_ATTEMPT_RUN_INVENTS_PHYSICS_WEAKNESS", "scope shortened without evidence")

    for state in report["human_expert_review_states"].values():
        if state == "PASS":
            fail("FAKE_HUMAN_REVIEW_STATE", "run report claims an expert pass")

    check("physics-cold-start-run-report.schema.json", report)
    check("physics-two-product-package.schema.json", pkg)
    return True


def validate_comparison(comparison, no_attempt, with_attempts):
    if comparison["comparison_digest"] != digest(comparison, "comparison_digest"):
        fail("ATTEMPT_RUN_CHANGES_REQUIRED_SCOPE", "comparison digest")
    inv = comparison["invariants"]
    scope_keys = [
        "question_set_digest_identical", "declared_topic_scope_digest_identical",
        "scope_authority_digest_identical", "problem_semantics_identical",
        "study_scope_digest_identical", "required_capability_set_identical",
        "required_item_set_identical",
    ]
    if not all(inv[k] for k in scope_keys):
        fail("ATTEMPT_RUN_CHANGES_REQUIRED_SCOPE",
             ",".join(k for k in scope_keys if not inv[k]))
    truth_keys = ["problem_family_truth_identical", "physical_model_truth_identical", "law_truth_identical"]
    if not all(inv[k] for k in truth_keys):
        fail("ATTEMPT_RUN_CHANGES_CANONICAL_PHYSICS_TRUTH",
             ",".join(k for k in truth_keys if not inv[k]))
    if not inv["external_corpus_digest_identical"] or not inv["external_eligibility_identical"]:
        fail("ATTEMPT_RUN_CHANGES_EXTERNAL_ELIGIBILITY")
    if not inv["two_product_topology_identical"]:
        fail("THIRD_PRODUCT_PDF_CREATED", "topology differs between runs")
    if no_attempt["input_custody"]["attempt_set_digest"] is not None:
        fail("ATTEMPT_RUN_CHANGES_REQUIRED_SCOPE", "no-attempt run carries an attempt digest")
    if with_attempts["input_custody"]["attempt_set_digest"] is None:
        fail("ATTEMPT_RUN_CHANGES_REQUIRED_SCOPE", "attempt run carries no attempt digest")
    check("physics-cold-start-comparison.schema.json", comparison)
    return True


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", required=True)
    ap.add_argument("--manifest", default=str(PHYS / "GENERATION_AUTHORITY_MANIFEST.json"))
    a = ap.parse_args()
    validate_report(load(a.report), load(a.manifest))
    print("PHY P-K cold-start report = PASS")


if __name__ == "__main__":
    main()
