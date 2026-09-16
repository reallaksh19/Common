#!/usr/bin/env python3
"""Content-first Chemistry Core1A/Core2A realization for unified Core custody.

Chemistry-bearing learner content remains in the semantic payload supplied by the
current repository Blueprint. This module owns only topic-neutral composition and
answer-navigation placement; it may not invent Chemistry or choose representations.
"""
from __future__ import annotations

from typing import Any

from chemistry_review_writer import ReviewWriter as PageWriter
from render_chemistry_learner_products import (
    BOLD,
    FONT,
    PAGE_H,
    TOKEN_REPLACEMENTS,
    _draw_provenance,
    _source_prompt,
    _visuals_for_refs,
    digest,
    public_text,
    representation_index,
    sha_file,
)


def _wrapped_height(writer: PageWriter, text: Any, *, question: bool = False, indent: float = 0.0) -> float:
    value = public_text(text)
    if question:
        lines = writer._wrap(value, FONT, writer.question, writer.width - indent)
        return len(lines) * writer.question_leading + 34.0
    lines = writer._wrap(value, FONT, writer.body, writer.width - indent)
    return len(lines) * writer.leading + 3.0


def _wrapped_list_height(writer: PageWriter, values: list[Any] | None, *, indent: float = 8.0) -> float:
    return sum(_wrapped_height(writer, "• " + public_text(value), indent=indent) for value in (values or []))


def _begin_semantic_block(writer: PageWriter, label: str, minimum_height: float, role: str | None = None) -> None:
    before = writer.page
    writer.ensure(minimum_height, label, role=role)
    if writer.page == before and writer.y < PAGE_H - writer.margin - 70:
        writer.rule()


def _core1a_attempt_height(writer: PageWriter, prompt: str, workspace_lines: int = 8) -> float:
    return writer.section + 24 + _wrapped_height(writer, prompt, question=True) + 34 + workspace_lines * 20 + 70


_ATTEMPT_SUPPORT_FIELDS = (
    ("WRITE THIS FIRST", "write_this_first", "CLUE_PANEL"),
    ("SMALL CLUE", "small_clue", "CLUE_PANEL"),
    ("BIGGER CLUE", "bigger_clue", "CLUE_PANEL"),
    ("HOW DO I START?", "how_do_i_start", "CLUE_PANEL"),
    ("WATCH FOR THIS", "watch_for_this", "CLUE_PANEL"),
    ("THINK IT THROUGH", "think_it_through", "CLUE_PANEL"),
    ("CHECK YOUR CHEMISTRY", "check_your_chemistry", "VERIFICATION_PANEL"),
)
_ANSWER_ROUTE_TEXT = "Complete the attempt first. The quick check starts on the next page."


def _support_text(value: Any) -> str:
    if value in (None, ""):
        return ""
    if isinstance(value, list):
        return "  •  ".join(public_text(item) for item in value if item not in (None, ""))
    return public_text(value)


def _semantic_panel_height(writer: PageWriter, title: str, text: str) -> float:
    """Mirror ReviewWriter._panel_text vertical geometry for atomic reservation."""
    inner_w = writer.width - 28
    title_rows = writer._wrap(public_text(title).upper(), BOLD, writer.small, inner_w)
    body_rows = writer._wrap(public_text(text), FONT, writer.body, inner_w)
    panel_height = 16.0 + len(title_rows) * (writer.small + 4.0) + len(body_rows) * writer.leading + 16.0
    return panel_height + 10.0


def _attempt_support_episode_height(writer: PageWriter, support: dict[str, Any]) -> float:
    """Measure the complete semantic support episode before emitting any panel."""
    total = 24.0
    for title, key, _kind in _ATTEMPT_SUPPORT_FIELDS:
        text = _support_text(support.get(key))
        if text:
            total += _semantic_panel_height(writer, title, text)
    total += _semantic_panel_height(writer, "ANSWER ROUTE", _ANSWER_ROUTE_TEXT)
    return total + 8.0


def _begin_attempt_support_episode(writer: PageWriter, support: dict[str, Any]) -> None:
    height = _attempt_support_episode_height(writer, support)
    maximum_fresh_page_height = PAGE_H - 54.0 - writer.margin - 8.0
    if height > maximum_fresh_page_height:
        raise ValueError("CHEM_LP_RENDER_SUPPORT_EPISODE_TOO_TALL")
    writer.ensure(height, "attempt support", role="QUESTION_EPISODE")
    writer.set_page_role("QUESTION_EPISODE")


def _render_attempt_support(writer: PageWriter, support: dict[str, Any], ref: str) -> None:
    """Render governed support as review-grade semantic surfaces, never raw filler."""
    for title, key, kind in _ATTEMPT_SUPPORT_FIELDS:
        text = _support_text(support.get(key))
        if not text:
            continue
        if kind == "VERIFICATION_PANEL":
            writer.verification_panel(title, text, ref)
        else:
            writer.clue_panel(title, text, ref)


def _joined(values: list[Any] | None) -> str:
    return "  •  ".join(public_text(x) for x in (values or []))


