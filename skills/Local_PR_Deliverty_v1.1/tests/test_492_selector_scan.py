import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
SPEC = importlib.util.spec_from_file_location("selector_scan", ROOT / "scripts" / "selector_scan.py")
module = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(module)


class SelectorScan492Tests(unittest.TestCase):
    def test_live_common_agents_v32_selector_is_visible_and_overridden(self):
        text = (REPO / "AGENTS.md").read_text(encoding="utf-8")
        result = module.scan_selector_text(text, source="AGENTS.md")
        self.assertEqual(result["status"], "OVERRIDDEN_SELECTOR_CONFLICT")
        self.assertEqual(result["effective_relay_path"], "skills/engineering-pr-delivery-v3.5")
        self.assertTrue(any(row["selected_path"] == "skills/engineering-pr-delivery-v3.2" for row in result["findings"]))

    def test_v35_repository_selector_has_no_conflict(self):
        result = module.scan_selector_text(
            "COMMON_POLICY_SOURCE: skills/engineering-pr-delivery-v3.5/",
            source="AGENTS.md",
        )
        self.assertEqual(result["status"], "PASS")
        self.assertTrue(result["observed_v35"])

    def test_historical_prose_is_not_scanned_as_selector_surface_implicitly(self):
        # Caller controls which files are selector surfaces. The scanner does not crawl
        # docs/issues and therefore cannot promote historical prose to active authority.
        result = module.scan_selector_text("No relay selector is declared here.", source="selector.conf")
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["findings"], [])

    def test_scanner_rejects_higher_authority_source_levels(self):
        with self.assertRaisesRegex(module.SelectorScanError, "lower-precedence"):
            module.scan_selector_text(
                "skills/engineering-pr-delivery-v3.2/",
                source="TASK",
                source_level="TASK_PIN",
            )


if __name__ == "__main__":
    unittest.main()
