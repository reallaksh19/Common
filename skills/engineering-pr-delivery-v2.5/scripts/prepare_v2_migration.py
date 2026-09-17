#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
import yaml
from relaylib import load_yaml


def build(inventory:dict,inventory_ref:str)->dict:
    if inventory.get("schema_version")!="relay-v2.5-migration-inventory":raise ValueError("inventory schema_version must be relay-v2.5-migration-inventory")
    if inventory.get("source_protocol")!="engineering-pr-delivery-v2":raise ValueError("inventory source_protocol must be engineering-pr-delivery-v2")
    categories=inventory.get("categories") or {}
    return {
        "schema_version":"relay-v2.5-migration-reconciliation",
        "status":"NEEDS_RECONCILIATION",
        "source_inventory":inventory_ref,
        "source_evidence":{name:list(paths or []) for name,paths in categories.items()},
        "owner_intent":{"authoritative_sources":[],"unresolved_questions":[]},
        "roadmap_mapping":{"objectives":[],"phases":[],"work_packages":[]},
        "current_position":{"objective":None,"phase":None,"work_package":None},
        "durable_inputs":[],"benchmarks":[],
        "history_to_preserve":{"checkpoints":[],"evidence":[],"decisions":[]},
        "unresolved_work":[],
        "first_v25_ep":{"create_only_after":["owner intent reconciled","current roadmap revision established","executable frontier computed","scope and acceptance made self-contained","cold-start inputs complete"],"ep_id":None},
        "notes":["Legacy files are evidence/context only; no V2 endpoint is automatically executable as V2.5.","Progress must be recalculated from an explicit V2.5 basis rather than copied from narrative history."],
    }


def main():
    ap=argparse.ArgumentParser(description="Prepare a repository-neutral V2→V2.5 reconciliation worksheet from a V2 inventory. No semantic migration is inferred.")
    ap.add_argument("inventory");ap.add_argument("--output")
    a=ap.parse_args();path=Path(a.inventory).resolve();data=build(load_yaml(path),a.inventory);text=yaml.safe_dump(data,sort_keys=False)
    if a.output:
        out=Path(a.output).resolve()
        if out.exists():raise FileExistsError(f"refusing to overwrite existing migration reconciliation: {out}")
        out.parent.mkdir(parents=True,exist_ok=True);out.write_text(text,encoding="utf-8");print(f"WROTE {out}")
    else:print(text,end="")

if __name__=="__main__":main()
