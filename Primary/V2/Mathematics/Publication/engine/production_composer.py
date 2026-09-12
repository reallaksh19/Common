"""Strict Primary Math V2 production publication entry point.

Legacy text-only H1/H2/H3 ladders remain readable by the historical page composer
for migration tests, but they are forbidden here. New production publication must
arrive through LearningRepresentationPlan / AuthoringLearningHandoff.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Mapping, Tuple

from Primary.V2.Mathematics.Publication.engine.authoring_handoff_adapter import AuthoringHandoffAdapter
from Primary.V2.Mathematics.Publication.engine.page_composer import PrimaryPageComposer


@dataclass
class ProductionPublicationError(ValueError):
    code: str
    message: str

    def __str__(self) -> str:
        return f"{self.code}: {self.message}"


def _require(condition: bool, code: str, message: str) -> None:
    if not condition:
        raise ProductionPublicationError(code, message)


class ProductionPrimaryPageComposer(PrimaryPageComposer):
    """PrimaryPageComposer with text-only learning support disabled."""

    @staticmethod
    def validate_core2_plan(companion_plan: Mapping[str, Any]) -> None:
        ladders = list(((companion_plan.get("appendix_b") or {}).get("ladders") or []))
        for ladder in ladders:
            item_id = str(ladder.get("item_id") or "<unknown>")
            _require(
                isinstance(ladder.get("learning_representation_plan"), dict),
                "LEGACY_TEXT_ONLY_HINT_LADDER_FORBIDDEN",
                f"{item_id}: production Core2 requires LearningRepresentationPlan",
            )
            _require(
                bool(str(ladder.get("fresh_independent_retry_H0") or "").strip()),
                "FRESH_H0_PROMPT_REQUIRED_FOR_LEARNER_PUBLICATION",
                item_id,
            )

    def render_core2_companion(
        self,
        companion_plan: Dict[str, Any],
        output_pdf_path: Path,
    ) -> Tuple[str, Dict[str, Any]]:
        self.validate_core2_plan(companion_plan)
        return super().render_core2_companion(companion_plan, output_pdf_path)


def render_core2_from_authoring_handoff(
    handoff: Mapping[str, Any],
    output_pdf_path: Path,
    *,
    companion_id: str,
    linked_core1_id: str,
    appendix_a: Mapping[str, Any] | None = None,
    appendix_c: Mapping[str, Any] | None = None,
) -> Tuple[str, Dict[str, Any]]:
    """Canonical one-call #336 -> #339 -> #327 production route."""
    companion_plan = AuthoringHandoffAdapter.build_core2_companion_plan(
        handoff,
        companion_id=companion_id,
        linked_core1_id=linked_core1_id,
        appendix_a=appendix_a,
        appendix_c=appendix_c,
    )
    return ProductionPrimaryPageComposer().render_core2_companion(companion_plan, output_pdf_path)
