from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve(); ROOT = HERE.parents[1]; ENGINE = ROOT / "engine"
if str(ENGINE) not in sys.path: sys.path.insert(0, str(ENGINE))

from compile_mathematics_engineering_workbench import compile_binding, compile_closure, load as load_engineering, resolve_manifest
from emit_stage_governance import artifact, build_receipt
from engineering_product_custody import build_custody, stamp_receipt
from release_product_governance import release

REGISTRY = ROOT / "golden" / "domain_registry" / "01-theory-of-equations-registry.json"
TECH_REGISTRY = load_engineering("policies/mathematics-technical-engineering-gates.v1.json")
THEORY_EQ_GATE = "MATH-ALG-POLY-ZEROS-GRAPH"
THEORY_EQ_AUTH = "MATH-ENG-AUTH-THEORY-EQ-GOLDEN"

SEMANTIC = {
    "CONCEPT", "MODEL", "EQUATION", "DERIVATION", "CAPABILITY",
    "LEARNING_ATOM", "REPRESENTATION", "MISCONCEPTION",
}


def load(path): return json.loads(Path(path).read_text(encoding="utf-8"))


def engineering_release_fixture(reg: dict):
    """Explicit test-only Engineering admission for the synthetic Vieta registry.

    This is not topic inference. The fixture names the exact Engineering gate whose
    authoritative technical core contains Vieta's coefficient/root relations and
    binds the synthetic THEORY-OF-EQUATIONS subtopic to that direct gate ID.
    """
    request = {
        "schema_version": "1.0.0",
        "subject": "MATHEMATICS",
        "request_id": "MATH-ENG-REQ-THEORY-EQ-GOLDEN",
        "scope_kind": "ENGINEERING_GATE",
        "scope_refs": [THEORY_EQ_GATE],
        "engineering_depth": "STANDARD",
        "learning_purpose": "FIRST_STUDY",
        "owner_decision_ref": None,
    }
    manifest = resolve_manifest(request, TECH_REGISTRY)
    closure = compile_closure(request, manifest, TECH_REGISTRY)
    binding = compile_binding(request, manifest, closure, "CANONICAL_DOMAIN_REGISTRY")
    injected = {THEORY_EQ_AUTH: {"request": request, "manifest": manifest, "binding": binding}}
    admission = {
        "schema_version": "2.0.0",
        "subject": "MATHEMATICS",
        "admission_id": "MATH-ENG-DOMAIN-ADMISSION-THEORY-EQ-GOLDEN",
        "domain_registry_ref": "runtime://theory-equations-registry",
        "authorizations": [{
            "authorization_id": THEORY_EQ_AUTH,
            "engineering_request_ref": "runtime://theory-eq/request",
            "engineering_manifest_ref": "runtime://theory-eq/manifest",
            "engineering_binding_ref": "runtime://theory-eq/binding",
        }],
        "subtopic_gate_map": [{
            "subtopic_id": "THEORY-OF-EQUATIONS",
            "gate_bindings": [{
                "engineering_gate_id": THEORY_EQ_GATE,
                "authorization_ref": THEORY_EQ_AUTH,
            }],
        }],
    }
    custody = build_custody(
        admission,
        reg,
        engineering_authorizations=injected,
        technical_registry=TECH_REGISTRY,
    )
    return admission, injected, custody


def hard_difficulty():
    dims = {k:3 for k in ["prerequisite_depth","element_interactivity","inferential_jump_severity","representation_translation","abstraction","method_discrimination","notation_density","derivation_burden","misconception_density","special_case_sensitivity"]}
    return {"subtopic_ref":"THEORY-OF-EQUATIONS","declared_badge":"HARD","badge_authority":"DERIVED","derived_dimensions":dims,"operational_badge":"HARD","page_ceiling":30,"research_level":"DEEP","owner_override_ref":None,"evidence_refs":["DIFF:THEORY-EQ","RESEARCH:THEORY-EQ"]}


