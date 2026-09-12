from pathlib import Path
import copy, importlib.util, json

ROOT=Path(__file__).resolve().parents[1]
ENGINE=ROOT/"engine"/"synthesize_study_model.py"
spec=importlib.util.spec_from_file_location("synth",ENGINE)
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

d=m.load_inputs(ROOT/"fixtures")
def run(**over):
    x={k:copy.deepcopy(v) for k,v in d.items()}; x.update(over)
    return m.synthesize(x["goal"],x["scope"],x["cks"],x["view"],x["policy"])

def decision(out,target):
    return next(x for x in out["learner_study_model"]["target_decisions"] if x["target_id"]==target)

# 1 deterministic exact replay
a=run(); b=run()
assert m.canonical_bytes(a)==m.canonical_bytes(b) and a["status"]=="PASS"

# 2 preserve demonstrated modelling
q=decision(a,"math.word-equation-modeling")
assert q["engagement_mode"]=="VERIFY_ONLY" and q["readiness_mode"]=="READY"

# 3 demonstrated setup becomes entry point because downstream equality repair depends on it
q=decision(a,"math.linear-system-setup")
assert q["engagement_mode"]=="USE_AS_ENTRY_POINT" and q["decision_basis"]["capability_state"]=="DEMONSTRATED"

# 4 downstream equality repair does not erase setup strength
q=decision(a,"math.equality-execution")
assert q["readiness_mode"]=="REPAIR_BEFORE" and q["decision_basis"]["capability_state"]=="REPAIR_REQUIRED"
assert decision(a,"math.linear-system-setup")["decision_basis"]["capability_state"]=="DEMONSTRATED"

# 5 ambiguity/probe remains probe-first
q=decision(a,"math.slope-semantics")
assert q["readiness_mode"]=="PROBE_FIRST" and q["decision_basis"]["capability_state"]=="PROBE_REQUIRED"

# 6 developing verification is repair-in-unit
assert decision(a,"math.verification")["readiness_mode"]=="REPAIR_IN_UNIT"

# 7 every decision has dual provenance
for q in a["learner_study_model"]["target_decisions"]:
    assert q["canonical_refs"] and q["learner_state_reason_refs"]
    for r in q["study_requirements"]:
        assert r["canonical_refs"] and r["learner_state_reason_refs"]

# 8 missing canonical truth -> canonical gap, no model
cks=copy.deepcopy(d["cks"]); cks["assets"]=[x for x in cks["assets"] if x["asset_id"]!="math.slope-semantics"]
o=run(cks=cks)
assert o["status"]=="BLOCKED" and "learner_study_model" not in o
assert any(g["gap_type"]=="CANONICAL_KNOWLEDGE_GAP" and g["target_id"]=="math.slope-semantics" for g in o["gaps"])

# 9 missing learner reason -> explicit reason gap
view=copy.deepcopy(d["view"]); next(x for x in view["capabilities"] if x["target_id"]=="math.verification")["reason_refs"]=[]
o=run(view=view)
assert o["status"]=="BLOCKED" and any(g["gap_type"]=="LEARNER_STATE_REASON_GAP" for g in o["gaps"])

# 10 goal target cannot silently disappear from target scope
scope=copy.deepcopy(d["scope"]); scope["required_target_ids"].remove("math.verification")
o=run(scope=scope)
assert o["status"]=="BLOCKED" and any(g["gap_type"]=="STUDY_SYNTHESIS_POLICY_GAP" and g["target_id"]=="math.verification" for g in o["gaps"])

# 11 raw evidence is forbidden: Study Synthesis may not re-diagnose
view=copy.deepcopy(d["view"]); view["raw_attempts"]=[{"answer":"x"}]
try:
    run(view=view); raise AssertionError("raw attempts should be rejected")
except ValueError as e:
    assert "forbidden producer input key" in str(e)

# 12 benchmark/reference artifacts forbidden
goal=copy.deepcopy(d["goal"]); goal["benchmark_refs"]=["PR156"]
try:
    run(goal=goal); raise AssertionError("benchmark should be rejected")
except ValueError as e:
    assert "forbidden producer input key" in str(e)

# 13 teaching choreography forbidden from output model
bad=copy.deepcopy(a["learner_study_model"]); bad["hint_ladder"]=[]
assert m.find_forbidden_output(bad)

# 14 scheduling forbidden from output model
bad=copy.deepcopy(a["learner_study_model"]); bad["study_calendar"]={}
assert m.find_forbidden_output(bad)

# 15 unknown/ambiguous cannot become repair-required in this layer
view=copy.deepcopy(d["view"]); cap=next(x for x in view["capabilities"] if x["target_id"]=="math.slope-semantics"); cap["state"]="AMBIGUOUS"
o=run(view=view)
assert decision(o,"math.slope-semantics")["readiness_mode"]=="PROBE_FIRST"

# 16 no blanket topic weakness object exists
s=json.dumps(a["learner_study_model"],sort_keys=True)
assert "MATH = WEAK" not in s and "topic_weakness" not in s

print("V2-04 Study Synthesis falsifiers: 16 PASS")
