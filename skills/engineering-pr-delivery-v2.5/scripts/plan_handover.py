#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from handover_planning import (
    build_handover_plan,
    parse_handover_command,
    render_generator_request,
    render_issue_body,
)
from render_owner_status import render as render_owner_status


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("repo_root",nargs="?",default=".")
    ap.add_argument("--command",default="Plan for Handover")
    ap.add_argument("--owner-requirement",action="append",default=[])
    ap.add_argument("--handover-issue-url")
    ap.add_argument("--json",action="store_true")
    a=ap.parse_args()

    root=Path(a.repo_root).resolve()
    mode=parse_handover_command(a.command)
    if mode.get("status")!="READY":
        raise SystemExit(mode.get("reason") or "Invalid handover command")

    plan=build_handover_plan(
        root,
        owner_requirements=a.owner_requirement,
        complex_project=bool(mode.get("complex_project")),
        handover_issue_url=a.handover_issue_url,
    )
    if a.json:
        print(json.dumps({"owner_status":render_owner_status(root),"handover_plan":plan},indent=2,sort_keys=True))
        raise SystemExit(0 if plan.get("status")=="READY" else 2)

    print(render_owner_status(root),end="")
    print("\n# Plan for Handover\n")
    if plan.get("status")!="READY":
        for error in plan.get("errors") or ["Handover plan could not be derived."]:
            print(f"- ERROR: {error}")
        raise SystemExit(2)

    print(render_issue_body(plan),end="")
    print("\n## Handover issue publication\n")
    strategy=plan["issue_strategy"]
    print(f"- Handover key: `{'{'}strategy['handover_key']{'}'}`")
    print(f"- Reuse rule: {strategy['reuse_rule']}")
    print(f"- Preferred relation: {strategy['relationship_preference']}")
    print(f"- Fallback relation: {strategy['relationship_fallback']}")
    print("- Publish through the existing GHGEN/GHOP crash-safe GitHub projection and verify provider readback before claiming issue/link state.")

    print("\n## Three-pass generation\n")
    generator=plan["generator"]
    print(f"- Mode: {generator['mode']}")
    print(f"- Complex mode: {'ON' if generator['complex_mode'] else 'OFF'}")
    if generator["complex_mode"]:
        print("- Prompt 1 must visibly include Q1 through Q5 in natural target-specific language; total prompt count remains exactly three.")
    if generator.get("target"):
        print("\n```text")
        print(render_generator_request(plan),end="")
        print("```")
    else:
        print("- Await verified handover issue readback, then rerun with --handover-issue-url before invoking the live standalone three-pass generator.")


if __name__=="__main__":
    main()
