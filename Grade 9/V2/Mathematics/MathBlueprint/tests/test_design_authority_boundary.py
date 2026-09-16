from __future__ import annotations

import ast
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "design"
ENGINE = ROOT / "engine"


def string_literals(source: str) -> list[tuple[int, str]]:
    tree = ast.parse(source)
    rows: list[tuple[int, str]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            rows.append((getattr(node, "lineno", 0), node.value))
    return rows


def design_reference_violations(source: str, design_names: set[str]) -> list[tuple[int, str]]:
    violations: list[tuple[int, str]] = []
    for line, value in string_literals(source):
        normalized = value.replace("\\", "/")
        if normalized == "design" or normalized.startswith("design/") or "/design/" in normalized:
            violations.append((line, value))
            continue
        if any(name in normalized for name in design_names):
            violations.append((line, value))
    return violations


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

    def test_production_engine_does_not_consume_design_workspace(self):
        design_names = {path.name for path in DESIGN.glob("*.md")}
        violations: list[str] = []
        for path in sorted(ENGINE.glob("*.py")):
            source = path.read_text(encoding="utf-8")
            for line, value in design_reference_violations(source, design_names):
                violations.append(f"{path.name}:{line}:{value}")
        self.assertEqual(
            violations,
            [],
            "Production MathBlueprint engine code must not consume design/ roadmap files as "
            "runtime authority. Promote approved design through governed contracts/policies first: "
            + "; ".join(violations),
        )

    def test_guard_detects_synthetic_design_consumption(self):
        synthetic_source = 'DESIGN_ROOT = "design"\nROADMAP = "design/FUTURE.md"\n'
        violations = design_reference_violations(synthetic_source, {"FUTURE.md"})
        self.assertEqual(violations, [(1, "design"), (2, "design/FUTURE.md")])


if __name__ == "__main__":
    unittest.main(verbosity=2)
