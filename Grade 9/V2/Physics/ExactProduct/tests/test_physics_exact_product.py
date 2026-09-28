#!/usr/bin/env python3
"""P-L falsifiers: fail-closed gates, no state impersonation, no fabricated review."""
import copy, json, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PHYS = ROOT.parent
REPO = ROOT.parents[3]
sys.path[:0] = [str(ROOT / "engine"), str(PHYS / "ColdStart" / "engine")]

from physics_cold_start_runner import run_cold_start  # noqa: E402
from evaluate_physics_exact_product import (  # noqa: E402
    build_candidate, evaluate, validate_release, validate_attestation, machine_findings,
    digest, PASS, FAIL, BLOCKED,
)
from audit_physics_exact_candidate import build_review  # noqa: E402

PASSES = []


def expect(code, fn):
    try:
        fn()
    except ValueError as e:
        assert str(e).startswith(code), (code, str(e))
        PASSES.append(code)
        return
    raise AssertionError("expected " + code)


def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


policy = load(ROOT / "registry" / "physics-exact-product-quality-policy.json")
primitive_registry = load(PHYS / "Representation" / "registry" / "physics-teaching-primitive-registry.json")
manifest = load(PHYS / "GENERATION_AUTHORITY_MANIFEST.json")

TMP = tempfile.TemporaryDirectory()
RUN = Path(TMP.name) / "with-attempts"
report, _ = run_cold_start(manifest, RUN, True, REPO)
closure = load(RUN / "coverage_closure.json")
core1_map = load(RUN / "core1_page_map.json")
core2_map = load(RUN / "core2_page_map.json")
core2_plan = load(RUN / "core2.json")


def candidate_for(**over):
    return build_candidate(
        over.get("run_dir", RUN), over.get("report", report), over.get("closure", closure),
        over.get("core1_map", core1_map), over.get("core2_map", core2_map),
        over.get("core2_plan", core2_plan), primitive_registry, policy,
    )


candidate = candidate_for()
ai_review = build_review(RUN, policy)
release = evaluate(candidate, policy, None, ai_review)
PASSES.append("EXACT_CANDIDATE_AND_RELEASE_BUILD_FROM_A_REAL_COLD_START_RUN")

# ------------------------------------------------------------- fail-closed --
assert candidate["machine_gate"] == "PASS", candidate["machine_findings"]
assert release["exit_code"] == BLOCKED
assert release["classification"] == policy["blocked_classification"]
PASSES.append("MACHINE_GREEN_WITHOUT_HUMAN_REVIEW_RETURNS_BLOCKED_NOT_PASS")

assert release["quality_states"]["PUBLICATION_ENGINEERING"] == "PASS"
for state in policy["human_settable_states"]:
    assert release["quality_states"][state] == "PENDING", state
assert release["quality_states"]["MATURE_DESIGN_QUALITY"] == "PENDING"
assert release["quality_states"]["REFERENCE_COMPARABILITY"] == "NOT_RUN"
PASSES.append("SEVEN_QUALITY_STATES_TRACKED_INDEPENDENTLY")

impersonating = copy.deepcopy(release)
impersonating["quality_states"]["PEDAGOGICAL_DESIGN"] = "PASS"
impersonating["release_digest"] = ""
impersonating["release_digest"] = digest(impersonating, "release_digest")
expect("MACHINE_GREEN_CLAIMED_AS_PEDAGOGY_PASS",
       lambda: validate_release(impersonating, candidate, policy))

mature_lie = copy.deepcopy(release)
mature_lie["quality_states"]["MATURE_DESIGN_QUALITY"] = "PASS"
mature_lie["release_digest"] = ""
mature_lie["release_digest"] = digest(mature_lie, "release_digest")
expect("MATURE_CLAIMED_WITH_A_PENDING_REVIEW",
       lambda: validate_release(mature_lie, candidate, policy))

blocked_as_pass = copy.deepcopy(release)
blocked_as_pass["exit_code"] = PASS
blocked_as_pass["release_digest"] = ""
blocked_as_pass["release_digest"] = digest(blocked_as_pass, "release_digest")
expect("BLOCKED_REPORTED_AS_PASS", lambda: validate_release(blocked_as_pass, candidate, policy))

