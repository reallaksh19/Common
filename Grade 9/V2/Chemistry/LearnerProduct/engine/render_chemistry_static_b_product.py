#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import sys
from pathlib import Path
from typing import Any

from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

HERE = Path(__file__).resolve()
CHEM_ROOT = HERE.parents[2]
sys.path.insert(0, str(CHEM_ROOT / "LearningBlueprint" / "engine"))
sys.path.insert(0, str(CHEM_ROOT / "ExactProduct" / "engine"))

from validate_static_b_layer_boundary import validate_core1b, validate_core2b  # noqa: E402
import learner_surface_guard as GUARD  # noqa: E402

FONT = "DejaVuSans"
BOLD = "DejaVuSans-Bold"
PAGE_W, PAGE_H = A4
MARGIN = 42.0

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


def _register_fonts() -> None:
    regular = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
    bold = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
    if not regular.exists() or not bold.exists():
        raise RuntimeError("CHEM_CORE_RENDER_UNICODE_FONT_UNAVAILABLE")
    if FONT not in pdfmetrics.getRegisteredFontNames():
        pdfmetrics.registerFont(TTFont(FONT, str(regular)))
        pdfmetrics.registerFont(TTFont(BOLD, str(bold)))


def _safe(value: Any) -> str:
    text = str(value or "").strip()
    GUARD.assert_learner_safe(text, "static B product")
    return text


def _wrap(text: str, size: float, width: float, font: str = FONT) -> list[str]:
    words = _safe(text).split()
    lines: list[str] = []
    current = ""
    for word in words:
        trial = (current + " " + word).strip()
        if pdfmetrics.stringWidth(trial, font, size) <= width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines or [""]


class Writer:
    def __init__(self, path: Path, title: str):
        _register_fonts()
        self.path = path
        self.c = canvas.Canvas(str(path), pagesize=A4, invariant=1, pageCompression=1)
        self.c.setTitle(title)
        self.page_count = 0
        self.y = 0.0
        self.new_page()

    def new_page(self) -> None:
        if self.page_count:
            self.c.showPage()
        self.page_count += 1
        self.y = PAGE_H - MARGIN
        self.c.setFont(FONT, 9.0)
        self.c.drawRightString(PAGE_W - MARGIN, 24, f"Chemistry | {self.page_count}")

    def _ensure(self, height: float) -> None:
        if self.y - height < MARGIN:
            self.new_page()

    def text(self, value: Any, *, size: float = 10.5, bold: bool = False, gap: float = 6.0) -> None:
        font = BOLD if bold else FONT
        lines = _wrap(_safe(value), size, PAGE_W - 2 * MARGIN, font)
        leading = size * 1.35
        self._ensure(len(lines) * leading + gap)
        self.c.setFont(font, size)
        for line in lines:
            self.c.drawString(MARGIN, self.y, line)
            self.y -= leading
        self.y -= gap

    def heading(self, value: Any, *, level: int = 1) -> None:
        self.text(value, size=16.0 if level == 1 else 12.5, bold=True, gap=10.0)

    def label(self, value: Any) -> None:
        self.text(value, size=9.5, bold=True, gap=3.0)

    def workspace(self, lines: int = 8) -> None:
        self.label("YOUR WORK")
        for _ in range(lines):
            self._ensure(22)
            self.c.setLineWidth(0.4)
            self.c.line(MARGIN, self.y, PAGE_W - MARGIN, self.y)
            self.y -= 22

    def finish(self) -> dict[str, Any]:
        self.c.save()
        raw = self.path.read_bytes()
        return {
            "path": self.path.name,
            "page_count": self.page_count,
            "pdf_sha256": "sha256:" + hashlib.sha256(raw).hexdigest(),
            "bytes": len(raw),
        }


def render_core1b(payload: dict[str, Any], path: Path) -> dict[str, Any]:
    evidence = validate_core1b(payload)
    w = Writer(path, "Chemistry Core1B")
    w.heading(payload.get("title") or "Chemistry reconstruction practice")
    w.text("Attempt the task before opening the clue pages.")
    w.heading("TASK", level=2)
    w.text(payload["task_prompt"], size=11.5, bold=True)
    w.workspace(int(payload.get("workspace_lines", 8)))

    w.new_page()
    w.heading("CLUES")
    w.text("Use only the smallest clue that gets your reasoning moving again.")
    for row in payload["help"]:
        label = CORE1_HELP_LABELS[row["level"]]
        w.label(label)
        w.text(row["text"])

    w.new_page()
    w.heading("CHECK YOUR RECONSTRUCTION")
    w.label("EXPECTED RESPONSE")
    w.text(payload["canonical_answer"], bold=True)
    if payload.get("explanation"):
        w.label("WHY IT WORKS")
        w.text(payload["explanation"])
    w.label("VERIFY")
    w.text(payload["check"], bold=True)
    out = w.finish()
    out.update({"product_mode": "CORE1B", "boundary_validation": evidence})
    return out


def render_core2b(payload: dict[str, Any], path: Path) -> dict[str, Any]:
    evidence = validate_core2b(payload)
    source = payload["source_item"]
    support = evidence["resolved_support_profile"]
    w = Writer(path, "Chemistry Core2B")
    w.heading("Chemistry transfer practice")
    w.label("SOURCE")
    w.text(source["source_locator"])
    w.heading("QUESTION", level=2)
    w.text(source["stem"], size=11.5, bold=True)
    w.workspace(int(payload.get("workspace_lines", 10)))

    entry = support["hint_entry_level"]
    allowed = list(CORE2_HELP_LABELS)
    start = allowed.index(entry)
    visible = [row for row in payload["help"] if row["level"] in CORE2_HELP_LABELS and allowed.index(row["level"]) >= start]
    w.new_page()
    w.heading("CLUES")
    w.text("Use the clues in order only as far as you need them.")
    for row in visible:
        w.label(CORE2_HELP_LABELS[row["level"]])
        w.text(row["text"])

    w.new_page()
    w.heading("FULL SOLUTION")
    w.text(payload["full_solution"], bold=True)
    w.label("ANSWER")
    w.text(source["canonical_answer"], bold=True)
    w.label("VERIFY AND REFLECT")
    w.text(payload["verify_reflect"], bold=True)
    out = w.finish()
    out.update({"product_mode": "CORE2B", "boundary_validation": evidence})
    return out


def render_static_b_product(product_mode: str, payload: dict[str, Any], path: Path) -> dict[str, Any]:
    path.parent.mkdir(parents=True, exist_ok=True)
    if product_mode == "CORE1B":
        return render_core1b(payload, path)
    if product_mode == "CORE2B":
        return render_core2b(payload, path)
    raise ValueError("CHEM_CORE_RENDER_B_MODE_INVALID")
