from __future__ import annotations
import hashlib
import json

FORBIDDEN_INPUT_KEY_TOKENS=("benchmark","reference_artifact","golden_artifact","comparator_artifact")

class ScopeInvariantError(ValueError): pass
class DependencyCycleError(ScopeInvariantError): pass

def canonical_bytes(value):
    return json.dumps(value,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode("utf-8")

def digest_of(value): return hashlib.sha256(canonical_bytes(value)).hexdigest()

def reject_forbidden_producer_inputs(value,path="$"):
    if isinstance(value,dict):
        for key,child in value.items():
            if any(token in key.lower() for token in FORBIDDEN_INPUT_KEY_TOKENS):
                raise ScopeInvariantError(f"forbidden producer input key at {path}.{key}")
            reject_forbidden_producer_inputs(child,f"{path}.{key}")
    elif isinstance(value,list):
        for i,child in enumerate(value): reject_forbidden_producer_inputs(child,f"{path}[{i}]")

def validate_goal_request(goal):
    target=set(goal["target_ids"]); mandatory=set(goal["mandatory_target_ids"]); optional=set(goal["optional_target_ids"])
    if not mandatory<=target: raise ScopeInvariantError("mandatory targets must be requested targets")
    if not optional<=target: raise ScopeInvariantError("optional targets must be requested targets")
    if mandatory&optional: raise ScopeInvariantError("target cannot be both mandatory and optional")
    reject_forbidden_producer_inputs(goal)

def validate_target_scope(goal,scope,registry):
    validate_goal_request(goal); reject_forbidden_producer_inputs(scope)
    if scope["goal_request_id"]!=goal["goal_request_id"]: raise ScopeInvariantError("target scope must bind exact goal request")
    if scope["canonical_registry_id"]!=registry["registry_id"]: raise ScopeInvariantError("target scope registry id mismatch")
    if scope["canonical_registry_version"]!=registry["version"]: raise ScopeInvariantError("target scope registry version mismatch")
    if scope["canonical_registry_digest"]!=registry["digest"]: raise ScopeInvariantError("target scope registry digest mismatch")
    obligations=scope["target_obligations"]; ids=[x["canonical_id"] for x in obligations]
    if len(ids)!=len(set(ids)): raise ScopeInvariantError("duplicate target obligation")
    required={x["canonical_id"] for x in obligations if x["obligation"]=="REQUIRED"}; optional={x["canonical_id"] for x in obligations if x["obligation"]=="OPTIONAL"}; excluded=set(scope["excluded_target_ids"]); requested=set(goal["target_ids"])
    if required&excluded or optional&excluded: raise ScopeInvariantError("included obligation cannot also be excluded")
    if not set(goal["mandatory_target_ids"])<=required: raise ScopeInvariantError("mandatory goal target silently lost from CanonicalTargetScope")
    if not required|optional<=requested: raise ScopeInvariantError("CanonicalTargetScope cannot invent requested targets")
    registry_ids={x["canonical_id"] for x in registry["assets"]}
    if not (required|optional|excluded)<=registry_ids: raise ScopeInvariantError("target scope references unknown canonical id")
    return required,optional

def validate_learner_study_scope(target_scope,study_scope):
    reject_forbidden_producer_inputs(study_scope)
    if study_scope["canonical_target_scope_id"]!=target_scope["canonical_target_scope_id"]: raise ScopeInvariantError("LearnerStudyScope must bind CanonicalTargetScope")
    required={x["canonical_id"] for x in target_scope["target_obligations"] if x["obligation"]=="REQUIRED"}; inherited=set(study_scope["inherited_required_target_ids"])
    if inherited!=required: raise ScopeInvariantError("LearnerStudyScope must inherit exact required target set")
    active=set(study_scope["active_target_ids"]); deferred={x["canonical_id"] for x in study_scope["deferred_required_targets"]}
    if active&deferred: raise ScopeInvariantError("required target cannot be active and deferred")
    if required-active-deferred: raise ScopeInvariantError("required target silently dropped rather than explicitly deferred")
    if deferred-required: raise ScopeInvariantError("only required targets may use required-target deferral accounting")
    excluded=set(target_scope["excluded_target_ids"])
    if (active|set(study_scope.get("added_dependency_target_ids",[])))&excluded: raise ScopeInvariantError("excluded CanonicalTargetScope target reintroduced downstream")

def validate_publication_scope(study_scope,publication_scope):
    reject_forbidden_producer_inputs(publication_scope)
    if publication_scope["learner_study_scope_id"]!=study_scope["learner_study_scope_id"]: raise ScopeInvariantError("PublicationScope must bind LearnerStudyScope")
    active=set(study_scope["active_target_ids"]); selected=set(publication_scope["selected_target_ids"]); omitted={x["canonical_id"] for x in publication_scope["omitted_active_targets"]}
    if selected&omitted: raise ScopeInvariantError("publication target cannot be both selected and omitted")
    if selected|omitted!=active: raise ScopeInvariantError("PublicationScope must account for every active study target exactly once")

def _asset_index(registry):
    idx={}
    for asset in registry["assets"]:
        cid=asset["canonical_id"]
        if cid in idx: raise ScopeInvariantError(f"duplicate canonical registry id: {cid}")
        idx[cid]=asset
    return idx

def _dependency_status(parent,child,dep):
    if child["status"]!="ACTIVE": return "REVALIDATE"
    if dep.get("required_version") and child["version"]!=dep["required_version"]: return "REVALIDATE"
    if dep.get("required_digest") and child["digest"]!=dep["required_digest"]: return "REVALIDATE"
    if parent["subject"]!=child["subject"]: return "COMPOSE_DEPENDENCY"
    return "REUSE_EXISTING"

def resolve_canonical_knowledge_set(scope,registry):
    reject_forbidden_producer_inputs(scope); reject_forbidden_producer_inputs(registry)
    if scope["canonical_registry_id"]!=registry["registry_id"] or scope["canonical_registry_version"]!=registry["version"] or scope["canonical_registry_digest"]!=registry["digest"]: raise ScopeInvariantError("scope/registry identity mismatch")
    idx=_asset_index(registry); primary_ids=sorted(x["canonical_id"] for x in scope["target_obligations"] if x["obligation"]=="REQUIRED"); primary=[]
    for cid in primary_ids:
        if cid not in idx: raise ScopeInvariantError(f"primary target missing from registry: {cid}")
        a=idx[cid]; primary.append({"canonical_id":cid,"subject":a["subject"],"version":a["version"],"digest":a["digest"]})
    events=[]; gaps=[]; dep_info={}; visiting=[]; visited=set(primary_ids)
    def visit(parent_id):
        if parent_id in visiting: raise DependencyCycleError("canonical dependency cycle: "+" -> ".join(visiting+[parent_id]))
        parent=idx[parent_id]; visiting.append(parent_id)
        for dep in sorted(parent["dependencies"],key=lambda x:(x["canonical_id"],x["reason"])):
            child_id=dep["canonical_id"]
            if child_id in visiting: raise DependencyCycleError("canonical dependency cycle: "+" -> ".join(visiting+[child_id]))
            child=idx.get(child_id)
            if child is None:
                events.append({"from_id":parent_id,"to_id":child_id,"status":"CANONICAL_GAP_CANDIDATE","reason":dep["reason"]}); gaps.append({"missing_canonical_id":child_id,"required_by":parent_id,"reason":dep["reason"]}); continue
            status=_dependency_status(parent,child,dep); events.append({"from_id":parent_id,"to_id":child_id,"status":status,"reason":dep["reason"]})
            info=dep_info.setdefault(child_id,{"canonical_id":child_id,"subject":child["subject"],"version":child["version"],"digest":child["digest"],"required_by":set(),"dependency_reason":set(),"statuses":set()}); info["required_by"].add(parent_id); info["dependency_reason"].add(dep["reason"]); info["statuses"].add(status)
            if child_id not in visited: visit(child_id); visited.add(child_id)
        visiting.pop()
    for pid in primary_ids: visit(pid)
    dependency_bundles=[]
    for cid in sorted(dep_info):
        if cid in primary_ids: continue
        info=dep_info[cid]; statuses=info["statuses"]; status="REVALIDATE" if "REVALIDATE" in statuses else ("COMPOSE_DEPENDENCY" if "COMPOSE_DEPENDENCY" in statuses else "REUSE_EXISTING")
        dependency_bundles.append({"canonical_id":info["canonical_id"],"subject":info["subject"],"version":info["version"],"digest":info["digest"],"required_by":sorted(info["required_by"]),"dependency_reason":sorted(info["dependency_reason"]),"resolution_status":status})
    output={"canonical_knowledge_set_id":f"cks:{scope['canonical_target_scope_id']}","schema_version":"2.0.0","canonical_registry_id":registry["registry_id"],"canonical_registry_version":registry["version"],"canonical_registry_digest":registry["digest"],"primary_bundles":primary,"dependency_bundles":dependency_bundles,"resolution_events":sorted(events,key=lambda x:(x["from_id"],x["to_id"],x["status"],x["reason"])),"canonical_gap_candidates":sorted(gaps,key=lambda x:(x["missing_canonical_id"],x["required_by"],x["reason"]))}
    output["knowledge_set_digest"]=digest_of(output); return output
