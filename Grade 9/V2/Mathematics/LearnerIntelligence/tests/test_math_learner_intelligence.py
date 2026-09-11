#!/usr/bin/env python3
from __future__ import annotations
import json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"engine"))
from derive_math_learner_state import derive, canonical_bytes, digest

interface=json.loads((ROOT/"fixtures/canonical_interface.synthetic.json").read_text())
evidence=json.loads((ROOT/"fixtures/learner_evidence.synthetic.json").read_text())
out=derive(interface,evidence)
state={r["capability_ref"]:r for r in out["state"]["capability_states"]}
cases={d["evidence_refs"][0]:d for d in out["diagnostic_cases"]}

assert evidence["privacy_class"]=="PUBLIC_SYNTHETIC"
assert evidence["learner_ref"].startswith("SYNTHETIC-")
assert interface["authority"]=="INTERFACE_FIXTURE_ONLY"

assert state["MATH-WORD-MODELLING"]["state"]=="READY"
assert state["MATH-LINEAR-SYSTEM-SETUP"]["state"]=="READY"
assert state["MATH-GEOMETRIC-MODELLING"]["state"]=="READY"
assert state["MATH-REPRESENTATION-TRANSLATION"]["state"]=="READY"

assert state["MATH-EQUALITY-PRESERVATION"]["state"]=="DEVELOPING"
assert state["MATH-BINOMIAL-SQUARE-EXPANSION"]["state"]=="DEVELOPING"
assert all(r["state"]!="REPAIR_REQUIRED" for r in out["state"]["capability_states"])
assert all(d["hypothesis_status"]!="SUPPORTED" for d in out["diagnostic_cases"])

eq_obs=[o for o in out["observations"] if o["capability_ref"]=="MATH-EQUALITY-PRESERVATION"]
assert any(o["evidence_class"]=="GUIDED_SUCCESS" and not o["independent"] for o in eq_obs)
assert state["MATH-EQUALITY-PRESERVATION"]["state"]!="READY"

assert state["MATH-ORDERED-PAIR-SEMANTICS"]["state"]=="UNKNOWN"
assert cases["E-C2"]["hypothesis_status"]=="UNRESOLVED"
assert cases["E-C2"]["probe_required"] is True
assert cases["E-C2"]["probe_ref"]=="MATH-PROBE-ORDERED-PAIR-SLOPE"

vb=out["state"]["verification_behavior"]
assert vb["can_verify_when_prompted"] is True
assert vb["self_initiated_verification"] is False
assert state["MATH-SOLUTION-VERIFICATION"]["state"]=="DEVELOPING"

for forbidden in ("description","success_criteria","formal_object","formula","theorem","semantic_definition"):
    assert forbidden not in json.dumps(interface)

view_blob=json.dumps(out["research_learner_view"])
for forbidden in ("RETEACH","REPAIR_BEFORE","REPAIR_IN_UNIT","PROBE_FIRST","COMPRESS","USE_AS_ENTRY_POINT","HINT_RUNG","practice_count","teaching_sequence","page_layout"):
    assert forbidden not in view_blob

for forbidden in ("working_memory","attention_deficit","motivation_deficit","cognitive_limit"):
    assert forbidden not in json.dumps(out).lower()

runtime_blob=(ROOT/"engine/derive_math_learner_state.py").read_text()+json.dumps(interface)+json.dumps(evidence)
for forbidden in ("pull/156","pull/157","pull/168","pull/170","benchmark_template","benchmark_reference"):
    assert forbidden not in runtime_blob

out2=derive(interface,evidence)
assert canonical_bytes(out)==canonical_bytes(out2)
core={k:v for k,v in out["state"].items() if k!="semantic_digest"}
assert out["state"]["semantic_digest"]==digest(core)

bad=json.loads(json.dumps(evidence))
bad["privacy_class"]="PRODUCTION"
try:
    derive(interface,bad)
    raise AssertionError("production evidence unexpectedly accepted")
except ValueError:
    pass

print("MATH-V2-02 learner-intelligence falsifiers: 15 PASS")
