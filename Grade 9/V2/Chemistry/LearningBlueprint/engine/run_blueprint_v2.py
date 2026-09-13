from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from common import digest, load_json, write_json
from compile_learner_state import compile_learner_state
from compile_purpose import compile_purpose
from compile_assimilation import compile_assimilation
from compile_taught_state import compile_taught_state


def run_v2(join: dict[str, Any], learner_input: dict[str, Any], purpose_input: dict[str, Any], design_input: dict[str, Any], realization: dict[str, Any] | None = None) -> dict[str, Any]:
    learner_state = compile_learner_state(join, learner_input)
    purpose = compile_purpose(purpose_input)
    assimilation = compile_assimilation(join, learner_state, purpose, design_input)
    taught = compile_taught_state(assimilation, realization) if realization is not None else None
    manifest = {
        "blueprint_version": "v2",
        "join_packet_ref": join["packet_id"],
        "learner_state_ref": learner_state["packet_id"],
        "purpose_ref": purpose["packet_id"],
        "assimilation_ref": assimilation["packet_id"],
        "taught_state_ref": taught["packet_id"] if taught else None,
        "status": "PASS_TAUGHT_STATE_RECORDED" if taught else "PASS_ASSIMILATION_READY_AWAITING_REALIZATION"
    }
    manifest["digest"] = digest(manifest)
    return {"learner_state": learner_state, "purpose": purpose, "assimilation": assimilation, "taught_state": taught, "manifest": manifest}


def main() -> int:
    parser = argparse.ArgumentParser(description="Compile Chemistry Learning Blueprint v2 assimilation reasoning")
    parser.add_argument("--join", required=True)
    parser.add_argument("--learner", required=True)
    parser.add_argument("--purpose", required=True)
    parser.add_argument("--design", required=True)
    parser.add_argument("--realization")
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()
    result = run_v2(load_json(args.join), load_json(args.learner), load_json(args.purpose), load_json(args.design), load_json(args.realization) if args.realization else None)
    out = Path(args.out_dir)
    write_json(out / "learner_state.json", result["learner_state"])
    write_json(out / "purpose.json", result["purpose"])
    write_json(out / "assimilation.json", result["assimilation"])
    if result["taught_state"] is not None:
        write_json(out / "taught_state.json", result["taught_state"])
    write_json(out / "manifest.json", result["manifest"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
