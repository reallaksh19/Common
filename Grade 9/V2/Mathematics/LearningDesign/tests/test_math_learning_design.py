#!/usr/bin/env python3
import copy, json, sys
from pathlib import Path
D=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(D/"engine")); sys.path.insert(0,str(D/"runtime"))
from design_math_learning import build_design, digest_without_field
from select_math_support import select_support
load=lambda n: json.loads((D/"fixtures"/n).read_text())
study=load("learner_study_model.synthetic.json"); pv=load("publication_planning_view.synthetic.json"); pt=load("publication_target.synthetic.json"); pol=load("policy.synthetic.json")
r=build_design(study,pv,pt,pol); assert r["status"]=="READY"; p=r["learning_design_plan"]
steps={s["step_id"]:s for s in p["steps"]}
by_target={}
for s in p["steps"]: by_target.setdefault(s["target_id"],[]).append(s)

obs={o for t in study["targets"] for o in t["study_obligations"]}
assert obs=={x["obligation_id"] for x in p["obligation_coverage"]}
expected={t["target_id"]:(t["engagement_mode"],t["readiness_mode"]) for t in study["targets"]}
actual={t["target_id"]:(t["engagement_mode"],t["readiness_mode"]) for t in p["target_preservation"]}
assert expected==actual
assert steps["S02"]["role"]=="ENTRY_POINT_ANCHOR" and steps["S02"]["payload"]["mode"]=="USE_AS_ENTRY_POINT"
slope=by_target["MATH-ORDERED-PAIR-SEMANTICS"]; assert slope[0]["role"]=="DIAGNOSTIC_PROBE"
assert slope[0]["payload"]["probe_ref"]=="MATH-PROBE-ORDERED-PAIR-SLOPE"
wrk=steps["E06"]["payload"]; assert wrk["one_legal_operation_per_line"] and len(wrk["lines"])>=2
assert all("operation" in x and "from" in x and "to" in x for x in wrk["lines"])
assert "self_check" in wrk
assert steps["E02"]["payload"]["meaning"] and len(steps["E02"]["payload"]["route"])>=2 and steps["E02"]["payload"]["not_formula_only"]
mc=steps["E04"]["payload"]; assert len(mc["controlled_shared_structure"])>=2 and mc["focal_distinction"]
assert mc["prediction_before_resolution"] and mc["discrimination_target"]
assert steps["E07"]["payload"]["support_level"]>steps["E08"]["payload"]["support_level"]>steps["E09"]["payload"]["support_level"]
ind=steps["E09"]["payload"]; assert ind["conceptual_hints"]==[] and not ind["preselected_operation"] and not ind["partially_completed_algebra"]
tr=steps["E11"]["payload"]; assert not tr["number_only"] and len(tr["structural_changes"])>=1
assert "E06" in steps["V01"]["payload"]["embedded_refs"] and "E09" in steps["V01"]["payload"]["embedded_refs"]
rp=steps["S04"]["payload"]; assert rp["source"] and rp["destination"] and rp["translation_job"] and rp["invariant"]
teach={"RECONSTRUCT","MINIMAL_CONTRAST","WORKED_REASONING"}; seq=p["steps"]
for i,s in enumerate(seq[:-1]):
    if s["role"] in teach:
        assert any(n["learner_action"] for n in seq[i+1:min(i+3,len(seq))]), (s["step_id"],"no near learner action")
bad=copy.deepcopy(pv); bad["interaction_support_state"]={"x":1}
try: build_design(study,bad,pt,pol); raise AssertionError("live state accepted")
except ValueError: pass
bad=copy.deepcopy(pt); bad["benchmark_inputs"]=["PR156"]
try: build_design(study,pv,bad,pol); raise AssertionError("benchmark accepted")
except ValueError: pass
bad=copy.deepcopy(study); bad["targets"][0]["study_obligations"].append("OBL-UNSUPPORTED")
g=build_design(bad,pv,pt,pol); assert g["status"]=="GAP" and "OBL-UNSUPPORTED" in g["missing_obligations"]
bad=copy.deepcopy(study); bad["authority"]="CANONICAL_AUTHORITY"
try: build_design(bad,pv,pt,pol); raise AssertionError("authority drift accepted")
except ValueError: pass
r2=build_design(copy.deepcopy(study),copy.deepcopy(pv),copy.deepcopy(pt),copy.deepcopy(pol))
assert json.dumps(r,sort_keys=True,separators=(",",":"))==json.dumps(r2,sort_keys=True,separators=(",",":"))
assert p["design_digest"]==digest_without_field(p)
state=load("interaction_support_state.synthetic.json"); sel=select_support(p,state)
assert sel["rung_id"]=="H3" and sel["route"]=="ROUTE_CHANGE" and sel["plan_digest"]==p["design_digest"]
a=copy.deepcopy(state); a["access_request"]=True; a["consecutive_unsuccessful_attempts"]=0
sel2=select_support(p,a); assert sel2["support_class"]=="ACCESS" and sel2["rung_id"]=="A1"
before=json.dumps(p,sort_keys=True); select_support(p,state); assert before==json.dumps(p,sort_keys=True)
assert any(x["route"]=="ROUTE_CHANGE" for x in p["support_ladder"])
blob=json.dumps(p).lower()
for token in ["weekly_allocation","time_allocation","page_coordinates","benchmark_reference","raw_evidence"]:
    assert token not in blob
assert steps["V02"]["learner_action"] and steps["V02"]["payload"]["prompted"] is False
assert steps["B04"]["payload"]["support_level"]>steps["B05"]["payload"]["support_level"]>steps["B06"]["payload"]["support_level"]
assert steps["B07"]["payload"]["number_only"] is False
print("MATH-V2-04 Learning Design falsifiers = 27 PASS")
