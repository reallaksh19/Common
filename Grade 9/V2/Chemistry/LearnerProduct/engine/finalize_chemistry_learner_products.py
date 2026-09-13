#!/usr/bin/env python3
"""C-LP-24/C-LP-25 machine final audit and durable handoff custody."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any


def load(path: Path | str) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def canonical(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(obj: Any) -> str:
    return hashlib.sha256(canonical(obj).encode("utf-8")).hexdigest()


def sha_file(path: Path | str) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def finalize(semantic_package: dict[str, Any], answer_audit: dict[str, Any], render_manifest: dict[str, Any], preflight: dict[str, Any], render_dir: Path, out_dir: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    if semantic_package.get("semantic_complete_through") != "VALIDATE_ANSWER_CLOSURE":
        raise ValueError("CHEM_LP_FINAL_AUDIT_SEMANTIC_INCOMPLETE")
    if answer_audit.get("status") != "PASS":
        raise ValueError("CHEM_LP_FINAL_AUDIT_ANSWER_CLOSURE_FAILED")
    if preflight.get("status") != "PASS":
        raise ValueError("CHEM_LP_FINAL_AUDIT_VISUAL_PREFLIGHT_FAILED")
    if preflight.get("render_manifest_ref") != render_manifest.get("manifest_id") or preflight.get("render_manifest_digest") != render_manifest.get("manifest_digest"):
        raise ValueError("CHEM_LP_FINAL_AUDIT_RENDER_BINDING_MISMATCH")

    artifacts = []
    for key in ("core1a", "core2a"):
        metrics = render_manifest[key]
        path = render_dir / metrics["pdf"]
        if not path.exists():
            raise ValueError("CHEM_LP_FINAL_AUDIT_ARTIFACT_MISSING:" + metrics["pdf"])
        actual = sha_file(path)
        if actual != metrics["pdf_sha256"]:
            raise ValueError("CHEM_LP_FINAL_AUDIT_ARTIFACT_HASH_MISMATCH:" + metrics["pdf"])
        artifacts.append({
            "product": metrics["product"],
            "filename": metrics["pdf"],
            "sha256": actual,
            "bytes": path.stat().st_size,
            "page_count": metrics["page_count"],
            "minimum_visible_font_pt": metrics["minimum_visible_font_pt"],
        })

    counts = answer_audit["counts"]
    if counts["objective_questions_total"] != counts["quick_checks_total"] or counts["objective_questions_total"] != counts["full_workings_total"]:
        raise ValueError("CHEM_LP_FINAL_AUDIT_OBJECTIVE_ANSWER_CLOSURE_DRIFT")
    if counts["open_questions_total"] != counts["expected_response_rubrics_total"]:
        raise ValueError("CHEM_LP_FINAL_AUDIT_OPEN_ANSWER_CLOSURE_DRIFT")

    final_audit = {
        "audit_id": "CHEM-LP-FINAL-" + semantic_package["package_id"].split("-")[-1],
        "schema_version": "1.0.0",
        "subject": "CHEMISTRY",
        "semantic_package_ref": semantic_package["package_id"],
        "semantic_package_digest": semantic_package["package_digest"],
        "answer_closure_audit_ref": answer_audit["audit_id"],
        "answer_closure_audit_digest": answer_audit["audit_digest"],
        "render_manifest_ref": render_manifest["manifest_id"],
        "render_manifest_digest": render_manifest["manifest_digest"],
        "visual_preflight_ref": preflight["preflight_id"],
        "visual_preflight_digest": preflight["preflight_digest"],
        "artifacts": artifacts,
        "machine_gates": {
            "semantic_chain_through_C_LP_21": "PASS",
            "answer_closure": "PASS",
            "pdf_realization": "PASS",
            "font_floor": "PASS",
            "page_geometry": "PASS",
            "clipping_overlap": "PASS",
            "internal_identifier_leak": "PASS",
            "reasoning_visual_closure": "PASS",
            "raster_proof": "PASS"
        },
        "human_gates": {
            "subject_correctness": "PENDING",
            "pedagogical_design": "PENDING",
            "assessment_design": "PENDING",
            "visual_usability": "PENDING",
            "mature_design_quality": "PENDING"
        },
        "machine_status": "PASS",
        "release_authorized": False,
        "release_boundary": "Machine publication engineering passed. Human subject/pedagogy/assessment/visual/mature-design approval is still required.",
        "audit_digest": ""
    }
    payload = copy.deepcopy(final_audit)
    payload.pop("audit_digest")
    final_audit["audit_digest"] = digest(payload)

    handoff = {
        "handoff_id": "CHEM-LP-HANDOFF-" + semantic_package["package_id"].split("-")[-1],
        "schema_version": "1.0.0",
        "subject": "CHEMISTRY",
        "status": "MACHINE_COMPLETE_HUMAN_REVIEW_PENDING",
        "semantic_package_ref": semantic_package["package_id"],
        "semantic_package_digest": semantic_package["package_digest"],
        "final_audit_ref": final_audit["audit_id"],
        "final_audit_digest": final_audit["audit_digest"],
        "artifacts": artifacts,
        "reusable_files": [
            "core1a_bucket_plan.json",
            "core1a_build_state.json",
            "core1a_manuscript.json",
            "core2a_source_plan.json",
            "core2a_challenge_plan.json",
            "answer_closure_audit.json",
            "render_manifest.json",
            "visual_preflight.json",
            "final_audit.json",
            "chemistry_core1a.pdf",
            "chemistry_core2a.pdf"
        ],
        "next_required_action": "Authorized human subject, pedagogy, assessment and actual-size visual review. Do not claim release maturity before those gates are granted.",
        "handoff_digest": ""
    }
    payload = copy.deepcopy(handoff)
    payload.pop("handoff_digest")
    handoff["handoff_digest"] = digest(payload)

    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "final_audit.json").write_text(json.dumps(final_audit, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (out_dir / "handoff_manifest.json").write_text(json.dumps(handoff, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return final_audit, handoff


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--semantic-package", required=True)
    parser.add_argument("--answer-audit", required=True)
    parser.add_argument("--render-manifest", required=True)
    parser.add_argument("--visual-preflight", required=True)
    parser.add_argument("--render-dir", required=True)
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()
    finalize(
        load(args.semantic_package), load(args.answer_audit), load(args.render_manifest), load(args.visual_preflight),
        Path(args.render_dir), Path(args.out_dir)
    )


if __name__ == "__main__":
    main()
