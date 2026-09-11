from __future__ import annotations
import argparse, copy, hashlib, json
from pathlib import Path

FORBIDDEN_INPUT_KEYS = {
    "raw_attempts","learner_evidence_ledger","reasoning_observations",
    "benchmark","benchmark_refs","reference_artifact","pr156","pr157",
    "lesson_sequence","hint_ladder","support_fading","practice_count",
    "page_layout","renderer","study_calendar","review_interval","time_allocation"
}
FORBIDDEN_OUTPUT_KEYS = {
    "lesson_sequence","explanation_sequence","hint_ladder","support_fading",
    "practice_count","page_layout","renderer","interaction_support_rung",
    "study_calendar","review_interval","time_allocation","next_study_order",
    "benchmark_refs","reference_artifact"
}

def canonical_bytes(value):
    return json.dumps(value, sort_keys=True, separators=(",",":"), ensure_ascii=False).encode("utf-8")

def stable_id(prefix, value):
    return prefix + hashlib.sha256(canonical_bytes(value)).hexdigest()[:16]

def reject_forbidden_inputs(value, path="$"):
    if isinstance(value, dict):
        for k,v in value.items():
            if k.lower() in FORBIDDEN_INPUT_KEYS:
                raise ValueError(f"forbidden producer input key at {path}.{k}")
            reject_forbidden_inputs(v, f"{path}.{k}")
    elif isinstance(value, list):
        for i,v in enumerate(value):
            reject_forbidden_inputs(v, f"{path}[{i}]")

def find_forbidden_output(value, path="$"):
    found=[]
    if isinstance(value, dict):
        for k,v in value.items():
            if k.lower() in FORBIDDEN_OUTPUT_KEYS:
                found.append(f"{path}.{k}")
            found.extend(find_forbidden_output(v, f"{path}.{k}"))
    elif isinstance(value, list):
        for i,v in enumerate(value):
            found.extend(find_forbidden_output(v, f"{path}[{i}]"))
    return found

def load_inputs(fixture_root):
    r=Path(fixture_root)
    return {
      "goal":json.loads((r/"learning_goal.synthetic.json").read_text()),
      "scope":json.loads((r/"canonical_target_scope.synthetic.json").read_text()),
      "cks":json.loads((r/"canonical_knowledge_set.synthetic.json").read_text()),
      "view":json.loads((r/"research_learner_view.synthetic.json").read_text()),
      "policy":json.loads((r/"study_synthesis_policy.synthetic.json").read_text()),
    }

def _gap(gap_type,target_id,description,refs):
    body={"gap_type":gap_type,"target_id":target_id,"description":description,"required_refs":sorted(set(refs))}
    return {"gap_id":stable_id("GAP-",body),**body}

