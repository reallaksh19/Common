#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,subprocess
from pathlib import Path
from relaylib import load_yaml
from inspect_git_context import inspect as inspect_git
from takeoverlib import current_routes,route_key
from validate_baton_readiness import expected_baton_ready
from validate_takeover_certification import is_takeover_certified
from validate_drift_receipt import validate_ep as validate_drift_ep
from control_state import active_executor,override_allows,override_allows_action,resolve_execution_override


def _git(root:Path,*args)->str:
    return subprocess.check_output(["git","-C",str(root),*args],text=True,stderr=subprocess.STDOUT).strip()


def _actual_branch(root:Path,branch:str|None)->str:
    return branch or _git(root,"branch","--show-current")


def _override_basis_ok(root:Path,override_record:dict|None)->tuple[bool,list[str],dict]:
    if not override_record:
        return False,[],{}
    scope=((override_record.get("override") or {}).get("scope") or {})
    base=str(scope.get("base_sha") or "")
    try:
        head=_git(root,"rev-parse","HEAD")
        subprocess.check_call(["git","-C",str(root),"merge-base","--is-ancestor",base,head],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    except Exception:
        return False,[f"Owner override base_sha {base} is not an ancestor of current HEAD"],{"base_sha":base}
    return True,[],{"base_sha":base,"head":head}


def _override_payload(record:dict|None)->dict|None:
    if not record:return None
    override=record.get("override") or {}
    return {
        "odr_id":record.get("odr_id"),
        "odr_path":record.get("odr_path"),
        "defers":override.get("defers") or [],
        "allows":override.get("allows") or [],
        "blocks":override.get("blocks") or [],
        "pending_obligations":[x.get("id") for x in (record.get("pending") or [])],
        "scope":override.get("scope") or {},
    }


def _common_nondeferrable(state:dict,baton:bool,baton_errors:list[str])->list[str]:
    errors=[]
    if not baton:errors.append("BATON_READY is false: "+"; ".join(baton_errors[:5]))
    execution=((state.get("status_planes") or {}).get("execution") or {})
    stop=((state.get("status_planes") or {}).get("stop") or {})
    if execution.get("material_authority")!="WRITE":
        errors.append("route-level material_authority is not WRITE; Owner override does not rewrite route authority")
    if execution.get("can_continue") is not True:
        errors.append("execution.can_continue is not true")
    if stop.get("active") is True:
        errors.append(f"hard stop is active and non-overridable: {stop.get('category')}")
    return errors


def _override_result(root:Path,state:dict,candidate_id:str,actual_branch:str,control_errors:list[str],
                     control_classes:list[str],base_errors:list[str],route_key_value:str|None,
                     live:dict|None=None,git_error:str|None=None)->dict:
    override,resolve_errors=resolve_execution_override(root,state,branch=actual_branch,route_key=route_key_value)
    errors=list(base_errors)+list(resolve_errors)
    if not override:
        errors.extend(control_errors)
        if git_error:errors.append(git_error)
        return {
            "status":"FAIL","material_write_ready":False,"candidate_id":candidate_id,
            "candidate_certified":False,"route_material_authority":((state.get("status_planes") or {}).get("execution") or {}).get("material_authority"),
            "route_key":route_key_value,"git":live or {"status":"FAIL","branch":actual_branch,"error":git_error},
            "errors":errors,
        }
    if not override_allows_action(override,"BOUNDED_PRODUCT_WRITES"):
        errors.append("Owner execution override does not allow BOUNDED_PRODUCT_WRITES")
    missing=[x for x in control_classes if not override_allows(override,x)]
    if missing:errors.append("Owner execution override does not defer: "+", ".join(sorted(set(missing))))
    basis_ok,basis_errors,basis=_override_basis_ok(root,override);errors.extend(basis_errors)
    if errors or not basis_ok:
        errors.extend(control_errors)
        if git_error:errors.append(git_error)
        return {
            "status":"FAIL","material_write_ready":False,"candidate_id":candidate_id,
            "candidate_certified":False,"route_material_authority":((state.get("status_planes") or {}).get("execution") or {}).get("material_authority"),
            "route_key":route_key_value,"git":live or {"status":"FAIL","branch":actual_branch,"error":git_error},
            "owner_override":_override_payload(override),"errors":errors,
        }
    return {
        "status":"PASS_WITH_OWNER_OVERRIDE",
        "material_write_ready":True,
        "write_basis":"BOUNDED_OWNER_OVERRIDE",
        "candidate_id":candidate_id,
        "candidate_certified":False,
        "route_material_authority":((state.get("status_planes") or {}).get("execution") or {}).get("material_authority"),
        "route_key":route_key_value,
        "git":live or {"status":"OWNER_OVERRIDE_BRANCH","branch":actual_branch,"original_route_error":git_error,**basis},
        "owner_override":_override_payload(override),
        "deferred_controls":sorted(set(control_classes)),
        "pending_obligations":[x.get("id") for x in (override.get("pending") or [])],
        "claim_limitations":[
            "Deferred controls remain OPEN and are not PASS.",
            "The override blocks its declared PR_READY/MERGE/CHECKPOINT/RELEASE boundaries until the pending obligations are resolved.",
            "This result does not replace or silently modify the active execution route.",
        ],
        "errors":[],
    }


def evaluate(root:Path,candidate_id:str,branch:str|None=None,worktree:str|None=None)->dict:
    state=load_yaml(root/"agents/relay/REPO_STATE.yaml")
    baton,baton_errors=expected_baton_ready(root)
    common_errors=_common_nondeferrable(state,baton,baton_errors)
    try:
        actual_branch=_actual_branch(root,branch)
    except Exception as exc:
        return {"status":"FAIL","material_write_ready":False,"candidate_id":candidate_id,"errors":[str(exc)]}

    try:
        live=inspect_git(root,branch,worktree)
    except Exception as exc:
        message=str(exc)
        # A branch/route mismatch is the only Git-route failure deferrable by the
        # bounded Owner exception path. Drift, ancestry, and ambiguous route
        # failures remain ordinary failures.
        if "does not match active EP branch" in message:
            return _override_result(
                root,state,candidate_id,actual_branch,
                ["live route requires reconciliation before normal V2.5 writes"],
                ["ROUTE_RECONCILIATION","CANDIDATE_ADMISSION"],
                common_errors,None,live=None,git_error=message,
            )
        return {"status":"FAIL","material_write_ready":False,"candidate_id":candidate_id,"errors":common_errors+[message]}

    routes=current_routes(root,state);route=None
    for item in routes:
        if str(item.get("ep_id"))!=str(live.get("ep_id")):continue
        if item.get("mode")=="PARALLEL_LANE" and str(item.get("lane_id"))!=str(live.get("lane_id")):continue
        route=item;break
    if route is None:
        return _override_result(
            root,state,candidate_id,actual_branch,
            ["live route does not map to a current certified execution route"],
            ["ROUTE_RECONCILIATION","CANDIDATE_ADMISSION"],
            common_errors,None,live=live,
        )

    rkey=route_key(route)
    candidate_certified,cert_errors=is_takeover_certified(root,route,candidate_id)
    control_errors=[];control_classes=[]
    if not candidate_certified:
        control_errors.append("candidate admission is not certified: "+"; ".join(cert_errors[:5]))
        control_classes.append("CANDIDATE_ADMISSION")

    # When custody enforcement is enabled, certification alone is insufficient:
    # the candidate must also hold the one ACTIVE lease for this route.
    custody=state.get("execution_custody") or {}
    custody_enforced=custody.get("enforced") is True
    lease=active_executor(state,rkey) if custody_enforced else None
    custody_errors=[]
    if custody_enforced:
        if lease is None:
            custody_errors.append(f"execution custody has no unique ACTIVE executor for {rkey}")
        else:
            active_id=str((lease.get("candidate") or {}).get("agent_instance_id") or "")
            if active_id!=str(candidate_id):
                custody_errors.append(f"execution custody belongs to {active_id}, not {candidate_id}")

    normal_errors=list(common_errors)+custody_errors
    if live.get("status")=="NEEDS_DRIFT_RECEIPT":
        ep=load_yaml(root/str(route.get("ep_path")));ref=(ep.get("git_basis") or {}).get("drift_receipt")
        if not ref:normal_errors.append("live base moved and current EP has no drift receipt")
        else:
            de,_=validate_drift_ep(root,str(route.get("ep_path")),"WRITE")
            normal_errors.extend("drift: "+x for x in de)
            path=root/str(ref)
            if path.exists():
                receipt=load_yaml(path)
                if str(receipt.get("to_base"))!=str(live.get("current_base_ref")):normal_errors.append("drift receipt to_base does not match currently observed base ref")
    elif live.get("status")!="PASS":
        normal_errors.append(f"live Git context is not write-ready: {live.get('status')}")

    if not normal_errors and not control_errors:
        return {
            "status":"PASS","material_write_ready":True,"write_basis":"NORMAL_V25",
            "candidate_id":candidate_id,"candidate_certified":candidate_certified,
            "route_material_authority":((state.get("status_planes") or {}).get("execution") or {}).get("material_authority"),
            "route_key":rkey,"git":live,"execution_custody_enforced":custody_enforced,
            "active_executor":((lease.get("candidate") or {}).get("agent_instance_id") if lease else None),
            "errors":[],
        }

    # Only named control errors may be deferred. Custody, hard stops, route
    # authority, drift, and other engineering safety failures are never removed.
    if control_errors and not normal_errors:
        return _override_result(
            root,state,candidate_id,actual_branch,control_errors,control_classes,
            [],rkey,live=live,
        )

    return {
        "status":"FAIL","material_write_ready":False,"candidate_id":candidate_id,
        "candidate_certified":candidate_certified,
        "route_material_authority":((state.get("status_planes") or {}).get("execution") or {}).get("material_authority"),
        "route_key":rkey,"git":live,"execution_custody_enforced":custody_enforced,
        "active_executor":((lease.get("candidate") or {}).get("agent_instance_id") if lease else None),
        "errors":normal_errors+control_errors,
    }


def main():
    ap=argparse.ArgumentParser(description="Derive MATERIAL_WRITE_READY for one candidate on the live execution route, including bounded Owner exception truth.")
    ap.add_argument("repo_root",nargs="?",default=".");ap.add_argument("--candidate-id",required=True);ap.add_argument("--branch");ap.add_argument("--worktree");a=ap.parse_args()
    out=evaluate(Path(a.repo_root).resolve(),a.candidate_id,a.branch,a.worktree);print(json.dumps(out,indent=2));raise SystemExit(0 if out["material_write_ready"] else 1)
if __name__=="__main__":main()
