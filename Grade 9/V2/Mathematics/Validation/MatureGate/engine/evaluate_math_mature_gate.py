#!/usr/bin/env python3
import argparse, copy, hashlib, json
from pathlib import Path
from jsonschema import Draft202012Validator

ROOT=Path(__file__).resolve().parents[1]
MATH=ROOT.parents[1]


def load(path): return json.loads(Path(path).read_text(encoding="utf-8"))
def canon(value): return json.dumps(value,sort_keys=True,separators=(",",":"),ensure_ascii=False)
def digest(value,omit=None):
    x=copy.deepcopy(value)
    if omit and isinstance(x,dict): x.pop(omit,None)
    return hashlib.sha256(canon(x).encode("utf-8")).hexdigest()
def fail(code,detail=""): raise ValueError(f"{code}:{detail}" if detail else code)
def schema(name): return load(ROOT/"contracts"/name)
def check_schema(name,obj): Draft202012Validator(schema(name)).validate(obj)

QUALITY_KEYS=["PUBLICATION_ENGINEERING","SUBJECT_CORRECTNESS","PEDAGOGICAL_DESIGN","ASSESSMENT_DESIGN","VISUAL_USABILITY","MATURE_DESIGN_QUALITY","REFERENCE_COMPARABILITY"]
REVIEW_GATE={"SUBJECT":"SUBJECT_CORRECTNESS","PEDAGOGY":"PEDAGOGICAL_DESIGN","ASSESSMENT":"ASSESSMENT_DESIGN","VISUAL":"VISUAL_USABILITY"}


def pck_release_legal(candidate):
    """True only when the bound Core1 PCK carries authorized expert review.

    An older binding that predates provisional PCK tracking is treated as
    release-legal only if it declares PRODUCTION_PLAN_READY, which by
    construction requires expert-reviewed promotions upstream.
    """
    if "pck_release_legal" in candidate:
        return bool(candidate["pck_release_legal"]) and candidate.get("pck_expert_review_state") in {"PASS","NOT_REQUIRED"}
    return candidate["core1_authoring_status"]=="PRODUCTION_PLAN_READY"


def validate_policy(policy):
    if policy["policy_digest"]!=digest(policy,"policy_digest"): fail("MATURE_QUALITY_POLICY_DIGEST_MISMATCH")
    if policy["quality_state_order"]!=QUALITY_KEYS: fail("MATURE_QUALITY_STATE_ORDER_DRIFT")
    if set(policy["required_human_dimensions"])!=set(REVIEW_GATE): fail("MATURE_HUMAN_DIMENSION_COVERAGE_DRIFT")
    if policy["human_dimension_to_gate"]!=REVIEW_GATE: fail("MATURE_REVIEW_GATE_MAPPING_DRIFT")
    return True


def validate_candidate(candidate):
    check_schema("math-exact-candidate-binding.schema.json",candidate)
    if candidate["binding_digest"]!=digest(candidate,"binding_digest"): fail("EXACT_CANDIDATE_BINDING_DIGEST_MISMATCH")
    if candidate["raw_mature_reference_runtime_used"]: fail("RAW_MATURE_REFERENCE_USED_AS_RUNTIME_TEMPLATE")
    if candidate["candidate_class"]=="RENDERED_TWO_PRODUCT_EXACT_CANDIDATE":
        if candidate["materialization_state"]!="RENDERED_EXACT": fail("RENDERED_CANDIDATE_STATE_MISMATCH")
        if len(candidate["artifacts"])!=2 or {x["artifact_role"] for x in candidate["artifacts"]}!={"CORE1_STUDY_GUIDE","CORE2_TRANSFER_BOOK"}: fail("EXACT_TWO_PRODUCT_TOPOLOGY_REQUIRED")
        if candidate["artifact_set_digest"]!=digest(candidate["artifacts"]): fail("EXACT_ARTIFACT_SET_DIGEST_MISMATCH")
        if candidate["core1_authoring_status"] not in {"PRODUCTION_PLAN_READY","PROVISIONAL_PLAN_READY"}: fail("CORE1_SUMMARY_LEVEL_BUT_MARKED_MATURE")
        if candidate["upstream_blockers"]: fail("RENDERED_CANDIDATE_WITH_UPSTREAM_BLOCKER",candidate["upstream_blockers"][0])
        if candidate.get("pck_release_legal") is True and candidate.get("pck_expert_review_state")!="PASS":
            fail("PROVISIONAL_PROMOTION_CLAIMED_PRODUCER_LEGAL",candidate["candidate_id"])
    else:
        if candidate["artifacts"] or candidate["artifact_set_digest"] is not None: fail("SEMANTIC_ONLY_CANDIDATE_HAS_RENDERED_ARTIFACTS")
    return True


