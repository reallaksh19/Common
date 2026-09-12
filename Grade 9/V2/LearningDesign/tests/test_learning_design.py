#!/usr/bin/env python3
import copy, json, sys
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
sys.path.insert(0,str(ROOT/"engine"))
sys.path.insert(0,str(ROOT/"runtime"))
from design_learning import build_design, validate_design_semantics, canonical_bytes
from select_support import select_support, validate_selection, digest

def load(name):
    return json.loads((ROOT/"fixtures"/name).read_text())

study=load("learner_study_model.synthetic.json")
view=load("publication_planning_view.synthetic.json")
target=load("publication_target.synthetic.json")
policy=load("learning_design_policy.synthetic.json")
state=load("interaction_support_state.synthetic.json")

def ready():
    r=build_design(study,view,target,policy)
    assert r["status"]=="READY",r
    return r["learning_design_plan"]

passes=0
def check(fn):
    global passes
    fn(); passes+=1

def expect_error(fn, contains=None):
    try: fn()
    except Exception as e:
        if contains: assert contains.lower() in str(e).lower(), (contains,str(e))
        return
    raise AssertionError("expected failure")

def assert_eq(a,b): assert a==b
check(lambda: assert_eq(canonical_bytes(build_design(study,view,target,policy)),canonical_bytes(build_design(study,view,target,policy))))

def t_coverage():
    p=ready()
    obs={o["obligation_id"] for t in study["targets"] for o in t["obligations"]}
    cov={c["obligation_id"] for c in p["obligation_coverage"]}
    assert obs==cov
check(t_coverage)

def t_preserve():
    p=ready(); src={t["target_id"]:(t["study_treatment"],t["readiness"]) for t in study["targets"]}
    for u in p["units"]: assert (u["study_treatment"],u["readiness"])==src[u["target_ref"]]
check(t_preserve)

def t_probe_first():
    p=ready(); u=next(u for u in p["units"] if u["target_ref"]=="MATH-SLOPE-SEMANTICS")
    assert u["choreography"][0]["role"]=="DIAGNOSTIC_PROBE"
check(t_probe_first)

def t_drop_obligation():
    p=ready(); p["obligation_coverage"]=p["obligation_coverage"][1:]
    expect_error(lambda: validate_design_semantics(p,study,policy),"coverage")
check(t_drop_obligation)

def t_reclassify():
    p=ready(); p["units"][0]["readiness"]="REPAIR_BEFORE"
    expect_error(lambda: validate_design_semantics(p,study,policy),"reclassified")
check(t_reclassify)

def t_probe_reteach_shortcut():
    p=ready(); u=next(u for u in p["units"] if u["target_ref"]=="MATH-SLOPE-SEMANTICS")
    bad=copy.deepcopy(u["choreography"][0]); bad["step_id"]="BAD"; bad["role"]="RECONSTRUCT"; bad["learner_action"]=False
    u["choreography"].insert(0,bad)
    expect_error(lambda: validate_design_semantics(p,study,policy),"diagnostic probe")
check(t_probe_reteach_shortcut)

def find_role(p,role):
    for u in p["units"]:
        for s in u["choreography"]:
            if s["role"]==role: return s
    raise AssertionError(role)

def t_worked_answer_only():
    p=ready(); s=find_role(p,"WORKED_REASONING"); s["payload"]["reasoning_moves"]=[]; s["payload"]["answer_only"]=True
    expect_error(lambda: validate_design_semantics(p,study,policy),"worked reasoning")
check(t_worked_answer_only)

def t_naked_formula():
    p=ready(); s=find_role(p,"RECONSTRUCT"); s["payload"]["term_origins"]=[]
    expect_error(lambda: validate_design_semantics(p,study,policy),"naked formula")
check(t_naked_formula)

def t_uncontrolled_contrast():
    p=ready(); s=find_role(p,"MINIMAL_CONTRAST"); s["payload"]["controlled_shared_features"]=[]
    expect_error(lambda: validate_design_semantics(p,study,policy),"contrast")
check(t_uncontrolled_contrast)

def t_fake_fading():
    p=ready(); u=next(u for u in p["units"] if u["target_ref"]=="MATH-EQUALITY-EXECUTION")
    u["support_progression"]["faded"]["support_features"]=copy.deepcopy(u["support_progression"]["guided"]["support_features"])
    expect_error(lambda: validate_design_semantics(p,study,policy),"fading")
check(t_fake_fading)

def t_independent_hints():
    p=ready(); s=find_role(p,"INDEPENDENT_ATTEMPT"); s["payload"]["support_features"]=["FIRST_STEP_CUE"]
    expect_error(lambda: validate_design_semantics(p,study,policy),"independent")
check(t_independent_hints)