def render_core1a_content_first(manuscript, representations, policy, path):
    writer = PageWriter(path, "Chemistry Core (1A) — Learner Study Guide", policy)
    rep_index = representation_index(representations)
    visual_rows = []

    writer.heading("Chemistry Core (1A)")
    writer.para("A learner study guide built from the governed Chemistry teaching plan. Learn the idea, use the representation, practise, check your response, then move to transfer questions.")
    writer.route_panel(
        "HOW TO USE THIS BOOK",
        "Study the idea before the routine. Attempt every practice prompt before reading its expected response. Use the readiness check before moving to transfer practice.",
    )

    for bi, bucket in enumerate(manuscript["buckets"], 1):
        writer.new_page("Core (1A) bucket", role="CONCEPT_EXPLANATION")
        writer.heading(f"Part {bi} — {public_text(bucket['learner_title'])}")
        writer.concept_panel("THE IDEA THAT HOLDS THIS PART TOGETHER", bucket["bucket_invariant"])

        atoms = bucket.get("learning_atoms") or []
        sections = bucket.get("teaching_sections") or []
        if len(atoms) != len(sections):
            raise ValueError(
                f"CHEM_LP_RENDER_CORE1A_SECTION_ATOM_COUNT_MISMATCH:{len(sections)}:{len(atoms)}"
            )
        for si, (atom, section) in enumerate(zip(atoms, sections), 1):
            ref = f"C1A-B{bi:02d}-S{si:02d}"
            learner_heading = public_text(atom.get("learner_title"))
            if not learner_heading:
                raise ValueError(f"CHEM_LP_RENDER_CORE1A_ATOM_TITLE_REQUIRED:{bi}:{si}")
            writer.heading(learner_heading, 2, ref)
            writer.concept_panel("SEE THE IDEA", section.get("see") or section.get("activation"), ref)
            writer.label("EXPLAIN", ref)
            writer.bullets(section.get("explain"), ref)
            refs = list(section.get("representation_refs") or [])
            realized, unavailable = _visuals_for_refs(writer, refs, rep_index, ref)
            if refs and realized == 0:
                raise ValueError("CHEM_LP_RENDER_REQUIRED_VISUAL_MISSING:" + ref)
            visual_rows.append({
                "content_ref": ref,
                "learning_atom_ref": atom.get("atom_id"),
                "learner_heading": learner_heading,
                "required_refs": refs,
                "realized": realized,
                "unavailable_secondary_refs": unavailable,
                "status": "PASS",
            })
            if section.get("watch_one"):
                writer.concept_panel("WATCH ONE", section["watch_one"], ref)
            worked = section.get("worked_example")
            if worked:
                writer.label("WORKED EXAMPLE", ref)
                writer.question_text(worked.get("prompt", ""), ref)
                writer.bullets(worked.get("reasoning_steps"), ref)
                if worked.get("verification_steps"):
                    writer.verification_panel("CHECK YOUR CHEMISTRY", _joined(worked.get("verification_steps")), ref)
            if section.get("verification_steps"):
                writer.verification_panel("VERIFY THE RESULT", _joined(section["verification_steps"]), ref)
            if section.get("transfer_bridge"):
                writer.action_panel("YOUR MOVE", section["transfer_bridge"], ref)
            writer.rule()

        for ri, routine in enumerate(bucket.get("problem_family_routines") or [], 1):
            ref = f"C1A-B{bi:02d}-R{ri:02d}"
            writer.heading("Problem-solving routine", 2, ref)
            writer.concept_panel("CHEMICAL SIGNATURE", routine.get("chemical_signature") or "Problem-solving routine", ref)
            writer.label("LOOK FOR", ref)
            writer.bullets(routine.get("recognition_signals"), ref)
            writer.label("STEP BY STEP", ref)
            writer.bullets(routine.get("method_steps"), ref)
            if routine.get("common_fatal_errors"):
                writer.action_panel("AVOID THIS", _joined(routine.get("common_fatal_errors")), ref)

        for pi, item in enumerate(bucket.get("practice_items") or [], 1):
            ref = f"C1A-B{bi:02d}-P{pi:02d}"
            _begin_semantic_block(
                writer,
                "Core (1A) practice",
                _core1a_attempt_height(writer, item["prompt"], 8),
                role="PRACTICE",
            )
            writer.set_page_role("PRACTICE")
            writer.heading(f"Practice {pi}", 2, ref)
            writer.label("TRY IT FIRST", ref)
            writer.question_text(item["prompt"], ref)
            writer.workspace(8, ref)
            writer.action_panel("CHECK ROUTE", "Finish your own response first. The expected response begins on the next page.", ref)

            writer.new_page("Core (1A) expected response", role="SOLUTION")
            writer.heading(f"Practice {pi} — check", 2, ref + "-A")
            writer.question_text(item["prompt"], ref + "-A-CONTEXT")
            rubric = item["answer_path"]["expected_response_rubric"]
            writer.answer_panel(rubric["learner_label"], _joined(rubric["criteria"]), ref + "-A")
            writer.verification_panel("SELF-CHECK", "Compare the reasoning in your response with every criterion above before moving on.", ref + "-A")

        gate = bucket.get("readiness_gate") or {}
        _begin_semantic_block(writer, "Core (1A) readiness", 230.0, role="SUMMARY_OR_HANDOUT")
        writer.set_page_role("SUMMARY_OR_HANDOUT")
        writer.heading("READY TO MOVE ON?", 2)
        writer.action_panel("READINESS RULE", "Move to transfer practice when you can complete these checks without opening a representation or start hint.")
        dimensions = [TOKEN_REPLACEMENTS.get(x, public_text(x)) for x in gate.get("required_dimensions", [])]
        if dimensions:
            writer.route_panel("CHECKLIST", _joined(dimensions))

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
    height = writer.section + 28.0
    if repeat_context:
        height += _wrapped_height(writer, question_context, question=True) + 18.0
    height += _wrapped_list_height(writer, full.get("steps"), indent=8.0)
    height += 70.0 + _wrapped_height(writer, full["verification"])
    return height


