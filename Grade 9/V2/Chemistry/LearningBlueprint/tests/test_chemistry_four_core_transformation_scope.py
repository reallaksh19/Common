import copy
import unittest

from test_chemistry_four_core_compilation import (
    REGISTRY,
    make_manifest,
    make_production_audit,
    make_request,
    payloads,
    transform_ref,
)

from compile_chemistry_blueprint_obligations import compile_blueprint_obligations
from compile_chemistry_core_authority import compile_core_authority
from compile_chemistry_core_product_custody import (
    ChemistryCoreProductCustodyError,
    compile_core_product_custody,
)
from compile_chemistry_engineering_closure import digest as engineering_digest


class ChemistryFourCoreTransformationScopeTests(unittest.TestCase):
    def setUp(self):
        self.gate = REGISTRY["subtopic_gates"][0]
        self.request = make_request()
        self.audit_ref = "tests/in-memory-transform-scope-audit.json"
        self.manifest = make_manifest(self.gate, self.audit_ref)

    def _authority(self, packet, mode, realized):
        return compile_core_authority(
            mode,
            "TEST_ONLY",
            payloads()[mode],
            packet,
            realized,
            authority_id=f"CHEM-CORE-AUTH-TRANSFORM-SCOPE-{mode}",
            payload_ref=f"tests/transform-scope-{mode.lower()}.json",
        )

    def _scope(self, authority, audit, held_ref=None):
        held = ["HELD_TIER"] if held_ref else []
        tiers = ["TEST_TIER"]
        guards = []
        if held_ref:
            guards = [{"fingerprint": held_ref, "detection_tokens": ["held marker"]}]
        return {
            "schema_version": "1.0.0",
            "scope_contract_id": f"CHEM-CORE-SCOPE-TRANSFORM-SCOPE-{authority['product_mode']}",
            "product_mode": authority["product_mode"],
            "gate_id": audit["gate_id"],
            "subtopic_id": authority["subtopic_id"],
            "source_audit_ref": self.audit_ref,
            "source_audit_digest": engineering_digest(audit),
            "learner_grade": 9,
            "program_context": "GRADE_LEVEL",
            "authorized_scope_tiers": tiers,
            "held_scope_tiers": held,
            "extension_authority_ref": "",
            "extension_reason": "",
            "scope_unit_assignments": [{**row, "scope_tier": "TEST_TIER"} for row in authority["scope_units"]],
            "held_transformation_guards": guards,
            "status": "CORE_SCOPE_READY",
        }

    def test_held_targeted_transformation_is_not_required_and_cannot_be_realized(self):
        audit = make_production_audit(self.gate)
        audit["scope_tiers"].append({
            "tier_id": "HELD_TIER",
            "grade_band": "9",
            "minimum_learner_grade": 9,
            "description": "Test-only held transformation tier for generic custody falsification."
        })
        held_transform = next(
            transform_ref(row)
            for row in self.gate["required_transformations"]
            if row["target_core_role"] == "CORE1B_GENERATIVE_RECONSTRUCTION"
        )
        binding = next(row for row in audit["asset_bindings"] if row["asset_ref"] == held_transform)
        binding["scope_tier_id"] = "HELD_TIER"
        binding["claim_class"] = "SOURCE_SCOPE_HELD"
        packet = compile_blueprint_obligations(
            self.request,
            self.manifest,
            registry=REGISTRY,
            source_audit_payloads={self.audit_ref: audit},
        )
        held_obligation = next(
            row for row in packet["obligations"]
            if row["kind"] == "TRANSFORMATION" and row["asset_ref"] == held_transform
        )
        self.assertEqual(held_obligation["required_realization_modes"], [])

        realized = [
            row["obligation_id"] for row in packet["obligations"]
            if "CORE1B" in row["authorized_modes"] and row["obligation_id"] != held_obligation["obligation_id"]
        ]
        authority = self._authority(packet, "CORE1B", realized)
        scope = self._scope(authority, audit, held_transform)
        custody = compile_core_product_custody(
            self.request,
            self.manifest,
            packet,
            scope,
            authority,
            registry=REGISTRY,
            source_audit_payloads={self.audit_ref: audit},
        )
        self.assertEqual(custody["status"], "CORE_PRODUCT_CUSTODY_READY")

        bad_authority = self._authority(packet, "CORE1B", realized + [held_obligation["obligation_id"]])
        with self.assertRaises(ChemistryCoreProductCustodyError) as ctx:
            compile_core_product_custody(
                self.request,
                self.manifest,
                packet,
                scope,
                bad_authority,
                registry=REGISTRY,
                source_audit_payloads={self.audit_ref: audit},
            )
        self.assertEqual(ctx.exception.code, "CHEM_CORE_CUSTODY_HELD_TRANSFORMATION_REALIZED")

    def test_authorized_targeted_transformation_is_required_at_custody(self):
        audit = make_production_audit(self.gate)
        packet = compile_blueprint_obligations(
            self.request,
            self.manifest,
            registry=REGISTRY,
            source_audit_payloads={self.audit_ref: audit},
        )
        target = next(
            row for row in packet["obligations"]
            if row["kind"] == "TRANSFORMATION"
            and row["direct"]
            and "CORE1A" in row["authorized_modes"]
        )
        realized = [
            row["obligation_id"] for row in packet["obligations"]
            if "CORE1A" in row["authorized_modes"] and row["obligation_id"] != target["obligation_id"]
        ]
        authority = self._authority(packet, "CORE1A", realized)
        scope = self._scope(authority, audit)
        with self.assertRaises(ChemistryCoreProductCustodyError) as ctx:
            compile_core_product_custody(
                self.request,
                self.manifest,
                packet,
                scope,
                authority,
                registry=REGISTRY,
                source_audit_payloads={self.audit_ref: audit},
            )
        self.assertEqual(ctx.exception.code, "CHEM_CORE_CUSTODY_AUTHORIZED_TRANSFORMATION_MISSING")


if __name__ == "__main__":
    unittest.main()
