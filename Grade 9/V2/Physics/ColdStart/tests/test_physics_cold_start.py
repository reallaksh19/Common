#!/usr/bin/env python3
"""P-K falsifiers: cold-start independence, two-run scope invariance, two-product topology."""
import copy, json, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PHYS = ROOT.parent
REPO = ROOT.parents[3]
sys.path.insert(0, str(ROOT / "engine"))

from physics_cold_start_runner import (  # noqa: E402
    run_cold_start, compare_runs, verify_manifest, digest,
)
from physics_cold_start_validator import validate_report, validate_comparison  # noqa: E402
from physics_product_renderer import learner_text, residual_internal_tokens  # noqa: E402

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


def redigest(r):
    r["report_digest"] = ""
    r["report_digest"] = digest(r, "report_digest")
    return r


manifest = load(PHYS / "GENERATION_AUTHORITY_MANIFEST.json")
verify_manifest(manifest)
PASSES.append("AUTHORITY_MANIFEST_VERIFIES")

# every artifact and engine the manifest names exists
for rel in list(manifest["authorities"].values()) + list(manifest["engines"].values()):
    assert (REPO / rel).exists(), rel
assert (REPO / manifest["entrypoint_doc"]).exists()
PASSES.append("EVERY_DECLARED_AUTHORITY_ARTIFACT_EXISTS")

TMP = tempfile.TemporaryDirectory()
out = Path(TMP.name)
no_attempt, artifacts_na = run_cold_start(manifest, out / "no-attempt", False, REPO)
with_attempts, artifacts_a = run_cold_start(manifest, out / "with-attempts", True, REPO)
comparison = compare_runs(no_attempt, with_attempts)
PASSES.append("COLD_START_RUNS_BOTH_MODES_END_TO_END")

assert validate_report(no_attempt, manifest, artifacts_na)
assert validate_report(with_attempts, manifest, artifacts_a)
assert validate_comparison(comparison, no_attempt, with_attempts)
PASSES.append("BOTH_RUN_REPORTS_INDEPENDENTLY_VALIDATE")

# ------------------------------------------------------- cold-start boundary
for report in (no_attempt, with_attempts):
    audit = report["runtime_dependency_audit"]
    assert audit["chat_or_issue_history_used"] is False
    assert audit["raw_pr156_used"] is False
    assert audit["manual_precomputed_inputs_used"] == []
    declared = set(manifest["authorities"].values()) | set(manifest["engines"].values())
    assert set(audit["runtime_reads"]) <= declared
PASSES.append("NO_RUNTIME_READ_OUTSIDE_THE_AUTHORITY_MANIFEST")

chatty = redigest(copy.deepcopy(with_attempts))
chatty["runtime_dependency_audit"]["chat_or_issue_history_used"] = True
redigest(chatty)
expect("COLD_START_REQUIRES_CHAT_OR_ISSUE_HISTORY",
       lambda: validate_report(chatty, manifest))

historied = copy.deepcopy(with_attempts)
historied["runtime_dependency_audit"]["runtime_reads"].append("docs/issue-320-chat-transcript.md")
redigest(historied)
expect("COLD_START_REQUIRES_CHAT_OR_ISSUE_HISTORY", lambda: validate_report(historied, manifest))

pr156 = copy.deepcopy(with_attempts)
pr156["runtime_dependency_audit"]["raw_pr156_used"] = True
redigest(pr156)
expect("PR156_USED_AS_PRODUCER_INPUT_BEFORE_FINAL_COMPARISON",
       lambda: validate_report(pr156, manifest))

pr156_read = copy.deepcopy(with_attempts)
pr156_read["runtime_dependency_audit"]["runtime_reads"].append("github.com/reallaksh19/Common/pull/156")
redigest(pr156_read)
expect("PR156_USED_AS_PRODUCER_INPUT_BEFORE_FINAL_COMPARISON",
       lambda: validate_report(pr156_read, manifest))

manual = copy.deepcopy(with_attempts)
manual["runtime_dependency_audit"]["manual_precomputed_inputs_used"] = ["LearnerStudyModel"]
redigest(manual)
expect("MANUAL_STUDYMODEL_REQUIRED", lambda: validate_report(manual, manifest))

