#!/usr/bin/env python3
import copy, json, sys
from pathlib import Path
from jsonschema import Draft202012Validator, RefResolver

D=Path(__file__).resolve().parents[1]
MATH=D.parent
sys.path[:0]=[str(D/"engine"),str(MATH/"ProblemSemantics"/"engine")]
from build_math_core2_transfer import build_plan,validate_plan,digest
from build_math_problem_semantics import build_package,load_family_registry

def L(p): return json.loads(Path(p).read_text(encoding="utf-8"))
def page(plan,q): return next(x for x in plan["pages"] if x["question_ref"]==q)
def reseal_page(p): p["page_digest"]=digest(p,"page_digest")
def reseal_plan(p): p["plan_digest"]=digest(p,"plan_digest")
def expect(code,fn):
    try: fn()
    except ValueError as e:
        assert str(e).startswith(code),(code,str(e)); return
    raise AssertionError("expected "+code)

Q=L(MATH/"AssessmentIntake/fixtures/mixed-grade9-question-set.fixture.json")
S=L(MATH/"AssessmentIntake/fixtures/mixed-grade9-topic-scope.fixture.json")
RR=L(MATH/"AssessmentReview/registry/assessment-item-validity-registry.json")
RP=L(MATH/"AssessmentReview/policies/diagnostic-use-policy.json")
A=L(MATH/"AssessmentScope/authority/math-assessment-scope-authority.json")
B=L(MATH/"AssessmentScope/registry/mixed-grade9-question-scope-bindings.json")
ROLE=L(MATH/"ProblemSemantics/registry/math-reasoning-role-registry.json")
FAM=load_family_registry(MATH/"ProblemSemantics/registry/math-problem-family-registry.json")
VER=L(MATH/"ProblemSemantics/registry/math-verification-route-registry.json")
ITEM=L(MATH/"ProblemSemantics/registry/mixed-grade9-item-semantics.json")
POL=L(MATH/"ProblemSemantics/registry/guide-demand-badge-policy.json")
PS=build_package(Q,S,RR,RP,A,B,ROLE,FAM,VER,ITEM,POL)
PRIM=L(MATH/"RepresentationSemantics/registry/math-teaching-primitive-registry.json")
PINT=L(MATH/"RepresentationSemantics/policies/math-page-intent-profile.json")
PROF=L(D/"registry/math-core2-authoring-profile.json")
ARGS=(Q,RR,RP,B,A,PS,VER,PRIM,PINT,PROF,None)
PLAN=build_plan(*copy.deepcopy(ARGS))

assert [x["question_ref"] for x in PLAN["pages"]]==[f"Q{i}" for i in range(1,15)]
assert PLAN["summary"]=={"question_count":14,"attempt_first":True,"source_fidelity":True,"psychometric_claims":False,"publication_ready":False}
assert PLAN["release_class"]=="SEMANTIC_TEST" and PLAN["core1_linkage_mode"]=="PLANNED_UNTIL_PCK_PROMOTED"
assert all(not p["hint_ladder"]["support_revealed_initially"] for p in PLAN["pages"])
assert all(p["attempt_policy"]["attempt_original_first"] and p["attempt_policy"]["support_hidden_initially"] for p in PLAN["pages"])
assert len(page(PLAN,"Q5")["source_options"])==4 and page(PLAN,"Q5")["source_options"][3]["text"]=="y=(2/3)x-11/3"
assert page(PLAN,"Q6")["question_ref"]=="Q6"
assert page(PLAN,"Q9")["assessment_safety"]["validity_state"]=="UNDERDETERMINED"
assert page(PLAN,"Q9")["assessment_safety"]["negative_inference_allowed"] is False
assert page(PLAN,"Q9")["solution_route"]["final_answer"]["uniqueness_status"]=="NON_UNIQUE"
assert page(PLAN,"Q12")["solution_route"]["final_answer"]["uniqueness_status"]=="MULTIPLE"
assert set(page(PLAN,"Q12")["solution_route"]["final_answer"]["accepted_answers"])=={"(0,2sqrt(3))","(3,-sqrt(3))"}
for q in ("Q10","Q12","Q14"):
    p=page(PLAN,q)
    assert p["guide_demand_badge"]["label"]=="HARD"
    assert len(p["reasoning_route"]["steps"])>=5 and len({x["role"] for x in p["reasoning_route"]["steps"]})>=4
