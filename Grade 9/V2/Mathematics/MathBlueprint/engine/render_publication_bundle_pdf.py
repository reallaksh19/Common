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


def _compact_counts(counts: dict) -> str:
    ordered = [
        ("concepts", "canonical_concepts"),
        ("equations", "mandatory_equations"),
        ("representations", "representations"),
        ("model conditions", "model_conditions"),
        ("reasoning steps", "reasoning_steps"),
        ("transformations", "transformations"),
        ("misconceptions", "misconceptions"),
        ("verifications", "verification_obligations"),
        ("problem families", "problem_families"),
        ("falsifiers", "falsification_cases"),
    ]
    return "; ".join(f"{label}: {counts.get(key, 0)}" for label, key in ordered)


def render_engineering_visibility(visibility: dict, st: dict) -> tuple[list, list[str]]:
    story = [
        PageBreak(),
        Paragraph("Engineering Map — why this material is in scope", st["stage"]),
        Paragraph(safe(visibility["visibility_notice"]), st["purpose"]),
        Paragraph(
            safe(
                f"Technical authorization: {visibility['technical_authorization']} · "
                f"Publication authorization from this view: {visibility['publication_authorization']} · "
                f"Bound Engineering authorizations: {visibility['authorization_count']} · "
                f"Visible gates: {visibility['gate_count']}"
            ),
            st["small"],
        ),
        Spacer(1, 5),
    ]
    rendered_gate_ids = []
    for gate in visibility["gates"]:
        rendered_gate_ids.append(gate["gate_id"])
        story.append(Paragraph(safe(gate["learner_title"]), st["heading"]))
        story.append(Paragraph(
            safe(
                f"{gate['gate_id']} · chapter: {gate['chapter']} · "
                f"scope role: {', '.join(gate['scope_roles'])} · "
                f"Engineering depth: {', '.join(gate['requested_engineering_depths'])} · "
                f"state: {gate['technical_state']}"
            ),
            st["small"],
        ))
        prerequisites = ", ".join(gate["prerequisite_ids"]) if gate["prerequisite_ids"] else "None"
        story.append(Paragraph(f"<b>Prerequisite closure:</b> {safe(prerequisites)}", st["small"]))
        story.append(Paragraph(f"<b>Engineering structure:</b> {safe(_compact_counts(gate['structure_counts']))}", st["small"]))

        if gate["representations"]:
            story.append(Paragraph("Representations", st["small"]))
            for rep in gate["representations"]:
                story.append(Paragraph(
                    f"• <b>{safe(rep['name'])}</b> ({safe(rep['representation_type'])}) — {safe(rep['verification_method'])}",
                    st["small"],
                ))
        if gate["misconceptions"]:
            story.append(Paragraph("Misconceptions to guard against", st["small"]))
            for misconception in gate["misconceptions"]:
                story.append(Paragraph(
                    f"• {safe(misconception['incorrect_belief'])} <b>Repair:</b> {safe(misconception['required_technical_repair'])}",
                    st["small"],
                ))
        if gate["verification_obligations"]:
            story.append(Paragraph("Verification obligations", st["small"]))
            for verification in gate["verification_obligations"]:
                story.append(Paragraph(f"• {safe(verification)}", st["small"]))
        story.append(Spacer(1, 7))
    return story, rendered_gate_ids


def render_bundle(
    bundle: dict,
    release_gate: dict,
    generation_spec: dict,
    catalog: dict,
    out_pdf: Path,
    research_manifest: dict | None = None,
    engineering_visibility_manifest: dict | None = None,
) -> dict:
    validation = validate_bundle(
        bundle,
        release_gate,
        generation_spec,
        catalog,
        research_manifest,
        engineering_visibility_manifest,
    )
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

    visibility_story, rendered_visibility_gate_ids = render_engineering_visibility(bundle["engineering_visibility"], st)
    story.extend(visibility_story)
    pdf.build(story)

    expected = set(validation["render_object_ids"])
    actual = set(rendered)
    if expected != actual:
        missing = sorted(expected - actual); extra = sorted(actual - expected)
        raise ValueError("MATH_PUBLICATION_BUNDLE_RENDER_COVERAGE_DRIFT:missing=" + ",".join(missing) + ";extra=" + ",".join(extra))
    if rendered_visibility_gate_ids != validation["engineering_visibility_gate_ids"]:
        raise ValueError("MATH_PUBLICATION_BUNDLE_ENGINEERING_VISIBILITY_RENDER_DRIFT")
    data = out_pdf.read_bytes()
    return {
        "status": "PASS",
        "bundle_id": bundle["bundle_id"],
        "bundle_sha256": digest(bundle),
        "rendered_object_count": len(rendered),
        "rendered_object_ids": rendered,
        "semantic_page_count": len(pages),
        "engineering_visibility_gate_count": len(rendered_visibility_gate_ids),
        "rendered_engineering_visibility_gate_ids": rendered_visibility_gate_ids,
        "engineering_visibility_manifest_digest": bundle["engineering_visibility_manifest_digest"],
        "pdf_sha256": hashlib.sha256(data).hexdigest(),
        "pdf_size_bytes": len(data),
        "semantic_source": "LEARNER_PUBLICATION_BUNDLE_ONLY",
        "difficulty_badge_counts": validation["difficulty_badge_counts"],
        "research_manifest_bound": validation["research_manifest_bound"],
        "engineering_visibility_bound": validation["engineering_visibility_bound"],
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--release-gate", required=True)
    ap.add_argument("--generation-spec", required=True)
    ap.add_argument("--core1a-example-catalog", required=True)
    ap.add_argument("--pedagogy-research-manifest")
    ap.add_argument("--engineering-visibility-manifest", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--audit-out", required=True)
    args = ap.parse_args()
    bundle = load(args.input)
    research = load(args.pedagogy_research_manifest) if args.pedagogy_research_manifest else None
    out = Path(args.out); out.parent.mkdir(parents=True, exist_ok=True)
    audit = render_bundle(
        bundle, load(args.release_gate), load(args.generation_spec),
        load(args.core1a_example_catalog), out, research,
        load(args.engineering_visibility_manifest),
    )
    Path(args.audit_out).write_text(json.dumps(audit, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(audit, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
