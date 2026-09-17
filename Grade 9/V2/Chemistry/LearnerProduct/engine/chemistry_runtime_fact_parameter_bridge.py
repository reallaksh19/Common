#!/usr/bin/env python3
"""Install governed v2 representation runtime-parameter consumption.

Intent-bound representation rows are produced by the LearningBlueprint compiler and
may consume only their governed ``runtime_parameters`` plus declarative semantic and
primitive authority already present in the bundle. Legacy non-intent representation
rows remain on the pre-v2 renderer path for compatibility.
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Callable

HERE = Path(__file__).resolve()
CHEM_ROOT = HERE.parents[2]
sys.path.insert(0, str(CHEM_ROOT / "ExactProduct" / "engine"))

import chemistry_visual_primitives as VP  # noqa: E402

_INSTALLED = False


def _governed_params(rep: dict[str, Any], extra: dict[str, Any] | None, renderer: Any) -> dict[str, Any]:
    extra = extra or {}
    data = rep.get("runtime_parameters")
    if data is None:
        data = {}
    if not isinstance(data, dict):
        raise ValueError("CHEM_LP_RENDER_RUNTIME_PARAMETERS_INVALID")
    if rep.get("runtime_fact_ref") and not data:
        raise ValueError("CHEM_LP_RENDER_RUNTIME_FACT_PARAMETERS_REQUIRED")

    semantics = rep.get("scientific_semantics") or {}
    if not isinstance(semantics, dict):
        raise ValueError("CHEM_LP_RENDER_SCIENTIFIC_SEMANTICS_INVALID")
    checks = data.get("checks") or []
    if not checks and semantics.get("verification_method"):
        checks = [semantics["verification_method"]]
    entities = data.get("chemical_entities") or []

    return VP.build_params(
        primitive_id=rep["primitive_id"],
        tokens=extra.get("tokens") or entities,
        declared_entities=entities,
        instructional_job=renderer.public_text(rep.get("instructional_job", "")),
        attention_target=renderer.public_text(rep.get("attention_target", "")),
        learner_action=renderer.public_text(rep.get("learner_action_expected", "")),
        condition_context=renderer.public_list(extra.get("condition_context") or []),
        species_roles=renderer.public_list(data.get("species_roles") or []),
        checks=renderer.public_list(checks),
        observation=renderer.public_text(extra.get("observation", "")) if extra.get("observation") else None,
        oxidation_states=data.get("oxidation_states") or [],
        particles=extra.get("particles") or data.get("particles") or [],
        site_labels=data.get("site_labels") or [],
        accessibility_text=renderer.public_text(rep.get("accessibility_text", "")),
        safe=renderer.public_text,
    )


def install() -> None:
    global _INSTALLED
    if _INSTALLED:
        return
    import render_chemistry_learner_products as renderer

    legacy: Callable[..., dict[str, Any]] = renderer.params_from_representation

    def params_from_representation(rep: dict[str, Any], extra: dict[str, Any] | None = None) -> dict[str, Any]:
        if "intent_ref" not in rep:
            return legacy(rep, extra)
        return _governed_params(rep, extra, renderer)

    params_from_representation.__name__ = "params_from_governed_representation"
    renderer.params_from_representation = params_from_representation
    _INSTALLED = True


__all__ = ["install"]
