#!/usr/bin/env python3
"""Review-grade static Core1B/Core2B Chemistry realization.

The B layer changes the learner experience, never Chemistry truth. It consumes only
validated upstream payloads and adds topic-neutral paper/workbook interaction surfaces.
"""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve()
CHEM_ROOT = HERE.parents[2]
sys.path.insert(0, str(CHEM_ROOT / "LearningBlueprint" / "engine"))
sys.path.insert(0, str(CHEM_ROOT / "ExactProduct" / "engine"))

from chemistry_review_writer import ReviewWriter  # noqa: E402
from render_chemistry_learner_products import representation_index  # noqa: E402
from validate_static_b_layer_boundary import validate_core1b, validate_core2b  # noqa: E402
import learner_surface_guard as GUARD  # noqa: E402

CORE1_HELP_LABELS = {
    "H1_ORIENT": "SMALL CLUE",
    "H2_REPRESENT": "SHOW THE MODEL",
    "H3_PRINCIPLE": "KEY IDEA",
    "H4_FIRST_MOVE": "HOW DO I START?",
}
CORE2_HELP_LABELS = {
    "H1_ORIENT": "SMALL CLUE",
    "H2_STRUCTURE": "BREAK IT DOWN",
    "H3_REPRESENTATION": "SHOW THE MODEL",
    "H4_PRINCIPLE": "KEY IDEA",
    "H5_FIRST_MOVE": "HOW DO I START?",
    "H6_PARTIAL_PATH": "NEXT STEP",
}


def _safe(value: Any) -> str:
    text = str(value or "").strip()
    GUARD.assert_learner_safe(text, "static B product")
    return text


def _render_used_representations(writer: ReviewWriter, payload: dict[str, Any], ref: str) -> list[str]:
    """Physically realize only the representations the validated B payload uses.

    This helper performs no representation selection. The payload's
    ``used_representation_refs`` is already constrained by upstream Engineering / Core
    authority; the renderer merely closes that declared use after the learner attempt.
    """
    refs = [str(value) for value in (payload.get("used_representation_refs") or []) if str(value).strip()]
    if not refs:
        return []
    bundle = payload.get("representation_bundle")
    if not isinstance(bundle, dict):
        raise ValueError("CHEM_CORE_RENDER_B_REPRESENTATION_BUNDLE_REQUIRED")
    by_ref = representation_index(bundle)
    realized: list[str] = []
    for rep_ref in refs:
        rep = by_ref.get(rep_ref)
        if rep is None:
            raise ValueError("CHEM_CORE_RENDER_B_REPRESENTATION_REF_MISSING:" + rep_ref)
        if not writer.primitive(rep, ref + ":" + rep_ref):
            raise ValueError("CHEM_CORE_RENDER_B_REQUIRED_VISUAL_UNAVAILABLE:" + rep_ref)
        realized.append(rep_ref)
    return realized


def _finish(writer: ReviewWriter, path: Path, mode: str, evidence: dict[str, Any]) -> dict[str, Any]:
    out = writer.finish()
    raw = path.read_bytes()
    out.update({
        "path": path.name,
        "product_mode": mode,
        "boundary_validation": evidence,
        "pdf_sha256": "sha256:" + hashlib.sha256(raw).hexdigest(),
        "bytes": len(raw),
        "pagination_mode": "CONTENT_FIRST",
    })
    return out


def render_core1b(payload: dict[str, Any], policy: dict[str, Any], path: Path) -> dict[str, Any]:
    evidence = validate_core1b(payload)
    w = ReviewWriter(path, "Chemistry Core1B — Reconstruction Workbook", policy)
    ref = "CORE1B-MODULE"
    w.set_page_role("QUESTION_EPISODE")

    w.heading(payload.get("title") or "Chemistry reconstruction practice")
    w.route_panel(
        "HOW THIS WORKS",
        "Attempt the reconstruction first. Commit your own representation and explanation before using clues. Open only the smallest clue that restarts your reasoning, then compare with the canonical response and verify.",
        ref,
    )
    w.heading("Reconstruction task", level=2, ref=ref)
    w.question_text(payload["task_prompt"], ref)
    w.action_panel("RECONSTRUCT", "Build the representation or relationship yourself before looking at the clue ladder.", ref)
    w.action_panel("EXPLAIN OR JUSTIFY", "Write why your reconstruction is chemically consistent, not only what the final statement is.", ref)
    w.workspace(max(7, int(payload.get("workspace_lines", 8))), ref)

    w.new_page("Core1B reconstruction clues", role="TTU_RECONSTRUCTION")
    w.heading("Progressive clues")
    w.route_panel("USE LESS HELP FIRST", "Read clues from the top. Stop as soon as you can continue independently.", ref)
    for row in payload["help"]:
        w.clue_panel(CORE1_HELP_LABELS[row["level"]], row["text"], ref)
    w.action_panel(
        "RESUME YOUR RECONSTRUCTION",
        "Use only the clue or clues you opened. Continue your original reconstruction now and commit a revised explanation before turning to the check.",
        ref,
    )
    w.workspace(4, ref)

    # The canonical check is a distinct post-attempt semantic episode. Starting it
    # explicitly prevents a governed visual from becoming an orphan continuation of
    # the clue page while preserving the attempt-first boundary.
    w.new_page("Core1B reconstruction check", role="SOLUTION")
    w.heading("Check your reconstruction", level=2, ref=ref)
    w.answer_panel("EXPECTED RESPONSE", payload["canonical_answer"], ref)
    if payload.get("explanation"):
        w.concept_panel("WHY IT WORKS", payload["explanation"], ref)
    realized = _render_used_representations(w, payload, ref + "-CHECK")
    w.verification_panel("VERIFY", payload["check"], ref)
    w.action_panel("TEACH IT BACK", "Cover the expected response and explain the decisive relationship in your own words, then run the verification again.", ref)
    evidence = dict(evidence)
    evidence["physically_realized_representation_refs"] = realized
    return _finish(w, path, "CORE1B", evidence)


