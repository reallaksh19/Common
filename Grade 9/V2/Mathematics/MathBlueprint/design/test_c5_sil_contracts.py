#!/usr/bin/env python3
"""Mutation falsifiers for the C5 SIL design contracts and PR #395 integration."""
from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

DESIGN = Path(__file__).resolve().parent
ROOT = DESIGN.parent
if str(DESIGN) not in sys.path:
    sys.path.insert(0, str(DESIGN))

from validate_c5_sil_contracts import (  # noqa: E402
    C4_RECEIPT_PATH,
    CATALOG_PATH,
    DOMAIN_SCHEMA_PATH,
    INTEGRATION_PATH,
    load,
    load_schemas,
    validate_documents,
)


class C5SILContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.catalog = load(CATALOG_PATH)
        self.integration = load(INTEGRATION_PATH)
        self.schemas = load_schemas(self.catalog)
        self.c4 = load(C4_RECEIPT_PATH)
        self.domain = load(DOMAIN_SCHEMA_PATH)

    def validate(self, catalog=None, integration=None, schemas=None, c4=None, domain=None):
        return validate_documents(
            catalog or self.catalog,
            integration or self.integration,
            schemas or self.schemas,
            c4 or self.c4,
            domain or self.domain,
            check_disk_custody=False,
        )

    def test_baseline_passes(self) -> None:
        self.assertEqual(self.validate(), [])

    def test_pack_cannot_grant_technical_authority(self) -> None:
        schemas = copy.deepcopy(self.schemas)
        schemas["SIL-PACK"]["properties"]["technical_authorization"]["const"] = "ALLOWED"
        self.assertIn("C5_PACK_TECH_AUTH", self.validate(schemas=schemas))

    def test_pack_cannot_inline_subject_truth(self) -> None:
        schemas = copy.deepcopy(self.schemas)
        schemas["SIL-PACK"]["properties"]["expression"] = {"type": "string"}
        self.assertIn("C5_INLINE_SUBJECT_TRUTH_FORBIDDEN", self.validate(schemas=schemas))

    def test_coverage_pass_cannot_authorize(self) -> None:
        schemas = copy.deepcopy(self.schemas)
        schemas["SIL-COVERAGE"]["properties"]["publication_authorization"]["const"] = "ALLOWED"
        self.assertIn("C5_COVERAGE_PUBLICATION_AUTH", self.validate(schemas=schemas))

    def test_pr395_whole_branch_merge_is_forbidden(self) -> None:
        integration = copy.deepcopy(self.integration)
        integration["source_pull_request"]["whole_branch_merge_authorized"] = True
        self.assertIn("C5_PR395_WHOLE_MERGE", self.validate(integration=integration))

    def test_pr395_candidate_surface_cannot_become_authority(self) -> None:
        integration = copy.deepcopy(self.integration)
        integration["candidate_surfaces"][0]["classification"] = "AUTHORITATIVE_SUBJECT_TRUTH"
        self.assertIn("C5_PR395_SURFACE_CLASSIFICATION", self.validate(integration=integration))

    def test_pr395_head_pin_is_exact(self) -> None:
        integration = copy.deepcopy(self.integration)
        integration["source_pull_request"]["head_sha"] = "0" * 40
        self.assertIn("C5_PR395_HEAD", self.validate(integration=integration))

    def test_c4_gate_must_precede_c5(self) -> None:
        c4 = copy.deepcopy(self.c4)
        c4["next_stage"] = "SOMETHING_ELSE"
        self.assertIn("C5_C4_NEXT_STAGE", self.validate(c4=c4))

    def test_f007_remains_documented_only(self) -> None:
        c4 = copy.deepcopy(self.c4)
        c4["tracked_runtime_gap"]["runtime_auto_materialization_executable"] = True
        self.assertIn("C5_F007_EXECUTABLE", self.validate(c4=c4))


if __name__ == "__main__":
    unittest.main()
