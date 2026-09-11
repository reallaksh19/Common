#!/usr/bin/env python3
"""Fail-closed checks for Primary diagnostic reasoning companion semantics."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SCHEMA = ROOT / "primary-diagnostic-reasoning.schema.json"
EXAMPLE = ROOT / "examples" / "division-zero-place-diagnostic-probe.example.json"


def fail(message: str) -> None:
    raise SystemExit(f"Primary diagnostic reasoning validation failed: {message}")


def load(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"cannot parse {path.relative_to(ROOT)}: {exc}")


def main() -> None:
    schema = load(SCHEMA)
    example = load(EXAMPLE)

    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        fail("companion schema must declare JSON Schema draft 2020-12")

    strategy = example.get("strategySupportEvidence") or {}
    if strategy.get("producedBy") != "CHILD":
        fail("regression fixture must preserve child production")
    initiation = strategy.get("initiation") or {}
    if not initiation.get("actor") or not initiation.get("mode"):
        fail("strategy production and initiation must be represented separately")
    if initiation.get("mode") == "EXPLICIT_DIRECTION" and strategy.get("conceptualSupport", {}).get("level") == "H0":
        fail("explicit direction cannot be represented as H0 independent support in the reference fixture")

    provenance = example.get("workStepProvenance") or {}
    required_provenance = {"actor", "productionState", "supportState", "transcriptionCertainty"}
    if not required_provenance.issubset(provenance):
        fail("work-step provenance must preserve actor, production state, support state and transcription certainty")

    contrast = example.get("contrastSet") or {}
    focal = contrast.get("focalFeature") or {}
    if not focal.get("id"):
        fail("ContrastSet requires an explicit focal feature")
    cases = contrast.get("cases") or []
    if len(cases) < 2:
        fail("ContrastSet requires at least two cases")
    values = {case.get("focalFeatureValue") for case in cases}
    if len(values) < 2:
        fail("reference ContrastSet must actually vary the focal feature")
    if not contrast.get("controlledSharedFeatures"):
        fail("ContrastSet must declare shared controlled structure")

    hypotheses = example.get("competingHypotheses") or []
    if not 2 <= len(hypotheses) <= 3:
        fail("diagnostic reasoning should keep 2-3 competing hypotheses in the reference fixture")
    hypothesis_ids = {h.get("hypothesisId") for h in hypotheses}
    if None in hypothesis_ids or len(hypothesis_ids) != len(hypotheses):
        fail("competing hypothesis ids must be present and unique")

    probe = example.get("diagnosticProbe") or {}
    probe_hypotheses = set(probe.get("hypothesisIds") or [])
    if probe_hypotheses != hypothesis_ids:
        fail("DiagnosticProbe must explicitly target the competing hypotheses in the fixture")
    manipulated = probe.get("manipulatedFeature") or {}
    if manipulated.get("id") != focal.get("id"):
        fail("DiagnosticProbe should manipulate the same focal feature as the ContrastSet")
    load = probe.get("controlledLoad") or {}
    for key in ("language", "representationNovelty", "factRetrievalDemand"):
        if load.get(key) == "HIGH":
            fail(f"diagnostic probe unnecessarily raises {key} in the regression fixture")
    if not probe.get("items"):
        fail("DiagnosticProbe requires at least one item")
    rules = probe.get("outcomeRules") or []
    if not rules:
        fail("DiagnosticProbe requires outcome interpretation rules")
    for rule in rules:
        if not rule.get("when"):
            fail("every outcome rule must describe an observed response pattern")
        if not any(k in rule for k in ("increasesHypothesis", "decreasesHypothesis", "keepOpen", "consider", "informationNeeded")):
            fail("every outcome rule must update or preserve diagnostic reasoning state")

    print("Primary diagnostic reasoning v1 companion fixture passed canonical invariants.")


if __name__ == "__main__":
    main()
