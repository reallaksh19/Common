import copy
import sys
import unittest
from pathlib import Path

ENGINE = Path(__file__).resolve().parents[1] / "engine"
TESTS = Path(__file__).resolve().parent
for p in (ENGINE, TESTS):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from blueprint_common import digest
from compile_publication_bundle import _seal_component
from materialize_intrinsic_depth import materialize_uniform_depth, depth_obligations
from validate_publication_bundle import validate_bundle
from test_intrinsic_depth_blueprint_validation import core1_pages, core2_pages, book


def _rename(value, mapping):
    if isinstance(value, dict):
        return {k: _rename(v, mapping) for k, v in value.items()}
    if isinstance(value, list):
        return [_rename(x, mapping) for x in value]
    if isinstance(value, str):
        return mapping.get(value, value)
    return value


def _prefixed_pages(pages, prefix):
    ids = []
    for page in pages:
        ids.append(page["page_id"])
        ids.extend(x["block_id"] for x in page.get("technical_blocks", []))
        ids.extend(x["block_id"] for x in page.get("prose_blocks", []))
        ids.extend(x["representation_id"] for x in page.get("representations", []))
        ids.extend(x["ttu_id"] for x in page.get("reconstructable_ttus", []))
        ids.extend(x["workspace_id"] for x in page.get("workspace_blocks", []))
    mapping = {x: prefix + "-" + x for x in ids}
    return _rename(copy.deepcopy(pages), mapping)


def make_visibility():
    visibility = {
        "schema_version": "1.0.0",
        "subject": "MATHEMATICS",
        "manifest_id": "",
        "view_class": "DERIVED_ENGINEERING_PRODUCT_VISIBILITY",
        "authority": "NON_AUTHORITATIVE_VIEW_OF_BOUND_ENGINEERING_AUTHORITY",
        "visibility_purpose": "LEARNER_AND_AUTHOR_EXPLAINABILITY",
        "visibility_notice": "Derived Engineering visibility for testing; this view explains technical custody and never authorizes publication.",
        "technical_authorization": "ALLOWED",
        "publication_authorization": "NOT_IMPLIED",
        "source_domain_admission_digest": "d" * 64,
        "source_release_gate_digest": "a" * 64,
        "registry_digest": "sha256:" + "e" * 64,
        "validator_contract_digest": "sha256:" + "f" * 64,
        "authorization_count": 1,
        "gate_count": 1,
        "authorizations": [{
            "authorization_id": "MATH-ENG-AUTH-TEST",
            "binding_id": "MATH-ENG-BIND-TEST",
            "request_id": "MATH-ENG-REQ-TEST",
            "engineering_depth": "STANDARD",
            "direct_gate_ids": ["MATH-TEST-GATE"],
            "transitive_gate_ids": ["MATH-TEST-GATE"],
            "closure_receipt_digest": "sha256:" + "1" * 64,
            "passport_digest": "2" * 64,
        }],
        "gates": [{
            "gate_id": "MATH-TEST-GATE",
            "scope_roles": ["DIRECT"],
            "authorization_refs": ["MATH-ENG-AUTH-TEST"],
            "requested_engineering_depths": ["STANDARD"],
            "learner_title": "Test Engineering Gate",
            "chapter": "Test chapter",
            "technical_state": "READY",
            "failure_codes": [],
            "prerequisite_ids": [],
            "provenance": {
                "authority_tier": "SOURCE-DEFINED",
                "source_scope": "IN_SCOPE",
                "claim_status": "VERIFIED_CANONICAL",
                "source_reference": "test-source",
            },
            "structure_counts": {
                "canonical_concepts": 1,
                "mandatory_equations": 1,
                "representations": 1,
                "model_conditions": 1,
                "reasoning_steps": 1,
                "transformations": 1,
                "misconceptions": 1,
                "verification_obligations": 1,
                "problem_families": 1,
                "falsification_cases": 1,
            },
            "difficulty_profile": {"provisional_difficulty": "EASY"},
            "release_checklist_pass": True,
            "representations": [{
                "representation_id": "REP-TEST",
                "representation_type": "TABLE",
                "name": "Test representation",
                "verification_method": "Check the governed relation.",
            }],
            "misconceptions": [{
                "misconception_id": "MISC-TEST",
                "incorrect_belief": "A test misconception.",
                "required_technical_repair": "Apply the governed invariant.",
            }],
            "verification_obligations": ["Verify the governed invariant."],
        }],
        "manifest_digest": "",
    }
    visibility["manifest_id"] = "MATH-ENG-VIS-" + digest({k: v for k, v in visibility.items() if k not in {"manifest_id", "manifest_digest"}})[:16]
    visibility["manifest_digest"] = digest(visibility, "manifest_digest")
    return visibility