def validate_review_receipt(receipt,candidate,gate_mode):
    check_schema("math-exact-review-receipt.schema.json",receipt)
    if receipt["receipt_digest"]!=digest(receipt,"receipt_digest"): fail("HUMAN_REVIEW_RECEIPT_DIGEST_MISMATCH",receipt["receipt_id"])
    if candidate["artifact_set_digest"] is None: fail("HUMAN_REVIEW_NOT_BOUND_TO_EXACT_ARTIFACT",receipt["receipt_id"])
    if receipt["candidate_digest"]!=candidate["binding_digest"] or receipt["artifact_set_digest"]!=candidate["artifact_set_digest"]:
        fail("HUMAN_REVIEW_NOT_BOUND_TO_EXACT_ARTIFACT",receipt["receipt_id"])
    dim=receipt["review_dimension"]
    if dim in {"SUBJECT","PEDAGOGY","VISUAL"} and receipt["source_system"]!="SHARED_HUMAN_REVIEW_INTAKE": fail("HUMAN_REVIEW_SOURCE_AUTHORITY_INVALID",dim)
    if dim=="ASSESSMENT" and receipt["source_system"]!="MATH_ASSESSMENT_REVIEW_INTAKE": fail("ASSESSMENT_REVIEW_SOURCE_AUTHORITY_INVALID")
    if not receipt["authorized"]: fail("HUMAN_REVIEW_NOT_AUTHORIZED",receipt["receipt_id"])
    if gate_mode=="REAL_RELEASE":
        if receipt["review_mode"]!="REAL_RELEASE" or receipt["fixture_class"]!="REAL" or not receipt["release_evidence_eligible"]:
            fail("TEST_ONLY_REVIEW_USED_FOR_REAL_RELEASE",receipt["receipt_id"])
    else:
        if receipt["review_mode"]!="TEST_ONLY" or receipt["fixture_class"]!="TEST_ONLY_SYNTHETIC" or receipt["release_evidence_eligible"]:
            fail("TEST_REVIEW_CUSTODY_INVALID",receipt["receipt_id"])
    return True


def validate_machine(machine,candidate):
    required={"evidence_id","candidate_digest","artifact_set_digest","machine_falsifiers","publication_engineering","exact_artifact_custody","failed_falsifiers"}
    if set(machine)!=required: fail("MACHINE_EVIDENCE_SHAPE_INVALID")
    if machine["candidate_digest"]!=candidate["binding_digest"] or machine["artifact_set_digest"]!=candidate["artifact_set_digest"]: fail("MACHINE_EVIDENCE_NOT_BOUND_TO_EXACT_ARTIFACT")
    if machine["machine_falsifiers"] not in {"PASS","FAIL"} or machine["publication_engineering"] not in {"PASS","FAIL"} or machine["exact_artifact_custody"] not in {"PASS","FAIL"}: fail("MACHINE_EVIDENCE_STATE_INVALID")
    if machine["failed_falsifiers"] and machine["machine_falsifiers"]=="PASS": fail("MACHINE_GREEN_WITH_FAILED_FALSIFIER")
    return True


def validate_ai(ai,candidate):
    required={"pre_review_id","candidate_digest","artifact_set_digest","status","unresolved_major_count"}
    if set(ai)!=required: fail("AI_PRE_REVIEW_SHAPE_INVALID")
    if ai["candidate_digest"]!=candidate["binding_digest"] or ai["artifact_set_digest"]!=candidate["artifact_set_digest"]: fail("AI_PRE_REVIEW_NOT_BOUND_TO_EXACT_ARTIFACT")
    if ai["status"] not in {"PASS","FAIL"} or not isinstance(ai["unresolved_major_count"],int) or ai["unresolved_major_count"]<0: fail("AI_PRE_REVIEW_STATE_INVALID")
    if ai["status"]=="PASS" and ai["unresolved_major_count"]>0: fail("AI_PRE_REVIEW_PASS_WITH_MAJOR_FINDINGS")
    return True