early_comparison = copy.deepcopy(release)
early_comparison["quality_states"]["REFERENCE_COMPARABILITY"] = "PASS"
early_comparison["release_digest"] = ""
early_comparison["release_digest"] = digest(early_comparison, "release_digest")
expect("REFERENCE_COMPARISON_RUN_BEFORE_HUMAN_GATES",
       lambda: validate_release(early_comparison, candidate, policy))

effectiveness = copy.deepcopy(release)
effectiveness["learning_effectiveness"] = "VALIDATED"
effectiveness["release_digest"] = ""
effectiveness["release_digest"] = digest(effectiveness, "release_digest")
expect("LEARNING_EFFECTIVENESS_CLAIMED_FROM_A_POLISHED_PDF",
       lambda: validate_release(effectiveness, candidate, policy))

# -------------------------------------------------------- AI is not a human --
assert ai_review["review_class"] == "AI_ASSISTED_REFERENCE_REVIEW"
assert ai_review["authority"] == "ADVISORY_ONLY"
assert ai_review["sets_quality_states"] is False
assert ai_review["may_set_mature_classification"] is False
assert ai_review["artifact_sha256_refs"]
assert any(c["concern"] == "NO_HUMAN_HAS_READ_THIS_PRODUCT" for c in ai_review["advisory_concerns"])
PASSES.append("AI_PRE_REVIEW_IS_ADVISORY_AND_BOUND_TO_EXACT_BYTES")

overreaching = copy.deepcopy(ai_review)
overreaching["sets_quality_states"] = True
expect("AI_PRE_REVIEW_COUNTED_AS_HUMAN_REVIEW",
       lambda: evaluate(candidate, policy, None, overreaching))

promoted = copy.deepcopy(ai_review)
promoted["authority"] = "AUTHORITATIVE"
expect("AI_PRE_REVIEW_COUNTED_AS_HUMAN_REVIEW",
       lambda: evaluate(candidate, policy, None, promoted))

ai_as_attestation = {
    "quality_state": "PEDAGOGICAL_DESIGN",
    "review_class": "AI_ASSISTED_REFERENCE_REVIEW",
    "reviewer_role": "AUTHORIZED_PEDAGOGY",
    "attestation_ref": "AI-2026-001",
    "artifact_sha256_refs": [candidate["products"][0]["artifact_sha256"]],
    "outcome": "PASS",
}
expect("AI_PRE_REVIEW_COUNTED_AS_HUMAN_REVIEW",
       lambda: evaluate(candidate, policy, [ai_as_attestation], None))

unbound = {
    "quality_state": "SUBJECT_CORRECTNESS",
    "review_class": "SUBJECT_EXPERT_PASS",
    "reviewer_role": "AUTHORIZED_PHYSICS_SUBJECT",
    "attestation_ref": "SUBJ-2026-001",
    "artifact_sha256_refs": ["0" * 64],
    "outcome": "PASS",
}
expect("HUMAN_ATTESTATION_NOT_BOUND_TO_EXACT_BYTES",
       lambda: evaluate(candidate, policy, [unbound], None))

no_ref = dict(unbound, artifact_sha256_refs=[candidate["products"][0]["artifact_sha256"]],
              attestation_ref="")
expect("HUMAN_ATTESTATION_NOT_BOUND_TO_EXACT_BYTES",
       lambda: evaluate(candidate, policy, [no_ref], None))

wrong_role = dict(unbound, artifact_sha256_refs=[candidate["products"][0]["artifact_sha256"]],
                  reviewer_role="AUTHORIZED_PEDAGOGY")
expect("FABRICATED_REVIEWER_ROLE", lambda: evaluate(candidate, policy, [wrong_role], None))

machine_state = dict(unbound, quality_state="PUBLICATION_ENGINEERING",
                     artifact_sha256_refs=[candidate["products"][0]["artifact_sha256"]])
expect("FABRICATED_REVIEWER_ROLE", lambda: evaluate(candidate, policy, [machine_state], None))

