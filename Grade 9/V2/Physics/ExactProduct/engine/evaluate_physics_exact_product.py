#!/usr/bin/env python3
"""P-L — Physics exact-product quality gate (fail-closed).

    P-K cold-start output (two exact PDFs + page maps + run report + closure)
  + P-L quality policy
  + zero or more review attestations
  -> PhysicsExactProductCandidate  (machine evidence bound to exact bytes)
  -> PhysicsExactProductRelease    (independently tracked quality states)

Seven states are tracked separately and none may impersonate another:

    PUBLICATION_ENGINEERING   machine-settable
    SUBJECT_CORRECTNESS       authorized human only
    PEDAGOGICAL_DESIGN        authorized human only
    ASSESSMENT_DESIGN         authorized human only
    VISUAL_USABILITY          authorized human only
    MATURE_DESIGN_QUALITY     derived; every other state must be PASS
    REFERENCE_COMPARABILITY   derived; the PR #156 comparator may only run last

Exit codes: 0 PASS, 1 FAIL, 2 BLOCKED. Machine-green with a missing authorized
review returns 2, never 0.
"""
import argparse, copy, hashlib, json, re, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve()
ROOT = HERE.parents[1]
PHYS = HERE.parents[2]
sys.path[:0] = [str(PHYS / "ColdStart" / "engine"), str(PHYS / "Representation" / "engine")]

from physics_product_renderer import residual_internal_tokens  # noqa: E402
from physics_page_custody import reconciliation_errors  # noqa: E402

PASS, FAIL, BLOCKED = 0, 1, 2
ANSWER_LEAK_PATTERNS = [
    re.compile(r"\bsolution\b", re.I),
    re.compile(r"\bthe answer is\b", re.I),
    re.compile(r"\bcorrect option\b", re.I),
]


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


def pdf_text(path):
    try:
        r = subprocess.run(["pdftotext", str(path), "-"], capture_output=True, text=True, timeout=120)
        return r.stdout if r.returncode == 0 else None
    except (OSError, subprocess.SubprocessError):
        return None


# ------------------------------------------------------------ machine gates