def validate_reference(reference,candidate,gate_mode):
    required={"validation_id","candidate_digest","artifact_set_digest","status","mode","fixture_class","reference_access_phase","raw_reference_used_as_runtime_template","release_evidence_eligible"}
    if set(reference)!=required: fail("REFERENCE_VALIDATION_SHAPE_INVALID")
    if reference["candidate_digest"]!=candidate["binding_digest"] or reference["artifact_set_digest"]!=candidate["artifact_set_digest"]: fail("REFERENCE_VALIDATION_NOT_BOUND_TO_EXACT_ARTIFACT")
    if reference["reference_access_phase"]!="FINAL_COMPARATIVE_VALIDATION" or reference["raw_reference_used_as_runtime_template"]: fail("RAW_MATURE_REFERENCE_USED_AS_RUNTIME_TEMPLATE")
    if reference["status"] not in {"PASS","FAIL"}: fail("REFERENCE_VALIDATION_STATE_INVALID")
    if gate_mode=="REAL_RELEASE":
        if reference["mode"]!="REAL_RELEASE" or reference["fixture_class"]!="REAL" or not reference["release_evidence_eligible"]: fail("TEST_REFERENCE_USED_FOR_REAL_RELEASE")
    else:
        if reference["mode"]!="TEST_ONLY" or reference["fixture_class"]!="TEST_ONLY_SYNTHETIC" or reference["release_evidence_eligible"]: fail("TEST_REFERENCE_CUSTODY_INVALID")
    return True


def validate_learning_effectiveness(efficacy,policy):
    if efficacy is None: return "NOT_RUN",None
    required={"state","evidence_ref","evidence_class"}
    if set(efficacy)!=required or efficacy["state"] not in policy["learning_effectiveness_states"]: fail("LEARNING_EFFECTIVENESS_STATE_INVALID")
    if efficacy["state"]=="VALIDATED":
        if efficacy["evidence_class"]!=policy["learning_effectiveness_required_evidence_for_validated"] or not efficacy["evidence_ref"]:
            fail("LEARNING_EFFECTIVENESS_CLAIMED_WITHOUT_STUDY")
    return efficacy["state"],efficacy["evidence_ref"]