def purpose(stage):
    return {
        "CORE1A":{"purpose_contract":"BUILD_UNDERSTANDING","learner_actions":["READ","INTERPRET","VERIFY"],"canonical_reveal_after_attempt":False,"evidence_refs":["P:C1A"]},
        "CORE1B":{"purpose_contract":"RECONSTRUCT_CONCEPT","learner_actions":["PREDICT","GENERATE","DERIVE","VERIFY"],"canonical_reveal_after_attempt":True,"evidence_refs":["P:C1B"]},
        "CORE2A":{"purpose_contract":"SOLUTION_APPRENTICESHIP","learner_actions":["STUDY_SOLUTION","ANALYZE_FIRST_MOVE","VERIFY"],"canonical_reveal_after_attempt":False,"evidence_refs":["P:C2A"]},
        "CORE2B":{"purpose_contract":"TRANSFER_TUTOR","learner_actions":["ATTEMPT","MODEL_SELECT","FIRST_MOVE","SOLVE","VERIFY","TRANSFER"],"canonical_reveal_after_attempt":True,"evidence_refs":["P:C2B"]},
    }[stage]


def calibration():
    return {"type":"KNOWLEDGE_PERCENT","learner_knowledge_percent":75,"knowledge_source_ref":"ASSESSMENT:1","calibration_policy_ref":"POLICY:1","capability_knowledge":[{"capability_ref":"REG-MATH-CAP-COEFF_ROOT","percent":75}]}


