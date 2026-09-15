#!/usr/bin/env python3
"""Regenerate the bound Mathematics learner product strictly from Blueprint bundle logic."""
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


def _research_manifest(root: Path) -> Path | None:
    candidates = [
        root / "inputs" / "pedagogy_research_manifest.json",
        root / "inputs" / "pedagogy_research_manifest.test.json",
    ]
    existing = [path for path in candidates if path.exists()]
    if len(existing) > 1:
        fail("BOUND_BLUEPRINT_PUBLICATION_RESEARCH_MANIFEST_AMBIGUOUS")
    return existing[0] if existing else None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--bound-dir", required=True)
    args = ap.parse_args()
    root = Path(args.bound_dir)
    gate_path = root / "release" / "product_release_gate.json"
    gate = load(gate_path)
    if gate.get("status") != "PASS":
        fail("BOUND_BLUEPRINT_PUBLICATION_REQUIRES_RELEASE_PASS")

    example_catalog = root / "core1a" / "core1a_governed_example_catalog.json"
    generation_spec = root / "inputs" / "generation_spec.json"
    research_manifest = _research_manifest(root)
    research_args = ["--pedagogy-research-manifest", str(research_manifest)] if research_manifest else []
    if not example_catalog.exists():
        fail("BOUND_BLUEPRINT_PUBLICATION_GOVERNED_EXAMPLE_CATALOG_REQUIRED")

    out = root / "publication"
    out.mkdir(parents=True, exist_ok=True)
    bundle = out / "learner_publication_bundle.json"
    bundle_audit = out / "learner_publication_bundle_audit.json"
    pdf = out / "blueprint_regenerated_learner_product.pdf"
    pdf_audit = out / "blueprint_pdf_audit.json"

    run(HERE / "compile_publication_bundle.py", [
        "--bucket-plan", str(root / "core1a" / "core1a_bucket_plan.json"),
        "--core1a-manuscript", str(root / "core1a" / "core1a_textbook_manuscript.json"),
        "--core1a-example-catalog", str(example_catalog),
        "--core1b-dir", str(root / "core1b"),
        "--core2a-blueprint", str(root / "core2a" / "core2a_product_blueprint.json"),
        "--core2b-plan", str(root / "core2b" / "plan.json"),
        "--generation-spec", str(generation_spec),
        *research_args,
        "--release-gate", str(gate_path),
        "--out", str(bundle),
    ])
    run(HERE / "validate_publication_bundle.py", [
        "--input", str(bundle), "--release-gate", str(gate_path),
        "--generation-spec", str(generation_spec),
        "--core1a-example-catalog", str(example_catalog),
        *research_args,
        "--audit-out", str(bundle_audit),
    ])
    run(HERE / "render_publication_bundle_pdf.py", [
        "--input", str(bundle), "--release-gate", str(gate_path),
        "--generation-spec", str(generation_spec),
        "--core1a-example-catalog", str(example_catalog),
        *research_args,
        "--out", str(pdf), "--audit-out", str(pdf_audit),
    ])

    bpa = load(bundle_audit); pda = load(pdf_audit); bundle_doc = load(bundle)
    if bpa.get("status") != "PASS" or pda.get("status") != "PASS":
        fail("BOUND_BLUEPRINT_PUBLICATION_AUDIT_FAILED")
    if bpa.get("bundle_sha256") != pda.get("bundle_sha256"):
        fail("BOUND_BLUEPRINT_PUBLICATION_DIGEST_DRIFT")
    if set(bpa.get("render_object_ids") or []) != set(pda.get("rendered_object_ids") or []):
        fail("BOUND_BLUEPRINT_PUBLICATION_RENDER_COVERAGE_DRIFT")
    if pda.get("semantic_source") != "LEARNER_PUBLICATION_BUNDLE_ONLY":
        fail("BOUND_BLUEPRINT_PUBLICATION_SOURCE_DRIFT")
    if bpa.get("research_manifest_bound") != pda.get("research_manifest_bound"):
        fail("BOUND_BLUEPRINT_PUBLICATION_RESEARCH_CUSTODY_DRIFT")

    summary = {
        "status": "PASS",
        "source_release_gate": "PASS",
        "bundle_id": bpa["bundle_id"],
        "bundle_sha256": bpa["bundle_sha256"],
        "concept_component_count": bpa["concept_component_count"],
        "difficulty_badge_counts": bpa["difficulty_badge_counts"],
        "governed_example_catalog_digest": bundle_doc["governed_example_catalog_digest"],
        "pedagogy_research_manifest_digest": bundle_doc["pedagogy_research_manifest_digest"],
        "research_manifest_bound": bpa["research_manifest_bound"],
        "semantic_page_count": pda["semantic_page_count"],
        "render_object_count": bpa["render_object_count"],
        "pdf_sha256": pda["pdf_sha256"],
        "pdf_size_bytes": pda["pdf_size_bytes"],
        "semantic_source": pda["semantic_source"],
        "paths": {
            "bundle": bundle.name,
            "bundle_audit": bundle_audit.name,
            "pdf": pdf.name,
            "pdf_audit": pdf_audit.name,
            "governed_example_catalog": "../core1a/core1a_governed_example_catalog.json",
            "pedagogy_research_manifest": str(research_manifest.relative_to(root)) if research_manifest else None,
        },
    }
    (out / "blueprint_publication_summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