def make_bundle():
    components = []
    for seq, badge in enumerate(("EASY", "MEDIUM", "HARD"), 1):
        pages = materialize_uniform_depth(core1_pages(), badge, book())
        pages = _prefixed_pages(pages, badge)
        obligations = depth_obligations(badge, pages)
        comp = _seal_component("MATH-CONCEPT-BP-", {
            "sequence": seq,
            "bucket_ref": f"BUCKET-{seq}",
            "subtopic_ref": f"SUBTOPIC-{seq}",
            "title": f"{badge.title()} concept",
            "difficulty_badge": badge,
            "pages": pages,
            "depth_obligations": obligations,
        })
        components.append(comp)
    problem = _seal_component("MATH-PROBLEM-BP-", {
        "governance": "LEARNER_FIT",
        "pages": core2_pages(),
    })
    visibility = make_visibility()
    bundle = {
        "schema_version": "1.1.0",
        "subject": "MATHEMATICS",
        "bundle_id": "",
        "source_release_status": "PASS",
        "source_release_gate_digest": "a" * 64,
        "generation_spec_digest": "b" * 64,
        "governed_example_catalog_digest": "c" * 64,
        "pedagogy_research_manifest_digest": None,
        "engineering_visibility_manifest_digest": visibility["manifest_digest"],
        "engineering_visibility": visibility,
        "concept_components": components,
        "problem_component": problem,
        "publication_stage_order": ["CORE1A", "CORE1B", "CORE2A", "CORE2B"],
        "bundle_digest": "",
    }
    bundle["bundle_id"] = "MATH-PUB-BUNDLE-" + digest({k: v for k, v in bundle.items() if k not in {"bundle_id", "bundle_digest"}})[:16]
    bundle["bundle_digest"] = digest(bundle, "bundle_digest")
    return bundle


def reseal(bundle):
    bundle["bundle_id"] = "MATH-PUB-BUNDLE-" + digest({k: v for k, v in bundle.items() if k not in {"bundle_id", "bundle_digest"}})[:16]
    bundle["bundle_digest"] = digest(bundle, "bundle_digest")


class PublicationBundleTests(unittest.TestCase):
    def test_mixed_easy_medium_hard_bundle_passes(self):
        audit = validate_bundle(make_bundle())
        self.assertEqual(audit["status"], "PASS")
        self.assertEqual(audit["difficulty_badge_counts"], {"EASY": 1, "MEDIUM": 1, "HARD": 1})
        self.assertEqual(audit["engineering_visibility_gate_count"], 1)
        self.assertEqual(audit["semantic_model"], "CONCEPT_BADGE_PLUS_PROBLEM_LEARNER_FIT_PLUS_ENGINEERING_VISIBILITY")

    def test_problem_component_has_no_intrinsic_difficulty_badge(self):
        bundle = make_bundle()
        self.assertNotIn("difficulty_badge", bundle["problem_component"])
        self.assertEqual(bundle["problem_component"]["governance"], "LEARNER_FIT")

    def test_engineering_visibility_cannot_authorize_publication(self):
        bundle = make_bundle()
        bundle["engineering_visibility"]["publication_authorization"] = "ALLOWED"
        bundle["engineering_visibility"]["manifest_digest"] = digest(bundle["engineering_visibility"], "manifest_digest")
        bundle["engineering_visibility_manifest_digest"] = bundle["engineering_visibility"]["manifest_digest"]
        reseal(bundle)
        with self.assertRaises(Exception):
            validate_bundle(bundle)

    def test_engineering_visibility_digest_mismatch_fails(self):
        bundle = make_bundle()
        bundle["engineering_visibility_manifest_digest"] = "0" * 64
        reseal(bundle)
        with self.assertRaisesRegex(ValueError, "MATH_PUBLICATION_BUNDLE_ENGINEERING_VISIBILITY_DIGEST_DRIFT"):
            validate_bundle(bundle)

    def test_duplicate_page_identity_across_concept_components_fails(self):
        bundle = make_bundle()
        bundle["concept_components"][1]["pages"][0]["page_id"] = bundle["concept_components"][0]["pages"][0]["page_id"]
        bundle["concept_components"][1]["component_digest"] = digest(bundle["concept_components"][1], "component_digest")
        material = {k: v for k, v in bundle["concept_components"][1].items() if k not in {"component_id", "component_digest"}}
        bundle["concept_components"][1]["component_id"] = "MATH-CONCEPT-BP-" + digest(material)[:16]
        bundle["concept_components"][1]["component_digest"] = digest(bundle["concept_components"][1], "component_digest")
        reseal(bundle)
        with self.assertRaisesRegex(ValueError, "MATH_PUBLICATION_BUNDLE_PAGE_ID_DUPLICATE"):
            validate_bundle(bundle)

    def test_problem_stage_leak_into_concept_component_fails(self):
        bundle = make_bundle()
        bundle["concept_components"][0]["pages"].append(copy.deepcopy(bundle["problem_component"]["pages"][0]))
        material = {k: v for k, v in bundle["concept_components"][0].items() if k not in {"component_id", "component_digest"}}
        bundle["concept_components"][0]["component_id"] = "MATH-CONCEPT-BP-" + digest(material)[:16]
        bundle["concept_components"][0]["component_digest"] = digest(bundle["concept_components"][0], "component_digest")
        reseal(bundle)
        with self.assertRaisesRegex(ValueError, "MATH_PUBLICATION_CONCEPT_COMPONENT_STAGE_DRIFT"):
            validate_bundle(bundle)


if __name__ == "__main__":
    unittest.main()