def make_receipts(reg, custody):
    semantic = [x for x in reg["assets"] if x["asset_type"] in SEMANTIC]
    c1a_claims=[{"local_ref":x["asset_id"],"local_type":x["asset_type"],"canonical_asset_refs":[x["asset_id"]],"disposition":"REALIZED","realization_refs":["A:"+x["asset_id"]]} for x in semantic]
    c1b_claims=[{"local_ref":x["asset_id"],"local_type":x["asset_type"],"canonical_asset_refs":[x["asset_id"]],"disposition":"RECONSTRUCTED","realization_refs":["B:"+x["asset_id"]]} for x in semantic]
    c2a_claims=[
        {"local_ref":"REG-MATH-Q-Q2","local_type":"SOURCE_QUESTION","canonical_asset_refs":["REG-MATH-Q-Q2"],"disposition":"USED","realization_refs":["Q2"]},
        {"local_ref":"REG-MATH-CAP-COEFF_ROOT","local_type":"CAPABILITY","canonical_asset_refs":["REG-MATH-CAP-COEFF_ROOT"],"disposition":"USED","realization_refs":["Q2"]},
    ]
    c2b_claims=[{"local_ref":"REG-MATH-CAP-COEFF_ROOT","local_type":"CAPABILITY","canonical_asset_refs":["REG-MATH-CAP-COEFF_ROOT"],"disposition":"USED","realization_refs":["B-Q2"]}]
    frozen=next(x for x in reg["assets"] if x["asset_id"]=="REG-MATH-Q-Q2")["payload"]["frozen_digest"]
    q2={"question_id":"Q2","origin":"SOURCE_CORE2","source_question_no":"Q2","source_ref":"SRC-Q2","source_relation":"EXACT_SOURCE","parent_question_refs":[],"exact_stem_hash":frozen,"answer_contract_ref":"ANS-Q2-v1","answer_status":"VERIFIED","learner_source_label":"Core (2) Q2","official_past_question_claim":False,"verified_official_source_ref":None}
    bq={"question_id":"B-Q2","origin":"GENERATED_ORIGINAL","source_question_no":None,"source_ref":"GENERATED:B-Q2","source_relation":"STRUCTURAL_SIBLING","parent_question_refs":["Q2"],"exact_stem_hash":None,"answer_contract_ref":"ANS-BQ2","answer_status":"VERIFIED","learner_source_label":"Generated transfer from Q2","official_past_question_claim":False,"verified_official_source_ref":None}
    a1=artifact("A-TTU","TTU","Explain coefficients, root sum and product with signs.",["READ","EXPLAIN"],capability_refs=["REG-MATH-CAP-COEFF_ROOT"],canonical_asset_refs=["REG-MATH-CON-VIETA"],structural_signature=["EXPLAIN"],lineage_keys=["VIETA"])
    b1=artifact("B-TTU","TTU","Predict which coefficient controls each symmetric root quantity.",["PREDICT","RECONSTRUCT"],capability_refs=["REG-MATH-CAP-COEFF_ROOT"],canonical_asset_refs=["REG-MATH-CON-VIETA"],structural_signature=["RECONSTRUCT"],lineage_keys=["VIETA"])
    a2=artifact("Q2","QUESTION","Use the coefficient relation to solve the source question.",["STUDY_SOLUTION","VERIFY"],capability_refs=["REG-MATH-CAP-COEFF_ROOT"],canonical_asset_refs=["REG-MATH-Q-Q2"],structural_signature=["SOURCE","M1"],lineage_keys=["Q2"])
    b2=artifact("B-Q2","QUESTION","Choose the needed relation in a changed coefficient-root problem.",["ATTEMPT","TRANSFER"],capability_refs=["REG-MATH-CAP-COEFF_ROOT"],canonical_asset_refs=["REG-MATH-CAP-COEFF_ROOT"],structural_signature=["TRANSFER","M2"],lineage_keys=["Q2"])
    diff=[hard_difficulty()]
    r1=build_receipt(stage="CORE1A",producer_ref="PROD-C1A",source_refs=["SRC-A"],purpose_evidence=purpose("CORE1A"),coverage_claims=c1a_claims,artifacts=[a1],registry=reg,difficulty_evidence=diff)
    r2=build_receipt(stage="CORE1B",producer_ref="PROD-C1B",source_refs=["SRC-B"],purpose_evidence=purpose("CORE1B"),coverage_claims=c1b_claims,artifacts=[b1],registry=reg,difficulty_evidence=copy.deepcopy(diff))
    fit_a={"item_ref":"Q2","calibration_basis":calibration(),"required_capability_refs":["REG-MATH-CAP-COEFF_ROOT"],"support_mode":"GUIDED","maximum_allowed_demand":"M3_INVERSE_TARGET","actual_demand":"M1_CONTROLLED_VARIATION","taught_scope_verified":True}
    fit_b={"item_ref":"B-Q2","calibration_basis":calibration(),"required_capability_refs":["REG-MATH-CAP-COEFF_ROOT"],"support_mode":"STANDARD","maximum_allowed_demand":"M4_HIDDEN_STRUCTURE","actual_demand":"M2_REPRESENTATION_TRANSFER","taught_scope_verified":True}
    r3=build_receipt(stage="CORE2A",producer_ref="PROD-C2A",source_refs=["SRC-C"],purpose_evidence=purpose("CORE2A"),coverage_claims=c2a_claims,artifacts=[a2],registry=reg,learner_fit_evidence=[fit_a],question_custody=[q2])
    r4=build_receipt(stage="CORE2B",producer_ref="PROD-C2B",source_refs=["SRC-D"],purpose_evidence=purpose("CORE2B"),coverage_claims=c2b_claims,artifacts=[b2],registry=reg,learner_fit_evidence=[fit_b],question_custody=[bq])
    return [stamp_receipt(r, custody) for r in (r1, r2, r3, r4)]


def governed_fixture():
    reg = load(REGISTRY)
    admission, injected, custody = engineering_release_fixture(reg)
    return reg, admission, injected, custody, make_receipts(reg, custody)


def run_release(reg, receipts, admission, injected):
    return release(
        reg,
        receipts,
        admission,
        engineering_authorizations=injected,
        technical_registry=TECH_REGISTRY,
    )


