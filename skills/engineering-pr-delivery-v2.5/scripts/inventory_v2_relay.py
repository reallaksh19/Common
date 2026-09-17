#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
import yaml

PATTERNS={
    "active_chain_state":"agents/chains/*/ACTIVE.md",
    "issue_basis":"agents/chains/*/issue-basis/*.md",
    "issue_current":"agents/chains/*/issue-state/CURRENT.md",
    "endpoints":"agents/chains/*/endpoints/*.md",
    "material_legs":"agents/chains/*/material-legs/**/*",
    "qualifications":"agents/chains/*/qualifications/**/*",
}

def _files(root:Path,pattern:str)->list[str]:
    out=[]
    for path in root.glob(pattern):
        if path.is_file():out.append(path.relative_to(root).as_posix())
    return sorted(set(out))

def build_inventory(root:Path)->dict:
    categories={name:_files(root,pattern) for name,pattern in PATTERNS.items()}
    return {
        "schema_version":"relay-v2.5-migration-inventory",
        "source_protocol":"engineering-pr-delivery-v2",
        "source_root":".",
        "categories":categories,
        "counts":{name:len(paths) for name,paths in categories.items()},
        "migration_rules":[
            "Inventory is evidence discovery only; no listed artifact is automatically authoritative V2.5 state.",
            "A V2 endpoint may seed history/context but is never automatically promoted to a V2.5 EP.",
            "Owner intent, roadmap topology, current frontier, acceptance, progress basis, and successor readiness must be reconciled explicitly.",
            "Do not copy narrative progress percentages into V2.5 calculated progress.",
        ],
    }

def main():
    ap=argparse.ArgumentParser(description="Inventory generic V2 relay artifacts without interpreting or mutating them.")
    ap.add_argument("repo_root",nargs="?",default=".");ap.add_argument("--output")
    a=ap.parse_args();root=Path(a.repo_root).resolve();data=build_inventory(root);text=yaml.safe_dump(data,sort_keys=False)
    if a.output:
        out=Path(a.output).resolve();out.parent.mkdir(parents=True,exist_ok=True);out.write_text(text,encoding="utf-8");print(f"WROTE {out}")
    else:print(text,end="")

if __name__=="__main__":main()