def _answer_pages_content_first(writer: PageWriter, answer_path, title, ref, question_context: str):
    quick, full = answer_path.get("quick_check"), answer_path.get("full_working")
    if not quick or not full:
        raise ValueError("CHEM_LP_RENDER_ANSWER_NAVIGATION_MISSING:" + ref)

    writer.new_page("answer check", role="SOLUTION")
    writer.heading(title + " — QUICK CHECK", 2, ref + "-Q")
    writer.question_text(question_context, ref + "-Q-CONTEXT")
    summary = public_text(quick["answer_summary"])
    if quick.get("unit"):
        summary += "  Unit: " + public_text(quick["unit"])
    if quick.get("marking_points"):
        summary += "  •  " + _joined(quick.get("marking_points"))
    writer.answer_panel("QUICK CHECK", summary, ref + "-Q")
    writer.action_panel("IF IT DOES NOT MATCH", "Return to the clues, repair the first point where your reasoning changed, then try the question again before reading the full working.", ref + "-Q")

    before = writer.page
    _begin_semantic_block(
        writer,
        "full working",
        _core2a_full_working_height(writer, full, question_context, repeat_context=False),
        role="SOLUTION",
    )
    moved = writer.page != before
    writer.heading(title + " — FULL WORKING", 2, ref + "-F")
    if moved:
        writer.question_text(question_context, ref + "-F-CONTEXT")
    writer.label("WHY THESE STEPS", ref + "-F")
    writer.bullets(full["steps"], ref + "-F")
    writer.verification_panel("VERIFY", full["verification"], ref + "-F")
    writer.action_panel("RETRY", "Cover the working and reproduce the first move and verification independently.", ref + "-F")


def _begin_core2a_attempt(writer: PageWriter, label: str, prompt: str, *, force_new: bool) -> None:
    if force_new:
        writer.new_page(label, role="QUESTION_EPISODE")
        return
    minimum = 300.0 + _wrapped_height(writer, prompt, question=True)
    _begin_semantic_block(writer, label, minimum, role="QUESTION_EPISODE")
    writer.set_page_role("QUESTION_EPISODE")


def render_core2a_content_first(source_plan, challenge_plan, representations, policy, path):
    writer = PageWriter(path, "Chemistry Core (2A) — Source & Challenge Practice", policy)
    rep_index = representation_index(representations)
    visual_rows = []
    questions = 0
    writer.heading("Chemistry Core (2A)")
    writer.para("Attempt-first source practice followed by clearly labelled fresh challenge practice. Answers are separated from attempt pages so you can genuinely check your work.")
    writer.route_panel("THE PRACTICE LOOP", "Try the question → use a clue only if needed → check the short answer → repair your reasoning → study the full working → verify independently.")

    first_attempt = True
    if source_plan:
        _begin_semantic_block(writer, "source practice", 110.0, role="ROUTE_OR_MAP")
        writer.heading("SOURCE PRACTICE")
        writer.route_panel("SOURCE CUSTODY", "These questions preserve the governed source wording. Support is added around the question; the source itself is not silently rewritten.")
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
            _begin_attempt_support_episode(writer, support)
            _render_attempt_support(writer, support, ref)
            writer.action_panel("ANSWER ROUTE", _ANSWER_ROUTE_TEXT, ref)
            _answer_pages_content_first(writer, item["answer_path"], f"Source question {index}", ref, context)

    if challenge_plan:
        _begin_semantic_block(writer, "fresh challenge practice", 120.0, role="ROUTE_OR_MAP")
        writer.heading("FRESH CHALLENGE PRACTICE")
        writer.route_panel("FRESH PRACTICE", "These are newly generated practice questions grounded in taught Chemistry. They are not claimed as official past-paper questions.")
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
            _begin_attempt_support_episode(writer, support)
            _render_attempt_support(writer, support, ref)
            writer.action_panel("ANSWER ROUTE", _ANSWER_ROUTE_TEXT, ref)
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