def evaluate(candidate,policy,machine=None,ai_pre_review=None,review_receipts=None,reference_validation=None,learning_effectiveness=None,gate_mode="REAL_RELEASE"):
    if gate_mode not in {"REAL_RELEASE","TEST_ONLY"}: fail("UNKNOWN_GATE_MODE")
    validate_policy(policy); validate_candidate(candidate)
    states={k:"NOT_RUN" for k in QUALITY_KEYS}
    blockers=[]; review_receipts=review_receipts or []
    efficacy_state,efficacy_ref=validate_learning_effectiveness(learning_effectiveness,policy)

    rendered=(candidate["candidate_class"]=="RENDERED_TWO_PRODUCT_EXACT_CANDIDATE" and candidate["materialization_state"]=="RENDERED_EXACT")
    if not rendered:
        states["PUBLICATION_ENGINEERING"]="BLOCKED"
        states["MATURE_DESIGN_QUALITY"]="BLOCKED"
        blockers.extend(candidate["upstream_blockers"] or ["M-L:RENDERED_EXACT_TWO_PRODUCT_NOT_BOUND"])
        if machine or ai_pre_review or review_receipts or reference_validation: fail("QUALITY_EVIDENCE_WITHOUT_RENDERED_EXACT_CANDIDATE")
    else:
        if gate_mode=="REAL_RELEASE" and candidate["fixture_class"]!="REAL_RUNTIME": blockers.append("M-L:REAL_RUNTIME_CANDIDATE_REQUIRED")
        if not pck_release_legal(candidate): blockers.append("M-L:PCK_EXPERT_REVIEW_PENDING")
        if machine is None:
            blockers.append("M-L:MACHINE_FALSIFIERS_NOT_RUN")
            states["MATURE_DESIGN_QUALITY"]="BLOCKED"
        else:
            validate_machine(machine,candidate)
            machine_pass=machine["machine_falsifiers"]=="PASS" and machine["publication_engineering"]=="PASS" and machine["exact_artifact_custody"]=="PASS"
            states["PUBLICATION_ENGINEERING"]="PASS" if machine_pass else "FAIL"
            if not machine_pass:
                states["MATURE_DESIGN_QUALITY"]="FAIL"
                blockers.append("M-L:PUBLICATION_ENGINEERING_OR_MACHINE_FALSIFIER_FAILED")
            elif ai_pre_review is None:
                states["MATURE_DESIGN_QUALITY"]="BLOCKED"
                blockers.append("M-L:AI_PRE_REVIEW_NOT_RUN")
            else:
                validate_ai(ai_pre_review,candidate)
                if ai_pre_review["status"]!="PASS":
                    states["MATURE_DESIGN_QUALITY"]="FAIL"
                    blockers.append("M-L:AI_PRE_REVIEW_FAILED")
                else:
                    by_dim={}
                    for receipt in review_receipts:
                        validate_review_receipt(receipt,candidate,gate_mode)
                        dim=receipt["review_dimension"]
                        if dim in by_dim: fail("DUPLICATE_HUMAN_REVIEW_DIMENSION",dim)
                        by_dim[dim]=receipt
                    for dim,gate in REVIEW_GATE.items():
                        if dim not in by_dim:
                            states[gate]="NOT_RUN"; blockers.append(f"M-L:AUTHORIZED_{dim}_REVIEW_NOT_RUN")
                        else:
                            states[gate]=by_dim[dim]["review_status"]
                            if by_dim[dim]["review_status"]!="PASS": blockers.append(f"M-L:{dim}_REVIEW_FAILED")
                    human_states=[states[x] for x in REVIEW_GATE.values()]
                    if any(x=="FAIL" for x in human_states):
                        states["MATURE_DESIGN_QUALITY"]="FAIL"
                    elif all(x=="PASS" for x in human_states):
                        states["MATURE_DESIGN_QUALITY"]="PASS"
                    else:
                        states["MATURE_DESIGN_QUALITY"]="BLOCKED"

                    if reference_validation is not None and states["MATURE_DESIGN_QUALITY"]!="PASS": fail("REFERENCE_READ_BEFORE_HUMAN_GATES")
                    if states["MATURE_DESIGN_QUALITY"]=="PASS":
                        if reference_validation is None:
                            states["REFERENCE_COMPARABILITY"]="NOT_RUN"; blockers.append("M-L:REFERENCE_COMPARISON_NOT_RUN")
                        else:
                            validate_reference(reference_validation,candidate,gate_mode)
                            states["REFERENCE_COMPARABILITY"]=reference_validation["status"]
                            if reference_validation["status"]!="PASS": blockers.append("M-L:REFERENCE_COMPARISON_FAILED")

    all_quality=(states["PUBLICATION_ENGINEERING"]=="PASS" and states["SUBJECT_CORRECTNESS"]=="PASS" and states["PEDAGOGICAL_DESIGN"]=="PASS" and states["ASSESSMENT_DESIGN"]=="PASS" and states["VISUAL_USABILITY"]=="PASS" and states["MATURE_DESIGN_QUALITY"]=="PASS" and states["REFERENCE_COMPARABILITY"]=="PASS")
    real_reviews=all(r["release_evidence_eligible"] and r["review_mode"]=="REAL_RELEASE" and r["fixture_class"]=="REAL" for r in review_receipts) and len(review_receipts)==4
    ref_real=bool(reference_validation and reference_validation["release_evidence_eligible"] and reference_validation["mode"]=="REAL_RELEASE" and reference_validation["fixture_class"]=="REAL")
    real_release=all_quality and gate_mode=="REAL_RELEASE" and candidate["fixture_class"]=="REAL_RUNTIME" and real_reviews and ref_real and pck_release_legal(candidate)
    if real_release:
        product_class=policy["mature_product_class"]; release_eligible=True
    elif all_quality and gate_mode=="TEST_ONLY":
        product_class=policy["test_only_product_class"]; release_eligible=False
    else:
        product_class="NOT_ELIGIBLE"; release_eligible=False
    if all_quality and gate_mode=="REAL_RELEASE" and not real_release: blockers.append("M-L:REAL_RELEASE_EVIDENCE_NOT_ELIGIBLE")

    decision={
      "gate_id":"",
      "schema_version":"1.0.0","subject":"MATHEMATICS","policy_ref":policy["policy_id"],
      "candidate_ref":candidate["candidate_id"],"candidate_digest":candidate["binding_digest"],"artifact_set_digest":candidate["artifact_set_digest"],
      "gate_mode":gate_mode,"quality_states":states,
      "learning_effectiveness_validation":efficacy_state,"learning_effectiveness_evidence_ref":efficacy_ref,
      "machine_evidence_ref":machine["evidence_id"] if machine else None,
      "ai_pre_review_ref":ai_pre_review["pre_review_id"] if ai_pre_review else None,
      "human_review_receipt_refs":sorted(r["receipt_id"] for r in review_receipts),
      "reference_validation_ref":reference_validation["validation_id"] if reference_validation else None,
      "reference_read_authorized":bool(reference_validation and states["MATURE_DESIGN_QUALITY"]=="PASS"),
      "mature_product_class":product_class,"release_evidence_eligible":release_eligible,
      "blockers":sorted(set(blockers)),"decision_digest":"",
    }
    decision["gate_id"]="MATH-ML-GATE-"+digest({"candidate":candidate["binding_digest"],"mode":gate_mode,"states":states,"reviews":decision["human_review_receipt_refs"],"ref":decision["reference_validation_ref"]})[:16]
    decision["decision_digest"]=digest(decision,"decision_digest")
    validate_decision(decision,candidate,review_receipts,policy)
    return decision


