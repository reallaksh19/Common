"""
Publication Physical Custody and Layout Verification for Primary Mathematics V2.
Binds rendered pages, visual element coordinates, and PDF checksums.
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional
from Primary.V2.Mathematics.Representation.engine.base import PageMetricsA4


@dataclass
class PageElementRecord:
    page_number: int
    element_type: str
    semantic_id: str
    x: float
    y: float
    width: float
    height: float


class PublicationCustodyTracker:
    """Tracks physical layout elements during PDF rendering and generates custody records."""

    def __init__(self) -> None:
        self.elements: List[PageElementRecord] = []
        self.page_count: int = 0
        self.min_body_font_observed: float = 14.0
        self.overflow_strategy: str = "ADD_PAGE"

    def new_page(self) -> int:
        self.page_count += 1
        return self.page_count

    def record_element(
        self,
        element_type: str,
        semantic_id: str,
        x: float,
        y: float,
        width: float,
        height: float
    ) -> None:
        rec = PageElementRecord(
            page_number=max(self.page_count, 1),
            element_type=element_type,
            semantic_id=semantic_id,
            x=x,
            y=y,
            width=width,
            height=height
        )
        self.elements.append(rec)

    def record_font_size(self, font_size: float) -> None:
        if font_size < self.min_body_font_observed:
            self.min_body_font_observed = font_size

    def compute_pdf_hash(self, pdf_path: Path) -> str:
        with open(pdf_path, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()

    def export_custody_record(self, pdf_sha256: str) -> Dict[str, Any]:
        """Produces layout_custody payload matching candidate_export schema."""
        page_map: List[Dict[str, Any]] = []
        for p in range(1, self.page_count + 1):
            page_elems = [e for e in self.elements if e.page_number == p]
            page_map.append({
                "page_number": p,
                "element_count": len(page_elems),
                "semantic_ids": [e.semantic_id for e in page_elems]
            })

        return {
            "page_count": max(self.page_count, 1),
            "page_map": page_map,
            "pdf_sha256": pdf_sha256,
            "child_first_geometry": {
                "min_body_font_pt": self.min_body_font_observed,
                "overflow_strategy": self.overflow_strategy
            }
        }
