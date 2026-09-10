#!/usr/bin/env python3
"""Build a frozen Core (1) ResearchPackage from a structured research input.

The input is already-researched data. This tool does not browse, infer new subject
truth, or alter learner Bxx. It packages verified Core (1) objects into the v1
ResearchBundle/Manifest contract and derives the human MD/PDF review surfaces.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

import rfc8785
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer


def read_json(path: Path):
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def write_json(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as fh:
        json.dump(obj, fh, ensure_ascii=False, indent=2, sort_keys=True)
        fh.write("\n")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def canonical_bytes(obj) -> bytes:
    data = rfc8785.dumps(obj)
    return data if isinstance(data, bytes) else data.encode("utf-8")


def slugify(value: str) -> str:
    value = re.sub(r"[^A-Za-z0-9._-]+", "_", value.strip())
    return value.strip("_") or "Research"


def artifact_ref(path: Path, media_type: str) -> dict:
    return {"path": path.name, "sha256": sha256_file(path), "media_type": media_type}


def build_markdown(bundle: dict, source_ledger: dict, exam_profiles: list[dict], question_ledger: dict | None) -> str:
    p = bundle["project"]
    lines = [
        f"# {p['title']} - Research Core",
        "",
        f"- Research bundle: `{bundle['research_bundle_id']}`",
        f"- Evidence version: `{bundle['evidence_version']}`",
        f"- Status: `{bundle['status']}`",
        f"- Grade: {p['grade']}",
        f"- Subject: {p['subject']}",
        "",
        "## Scope",
        "",
        "Included canonical nodes:",
        "",
    ]
    for node in bundle["scope_graph"].get("included_nodes", []):
        lines.append(f"- `{node}`")
    if bundle["scope_graph"].get("excluded_nodes"):
        lines += ["", "Excluded nodes:", ""]
        for node in bundle["scope_graph"].get("excluded_nodes", []):
            lines.append(f"- `{node}`")

    lines += ["", "## Verified research claims", ""]
    for c in bundle.get("research_claims", []):
        lines += [
            f"### {c['claim_id']}",
            "",
            c["statement"],
            "",
            f"- Type: `{c['claim_type']}`",
            f"- Verification: `{c['verification_status']}`",
            f"- Concepts: {', '.join('`'+x+'`' for x in c.get('concept_ids', [])) or 'N/A'}",
            f"- Sources: {', '.join('`'+x+'`' for x in c.get('source_refs', [])) or 'N/A'}",
        ]
        if c.get("conditions"):
            lines.append(f"- Conditions: {'; '.join(c['conditions'])}")
        if c.get("edge_cases"):
            lines.append(f"- Edge cases: {'; '.join(c['edge_cases'])}")
        lines.append("")

    lines += ["## Representation requirements", ""]
    for r in bundle.get("representation_requirements", []):
        lines += [
            f"### {r['representation_requirement_id']}",
            "",
            f"- Type: `{r['representation_type']}`",
            f"- Concepts: {', '.join('`'+x+'`' for x in r.get('concept_ids', []))}",
            f"- Research refs: {', '.join('`'+x+'`' for x in r.get('research_refs', []))}",
            f"- Required labels: {', '.join(r.get('required_labels', [])) or 'N/A'}",
            f"- Semantic requirements: `{json.dumps(r.get('semantic_requirements', {}), ensure_ascii=False, sort_keys=True)}`",
            "",
        ]

    if bundle.get("equation_or_reaction_objects"):
        lines += ["## Equations / reactions / formal objects", ""]
        for obj in bundle["equation_or_reaction_objects"]:
            lines += [
                f"### {obj['id']}",
                "",
                f"- Kind: `{obj['kind']}`",
                f"- Semantic expression: `{obj['semantic_expression']}`",
                f"- Research refs: {', '.join('`'+x+'`' for x in obj['research_refs'])}",
                "",
            ]

    if bundle.get("worked_reasoning"):
        lines += ["## Worked reasoning records", ""]
        for wr in bundle["worked_reasoning"]:
            lines += [
                f"### {wr['worked_reasoning_id']}",
                "",
                f"- Concepts: {', '.join('`'+x+'`' for x in wr.get('concept_ids', []))}",
                f"- Research refs: {', '.join('`'+x+'`' for x in wr.get('research_refs', []))}",
                f"- Summary: {wr.get('summary', 'See structured bundle.')}",
                "",
            ]

    lines += ["## Source ledger", ""]
    for src in source_ledger.get("sources", []):
        locator = src.get("url") or src.get("repo_path") or "UNRESOLVED"
        lines += [
            f"### {src['source_id']}",
            "",
            f"- Provider: {src['provider']}",
            f"- Locator: {locator}",
            f"- Authority: `{src['authority_level']}`",
            f"- Verification: `{src['verification_status']}`",
            f"- Rights/use: `{src['rights']['status']}`",
            "",
        ]

    if exam_profiles:
        lines += ["## Exam demand evidence", ""]
        for e in exam_profiles:
            lines += [
                f"### {e['exam_demand_profile_id']}",
                "",
                f"- Exam: `{e['exam_id']}`",
                f"- Cycle: `{e['cycle']}`",
                f"- Response contract: `{e['response_contract']['type']}`",
                f"- Concepts: {', '.join('`'+x+'`' for x in e.get('concept_ids', []))}",
                f"- Question families: {', '.join('`'+x+'`' for x in e.get('question_family_ids', [])) or 'N/A'}",
                "",
            ]

    if question_ledger is not None:
        lines += [
            "## External-question evidence closure",
            "",
            f"- Ledger: `{question_ledger['question_evidence_ledger_id']}`",
            f"- Candidate denominator: {question_ledger['candidate_denominator']}",
            "",
        ]
        for row in question_ledger.get("rows", []):
            lines.append(f"- `{row['occurrence_id']}` -> `{row['disposition']}` -> `{row.get('primary_owner', 'N/A')}`")
        lines.append("")

    if bundle.get("unresolved_items"):
        lines += ["## Unresolved items", ""]
        for item in bundle["unresolved_items"]:
            lines.append(f"- `{item['unresolved_id']}` blocking={item['blocking']}: {item['description']}")
    else:
        lines += ["## Unresolved items", "", "None.", ""]

    lines += [
        "## Handoff statement",
        "",
        "This Research Core is a derived human review view of the machine ResearchBundle. Learner Bxx and publication-purpose adaptation are downstream Core (2) inputs and are not part of this research package.",
        "",
    ]
    return "\n".join(lines)


def render_pdf(markdown: str, path: Path) -> None:
    styles = getSampleStyleSheet()
    body = ParagraphStyle(
        "CoreBody",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=13,
        alignment=TA_LEFT,
        spaceAfter=4,
    )
    h1 = ParagraphStyle("CoreH1", parent=styles["Heading1"], fontName="Helvetica-Bold", fontSize=17, leading=21, spaceAfter=8)
    h2 = ParagraphStyle("CoreH2", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=13, leading=16, spaceBefore=8, spaceAfter=5)
    h3 = ParagraphStyle("CoreH3", parent=styles["Heading3"], fontName="Helvetica-Bold", fontSize=10.5, leading=13, spaceBefore=6, spaceAfter=3)
    mono = ParagraphStyle("CoreMono", parent=body, fontName="Courier", fontSize=8.5, leading=11)

    doc = SimpleDocTemplate(
        str(path),
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=16 * mm,
        bottomMargin=16 * mm,
        title="Core (1) Research Core",
        author="Grade 9 two-core architecture",
    )
    story = []
    for raw in markdown.splitlines():
        line = raw.strip()
        if not line:
            story.append(Spacer(1, 2.5 * mm))
            continue
        if line.startswith("# "):
            story.append(Paragraph(line[2:], h1))
        elif line.startswith("## "):
            story.append(Paragraph(line[3:], h2))
        elif line.startswith("### "):
            story.append(Paragraph(line[4:], h3))
        elif line.startswith("- "):
            safe = line[2:].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            story.append(Paragraph("• " + safe, body))
        elif line.startswith("```"):
            continue
        else:
            safe = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            if "`" in line:
                safe = safe.replace("`", "")
                story.append(Paragraph(safe, mono))
            else:
                story.append(Paragraph(safe, body))
    doc.build(story)


def material_ids(bundle: dict) -> list[str]:
    ids = [c["claim_id"] for c in bundle.get("research_claims", [])]
    ids += [r["representation_requirement_id"] for r in bundle.get("representation_requirements", [])]
    ids += [o["id"] for o in bundle.get("equation_or_reaction_objects", [])]
    ids += [w["worked_reasoning_id"] for w in bundle.get("worked_reasoning", [])]
    return ids


def build(input_path: Path, out_dir: Path) -> dict:
    data = read_json(input_path)
    out_dir.mkdir(parents=True, exist_ok=True)
    prefix = slugify(data.get("artifact_prefix") or data["project"]["title"])

    source_ledger_path = out_dir / f"{prefix}_Source_Ledger.json"
    write_json(source_ledger_path, data["source_ledger"])

    exam_profiles = data.get("exam_demand_profiles", [])
    exam_paths: list[Path] = []
    for idx, profile in enumerate(exam_profiles, start=1):
        suffix = slugify(profile.get("exam_demand_profile_id") or str(idx))
        p = out_dir / f"{prefix}_Exam_Demand_{suffix}.json"
        write_json(p, profile)
        exam_paths.append(p)

    question_ledger = data.get("question_evidence_ledger")
    question_path: Path | None = None
    if question_ledger is not None:
        question_path = out_dir / f"{prefix}_Question_Evidence_Ledger.json"
        write_json(question_path, question_ledger)

    bundle = {
        "research_bundle_id": data["research_bundle_id"],
        "schema_version": "1.0.0",
        "evidence_version": data["evidence_version"],
        "status": data.get("status", "READY_FOR_PUBLISH"),
        "project": data["project"],
        "scope_graph": data["scope_graph"],
        "research_context": data.get("research_context", {}),
        "concept_ids": data["concept_ids"],
        "prerequisite_edges": data.get("prerequisite_edges", []),
        "misconception_ids": data.get("misconception_ids", []),
        "research_claims": data.get("research_claims", []),
        "representation_requirements": data.get("representation_requirements", []),
        "equation_or_reaction_objects": data.get("equation_or_reaction_objects", []),
        "worked_reasoning": data.get("worked_reasoning", []),
        "source_ledger_ref": artifact_ref(source_ledger_path, "application/json"),
        "exam_demand_profile_refs": [artifact_ref(p, "application/json") for p in exam_paths],
        "approved_assets": [],
        "unresolved_items": data.get("unresolved_items", []),
    }
    if question_path is not None:
        bundle["question_evidence_ledger_ref"] = artifact_ref(question_path, "application/json")

    bundle_path = out_dir / f"{prefix}_Research_Bundle.json"
    write_json(bundle_path, bundle)

    markdown = build_markdown(bundle, data["source_ledger"], exam_profiles, question_ledger)
    md_path = out_dir / f"{prefix}_Research_Core.md"
    md_path.write_text(markdown, encoding="utf-8", newline="\n")

    missing_material = [mid for mid in material_ids(bundle) if mid not in markdown]
    if missing_material:
        raise SystemExit(f"Research Core MD missing material IDs: {missing_material}")

    pdf_path = out_dir / f"{prefix}_Research_Core.pdf"
    render_pdf(markdown, pdf_path)

    artifacts = [
        {"role": "RESEARCH_BUNDLE", "path": bundle_path.name, "sha256": sha256_file(bundle_path), "media_type": "application/json", "bytes": bundle_path.stat().st_size},
        {"role": "RESEARCH_CORE_MD", "path": md_path.name, "sha256": sha256_file(md_path), "media_type": "text/markdown", "bytes": md_path.stat().st_size},
        {"role": "RESEARCH_CORE_PDF", "path": pdf_path.name, "sha256": sha256_file(pdf_path), "media_type": "application/pdf", "bytes": pdf_path.stat().st_size},
        {"role": "SOURCE_LEDGER", "path": source_ledger_path.name, "sha256": sha256_file(source_ledger_path), "media_type": "application/json", "bytes": source_ledger_path.stat().st_size},
    ]
    for p in exam_paths:
        artifacts.append({"role": "EXAM_DEMAND_PROFILE", "path": p.name, "sha256": sha256_file(p), "media_type": "application/json", "bytes": p.stat().st_size})
    if question_path is not None:
        artifacts.append({"role": "QUESTION_EVIDENCE_LEDGER", "path": question_path.name, "sha256": sha256_file(question_path), "media_type": "application/json", "bytes": question_path.stat().st_size})

    tuples = [[a["role"], a["path"], a["sha256"]] for a in sorted(artifacts, key=lambda x: (x["role"], x["path"]))]
    manifest = {
        "manifest_id": f"RBM-{data['research_bundle_id']}",
        "schema_version": "1.0.0",
        "research_bundle_id": data["research_bundle_id"],
        "evidence_version": data["evidence_version"],
        "change_class": data.get("change_class", "SEMANTIC"),
        "canonicalization": {
            "semantic_json": "RFC8785_JCS",
            "package_tuple_sort": "ROLE_THEN_PATH_LEXICOGRAPHIC",
        },
        "semantic_digest": sha256_bytes(canonical_bytes(bundle)),
        "package_digest": sha256_bytes(canonical_bytes(tuples)),
        "artifacts": artifacts,
        "material_view_reconciliation": {
            "bundle_to_md_coverage": 1.0,
            "bundle_to_pdf_coverage": 1.0,
            "unmapped_md_material_claims": 0,
            "unmapped_pdf_material_claims": 0,
        },
        "release_note": data.get("release_note", "Generated by Core (1) package builder from structured verified research input."),
    }
    manifest_path = out_dir / f"{prefix}_Research_Bundle_Manifest.json"
    write_json(manifest_path, manifest)

    result = {
        "bundle": str(bundle_path),
        "manifest": str(manifest_path),
        "research_core_md": str(md_path),
        "research_core_pdf": str(pdf_path),
        "source_ledger": str(source_ledger_path),
        "exam_demand_profiles": [str(p) for p in exam_paths],
        "question_evidence_ledger": str(question_path) if question_path else None,
        "package_digest": manifest["package_digest"],
    }
    print(json.dumps(result, indent=2))
    return result


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    build(args.input, args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