def validate_decision(decision,candidate,review_receipts,policy):
    check_schema("math-mature-gate-decision.schema.json",decision)
    if decision["decision_digest"]!=digest(decision,"decision_digest"): fail("MATURE_GATE_DECISION_DIGEST_MISMATCH")
    if decision["candidate_digest"]!=candidate["binding_digest"] or decision["artifact_set_digest"]!=candidate["artifact_set_digest"]: fail("MATURE_GATE_NOT_BOUND_TO_EXACT_CANDIDATE")
    dims={r["review_dimension"] for r in review_receipts}
    if decision["quality_states"]["SUBJECT_CORRECTNESS"]=="PASS" and "SUBJECT" not in dims: fail("MACHINE_GREEN_CLAIMED_AS_SUBJECT_PASS")
    if decision["quality_states"]["PEDAGOGICAL_DESIGN"]=="PASS" and "PEDAGOGY" not in dims: fail("MACHINE_GREEN_CLAIMED_AS_PEDAGOGY_PASS")
    if decision["quality_states"]["ASSESSMENT_DESIGN"]=="PASS" and "ASSESSMENT" not in dims: fail("MACHINE_GREEN_CLAIMED_AS_ASSESSMENT_PASS")
    if decision["quality_states"]["VISUAL_USABILITY"]=="PASS" and "VISUAL" not in dims: fail("MACHINE_GREEN_CLAIMED_AS_VISUAL_PASS")
    if decision["mature_product_class"]==policy["mature_product_class"]:
        if candidate["core1_authoring_status"]!="PRODUCTION_PLAN_READY": fail("CORE1_SUMMARY_LEVEL_BUT_MARKED_MATURE")
        if not pck_release_legal(candidate): fail("PROVISIONAL_PCK_MARKED_MATURE",candidate["candidate_id"])
        if not all(v=="PASS" for v in decision["quality_states"].values()): fail("MATURE_PRODUCT_WITH_INCOMPLETE_QUALITY_GATES")
        if not decision["release_evidence_eligible"] or decision["gate_mode"]!="REAL_RELEASE" or candidate["fixture_class"]!="REAL_RUNTIME": fail("MATURE_PRODUCT_WITHOUT_REAL_RELEASE_EVIDENCE")
    if decision["learning_effectiveness_validation"]=="VALIDATED" and not decision["learning_effectiveness_evidence_ref"]: fail("LEARNING_EFFECTIVENESS_CLAIMED_WITHOUT_STUDY")
    return True


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--candidate",required=True); ap.add_argument("--policy",default=str(ROOT/"registry"/"math-mature-quality-policy.json")); ap.add_argument("--out",required=True)
    ap.add_argument("--gate-mode",choices=["REAL_RELEASE","TEST_ONLY"],default="REAL_RELEASE")
    args=ap.parse_args()
    result=evaluate(load(args.candidate),load(args.policy),gate_mode=args.gate_mode)
    Path(args.out).write_text(json.dumps(result,indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding="utf-8")


if __name__=="__main__": main()