assert "m_AB = ____" in page(PLAN,"Q7")["workspace_spec"]["fields"]
assert "downstream equation = ____" in page(PLAN,"Q14")["workspace_spec"]["fields"]
assert all(p["core1_lesson_refs"] and all(x["learner_title"] and not x["source_question_reuse"] for x in p["core1_lesson_refs"]) for p in PLAN["pages"])
BMAP={x["item_ref"]:x for x in B["bindings"]}
assert all(set(p["representation_plan"]["required_representation_refs"])==set(BMAP[p["question_ref"]]["representation_demands"]) for p in PLAN["pages"])

store={}
for sp in (D/"contracts").glob("*.schema.json"):
    doc=L(sp); store[doc["$id"]]=doc
root=store["math-core2-transfer-plan.schema.json"]
resolver=RefResolver.from_schema(root,store=store)
Draft202012Validator(root,resolver=resolver).validate(PLAN)
for p in PLAN["pages"]:
    Draft202012Validator(store["math-transfer-question-page.schema.json"],resolver=resolver).validate(p)
    Draft202012Validator(store["math-hint-ladder.schema.json"],resolver=resolver).validate(p["hint_ladder"])
    Draft202012Validator(store["math-solution-verification.schema.json"],resolver=resolver).validate(p["solution_route"])
    for l in p["core1_lesson_refs"]:
        Draft202012Validator(store["math-core1-core2-linkage.schema.json"],resolver=resolver).validate(l)

