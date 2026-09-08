#!/usr/bin/env python3
"""Detect material text overlaps and page-bound escapes in a generated PDF.

This is a deterministic baseline gate for the Grade 9 Publication skill.
It uses PyMuPDF word boxes, compares words that belong to different extracted
text lines, and fails when material overlap is found.

Usage:
    python check_text_overlaps.py publication.pdf
    python check_text_overlaps.py publication.pdf --threshold 0.15 --json report.json

Exit codes:
    0  no overlap/bounds findings
    1  one or more findings
    2  usage/dependency/read error

This does not replace render inspection. Intentional graphic/text overprint,
math construction, or unusual PDFs can create false positives; investigate
rather than suppressing findings blindly.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    import fitz  # PyMuPDF
except Exception as exc:  # pragma: no cover - dependency message
    print(f"ERROR: PyMuPDF (fitz) is required: {exc}", file=sys.stderr)
    raise SystemExit(2)


def area(box: tuple[float, float, float, float]) -> float:
    x0, y0, x1, y1 = box
    return max(0.0, x1 - x0) * max(0.0, y1 - y0)


def intersection_area(
    a: tuple[float, float, float, float],
    b: tuple[float, float, float, float],
) -> float:
    ix = max(0.0, min(a[2], b[2]) - max(a[0], b[0]))
    iy = max(0.0, min(a[3], b[3]) - max(a[1], b[1]))
    return ix * iy


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf", help="Generated PDF to inspect")
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.15,
        help="Minimum intersection/min(word area) ratio; default 0.15",
    )
    parser.add_argument(
        "--min-intersection",
        type=float,
        default=2.0,
        help="Minimum overlap area in PDF points squared; default 2",
    )
    parser.add_argument("--json", dest="json_path", help="Optional JSON report path")
    args = parser.parse_args()

    path = Path(args.pdf)
    if not path.exists():
        print(f"ERROR: file not found: {path}", file=sys.stderr)
        return 2

    try:
        doc = fitz.open(path)
    except Exception as exc:
        print(f"ERROR: cannot open PDF: {exc}", file=sys.stderr)
        return 2

    overlaps: list[dict[str, object]] = []
    bounds: list[dict[str, object]] = []

    for page_index, page in enumerate(doc, start=1):
        page_rect = page.rect
        words = page.get_text("words")

        for word in words:
            x0, y0, x1, y1, text = word[:5]
            if x0 < -0.5 or y0 < -0.5 or x1 > page_rect.width + 0.5 or y1 > page_rect.height + 0.5:
                bounds.append(
                    {
                        "page": page_index,
                        "text": text,
                        "box": [round(x0, 2), round(y0, 2), round(x1, 2), round(y1, 2)],
                        "page_size": [round(page_rect.width, 2), round(page_rect.height, 2)],
                    }
                )

        for i in range(len(words)):
            wi = words[i]
            ai = tuple(float(v) for v in wi[:4])
            ai_area = max(area(ai), 1e-6)
            for j in range(i + 1, len(words)):
                wj = words[j]

                # PyMuPDF fields 5,6,7 are block_no, line_no, word_no.
                # Words on the same extracted line are expected to be adjacent
                # and are not treated as independent collision candidates.
                if wi[5:7] == wj[5:7]:
                    continue

                bj = tuple(float(v) for v in wj[:4])
                bj_area = max(area(bj), 1e-6)
                inter = intersection_area(ai, bj)
                if inter <= args.min_intersection:
                    continue
                ratio = inter / min(ai_area, bj_area)
                if ratio <= args.threshold:
                    continue

                overlaps.append(
                    {
                        "page": page_index,
                        "text_a": wi[4],
                        "text_b": wj[4],
                        "ratio": round(ratio, 3),
                        "box_a": [round(v, 2) for v in ai],
                        "box_b": [round(v, 2) for v in bj],
                    }
                )

    report = {
        "pdf": str(path),
        "pages": len(doc),
        "threshold": args.threshold,
        "min_intersection": args.min_intersection,
        "text_overlap_findings": len(overlaps),
        "component_bounds_escape_findings": len(bounds),
        "overlaps": overlaps,
        "bounds_escapes": bounds,
    }

    if args.json_path:
        Path(args.json_path).write_text(json.dumps(report, indent=2), encoding="utf-8")

    print("PUBLICATION LAYOUT COLLISION CHECK")
    print(f"- PDF: {path}")
    print(f"- pages: {len(doc)}")
    print(f"- text overlap findings: {len(overlaps)}")
    print(f"- page-bound escapes: {len(bounds)}")

    for finding in overlaps[:25]:
        print(
            f"  page {finding['page']}: {finding['text_a']!r} overlaps "
            f"{finding['text_b']!r} ratio={finding['ratio']}"
        )
    if len(overlaps) > 25:
        print(f"  ... {len(overlaps) - 25} more overlap findings")

    for finding in bounds[:25]:
        print(f"  page {finding['page']}: out-of-bounds text {finding['text']!r}")
    if len(bounds) > 25:
        print(f"  ... {len(bounds) - 25} more bounds findings")

    if overlaps or bounds:
        print("PUBLICATION LAYOUT COLLISION CHECK: FAIL")
        return 1

    print("PUBLICATION LAYOUT COLLISION CHECK: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
