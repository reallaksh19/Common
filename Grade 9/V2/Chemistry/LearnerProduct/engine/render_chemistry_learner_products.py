#!/usr/bin/env python3
"""Deterministic Chemistry Core (1A) / Core (2A) PDF realization.

The renderer consumes only the closed semantic learner-product package plus the
C-H RepresentationBundle. It does not select representations and it does not
invent Chemistry. Selected C-H primitives are handed to the existing Chemistry
vector primitive renderer; unavailable secondary primitives are recorded, while
each teaching section / question must still realize at least one reasoning visual
when its governed representation evidence is renderable.

Every visible text run passes through the existing learner-surface identifier
guard. Physical text/primitive rectangles are recorded while drawing so the
visual-preflight stage can check the actual page geometry rather than a plan.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas

HERE = Path(__file__).resolve()
LP_ROOT = HERE.parents[1]
CHEM_ROOT = LP_ROOT.parent
sys.path.insert(0, str(CHEM_ROOT / "ExactProduct" / "engine"))

import chemistry_visual_primitives as VP  # noqa: E402
import learner_surface_guard as GUARD  # noqa: E402

PAGE_W, PAGE_H = A4
FONT = "DejaVuSans"
BOLD = "DejaVuSans-Bold"

CAPABILITY_TITLES = {
    "CAP-READ-FORMULA": "Read a chemical formula before calculating",
    "CAP-PARSE-ION-CHARGE": "Separate ionic charge from subscripts",
    "CAP-TRANSLATE-PARTICLE-SYMBOL": "Translate between particles and symbols",
    "CAP-CHECK-ATOM-CONSERVATION": "Check atom conservation explicitly",
    "CAP-CLASSIFY-CHANGE-EVIDENCE": "Classify a change from the stated evidence",
    "CAP-CHECK-RULE-EXCEPTION": "Check the rule, condition and exception",
    "CAP-PRESERVE-REACTION-CONDITION": "Keep reaction conditions attached",
    "CAP-SEPARATE-OBSERVATION-INFERENCE": "Separate observation from inference",
    "CAP-READ-APPARATUS-METHOD": "Connect apparatus, property and method",
    "CAP-TRACK-REACTING-SPECIES": "Track the same reacting species",
    "CAP-ATTACH-SPECIES-ROLE": "Attach a role only after tracking the species",
    "CAP-VERIFY-CHEMICAL-REPRESENTATION": "Verify a chemical representation before accepting it",
    "CAP-READ-STRUCTURE-SITE": "Track the exact structural site",
    "CAP-TRACK-OXIDATION-STATE": "Track oxidation-state change",
}

TOKEN_REPLACEMENTS = {
    "READ_GIVEN": "Read the given information exactly as shown.",
    "IDENTIFY_CHEMICAL_ENTITIES": "Identify the chemical entities that must be tracked.",
    "PARSE_FORMULA_OR_EQUATION": "Read coefficients, subscripts, charges and equation sides in their correct positions.",
    "IDENTIFY_REPRESENTATION_LEVEL": "Identify whether the information is macroscopic, particulate or symbolic.",
    "TRANSLATE_REPRESENTATION": "Translate the representation without changing chemical identity or count.",
    "INTERPRET_CHEMICAL_MEANING": "State what the representation means chemically.",
    "APPLY_CONSERVATION": "Apply the required conservation check.",
    "TRACK_SPECIES_OR_STATE_CHANGE": "Track the same species or state from before to after.",
    "CLASSIFY": "Classify only after the decisive evidence is established.",
    "CHECK_ATOMS": "Count each required atom on both sides.",
    "CHECK_CHARGE": "Check charge explicitly.",
    "CHECK_SPECIES_IDENTITY": "Check that the same chemical species is being tracked.",
    "CHECK_CONDITIONS": "Check that every stated condition or exception is still attached.",
    "VERIFY_RESULT": "Run an independent Chemistry check before accepting the result.",
    "RECOGNISE": "Recognise the problem family.",
    "REPRESENT": "Choose or build the useful representation.",
    "FIRST_MOVE": "Choose the first useful move without a start hint.",
    "FINISH_AND_VERIFY": "Finish the problem and verify the Chemistry.",
}

EXACT_REPLACEMENTS = {
    "Decision support cannot add chemistry beyond the active StudyModel.": "Use only the Chemistry stated or taught for this task.",
    "The active conservation ledger comes from source/problem-family authority.": "Use the conservation check required by this question.",
    "Original external transfer remains reserved for Core2.": "Attempt the transfer questions after this learning step.",
    "Provide no procedural cue beyond the task and source-authorized representation.": "Try it independently using only the information in the task.",
    "Use explicit first-move and representation cues.": "Use the first-move and representation cues shown here.",
    "Remove one supplied cue and require the learner to choose the next move.": "One cue has been removed; choose the next move yourself.",
}


def load(path: Path | str) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def canonical(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(obj: Any) -> str:
    return hashlib.sha256(canonical(obj).encode("utf-8")).hexdigest()


def sha_file(path: Path | str) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def register_fonts() -> None:
    pairs = [
        ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
        ("/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf", "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"),
    ]
    for regular, bold in pairs:
        if Path(regular).exists() and Path(bold).exists():
            pdfmetrics.registerFont(TTFont(FONT, regular))
            pdfmetrics.registerFont(TTFont(BOLD, bold))
            VP.use_fonts(FONT, BOLD)
            return
    raise RuntimeError("CHEM_LP_RENDER_UNICODE_FONT_UNAVAILABLE")


def capability_title(ref: str) -> str:
    if ref in CAPABILITY_TITLES:
        return CAPABILITY_TITLES[ref]
    if ref.startswith("CAP-"):
        return ref[4:].replace("-", " ").strip().capitalize()
    return "Chemistry skill"


def _humanize_identifier(token: str) -> str:
    if token in TOKEN_REPLACEMENTS:
        return TOKEN_REPLACEMENTS[token]
    for prefix in ("CAP-", "PF-", "QF-", "REP-", "PCK-", "CHEM-CONCEPT-", "CHEM-"):
        if token.startswith(prefix):
            value = token[len(prefix):].replace("-", " ").replace("_", " ").strip().lower()
            return value[:1].upper() + value[1:] if value else "Chemistry idea"
    if token.startswith("OBLIGATION_LEVEL:"):
        return "Use the " + token.split(":", 1)[1].replace("_", " ").lower() + " representation level."
    if token.startswith("OBLIGATION_REP:"):
        return "Use the " + token.split(":", 1)[1].replace("_", " ").lower() + " representation."
    if "_" in token and token.upper() == token:
        value = token.replace("_", " ").lower()
        return value[:1].upper() + value[1:] + "."
    raise ValueError("CHEM_LP_RENDER_INTERNAL_ID_LEAK:" + token)


def public_text(value: Any) -> str:
    text = str(value or "")
    for old, new in EXACT_REPLACEMENTS.items():
        text = text.replace(old, new)
    # Replace only identifier-shaped tokens already identified by the repository
    # firewall. Unknown shapes fail closed rather than being silently hidden.
    for token in GUARD.find_internal_identifiers(text):
        text = text.replace(token, _humanize_identifier(token))
    GUARD.assert_learner_safe(text, "learner product")
    return text


def public_list(values: list[Any] | None) -> list[str]:
    return [public_text(x) for x in (values or [])]


def representation_index(bundle: dict[str, Any]) -> dict[str, dict[str, Any]]:
    rows = bundle.get("representations", [])
    out = {r["representation_id"]: r for r in rows}
    if len(out) != len(rows):
        raise ValueError("CHEM_LP_RENDER_REPRESENTATION_ID_DUPLICATE")
    return out


def params_from_representation(rep: dict[str, Any], extra: dict[str, Any] | None = None) -> dict[str, Any]:
    extra = extra or {}
    data = rep.get("source_semantic_data") or {}
    return VP.build_params(
        primitive_id=rep["primitive_id"],
        tokens=extra.get("tokens") or rep.get("notation_tokens") or rep.get("chemical_entities") or [],
        declared_entities=rep.get("chemical_entities") or data.get("chemical_entities") or [],
        instructional_job=public_text(rep.get("instructional_job", "")),
        attention_target=public_text(rep.get("attention_target", "")),
        learner_action=public_text(rep.get("learner_action_expected", "")),
        condition_context=public_list(extra.get("condition_context") or rep.get("condition_exception_context") or []),
        species_roles=public_list(rep.get("species_roles") or []),
        checks=public_list(data.get("verification_requirements") or []),
        observation=public_text(extra.get("observation", "")) if extra.get("observation") else None,
        oxidation_states=data.get("oxidation_states") or [],
        particles=extra.get("particles") or [],
        site_labels=data.get("site_labels") or [],
        accessibility_text=public_text(rep.get("accessibility_text", "")),
        safe=public_text,
    )


class PageWriter:
    def __init__(self, path: Path, title: str, policy: dict[str, Any]):
        register_fonts()
        page = policy["page"]
        self.path = Path(path)
        self.title = title
        self.margin = float(page["margin_pt"])
        self.body = float(page["body_font_pt"])
        self.leading = float(page["body_leading_pt"])
        self.question = float(page["question_font_pt"])
        self.question_leading = float(page["question_leading_pt"])
        self.small = float(page["small_label_font_pt"])
        self.section = float(page["section_heading_font_pt"])
        self.chapter = float(page["chapter_heading_font_pt"])
        self.minimum_font = 999.0
        self.c = canvas.Canvas(str(path), pagesize=A4, invariant=1, pageCompression=1)
        self.c.setTitle(title)
        self.c.setAuthor("Chemistry V2 LearnerProduct deterministic renderer")
        self.page = 0
        self.y = 0.0
        self.draw_ops: list[dict[str, Any]] = []
        self.primitives: list[dict[str, Any]] = []
        self.unavailable_primitives: list[dict[str, Any]] = []
        self.page_labels: list[dict[str, Any]] = []
        self.new_page("cover")

    @property
    def width(self) -> float:
        return PAGE_W - 2 * self.margin

    def _record(self, kind: str, x0: float, y0: float, x1: float, y1: float, text: str | None = None, font: float | None = None, ref: str | None = None) -> None:
        self.draw_ops.append({
            "page": self.page,
            "kind": kind,
            "x0": round(float(x0), 2), "y0": round(float(y0), 2),
            "x1": round(float(x1), 2), "y1": round(float(y1), 2),
            "text": text, "font_pt": font, "content_ref": ref,
        })
        if font is not None:
            self.minimum_font = min(self.minimum_font, float(font))

    def new_page(self, label: str) -> None:
        if self.page:
            self.c.showPage()
        self.page += 1
        self.y = PAGE_H - self.margin
        footer = f"Chemistry V2 | {self.page}"
        self.c.setFont(FONT, self.small)
        GUARD.assert_learner_safe(footer, "footer")
        self.c.drawRightString(PAGE_W - self.margin, 24, footer)
        self._record("FOOTER", PAGE_W - self.margin - stringWidth(footer, FONT, self.small), 20, PAGE_W - self.margin, 20 + self.small + 2, footer, self.small)
        self.page_labels.append({"page": self.page, "label": public_text(label)})

    def ensure(self, height: float, label: str = "continuation") -> None:
        if self.y - height < self.margin:
            self.new_page(label)

    def _wrap(self, text: str, font: str, size: float, width: float) -> list[str]:
        words = public_text(text).replace("\n", " \n ").split()
        lines: list[str] = []
        current = ""
        for word in words:
            if word == "\n":
                if current:
                    lines.append(current)
                    current = ""
                lines.append("")
                continue
            trial = (current + " " + word).strip()
            if stringWidth(trial, font, size) <= width:
                current = trial
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)
        return lines or [""]

    def line(self, text: str, size: float | None = None, font: str = FONT, indent: float = 0.0, leading: float | None = None, ref: str | None = None) -> None:
        size = float(size or self.body)
        leading = float(leading or self.leading)
        safe = public_text(text)
        for row in self._wrap(safe, font, size, self.width - indent):
            self.ensure(leading + 2)
            x = self.margin + indent
            self.c.setFont(font, size)
            self.c.drawString(x, self.y, row)
            w = stringWidth(row, font, size)
            self._record("TEXT", x, self.y - size * 0.25, x + w, self.y + size, row, size, ref)
            self.y -= leading
        self.y -= 3

    def heading(self, text: str, level: int = 1, ref: str | None = None) -> None:
        size = self.chapter if level == 1 else self.section
        self.ensure(size + 18, text)
        self.line(text, size=size, font=BOLD, leading=size + 5, ref=ref)

    def label(self, text: str, ref: str | None = None) -> None:
        self.ensure(self.small + 8)
        self.line(text, size=self.small, font=BOLD, leading=self.small + 4, ref=ref)

    def para(self, text: Any, ref: str | None = None) -> None:
        if text in (None, ""):
            return
        self.line(public_text(text), ref=ref)

    def question_text(self, text: Any, ref: str | None = None) -> None:
        self.line(public_text(text), size=self.question, font=FONT, leading=self.question_leading, ref=ref)

    def bullets(self, values: list[Any] | None, ref: str | None = None) -> None:
        for value in values or []:
            self.line("• " + public_text(value), indent=8, ref=ref)

    def rule(self) -> None:
        self.ensure(8)
        self.c.setLineWidth(0.7)
        self.c.line(self.margin, self.y, PAGE_W - self.margin, self.y)
        self._record("RULE", self.margin, self.y - 0.5, PAGE_W - self.margin, self.y + 0.5)
        self.y -= 10

    def workspace(self, lines: int = 5, ref: str | None = None) -> None:
        self.label("WORKSPACE", ref)
        for _ in range(lines):
            self.ensure(18)
            y = self.y - 6
            self.c.setLineWidth(0.35)
            self.c.line(self.margin, y, PAGE_W - self.margin, y)
            self._record("WORKSPACE_LINE", self.margin, y - 0.5, PAGE_W - self.margin, y + 0.5, ref=ref)
            self.y -= 18

    def primitive(self, rep: dict[str, Any], ref: str, extra: dict[str, Any] | None = None) -> bool:
        kind = rep["primitive_id"]
        params = params_from_representation(rep, extra)
        try:
            height = float(VP.primitive_height(kind, params, self.width))
        except VP.PrimitiveDataUnavailable as exc:
            self.unavailable_primitives.append({"page": self.page, "content_ref": ref, "representation_ref": rep["representation_id"], "primitive_id": kind, "reason": str(exc)})
            return False
        self.ensure(height + 10, "reasoning visual")
        try:
            record = VP.render_primitive(kind, params, self.c, (self.margin, self.y - height, self.width, height))
        except VP.PrimitiveDataUnavailable as exc:
            self.unavailable_primitives.append({"page": self.page, "content_ref": ref, "representation_ref": rep["representation_id"], "primitive_id": kind, "reason": str(exc)})
            return False
        self._record("PRIMITIVE", self.margin, self.y - height, PAGE_W - self.margin, self.y, ref=ref)
        self.primitives.append(dict(record, page=self.page, content_ref=ref, representation_ref=rep["representation_id"]))
        self.y -= height + 10
        return True

    def finish(self) -> dict[str, Any]:
        self.c.save()
        return {
            "pdf": self.path.name,
            "page_count": self.page,
            "minimum_visible_font_pt": round(self.minimum_font, 2),
            "page_size_pt": [round(PAGE_W, 3), round(PAGE_H, 3)],
            "draw_ops": self.draw_ops,
            "primitives": self.primitives,
            "unavailable_primitives": self.unavailable_primitives,
            "page_labels": self.page_labels,
        }


def _visuals_for_refs(writer: PageWriter, refs: list[str], rep_index: dict[str, dict[str, Any]], content_ref: str, extra: dict[str, Any] | None = None) -> tuple[int, list[str]]:
    realized = 0
    unavailable: list[str] = []
    for ref in refs:
        rep = rep_index.get(ref)
        if rep is None:
            raise ValueError("CHEM_LP_RENDER_REPRESENTATION_REF_MISSING:" + ref)
        if writer.primitive(rep, content_ref + ":" + ref, extra):
            realized += 1
        else:
            unavailable.append(ref)
    return realized, unavailable


def _routine_title(row: dict[str, Any]) -> str:
    signature = str(row.get("chemical_signature") or "").strip().rstrip(".")
    return public_text(signature or "Problem-solving routine")


def render_core1a(manuscript: dict[str, Any], representations: dict[str, Any], policy: dict[str, Any], path: Path) -> dict[str, Any]:
    writer = PageWriter(path, "Chemistry Core (1A) — Learner Study Guide", policy)
    rep_index = representation_index(representations)
    section_visuals: list[dict[str, Any]] = []

    writer.heading("Chemistry Core (1A)", 1)
    writer.para("A learner study guide built from the governed Chemistry teaching plan. Learn the idea, use the representation, practise, check your response, then move to transfer questions.")
    writer.label("HOW TO USE THIS BOOK")
    writer.bullets(["Study the idea before the routine.", "Attempt every practice prompt before reading its expected response.", "Use the readiness check before moving to transfer practice."])

    for b_index, bucket in enumerate(manuscript["buckets"], 1):
        writer.new_page("Core (1A) bucket")
        writer.heading(f"Part {b_index} — {public_text(bucket['learner_title'])}", 1)
        writer.label("THE IDEA THAT HOLDS THIS PART TOGETHER")
        writer.para(bucket["bucket_invariant"])

        for s_index, section in enumerate(bucket["teaching_sections"], 1):
            section_ref = f"C1A-B{b_index:02d}-S{s_index:02d}"
            writer.heading(capability_title(section["capability_ref"]), 2, section_ref)
            writer.label("SEE THE IDEA", section_ref)
            writer.para(section.get("see") or section.get("activation"), section_ref)
            writer.label("EXPLAIN", section_ref)
            writer.bullets(section.get("explain"), section_ref)
            refs = list(section.get("representation_refs") or [])
            realized, unavailable = _visuals_for_refs(writer, refs, rep_index, section_ref)
            supported = bool(refs)
            if supported and realized == 0:
                raise ValueError("CHEM_LP_RENDER_REQUIRED_VISUAL_MISSING:" + section_ref)
            section_visuals.append({"content_ref": section_ref, "required_refs": refs, "realized": realized, "unavailable_secondary_refs": unavailable, "status": "PASS"})

            if section.get("watch_one"):
                writer.label("WATCH ONE", section_ref)
                writer.para(section["watch_one"], section_ref)
            worked = section.get("worked_example")
            if worked:
                writer.label("WORKED EXAMPLE", section_ref)
                writer.question_text(worked.get("prompt", ""), section_ref)
                writer.bullets(worked.get("reasoning_steps"), section_ref)
                writer.label("CHECK YOUR CHEMISTRY", section_ref)
                writer.bullets(worked.get("verification_steps"), section_ref)
            if section.get("verification_steps"):
                writer.label("VERIFY THE RESULT", section_ref)
                writer.bullets(section["verification_steps"], section_ref)
            writer.para(section.get("transfer_bridge"), section_ref)
            writer.rule()

        for r_index, routine in enumerate(bucket.get("problem_family_routines") or [], 1):
            ref = f"C1A-B{b_index:02d}-R{r_index:02d}"
            writer.heading("Problem-solving routine", 2, ref)
            writer.para(_routine_title(routine), ref)
            writer.label("LOOK FOR", ref)
            writer.bullets(routine.get("recognition_signals"), ref)
            writer.label("STEP BY STEP", ref)
            writer.bullets(routine.get("method_steps"), ref)

        for p_index, item in enumerate(bucket.get("practice_items") or [], 1):
            ref = f"C1A-B{b_index:02d}-P{p_index:02d}"
            writer.new_page("Core (1A) practice")
            writer.heading(f"Practice {p_index}", 2, ref)
            writer.label("TRY IT FIRST", ref)
            writer.question_text(item["prompt"], ref)
            writer.workspace(6, ref)
            writer.para("Check your response on the next page.", ref)
            writer.new_page("Core (1A) expected response")
            writer.heading(f"Practice {p_index} — check", 2, ref + "-A")
            rubric = item["answer_path"]["expected_response_rubric"]
            writer.label(rubric["learner_label"], ref + "-A")
            writer.bullets(rubric["criteria"], ref + "-A")

        gate = bucket.get("readiness_gate") or {}
        writer.new_page("Core (1A) readiness")
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
        "section_visual_closure": section_visuals,
    })
    metrics["pdf_sha256"] = sha_file(path)
    metrics["metrics_digest"] = digest({k: v for k, v in metrics.items() if k != "metrics_digest"})
    return metrics


def _draw_provenance(writer: PageWriter, provenance: dict[str, Any], ref: str) -> None:
    writer.label("WHERE THIS QUESTION CAME FROM", ref)
    for citation in provenance.get("citations") or []:
        label = public_text(citation.get("label", ""))
        locator = public_text(citation.get("locator", ""))
        text = label + (" — " + locator if locator else "")
        writer.para(text, ref)


def _source_prompt(writer: PageWriter, item: dict[str, Any], ref: str) -> None:
    snap = item["source_snapshot"]
    writer.question_text(snap["stem"], ref)
    for option in snap.get("options") or []:
        writer.para(f"{option.get('label', '')}. {option.get('text', '')}", ref)
    for subpart in snap.get("subparts") or []:
        writer.para(subpart if isinstance(subpart, str) else canonical(subpart), ref)
    if snap.get("condition_text"):
        writer.para("Recorded condition: " + public_text(snap["condition_text"]), ref)


def _attempt_support(writer: PageWriter, support: dict[str, Any], ref: str) -> None:
    writer.label("WRITE THIS FIRST", ref)
    writer.para(support.get("write_this_first"), ref)
    writer.label("SMALL CLUE", ref)
    writer.para(support.get("small_clue"), ref)
    writer.label("BIGGER CLUE", ref)
    writer.para(support.get("bigger_clue"), ref)
    writer.label("HOW DO I START?", ref)
    writer.para(support.get("how_do_i_start"), ref)
    writer.label("WATCH FOR THIS", ref)
    writer.para(support.get("watch_for_this"), ref)
    writer.label("THINK IT THROUGH", ref)
    writer.bullets(support.get("think_it_through"), ref)
    writer.label("CHECK YOUR CHEMISTRY", ref)
    writer.bullets(support.get("check_your_chemistry"), ref)


def _answer_pages(writer: PageWriter, answer_path: dict[str, Any], title: str, ref: str) -> None:
    quick = answer_path.get("quick_check")
    full = answer_path.get("full_working")
    if not quick or not full:
        raise ValueError("CHEM_LP_RENDER_ANSWER_NAVIGATION_MISSING:" + ref)
    writer.new_page("answer check")
    writer.heading(title + " — QUICK CHECK", 2, ref + "-Q")
    writer.para(quick["answer_summary"], ref + "-Q")
    if quick.get("unit"):
        writer.para("Unit: " + public_text(quick["unit"]), ref + "-Q")
    writer.bullets(quick.get("marking_points"), ref + "-Q")
    writer.para("If your result does not match, return to the clues before opening the full working.", ref + "-Q")
    writer.new_page("full working")
    writer.heading(title + " — FULL WORKING", 2, ref + "-F")
    writer.bullets(full["steps"], ref + "-F")
    writer.label("VERIFY", ref + "-F")
    writer.para(full["verification"], ref + "-F")


def render_core2a(source_plan: dict[str, Any] | None, challenge_plan: dict[str, Any] | None, representations: dict[str, Any], policy: dict[str, Any], path: Path) -> dict[str, Any]:
    writer = PageWriter(path, "Chemistry Core (2A) — Source & Challenge Practice", policy)
    rep_index = representation_index(representations)
    item_visuals: list[dict[str, Any]] = []
    question_count = 0

    writer.heading("Chemistry Core (2A)", 1)
    writer.para("Attempt-first source practice followed by clearly labelled fresh challenge practice. Answers are separated from attempt pages so you can genuinely check your work.")
    writer.label("THE PRACTICE LOOP")
    writer.para("Try → use a clue only if needed → check the short answer → return to the question if wrong → open the full working.")

    if source_plan:
        writer.new_page("source practice")
        writer.heading("SOURCE PRACTICE", 1)
        writer.para("These questions preserve the governed Core (2) source identity and wording. Support is added around the question; the source itself is not silently rewritten.")
        for index, item in enumerate(source_plan["items"], 1):
            question_count += 1
            ref = f"C2A-S-{index:03d}"
            writer.new_page("source question attempt")
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
            item_visuals.append({"content_ref": ref, "required_refs": refs, "realized": realized, "unavailable_secondary_refs": unavailable, "status": "PASS" if (not refs or realized > 0) else "FAIL"})
            if refs and realized == 0:
                raise ValueError("CHEM_LP_RENDER_REQUIRED_VISUAL_MISSING:" + ref)
            _attempt_support(writer, support, ref)
            writer.para("Answer check: next page.", ref)
            _answer_pages(writer, item["answer_path"], f"Source question {index}", ref)

    if challenge_plan:
        writer.new_page("fresh challenge practice")
        writer.heading("FRESH CHALLENGE PRACTICE", 1)
        writer.para("These are newly generated practice questions grounded in taught Chemistry. They are not claimed as official past-paper questions.")
        for index, item in enumerate(challenge_plan["items"], 1):
            question_count += 1
            ref = f"C2A-G-{index:03d}"
            writer.new_page("fresh challenge attempt")
            writer.heading(f"Fresh challenge {index}", 2, ref)
            writer.label("TRY IT FIRST", ref)
            writer.question_text(item["prompt"], ref)
            _draw_provenance(writer, item["provenance"], ref)
            writer.workspace(5, ref)
            support = item["learner_support"]
            writer.label("SEE THE IDEA", ref)
            refs = list(item["core1a_binding"].get("h2_evidence_refs") or [])
            realized, unavailable = _visuals_for_refs(writer, refs, rep_index, ref) if refs else (0, [])
            item_visuals.append({"content_ref": ref, "required_refs": refs, "realized": realized, "unavailable_secondary_refs": unavailable, "status": "PASS" if (not refs or realized > 0) else "FAIL"})
            if refs and realized == 0:
                raise ValueError("CHEM_LP_RENDER_REQUIRED_VISUAL_MISSING:" + ref)
            _attempt_support(writer, support, ref)
            writer.para("Answer check: next page.", ref)
            _answer_pages(writer, item["answer_path"], f"Fresh challenge {index}", ref)

    metrics = writer.finish()
    metrics.update({
        "product": "CORE2A",
        "source_plan_ref": source_plan["plan_id"] if source_plan else None,
        "source_plan_digest": source_plan["plan_digest"] if source_plan else None,
        "challenge_plan_ref": challenge_plan["plan_id"] if challenge_plan else None,
        "challenge_plan_digest": challenge_plan["plan_digest"] if challenge_plan else None,
        "representation_bundle_ref": representations["bundle_id"],
        "representation_bundle_digest": representations["bundle_digest"],
        "question_count": question_count,
        "item_visual_closure": item_visuals,
    })
    metrics["pdf_sha256"] = sha_file(path)
    metrics["metrics_digest"] = digest({k: v for k, v in metrics.items() if k != "metrics_digest"})
    return metrics


def render_products(manuscript: dict[str, Any], source_plan: dict[str, Any] | None, challenge_plan: dict[str, Any] | None, representations: dict[str, Any], policy: dict[str, Any], out_dir: Path) -> dict[str, Any]:
    if policy.get("policy_id") != "CHEM-LEARNER-RENDER-v1":
        raise ValueError("CHEM_LP_RENDER_POLICY_MISMATCH")
    out_dir.mkdir(parents=True, exist_ok=True)
    core1_path = out_dir / "chemistry_core1a.pdf"
    core2_path = out_dir / "chemistry_core2a.pdf"
    core1_metrics = render_core1a(manuscript, representations, policy, core1_path)
    core2_metrics = render_core2a(source_plan, challenge_plan, representations, policy, core2_path)
    manifest = {
        "manifest_id": "CHEM-LP-RENDER-" + manuscript["manuscript_id"].split("-")[-1],
        "schema_version": "1.0.0",
        "subject": "CHEMISTRY",
        "render_policy_ref": policy["policy_id"],
        "core1a": core1_metrics,
        "core2a": core2_metrics,
        "status": "RENDERED_NOT_PREFLIGHTED",
        "manifest_digest": "",
    }
    payload = copy.deepcopy(manifest)
    payload.pop("manifest_digest")
    manifest["manifest_digest"] = digest(payload)
    (out_dir / "render_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--core1a-manuscript", required=True)
    parser.add_argument("--core2a-source-plan")
    parser.add_argument("--core2a-challenge-plan")
    parser.add_argument("--representation-bundle", required=True)
    parser.add_argument("--render-policy", required=True)
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()
    render_products(
        load(args.core1a_manuscript),
        load(args.core2a_source_plan) if args.core2a_source_plan else None,
        load(args.core2a_challenge_plan) if args.core2a_challenge_plan else None,
        load(args.representation_bundle),
        load(args.render_policy),
        Path(args.out_dir),
    )


if __name__ == "__main__":
    main()