def synthesize(goal, scope, cks, view, policy):
    for obj in [goal,scope,cks,view,policy]:
        reject_forbidden_inputs(obj)

    requested=list(goal["requested_target_ids"])
    required=list(scope["required_target_ids"])
    missing_goal=sorted(set(requested)-set(required))
    gaps=[]
    for t in missing_goal:
        gaps.append(_gap("STUDY_SYNTHESIS_POLICY_GAP",t,"requested goal target is absent from canonical target scope",[goal["goal_id"],scope["scope_id"]]))

    assets={a["asset_id"]:a for a in cks["assets"]}
    states={c["target_id"]:c for c in view["capabilities"]}
    rules=policy["state_rules"]
    edges=scope.get("dependency_edges",[])

    decisions=[]
    readiness_by_target={}
    for target in required:
        if target not in assets:
            gaps.append(_gap("CANONICAL_KNOWLEDGE_GAP",target,"target has no canonical binding",[cks["canonical_knowledge_set_id"]]))
            continue
        cap=states.get(target)
        if not cap or not cap.get("reason_refs"):
            gaps.append(_gap("LEARNER_STATE_REASON_GAP",target,"learner-conditioned synthesis requires a descriptive state reason",[view["research_learner_view_id"]]))
            continue
        state=cap["state"]
        if state not in rules:
            gaps.append(_gap("STUDY_SYNTHESIS_POLICY_GAP",target,f"no policy rule for state {state}",[policy["policy_id"]]))
            continue
        readiness_by_target[target]=rules[state]["readiness_mode"]

    if gaps:
        return {
          "status":"BLOCKED",
          "input_identity":{
             "goal_ref":goal["goal_id"],"canonical_target_scope_ref":scope["scope_id"],
             "canonical_knowledge_set_ref":cks["canonical_knowledge_set_id"],
             "research_learner_view_ref":view["research_learner_view_id"],
             "policy_version":policy["version"]
          },
          "gaps":sorted(gaps,key=lambda x:(x["gap_type"],x["target_id"],x["gap_id"]))
        }

    dep_of_repair=set()
    allowed_entry=set(policy["entry_point_rule"]["when_dependency_of_readiness"])
    if policy["entry_point_rule"]["enabled"]:
        for e in edges:
            if readiness_by_target.get(e["to"]) in allowed_entry:
                dep_of_repair.add(e["from"])

    for target in sorted(required):
        asset=assets[target]
        cap=states[target]
        state=cap["state"]
        rule=rules[state]
        engagement=rule["engagement_mode"]
        readiness=rule["readiness_mode"]
        policy_rule=f"state_rules.{state}"
        if state=="DEMONSTRATED" and target in dep_of_repair:
            engagement="USE_AS_ENTRY_POINT"
            policy_rule="entry_point_rule"

        required_kinds=[]
        if engagement=="VERIFY_ONLY":
            required_kinds.extend(policy["requirement_rules"]["VERIFY_ONLY"])
        if readiness in policy["requirement_rules"]:
            required_kinds.extend(policy["requirement_rules"][readiness])
        required_kinds.extend(asset.get("semantic_requirements",[]))
        required_kinds=sorted(set(required_kinds))

        reqs=[]
        for kind in required_kinds:
            body={"target_id":target,"kind":kind,"asset_id":asset["asset_id"],"reason_refs":sorted(cap["reason_refs"])}
            reqs.append({
              "requirement_id":stable_id("REQ-",body),
              "kind":kind,
              "statement":f"{kind} obligation for {target}",
              "canonical_refs":[asset["asset_id"]],
              "learner_state_reason_refs":sorted(cap["reason_refs"])
            })

        decisions.append({
          "target_id":target,
          "engagement_mode":engagement,
          "readiness_mode":readiness,
          "canonical_refs":[asset["asset_id"]],
          "learner_state_reason_refs":sorted(cap["reason_refs"]),
          "decision_basis":{"capability_state":state,"policy_rule":policy_rule},
          "study_requirements":reqs
        })

    model_seed={
      "goal_ref":goal["goal_id"],"canonical_target_scope_ref":scope["scope_id"],
      "canonical_knowledge_set_ref":cks["canonical_knowledge_set_id"],
      "research_learner_view_ref":view["research_learner_view_id"],
      "study_synthesis_policy_version":policy["version"],"target_decisions":decisions
    }
    model={"study_model_id":stable_id("LSM-",model_seed),"schema_version":"1.0.0",**model_seed}
    forbidden=find_forbidden_output(model)
    if forbidden:
        raise ValueError("forbidden StudyModel fields: "+", ".join(forbidden))
    return {
      "status":"PASS",
      "input_identity":{
         "goal_ref":goal["goal_id"],"canonical_target_scope_ref":scope["scope_id"],
         "canonical_knowledge_set_ref":cks["canonical_knowledge_set_id"],
         "research_learner_view_ref":view["research_learner_view_id"],
         "policy_version":policy["version"]
      },
      "learner_study_model":model,
      "gaps":[]
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--fixture-root",required=True)
    args=ap.parse_args()
    d=load_inputs(args.fixture_root)
    out=synthesize(d["goal"],d["scope"],d["cks"],d["view"],d["policy"])
    print(json.dumps(out,sort_keys=True,separators=(",",":"),ensure_ascii=False))

if __name__=="__main__":
    main()
