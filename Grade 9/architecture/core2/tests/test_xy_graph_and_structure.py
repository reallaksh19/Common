#!/usr/bin/env python3
"""Falsify shared XY_GRAPH and executable PublicationStructure wiring."""
from __future__ import annotations

import copy
import json
import tempfile
from pathlib import Path

import pymupdf as fitz
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate

import sys

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT.parents[1] / "skills" / "grade9-core2-publisher" / "scripts"
sys.path.insert(0, str(SCRIPTS))

import run_core2_structured_impl as impl  # noqa: E402


def bundle(subject: str) -> dict:
    return {
        "research_bundle_id": f"RB-XY-{subject}",
        "project": {"subject": subject, "topic_id": f"T-{subject}", "title": f"XY {subject}"},
        "concept_ids": [f"C-{subject}"],
        "research_claims": [{"claim_id": f"R-{subject}", "statement": "Reference claim for XY capability reuse.", "concept_ids": [f"C-{subject}"], "conditions": []}],
        "representation_requirements": [{
            "representation_requirement_id": f"REQ-XY-{subject}",
            "representation_type": "XY_GRAPH",
            "concept_ids": [f"C-{subject}"],
            "research_refs": [f"R-{subject}"],
            "required_labels": ["x", "y", "series"],
            "blocking_if_unsupported": True,
            "semantic_requirements": {
                "x_axis": {"label": "x", "min": -2, "max": 2, "ticks": [-2, -1, 0, 1, 2]},
                "y_axis": {"label": "y", "min": -2, "max": 2, "ticks": [-2, -1, 0, 1, 2]},
                "series": [{"label": "series", "points": [[-2, -1], [0, 0], [2, 1]], "line_style": "SOLID", "marker": "CIRCLE"}],
                "reference_lines": [{"axis": "x", "value": 0, "label": "origin", "line_style": "DASHED"}],
                "annotations": [{"x": 2, "y": 1, "label": "endpoint"}]
            }
        }],
        "equation_or_reaction_objects": [],
        "worked_reasoning": [],
    }


def learner(subject: str) -> dict:
    return {"learner_profile_id": f"LP-{subject}", "baselines": [{"subtopic_id": f"C-{subject}", "value": 40}]}


def target(subject: str) -> dict:
    return {"publication_target_id": f"PT-{subject}", "research_package_digest": "0" * 64, "purpose": {"type": "STUDY_GUIDE"}, "requested_products": {"study_guide": True, "transfer_book": False}}


def main() -> int:
    registry_path = ROOT / "representation" / "capabilities.v1.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    xy = [x for x in registry["capabilities"] if x["representation_type"] == "XY_GRAPH"]
    assert len(xy) == 1
    cap = xy[0]
    assert cap["status"] == "IMPLEMENTED"
    assert cap["renderer_id"] == "xy_graph_v1"
    assert set(cap["subjects"]) == {"MATHEMATICS", "PHYSICS", "CHEMISTRY"}

    planned = copy.deepcopy(registry)
    for row in planned["capabilities"]:
        if row["representation_type"] == "XY_GRAPH":
            row["status"] = "PLANNED"
    try:
        impl._ORIG_BUILD_PLAN(bundle("MATHEMATICS"), {}, learner("MATHEMATICS"), target("MATHEMATICS"), planned)
    except SystemExit as exc:
        assert exc.code == 2
    else:
        raise AssertionError("XY_GRAPH PLANNED state did not fail closed")

    plans = []
    for subject in ("MATHEMATICS", "PHYSICS", "CHEMISTRY"):
        b = bundle(subject)
        p = impl.build_plan(b, {}, learner(subject), target(subject), registry)
        rep = p["representation_instances"][0]
        assert rep["capability_id"] == "REP-GENERIC-XY-GRAPH"
        assert rep["renderer_id"] == "xy_graph_v1"
        assert rep["semantic_payload"] == b["representation_requirements"][0]["semantic_requirements"]
        plans.append(rep)

    with tempfile.TemporaryDirectory() as td:
        pdf = Path(td) / "xy_graph_golden.pdf"
        doc = SimpleDocTemplate(str(pdf), pagesize=A4)
        doc.build([impl.StructuredRepresentationFlowable(plans[0])])
        reopened = fitz.open(pdf)
        text = "\n".join(p.get_text() for p in reopened)
        nongray = 0
        for page in reopened:
            for drawing in page.get_drawings():
                for key in ("color", "fill"):
                    col = drawing.get(key)
                    if isinstance(col, (list, tuple)) and len(col) >= 3 and max(col[:3]) - min(col[:3]) > 1e-6:
                        nongray += 1
        reopened.close()
        for marker in ("XY GRAPH", "x", "y", "series", "origin", "endpoint"):
            assert marker in text, marker
        assert nongray == 0

    print("XY_GRAPH_FAIL_CLOSED = PASS")
    print("XY_GRAPH_GENERIC_REUSE = PASS")
    print("XY_GRAPH_REOPENED_PDF = PASS")
    print("PUBLICATION_STRUCTURE_EXECUTABLE_LAYER = PRESENT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