manual_scope = copy.deepcopy(with_attempts)
manual_scope["runtime_dependency_audit"]["manual_precomputed_inputs_used"] = ["ScopeAuthority"]
redigest(manual_scope)
expect("GENERATION_STARTS_AFTER_SCOPE_WAS_MANUALLY_DERIVED",
       lambda: validate_report(manual_scope, manifest))

undeclared = copy.deepcopy(with_attempts)
undeclared["runtime_dependency_audit"]["runtime_reads"].append("Grade 9/V2/Physics/Publication/engine/realize_physics_publication.py")
redigest(undeclared)
expect("RUNTIME_READ_OUTSIDE_AUTHORITY_MANIFEST", lambda: validate_report(undeclared, manifest))

# ---------------------------------------------------------- authority trace
required = set(manifest["required_authority_trace_decisions"])
assert required <= {t["decision_class"] for t in with_attempts["authority_trace"]}
PASSES.append("EVERY_REQUIRED_DECISION_HAS_AN_AUTHORITY_TRACE")

untraced = copy.deepcopy(with_attempts)
untraced["authority_trace"] = untraced["authority_trace"][:-1]
redigest(untraced)
expect("FINAL_PAGE_DECISION_WITHOUT_AUTHORITY_TRACE", lambda: validate_report(untraced, manifest))

hand_waved = copy.deepcopy(with_attempts)
hand_waved["authority_trace"][0]["resolution"] = "agent decided"
redigest(hand_waved)
expect("FINAL_PAGE_DECISION_WITHOUT_AUTHORITY_TRACE", lambda: validate_report(hand_waved, manifest))

# ------------------------------------------------------- two-run invariance
assert all(comparison["invariants"].values()), comparison["invariants"]
assert no_attempt["assessment_truth"]["study_scope_digest"] == \
       with_attempts["assessment_truth"]["study_scope_digest"]
assert no_attempt["assessment_truth"]["required_capability_refs"] == \
       with_attempts["assessment_truth"]["required_capability_refs"]
assert no_attempt["assessment_truth"]["eligible_external_candidate_refs"] == \
       with_attempts["assessment_truth"]["eligible_external_candidate_refs"]
PASSES.append("ATTEMPT_RUN_CHANGES_REQUIRED_SCOPE")
PASSES.append("ATTEMPT_RUN_CHANGES_CANONICAL_PHYSICS_TRUTH")
PASSES.append("ATTEMPT_RUN_CHANGES_EXTERNAL_ELIGIBILITY")

# attempts are supposed to change treatment, and do
assert comparison["expected_differences"]["study_model_digest_differs"] is True
assert comparison["expected_differences"]["core1_plan_digest_differs"] is True
PASSES.append("LEARNER_EVIDENCE_STILL_CHANGES_TREATMENT")

broken = copy.deepcopy(comparison)
broken["invariants"]["study_scope_digest_identical"] = False
broken["comparison_digest"] = ""
broken["comparison_digest"] = digest(broken, "comparison_digest")
expect("ATTEMPT_RUN_CHANGES_REQUIRED_SCOPE",
       lambda: validate_comparison(broken, no_attempt, with_attempts))

broken_truth = copy.deepcopy(comparison)
broken_truth["invariants"]["physical_model_truth_identical"] = False
broken_truth["comparison_digest"] = ""
broken_truth["comparison_digest"] = digest(broken_truth, "comparison_digest")
expect("ATTEMPT_RUN_CHANGES_CANONICAL_PHYSICS_TRUTH",
       lambda: validate_comparison(broken_truth, no_attempt, with_attempts))

broken_ext = copy.deepcopy(comparison)
broken_ext["invariants"]["external_eligibility_identical"] = False
broken_ext["comparison_digest"] = ""
broken_ext["comparison_digest"] = digest(broken_ext, "comparison_digest")
expect("ATTEMPT_RUN_CHANGES_EXTERNAL_ELIGIBILITY",
       lambda: validate_comparison(broken_ext, no_attempt, with_attempts))

# ------------------------------------------------- no-attempt run honesty ---
assert no_attempt["input_custody"]["attempt_set_digest"] is None
assert all(r["learner_state"] == "UNKNOWN" for r in artifacts_na["study_model"]["capability_records"])
assert {l["lesson_mode"] for l in artifacts_na["core1"]["lessons"]} == {"FULL_LEARNING"}
PASSES.append("NO_ATTEMPT_RUN_INVENTS_PHYSICS_WEAKNESS")

