#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve()
LP_ROOT = HERE.parents[1]
CHEM_ROOT = LP_ROOT.parent
sys.path.insert(0, str(CHEM_ROOT / "LearningBlueprint" / "engine"))
sys.path.insert(0, str(CHEM_ROOT / "ExactProduct" / "engine"))

from chemistry_electron_transfer_primitive import install as install_electron_transfer_primitive  # noqa: E402
from chemistry_runtime_fact_parameter_bridge import install as install_runtime_fact_parameter_bridge  # noqa: E402

# Additive C-H runtime capability. These installs provide renderer capability and
# governed parameter consumption only; they never select a primitive or author
# scientific facts. Selection/facts remain upstream governed representation authority.
install_electron_transfer_primitive()
install_runtime_fact_parameter_bridge()

from compile_chemistry_core_authority import digest as semantic_digest  # noqa: E402
from compile_chemistry_core_product_custody import digest_without  # noqa: E402
from render_chemistry_core1a_review import render_core1a_content_first  # noqa: E402
from render_chemistry_a_content_first import render_core2a_content_first  # noqa: E402
from render_chemistry_static_b_product import render_static_b_product  # noqa: E402
from preflight_chemistry_core_product import run_core_product_preflight  # noqa: E402


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def canonical(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(obj: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical(obj).encode("utf-8")).hexdigest()


def file_digest(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def run_core_product(
    custody: dict[str, Any],
    authority: dict[str, Any],
    payload: dict[str, Any],
    out_dir: Path,
) -> tuple[dict[str, Any], dict[str, Any]]:
    if custody.get("status") != "CORE_PRODUCT_CUSTODY_READY":
        raise ValueError("CHEM_CORE_RUN_CUSTODY_NOT_READY")
    if authority.get("status") != "CORE_AUTHORITY_READY":
        raise ValueError("CHEM_CORE_RUN_AUTHORITY_NOT_READY")
    if custody["core_authority_id"] != authority["authority_id"] or custody["core_authority_digest"] != authority["authority_digest"]:
        raise ValueError("CHEM_CORE_RUN_AUTHORITY_CUSTODY_DRIFT")
    if custody["custody_digest"] != digest_without(custody, "custody_digest"):
        raise ValueError("CHEM_CORE_RUN_CUSTODY_DIGEST_MISMATCH")
    if authority["payload_digest"] != semantic_digest(payload):
        raise ValueError("CHEM_CORE_RUN_PAYLOAD_DIGEST_MISMATCH")
    mode = authority["product_mode"]
    if custody["product_mode"] != mode:
        raise ValueError("CHEM_CORE_RUN_MODE_DRIFT")

    out_dir.mkdir(parents=True, exist_ok=True)
    policy = load(LP_ROOT / "policies" / "chemistry-learner-render-policy.json")
    policy_digest = digest(policy)
    pdf_path = out_dir / f"chemistry_{mode.lower()}.pdf"

    if mode == "CORE1A":
        metrics = render_core1a_content_first(payload["manuscript"], payload["representation_bundle"], policy, pdf_path)
    elif mode == "CORE2A":
        metrics = render_core2a_content_first(payload.get("source_plan"), payload.get("challenge_plan"), payload["representation_bundle"], policy, pdf_path)
    elif mode in {"CORE1B", "CORE2B"}:
        metrics = render_static_b_product(mode, payload, policy, pdf_path)
    else:
        raise ValueError("CHEM_CORE_RUN_MODE_INVALID")

    artifact = {
        "path": pdf_path.name,
        "page_count": int(metrics["page_count"]),
        "pdf_sha256": file_digest(pdf_path),
        "bytes": pdf_path.stat().st_size,
    }
    render_manifest = {
        "schema_version": "1.0.0",
        "render_id": custody["custody_id"].replace("CHEM-CORE-CUSTODY-", "CHEM-CORE-RENDER-", 1),
        "product_mode": mode,
        "subtopic_id": custody["subtopic_id"],
        "custody_id": custody["custody_id"],
        "custody_digest": custody["custody_digest"],
        "core_authority_id": authority["authority_id"],
        "core_authority_digest": authority["authority_digest"],
        "render_policy_ref": policy["policy_id"],
        "render_policy_digest": policy_digest,
        "artifact": artifact,
        "renderer_metrics": metrics,
        "status": "RENDERED_NOT_PREFLIGHTED",
        "render_digest": "",
    }
    render_manifest["render_digest"] = digest({k: v for k, v in render_manifest.items() if k != "render_digest"})
    (out_dir / "core_product_render_manifest.json").write_text(json.dumps(render_manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    preflight = run_core_product_preflight(render_manifest, custody, authority, out_dir)
    (out_dir / "core_product_preflight.json").write_text(json.dumps(preflight, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return render_manifest, preflight


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--custody", type=Path, required=True)
    parser.add_argument("--authority", type=Path, required=True)
    parser.add_argument("--payload", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    args = parser.parse_args()
    render_manifest, preflight = run_core_product(load(args.custody), load(args.authority), load(args.payload), args.out_dir)
    print(json.dumps({"render": render_manifest, "preflight": preflight}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
