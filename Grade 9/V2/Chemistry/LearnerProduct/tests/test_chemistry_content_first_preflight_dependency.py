import ast
import unittest
from pathlib import Path

HERE = Path(__file__).resolve()
ENGINE = HERE.parents[1] / "engine"


class ChemistryContentFirstPreflightDependencyTests(unittest.TestCase):
    def test_density_helper_uses_only_stdlib_imports(self):
        path = ENGINE / "chemistry_content_first_preflight.py"
        tree = ast.parse(path.read_text(encoding="utf-8"))
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.extend(alias.name.split(".", 1)[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imports.append(node.module.split(".", 1)[0])
        self.assertEqual(set(imports), {"__future__", "typing"})


if __name__ == "__main__":
    unittest.main()
