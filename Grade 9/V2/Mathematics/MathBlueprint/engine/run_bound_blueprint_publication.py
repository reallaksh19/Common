#!/usr/bin/env python3
"""Regenerate the bound Mathematics learner product strictly from Blueprint logic."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def fail(code: str, detail: str = "") -> None:
    raise ValueError(f"{code}:{detail}" if detail else code)


def run(script: Path, args: list[str]) -> None:
    proc = subprocess.run([sys.executable, str(script), *args], text=True, capture_output=True)
    if proc.returncode != 0:
        raise RuntimeError(f"BOUND_BLUEPRINT_PUBLICATION_FAILED:{script.name}\nSTDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--bound-dir", required=True)
    args = ap.parse_args()
    root = Path(args.bound_dir)
    gate = load(root / "release" / "product_release_gate.json")
    if gate.get("status") != "PASS":
        fail("BOUND_BLUEPRINT_PUBLICATION_REQUIRES_RELEASE_PASS")

    example_catalog = root / "core1a" / "core1a_governed_example_catalog.json"
    if not example_catalog.exists():
        fail("BOUND_BLUEPRINT_PUBLICATION_GOVERNED_EXAMPLE_CATALOG_REQUIRED")

    out = root / "publication"
    out.mkdir(parents=True, exist_ok=True)
    bp = out / "learner_page_blueprint.json"
    bp_audit = out / "learner_page_blueprint_audit.json"
    pdf = out / "blueprint_regenerated_learner_product.pdf"
    pdf_audit = out / "blueprint_pdf_audit.json"

    run(HERE / "compile_governed_product_page_blueprint.py", [
        "--bucket-plan", str(root / "core1a" / "core1a_bucket_plan.json"),
        "--core1a-manuscript", str(root / "core1a" / "core1a_textbook_manuscript.json"),
        "--core1a-example-catalog", str(example_catalog),
        "--core1b-dir", str(root / "core1b"),
        "--core2a-blueprint", str(root / "core2a" / "core2a_product_blueprint.json"),
        "--core2b-plan", str(root / "core2b" / "plan.json"),
        "--generation-spec", str(root / "inputs" / "generation_spec.json"),
        "--out", str(bp),
    ])
    run(HERE / "validate_content_complete_page_blueprint.py", ["--input", str(bp), "--audit-out", str(bp_audit)])
    run(HERE / "render_content_complete_blueprint_pdf.py", ["--input", str(bp), "--out", str(pdf), "--audit-out", str(pdf_audit)])

    bpa = load(bp_audit); pda = load(pdf_audit)
    if bpa.get("status") != "PASS" or pda.get("status") != "PASS":
        fail("BOUND_BLUEPRINT_PUBLICATION_AUDIT_FAILED")
    if bpa.get("blueprint_sha256") != pda.get("blueprint_sha256"):
        fail("BOUND_BLUEPRINT_PUBLICATION_DIGEST_DRIFT")
    if set(bpa.get("render_object_ids") or []) != set(pda.get("rendered_object_ids") or []):
        fail("BOUND_BLUEPRINT_PUBLICATION_RENDER_COVERAGE_DRIFT")
    if pda.get("semantic_source") != "LEARNER_PAGE_BLUEPRINT_ONLY":
        fail("BOUND_BLUEPRINT_PUBLICATION_SOURCE_DRIFT")

    summary = {
        "status": "PASS",
        "source_release_gate": "PASS",
        "blueprint_id": bpa["blueprint_id"],
        "blueprint_sha256": bpa["blueprint_sha256"],
        "difficulty_badge": load(bp)["difficulty_badge"],
        "governed_example_catalog_digest": load(example_catalog)["catalog_digest"],
        "blueprint_page_count": bpa["page_count"],
        "render_object_count": bpa["render_object_count"],
        "pdf_sha256": pda["pdf_sha256"],
        "pdf_size_bytes": pda["pdf_size_bytes"],
        "semantic_source": pda["semantic_source"],
        "paths": {
            "blueprint": bp.name,
            "blueprint_audit": bp_audit.name,
            "pdf": pdf.name,
            "pdf_audit": pdf_audit.name,
            "governed_example_catalog": "../core1a/core1a_governed_example_catalog.json",
        },
    }
    (out / "blueprint_publication_summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