# ---------------------------------------- a complete, properly bound review --
hashes = [p["artifact_sha256"] for p in candidate["products"]]
full = [
    {"quality_state": "SUBJECT_CORRECTNESS", "review_class": "SUBJECT_EXPERT_PASS",
     "reviewer_role": "AUTHORIZED_PHYSICS_SUBJECT", "attestation_ref": "SYNTHETIC-TEST-SUBJ",
     "artifact_sha256_refs": hashes, "outcome": "PASS"},
    {"quality_state": "PEDAGOGICAL_DESIGN", "review_class": "PEDAGOGY_EXPERT_PASS",
     "reviewer_role": "AUTHORIZED_PEDAGOGY", "attestation_ref": "SYNTHETIC-TEST-PED",
     "artifact_sha256_refs": hashes, "outcome": "PASS"},
    {"quality_state": "ASSESSMENT_DESIGN", "review_class": "ASSESSMENT_EXPERT_PASS",
     "reviewer_role": "AUTHORIZED_ASSESSMENT", "attestation_ref": "SYNTHETIC-TEST-ASM",
     "artifact_sha256_refs": hashes, "outcome": "PASS"},
    {"quality_state": "VISUAL_USABILITY", "review_class": "VISUAL_USABILITY_EXPERT_PASS",
     "reviewer_role": "AUTHORIZED_VISUAL_USABILITY", "attestation_ref": "SYNTHETIC-TEST-VIS",
     "artifact_sha256_refs": hashes, "outcome": "PASS"},
]
# These are synthetic attestations exercising the state machine only. They are NOT
# committed anywhere as real review, and the shipped run carries none of them.
all_pass = evaluate(candidate, policy, full, ai_review)
assert all_pass["quality_states"]["REFERENCE_COMPARABILITY"] == "READY_TO_RUN"
assert all_pass["quality_states"]["MATURE_DESIGN_QUALITY"] == "PENDING"
assert all_pass["exit_code"] == BLOCKED
PASSES.append("EVEN_FOUR_HUMAN_PASSES_STILL_BLOCK_UNTIL_THE_COMPARATOR_RUNS")

one_fail = copy.deepcopy(full)
one_fail[1]["outcome"] = "FAIL"
failed = evaluate(candidate, policy, one_fail, ai_review)
assert failed["exit_code"] == FAIL
assert failed["classification"] == policy["failed_classification"]
assert failed["quality_states"]["MATURE_DESIGN_QUALITY"] == "FAIL"
PASSES.append("A_FAILED_HUMAN_REVIEW_FAILS_THE_RELEASE")

mature_with_fail = copy.deepcopy(failed)
mature_with_fail["quality_states"]["MATURE_DESIGN_QUALITY"] = "PASS"
mature_with_fail["release_digest"] = ""
mature_with_fail["release_digest"] = digest(mature_with_fail, "release_digest")
expect("MATURE_CLAIMED_WITH_A_FAILED_REVIEW",
       lambda: validate_release(mature_with_fail, candidate, policy))

# ------------------------------------------------------------ machine gates --
assert not machine_findings(RUN, report, closure, core1_map, core2_map, core2_plan,
                            primitive_registry, policy)
PASSES.append("MACHINE_GATES_GREEN_ON_THE_REAL_PRODUCT")


def findings_codes(**over):
    return {f["code"] for f in machine_findings(
        over.get("run_dir", RUN), over.get("report", report), over.get("closure", closure),
        over.get("core1_map", core1_map), over.get("core2_map", core2_map),
        over.get("core2_plan", core2_plan), primitive_registry, policy)}


open_closure = copy.deepcopy(closure)
open_closure["closure_state"] = "OPEN"
assert "COVERAGE_CLOSURE_OPEN" in findings_codes(closure=open_closure)
PASSES.append("COVERAGE_CLOSURE_OPEN")

uncovered = copy.deepcopy(closure)
uncovered["source_coverage_matrix"]["uncovered_item_refs"] = ["Q1"]
assert "SOURCE_COVERAGE_RECONCILIATION_FAILURE" in findings_codes(closure=uncovered)
PASSES.append("SOURCE_COVERAGE_RECONCILIATION_FAILURE")

ext_uncovered = copy.deepcopy(closure)
ext_uncovered["external_corpus_coverage_matrix"]["uncovered_candidate_refs"] = ["PHY-EXT01"]
assert "EXTERNAL_CORPUS_RECONCILIATION_FAILURE" in findings_codes(closure=ext_uncovered)
PASSES.append("EXTERNAL_CORPUS_RECONCILIATION_FAILURE")

no_appendix = copy.deepcopy(report)
no_appendix["two_product_package"]["products"][0]["required_sections"] = ["MAIN_TEACHING"]
codes = findings_codes(report=no_appendix)
assert {"APPENDIX_A_MISSING", "APPENDIX_B_MISSING", "APPENDIX_C_MISSING"} <= codes
PASSES.append("APPENDIX_A_MISSING")
PASSES.append("APPENDIX_B_MISSING")
PASSES.append("APPENDIX_C_MISSING")

