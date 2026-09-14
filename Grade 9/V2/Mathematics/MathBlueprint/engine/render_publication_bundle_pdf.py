#!/usr/bin/env python3
"""Presentation-only renderer for Mathematics Learner Publication Bundles."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer

from blueprint_common import digest, load
from render_content_complete_blueprint_pdf import (
    safe, styles, render_node, render_representation, render_ttu, render_workspace,
)
from validate_publication_bundle import validate_bundle


def ordered_pages(bundle: dict) -> list[dict]:
    concepts = sorted(bundle["concept_components"], key=lambda x: x["sequence"])
    problem = bundle["problem_component"]
    pages = []
    for stage in bundle["publication_stage_order"]:
        if stage in {"CORE1A", "CORE1B"}:
            for component in concepts:
                pages.extend(p for p in component["pages"] if p["stage"] == stage)
        else:
            pages.extend(p for p in problem["pages"] if p["stage"] == stage)
    return pages


def render_bundle(bundle: dict, release_gate: dict, generation_spec: dict, catalog: dict, out_pdf: Path) -> dict:
    validation = validate_bundle(bundle, release_gate, generation_spec, catalog)
    st = styles()
    pages = ordered_pages(bundle)
    pdf = SimpleDocTemplate(
        str(out_pdf), pagesize=A4, leftMargin=17*mm, rightMargin=17*mm,
        topMargin=15*mm, bottomMargin=15*mm, title="Mathematics Blueprint Bundle Publication",
    )
    story = []
    rendered = []
    for pi, page in enumerate(pages):
        story.append(Paragraph(f"{safe(page['stage'])} — {safe(page['page_kind'].replace('_',' ').title())}", st["stage"]))
        story.append(Paragraph(safe(page["page_purpose"]), st["purpose"]))
        for block in page["technical_blocks"]:
            for node in block["render_nodes"]:
                story.append(render_node(node, st))
            rendered.append(block["block_id"])
        for block in page["prose_blocks"]:
            for node in block["render_nodes"]:
                story.append(render_node(node, st))
            rendered.append(block["block_id"])
        for rep in page["representations"]:
            story.append(Spacer(1, 4)); story.append(render_representation(rep, st)); story.append(Spacer(1, 5))
            rendered.append(rep["representation_id"])
        for ttu in page["reconstructable_ttus"]:
            story.append(Spacer(1, 5)); story.append(render_ttu(ttu, st)); story.append(Spacer(1, 5))
            rendered.append(ttu["ttu_id"])
        for ws in page["workspace_blocks"]:
            story.append(render_workspace(ws, st)); story.append(Spacer(1, 5))
            rendered.append(ws["workspace_id"])
        if pi != len(pages) - 1:
            story.append(PageBreak())
    pdf.build(story)

    expected = set(validation["render_object_ids"])
    actual = set(rendered)
    if expected != actual:
        missing = sorted(expected - actual); extra = sorted(actual - expected)
        raise ValueError("MATH_PUBLICATION_BUNDLE_RENDER_COVERAGE_DRIFT:missing=" + ",".join(missing) + ";extra=" + ",".join(extra))
    data = out_pdf.read_bytes()
    return {
        "status": "PASS",
        "bundle_id": bundle["bundle_id"],
        "bundle_sha256": digest(bundle),
        "rendered_object_count": len(rendered),
        "rendered_object_ids": rendered,
        "semantic_page_count": len(pages),
        "pdf_sha256": hashlib.sha256(data).hexdigest(),
        "pdf_size_bytes": len(data),
        "semantic_source": "LEARNER_PUBLICATION_BUNDLE_ONLY",
        "difficulty_badge_counts": validation["difficulty_badge_counts"],
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--release-gate", required=True)
    ap.add_argument("--generation-spec", required=True)
    ap.add_argument("--core1a-example-catalog", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--audit-out", required=True)
    args = ap.parse_args()
    bundle = load(args.input)
    out = Path(args.out); out.parent.mkdir(parents=True, exist_ok=True)
    audit = render_bundle(
        bundle, load(args.release_gate), load(args.generation_spec),
        load(args.core1a_example_catalog), out,
    )
    Path(args.audit_out).write_text(json.dumps(audit, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(audit, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
