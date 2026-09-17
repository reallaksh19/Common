#!/usr/bin/env python3
"""Mutation falsifiers for the C5 SIL family, field contracts and PR #395 custody."""
from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

DESIGN = Path(__file__).resolve().parent
if str(DESIGN) not in sys.path:
    sys.path.insert(0, str(DESIGN))

from validate_c5_sil_contracts import (  # noqa: E402
    C4_RECEIPT_PATH,
    DOMAIN_SCHEMA_PATH,
    FAMILY_PATH,
    FAMILY_SCHEMA_PATH,
    load,
    load_field_schemas,
    validate_documents,
)


class C5SILContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.family = load(FAMILY_PATH)
        self.family_schema = load(FAMILY_SCHEMA_PATH)
        self.fields = load_field_schemas()
        self.c4 = load(C4_RECEIPT_PATH)
        self.domain = load(DOMAIN_SCHEMA_PATH)

    def validate(self, family=None, family_schema=None, fields=None, c4=None, domain=None):
        return validate_documents(
            family or self.family,
            family_schema or self.family_schema,
            fields or self.fields,
            c4 or self.c4,
            domain or self.domain,
            receipt=None,
            check_disk_custody=False,
        )

    def test_baseline_passes(self) -> None:
        self.assertEqual(self.validate(), [])

    def test_family_cannot_inline_subject_truth(self) -> None:
        family = copy.deepcopy(self.family)
        family["central_doctrine"]["pack_may_define_subject_truth"] = True
        self.assertIn("C5_PACK_SUBJECT_TRUTH", self.validate(family=family))

    def test_pr395_runtime_import_is_forbidden(self) -> None:
        family = copy.deepcopy(self.family)
        family["pr395_integration"]["direct_runtime_import_allowed"] = True
        self.assertIn("C5_PR395_RUNTIME_IMPORT", self.validate(family=family))

    def test_pr395_head_pin_is_exact(self) -> None:
        family = copy.deepcopy(self.family)
        family["pr395_integration"]["source_head_sha"] = "0" * 40
        self.assertIn("C5_PR395_HEAD", self.validate(family=family))

    def test_pack_schema_cannot_inline_equation_payload(self) -> None:
        fields = copy.deepcopy(self.fields)
        fields["STEM-SIL-SUBTOPIC-PACK"]["properties"]["expression"] = {"type": "string"}
        self.assertIn("C5_INLINE_SUBJECT_TRUTH_FORBIDDEN", self.validate(fields=fields))

    def test_pack_schema_must_match_family_authority_lock(self) -> None:
        fields = copy.deepcopy(self.fields)
        fields["STEM-SIL-SUBTOPIC-PACK"]["properties"]["authority"]["const"] = "NONE"
        self.assertIn("C5_PACK_SCHEMA_AUTHORITY", self.validate(fields=fields))

    def test_instructional_transition_cannot_replace_logical_dependency(self) -> None:
        family = copy.deepcopy(self.family)
        for row in family["dependency_classes"]:
            if row["dependency_class"] == "LOGICAL_DEPENDENCY":
                row["owner_domain"] = "LEARNING_STRUCTURE"
                row["sil_may_define"] = True
        errors = self.validate(family=family)
        self.assertIn("C5_DEPENDENCY_OWNER", errors)
        self.assertIn("C5_DEPENDENCY_AUTHORITY", errors)

    def test_coverage_cannot_authorize_publication(self) -> None:
        fields = copy.deepcopy(self.fields)
        fields["STEM-SIL-COVERAGE-REPORT"]["properties"]["publication_authorization"]["const"] = "ALLOWED"
        self.assertIn("C5_COVERAGE_PUBLICATION_AUTH", self.validate(fields=fields))

    def test_unresolved_exact_reference_must_block(self) -> None:
        family = copy.deepcopy(self.family)
        family["exact_reference_contract"]["unresolved_ref_action"] = "GENERATE_PLAUSIBLE_CONTENT"
        self.assertIn("C5_UNRESOLVED_REF_ACTION", self.validate(family=family))

    def test_f007_remains_documented_only(self) -> None:
        family = copy.deepcopy(self.family)
        family["tracked_runtime_gap"]["runtime_auto_materialization_executable"] = True
        self.assertIn("C5_F007_EXECUTABLE", self.validate(family=family))


if __name__ == "__main__":
    unittest.main()
