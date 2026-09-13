"""Canonical source-anchored StudyJourney publication adapter.

Every SOURCE learner question is bound to its authored H1/H2/H3 visual support
before publication. Multi-question source blocks are split so each source item
is an atomic measured publication unit and can paginate independently. The
actual staged hints are rendered by the generic StudyJourney composer through
its intrinsic StagedHintComponent; this adapter does not duplicate them as a
second block-level representation.
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


def _split_source_question_blocks(plan: Mapping[str, Any]) -> Dict[str, Any]:
    """Give each SOURCE question its own block for independent measurement.

    This is a pagination/layout boundary only. It does not invent or alter
    pedagogy, mathematical semantics, hint stages, source identity or answers.
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
                qblock["block_id"] = f"{block['block_id']}-SOURCE-{idx}"
                qblock["questions"] = [question]
                qblock["source_refs"] = [str((question.get("source_identity") or {}).get("source_ref") or "")]
                qblock["title"] = f"{block.get('title', '')} - {question.get('display_ref', '')}".strip(" -")
                # Staged H1/H2/H3 live inside the question contract. A stale
                # block-level primary visual would duplicate the hint visual.
                qblock.pop("representation", None)
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
    materialized = _split_source_question_blocks(enriched)
    pdf_sha, custody = render_study_journey(materialized, output_pdf_path)
    custody.setdefault("study_journey", {})["source_visual_hint_required"] = True
    custody["study_journey"]["source_visual_hint_coverage"] = coverage
    custody["study_journey"]["source_question_atomic_layout"] = True
    return pdf_sha, custody
