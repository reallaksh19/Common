#!/usr/bin/env python3
"""Review-grade Core1A composition with topic-neutral learner work on every page.

This module changes only page composition. Chemistry content, representation choice,
and scientific runtime facts remain upstream governed authority. Sparse answer/routine
pages are repaired by adding task-bound rehearsal, correction, and readiness evidence
workspaces rather than by weakening review thresholds or inventing Chemistry.
"""
from __future__ import annotations

from chemistry_review_writer import ReviewWriter as PageWriter
from render_chemistry_a_content_first import (
    _begin_semantic_block,
    _core1a_attempt_height,
    _joined,
)
from render_chemistry_learner_products import (
    TOKEN_REPLACEMENTS,
    _visuals_for_refs,
    digest,
    public_text,
    representation_index,
    sha_file,
)


def render_core1a_content_first(manuscript, representations, policy, path):
    writer = PageWriter(path, "Chemistry Core (1A) — Learner Study Guide", policy)
    rep_index = representation_index(representations)
    visual_rows = []

    writer.heading("Chemistry Core (1A)")
    writer.para(
        "A learner study guide built from the governed Chemistry teaching plan. "
        "Learn the idea, use the representation, practise, check your response, then move to transfer questions."
    )
    writer.route_panel(
        "HOW TO USE THIS BOOK",
        "Study the idea before the routine. Attempt every practice prompt before reading its expected response. "
        "Use the readiness check before moving to transfer practice.",
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
                    writer.verification_panel(
                        "CHECK YOUR CHEMISTRY",
                        _joined(worked.get("verification_steps")),
                        ref,
                    )
            if section.get("verification_steps"):
                writer.verification_panel("VERIFY THE RESULT", _joined(section["verification_steps"]), ref)
            if section.get("transfer_bridge"):
                writer.action_panel("YOUR MOVE", section["transfer_bridge"], ref)
            writer.rule()

        for ri, routine in enumerate(bucket.get("problem_family_routines") or [], 1):
            ref = f"C1A-B{bi:02d}-R{ri:02d}"
            writer.heading("Problem-solving routine", 2, ref)
            writer.concept_panel(
                "CHEMICAL SIGNATURE",
                routine.get("chemical_signature") or "Problem-solving routine",
                ref,
            )
            writer.label("LOOK FOR", ref)
            writer.bullets(routine.get("recognition_signals"), ref)
            writer.label("STEP BY STEP", ref)
            writer.bullets(routine.get("method_steps"), ref)
            if routine.get("common_fatal_errors"):
                writer.action_panel("AVOID THIS", _joined(routine.get("common_fatal_errors")), ref)
            writer.action_panel(
                "REHEARSE THE ROUTINE",
                "Before starting practice, write the recognition signal and first technical move you will use. "
                "Do not copy a worked answer.",
                ref + "-REHEARSE",
            )
            writer.workspace(5, ref + "-REHEARSE")

        for pi, item in enumerate(bucket.get("practice_items") or [], 1):
            ref = f"C1A-B{bi:02d}-P{pi:02d}"
            _begin_semantic_block(
                writer,
                "Core (1A) practice",
                _core1a_attempt_height(writer, item["prompt"], 9),
                role="PRACTICE",
            )
            writer.set_page_role("PRACTICE")
            writer.heading(f"Practice {pi}", 2, ref)
            writer.label("TRY IT FIRST", ref)
            writer.question_text(item["prompt"], ref)
            writer.workspace(9, ref)
            writer.action_panel(
                "CHECK ROUTE",
                "Finish your own response first. The expected response begins on the next page.",
                ref,
            )

            writer.new_page("Core (1A) expected response", role="SOLUTION")
            writer.heading(f"Practice {pi} — check", 2, ref + "-A")
            writer.question_text(item["prompt"], ref + "-A-CONTEXT")
            rubric = item["answer_path"]["expected_response_rubric"]
            writer.answer_panel(rubric["learner_label"], _joined(rubric["criteria"]), ref + "-A")
            writer.verification_panel(
                "SELF-CHECK",
                "Compare the reasoning in your response with every criterion above before moving on.",
                ref + "-A",
            )
            writer.action_panel(
                "REPAIR & RETRY",
                "If any criterion was missing or incorrect, rewrite the corrected response below before continuing.",
                ref + "-A-RETRY",
            )
            writer.workspace(5, ref + "-A-RETRY")

        gate = bucket.get("readiness_gate") or {}
        _begin_semantic_block(writer, "Core (1A) readiness", 420.0, role="SUMMARY_OR_HANDOUT")
        writer.set_page_role("SUMMARY_OR_HANDOUT")
        writer.heading("READY TO MOVE ON?", 2)
        writer.action_panel(
            "READINESS RULE",
            "Move to transfer practice when you can complete these checks without opening a representation or start hint.",
        )
        dimensions = [TOKEN_REPLACEMENTS.get(x, public_text(x)) for x in gate.get("required_dimensions", [])]
        if dimensions:
            writer.route_panel("CHECKLIST", _joined(dimensions))
        writer.action_panel(
            "SHOW YOUR EVIDENCE",
            "For each checklist item, record the evidence that you can perform it independently. "
            "If you need a representation or start hint, return to the corresponding study section before transfer practice.",
        )
        writer.workspace(10, "C1A-READINESS-EVIDENCE")

    metrics = writer.finish()
    metrics.update({
        "product": "CORE1A",
        "manuscript_ref": manuscript["manuscript_id"],
        "manuscript_digest": manuscript["manuscript_digest"],
        "representation_bundle_ref": representations["bundle_id"],
        "representation_bundle_digest": representations["bundle_digest"],
        "section_visual_closure": visual_rows,
        "pagination_mode": "CONTENT_FIRST",
        "review_composition_mode": "TASK_BOUND_WORKSPACE",
    })
    metrics["pdf_sha256"] = sha_file(path)
    metrics["metrics_digest"] = digest({k: v for k, v in metrics.items() if k != "metrics_digest"})
    return metrics
