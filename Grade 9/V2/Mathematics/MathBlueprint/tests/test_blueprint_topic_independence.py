from __future__ import annotations

import ast
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "engine"
if str(ENGINE) not in sys.path:
    sys.path.insert(0, str(ENGINE))

from compile_mathematics_engineering_workbench import load as load_engineering  # noqa: E402
from engineering_registry_composition import load_extension_catalog  # noqa: E402
from validate_assessment_engineering_crosswalk import (  # noqa: E402
    DEFAULT_CROSSWALK,
    load as load_crosswalk,
)

# This file is an upstream Engineering-authoring generator. Topic-specific
# mathematical source data is legal there; the prohibition applies to Blueprint
# runtime/orchestration consumers of Engineering authority.
ENGINEERING_AUTHORING_EXEMPTIONS = {
    "build_mathematics_engineering_gate_registry.py",
}


def authority_literals() -> set[str]:
    """Derive forbidden runtime literals from current Engineering authority.

    No topic/gate/capability blacklist is maintained in this test. If Engineering
    data grows, this guard grows automatically.
    """
    registry = load_engineering("policies/mathematics-technical-engineering-gates.v1.json")
    tokens: set[str] = set()
    for gate in registry["subtopic_gates"]:
        tokens.add(gate["subtopic_id"])
        tokens.update(gate.get("prerequisite_ids") or [])
        tokens.update(gate.get("linked_buckets") or [])
        tokens.update(gate.get("linked_problem_family_ids") or [])
        tokens.update(row["concept_id"] for row in gate.get("technical_core") or [])
        tokens.update(row["equation_id"] for row in gate.get("mandatory_equations") or [])
        tokens.update(row["representation_id"] for row in gate.get("representations") or [])
        tokens.update(row["misconception_id"] for row in gate.get("misconceptions") or [])
        tokens.update(row["family_id"] for row in gate.get("problem_families") or [])

    crosswalk = load_crosswalk(DEFAULT_CROSSWALK)
    tokens.update(row["capability_ref"] for row in crosswalk["rows"])

    catalog = load_extension_catalog()
    for entry in catalog["extensions"]:
        ref = entry["extension_ref"]
        tokens.add(ref)
        tokens.add(Path(ref).name)

    return {token for token in tokens if isinstance(token, str) and token}


def literal_violations(source: str, forbidden: set[str]) -> list[tuple[int, str]]:
    tree = ast.parse(source)
    violations: list[tuple[int, str]] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Constant) or not isinstance(node.value, str):
            continue
        value = node.value
        for token in forbidden:
            if token in value:
                violations.append((getattr(node, "lineno", 0), token))
    return violations


class BlueprintTopicIndependenceTests(unittest.TestCase):
    def test_runtime_orchestration_contains_no_engineering_topic_literals(self):
        forbidden = authority_literals()
        self.assertTrue(forbidden)
        violations: list[str] = []
        for path in sorted(ENGINE.glob("*.py")):
            if path.name in ENGINEERING_AUTHORING_EXEMPTIONS:
                continue
            source = path.read_text(encoding="utf-8")
            for line, token in literal_violations(source, forbidden):
                violations.append(f"{path.name}:{line}:{token}")
        self.assertEqual(
            violations,
            [],
            "Blueprint runtime/orchestration contains Engineering topic-specific literals; "
            "move mathematical identity/mapping into governed Engineering data: "
            + "; ".join(violations),
        )

    def test_guard_detects_a_data_derived_topic_leak(self):
        token = sorted(authority_literals())[0]
        synthetic_source = f'LEAK = {token!r}\n'
        self.assertEqual(literal_violations(synthetic_source, {token}), [(1, token)])


if __name__ == "__main__":
    unittest.main(verbosity=2)