bad=copy.deepcopy(PLAN); x=page(bad,"Q5"); x["hint_ladder"]["H2"]["text"]=x["solution_route"]["steps"][0]; reseal_page(x); reseal_plan(bad)
expect("HINT_EQUALS_SOLUTION",lambda:validate_plan(bad,*ARGS))
bad=copy.deepcopy(PLAN); x=page(bad,"Q7"); x["hint_ladder"]["H1"]["text"]=x["hint_ladder"]["H3"]["text"]; reseal_page(x); reseal_plan(bad)
expect("H1_DISCLOSES_H3",lambda:validate_plan(bad,*ARGS))
bad=copy.deepcopy(PLAN); x=page(bad,"Q8"); hs=[x["hint_ladder"][k]["text"] for k in ("H1","H2","H3")]
for i,s in enumerate(x["reasoning_route"]["steps"]): s["mathematical_transition"]=hs[i%3]
reseal_page(x); reseal_plan(bad)
expect("REASONING_ROUTE_EQUALS_HINT_COPY",lambda:validate_plan(bad,*ARGS))
bad=copy.deepcopy(PLAN); x=page(bad,"Q5"); x["source_options"]=x["source_options"][:-1]; reseal_page(x); reseal_plan(bad)
expect("SOURCE_MC_OPTIONS_MISSING",lambda:validate_plan(bad,*ARGS))
bad=copy.deepcopy(PLAN); x=page(bad,"Q14"); x["workspace_spec"]={"workspace_type":x["problem_family_ref"],"fields":["blank 1","blank 2"]}; reseal_page(x); reseal_plan(bad)
expect("GENERIC_WORKSPACE_IGNORES_RESPONSE_SHAPE",lambda:validate_plan(bad,*ARGS))
bad=copy.deepcopy(PLAN); x=page(bad,"Q10"); x["core1_lesson_refs"][0]["learner_title"]=x["core1_lesson_refs"][0]["stable_id"]; reseal_page(x); reseal_plan(bad)
expect("OPAQUE_CORE1_LINK_ONLY",lambda:validate_plan(bad,*ARGS))
bad=copy.deepcopy(PLAN); x=page(bad,"Q10"); x["reasoning_route"]["steps"]=x["reasoning_route"]["steps"][:2]; reseal_page(x); reseal_plan(bad)
expect("HARD_BADGE_WITHOUT_DEEP_REASONING_STRUCTURE",lambda:validate_plan(bad,*ARGS))
bad=copy.deepcopy(PLAN); x=page(bad,"Q12"); x["core1_lesson_refs"][0]["source_question_reuse"]=True; reseal_page(x); reseal_plan(bad)
expect("ORIGINAL_TRANSFER_LEAKED_INTO_CORE1_WORKED_EXAMPLE",lambda:validate_plan(bad,*ARGS))
bad=copy.deepcopy(PLAN); x=page(bad,"Q11"); x["solution_route"]["steps"]=[]; reseal_page(x); reseal_plan(bad)
expect("SOLUTION_IS_ANSWER_ONLY",lambda:validate_plan(bad,*ARGS))
bad=copy.deepcopy(PLAN); x=page(bad,"Q9"); x["assessment_safety"]["negative_inference_allowed"]=True; reseal_page(x); reseal_plan(bad)
expect("ASSESSMENT_SAFETY_POLICY_LOST",lambda:validate_plan(bad,*ARGS))
bad=copy.deepcopy(PLAN); x=page(bad,"Q12"); x["solution_route"]["final_answer"]["accepted_answers"]=["(0,2sqrt(3))"]; x["solution_route"]["final_answer"]["uniqueness_status"]="SINGLE"; reseal_page(x); reseal_plan(bad)
expect("MULTI_SOLUTION_COLLAPSED",lambda:validate_plan(bad,*ARGS))
bad=copy.deepcopy(PLAN); x=page(bad,"Q7"); x["representation_plan"]["required_representation_refs"]=x["representation_plan"]["required_representation_refs"][:-1]; reseal_page(x); reseal_plan(bad)
expect("REPRESENTATION_PLAN_DRIFT",lambda:validate_plan(bad,*ARGS))
bad=copy.deepcopy(PLAN); x=page(bad,"Q7"); x["source_stem"]="changed source"; reseal_page(x); reseal_plan(bad)
expect("SOURCE_SHAPE_DRIFT",lambda:validate_plan(bad,*ARGS))
bad=copy.deepcopy(PLAN); bad["pages"]=[x for x in bad["pages"] if x["question_ref"]!="Q3"]; reseal_plan(bad)
expect("MISSING_TRANSFER_QUESTION",lambda:validate_plan(bad,*ARGS))
bad=copy.deepcopy(PLAN); x=page(bad,"Q10"); x["guide_demand_badge"]["psychometric_claim"]=True; reseal_page(x); reseal_plan(bad)
expect("GUIDE_BADGE_PRESENTED_AS_PSYCHOMETRIC",lambda:validate_plan(bad,*ARGS))
bad=copy.deepcopy(PLAN); bad["release_class"]="PRODUCTION_READY"; bad["summary"]["publication_ready"]=True; reseal_plan(bad)
expect("UNPROMOTED_CORE1_LINK_PUBLISHED",lambda:validate_plan(bad,*ARGS))

AGAIN=build_plan(*copy.deepcopy(ARGS))
assert json.dumps(PLAN,sort_keys=True,separators=(",",":"),ensure_ascii=False)==json.dumps(AGAIN,sort_keys=True,separators=(",",":"),ensure_ascii=False)
print("MATH M-I transfer pages = 14/14 PASS")
print("MATH M-I H0/H1/H2/H3 separation = PASS")
print("MATH M-I source fidelity + item-safety = PASS")
print("MATH M-I Core1 planned-link fail-closed gate = PASS")
print("MATH M-I M-H representation closure = PASS")
print("MATH M-I required falsifiers = 16 PASS")
print("MATH M-I deterministic replay = PASS")
