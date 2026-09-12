#!/usr/bin/env python3
"""Render an HTML authoring source to PDF using WeasyPrint.

Usage:
    python tools/rebuild_pdf.py path/to/core1.html path/to/core1.pdf

The authoring HTML contains its own print CSS. The renderer should not invent
page content or select teaching primitives.
"""
from __future__ import annotations

import argparse
from pathlib import Path

try:
    from weasyprint import HTML
except ImportError as exc:
    raise SystemExit(
        "WeasyPrint is required. Install it in the authoring environment before rendering."
    ) from exc


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("html", type=Path)
    parser.add_argument("pdf", type=Path)
    args = parser.parse_args()

    if not args.html.exists():
        raise SystemExit(f"HTML source does not exist: {args.html}")
    args.pdf.parent.mkdir(parents=True, exist_ok=True)
    HTML(filename=str(args.html)).write_pdf(str(args.pdf))
    if not args.pdf.exists() or args.pdf.stat().st_size == 0:
        raise SystemExit("PDF render did not produce a non-empty file")
    print(f"rendered {args.html} -> {args.pdf} ({args.pdf.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
