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
    engineering_admission = root / "inputs" / "engineering_domain_admission.json"
    research_manifest = _research_manifest(root)
    research_args = ["--pedagogy-research-manifest", str(research_manifest)] if research_manifest else []
    if not example_catalog.exists():
        fail("BOUND_BLUEPRINT_PUBLICATION_GOVERNED_EXAMPLE_CATALOG_REQUIRED")
    if not engineering_admission.exists():
        fail("BOUND_BLUEPRINT_PUBLICATION_ENGINEERING_ADMISSION_REQUIRED")

    out = root / "publication"
    out.mkdir(parents=True, exist_ok=True)
    visibility = out / "engineering_visibility_manifest.json"
    bundle = out / "learner_publication_bundle.json"
    bundle_audit = out / "learner_publication_bundle_audit.json"
    pdf = out / "blueprint_regenerated_learner_product.pdf"
    pdf_audit = out / "blueprint_pdf_audit.json"

    run(HERE / "compile_engineering_visibility_manifest.py", [
        "--engineering-admission", str(engineering_admission),
        "--release-gate", str(gate_path),
        "--out", str(visibility),
    ])
    visibility_args = ["--engineering-visibility-manifest", str(visibility)]

    run(HERE / "compile_publication_bundle.py", [
        "--bucket-plan", str(root / "core1a" / "core1a_bucket_plan.json"),
        "--core1a-manuscript", str(root / "core1a" / "core1a_textbook_manuscript.json"),
        "--core1a-example-catalog", str(example_catalog),
        "--core1b-dir", str(root / "core1b"),
        "--core2a-blueprint", str(root / "core2a" / "core2a_product_blueprint.json"),
        "--core2b-plan", str(root / "core2b" / "plan.json"),
        "--generation-spec", str(generation_spec),
        *research_args,
        *visibility_args,
        "--release-gate", str(gate_path),
        "--out", str(bundle),
    ])
    run(HERE / "validate_publication_bundle.py", [
        "--input", str(bundle), "--release-gate", str(gate_path),
        "--generation-spec", str(generation_spec),
        "--core1a-example-catalog", str(example_catalog),
        *research_args,
        *visibility_args,
        "--audit-out", str(bundle_audit),
    ])
    run(HERE / "render_publication_bundle_pdf.py", [
        "--input", str(bundle), "--release-gate", str(gate_path),
        "--generation-spec", str(generation_spec),
        "--core1a-example-catalog", str(example_catalog),
        *research_args,
        *visibility_args,
        "--out", str(pdf), "--audit-out", str(pdf_audit),
    ])

    bpa = load(bundle_audit); pda = load(pdf_audit); bundle_doc = load(bundle); visibility_doc = load(visibility)
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
    if not bpa.get("engineering_visibility_bound") or not pda.get("engineering_visibility_bound"):
        fail("BOUND_BLUEPRINT_PUBLICATION_ENGINEERING_VISIBILITY_UNBOUND")
    if bpa.get("engineering_visibility_manifest_digest") != visibility_doc.get("manifest_digest"):
        fail("BOUND_BLUEPRINT_PUBLICATION_ENGINEERING_VISIBILITY_DIGEST_DRIFT")
    if pda.get("engineering_visibility_manifest_digest") != visibility_doc.get("manifest_digest"):
        fail("BOUND_BLUEPRINT_PUBLICATION_ENGINEERING_VISIBILITY_RENDER_DIGEST_DRIFT")
    if pda.get("rendered_engineering_visibility_gate_ids") != bpa.get("engineering_visibility_gate_ids"):
        fail("BOUND_BLUEPRINT_PUBLICATION_ENGINEERING_VISIBILITY_RENDER_COVERAGE_DRIFT")
    if bundle_doc["engineering_visibility"]["publication_authorization"] != "NOT_IMPLIED":
        fail("BOUND_BLUEPRINT_PUBLICATION_ENGINEERING_VISIBILITY_AUTHORITY_DRIFT")

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
        "engineering_visibility_manifest_id": visibility_doc["manifest_id"],
        "engineering_visibility_manifest_digest": visibility_doc["manifest_digest"],
        "engineering_visibility_authorization_count": visibility_doc["authorization_count"],
        "engineering_visibility_gate_count": visibility_doc["gate_count"],
        "engineering_visibility_publication_authorization": visibility_doc["publication_authorization"],
        "engineering_visibility_bound": True,
        "semantic_page_count": pda["semantic_page_count"],
        "render_object_count": bpa["render_object_count"],
        "pdf_sha256": pda["pdf_sha256"],
        "pdf_size_bytes": pda["pdf_size_bytes"],
        "semantic_source": pda["semantic_source"],
        "paths": {
            "engineering_visibility_manifest": visibility.name,
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
