#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import yaml

REQUIRED_STAGES=(
    "source_contract",
    "declarative_schema",
    "procedural_validator",
    "report_projection",
    "communication_projection",
    "renderer",
    "regression",
)
MANIFEST="operating-model/owner-field-lineage.yaml"


def validate(skill_root:Path):
    e=[];w=[];path=skill_root/MANIFEST
    if not path.exists():return [f"missing Owner field-lineage contract: {MANIFEST}"],w
    try:data=yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as exc:return [f"Owner field-lineage YAML parse failed: {exc}"],w
    if not isinstance(data,dict):return ["Owner field-lineage top-level must be mapping"],w
    if data.get("schema_version")!="relay-v2.5-owner-field-lineage":e.append("Owner field-lineage schema_version invalid")
    stages=data.get("required_stages")
    if not isinstance(stages,list) or set(stages)!=set(REQUIRED_STAGES):e.append("Owner field-lineage required_stages must exactly declare the release lineage stages")
    fields=data.get("fields")
    if not isinstance(fields,list) or not fields:return e+["Owner field-lineage fields must be non-empty list"],w
    seen=set()
    for index,field in enumerate(fields):
        label=f"field[{index}]"
        if not isinstance(field,dict):e.append(f"{label} must be mapping");continue
        fid=str(field.get("id") or "")
        if not fid.startswith("OWNER_"):e.append(f"{label}.id must use OWNER_* namespace")
        elif fid in seen:e.append(f"duplicate Owner field-lineage id {fid}")
        seen.add(fid)
        if not str(field.get("human_need") or "").strip():e.append(f"{fid or label}.human_need must be explicit")
        if not str(field.get("authority") or "").strip():e.append(f"{fid or label}.authority must be explicit")
        stage_map=field.get("stages")
        if not isinstance(stage_map,dict):e.append(f"{fid or label}.stages must be mapping");continue
        missing=set(REQUIRED_STAGES)-set(stage_map)
        extra=set(stage_map)-set(REQUIRED_STAGES)
        if missing:e.append(f"{fid} missing lineage stages: {', '.join(sorted(missing))}")
        if extra:e.append(f"{fid} has unknown lineage stages: {', '.join(sorted(extra))}")
        for stage in REQUIRED_STAGES:
            surfaces=stage_map.get(stage)
            if not isinstance(surfaces,list) or not surfaces:
                e.append(f"{fid}.{stage} must contain at least one surface")
                continue
            for sidx,surface in enumerate(surfaces):
                sl=f"{fid}.{stage}[{sidx}]"
                if not isinstance(surface,dict):e.append(f"{sl} must be mapping");continue
                rel=surface.get("path");tokens=surface.get("tokens")
                if not str(rel or "").strip():e.append(f"{sl}.path must be explicit");continue
                target=skill_root/str(rel)
                if not target.exists():
                    e.append(f"{sl} missing surface {rel}")
                    continue
                if not isinstance(tokens,list) or not tokens:
                    e.append(f"{sl}.tokens must be non-empty list")
                    continue
                text=target.read_text(encoding="utf-8")
                for token in tokens:
                    if not str(token or ""):e.append(f"{sl} contains empty token")
                    elif str(token) not in text:e.append(f"{fid}: {stage} surface {rel} missing required token: {token}")
    if len(fields)<10:w.append("Owner field-lineage contract covers fewer than 10 critical data families")
    return e,w


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("skill_root",nargs="?",default=str(Path(__file__).resolve().parents[1]))
    a=ap.parse_args();e,w=validate(Path(a.skill_root).resolve())
    for item in w:print(f"WARNING: {item}")
    for item in e:print(f"ERROR: {item}")
    if e:
        print(f"FAIL: {len(e)} error(s), {len(w)} warning(s)")
        raise SystemExit(1)
    print(f"PASS: Owner field-lineage contract; {len(w)} warning(s)")


if __name__=="__main__":
    main()
