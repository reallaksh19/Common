#!/usr/bin/env python3
import json, sys, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"engine"))
from synthesize_math_study_model import synthesize, canonical_bytes, digest

def load(n): return json.loads((ROOT/"fixtures"/n).read_text(encoding="utf-8"))
model=synthesize(ROOT/"fixtures")
assert "status" not in model
by={d["target_id"]:d for d in model["target_decisions"]}
checks=[]
def ok(name, cond):
    assert cond, name
    checks.append(name)

ok("MODELLING_STRENGTH_PRESERVED", by["MATH-WORD-MODELLING"]["engagement_mode"]=="VERIFY_ONLY" and by["MATH-WORD-MODELLING"]["readiness_mode"]=="READY")
ok("GEOMETRY_STRENGTH_PRESERVED", by["MATH-GEOMETRIC-MODELLING"]["engagement_mode"]=="VERIFY_ONLY")
ok("SETUP_ENTRY_POINT_NOT_RELABELED", by["MATH-LINEAR-SYSTEM-SETUP"]["engagement_mode"]=="USE_AS_ENTRY_POINT" and by["MATH-LINEAR-SYSTEM-SETUP"]["decision_basis"]["capability_state"]=="READY")
ok("REPRESENTATION_ENTRY_POINT_NOT_RELABELED", by["MATH-REPRESENTATION-TRANSLATION"]["engagement_mode"]=="USE_AS_ENTRY_POINT")
ok("EQUALITY_REPAIR_LOCALIZED", by["MATH-EQUALITY-PRESERVATION"]["readiness_mode"]=="REPAIR_BEFORE" and by["MATH-EQUALITY-PRESERVATION"]["decision_basis"]["capability_state"]=="DEVELOPING")
ok("BINOMIAL_REPAIR_LOCALIZED", by["MATH-BINOMIAL-SQUARE-EXPANSION"]["readiness_mode"]=="REPAIR_IN_UNIT")
ok("AMBIGUOUS_SLOPE_TO_PROBE", by["MATH-ORDERED-PAIR-SEMANTICS"]["readiness_mode"]=="PROBE_FIRST")
probe=[r for r in by["MATH-ORDERED-PAIR-SEMANTICS"]["study_requirements"] if r["requirement_type"]=="DIAGNOSTIC_PROBE"][0]
ok("SLOPE_PROBE_REF_PRESERVED", probe["required_probe_ref"]=="MATH-PROBE-ORDERED-PAIR-SLOPE")
ok("VERIFICATION_OBLIGATION_PRESERVED", by["MATH-SOLUTION-VERIFICATION"]["readiness_mode"]=="REPAIR_IN_UNIT" and any(r["requirement_type"]=="VERIFICATION" for r in by["MATH-SOLUTION-VERIFICATION"]["study_requirements"]))
ok("DUAL_PROVENANCE", all(d["canonical_refs"] and d["learner_state_reason_refs"] and all(r["canonical_refs"] and r["learner_state_reason_refs"] for r in d["study_requirements"]) for d in model["target_decisions"]))
forbidden={"lesson_sequence","hint_ladder","hint_rung","practice_count","page_layout","calendar","spacing","time_allocation","benchmark_ref","raw_attempts","misconception_confirmed"}
text=canonical_bytes(model).decode()
ok("NO_TEACHING_OR_SCHEDULING_FIELDS", not any(f'"{k}"' in text for k in forbidden))
ok("NO_BLANKET_MATH_WEAK", "MATH_WEAK" not in text and "MATHEMATICS_WEAK" not in text)
ok("NO_CONFIRMED_MISCONCEPTION", "CONFIRMED" not in text and "misconception" not in text.lower())
m2=synthesize(ROOT/"fixtures")
ok("DETERMINISTIC_SYNTHESIS", canonical_bytes(model)==canonical_bytes(m2))
inputs={"goal":load("goal_scope.synthetic.json"),"canonical":load("canonical_interface.synthetic.json"),"learner":load("research_learner_view.synthetic.json"),"policy":load("policy.synthetic.json")}
ok("INPUT_DIGEST_RECOMPUTES", model["input_digest"]==digest(inputs))
can=load("canonical_interface.synthetic.json"); lr=load("research_learner_view.synthetic.json")
ok("INTERFACES_NON_AUTHORITATIVE", can["interface_role"]=="INTERFACE_FIXTURE_ONLY" and can["contains_definitions"] is False and lr["interface_role"]=="DESCRIPTIVE_VIEW_FIXTURE_ONLY")
with tempfile.TemporaryDirectory() as td:
    p=Path(td)
    for name in ["goal_scope.synthetic.json","canonical_interface.synthetic.json","research_learner_view.synthetic.json","policy.synthetic.json"]:
        data=load(name)
        if name=="canonical_interface.synthetic.json": data["requirement_catalog"].pop("MATH-BINOMIAL-SQUARE-EXPANSION")
        (p/name).write_text(json.dumps(data),encoding="utf-8")
    blocked=synthesize(p)
    ok("CANONICAL_GAP_FAILBACK", blocked["status"]=="BLOCKED" and blocked["gap"]["gap_type"]=="CANONICAL_KNOWLEDGE_GAP")
print(f"MATH-V2-03 Study Synthesis falsifiers: {len(checks)} PASS")
