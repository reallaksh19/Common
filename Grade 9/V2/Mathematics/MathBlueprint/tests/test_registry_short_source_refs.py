from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve()
ROOT = HERE.parents[1]
ENGINE = ROOT / "engine"
if str(ENGINE) not in sys.path:
    sys.path.insert(0, str(ENGINE))

from validate_canonical_domain_registry import validate_registry

GOLDEN = ROOT / "golden" / "domain_registry" / "01-theory-of-equations-registry.json"


class RegistryShortSourceRefTests(unittest.TestCase):
    def test_exact_two_character_core2_source_ref_is_legal(self):
        doc = json.loads(GOLDEN.read_text(encoding="utf-8"))
        source = next(x for x in doc["assets"] if x["asset_type"] == "SOURCE_QUESTION")
        source["core2_refs"] = ["Q9"]
        validate_registry(copy.deepcopy(doc))


if __name__ == "__main__":
    unittest.main(verbosity=2)