def machine_findings(run_dir, run_report, closure, core1_map, core2_map, core2_plan,
                     primitive_registry, policy):
    """Every machine check. Returns a list of {code, detail} findings; empty means green."""
    findings = []

    def note(code, detail):
        if code not in policy["machine_failure_codes"]:
            fail("MACHINE_FAILURE_CODE_NOT_IN_POLICY", code)
        findings.append({"code": code, "detail": detail})

    run_dir = Path(run_dir)
    pkg = run_report["two_product_package"]
    products = {p["product_id"]: p for p in pkg["products"]}
    for pid in policy["required_product_ids"]:
        if pid not in products:
            note("MISSING_CORE1_PDF" if pid == "CORE_STUDY_GUIDE" else "MISSING_CORE2_PDF", pid)
    if pkg.get("third_product_created"):
        note("THIRD_REQUIRED_PRODUCT_INSTEAD_OF_APPENDIX_C", "package declares a third product")

    core1 = products.get("CORE_STUDY_GUIDE")
    core2 = products.get("TRANSFER_SOLUTION_BOOK")
    if core1:
        for section, code in (("APPENDIX_A_CORE_PRACTICE", "APPENDIX_A_MISSING"),
                              ("APPENDIX_B_CORE_SOLUTIONS", "APPENDIX_B_MISSING"),
                              ("APPENDIX_C_PRINTABLE_HANDOUT", "APPENDIX_C_MISSING")):
            if section not in core1["required_sections"]:
                note(code, section)
        if core1["figure_count"] < policy["minimum_figures_in_core1"]:
            note("FIGURE_ABSENT_FROM_CORE1", str(core1["figure_count"]))
        if core1["vector_ops"] <= 0:
            note("TEACHING_PRIMITIVE_LABEL_ONLY_NOT_REALIZED", "core study guide")

    minimums = {p["primitive_id"]: p["minimum_vector_ops"] for p in primitive_registry["primitives"]}
    for label, page_map, product in (("CORE_STUDY_GUIDE", core1_map, core1),
                                     ("TRANSFER_SOLUTION_BOOK", core2_map, core2)):
        if page_map is None or product is None:
            continue
        path = run_dir / product["artifact_path"]
        if not path.exists():
            note("MISSING_CORE1_PDF" if label == "CORE_STUDY_GUIDE" else "MISSING_CORE2_PDF",
                 product["artifact_path"])
            continue
        data = path.read_bytes()
        if sha_bytes(data) != product["artifact_sha256"] or sha_bytes(data) != page_map["artifact_sha256"]:
            note("EXACT_ARTIFACT_HASH_MISMATCH", label)
        errors = reconciliation_errors(page_map, page_map["page_width_pt"],
                                       page_map["page_height_pt"], minimums, 14)
        if errors:
            note("PHYSICAL_PAGE_CUSTODY_FAILURE", f"{label}: {errors[0]}")
        if page_map["realization_summary"]["label_only_figure_count"]:
            note("TEACHING_PRIMITIVE_LABEL_ONLY_NOT_REALIZED", label)
        if any(m["bounds_violations"] for m in page_map["page_metrics"]):
            note("OFF_PAGE_TEXT", label)
        if page_map.get("minimum_font_pt", 99) < policy["minimum_font_pt"]:
            note("MIN_FONT_SIZE_FAILURE", f"{label}:{page_map.get('minimum_font_pt')}")

        text = pdf_text(path)
        if text is not None:
            leaked = residual_internal_tokens(text)
            if leaked:
                note("INTERNAL_TOKEN_LEAKED_TO_LEARNER", f"{label}: {', '.join(leaked[:4])}")
            if label == "CORE_STUDY_GUIDE":
                marker = "Appendix C"
                idx = text.rfind(marker)
                if idx >= 0:
                    handout = text[idx:]
                    for pattern in ANSWER_LEAK_PATTERNS:
                        if pattern.search(handout):
                            note("HANDOUT_ANSWER_LEAKAGE", pattern.pattern)
                            break

    if closure["closure_state"] != "CLOSED":
        note("COVERAGE_CLOSURE_OPEN", closure["closure_state"])
    if closure["source_coverage_matrix"]["uncovered_item_refs"]:
        note("SOURCE_COVERAGE_RECONCILIATION_FAILURE",
             ",".join(closure["source_coverage_matrix"]["uncovered_item_refs"][:3]))
    if closure["external_corpus_coverage_matrix"]["uncovered_candidate_refs"]:
        note("EXTERNAL_CORPUS_RECONCILIATION_FAILURE",
             ",".join(closure["external_corpus_coverage_matrix"]["uncovered_candidate_refs"][:3]))

    published = {p["candidate_ref"] for p in core2_plan["transfer_pages"]}
    if set(core2_plan["eligible_candidate_refs"]) - published:
        note("ELIGIBLE_ITEM_MISSING_CORE2",
             ",".join(sorted(set(core2_plan["eligible_candidate_refs"]) - published)[:3]))
    for page in core2_plan["transfer_pages"]:
        if len(page["hint_ladder"]) < policy["minimum_hints_per_transfer_page"]:
            note("HINT_SUPPORT_FAILURE", page["page_id"])
        if not page["solution"]["verification_steps"] or not page["solution"]["sections"]:
            note("SOLUTION_FAILURE", page["page_id"])

    return findings


# -------------------------------------------------------------- attestations


