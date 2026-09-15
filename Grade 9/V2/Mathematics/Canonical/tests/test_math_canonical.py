#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANON = ROOT/"canonical"
FIX = ROOT/"fixtures"

def load(p): return json.loads(Path(p).read_text(encoding="utf-8"))
caps=load(CANON/"capabilities.v1.json")
errs=load(CANON/"error_signatures.v1.json")
probes=load(CANON/"diagnostic_probes.v1.json")
rcs=load(CANON/"reasoning_contracts.v1.json")
fixture=load(FIX/"acceptance_cases.synthetic.json")
cap_ids={x["capability_id"] for x in caps}
err_ids={x["error_signature_id"] for x in errs}
probe_ids={x["probe_id"] for x in probes}

def check(condition, label):
    assert condition, label
    print(label + " = PASS")

for c in caps:
    for ref in c.get("prerequisite_capability_refs",[]):
        assert ref in cap_ids or ref.startswith("SHARED-"), ("bad prerequisite",ref)
    assert set(c.get("error_signature_refs",[])) <= err_ids
    assert set(c.get("diagnostic_probe_refs",[])) <= probe_ids
for e in errs:
    assert set(e["candidate_capability_refs"]) <= cap_ids
for p in probes:
    assert p["target_capability_ref"] in cap_ids
for rc in rcs:
    for cp in rc["checkpoints"]:
        assert set(cp["required_capability_refs"]) <= cap_ids
        assert set(cp.get("error_signature_refs",[])) <= err_ids
check(True,"REFERENTIAL_INTEGRITY")

required_stages={"UNDERSTAND_OBJECT","SELECT_REPRESENTATION","RECOGNIZE_STRUCTURE","TRANSFORM","PRESERVE_INVARIANT","VERIFY_RESULT"}
present={c["reasoning_stage"] for c in caps}
check(required_stages <= present,"MATH_REASONING_CHECKPOINTS")

cases={c["case_id"]:c for c in fixture["cases"]}
ls=cases["MATH-LINEAR-SYSTEM-01"]
check({"MATH-WORD-MODELLING","MATH-LINEAR-SYSTEM-SETUP"} <= set(ls["must_preserve"]),"MODELLING_SURVIVES_DOWNSTREAM_ALGEBRA_FAILURE")
check(not (set(ls["must_preserve"]) & set(ls["candidate_failure_capabilities"])),"UPSTREAM_SUCCESS_NOT_RELABELED_AS_FAILURE")

ga=cases["MATH-GEOMETRY-ALGEBRA-01"]
check("MATH-GEOMETRIC-MODELLING" in ga["must_preserve"],"GEOMETRY_SURVIVES_EXPANSION_FAILURE")
check("MATH-BINOMIAL-SQUARE-EXPANSION" in ga["candidate_failure_capabilities"],"EXPANSION_FAILURE_LOCALIZED")

sl=cases["MATH-COORDINATE-SLOPE-01"]
check(sl["required_probe_ref"]=="MATH-PROBE-ORDERED-PAIR-SLOPE" and sl["required_probe_ref"] in probe_ids,"AMBIGUOUS_COORDINATE_SEMANTICS_HAS_TARGETED_PROBE")
probe=next(p for p in probes if p["probe_id"]=="MATH-PROBE-ORDERED-PAIR-SLOPE")
check("long word-problem parsing" not in probe["confounds_to_avoid"],"COORDINATE_PROBE_CONFOUNDS_EXPLICIT")

ver=next(c for c in caps if c["capability_id"]=="MATH-SOLUTION-VERIFICATION")
check(ver["reasoning_stage"]=="VERIFY_RESULT" and "VALIDATION" in ver["capability_class"],"VERIFICATION_IS_FIRST_CLASS")
verify_case=cases["MATH-VERIFY-01"]
check(verify_case["candidate_failure_capabilities"]==["MATH-SOLUTION-VERIFICATION"],"VERIFICATION_FAILURE_SEPARATE_FROM_SOLVING")

forbidden={"learner_state","mastery","repair_required","weakness","diagnosis","bxx"}
blob=json.dumps(caps).lower()
check(not any(f'"{k}"' in blob for k in forbidden),"SHARED_FAMILY_TAG_NOT_LEARNER_TRAIT")

check(fixture["privacy_class"]=="PUBLIC_SYNTHETIC" and "learner_ref" not in json.dumps(fixture),"REAL_LEARNER_DATA_ZERO")

with tempfile.TemporaryDirectory() as td:
    a=Path(td)/"a.json"; b=Path(td)/"b.json"
    cmd=[sys.executable,str(ROOT/"engine"/"build_math_canonical.py"),"--out"]
    subprocess.check_call(cmd+[str(a)])
    subprocess.check_call(cmd+[str(b)])
    check(a.read_bytes()==b.read_bytes(),"DETERMINISTIC_CANONICAL_PACKAGE")
    pkg=load(a)
    check(pkg["benchmark_inputs"]==[],"BENCHMARK_PRODUCER_INPUTS_ZERO")
    digest=pkg["package_digest"]
    payload=dict(pkg); payload.pop("package_digest")
    expected=hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()
    check(digest==expected,"PACKAGE_DIGEST_RECOMPUTES")

eq=next(e for e in errs if e["error_signature_id"]=="MATH-ERR-ILLEGAL-EQUALITY-CANCELLATION")
check("MATHEMATICS-GLOBALLY-WEAK" in eq["must_not_imply"],"ERROR_SIGNATURE_NOT_BLANKET_TOPIC_LABEL")

forbidden_keys={"study_treatment","readiness","hint_rung","page_intent","publication_layout","practice_count","teaching_sequence","benchmark_reference"}
def walk(x):
    if isinstance(x,dict):
        for k,v in x.items():
            assert k not in forbidden_keys, ("forbidden downstream key",k)
            walk(v)
    elif isinstance(x,list):
        for v in x: walk(v)
for obj in [caps,errs,probes,rcs]: walk(obj)
check(True,"CANONICAL_AUTHORITY_BOUNDARY")

print("MATH-V2-01 canonical falsifiers: PASS")
