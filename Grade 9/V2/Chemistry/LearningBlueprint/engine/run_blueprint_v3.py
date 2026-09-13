from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from common import digest, load_json, write_json
from compile_transfer_eligibility import compile_transfer_eligibility


def run_v3(
    assimilation: dict[str, Any],
    taught_state: dict[str, Any],
    envelope: dict[str, Any],
    request: dict[str, Any],
) -> dict[str, Any]:
    transfer = compile_transfer_eligibility(assimilation, taught_state, envelope, request)
    manifest = {
        "blueprint_version": "v3",
        "assimilation_ref": assimilation["packet_id"],
        "taught_state_ref": taught_state["packet_id"],
        "transfer_envelope_ref": envelope["envelope_id"],
        "transfer_eligibility_ref": transfer["packet_id"],
        "eligible_item_count": len(transfer["eligible_item_ids"]),
        "blocked_item_count": len(transfer["blocked_item_ids"]),
        "status": (
            "PASS_TRANSFER_ITEMS_RELEASED"
            if transfer["eligible_item_ids"]
            else "PASS_NO_TRANSFER_ITEMS_RELEASED"
        ),
    }
    manifest["digest"] = digest(manifest)
    return {"transfer_eligibility": transfer, "manifest": manifest}


def main() -> int:
    parser = argparse.ArgumentParser(description="Compile Chemistry Learning Blueprint v3 Core2A transfer eligibility")
    parser.add_argument("--assimilation", required=True)
    parser.add_argument("--taught", required=True)
    parser.add_argument("--envelope", required=True)
    parser.add_argument("--request", required=True)
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()
    result = run_v3(
        load_json(args.assimilation),
        load_json(args.taught),
        load_json(args.envelope),
        load_json(args.request),
    )
    out = Path(args.out_dir)
    write_json(out / "transfer_eligibility.json", result["transfer_eligibility"])
    write_json(out / "manifest.json", result["manifest"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