def validate_attestation(att, policy, artifact_hashes):
    """An attestation is only admissible if a real authorized human bound it to exact bytes."""
    state = att.get("quality_state")
    if state not in policy["human_settable_states"]:
        fail("FABRICATED_REVIEWER_ROLE", f"{state} is not a human-settable state")
    if att.get("review_class") == "AI_ASSISTED_REFERENCE_REVIEW":
        fail("AI_PRE_REVIEW_COUNTED_AS_HUMAN_REVIEW", state)
    if att.get("reviewer_role") != policy["required_human_roles"][state]:
        fail("FABRICATED_REVIEWER_ROLE", f"{state}:{att.get('reviewer_role')}")
    if not att.get("attestation_ref"):
        fail("HUMAN_ATTESTATION_NOT_BOUND_TO_EXACT_BYTES", state + ":no attestation ref")
    bound = set(att.get("artifact_sha256_refs") or [])
    if not bound or not bound <= artifact_hashes:
        fail("HUMAN_ATTESTATION_NOT_BOUND_TO_EXACT_BYTES", state)
    if att.get("outcome") not in {"PASS", "FAIL"}:
        fail("FABRICATED_REVIEWER_ROLE", state + ":outcome")
    return True


# --------------------------------------------------------------- evaluation


def build_candidate(run_dir, run_report, closure, core1_map, core2_map, core2_plan,
                    primitive_registry, policy, candidate_id="PHY-P-L-EXACT-CANDIDATE-v1"):
    findings = machine_findings(run_dir, run_report, closure, core1_map, core2_map,
                                core2_plan, primitive_registry, policy)
    products = []
    for p in run_report["two_product_package"]["products"]:
        path = Path(run_dir) / p["artifact_path"]
        products.append({
            "product_id": p["product_id"],
            "artifact_path": p["artifact_path"],
            "artifact_sha256": p["artifact_sha256"],
            "artifact_bytes": p["artifact_bytes"],
            "artifact_exists": path.exists(),
            "page_count": p["page_count"],
            "figure_count": p["figure_count"],
            "vector_ops": p["vector_ops"],
            "required_sections": list(p["required_sections"]),
        })
    candidate = {
        "candidate_id": candidate_id,
        "schema_version": "1.0.0",
        "subject": "PHYSICS",
        "policy_ref": policy["policy_id"],
        "run_report_ref": run_report["report_id"],
        "run_report_digest": run_report["report_digest"],
        "coverage_closure_ref": closure["closure_id"],
        "coverage_closure_state": closure["closure_state"],
        "products": sorted(products, key=lambda x: x["product_id"]),
        "machine_findings": findings,
        "machine_gate": "PASS" if not findings else "FAIL",
        "exact_artifacts_present": all(p["artifact_exists"] for p in products),
        "candidate_digest": "",
    }
    candidate["candidate_digest"] = digest(candidate, "candidate_digest")
    return candidate


