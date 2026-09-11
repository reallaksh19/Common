#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path

FORBIDDEN_KEYS = {
    "lesson_sequence","example_order","hint_ladder","hint_rung","support_fading",
    "practice_count","page_layout","renderer","calendar","spacing","time_allocation",
    "benchmark_ref","benchmark_page","raw_attempts","misconception_confirmed"
}

def canonical_bytes(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")

def digest(obj):
    return hashlib.sha256(canonical_bytes(obj)).hexdigest()

def load(root: Path, name: str):
    return json.loads((root / name).read_text(encoding="utf-8"))

def find_forbidden(obj):
    found=[]
    def walk(x):
        if isinstance(x, dict):
            for k,v in x.items():
                if k in FORBIDDEN_KEYS: found.append(k)
                walk(v)
        elif isinstance(x, list):
            for v in x: walk(v)
    walk(obj)
    return sorted(set(found))

def synthesize(root: Path):
    goal=load(root,"goal_scope.synthetic.json")
    canonical=load(root,"canonical_interface.synthetic.json")
    learner=load(root,"research_learner_view.synthetic.json")
    policy=load(root,"policy.synthetic.json")

    for obj in (goal, canonical, learner):
        if obj.get("fixture_class") != "PUBLIC_SYNTHETIC":
            raise ValueError("production or non-synthetic input rejected")
    if canonical.get("interface_role") != "INTERFACE_FIXTURE_ONLY":
        raise ValueError("canonical interface fixture must remain non-authoritative")
    if learner.get("interface_role") != "DESCRIPTIVE_VIEW_FIXTURE_ONLY":
        raise ValueError("learner interface fixture must remain descriptive")
    if learner.get("contains_raw_attempts") is not False:
        raise ValueError("raw evidence is not legal Study Synthesis input")
    if policy.get("benchmark_inputs"):
        raise ValueError("benchmark inputs forbidden")
    forbidden=find_forbidden([goal,canonical,learner,policy])
    if forbidden:
        raise ValueError(f"forbidden producer semantics: {forbidden}")

    state_by={r["capability_ref"]:r for r in learner["capability_states"]}
    allowed=set(canonical["capability_refs"])
    probe_refs=set(canonical["probe_refs"])
    catalog=canonical["requirement_catalog"]
    decisions=[]

    for target in goal["targets"]:
        if target not in allowed or target not in catalog:
            return {"status":"BLOCKED","gap":{"gap_type":"CANONICAL_KNOWLEDGE_GAP","target_id":target}}
        state=state_by.get(target)
        if not state or not state.get("reason_refs"):
            return {"status":"BLOCKED","gap":{"gap_type":"LEARNER_STATE_REASON_GAP","target_id":target}}
        s=state["state"]
        if s == "READY":
            if target in policy["entry_point_targets"]:
                engagement, readiness, rule = "USE_AS_ENTRY_POINT", "READY", "READY_ENTRY_POINT"
            else:
                engagement, readiness, rule = policy["ready_default_engagement"], "READY", "READY_VERIFY"
        elif s == "DEVELOPING":
            engagement="ACTIVE_STUDY"
            if target in policy["repair_before_targets"]:
                readiness, rule="REPAIR_BEFORE","DEVELOPING_HIGH_DEPENDENCY_REPAIR_BEFORE"
            else:
                readiness, rule=policy["developing_default_readiness"],"DEVELOPING_REPAIR_IN_UNIT"
        elif s == "UNKNOWN" and state.get("probe_required"):
            if state.get("probe_ref") not in probe_refs:
                return {"status":"BLOCKED","gap":{"gap_type":"CANONICAL_KNOWLEDGE_GAP","target_id":target,"missing_ref":state.get("probe_ref")}}
            engagement, readiness, rule="ACTIVE_STUDY",policy["unknown_with_probe_action"],"UNKNOWN_PRESERVE_PROBE"
        else:
            engagement, readiness, rule="ACTIVE_STUDY","PROBE_FIRST","UNRESOLVED_STATE_PROBE"

        reqs=[]
        for r in catalog[target]:
            refs=r["canonical_refs"]
            missing=[ref for ref in refs if ref not in allowed and ref not in probe_refs]
            if missing:
                return {"status":"BLOCKED","gap":{"gap_type":"CANONICAL_KNOWLEDGE_GAP","target_id":target,"missing_ref":missing[0]}}
            req={
                "requirement_id":r["requirement_id"],
                "requirement_type":r["requirement_type"],
                "canonical_refs":refs,
                "learner_state_reason_refs":state["reason_refs"],
                "completion_evidence":r["completion_evidence"]
            }
            if "required_probe_ref" in r:
                req["required_probe_ref"]=r["required_probe_ref"]
            reqs.append(req)
        decisions.append({
            "target_id":target,
            "engagement_mode":engagement,
            "readiness_mode":readiness,
            "canonical_refs":[target],
            "learner_state_reason_refs":state["reason_refs"],
            "decision_basis":{"capability_state":s,"policy_rule":rule},
            "study_requirements":reqs
        })

    inputs={"goal":goal,"canonical":canonical,"learner":learner,"policy":policy}
    inp=digest(inputs)
    return {
        "study_model_id":"MATH-LSM-"+inp[:16],
        "schema_version":"1.0.0",
        "goal_ref":goal["goal_ref"],
        "canonical_target_scope_ref":goal["canonical_target_scope_ref"],
        "canonical_knowledge_set_ref":canonical["canonical_knowledge_set_ref"],
        "research_learner_view_ref":learner["research_learner_view_ref"],
        "study_synthesis_policy_version":policy["version"],
        "target_decisions":decisions,
        "input_digest":inp
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--fixture-root",type=Path,default=Path(__file__).resolve().parents[1]/"fixtures")
    args=ap.parse_args()
    print(json.dumps(synthesize(args.fixture_root), sort_keys=True, separators=(",", ":"), ensure_ascii=False))

if __name__=="__main__": main()
