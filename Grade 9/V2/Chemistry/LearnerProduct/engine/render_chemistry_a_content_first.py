#!/usr/bin/env python3
"""Content-first Chemistry Core1A/Core2A realization for unified Core custody.

This module changes pagination only. Chemistry-bearing learner content remains in the
semantic payload supplied by the current repository Blueprint. It reuses the governed
A-layer primitives and learner-surface guard from render_chemistry_learner_products.
"""
from __future__ import annotations

from typing import Any

from render_chemistry_learner_products import (
    FONT,
    PAGE_H,
    PageWriter,
    TOKEN_REPLACEMENTS,
    _attempt_support,
    _draw_provenance,
    _source_prompt,
    _visuals_for_refs,
    capability_title,
    digest,
    public_text,
    representation_index,
    sha_file,
)


def _wrapped_height(writer: PageWriter, text: Any, *, question: bool = False, indent: float = 0.0) -> float:
    value = public_text(text)
    if question:
        lines = writer._wrap(value, FONT, writer.question, writer.width - indent)
        return len(lines) * writer.question_leading + 3.0
    lines = writer._wrap(value, FONT, writer.body, writer.width - indent)
    return len(lines) * writer.leading + 3.0


def _wrapped_list_height(writer: PageWriter, values: list[Any] | None, *, indent: float = 8.0) -> float:
    return sum(_wrapped_height(writer, "• " + public_text(value), indent=indent) for value in (values or []))


def _begin_semantic_block(writer: PageWriter, label: str, minimum_height: float) -> None:
    """Place a semantic block in remaining space or move the whole start to a new page."""
    before = writer.page
    writer.ensure(minimum_height, label)
    if writer.page == before and writer.y < PAGE_H - writer.margin - 10:
        writer.rule()


def _core1a_attempt_height(writer: PageWriter, prompt: str, workspace_lines: int = 6) -> float:
    return (
        writer.section + 18
        + writer.small + 12
        + _wrapped_height(writer, prompt, question=True)
        + writer.small + 12
        + workspace_lines * 18
        + 36
    )


def render_core1a_content_first(manuscript, representations, policy, path):
    writer = PageWriter(path, "Chemistry Core (1A) — Learner Study Guide", policy)
    rep_index = representation_index(representations)
    visual_rows = []
    writer.heading("Chemistry Core (1A)")
    writer.para("A learner study guide built from the governed Chemistry teaching plan. Learn the idea, use the representation, practise, check your response, then move to transfer questions.")
    writer.label("HOW TO USE THIS BOOK")
    writer.bullets([
        "Study the idea before the routine.",
        "Attempt every practice prompt before reading its expected response.",
        "Use the readiness check before moving to transfer practice.",
    ])

    for bi, bucket in enumerate(manuscript["buckets"], 1):
        writer.new_page("Core (1A) bucket")
        writer.heading(f"Part {bi} — {public_text(bucket['learner_title'])}")
        writer.label("THE IDEA THAT HOLDS THIS PART TOGETHER")
        writer.para(bucket["bucket_invariant"])

        for si, section in enumerate(bucket["teaching_sections"], 1):
            ref = f"C1A-B{bi:02d}-S{si:02d}"
            writer.heading(capability_title(section["capability_ref"]), 2, ref)
            writer.label("SEE THE IDEA", ref)
            writer.para(section.get("see") or section.get("activation"), ref)
            writer.label("EXPLAIN", ref)
            writer.bullets(section.get("explain"), ref)
            refs = list(section.get("representation_refs") or [])
            realized, unavailable = _visuals_for_refs(writer, refs, rep_index, ref)
            if refs and realized == 0:
                raise ValueError("CHEM_LP_RENDER_REQUIRED_VISUAL_MISSING:" + ref)
            visual_rows.append({
                "content_ref": ref,
                "required_refs": refs,
                "realized": realized,
                "unavailable_secondary_refs": unavailable,
                "status": "PASS",
            })
            if section.get("watch_one"):
                writer.label("WATCH ONE", ref)
                writer.para(section["watch_one"], ref)
            worked = section.get("worked_example")
            if worked:
                writer.label("WORKED EXAMPLE", ref)
                writer.question_text(worked.get("prompt", ""), ref)
                writer.bullets(worked.get("reasoning_steps"), ref)
                writer.label("CHECK YOUR CHEMISTRY", ref)
                writer.bullets(worked.get("verification_steps"), ref)
            if section.get("verification_steps"):
                writer.label("VERIFY THE RESULT", ref)
                writer.bullets(section["verification_steps"], ref)
            writer.para(section.get("transfer_bridge"), ref)
            writer.rule()

        for ri, routine in enumerate(bucket.get("problem_family_routines") or [], 1):
            ref = f"C1A-B{bi:02d}-R{ri:02d}"
            writer.heading("Problem-solving routine", 2, ref)
            writer.para(routine.get("chemical_signature") or "Problem-solving routine", ref)
            writer.label("LOOK FOR", ref)
            writer.bullets(routine.get("recognition_signals"), ref)
            writer.label("STEP BY STEP", ref)
            writer.bullets(routine.get("method_steps"), ref)

        for pi, item in enumerate(bucket.get("practice_items") or [], 1):
            ref = f"C1A-B{bi:02d}-P{pi:02d}"
            _begin_semantic_block(
                writer,
                "Core (1A) practice",
                _core1a_attempt_height(writer, item["prompt"], 6),
            )
            writer.heading(f"Practice {pi}", 2, ref)
            writer.label("TRY IT FIRST", ref)
            writer.question_text(item["prompt"], ref)
            writer.workspace(6, ref)
            writer.para("Check your response on the next page.", ref)

            # Answer visibility remains next-page-or-later. The answer page itself is
            # content-first: it carries the governed question context and may also
            # host the next independent semantic block if space remains.
            writer.new_page("Core (1A) expected response")
            writer.heading(f"Practice {pi} — check", 2, ref + "-A")
            writer.label("QUESTION", ref + "-A-CONTEXT")
            writer.question_text(item["prompt"], ref + "-A-CONTEXT")
            rubric = item["answer_path"]["expected_response_rubric"]
            writer.label(rubric["learner_label"], ref + "-A")
            writer.bullets(rubric["criteria"], ref + "-A")

        gate = bucket.get("readiness_gate") or {}
        _begin_semantic_block(writer, "Core (1A) readiness", 150.0)
        writer.heading("READY TO MOVE ON?", 2)
        writer.para("Move to transfer practice when you can do all four without opening a representation or start hint.")
        writer.bullets([TOKEN_REPLACEMENTS.get(x, public_text(x)) for x in gate.get("required_dimensions", [])])

    metrics = writer.finish()
    metrics.update({
        "product": "CORE1A",
        "manuscript_ref": manuscript["manuscript_id"],
        "manuscript_digest": manuscript["manuscript_digest"],
        "representation_bundle_ref": representations["bundle_id"],
        "representation_bundle_digest": representations["bundle_digest"],
        "section_visual_closure": visual_rows,
        "pagination_mode": "CONTENT_FIRST",
    })
    metrics["pdf_sha256"] = sha_file(path)
    metrics["metrics_digest"] = digest({k: v for k, v in metrics.items() if k != "metrics_digest"})
    return metrics