def evaluate(candidate, policy, attestations=None, ai_pre_review=None,
             release_id="PHY-P-L-EXACT-RELEASE-v1"):
    attestations = attestations or []
    artifact_hashes = {p["artifact_sha256"] for p in candidate["products"]}

    states = {s: "PENDING" for s in policy["required_quality_states"]}
    states["PUBLICATION_ENGINEERING"] = candidate["machine_gate"]
    states["REFERENCE_COMPARABILITY"] = "NOT_RUN"

    evidence = {}
    for att in attestations:
        validate_attestation(att, policy, artifact_hashes)
        states[att["quality_state"]] = att["outcome"]
        evidence[att["quality_state"]] = {
            "attestation_ref": att["attestation_ref"],
            "reviewer_role": att["reviewer_role"],
            "artifact_sha256_refs": sorted(att["artifact_sha256_refs"]),
        }

    if ai_pre_review is not None:
        if ai_pre_review.get("review_class") != policy["ai_pre_review"]["review_class"]:
            fail("AI_PRE_REVIEW_COUNTED_AS_HUMAN_REVIEW", "wrong review class")
        if ai_pre_review.get("authority") != policy["ai_pre_review"]["authority"]:
            fail("AI_PRE_REVIEW_COUNTED_AS_HUMAN_REVIEW", "authority is not advisory")
        if set(ai_pre_review.get("artifact_sha256_refs") or []) - artifact_hashes:
            fail("HUMAN_ATTESTATION_NOT_BOUND_TO_EXACT_BYTES", "ai pre-review artifact binding")
        if ai_pre_review.get("sets_quality_states"):
            fail("AI_PRE_REVIEW_COUNTED_AS_HUMAN_REVIEW", "ai review claims to set a quality state")

    human_states = policy["human_settable_states"]
    all_human_pass = all(states[s] == "PASS" for s in human_states)
    any_human_fail = any(states[s] == "FAIL" for s in human_states)

    # REFERENCE_COMPARABILITY: the frozen PR #156 comparator is admissible only last.
    if all_human_pass and states["PUBLICATION_ENGINEERING"] == "PASS":
        states["REFERENCE_COMPARABILITY"] = "READY_TO_RUN"
    # MATURE_DESIGN_QUALITY: derived, never declared.
    if any_human_fail or states["PUBLICATION_ENGINEERING"] == "FAIL":
        states["MATURE_DESIGN_QUALITY"] = "FAIL"
    elif all_human_pass and states["REFERENCE_COMPARABILITY"] == "PASS":
        states["MATURE_DESIGN_QUALITY"] = "PASS"
    else:
        states["MATURE_DESIGN_QUALITY"] = "PENDING"

    if states["PUBLICATION_ENGINEERING"] == "FAIL" or any_human_fail:
        classification, exit_code = policy["failed_classification"], FAIL
    elif states["MATURE_DESIGN_QUALITY"] == "PASS" and candidate["exact_artifacts_present"]:
        classification, exit_code = policy["mature_classification"], PASS
    else:
        classification, exit_code = policy["blocked_classification"], BLOCKED

    blocking = sorted(
        s for s in policy["required_quality_states"]
        if states[s] in {"PENDING", "NOT_RUN", "READY_TO_RUN"}
    )
    release = {
        "release_id": release_id,
        "schema_version": "1.0.0",
        "subject": "PHYSICS",
        "policy_ref": policy["policy_id"],
        "candidate_ref": candidate["candidate_id"],
        "candidate_digest": candidate["candidate_digest"],
        "quality_states": states,
        "state_evidence": evidence,
        "ai_pre_review_ref": ai_pre_review["review_id"] if ai_pre_review else None,
        "ai_pre_review_is_advisory_only": True,
        "learning_effectiveness": policy["learning_effectiveness_default"],
        "reference_comparator_id": policy["reference_comparator_id"],
        "reference_comparator_allowed_stage": policy["reference_comparator_allowed_stage"],
        "classification": classification,
        "exit_code": exit_code,
        "blocking_states": blocking,
        "blocking_reason": (
            "Machine publication-engineering gates are green, but no authorized human reviewer has "
            "examined these exact artifacts, so subject, pedagogical, assessment and visual states "
            "remain PENDING and the product is not mature."
            if exit_code == BLOCKED else
            "A machine or review gate failed." if exit_code == FAIL else
            "Every required gate resolved PASS."
        ),
        "release_digest": "",
    }
    release["release_digest"] = digest(release, "release_digest")
    validate_release(release, candidate, policy)
    return release


