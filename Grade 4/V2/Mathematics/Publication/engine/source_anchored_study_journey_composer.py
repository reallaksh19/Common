"""Canonical source-anchored StudyJourney publication adapter.

This adapter binds every SOURCE learner question to a previously authored visual
representation before calling the generic StudyJourney composer. It never
creates mathematical semantics in Publication.
"""
from __future__ import annotations

import copy
from pathlib import Path
from typing import Any, Dict, Mapping, Tuple

from Grade4.V2.Mathematics.Publication.engine.study_journey_composer import render_study_journey
from Grade4.V2.Mathematics.StudyDesign.engine.source_visual_hints import (
    assert_source_visual_hint_coverage,
    attach_source_visual_hints,
)


def _materialize_question_visual_blocks(plan: Mapping[str, Any]) -> Dict[str, Any]:
    """Split multi-question blocks so each SOURCE question owns one visual.

    The existing document composer already realizes typed block representations.
    This adapter only moves the resolved question visual into that existing seam.
    Generated-practice blocks are not changed.
    """
    out = copy.deepcopy(plan)
    for module in out.get("modules") or []:
        new_blocks = []
        for block in module.get("blocks") or []:
            questions = list(block.get("questions") or [])
            source_questions = [q for q in questions if str(q.get("origin") or "") == "SOURCE"]
            if not source_questions:
                new_blocks.append(block)
                continue

            generated = [q for q in questions if str(q.get("origin") or "") != "SOURCE"]
            for idx, question in enumerate(source_questions, start=1):
                qblock = copy.deepcopy(block)
                qblock["block_id"] = f"{block['block_id']}-SRCVIS-{idx}"
                qblock["questions"] = [question]
                qblock["source_refs"] = [str((question.get("source_identity") or {}).get("source_ref") or "")]
                qblock["title"] = f"{block.get('title', '')} - {question.get('display_ref', '')}".strip(" -")
                hint = question.get("hint_contract") or {}
                visual = hint.get("visual_hint") or {}
                qblock["representation"] = {
                    "kind": str(visual.get("primitive_kind") or ""),
                    "params": dict(visual.get("semantic_params") or {}),
                    "fidelity": str(visual.get("fidelity") or "SCHEMATIC"),
                }
                new_blocks.append(qblock)
            if generated:
                gblock = copy.deepcopy(block)
                gblock["block_id"] = f"{block['block_id']}-GENERATED"
                gblock["questions"] = generated
                new_blocks.append(gblock)
        module["blocks"] = new_blocks
    return out


def render_source_anchored_study_journey(
    plan: Mapping[str, Any],
    visual_catalog: Mapping[str, Mapping[str, Any]],
    output_pdf_path: Path,
) -> Tuple[str, Dict[str, Any]]:
    enriched = attach_source_visual_hints(plan, visual_catalog)
    coverage = assert_source_visual_hint_coverage(enriched)
    materialized = _materialize_question_visual_blocks(enriched)
    pdf_sha, custody = render_study_journey(materialized, output_pdf_path)
    custody.setdefault("study_journey", {})["source_visual_hint_required"] = True
    custody["study_journey"]["source_visual_hint_coverage"] = coverage
    return pdf_sha, custody