def _source_context(item: dict[str, Any]) -> str:
    snap = item["source_snapshot"]
    rows = [snap["stem"]]
    rows.extend(f"{option.get('label', '')}. {option.get('text', '')}" for option in snap.get("options") or [])
    for subpart in snap.get("subparts") or []:
        if isinstance(subpart, str):
            rows.append(subpart)
        elif isinstance(subpart, dict):
            text = subpart.get("text") or subpart.get("prompt") or subpart.get("stem")
            if text:
                rows.append(text)
    if snap.get("condition_text"):
        rows.append("Recorded condition: " + str(snap["condition_text"]))
    return "\n".join(str(row) for row in rows if str(row).strip())


def _core2a_full_working_height(writer: PageWriter, full: dict[str, Any], question_context: str, *, repeat_context: bool) -> float:
    height = writer.section + 24.0
    if repeat_context:
        height += writer.small + 12.0 + _wrapped_height(writer, question_context, question=True) + 14.0
    height += _wrapped_list_height(writer, full.get("steps"), indent=8.0)
    height += writer.small + 12.0 + _wrapped_height(writer, full["verification"])
    return height + 18.0


def _answer_pages_content_first(writer: PageWriter, answer_path, title, ref, question_context: str):
    quick, full = answer_path.get("quick_check"), answer_path.get("full_working")
    if not quick or not full:
        raise ValueError("CHEM_LP_RENDER_ANSWER_NAVIGATION_MISSING:" + ref)

    # The quick check remains next-page-or-later, preserving attempt-first answer
    # visibility. Full working is ordered after quick check but is not forced onto a
    # separate page. If it cannot fit as one semantic block, the block moves intact.
    writer.new_page("answer check")
    writer.heading(title + " — QUICK CHECK", 2, ref + "-Q")
    writer.label("QUESTION", ref + "-Q-CONTEXT")
    writer.question_text(question_context, ref + "-Q-CONTEXT")
    writer.rule()
    writer.para(quick["answer_summary"], ref + "-Q")
    if quick.get("unit"):
        writer.para("Unit: " + public_text(quick["unit"]), ref + "-Q")
    writer.bullets(quick.get("marking_points"), ref + "-Q")
    writer.para("If your result does not match, return to the clues before opening the full working.", ref + "-Q")

    before = writer.page
    _begin_semantic_block(
        writer,
        "full working",
        _core2a_full_working_height(writer, full, question_context, repeat_context=False),
    )
    moved = writer.page != before
    writer.heading(title + " — FULL WORKING", 2, ref + "-F")
    if moved:
        writer.label("QUESTION", ref + "-F-CONTEXT")
        writer.question_text(question_context, ref + "-F-CONTEXT")
        writer.rule()
    writer.bullets(full["steps"], ref + "-F")
    writer.label("VERIFY", ref + "-F")
    writer.para(full["verification"], ref + "-F")