def render_core2b(payload: dict[str, Any], policy: dict[str, Any], path: Path) -> dict[str, Any]:
    evidence = validate_core2b(payload)
    source = payload["source_item"]
    support = evidence["resolved_support_profile"]
    ref = "CORE2B-ITEM"
    w = ReviewWriter(path, "Chemistry Core2B — Transfer Workbook", policy)
    w.set_page_role("QUESTION_EPISODE")

    w.heading("Chemistry transfer practice")
    w.route_panel("SOURCE", source["source_locator"], ref)
    w.heading("Question", level=2, ref=ref)
    w.question_text(source["stem"], ref)
    w.action_panel("TARGET", "State exactly what the question is asking you to determine before choosing a method.", ref)
    w.action_panel("MODEL OR REPRESENTATION CHOICE", "Commit to the representation, quantities or species you will track before opening the clue ladder.", ref)
    w.action_panel("FIRST MOVE + WHY", "Write your first move and one sentence justifying why it is chemically valid.", ref)
    w.workspace(max(7, int(payload.get("workspace_lines", 10))), ref)

    entry = support["hint_entry_level"]
    allowed = list(CORE2_HELP_LABELS)
    start = allowed.index(entry)
    visible = [row for row in payload["help"] if row["level"] in CORE2_HELP_LABELS and allowed.index(row["level"]) >= start]

    w.new_page("Core2B transfer clues", role="TTU_RECONSTRUCTION")
    w.heading("Progressive clues")
    w.route_panel("USE ONLY WHAT YOU NEED", "Start at the first visible clue and stop when you can resume the solution independently.", ref)
    for row in visible:
        w.clue_panel(CORE2_HELP_LABELS[row["level"]], row["text"], ref)
    w.action_panel(
        "RESUME YOUR SOLUTION",
        "Use only the clue or clues you opened. Continue your own reasoning and commit the next steps before opening the full solution.",
        ref,
    )
    w.workspace(4, ref)

    # Solution closure is deliberately a complete semantic episode rather than a
    # terminal fragment left behind by clue pagination. The repeated source stem is
    # upstream-governed question context, not newly authored Chemistry.
    w.new_page("Core2B solution", role="SOLUTION")
    w.heading("Full solution")
    w.question_text(source["stem"], ref + "-SOLUTION-CONTEXT")
    w.answer_panel("FULL SOLUTION", payload["full_solution"], ref)
    w.answer_panel("ANSWER", source["canonical_answer"], ref)
    realized = _render_used_representations(w, payload, ref + "-SOLUTION")
    w.verification_panel("VERIFY AND REFLECT", payload["verify_reflect"], ref)

    # Reflection is intentionally a task-bound workspace page, not a sparse solution
    # continuation. This uses the existing workspace-page density authority.
    w.new_page("Core2B transfer reflection", role="WORKSPACE")
    w.heading("Rebuild and generalize")
    w.action_panel("GENERALIZE", "Name the decisive clue that made this problem belong to its problem family, then state what would make the method fail.", ref)
    w.action_panel("REBUILD WITHOUT LOOKING", "Cover the solution. Reproduce the reasoning path from the original question, then compare only after you have committed a complete chain.", ref)
    w.workspace(5, ref)
    w.action_panel("FINAL CHECK", "Mark the first point where your rebuilt path diverged from the governed solution, repair that step, and verify the conclusion again.", ref)
    evidence = dict(evidence)
    evidence["physically_realized_representation_refs"] = realized
    return _finish(w, path, "CORE2B", evidence)


def render_static_b_product(product_mode: str, payload: dict[str, Any], policy: dict[str, Any], path: Path) -> dict[str, Any]:
    path.parent.mkdir(parents=True, exist_ok=True)
    if product_mode == "CORE1B":
        return render_core1b(payload, policy, path)
    if product_mode == "CORE2B":
        return render_core2b(payload, policy, path)
    raise ValueError("CHEM_CORE_RENDER_B_MODE_INVALID")
