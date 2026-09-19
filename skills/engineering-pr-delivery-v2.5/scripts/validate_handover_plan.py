#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from handover_planning import build_handover_plan
from relaylib import print_result


def validate(root:Path,owner_requirements:list[str]|None=None,complex_project:bool=False):
    e=[];w=[]
    plan=build_handover_plan(root,owner_requirements=owner_requirements or [],complex_project=complex_project)
    if plan.get("status")!="READY":
        return list(plan.get("errors") or ["handover plan is not READY"]),w
    if plan.get("schema_version")!="relay-v2.5-handover-plan":e.append("handover plan schema_version mismatch")
    contract=plan.get("work_contract") or {}
    if contract.get("status")!="RESOLVED":e.append("handover work contract must resolve")
    if contract.get("kind") not in {"GITHUB_ISSUE","ACTIVE_TASK","ROADMAP_WORK_PACKAGE"}:e.append("handover work contract kind invalid")

    seen=set()
    for index,item in enumerate(plan.get("intent") or []):
        label=f"handover intent[{index}]"
        iid=str(item.get("id") or "")
        if not iid:e.append(f"{label}.id must be explicit")
        elif iid in seen:e.append(f"duplicate handover intent id {iid}")
        else:seen.add(iid)
        for key in ("kind","what_remains","why_it_remains","done_when"):
            if not str(item.get(key) or "").strip():e.append(f"{label}.{key} must be explicit")
        if not isinstance(item.get("basis"),list):e.append(f"{label}.basis must be a list")

    for family in ("inputs","benchmarks"):
        for index,item in enumerate(plan.get(family) or []):
            if not str(item.get("definition_path") or "").strip():e.append(f"handover {family}[{index}] requires durable definition_path")

    incremental=plan.get("incremental") or {}
    if not isinstance(incremental.get("prior_publication_present"),bool):e.append("handover incremental.prior_publication_present must be boolean")
    for key_name in ("newly_pending","retained_pending","completed_since_prior"):
        if not isinstance(incremental.get(key_name),list):e.append(f"handover incremental.{key_name} must be list")
    if incremental.get("prior_publication_present") and not incremental.get("prior_issue_node"):e.append("handover incremental prior publication requires prior_issue_node")
    strategy=plan.get("issue_strategy") or {}
    key=str(strategy.get("handover_key") or "")
    if not key.startswith("sha256:"):e.append("handover issue strategy requires stable sha256 handover_key")
    marker=str(strategy.get("body_marker") or "")
    if key and key not in marker:e.append("handover body marker must contain stable handover key")
    if strategy.get("reuse_rule")!="UPDATE_MATCHING_OPEN_HANDOVER_ISSUE_FOR_SAME_KEY_ELSE_CREATE":e.append("handover issue reuse rule invalid")
    if strategy.get("relationship_claim")!="UNVERIFIED_UNTIL_PROVIDER_READBACK":e.append("handover relationship must remain unverified until provider readback")

    generator=plan.get("generator") or {}
    if generator.get("mode")!="THREE_PASS_ONLY":e.append("handover generator mode must remain THREE_PASS_ONLY")
    if bool(generator.get("visible_q1_q5"))!=bool(generator.get("complex_mode")):e.append("visible Q1-Q5 must track complex handover mode exactly")
    if complex_project and generator.get("complex_mode") is not True:e.append("complex project handover must enable generator complex mode")
    if not complex_project and generator.get("complex_mode") is not False:e.append("plain handover must not inherit complex mode")
    if generator.get("target_status")!="AWAITING_HANDOVER_ISSUE_READBACK":e.append("pre-publication handover plan must await verified issue readback before prompt generation")
    return e,w


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("repo_root",nargs="?",default=".")
    ap.add_argument("--owner-requirement",action="append",default=[])
    ap.add_argument("--complex-project",action="store_true")
    a=ap.parse_args()
    try:e,w=validate(Path(a.repo_root).resolve(),a.owner_requirement,a.complex_project)
    except Exception as exc:e,w=[str(exc)],[]
    raise SystemExit(print_result(e,w))


if __name__=="__main__":
    main()