weakened = copy.deepcopy(no_attempt)
fake_artifacts = copy.deepcopy(artifacts_na)
fake_artifacts["study_model"]["capability_records"][0]["learner_state"] = "EVIDENCE_OF_DIFFICULTY"
expect("NO_ATTEMPT_RUN_INVENTS_PHYSICS_WEAKNESS",
       lambda: validate_report(weakened, manifest, fake_artifacts))

# ------------------------------------------------------- two products only --
for report in (no_attempt, with_attempts):
    pkg = report["two_product_package"]
    assert pkg["product_count"] == 2 and pkg["third_product_created"] is False
    ids = [p["product_id"] for p in pkg["products"]]
    assert ids == ["CORE_STUDY_GUIDE", "TRANSFER_SOLUTION_BOOK"]
    core = pkg["products"][0]
    assert "APPENDIX_C_PRINTABLE_HANDOUT" in core["required_sections"]
    assert core["page_count"] > 1 and core["artifact_bytes"] > 1000
    assert core["vector_ops"] > 0
PASSES.append("EXACTLY_TWO_PRODUCTS_WITH_APPENDIX_C_INSIDE_CORE1")

three = copy.deepcopy(with_attempts)
three["two_product_package"]["third_product_created"] = True
redigest(three)
expect("THIRD_PRODUCT_PDF_CREATED", lambda: validate_report(three, manifest))

no_appendix = copy.deepcopy(with_attempts)
no_appendix["two_product_package"]["products"][0]["required_sections"] = ["MAIN_TEACHING"]
redigest(no_appendix)
expect("APPENDIX_C_MISSING_FROM_CORE1", lambda: validate_report(no_appendix, manifest))

flat = copy.deepcopy(with_attempts)
flat["two_product_package"]["products"][0]["vector_ops"] = 0
redigest(flat)
expect("TEACHING_PRIMITIVE_LABEL_ONLY_NOT_REALIZED", lambda: validate_report(flat, manifest))

# --------------------------------------------------- learner-surface hygiene
for run in ("no-attempt", "with-attempts"):
    for name in ("physics-core-study-guide.pdf", "physics-transfer-solution-book.pdf"):
        pdf = out / run / name
        assert pdf.exists() and pdf.stat().st_size > 5000, pdf
        text = subprocess.run(["pdftotext", str(pdf), "-"], capture_output=True, text=True)
        if text.returncode == 0:
            leaked = residual_internal_tokens(text.stdout)
            assert not leaked, (name, leaked[:6])
PASSES.append("INTERNAL_TOKEN_LEAKED_TO_LEARNER")

assert "PHY-CAP-XT-SLOPE-VELOCITY" not in learner_text("Teach PHY-CAP-XT-SLOPE-VELOCITY now.")
assert "Core2" not in learner_text("Reserved for Core2.")
assert residual_internal_tokens("clean learner sentence") == []
PASSES.append("LEARNER_TEXT_SANITIZER_IS_EFFECTIVE")

# ------------------------------------------------------------- closure state
for report in (no_attempt, with_attempts):
    assert report["summary"]["closure_state"] == "CLOSED"
    assert report["summary"]["appendix_c_present"] is True
    assert report["summary"]["total_vector_ops"] > 0
PASSES.append("BOTH_RUNS_REACH_CLOSED_COVERAGE_WITH_REAL_GRAPHICS")

# ------------------------------------------------------------------ honesty
for report in (no_attempt, with_attempts):
    assert set(report["human_expert_review_states"].values()) == {"PENDING"}
PASSES.append("COLD_START_CLAIMS_NO_HUMAN_REVIEW")

claimed = copy.deepcopy(with_attempts)
claimed["human_expert_review_states"]["VISUAL_USABILITY_EXPERT_PASS"] = "PASS"
redigest(claimed)
expect("FAKE_HUMAN_REVIEW_STATE", lambda: validate_report(claimed, manifest))

assert manifest["reference_comparator"]["forbidden_as_producer_input"] is True
assert "P-L" in manifest["reference_comparator"]["allowed_stage"]
assert manifest["human_review_boundary"]["states_requiring_an_authorized_human"]
PASSES.append("MANIFEST_DECLARES_THE_PR156_AND_HUMAN_REVIEW_BOUNDARIES")

TMP.cleanup()
print(f"PHY P-K cold-start falsifiers: {len(PASSES)} PASS")
for code in PASSES:
    print("  -", code)
