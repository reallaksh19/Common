#!/usr/bin/env python3
"""Falsifiers for intrinsic H1/H2/H3 layout and child-readable fallback."""
from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[5]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from reportlab.pdfgen import canvas

from Grade4.V2.Mathematics.Publication.engine.staged_hint_layout import (
    StagedHintComponent,
    StagedHintLayoutError,
)
from Grade4.V2.Mathematics.Representation.engine.base import ReportLabBackend


def _stage(level: str, label: str, cue: str, action: str, branches: list[str]) -> dict:
    return {
        "level": level,
        "child_label": label,
        "primitive_kind": "QUANTITY_STRUCTURE_MAP",
        "semantic_params": {"branches": branches},
        "verbal_cue": cue,
        "learner_action": action,
    }


def _long_stages() -> list[dict]:
    return [
        _stage("H1", "LOOK", "Read the story and point to what we know, what changes, and what the question asks us to find.", "Say the quantities aloud before choosing an operation.", ["45 cycles", "Rs 56,250", "need 25 cycles"]),
        _stage("H2", "SHOW", "First find the value of one item. Keep the units beside the number so the meaning stays clear.", "Write the one-item number sentence only.", ["many", "divide", "one"]),
        _stage("H3", "NEXT", "Use the value of one item to find the value of the number the question asks for.", "Write only the next multiplication step; finish the calculation yourself.", ["one", "scale", "needed"]),
    ]


def _short_stages() -> list[dict]:
    return [
        _stage("H1", "LOOK", "Find the two numbers.", "Point to them.", ["40", "5"]),
        _stage("H2", "SHOW", "Do division first.", "Write 40 / 5.", ["40 / 5"]),
        _stage("H3", "NEXT", "Use the result next.", "Continue yourself.", ["result", "+ 12"]),
    ]


def _thinking_path() -> list[dict]:
    return [
        {"child_label": "READ", "one_line_action": "Read the quantities and units."},
        {"child_label": "ONE", "one_line_action": "Find the value of one item."},
        {"child_label": "NEEDED", "one_line_action": "Find the amount the question asks for."},
        {"child_label": "CHECK", "one_line_action": "Check the operation and label the answer."},
    ]


def _expect_fail(fn, code: str) -> None:
    try:
        fn()
    except StagedHintLayoutError as exc:
        if not str(exc).startswith(code + ":"):
            raise AssertionError(f"expected {code}, got {exc}") from exc
        return
    raise AssertionError(f"expected {code}, operation passed")


def main() -> None:
    dense = StagedHintComponent.plan(_long_stages(), x=40.0, top_y=760.0, width=515.0, thinking_path=_thinking_path())
    if dense.mode != "H1_TOP_H2H3_ROW":
        raise SystemExit(f"DENSE_STAGE_TWO_ROW_EXPECTED: {dense.mode}")

    compact = StagedHintComponent.plan(_short_stages(), x=40.0, top_y=760.0, width=515.0, thinking_path=_thinking_path())
    if compact.mode != "ROW":
        raise SystemExit(f"COMPACT_STAGE_ROW_EXPECTED: {compact.mode}")

    narrow = StagedHintComponent.plan(_short_stages(), x=40.0, top_y=760.0, width=330.0, thinking_path=_thinking_path())
    if narrow.mode != "STACK":
        raise SystemExit(f"NARROW_STAGE_MUST_STACK: {narrow.mode}")

    if dense.height >= sum(StagedHintComponent._stage_height(s, 515.0) for s in _long_stages()):
        raise SystemExit("DENSE_TWO_ROW_DID_NOT_REDUCE_VERTICAL_LOAD")

    _expect_fail(lambda: StagedHintComponent.plan(_short_stages()[:2], x=40.0, top_y=760.0, width=515.0), "STAGED_HINT_EXACTLY_THREE_REQUIRED")

    broken = _short_stages()
    broken[1].pop("primitive_kind")
    out = REPO_ROOT / "build" / "grade4_math_v2" / "Staged_Hint_Layout_Probe.pdf"
    out.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(out), pagesize=(595.27, 841.89))
    backend = ReportLabBackend(c)
    StagedHintComponent.render(backend, _long_stages(), x=40.0, top_y=790.0, width=515.0, thinking_path=_thinking_path())
    c.showPage()
    StagedHintComponent.render(backend, _short_stages(), x=40.0, top_y=790.0, width=515.0, thinking_path=_thinking_path())
    c.save()

    c2 = canvas.Canvas(str(out.with_name("Staged_Hint_Invalid.pdf")), pagesize=(595.27, 841.89))
    backend2 = ReportLabBackend(c2)
    _expect_fail(lambda: StagedHintComponent.render(backend2, broken, x=40.0, top_y=790.0, width=515.0), "STAGED_HINT_PRIMITIVE_MISSING")
    c2.save()

    print({"status": "PASS", "dense_mode": dense.mode, "compact_mode": compact.mode, "narrow_mode": narrow.mode, "pdf": str(out)})


if __name__ == "__main__":
    main()
