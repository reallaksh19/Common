#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from relaylib import load_yaml,print_result
from pr_correlation import (
    checkpoint_ep_id,
    covered_ep_ids,
    current_ep_ids,
    load_observations,
    nonterminal_observations,
    validate_correlation_rows,
)
from validate_delivery_observation import validate_file as validate_delivery_file


def validate(root:Path):
    e=[];w=[];state=load_yaml(root/"agents/relay/REPO_STATE.yaml");delivery=state.get("delivery")
    if not delivery or delivery.get("required") is False:return e,w

    observations=load_observations(root,state)
    if not observations:
        return ["PR delivery is required but no delivery observations are tracked"],w

    graph_path=root/"agents/relay/roadmap/ISSUE_GRAPH.yaml"
    if not graph_path.exists():return ["PR correlation requires ISSUE_GRAPH"],w
    graph=load_yaml(graph_path)
    identities=set()
    for item in observations:
        obs=item["observation"];path=root/item["path"]
        ce,cw=validate_delivery_file(path,(state.get("repository") or {}).get("remote"),(item.get("pointer") or {}).get("id"))
        e.extend(f"{item['path']}: {x}" for x in ce);w.extend(f"{item['path']}: {x}" for x in cw)
        e.extend(validate_correlation_rows(root,obs,graph))
        vehicle=obs.get("vehicle") or {};identity=(obs.get("repository"),vehicle.get("number"))
        if identity in identities:e.append(f"multiple tracked delivery observations claim the same current PR identity {identity}")
        identities.add(identity)

    active=nonterminal_observations(root,state)
    active_coverage=covered_ep_ids(active)
    expected_active=current_ep_ids(root,state)
    for ep_id in sorted(expected_active-active_coverage):
        e.append(f"active EP {ep_id} is not declared in any carried-forward non-terminal PR description")

    cp_ep=checkpoint_ep_id(root,state)
    if cp_ep:
        all_coverage=covered_ep_ids(observations)
        if cp_ep not in all_coverage:e.append(f"task-close checkpoint EP {cp_ep} is not verified in any tracked PR description correlation")

    return e,w


def main():
    ap=argparse.ArgumentParser();ap.add_argument("repo_root",nargs="?",default=".");a=ap.parse_args()
    try:e,w=validate(Path(a.repo_root).resolve())
    except Exception as exc:e,w=[str(exc)],[]
    raise SystemExit(print_result(e,w))


if __name__=="__main__":
    main()
