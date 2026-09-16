#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GATE_FILES = [
    "engineering-gates/vectors/PHY-VEC-BASICS.v3.json",
    "engineering-gates/vectors/PHY-VEC-ADD-SUB.v3.json",
    "engineering-gates/vectors/PHY-VEC-COMPONENTS.v3.json",
    "engineering-gates/newtonian-mechanics/PHY-NLM-INTERACTION.v3.json",
    "engineering-gates/newtonian-mechanics/PHY-NLM-FBD.v3.json",
    "engineering-gates/newtonian-mechanics/PHY-NLM-FIRST-LAW.v3.json",
    "engineering-gates/newtonian-mechanics/PHY-NLM-SECOND-LAW.v3.json",
    "engineering-gates/newtonian-mechanics/PHY-NLM-THIRD-LAW.v3.json",
    "engineering-gates/newtonian-mechanics/PHY-NLM-NORMAL.v3.json",
    "engineering-gates/newtonian-mechanics/PHY-NLM-TENSION.v3.json",
    "engineering-gates/newtonian-mechanics/PHY-NLM-FRICTION.v3.json",
    "engineering-gates/newtonian-mechanics/PHY-NLM-CONNECTED.v3.json",
    "engineering-gates/gravitation/PHY-GRAV-FORCE.v3.json",
    "engineering-gates/gravitation/PHY-GRAV-FIELD.v3.json",
    "engineering-gates/motion-in-2d/PHY-M2D-PROJECTILE-COMPONENTS.v3.json",
    "engineering-gates/motion-in-2d/PHY-M2D-SHARED-CLOCK.v3.json",
    "engineering-gates/motion-in-2d/PHY-M2D-VELOCITY-EVOLUTION.v3.json",
    "engineering-gates/motion-in-2d/PHY-M2D-VELOCITY-DIRECTION.v3.json",
    "engineering-gates/motion-in-2d/PHY-M2D-SPEED-MAGNITUDE.v3.json",
    "engineering-gates/motion-in-2d/PHY-M2D-SAME-HEIGHT-VELOCITY.v3.json",
    "engineering-gates/motion-in-2d/PHY-M2D-PERPENDICULAR-VELOCITY.v3.json",
    "engineering-gates/motion-in-2d/PHY-M2D-SPEED-AT-HEIGHT.v3.json",
    "engineering-gates/motion-in-2d/PHY-M2D-RELATIVE-VELOCITY.v3.json",
    "engineering-gates/motion-in-2d/PHY-M2D-MOVING-LAUNCHER.v3.json",
    "engineering-gates/work-energy/PHY-WORK-ENERGY-POWER.v3.json",
    "engineering-gates/work-energy/PHY-ENERGY-CONSERVATION-LAW.v3.json",
]


def load(rel: str) -> dict:
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(value: object) -> str:
    return "sha256:" + hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def build_registry() -> dict:
    gates = [load(path) for path in GATE_FILES]
    if len({gate["subtopic_id"] for gate in gates}) != len(gates):
        raise ValueError("PHY_GATE_DUPLICATE_ID: duplicate subtopic_id in v3 gate source set")
    return {"schema_version":"3.0.0","registry_id":"PHYSICS-TECHNICAL-ENGINEERING-GATES-V3","maturity":"ENGINEERING","gates":gates}


def main() -> None:
    ap = argparse.ArgumentParser(description="Build the deterministic canonical Physics Technical Engineering Gate v3 registry")
    ap.add_argument("--out")
    args = ap.parse_args()
    registry = build_registry()
    rendered = json.dumps(registry, indent=2, ensure_ascii=False) + "\n"
    if args.out:
        out = Path(args.out); out.parent.mkdir(parents=True, exist_ok=True); out.write_text(rendered, encoding="utf-8")
    print(json.dumps({"status":"BUILT","registry_id":registry["registry_id"],"gate_count":len(registry["gates"]),"gate_ids":[g["subtopic_id"] for g in registry["gates"]],"registry_digest":digest(registry)}, indent=2))


if __name__ == "__main__": main()
