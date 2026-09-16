from __future__ import annotations

import ast
import json
import unittest
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "design"
ENGINE = ROOT / "engine"
CONTRACTS = ROOT / "contracts"
POLICIES = ROOT / "policies"


def string_literals(source: str) -> list[tuple[int, str]]:
    tree = ast.parse(source)
    rows: list[tuple[int, str]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            rows.append((getattr(node, "lineno", 0), node.value))
    return rows


def json_string_values(value: Any) -> list[str]:
    rows: list[str] = []
    if isinstance(value, str):
        rows.append(value)
    elif isinstance(value, list):
        for item in value:
            rows.extend(json_string_values(item))
    elif isinstance(value, dict):
        for key, item in value.items():
            if isinstance(key, str):
                rows.append(key)
            rows.extend(json_string_values(item))
    return rows


def is_design_reference(value: str, design_names: set[str], *, bare_dir: bool) -> bool:
    normalized = value.replace("\\", "/")
    if normalized.startswith("design/") or "/design/" in normalized:
        return True
    if bare_dir and normalized == "design":
        return True
    return any(name in normalized for name in design_names)


def python_design_reference_violations(
    source: str, design_names: set[str]
) -> list[tuple[int, str]]:
    return [
        (line, value)
        for line, value in string_literals(source)
        if is_design_reference(value, design_names, bare_dir=True)
    ]


def json_design_reference_violations(source: str, design_names: set[str]) -> list[str]:
    payload = json.loads(source)
    return [
        value
        for value in json_string_values(payload)
        if is_design_reference(value, design_names, bare_dir=False)
    ]


class DesignAuthorityBoundaryTests(unittest.TestCase):
    def test_every_design_markdown_is_explicitly_non_normative(self):
        docs = sorted(DESIGN.glob("*.md"))
        self.assertTrue(docs, "design workspace must contain at least one document")
        violations: list[str] = []
        for path in docs:
            header = "\n".join(path.read_text(encoding="utf-8").splitlines()[:12])
            if "Status:" not in header or "DESIGN" not in header or "NON-NORMATIVE" not in header:
                violations.append(path.name)
        self.assertEqual(
            violations,
            [],
            "Every MathBlueprint/design Markdown file must declare DESIGN / NON-NORMATIVE "
            "near the top so roadmap prose cannot be mistaken for current authority: "
            + "; ".join(violations),
        )

    def test_production_governance_does_not_consume_design_workspace(self):
        design_names = {path.name for path in DESIGN.glob("*.md")}
        violations: list[str] = []

        for path in sorted(ENGINE.glob("*.py")):
            source = path.read_text(encoding="utf-8")
            for line, value in python_design_reference_violations(source, design_names):
                violations.append(f"engine/{path.name}:{line}:{value}")

        for directory in (CONTRACTS, POLICIES):
            for path in sorted(directory.glob("*.json")):
                source = path.read_text(encoding="utf-8")
                for value in json_design_reference_violations(source, design_names):
                    violations.append(f"{directory.name}/{path.name}:{value}")

        self.assertEqual(
            violations,
            [],
            "Production MathBlueprint engine/contracts/policies must not consume design/ roadmap "
            "files as authority. Promote approved design through governed contracts/policies and "
            "validators first: "
            + "; ".join(violations),
        )

    def test_guard_detects_synthetic_design_consumption(self):
        synthetic_python = 'DESIGN_ROOT = "design"\nROADMAP = "design/FUTURE.md"\n'
        python_violations = python_design_reference_violations(
            synthetic_python, {"FUTURE.md"}
        )
        self.assertEqual(
            python_violations,
            [(1, "design"), (2, "design/FUTURE.md")],
        )

        synthetic_json = json.dumps(
            {"policy_ref": "design/FUTURE.md", "ordinary_term": "design"}
        )
        self.assertEqual(
            json_design_reference_violations(synthetic_json, {"FUTURE.md"}),
            ["design/FUTURE.md"],
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
