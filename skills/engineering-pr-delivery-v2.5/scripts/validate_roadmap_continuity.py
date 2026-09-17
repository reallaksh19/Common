#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from relaylib import compute_frontier,load_yaml,print_result,require

DISPOSITIONS={"CONTINUE_UNCHANGED","RECONCILE_REQUIRED","INVALIDATED"}
IMPACT_KEYS=("work_package_definition_changed","dependencies_changed","acceptance_changed","scope_authority_changed","protected_invariants_changed")
NONE={None,"","NONE"}

def _changed_ids(rev,key):
    items=(rev.get("changes") or {}).get(key) or []
    out=set()
    for item in items:
        if isinstance(item,dict):
            ident=item.get("id") or item.get("work_package") or item.get("node")
            if ident:out.add(str(ident))
        elif item is not None:out.add(str(item))
    return out

def validate(root:Path):
    e=[];w=[];s=load_yaml(root/"agents/relay/REPO_STATE.yaml")
    if s.get("relay_state")!="ACTIVE":return e,w
    active=s.get("active_ep") or {};ep_path=active.get("path")
    if not ep_path or not (root/ep_path).exists():return e,w
    ep=load_yaml(root/ep_path);src=ep.get("roadmap_source") or {};ep_rev=str(src.get("roadmap_revision"));cur_rev=str((s.get("roadmap") or {}).get("revision"))
    ref=active.get("continuity_receipt")
    if ep_rev==cur_rev:
        if ref not in NONE:w.append("active EP continuity_receipt is unnecessary because EP already matches current roadmap revision")
        return e,w
    if ref in NONE:return [f"active EP roadmap revision {ep_rev} != current {cur_rev}; continuity_receipt is required"],w
    path=root/str(ref)
    if not path.exists():return [f"roadmap continuity receipt does not exist: {ref}"],w
    rec=load_yaml(path);e+=require(rec,["schema_version","id","ep_id","work_package","from_revision","to_revision","revision_chain","disposition","impact_checks","basis"],"ROADMAP_CONTINUITY")
    if rec.get("schema_version")!="relay-v2.5-roadmap-continuity":e.append("ROADMAP_CONTINUITY.schema_version must be relay-v2.5-roadmap-continuity")
    if str(rec.get("ep_id"))!=str((ep.get("identity") or {}).get("ep_id")):e.append("continuity ep_id does not match active EP")
    if str(rec.get("work_package"))!=str(src.get("work_package")):e.append("continuity work_package does not match active EP")
    if str(rec.get("from_revision"))!=ep_rev:e.append("continuity from_revision must match EP roadmap revision")
    if str(rec.get("to_revision"))!=cur_rev:e.append("continuity to_revision must match current roadmap revision")
    if not isinstance(rec.get("basis"),list) or not rec.get("basis"):e.append("continuity basis must contain durable references")
    disposition=rec.get("disposition")
    if disposition not in DISPOSITIONS:e.append(f"invalid continuity disposition {disposition}")
    chain=rec.get("revision_chain") or []
    if not isinstance(chain,list) or not chain:e.append("continuity revision_chain must contain at least one revision record")
    expected=ep_rev;seen=set();wp=str(src.get("work_package"));all_unaffected=True
    for i,item in enumerate(chain):
        label=f"revision_chain[{i}]"
        if not isinstance(item,dict):e.append(f"{label} must be a mapping");continue
        e+=require(item,["path"],label);rpath=str(item.get("path","")).strip()
        if not rpath:continue
        if rpath in seen:e.append(f"continuity revision_chain repeats {rpath}");continue
        seen.add(rpath);p=root/rpath
        if not p.exists():e.append(f"{label} revision record does not exist: {rpath}");continue
        rev=load_yaml(p);info=rev.get("revision") or {};frm=str(info.get("from_revision"));to=str(info.get("to_revision"))
        if frm!=expected:e.append(f"{label} from_revision {frm} does not continue expected {expected}")
        expected=to
        changed=_changed_ids(rev,"changed");removed=_changed_ids(rev,"removed");unaffected=_changed_ids(rev,"unaffected")
        if wp in changed or wp in removed or wp not in unaffected:all_unaffected=False
    if expected!=cur_rev:e.append(f"continuity revision_chain ends at {expected}, expected current {cur_rev}")
    impact=rec.get("impact_checks") or {};e+=require(impact,IMPACT_KEYS,"ROADMAP_CONTINUITY.impact_checks")
    any_impact=any(impact.get(k) is True for k in IMPACT_KEYS)
    ex=(s.get("status_planes") or {}).get("execution") or {}
    if disposition=="CONTINUE_UNCHANGED":
        if not all_unaffected:e.append("CONTINUE_UNCHANGED requires active work package to be explicitly unaffected in every covered roadmap revision")
        if any_impact:e.append("CONTINUE_UNCHANGED requires all impact_checks false")
        if wp not in compute_frontier(load_yaml(root/s["roadmap"]["path"])):e.append("CONTINUE_UNCHANGED active work package must remain on current computed frontier")
        if active.get("state")=="RECONCILING":e.append("CONTINUE_UNCHANGED must not expose active_ep.state RECONCILING")
    elif disposition=="RECONCILE_REQUIRED":
        if active.get("state")!="RECONCILING":e.append("RECONCILE_REQUIRED requires active_ep.state RECONCILING")
        if ex.get("material_authority")!="READ_ONLY":e.append("RECONCILE_REQUIRED requires material_authority READ_ONLY")
    elif disposition=="INVALIDATED":
        e.append("INVALIDATED continuity receipt cannot remain attached to an ACTIVE EP; replace/supersede the EP and recompute routing")
    return e,w

def main():
    ap=argparse.ArgumentParser();ap.add_argument("repo_root",nargs="?",default=".");a=ap.parse_args()
    try:e,w=validate(Path(a.repo_root).resolve())
    except Exception as exc:e,w=[str(exc)],[]
    raise SystemExit(print_result(e,w))
if __name__=="__main__":main()
