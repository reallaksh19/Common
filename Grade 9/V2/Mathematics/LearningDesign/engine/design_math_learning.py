#!/usr/bin/env python3
import argparse, copy, hashlib, json
from pathlib import Path

FORBIDDEN_KEYS = {
    "schedule","calendar","spacing","weekly_allocation","time_allocation",
    "page","page_number","page_coordinates","typography","renderer","benchmark_reference",
    "benchmark_page_id","raw_evidence","interaction_support_state","diagnosis"
}

def canonical_bytes(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()

def digest_without_field(plan):
    x=copy.deepcopy(plan); x.pop("design_digest",None)
    return hashlib.sha256(canonical_bytes(x)).hexdigest()

def walk_keys(obj):
    if isinstance(obj, dict):
        for k,v in obj.items():
            yield k
            yield from walk_keys(v)
    elif isinstance(obj, list):
        for v in obj: yield from walk_keys(v)

def check_inputs(study, pubview, pubtarget, policy):
    if study.get("fixture_class")!="PUBLIC_SYNTHETIC" or study.get("authority")!="INTERFACE_FIXTURE_ONLY":
        raise ValueError("study interface must be PUBLIC_SYNTHETIC / INTERFACE_FIXTURE_ONLY")
    if pubview.get("fixture_class")!="PUBLIC_SYNTHETIC" or pubview.get("authority")!="INTERFACE_FIXTURE_ONLY":
        raise ValueError("publication view must be interface-only")
    if not pubview.get("static_only"):
        raise ValueError("publication planning view must be static")
    if pubtarget.get("benchmark_inputs"):
        raise ValueError("benchmark producer inputs forbidden")
    bad=FORBIDDEN_KEYS.intersection(set(walk_keys({"study":study,"pubview":pubview,"pubtarget":pubtarget})))
    if bad: raise ValueError(f"forbidden producer fields: {sorted(bad)}")
    if policy.get("fixture_class")!="PUBLIC_SYNTHETIC":
        raise ValueError("policy fixture must be PUBLIC_SYNTHETIC")

def step(step_id,target,role,learner_action,payload):
    return {"step_id":step_id,"target_id":target,"role":role,"learner_action":learner_action,"payload":payload}

def build_design(study,pubview,pubtarget,policy):
    check_inputs(study,pubview,pubtarget,policy)
    targets={t["target_id"]:t for t in study["targets"]}
    steps=[]

    steps += [
      step("S01","MATH-WORD-MODELLING","ENTRY_POINT_ANCHOR",True,{"mode":"VERIFY_STRENGTH","prompt":"Translate a short relation into equations and state what each variable means."}),
      step("S02","MATH-LINEAR-SYSTEM-SETUP","ENTRY_POINT_ANCHOR",True,{"mode":"USE_AS_ENTRY_POINT","prompt":"Use the correctly formed system as the launch point for transformation analysis."}),
      step("S03","MATH-GEOMETRIC-MODELLING","ENTRY_POINT_ANCHOR",True,{"mode":"VERIFY_STRENGTH","prompt":"State the geometric relation before any algebraic expansion."}),
      step("S04","MATH-REPRESENTATION-TRANSLATION","REPRESENTATION_TRANSLATE",True,{"source":"geometric relation","destination":"symbolic equation","translation_job":"name which geometric quantity each algebraic expression represents","invariant":"the represented quantity remains unchanged"})
    ]

    steps += [
      step("E01","MATH-EQUALITY-PRESERVATION","PREDICT_LEGALITY",True,{"prompt":"Before changing the equation, predict whether the proposed move preserves the same solution set."}),
      step("E02","MATH-EQUALITY-PRESERVATION","RECONSTRUCT",False,{"meaning":"equality states two expressions have the same value","route":["name the operation","apply it to both sides when required","simplify one transformation at a time"],"conditions":["each line must be equivalent to the previous line"],"not_formula_only":True}),
      step("E03","MATH-EQUALITY-PRESERVATION","GUIDED_ATTEMPT",True,{"support_level":3,"conceptual_hints":["Name the operation before writing the next line."],"preselected_operation":False}),
      step("E04","MATH-EQUALITY-PRESERVATION","MINIMAL_CONTRAST",False,{"controlled_shared_structure":["same equation","same target variable","same starting expression"],"focal_distinction":"operation applied legally to both sides vs term deleted from one side","prediction_before_resolution":True,"discrimination_target":"which next line preserves equivalence"}),
      step("E05","MATH-EQUALITY-PRESERVATION","GUIDED_ATTEMPT",True,{"support_level":2,"conceptual_hints":["Choose which of the two next lines is equivalent and justify."],"preselected_operation":False}),
      step("E06","MATH-EQUALITY-PRESERVATION","WORKED_REASONING",False,{"problem":"2x + 7 = 19","one_legal_operation_per_line":True,"lines":[{"from":"2x + 7 = 19","operation":"subtract 7 from both sides","to":"2x = 12"},{"from":"2x = 12","operation":"divide both sides by 2","to":"x = 6"}],"self_check":"substitute x=6 into the original equation: 12+7=19"}),
      step("E07","MATH-EQUALITY-PRESERVATION","GUIDED_ATTEMPT",True,{"support_level":2,"conceptual_hints":["State the operation; write one equivalent line."],"preselected_operation":False}),
      step("E08","MATH-EQUALITY-PRESERVATION","FADED_ATTEMPT",True,{"support_level":1,"conceptual_hints":["Check that your next line is equivalent."],"preselected_operation":False,"partially_completed_algebra":False}),
      step("E09","MATH-EQUALITY-PRESERVATION","INDEPENDENT_ATTEMPT",True,{"support_level":0,"conceptual_hints":[],"preselected_operation":False,"partially_completed_algebra":False}),
      step("E10","MATH-EQUALITY-PRESERVATION","VERIFY",True,{"methods":["substitution","equivalence check"],"embedded_after_attempt":"E09","prompt":"Verify against the original relation, not only your final line."}),
      step("E11","MATH-EQUALITY-PRESERVATION","TRANSFER",True,{"structural_changes":["variable appears on both sides","task asks to identify an illegal transformation rather than solve"],"number_only":False,"prompt":"Find the first non-equivalent line in a different-form equation and repair it."}),
      step("E12","MATH-EQUALITY-PRESERVATION","COMPLETION_EVIDENCE",True,{"observable":"independently chooses legal transformations one line at a time and verifies against the original relation","prompted":False})
    ]

    steps += [
      step("B01","MATH-BINOMIAL-SQUARE-EXPANSION","RECONSTRUCT",False,{"meaning":"(a-b)^2=(a-b)(a-b), not a^2-b^2","route":["write repeated product","distribute all terms","combine like terms"],"not_formula_only":True}),
      step("B02","MATH-BINOMIAL-SQUARE-EXPANSION","GUIDED_ATTEMPT",True,{"support_level":3,"conceptual_hints":["Write the square as a repeated product first."],"preselected_operation":True}),
      step("B03","MATH-BINOMIAL-SQUARE-EXPANSION","MINIMAL_CONTRAST",False,{"controlled_shared_structure":["same binomial","same square operation"],"focal_distinction":"middle product terms retained vs omitted","prediction_before_resolution":True,"discrimination_target":"which expansion preserves the repeated-product structure"}),
      step("B04","MATH-BINOMIAL-SQUARE-EXPANSION","GUIDED_ATTEMPT",True,{"support_level":2,"conceptual_hints":["Track all four products."],"preselected_operation":False}),
      step("B05","MATH-BINOMIAL-SQUARE-EXPANSION","FADED_ATTEMPT",True,{"support_level":1,"conceptual_hints":["Check the middle term."],"preselected_operation":False,"partially_completed_algebra":False}),
      step("B06","MATH-BINOMIAL-SQUARE-EXPANSION","INDEPENDENT_ATTEMPT",True,{"support_level":0,"conceptual_hints":[],"preselected_operation":False,"partially_completed_algebra":False}),
      step("B07","MATH-BINOMIAL-SQUARE-EXPANSION","TRANSFER",True,{"structural_changes":["symbolic parameters instead of numbers","expression embedded inside a geometry-derived equation"],"number_only":False})
    ]

    probe=targets["MATH-ORDERED-PAIR-SEMANTICS"].get("required_probe_ref")
    steps += [step("P01","MATH-ORDERED-PAIR-SEMANTICS","DIAGNOSTIC_PROBE",True,{"probe_ref":probe,"controlled_load":"LOW","purpose":"distinguish ordered-pair role confusion from execution slip"})]
    steps += [
      step("V01","MATH-SOLUTION-VERIFICATION","VERIFY",True,{"methods":["substitution","equivalence","domain/constraint check"],"embedded_refs":["E06","E09","E10"],"prompt":"Choose an appropriate check without being told which method to use."}),
      step("V02","MATH-SOLUTION-VERIFICATION","COMPLETION_EVIDENCE",True,{"observable":"initiates an appropriate mathematical check without a verification prompt","prompted":False})
    ]

    obligations=[o for t in study["targets"] for o in t["study_obligations"]]
    coverage_map={
      "OBL-MODELLING-VERIFY":["S01"],"OBL-SYSTEM-ENTRY":["S02"],"OBL-GEOM-VERIFY":["S03"],"OBL-REP-ENTRY":["S04"],
      "OBL-EQ-RECONSTRUCT":["E02","E03"],"OBL-EQ-CONTRAST":["E04","E05"],"OBL-EQ-WORKED":["E06","E07"],"OBL-EQ-FADE":["E08","E09"],
      "OBL-EQ-VERIFY":["E06","E10"],"OBL-EQ-TRANSFER":["E11"],"OBL-EQ-COMPLETE":["E12"],
      "OBL-BINOMIAL-RECONSTRUCT":["B01","B02"],"OBL-BINOMIAL-CONTRAST":["B03","B04"],"OBL-BINOMIAL-FADE":["B05","B06"],"OBL-BINOMIAL-TRANSFER":["B07"],
      "OBL-SLOPE-PROBE":["P01"],"OBL-VERIFY-INDEPENDENT-INITIATION":["V01","V02"]
    }
    missing=[o for o in obligations if o not in coverage_map]
    if missing:
        return {"status":"GAP","gap_code":"LEARNING_DESIGN_GAP","missing_obligations":sorted(missing)}
    target_pres=[{"target_id":t["target_id"],"engagement_mode":t["engagement_mode"],"readiness_mode":t["readiness_mode"]} for t in study["targets"]]
    plan={"learning_design_id":"MATH-LD-SYN-001","schema_version":"1.0.0","study_model_ref":study["study_model_id"],"policy_ref":policy["policy_id"],
          "target_preservation":target_pres,
          "obligation_coverage":[{"obligation_id":o,"step_ids":coverage_map[o]} for o in obligations],
          "steps":steps,"support_ladder":copy.deepcopy(policy["support_rungs"])}
    plan["design_digest"]=digest_without_field(plan)
    return {"status":"READY","learning_design_plan":plan}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--study-model",required=True); ap.add_argument("--publication-view",required=True)
    ap.add_argument("--publication-target",required=True); ap.add_argument("--policy",required=True); ap.add_argument("--out")
    a=ap.parse_args()
    load=lambda p: json.loads(Path(p).read_text())
    result=build_design(load(a.study_model),load(a.publication_view),load(a.publication_target),load(a.policy))
    out=json.dumps(result,sort_keys=True,indent=2)
    if a.out: Path(a.out).write_text(out+"\n")
    else: print(out)
if __name__=="__main__": main()
