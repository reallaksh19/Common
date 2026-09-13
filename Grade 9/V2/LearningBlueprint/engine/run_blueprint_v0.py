from __future__ import annotations

import argparse
from pathlib import Path

from apply_owner_override import apply_owner_override
from common import digest, load_json, write_json
from freeze_ground_truth import freeze_ground_truth
from route_evidence import route_evidence


def execute(ground_truth_path: str, routing_input_path: str, out_dir: str, override_path: str | None = None) -> dict:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    ground_truth = load_json(ground_truth_path)
    routing_input = load_json(routing_input_path)
    frozen = freeze_ground_truth(ground_truth)
    route = route_evidence(ground_truth, routing_input)
    if override_path:
        route = apply_owner_override(route, load_json(override_path))

    write_json(out / "frozen_ground_truth.json", frozen)
    write_json(out / "route_packet.json", route)
    manifest = {
        "blueprint_stage": "V0_EVIDENCE_AND_ROUTING",
        "ground_truth_manifest_id": ground_truth["manifest_id"],
        "ground_truth_digest": frozen["manifest_digest"],
        "route_packet_id": route["packet_id"],
        "route_packet_digest": route["digest"],
        "system_decision": route["system_decision"],
        "final_decision": route["final_decision"],
        "execution_blocked": route["execution_blocked"],
        "next_milestone": "V1_INDEPENDENT_CORE1_CORE2_AND_JOIN"
    }
    manifest["manifest_digest"] = digest(manifest)
    write_json(out / "blueprint_v0_manifest.json", manifest)
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Learning Blueprint v0 evidence freeze and adaptive routing")
    parser.add_argument("--ground-truth", required=True)
    parser.add_argument("--routing-input", required=True)
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--override")
    args = parser.parse_args()
    execute(args.ground_truth, args.routing_input, args.out_dir, args.override)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
