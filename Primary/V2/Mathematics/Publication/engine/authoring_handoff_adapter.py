"""Adapter from #339 AuthoringLearningHandoff to #327 publication inputs.

This module does not select visuals, hints, or work surfaces. It translates
already-validated module support records into publisher inputs. Diagnostic PROBE
modules are explicitly independent-only and never acquire guided support here.
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
    """Consumes a validated #339 handoff without publisher-local pedagogy."""

    @classmethod
    def validate_handoff(cls, handoff: Mapping[str, Any]) -> None:
        _require(handoff.get("schema_version") == "1.0.0", "AUTHORING_HANDOFF_SCHEMA_UNSUPPORTED", "expected schema_version 1.0.0")
        _require(handoff.get("publisher_invention_allowed") is False, "PUBLISHER_INVENTION_NOT_FORBIDDEN", "handoff must forbid publisher invention")
        coverage = handoff.get("coverage") or {}
        _require(int(coverage.get("unaccounted_modules", -1)) == 0, "AUTHORING_HANDOFF_COVERAGE_INCOMPLETE", "handoff contains unaccounted modules")
        _require(isinstance(handoff.get("module_support"), list), "AUTHORING_HANDOFF_MODULE_SUPPORT_MISSING", "module_support list required")

    @classmethod
    def _validate_planned_row(cls, row: Mapping[str, Any], module_id: str) -> Dict[str, Any]:
        _require(row.get("support_status") == "PLANNED", "AUTHORING_HANDOFF_UNKNOWN_SUPPORT_STATUS", f"{module_id}: {row.get('support_status')}")
        plan = row.get("learning_representation_plan")
        _require(isinstance(plan, dict), "LEARNING_REPRESENTATION_PLAN_REQUIRED", module_id)
        _require(plan.get("publisher_invention_allowed") is False, "PUBLISHER_INVENTION_NOT_FORBIDDEN", module_id)
        _require(plan.get("task_ref") == module_id, "AUTHORING_HANDOFF_TASK_REF_MISMATCH", module_id)
        return dict(plan)

    @classmethod
    def build_core1_items(cls, handoff: Mapping[str, Any]) -> Dict[str, Any]:
        """Return validated Core1 module items without converting them to old sections."""
        cls.validate_handoff(handoff)
        authoring = handoff.get("authoring_result") or {}
        modules = list(((authoring.get("core1_plan") or {}).get("modules") or []))
        concepts = {
            str(c.get("concept_id")): c
            for c in ((authoring.get("skill_model") or {}).get("concepts") or [])
            if c.get("concept_id")
        }
        module_index = {str(m.get("module_id")): m for m in modules if m.get("module_id")}
        _require(len(module_index) == len(modules), "AUTHORING_HANDOFF_DUPLICATE_MODULE", "Core1 module ids must be unique")

        support_rows = [row for row in handoff["module_support"] if row.get("product") == "CORE1"]
        support_ids = {str(row.get("module_id") or "") for row in support_rows}
        _require(support_ids == set(module_index), "CORE1_HANDOFF_COVERAGE_INCOMPLETE", "Core1 module/support rows do not match exactly")

        items: List[Dict[str, Any]] = []
        probe_module_ids: List[str] = []
        seen: set[str] = set()
        for row in support_rows:
            module_id = str(row.get("module_id") or "").strip()
            _require(module_id not in seen, "AUTHORING_HANDOFF_DUPLICATE_MODULE", module_id)
            seen.add(module_id)
            module = module_index[module_id]
            concept_ref = str(module.get("concept_ref") or "")
            concept = concepts.get(concept_ref) or {}
            status = row.get("support_status")

            if status == "INDEPENDENT_PROBE_ONLY":
                _require(row.get("learning_representation_plan") is None, "PROBE_MODULE_RECEIVED_GUIDED_HINTS", module_id)
                probe_module_ids.append(module_id)
                continue

            plan = cls._validate_planned_row(row, module_id)
            items.append({
                "module_id": module_id,
                "concept_ref": concept_ref,
                "concept_title": concept.get("title", module_id),
                "concept_mode": module.get("concept_mode"),
                "objective": module.get("objective", ""),
                "learner_action": module.get("learner_action", ""),
                "source_refs": list(module.get("source_refs") or []),
                "learning_representation_plan": plan,
            })

        return {
            "items": items,
            "independent_probe_module_ids": probe_module_ids,
            "planned_module_count": len(items),
            "probe_module_count": len(probe_module_ids),
        }

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

            plan = cls._validate_planned_row(row, module_id)
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
