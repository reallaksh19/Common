"""Adapter from #339 AuthoringLearningHandoff to #327 Core2 publication input.

This module does not select visuals, hints, or work surfaces.  It only translates
already-validated module support records into the existing Core2 Appendix-B seam.
Diagnostic probe modules are explicitly excluded from guided hint ladders.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Mapping


@dataclass
class AuthoringHandoffPublicationError(ValueError):
    code: str
    message: str

    def __str__(self) -> str:
        return f"{self.code}: {self.message}"


def _require(condition: bool, code: str, message: str) -> None:
    if not condition:
        raise AuthoringHandoffPublicationError(code, message)


class AuthoringHandoffAdapter:
    """Builds a Core2 companion input from a validated #339 handoff object."""

    @classmethod
    def validate_handoff(cls, handoff: Mapping[str, Any]) -> None:
        _require(handoff.get("schema_version") == "1.0.0", "AUTHORING_HANDOFF_SCHEMA_UNSUPPORTED", "expected schema_version 1.0.0")
        _require(handoff.get("publisher_invention_allowed") is False, "PUBLISHER_INVENTION_NOT_FORBIDDEN", "handoff must forbid publisher invention")
        coverage = handoff.get("coverage") or {}
        _require(int(coverage.get("unaccounted_modules", -1)) == 0, "AUTHORING_HANDOFF_COVERAGE_INCOMPLETE", "handoff contains unaccounted modules")
        _require(isinstance(handoff.get("module_support"), list), "AUTHORING_HANDOFF_MODULE_SUPPORT_MISSING", "module_support list required")

    @classmethod
    def build_core2_ladders(cls, handoff: Mapping[str, Any]) -> Dict[str, Any]:
        """Return guided ladders plus explicit probe-only module ids."""
        cls.validate_handoff(handoff)
        ladders: List[Dict[str, Any]] = []
        probe_module_ids: List[str] = []
        seen: set[str] = set()

        for row in handoff["module_support"]:
            if row.get("product") != "CORE2":
                continue
            module_id = str(row.get("module_id") or "").strip()
            _require(bool(module_id), "AUTHORING_HANDOFF_MODULE_ID_MISSING", "CORE2 support row needs module_id")
            _require(module_id not in seen, "AUTHORING_HANDOFF_DUPLICATE_MODULE", module_id)
            seen.add(module_id)
            status = row.get("support_status")

            if status == "INDEPENDENT_PROBE_ONLY":
                _require(row.get("learning_representation_plan") is None, "PROBE_MODULE_RECEIVED_GUIDED_HINTS", module_id)
                probe_module_ids.append(module_id)
                continue

            _require(status == "PLANNED", "AUTHORING_HANDOFF_UNKNOWN_SUPPORT_STATUS", f"{module_id}: {status}")
            plan = row.get("learning_representation_plan")
            _require(isinstance(plan, dict), "LEARNING_REPRESENTATION_PLAN_REQUIRED", module_id)
            _require(plan.get("publisher_invention_allowed") is False, "PUBLISHER_INVENTION_NOT_FORBIDDEN", module_id)
            _require(plan.get("task_ref") == module_id, "AUTHORING_HANDOFF_TASK_REF_MISMATCH", module_id)
            fresh_prompt = str(row.get("fresh_retry_prompt") or plan.get("fresh_retry_prompt") or "").strip()
            _require(bool(fresh_prompt), "FRESH_H0_PROMPT_REQUIRED_FOR_LEARNER_PUBLICATION", module_id)

            ladders.append({
                "item_id": module_id,
                "learning_representation_plan": plan,
                "fresh_independent_retry_H0": fresh_prompt,
            })

        return {
            "ladders": ladders,
            "independent_probe_module_ids": probe_module_ids,
            "guided_module_count": len(ladders),
            "probe_module_count": len(probe_module_ids),
        }

    @classmethod
    def build_core2_companion_plan(
        cls,
        handoff: Mapping[str, Any],
        *,
        companion_id: str,
        linked_core1_id: str,
        appendix_a: Mapping[str, Any] | None = None,
        appendix_c: Mapping[str, Any] | None = None,
    ) -> Dict[str, Any]:
        """Create the existing page-composer input without recreating pedagogy."""
        core2 = cls.build_core2_ladders(handoff)
        return {
            "companion_id": companion_id,
            "linked_core1_id": linked_core1_id,
            "appendix_a": dict(appendix_a or {"batches": []}),
            "appendix_b": {"ladders": core2["ladders"]},
            "appendix_c": dict(appendix_c or {}),
            "authoring_handoff_trace": {
                "handoff_id": handoff.get("handoff_id"),
                "input_ref": handoff.get("input_ref"),
                "guided_module_count": core2["guided_module_count"],
                "independent_probe_module_ids": core2["independent_probe_module_ids"],
                "publisher_invention_allowed": False,
            },
        }
