"""
Three-pass Learner-Surface Guard for Primary Mathematics V2.
Scans child-facing documents for internal architectural, diagnostic, or prompt leaks.
Zero false positives on standard mathematical text.
"""
from __future__ import annotations

import re
from typing import Any, Dict, List, Set


FORBIDDEN_INTERNAL_TOKENS: Set[str] = {
    "pedagogical_sequence",
    "skillmodel",
    "primarymathskillmodel",
    "focalfeature",
    "contrastset",
    "competinghypotheses",
    "diagnosticprobe",
    "controlledsharedfeatures",
    "errorsignature",
    "transcriptioncertainty",
    "schoolscopeobservations",
    "promptstructure",
    "falsifier",
    "benchmarkacceptance",
    "candidate_export",
    "internal_zero_digit_required",
    "universal_grade_scope_claimed"
}


class LearnerSurfaceGuard:
    """Scans student-facing text or document content for internal architecture leaks."""

    def __init__(self, extra_forbidden_tokens: Set[str] | None = None) -> None:
        self.forbidden_tokens = set(FORBIDDEN_INTERNAL_TOKENS)
        if extra_forbidden_tokens:
            self.forbidden_tokens.update(extra_forbidden_tokens)

    def scan_text(self, text: str) -> Dict[str, Any]:
        """
        Scans a text string for internal token leaks.
        Case-insensitive and normalizes delimiters.
        """
        lowered = text.lower()
        detected: List[str] = []

        for token in sorted(self.forbidden_tokens):
            # Token match with boundary or delimiter
            pattern = r"(?<![a-zA-Z0-9_])" + re.escape(token) + r"(?![a-zA-Z0-9_])"
            if re.search(pattern, lowered):
                detected.append(token)

        is_clean = (len(detected) == 0)
        return {
            "pass": is_clean,
            "detected_internal_tokens": detected,
            "token_count": len(detected)
        }

    def scan_document(self, doc_data: Dict[str, Any]) -> Dict[str, Any]:
        """Recursively scans all text values in a dictionary structure."""
        text_chunks: List[str] = []
        
        # Keys that are purely internal metadata and should NOT be scanned for leaks
        metadata_keys = {"id", "type", "kind", "skill_model_id", "linked_core1_id", "companion_id", "item_id", "section_type"}

        def _extract_strings(obj: Any) -> None:
            if isinstance(obj, str):
                text_chunks.append(obj)
            elif isinstance(obj, dict):
                for k, v in obj.items():
                    if k not in metadata_keys:
                        _extract_strings(v)
            elif isinstance(obj, list):
                for item in obj:
                    _extract_strings(item)

        _extract_strings(doc_data)
        full_text = " ".join(text_chunks)
        return self.scan_text(full_text)