def _begin_core2a_attempt(writer: PageWriter, label: str, prompt: str, *, force_new: bool) -> None:
    if force_new:
        writer.new_page(label)
        return
    minimum = 250.0 + _wrapped_height(writer, prompt, question=True)
    _begin_semantic_block(writer, label, minimum)


def render_core2a_content_first(source_plan, challenge_plan, representations, policy, path):
    writer = PageWriter(path, "Chemistry Core (2A) — Source & Challenge Practice", policy)
    rep_index = representation_index(representations)
    visual_rows = []
    questions = 0
    writer.heading("Chemistry Core (2A)")
    writer.para("Attempt-first source practice followed by clearly labelled fresh challenge practice. Answers are separated from attempt pages so you can genuinely check your work.")
    writer.label("THE PRACTICE LOOP")
    writer.para("Try → use a clue only if needed → check the short answer → return to the question if wrong → open the full working.")

    first_attempt = True
    if source_plan:
        _begin_semantic_block(writer, "source practice", 90.0)
        writer.heading("SOURCE PRACTICE")
        writer.para("These questions preserve the governed source wording. Support is added around the question; the source itself is not silently rewritten.")
        for index, item in enumerate(source_plan["items"], 1):
            questions += 1
            ref = f"C2A-S-{index:03d}"
            context = _source_context(item)
            _begin_core2a_attempt(writer, "source question attempt", context, force_new=first_attempt)
            first_attempt = False
            writer.heading(f"Source question {index}", 2, ref)
            writer.label("TRY IT FIRST", ref)
            _source_prompt(writer, item, ref)
            _draw_provenance(writer, item["provenance"], ref)
            writer.workspace(5, ref)
            support = item["learner_support"]
            writer.label("SEE THE IDEA", ref)
            refs = list((support.get("see_the_idea") or {}).get("pre_taught_representation_refs") or [])
            snap = item["source_snapshot"]
            extra = {
                "observation": snap.get("stem"),
                "condition_context": [snap["condition_text"]] if snap.get("condition_text") else [],
                "particles": (snap.get("figure_semantic") or {}).get("particles") or [],
            }
            realized, unavailable = _visuals_for_refs(writer, refs, rep_index, ref, extra) if refs else (0, [])
            if refs and realized == 0:
                raise ValueError("CHEM_LP_RENDER_REQUIRED_VISUAL_MISSING:" + ref)
            visual_rows.append({
                "content_ref": ref,
                "required_refs": refs,
                "realized": realized,
                "unavailable_secondary_refs": unavailable,
                "status": "PASS",
            })
            _attempt_support(writer, support, ref)
            writer.para("Answer check: next page.", ref)
            _answer_pages_content_first(writer, item["answer_path"], f"Source question {index}", ref, context)

    if challenge_plan:
        _begin_semantic_block(writer, "fresh challenge practice", 90.0)
        writer.heading("FRESH CHALLENGE PRACTICE")
        writer.para("These are newly generated practice questions grounded in taught Chemistry. They are not claimed as official past-paper questions.")
        for index, item in enumerate(challenge_plan["items"], 1):
            questions += 1
            ref = f"C2A-G-{index:03d}"
            context = str(item["prompt"])
            _begin_core2a_attempt(writer, "fresh challenge attempt", context, force_new=first_attempt)
            first_attempt = False
            writer.heading(f"Fresh challenge {index}", 2, ref)
            writer.label("TRY IT FIRST", ref)
            writer.question_text(item["prompt"], ref)
            _draw_provenance(writer, item["provenance"], ref)
            writer.workspace(5, ref)
            support = item["learner_support"]
            writer.label("SEE THE IDEA", ref)
            refs = list(item["core1a_binding"].get("h2_evidence_refs") or [])
            realized, unavailable = _visuals_for_refs(writer, refs, rep_index, ref) if refs else (0, [])
            if refs and realized == 0:
                raise ValueError("CHEM_LP_RENDER_REQUIRED_VISUAL_MISSING:" + ref)
            visual_rows.append({
                "content_ref": ref,
                "required_refs": refs,
                "realized": realized,
                "unavailable_secondary_refs": unavailable,
                "status": "PASS",
            })
            _attempt_support(writer, support, ref)
            writer.para("Answer check: next page.", ref)
            _answer_pages_content_first(writer, item["answer_path"], f"Fresh challenge {index}", ref, context)

    metrics = writer.finish()
    metrics.update({
        "product": "CORE2A",
        "source_plan_ref": source_plan["plan_id"] if source_plan else None,
        "source_plan_digest": source_plan["plan_digest"] if source_plan else None,
        "challenge_plan_ref": challenge_plan["plan_id"] if challenge_plan else None,
        "challenge_plan_digest": challenge_plan["plan_digest"] if challenge_plan else None,
        "representation_bundle_ref": representations["bundle_id"],
        "representation_bundle_digest": representations["bundle_digest"],
        "question_count": questions,
        "item_visual_closure": visual_rows,
        "pagination_mode": "CONTENT_FIRST",
    })
    metrics["pdf_sha256"] = sha_file(path)
    metrics["metrics_digest"] = digest({k: v for k, v in metrics.items() if k != "metrics_digest"})
    return metrics