def validate_release(release, candidate, policy):
    if release["release_digest"] != digest(release, "release_digest"):
        fail("BLOCKED_REPORTED_AS_PASS", "release digest")
    states = release["quality_states"]
    if set(states) != set(policy["required_quality_states"]):
        fail("MACHINE_GREEN_CLAIMED_AS_PEDAGOGY_PASS", "state coverage")

    # a machine pass may never imply a human pass
    if states["PUBLICATION_ENGINEERING"] == "PASS" and not release["state_evidence"]:
        for s in policy["human_settable_states"]:
            if states[s] == "PASS":
                fail("MACHINE_GREEN_CLAIMED_AS_PEDAGOGY_PASS", s)
    for s in policy["human_settable_states"]:
        if states[s] == "PASS" and s not in release["state_evidence"]:
            fail("HUMAN_ATTESTATION_NOT_BOUND_TO_EXACT_BYTES", s)

    mature = states["MATURE_DESIGN_QUALITY"] == "PASS"
    if mature:
        pending = [s for s in policy["required_quality_states"]
                   if s != "MATURE_DESIGN_QUALITY" and states[s] == "PENDING"]
        if pending:
            fail("MATURE_CLAIMED_WITH_A_PENDING_REVIEW", ",".join(pending))
        failed = [s for s in policy["required_quality_states"] if states[s] == "FAIL"]
        if failed:
            fail("MATURE_CLAIMED_WITH_A_FAILED_REVIEW", ",".join(failed))
        if states["REFERENCE_COMPARABILITY"] != "PASS":
            fail("MATURE_CLAIMED_WITH_A_PENDING_REVIEW", "REFERENCE_COMPARABILITY")

    if states["REFERENCE_COMPARABILITY"] in {"PASS", "FAIL"}:
        if not all(states[s] == "PASS" for s in policy["human_settable_states"]):
            fail("REFERENCE_COMPARISON_RUN_BEFORE_HUMAN_GATES")

    if release["classification"] == policy["mature_classification"] and not mature:
        fail("BLOCKED_REPORTED_AS_PASS", "mature classification without a mature state")
    if release["exit_code"] == PASS and release["classification"] != policy["mature_classification"]:
        fail("BLOCKED_REPORTED_AS_PASS", "exit 0 without mature classification")
    if release["exit_code"] == BLOCKED and not release["blocking_states"]:
        fail("BLOCKED_REPORTED_AS_PASS", "blocked without a blocking state")

    if release["learning_effectiveness"] not in policy["learning_effectiveness_states"]:
        fail("LEARNING_EFFECTIVENESS_CLAIMED_FROM_A_POLISHED_PDF", release["learning_effectiveness"])
    if release["learning_effectiveness"] == "VALIDATED":
        fail("LEARNING_EFFECTIVENESS_CLAIMED_FROM_A_POLISHED_PDF",
             "a rendered PDF is not evidence of validated learning")
    if release["ai_pre_review_is_advisory_only"] is not True:
        fail("AI_PRE_REVIEW_COUNTED_AS_HUMAN_REVIEW", "advisory flag")
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-dir", required=True, help="a P-K cold-start run directory")
    ap.add_argument("--policy", default=str(ROOT / "registry" / "physics-exact-product-quality-policy.json"))
    ap.add_argument("--primitive-registry",
                    default=str(PHYS / "Representation" / "registry" / "physics-teaching-primitive-registry.json"))
    ap.add_argument("--attestations", help="optional JSON array of human review attestations")
    ap.add_argument("--ai-pre-review", help="optional advisory AI pre-review record")
    ap.add_argument("--out-candidate")
    ap.add_argument("--out-release")
    a = ap.parse_args()

    run_dir = Path(a.run_dir)
    policy = load(a.policy)
    candidate = build_candidate(
        run_dir, load(run_dir / "run_report.json"), load(run_dir / "coverage_closure.json"),
        load(run_dir / "core1_page_map.json"), load(run_dir / "core2_page_map.json"),
        load(run_dir / "core2.json"), load(a.primitive_registry), policy,
    )
    release = evaluate(candidate, policy,
                       load(a.attestations) if a.attestations else None,
                       load(a.ai_pre_review) if a.ai_pre_review else None)
    if a.out_candidate:
        Path(a.out_candidate).write_text(
            json.dumps(candidate, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if a.out_release:
        Path(a.out_release).write_text(
            json.dumps(release, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    label = {PASS: "PASS", FAIL: "FAIL", BLOCKED: "BLOCKED"}[release["exit_code"]]
    print(f"PHY P-L exact product: {label} — {release['classification']}")
    print(f"  machine gate: {candidate['machine_gate']} ({len(candidate['machine_findings'])} findings)")
    for state, value in sorted(release["quality_states"].items()):
        print(f"  {state:26s} {value}")
    if release["blocking_states"]:
        print("  blocking: " + ", ".join(release["blocking_states"]))
    print("  " + release["blocking_reason"])
    return release["exit_code"]


if __name__ == "__main__":
    raise SystemExit(main())