class StageReceiptReleaseTests(unittest.TestCase):
    def test_four_producer_receipts_release(self):
        reg, admission, injected, _, receipts=governed_fixture()
        coverage, similarity, governance, result=run_release(reg,receipts,admission,injected)
        self.assertEqual(result["status"],"PASS")
        self.assertEqual(result["engineering_domain_authorization"]["status"],"BOUND")
        self.assertEqual(result["frozen_source_custody"]["status"],"PASS")
        self.assertEqual(result["canonical_answer_custody"]["status"],"PASS")
        self.assertEqual(coverage["coverage_scope"],"FULL_REGISTRY")
        self.assertEqual(set(similarity["coverage_declaration"]["stage_pairs"]),set(["CORE1A__CORE1B","CORE1A__CORE2A","CORE1A__CORE2B","CORE1B__CORE2A","CORE1B__CORE2B","CORE2A__CORE2B"]))
        self.assertEqual(len(governance["purpose_audits"]),4)

    def test_release_requires_current_engineering_admission(self):
        reg, _, _, _, receipts=governed_fixture()
        with self.assertRaisesRegex(ValueError,"RELEASE_ENGINEERING_ADMISSION_REQUIRED"):
            release(reg,receipts)

    def test_stale_engineering_custody_fails(self):
        reg, admission, injected, _, receipts=governed_fixture()
        receipts[0]["engineering_custody"]["custody_digest"] = "sha256:" + "0" * 64
        with self.assertRaisesRegex(ValueError,"RELEASE_ENGINEERING_CUSTODY_STALE_OR_DRIFT"):
            run_release(reg,receipts,admission,injected)

    def test_missing_semantic_asset_from_core1b_fails(self):
        reg, admission, injected, _, receipts=governed_fixture(); target="REG-MATH-EQ-VIETA_SUM"
        receipts[1]["coverage_claims"]=[x for x in receipts[1]["coverage_claims"] if target not in x["canonical_asset_refs"]]
        with self.assertRaisesRegex(ValueError,"ASSEMBLER_REQUIRED_ASSET_MISSING"): run_release(reg,receipts,admission,injected)

    def test_unbound_stage_cannot_release(self):
        reg, admission, injected, _, receipts=governed_fixture(); receipts[0]["registry_binding"]={"status":"UNBOUND","registry_ref":None,"matched_asset_refs":[]}; receipts[0]["release_state"]="UNBOUND_PRE_RELEASE"
        with self.assertRaisesRegex(ValueError,"ASSEMBLER_RECEIPT_REGISTRY_UNBOUND"): run_release(reg,receipts,admission,injected)

    def test_core1a_core1b_difficulty_drift_fails(self):
        reg, admission, injected, _, receipts=governed_fixture(); receipts[1]["difficulty_evidence"][0]["operational_badge"]="MEDIUM"
        with self.assertRaisesRegex(ValueError,"ASSEMBLER_CORE1A_CORE1B_DIFFICULTY_DRIFT"): run_release(reg,receipts,admission,injected)

    def test_frozen_source_digest_mismatch_fails(self):
        reg, admission, injected, _, receipts=governed_fixture(); receipts[2]["question_custody"][0]["exact_stem_hash"]="0"*64
        with self.assertRaisesRegex(ValueError,"RELEASE_FROZEN_SOURCE_DIGEST_MISMATCH"): run_release(reg,receipts,admission,injected)

    def test_canonical_answer_contract_mismatch_fails(self):
        reg, admission, injected, _, receipts=governed_fixture(); receipts[2]["question_custody"][0]["answer_contract_ref"]="ANS-Q2-SWAPPED"
        with self.assertRaisesRegex(ValueError,"RELEASE_CANONICAL_ANSWER_CONTRACT_MISMATCH"): run_release(reg,receipts,admission,injected)

    def test_learner_fit_over_ceiling_fails(self):
        reg, admission, injected, _, receipts=governed_fixture(); receipts[3]["learner_fit_evidence"][0]["actual_demand"]="M8_MIXED_COMPETITIVE"
        with self.assertRaisesRegex(ValueError,"LEARNER_FIT_DEMAND_CEILING_EXCEEDED"): run_release(reg,receipts,admission,injected)

if __name__=="__main__": unittest.main(verbosity=2)
