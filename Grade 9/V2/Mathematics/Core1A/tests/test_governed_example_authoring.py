import sys
import unittest
from pathlib import Path

ENGINE = Path(__file__).resolve().parents[1] / "engine"
if str(ENGINE) not in sys.path:
    sys.path.insert(0, str(ENGINE))

import core1a_governed_example_authoring as governed


class GovernedExampleAuthoringTests(unittest.TestCase):
    def setUp(self):
        self.cap = "MATH-BINOMIAL-SQUARE-EXPANSION"
        self.registry = {
            "assets": [
                {
                    "asset_id": "REG-MATH-CAP-BINOMIAL",
                    "asset_type": "CAPABILITY",
                    "core1_refs": [self.cap],
                }
            ]
        }
        governed.install(self.registry)

    def test_candidate_bank_is_admitted_before_use(self):
        rows = governed.governed_bank(self.cap, "MATH-PF-TEST")
        self.assertGreaterEqual(len(rows), 6)
        self.assertEqual(len({x["example_asset_id"] for x in rows}), len(rows))
        self.assertTrue(all(x["admission_status"] == "ADMITTED" for x in rows))
        self.assertTrue(all(x["capability_registry_refs"] == ["REG-MATH-CAP-BINOMIAL"] for x in rows))
        self.assertTrue(all(len(x["content_digest"]) == 64 for x in rows))

    def test_missing_registry_capability_fails_closed(self):
        governed.install({"assets": []})
        with self.assertRaisesRegex(ValueError, "CORE1A_GOVERNED_EXAMPLE_CAPABILITY_NOT_IN_REGISTRY"):
            governed.governed_bank(self.cap, "MATH-PF-TEST")


if __name__ == "__main__":
    unittest.main()