def t_number_only_transfer():
    p=ready(); s=find_role(p,"TRANSFER"); s["payload"]["changed_dimensions"]=["NUMBER_CHANGE"]
    expect_error(lambda: validate_design_semantics(p,study,policy),"number-only")
check(t_number_only_transfer)

def t_rep_translation_payload():
    p=ready(); s=find_role(p,"REPRESENTATION_TRANSLATE"); s["payload"]["translation_job"]=""
    expect_error(lambda: validate_design_semantics(p,study,policy),"translation")
check(t_rep_translation_payload)

def t_teaching_without_action():
    p=ready(); u=next(u for u in p["units"] if u["target_ref"]=="MATH-EQUALITY-EXECUTION")
    steps=u["choreography"]
    wi=next(i for i,s in enumerate(steps) if s["role"]=="WORKED_REASONING")
    for s in steps[wi+1:]:
        if s["role"] in {"RECONSTRUCT","WORKED_REASONING","MINIMAL_CONTRAST","MISCONCEPTION_REPAIR"}: break
        s["learner_action"]=False
    expect_error(lambda: validate_design_semantics(p,study,policy),"learner action")
check(t_teaching_without_action)

def t_live_state_rejected():
    r=build_design(study,view,target,policy,interaction_support_state=state)
    assert r["status"]=="BLOCKED" and "forbidden producer input" in r["gaps"][0]["reason"]
check(t_live_state_rejected)

def t_benchmark_rejected():
    r=build_design(study,view,target,policy,benchmark_ref="PR156")
    assert r["status"]=="BLOCKED"
check(t_benchmark_rejected)

def t_layout_scheduling_rejected():
    p=ready(); p["page_layout"]="two-column"
    expect_error(lambda: validate_design_semantics(p,study,policy),"forbidden design")
    p=ready(); p["weekly_minutes"]=90
    expect_error(lambda: validate_design_semantics(p,study,policy),"forbidden design")
check(t_layout_scheduling_rejected)

def t_runtime_route_change():
    p=ready(); sel=select_support(p,state); validate_selection(p,sel)
    assert sel["rung_id"]=="H3" and sel["route_mode"]=="ROUTE_CHANGE"
check(t_runtime_route_change)

def t_access_is_separate():
    p=ready(); st=copy.deepcopy(state); st["access_request"]=True; st["rungs_used"]=[]
    sel=select_support(p,st); validate_selection(p,sel)
    assert sel["rung_id"]=="A1" and sel["support_class"]=="ACCESS"
    assert "FIRST_STEP_CUE" not in sel["support_features"]
check(t_access_is_separate)

def t_runtime_no_rewrite():
    p=ready(); before=copy.deepcopy(p); sel=select_support(p,state); validate_selection(p,sel)
    assert p==before and sel["frozen_design_digest"]==digest(p)
check(t_runtime_no_rewrite)

def t_unapproved_rung():
    p=ready(); st=copy.deepcopy(state); st["rungs_used"]=["H999"]
    expect_error(lambda: select_support(p,st),"unapproved")
check(t_unapproved_rung)

def t_runtime_deterministic():
    p=ready(); a=select_support(p,state); b=select_support(p,state); assert a==b
check(t_runtime_deterministic)

def t_choreography_order():
    p=ready(); u=next(u for u in p["units"] if u["target_ref"]=="MATH-EQUALITY-EXECUTION")
    roles=[s["role"] for s in u["choreography"]]
    assert roles.index("RECONSTRUCT") < roles.index("WORKED_REASONING")
    assert roles.index("MINIMAL_CONTRAST") < roles.index("WORKED_REASONING")
    assert roles.index("INDEPENDENT_ATTEMPT") < roles.index("TRANSFER")
check(t_choreography_order)

def t_verification_integrated():
    p=ready(); u=next(u for u in p["units"] if u["target_ref"]=="MATH-EQUALITY-EXECUTION")
    family=[s for s in u["choreography"] if s["role"] in {"WORKED_REASONING","GUIDED_ATTEMPT","FADED_ATTEMPT","INDEPENDENT_ATTEMPT"}]
    assert any("OB-EQ-VERIFY" in s["obligation_refs"] and s["payload"].get("verification_embedded") for s in family)
check(t_verification_integrated)

def t_contaminated_publication_view():
    bad=copy.deepcopy(view); bad["teaching_sequence"]=["do x"]
    r=build_design(study,bad,target,policy); assert r["status"]=="BLOCKED"
check(t_contaminated_publication_view)

def t_unsupported_obligation_gap():
    bad=copy.deepcopy(study)
    bad["targets"][1]["obligations"][0]["kind"]="SPACING"
    r=build_design(bad,view,target,policy)
    assert r["status"]=="BLOCKED" and r["gaps"][0]["gap_type"]=="LEARNING_DESIGN_GAP"
check(t_unsupported_obligation_gap)

print(f"V2-05 Learning Design falsifiers: {passes} PASS")