third = copy.deepcopy(report)
third["two_product_package"]["third_product_created"] = True
assert "THIRD_REQUIRED_PRODUCT_INSTEAD_OF_APPENDIX_C" in findings_codes(report=third)
PASSES.append("THIRD_REQUIRED_PRODUCT_INSTEAD_OF_APPENDIX_C")

flat = copy.deepcopy(report)
flat["two_product_package"]["products"][0]["vector_ops"] = 0
flat["two_product_package"]["products"][0]["figure_count"] = 0
codes = findings_codes(report=flat)
assert {"TEACHING_PRIMITIVE_LABEL_ONLY_NOT_REALIZED", "FIGURE_ABSENT_FROM_CORE1"} <= codes
PASSES.append("TEACHING_PRIMITIVE_LABEL_ONLY_NOT_REALIZED")
PASSES.append("FIGURE_ABSENT_FROM_CORE1")

drifted = copy.deepcopy(report)
drifted["two_product_package"]["products"][0]["artifact_sha256"] = "0" * 64
assert "EXACT_ARTIFACT_HASH_MISMATCH" in findings_codes(report=drifted)
PASSES.append("EXACT_ARTIFACT_HASH_MISMATCH")

tiny_font = copy.deepcopy(core1_map)
tiny_font["minimum_font_pt"] = 3.0
assert "MIN_FONT_SIZE_FAILURE" in findings_codes(core1_map=tiny_font)
PASSES.append("MIN_FONT_SIZE_FAILURE")

offpage = copy.deepcopy(core1_map)
offpage["page_metrics"][0]["bounds_violations"] = 2
assert "OFF_PAGE_TEXT" in findings_codes(core1_map=offpage)
PASSES.append("OFF_PAGE_TEXT")

label_only = copy.deepcopy(core1_map)
label_only["realization_summary"]["label_only_figure_count"] = 1
assert "TEACHING_PRIMITIVE_LABEL_ONLY_NOT_REALIZED" in findings_codes(core1_map=label_only)

thin_hints = copy.deepcopy(core2_plan)
thin_hints["transfer_pages"][0]["hint_ladder"] = thin_hints["transfer_pages"][0]["hint_ladder"][:1]
assert "HINT_SUPPORT_FAILURE" in findings_codes(core2_plan=thin_hints)
PASSES.append("HINT_SUPPORT_FAILURE")

no_solution = copy.deepcopy(core2_plan)
no_solution["transfer_pages"][0]["solution"]["verification_steps"] = []
assert "SOLUTION_FAILURE" in findings_codes(core2_plan=no_solution)
PASSES.append("SOLUTION_FAILURE")

missing_page = copy.deepcopy(core2_plan)
missing_page["transfer_pages"] = missing_page["transfer_pages"][:-1]
assert "ELIGIBLE_ITEM_MISSING_CORE2" in findings_codes(core2_plan=missing_page)
PASSES.append("ELIGIBLE_ITEM_MISSING_CORE2")

# a candidate with machine findings must FAIL, never merely BLOCK
bad_candidate = candidate_for(closure=open_closure)
assert bad_candidate["machine_gate"] == "FAIL"
bad_release = evaluate(bad_candidate, policy, None, None)
assert bad_release["exit_code"] == FAIL
assert bad_release["classification"] == policy["failed_classification"]
PASSES.append("MACHINE_FAILURE_FAILS_RATHER_THAN_BLOCKS")

# --------------------------------------------------------- PR #156 boundary --
assert policy["reference_comparator_id"] == "FROZEN_PR156_MATURE_DESIGN_COMPARATOR"
assert policy["reference_comparator_allowed_stage"] == "AFTER_ALL_HUMAN_GATES_PASS"
assert manifest["reference_comparator"]["forbidden_as_producer_input"] is True
assert report["runtime_dependency_audit"]["raw_pr156_used"] is False
reads = " ".join(report["runtime_dependency_audit"]["runtime_reads"]).lower()
for token in policy["forbidden_runtime_reference_fragments"]:
    assert token.lower() not in reads, token
PASSES.append("PR156_NOT_READ_BY_ANY_PRODUCER_STAGE")

TMP.cleanup()
print(f"PHY P-L exact-product falsifiers: {len(PASSES)} PASS")
for code in PASSES:
    print("  -", code)
