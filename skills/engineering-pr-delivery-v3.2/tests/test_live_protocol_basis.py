from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from live_protocol_basis import resolve


class LiveProtocolBasisTests(unittest.TestCase):
    def test_common_checkout_reports_current_v31_and_two_pass_basis(self):
        basis = resolve()
        self.assertEqual("relay-v3.1-live-protocol-basis", basis["schema_version"])
        self.assertEqual("V3.1", basis["protocol"])
        self.assertEqual("reallaksh19/Common", basis["common_repository"])
        self.assertRegex(basis["common_sha"], r"^[0-9a-f]{40}$")
        self.assertTrue(basis["two_pass_revision"].startswith("TPG-2P-"))


if __name__ == "__main__":
    unittest.main()
