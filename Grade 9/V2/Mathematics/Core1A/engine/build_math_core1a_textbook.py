#!/usr/bin/env python3
"""Core 1A: turn a semantic MathCore1StudyPlan into a learner-facing textbook PDF.

Core 1 deliberately expresses instructional obligations in machine-oriented form.
Core 1A is the learner-authoring boundary. It consumes that output plus repository
instructional authority, materializes real learner problems, rewrites internal
authoring language into textbook prose, validates learner-product quality, and
emits a PDF + manuscript + audit.

Core 1A never reuses original assessment questions. Authored learner examples are
loaded from typed, digest-bound repository assets; executable Python contains only
selection, realization, validation and rendering logic.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import core1a_family_authoring as family_authoring

FULL_TREATMENTS = {"ACTIVE_STUDY", "REPAIR_BEFORE", "REPAIR_IN_UNIT"}
REQUIRED_ROLES = ("WORKED", "GUIDED", "FADED", "INDEPENDENT", "TRANSFER")
FORBIDDEN_LEARNER_TOKENS = (
    "capability_ref",
    "problem_family_ref",
    "release class",
    "pck ",
    "promotion registry",
    "author a new instance",
    "source reuse is forbidden",
    "core1 study plan",
    "treatment ",
    "reconstruction route",
    "fading dimensions",
    "candidate learner product",
    "publication engineering",
    "{rows}",
)
INTERNAL_CODE_RE = re.compile(r"\b(?:MATH-(?:PF|PCK|C1L|PAP|C1SP)-[A-Z0-9-]+)\b")

ROOT = Path(__file__).resolve().parents[2]
FONT_NAME = "Core1A-Regular"
FONT_BOLD = "Core1A-Bold"


def register_fonts() -> None:
    global FONT_NAME, FONT_BOLD
    candidates = [
        ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
        ("/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf", "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"),
    ]
    for regular, bold in candidates:
        if Path(regular).exists() and Path(bold).exists():
            pdfmetrics.registerFont(TTFont(FONT_NAME, regular))
            pdfmetrics.registerFont(TTFont(FONT_BOLD, bold))
            return
    FONT_NAME, FONT_BOLD = "Helvetica", "Helvetica-Bold"


DEFAULT_PCK_INDEX = ROOT / "InstructionalKnowledge" / "registry" / "math-pck-candidates.json"
DEFAULT_FAMILY_INDEX = ROOT / "ProblemSemantics" / "registry" / "math-problem-family-registry.json"


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(value: Any, omit: str | None = None) -> str:
    item = copy.deepcopy(value)
    if omit and isinstance(item, dict):
        item.pop(omit, None)
    return hashlib.sha256(canonical(item).encode("utf-8")).hexdigest()


def load(path: Path | str) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def fail(code: str, detail: str = "") -> None:
    raise ValueError(f"{code}:{detail}" if detail else code)


def humanize_code(value: str) -> str:
    text = re.sub(r"^MATH-(?:PF|PCK)-", "", str(value))
    return text.replace("_", " ").replace("-", " ").strip().title()


def sentence(text: str) -> str:
    text = str(text or "").strip()
    if not text:
        return ""
    text = text[0].upper() + text[1:]
    return text if text.endswith((".", "?", "!")) else text + "."


def public_phrase(value: str) -> str:
    text = str(value or "").strip()
    if not text:
        return ""
    if re.fullmatch(r"[A-Z0-9_]+", text):
        label = text
        for prefix in ("VERIFY_", "CHECK_"):
            if label.startswith(prefix):
                label = label[len(prefix):]
                return sentence("Check " + label.replace("_", " ").lower())
        return sentence(label.replace("_", " ").lower())
    return sentence(text)


def safe_text(text: str) -> str:
    return (
        str(text or "")
        .replace("&", "&amp;")
        .replace("<=", "≤")
        .replace(">=", "≥")
        .replace("!=", "≠")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def load_pck_assets(index_path: Path) -> dict[str, dict]:
    index = load(index_path)
    out: dict[str, dict] = {}
    for row in index.get("asset_documents", []):
        asset_path = index_path.parent / row["path"]
        asset = load(asset_path)
        if asset.get("asset_id") != row.get("asset_id"):
            fail("CORE1A_PCK_INDEX_BINDING_MISMATCH", str(asset_path))
        out[asset["asset_id"]] = asset
    return out


def load_problem_families(index_path: Path) -> dict[str, dict]:
    index = load(index_path)
    out: dict[str, dict] = {}
    for shard in index.get("family_shards", []):
        body = load(index_path.parent / shard["path"])
        for family in body.get("families", []):
            out[family["family_id"]] = family
    if len(out) != index.get("family_count"):
        fail("CORE1A_PROBLEM_FAMILY_REGISTRY_INCOMPLETE")
    return out


@dataclass(frozen=True)
class Instance:
    prompt: str
    steps: tuple[str, ...]
    answer: str
    hints: tuple[str, str, str]


def inst(prompt: str, steps: list[str], answer: str, hints: list[str]) -> Instance:
    if len(hints) != 3:
        raise AssertionError("all learner instances require three hints")
    return Instance(prompt, tuple(steps), answer, tuple(hints))


FAMILY_AUTHORING_ASSET_SET = family_authoring.load_family_authoring_assets()
_FAMILY_BY_ID = {row["family_ref"]: row for row in FAMILY_AUTHORING_ASSET_SET["families"]}
FAMILY_BANKS = {family_ref: None for family_ref in _FAMILY_BY_ID}
DISPLAY_TITLES = {family_ref: row["title"] for family_ref, row in _FAMILY_BY_ID.items()}


def family_bank(family_id: str) -> list[Instance]:
    row = _FAMILY_BY_ID.get(family_id)
    if row is None:
        fail("CORE1A_FAMILY_GENERATOR_MISSING", family_id)
    rows = [inst(x["prompt"], list(x["steps"]), x["answer"], list(x["hints"])) for x in row["examples"]]
    if len(rows) < 6:
        fail("CORE1_AUTHORED_INSTANCE_NOT_MATERIALIZED", family_id + ":need_six_distinct_instances")
    return rows


# -------------------------- manuscript authoring --------------------------
def choose_family(lesson: dict) -> str | None:
    plans = lesson.get("problem_authoring_plans") or []
    if plans:
        return plans[0].get("problem_family_ref")
    return None


def choose_asset(lesson: dict, assets: dict[str, dict]) -> dict | None:
    for ref in lesson.get("pck_asset_refs", []):
        if ref in assets:
            return assets[ref]
    return None


def public_route(asset: dict | None, family: dict | None) -> list[str]:
    if asset and asset.get("reconstruction_route"):
        return [sentence(x) for x in asset["reconstruction_route"]]
    if family:
        return [sentence(x.get("semantic_job", "")) for x in family.get("reasoning_route_template", [])]
    return []


def materialize_practice(bank: list[Instance], lesson: dict) -> dict[str, dict]:
    index_for = {"WORKED": 0, "GUIDED": 2, "FADED": 3, "INDEPENDENT": 4, "TRANSFER": 5, "VERIFY": 4}
    needed = [p["instance_role"] for p in lesson.get("problem_authoring_plans", [])]
    out = {}
    for role in needed:
        if role not in index_for:
            fail("CORE1A_UNKNOWN_INSTANCE_ROLE", role)
        i = index_for[role]
        if i >= len(bank):
            fail("CORE1_AUTHORED_INSTANCE_NOT_MATERIALIZED", role)
        item = bank[i]
        out[role] = {
            "prompt": item.prompt,
            "solution_steps": list(item.steps),
            "answer": item.answer,
            "hints": list(item.hints),
            "source_class": "NEW_AUTHORED_CORE1A",
        }
    return out


def authored_lesson(lesson: dict, assets: dict[str, dict], families: dict[str, dict]) -> dict:
    family_id = choose_family(lesson)
    asset = choose_asset(lesson, assets)
    family = families.get(family_id) if family_id else None
    full = lesson["treatment"] in FULL_TREATMENTS

    if full and not family_id:
        fail("CORE1A_PROBLEM_FAMILY_REQUIRED", lesson["lesson_id"])
    if full and family_id not in FAMILY_BANKS:
        fail("CORE1A_FAMILY_GENERATOR_MISSING", family_id or lesson["lesson_id"])

    if family_id in FAMILY_BANKS:
        bank = family_bank(family_id)
        practice = materialize_practice(bank, lesson)
    else:
        bank = []
        practice = {}

    title = DISPLAY_TITLES.get(family_id, lesson.get("learner_title") or "Mathematics")
    recognition = []
    if family:
        recognition = [sentence(x) for x in family.get("problem_signature", {}).get("recognition_cues", [])]

    ordinary = sentence(asset.get("ordinary_language_bridge", "")) if asset else ""
    anchor = sentence(asset.get("anchor", "")) if asset else ""
    route = public_route(asset, family)
    mistake = ""
    repair = []
    if asset:
        wrong = asset.get("misconception_discriminator", {}).get("candidate_wrong_model", "")
        probe = asset.get("misconception_discriminator", {}).get("probe", "")
        if wrong:
            mistake = sentence(wrong) + (" " + sentence(probe) if probe else "")
        repair = [sentence(x) for x in asset.get("repair_route", [])]
    elif family and family.get("common_invalid_mechanisms"):
        row = family["common_invalid_mechanisms"][0]
        mistake = sentence(row.get("invalid_move", "")) + " " + sentence(row.get("why_invalid", ""))

    verification = []
    if asset:
        verification.extend(sentence(x) for x in asset.get("verification_method", []))
    verification.extend(public_phrase(x) for x in lesson.get("verification_requirements", []))
    verification = list(dict.fromkeys(x for x in verification if x))

    return {
        "lesson_id": lesson["lesson_id"],
        "title": title,
        "treatment": lesson["treatment"],
        "family_ref": family_id,
        "opening": ordinary or "Begin by identifying what the question is asking you to preserve, compare or determine.",
        "concept_explanation": anchor or (sentence(family.get("problem_signature", {}).get("target_job", "")) if family else ""),
        "what_to_notice": recognition,
        "why_it_works": route,
        "common_mistake": mistake,
        "repair": repair,
        "worked_examples": (
            [
                {"prompt": bank[0].prompt, "steps": list(bank[0].steps), "answer": bank[0].answer},
                {"prompt": bank[1].prompt, "steps": list(bank[1].steps), "answer": bank[1].answer},
            ]
            if full and len(bank) >= 2
            else []
        ),
        "practice": practice,
        "verification": verification,
        "source_trace": {
            "core1_lesson_ref": lesson["lesson_id"],
            "assessment_question_refs": list(lesson.get("assessment_question_refs", [])),
            "pck_asset_refs": list(lesson.get("pck_asset_refs", [])),
            "family_authoring_asset_set_id": FAMILY_AUTHORING_ASSET_SET["asset_set_id"],
            "family_authoring_asset_set_digest": FAMILY_AUTHORING_ASSET_SET["asset_set_digest"],
        },
    }


def manuscript(core1: dict, assets: dict[str, dict], families: dict[str, dict]) -> dict:
    lessons = [authored_lesson(x, assets, families) for x in core1["lessons"]]
    out = {
        "core1a_book_id": "MATH-C1A-" + digest({"core1": core1["core1_study_plan_id"], "plan_digest": core1["plan_digest"]})[:16],
        "schema_version": "1.0.0",
        "subject": "MATHEMATICS",
        "source_core1_study_plan_ref": core1["core1_study_plan_id"],
        "source_core1_plan_digest": core1["plan_digest"],
        "release_class": core1["release_class"],
        "lessons": lessons,
        "quality_audit": {},
        "book_digest": "",
    }
    out["quality_audit"] = validate_manuscript(out)
    out["book_digest"] = digest(out, "book_digest")
    return out


def learner_texts(book: dict) -> list[str]:
    texts: list[str] = []
    for lesson in book["lessons"]:
        for key in ("title", "opening", "concept_explanation", "common_mistake"):
            texts.append(str(lesson.get(key, "")))
        texts.extend(lesson.get("what_to_notice", []))
        texts.extend(lesson.get("why_it_works", []))
        texts.extend(lesson.get("repair", []))
        texts.extend(lesson.get("verification", []))
        for ex in lesson.get("worked_examples", []):
            texts.append(ex["prompt"])
            texts.extend(ex["steps"])
            texts.append(ex["answer"])
        for item in lesson.get("practice", {}).values():
            texts.append(item["prompt"])
            texts.extend(item["hints"])
    return texts


def validate_manuscript(book: dict) -> dict:
    failures: list[str] = []
    full_count = 0
    actual_problem_count = 0

    for lesson in book["lessons"]:
        full = lesson["treatment"] in FULL_TREATMENTS
        if full:
            full_count += 1
            if len(lesson["worked_examples"]) < 2:
                failures.append(f"CORE1A_WORKED_EXAMPLE_DEPTH_MISSING:{lesson['lesson_id']}")
            required = set(REQUIRED_ROLES)
            got = set(lesson["practice"])
            missing = sorted(required - got)
            if missing:
                failures.append(f"CORE1_AUTHORED_INSTANCE_NOT_MATERIALIZED:{lesson['lesson_id']}:{','.join(missing)}")
            if not lesson["concept_explanation"] or len(lesson["why_it_works"]) < 2:
                failures.append(f"CORE1A_CONCEPT_EXPLANATION_UNDERREALIZED:{lesson['lesson_id']}")
            if not lesson["common_mistake"] or not lesson["repair"]:
                failures.append(f"CORE1_MISCONCEPTION_REPAIR_NOT_MATERIALIZED:{lesson['lesson_id']}")
        for item in lesson.get("practice", {}).values():
            if item.get("source_class") == "NEW_AUTHORED_CORE1A":
                actual_problem_count += 1

    for text in learner_texts(book):
        lower = text.lower()
        for token in FORBIDDEN_LEARNER_TOKENS:
            if token in lower:
                failures.append(f"CORE1A_INTERNAL_JARGON_LEAK:{token}")
        if INTERNAL_CODE_RE.search(text):
            failures.append("CORE1A_INTERNAL_IDENTIFIER_LEAK")

    if failures:
        fail("CORE1A_QUALITY_GATE_FAILED", "|".join(sorted(set(failures))))

    return {
        "status": "PASS",
        "full_teaching_lessons": full_count,
        "actual_problem_instances": actual_problem_count,
        "checks": [
            "NO_INTERNAL_AUTHORING_JARGON",
            "FULL_TEACHING_HAS_TWO_WORKED_EXAMPLES",
            "REQUIRED_PRACTICE_ROLES_MATERIALIZED",
            "MISCONCEPTION_REPAIR_MATERIALIZED",
            "CONCEPT_EXPLANATION_MATERIALIZED",
            "NO_UNRESOLVED_TEMPLATE_TOKENS",
        ],
    }


# -------------------------- textbook PDF --------------------------
def styles():
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "BookTitle", parent=base["Title"], fontName=FONT_BOLD,
            fontSize=25, leading=29, textColor=colors.HexColor("#16324F"),
            alignment=TA_CENTER, spaceAfter=10,
        ),
        "chapter": ParagraphStyle(
            "Chapter", parent=base["Heading1"], fontName=FONT_BOLD,
            fontSize=19, leading=23, textColor=colors.HexColor("#16324F"),
            spaceAfter=8,
        ),
        "h2": ParagraphStyle(
            "H2", parent=base["Heading2"], fontName=FONT_BOLD,
            fontSize=13.5, leading=17, textColor=colors.HexColor("#1E5A7A"),
            spaceBefore=5, spaceAfter=5,
        ),
        "body": ParagraphStyle(
            "Body", parent=base["BodyText"], fontName=FONT_NAME,
            fontSize=10.2, leading=14.2, textColor=colors.HexColor("#20262E"),
            spaceAfter=6,
        ),
        "small": ParagraphStyle(
            "Small", parent=base["BodyText"], fontName=FONT_NAME,
            fontSize=8.8, leading=11.5, textColor=colors.HexColor("#425466"),
        ),
        "example": ParagraphStyle(
            "Example", parent=base["BodyText"], fontName=FONT_NAME,
            fontSize=9.8, leading=13.5, leftIndent=4, rightIndent=4,
            textColor=colors.HexColor("#20262E"),
        ),
    }


def card(title: str, body_parts: list[Any], color: str, st: dict) -> Table:
    title_p = Paragraph(f"<b>{safe_text(title)}</b>", ParagraphStyle(
        f"card-{hash(title)}", parent=st["small"], textColor=colors.white, fontName=FONT_BOLD
    ))
    rows = [[title_p]]
    for part in body_parts:
        if isinstance(part, Paragraph):
            rows.append([part])
        else:
            rows.append([Paragraph(safe_text(str(part)), st["example"])])
    t = Table(rows, colWidths=[174 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), colors.HexColor(color)),
        ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#F9FBFD")),
        ("BOX", (0, 0), (-1, -1), 0.8, colors.HexColor(color)),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    return t


def bullet_paragraphs(items: list[str], st: dict) -> list[Paragraph]:
    return [Paragraph("• " + safe_text(x), st["body"]) for x in items if x]


def example_box(number: int, ex: dict, st: dict) -> Table:
    body: list[Any] = [Paragraph(f"<b>{safe_text(ex['prompt'])}</b>", st["example"])]
    for i, step in enumerate(ex["steps"], 1):
        body.append(Paragraph(f"<b>{i}.</b> {safe_text(step)}", st["example"]))
    body.append(Paragraph(f"<b>Answer:</b> {safe_text(ex['answer'])}", st["example"]))
    return card(f"Worked example {number}", body, "#2E8B57", st)


def practice_box(title: str, item: dict, st: dict, show_hints: int) -> Table:
    parts: list[Any] = [Paragraph(f"<b>{safe_text(item['prompt'])}</b>", st["example"])]
    for i in range(show_hints):
        parts.append(Paragraph(f"<b>Hint {i+1}:</b> {safe_text(item['hints'][i])}", st["example"]))
    return card(title, parts, "#B7791F", st)


def add_page_number(canvas, doc):
    canvas.saveState()
    canvas.setFont(FONT_NAME, 8)
    canvas.setFillColor(colors.HexColor("#667788"))
    canvas.drawString(18 * mm, 10 * mm, "Mathematics | Core 1A")
    canvas.drawRightString(A4[0] - 18 * mm, 10 * mm, f"{doc.page}")
    canvas.restoreState()


def render_pdf(book: dict, path: Path) -> dict:
    register_fonts()
    st = styles()
    doc = SimpleDocTemplate(
        str(path), pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm,
        topMargin=16 * mm, bottomMargin=16 * mm,
        title="Mathematics Core 1A Student Textbook",
        author="Grade 9 V2 Mathematics",
    )
    story: list[Any] = []
    story.append(Spacer(1, 18))
    story.append(Paragraph("Mathematics", st["title"]))
    story.append(Paragraph("Core 1A — Student Textbook", st["title"]))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "This book develops each idea through examples, explanation, guided practice and independent checks. "
        "Internal authoring and review metadata are intentionally kept out of the learner pages.",
        ParagraphStyle("cover", parent=st["body"], alignment=TA_CENTER, fontSize=11, leading=15)
    ))
    story.append(Spacer(1, 12))
    story.append(card(
        "How to study a lesson",
        [
            "Read the opening example before memorising a rule.",
            "Follow the worked examples line by line and check why each step is legal.",
            "Use hints only when you are stuck; later questions deliberately remove support.",
            "Always perform the final check before accepting an answer.",
        ],
        "#16324F", st
    ))
    story.append(PageBreak())

    for li, lesson in enumerate(book["lessons"], 1):
        story.append(Paragraph(f"{li}. {safe_text(lesson['title'])}", st["chapter"]))
        story.append(Paragraph(safe_text(lesson["opening"]), st["body"]))
        if lesson["what_to_notice"]:
            story.append(Paragraph("What should you notice?", st["h2"]))
            story.extend(bullet_paragraphs(lesson["what_to_notice"], st))
        if lesson["concept_explanation"]:
            story.append(Paragraph("The idea", st["h2"]))
            story.append(Paragraph(safe_text(lesson["concept_explanation"]), st["body"]))
        if lesson["why_it_works"]:
            story.append(Paragraph("Why the method works", st["h2"]))
            for i, step in enumerate(lesson["why_it_works"], 1):
                story.append(Paragraph(f"<b>{i}.</b> {safe_text(step)}", st["body"]))
        for ei, ex in enumerate(lesson["worked_examples"], 1):
            story.append(Spacer(1, 4))
            story.append(example_box(ei, ex, st))
            story.append(Spacer(1, 7))
        if lesson["common_mistake"]:
            story.append(card("Common mistake", [lesson["common_mistake"]] + lesson.get("repair", []), "#B03A2E", st))
            story.append(Spacer(1, 8))

        practice = lesson["practice"]
        if "GUIDED" in practice:
            story.append(Paragraph("Try it with help", st["h2"]))
            story.append(practice_box("Guided practice", practice["GUIDED"], st, 2))
            story.append(Spacer(1, 6))
        if "FADED" in practice:
            story.append(practice_box("Now with less help", practice["FADED"], st, 1))
            story.append(Spacer(1, 6))
        if "INDEPENDENT" in practice:
            story.append(practice_box("Your turn", practice["INDEPENDENT"], st, 0))
            story.append(Spacer(1, 6))
        if "TRANSFER" in practice:
            story.append(practice_box("Challenge", practice["TRANSFER"], st, 0))
            story.append(Spacer(1, 6))
        if "VERIFY" in practice and lesson["treatment"] not in FULL_TREATMENTS:
            story.append(practice_box("Quick check", practice["VERIFY"], st, 0))
            story.append(Spacer(1, 6))
        if lesson["verification"]:
            story.append(Paragraph("Check your work", st["h2"]))
            story.extend(bullet_paragraphs(lesson["verification"], st))
        if li != len(book["lessons"]):
            story.append(PageBreak())

    story.append(PageBreak())
    story.append(Paragraph("Answer check", st["chapter"]))
    story.append(Paragraph(
        "Use this section after you have attempted the practice. If your answer differs, return to the worked example and identify the first step where your reasoning changed.",
        st["body"],
    ))
    for li, lesson in enumerate(book["lessons"], 1):
        practice = lesson.get("practice", {})
        if not practice:
            continue
        story.append(Paragraph(f"{li}. {safe_text(lesson['title'])}", st["h2"]))
        for role in ("GUIDED", "FADED", "INDEPENDENT", "TRANSFER", "VERIFY"):
            if role not in practice:
                continue
            label = {
                "GUIDED": "Guided practice",
                "FADED": "Less-help practice",
                "INDEPENDENT": "Your turn",
                "TRANSFER": "Challenge",
                "VERIFY": "Quick check",
            }[role]
            story.append(Paragraph(f"<b>{label}:</b> {safe_text(practice[role]['answer'])}", st["body"]))

    doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
    pdf_bytes = path.read_bytes()
    return {"pdf_sha256": hashlib.sha256(pdf_bytes).hexdigest(), "pdf_size_bytes": len(pdf_bytes)}


# -------------------------- CLI --------------------------
def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--core1-plan", required=True)
    ap.add_argument("--pck-index", default=str(DEFAULT_PCK_INDEX))
    ap.add_argument("--problem-family-index", default=str(DEFAULT_FAMILY_INDEX))
    ap.add_argument("--out-dir", required=True)
    args = ap.parse_args()

    core1 = load(args.core1_plan)
    if core1.get("subject") != "MATHEMATICS":
        fail("CORE1A_NON_MATH_INPUT")
    if core1.get("plan_digest") != digest(core1, "plan_digest"):
        fail("CORE1A_CORE1_PLAN_DIGEST_MISMATCH")

    assets = load_pck_assets(Path(args.pck_index))
    families = load_problem_families(Path(args.problem_family_index))
    book = manuscript(core1, assets, families)

    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    manuscript_path = out / "core1a_textbook_manuscript.json"
    manuscript_path.write_text(json.dumps(book, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    pdf_path = out / "core1a_student_textbook.pdf"
    pdf_meta = render_pdf(book, pdf_path)

    audit = {
        "core1a_book_id": book["core1a_book_id"],
        "source_core1_plan_digest": book["source_core1_plan_digest"],
        "book_digest": book["book_digest"],
        "quality_audit": book["quality_audit"],
        "artifact": {"path": pdf_path.name, **pdf_meta},
        "release_class": book["release_class"],
    }
    (out / "core1a_quality_audit.json").write_text(
        json.dumps(audit, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
