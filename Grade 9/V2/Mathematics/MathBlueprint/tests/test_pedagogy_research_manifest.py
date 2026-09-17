from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

ENGINE = Path(__file__).resolve().parents[1] / "engine"
if str(ENGINE) not in sys.path:
    sys.path.insert(0, str(ENGINE))

from blueprint_common import digest  # noqa: E402
from validate_pedagogy_research_manifest import validate_manifest  # noqa: E402


def source(ref: str, supports: list[str], *, production: bool = False) -> dict:
    return {
        "research_ref": ref,
        "source_url": "https://example.org/" + ref.lower(),
        "source_title": "Governed pedagogy evidence fixture for claim-level promotion testing",
        "publisher": "TEST EVIDENCE",
        "accessed_on": "2026-09-15",
        "evidence_class": "VERIFIED_WEB_CAPTURE" if production else "TEST_FIXTURE",
        "capture_ref": ("CAPTURE:" if production else "TEST_FIXTURE:") + ref,
        "capture_digest": digest({"capture": ref}),
        "supports": supports,
    }


def seal(doc: dict) -> dict:
    doc["manifest_digest"] = digest(doc, "manifest_digest")
    return doc


def manifest(*, production: bool = False) -> dict:
    release_class = "PRODUCTION" if production else "TEST_ONLY"
    research_ref = "PED-WEB-CLAIM-PRIMARY"
    decision_ref = "PED-BRIEF-CLAIM-UNIT"
    doc = {
        "schema_version": "1.1.0",
        "subject": "MATHEMATICS",
        "manifest_id": "MATH-PED-RESEARCH-CLAIM-UNIT",
        "release_class": release_class,
        "curriculum_authority": False,
        "sources": [source(
            research_ref,
            ["REPRESENTATION_DESIGN", "MISCONCEPTION_REPAIR"],
            production=production,
        )],
        "decisions": [{
            "decision_ref": decision_ref,
            "subtopic_ref": "SUBTOPIC-UNIT",
            "research_depth": "STANDARD",
            "coverage": ["REPRESENTATION_DESIGN", "MISCONCEPTION_REPAIR"],
            "research_refs": [research_ref],
            "decision_summary": "Use retained evidence to govern representation design and misconception repair.",
        }],
        "claims": [
            {
                "claim_ref": "PED-CLAIM-REPRESENTATION-UNIT",
                "decision_ref": decision_ref,
                "support_category": "REPRESENTATION_DESIGN",
                "claim_text": "The selected representation should make the governed mathematical relation explicit.",
                "confidence": "MODERATE",
                "confidence_basis": "The retained evidence directly addresses representation design for this promoted decision.",
                "evidence_links": [{
                    "research_ref": research_ref,
                    "stance": "SUPPORTS",
                    "rationale": "The retained source directly addresses representation design.",
                }],
                "contradiction_resolution": None,
            },
            {
                "claim_ref": "PED-CLAIM-MISCONCEPTION-UNIT",
                "decision_ref": decision_ref,
                "support_category": "MISCONCEPTION_REPAIR",
                "claim_text": "The teaching design should explicitly repair a plausible misconception rather than merely warn about it.",
                "confidence": "MODERATE",
                "confidence_basis": "The retained evidence directly addresses misconception repair for this promoted decision.",
                "evidence_links": [{
                    "research_ref": research_ref,
                    "stance": "SUPPORTS",
                    "rationale": "The retained source directly addresses misconception repair.",
                }],
                "contradiction_resolution": None,
            },
        ],
        "manifest_digest": "",
    }
    return seal(doc)


class PedagogyResearchClaimLedgerTests(unittest.TestCase):
    def test_single_relevant_source_can_ground_multiple_claims_without_source_count_quota(self):
        validate_manifest(manifest())

    def test_declared_decision_coverage_requires_claim(self):
        doc = manifest()
        doc["claims"] = [doc["claims"][0]]
        seal(doc)
        with self.assertRaisesRegex(ValueError, "MATH_PEDAGOGY_RESEARCH_DECISION_CLAIM_COVERAGE_INCOMPLETE"):
            validate_manifest(doc)

    def test_all_retained_category_relevant_sources_must_be_classified(self):
        doc = manifest()
        second = source("PED-WEB-CLAIM-SECOND", ["REPRESENTATION_DESIGN"])
        doc["sources"].append(second)
        doc["decisions"][0]["research_refs"].append(second["research_ref"])
        seal(doc)
        with self.assertRaisesRegex(ValueError, "MATH_PEDAGOGY_RESEARCH_CLAIM_RELEVANT_SOURCE_UNCLASSIFIED"):
            validate_manifest(doc)

    def test_claim_cannot_promote_source_outside_its_decision(self):
        doc = manifest()
        second = source("PED-WEB-CLAIM-SECOND", ["REPRESENTATION_DESIGN"])
        doc["sources"].append(second)
        doc["claims"][0]["evidence_links"].append({
            "research_ref": second["research_ref"],
            "stance": "SUPPORTS",
            "rationale": "This source was not retained by the governing decision.",
        })
        seal(doc)
        with self.assertRaisesRegex(ValueError, "MATH_PEDAGOGY_RESEARCH_CLAIM_SOURCE_OUTSIDE_DECISION"):
            validate_manifest(doc)

    def test_claim_source_must_match_promoted_support_category(self):
        doc = manifest()
        second = source("PED-WEB-CLAIM-SECOND", ["TRANSFER_DESIGN"])
        doc["sources"].append(second)
        doc["decisions"][0]["research_refs"].append(second["research_ref"])
        doc["claims"][0]["evidence_links"].append({
            "research_ref": second["research_ref"],
            "stance": "SUPPORTS",
            "rationale": "An unrelated evidence category cannot ground this representation claim.",
        })
        seal(doc)
        with self.assertRaisesRegex(ValueError, "MATH_PEDAGOGY_RESEARCH_CLAIM_SOURCE_CATEGORY_MISMATCH"):
            validate_manifest(doc)

    def test_contradictory_evidence_requires_explicit_resolution(self):
        doc = manifest()
        second = source("PED-WEB-CLAIM-SECOND", ["REPRESENTATION_DESIGN"])
        doc["sources"].append(second)
        doc["decisions"][0]["research_refs"].append(second["research_ref"])
        doc["claims"][0]["evidence_links"].append({
            "research_ref": second["research_ref"],
            "stance": "CONTRADICTS",
            "rationale": "The second source points to a materially different representation choice.",
        })
        seal(doc)
        with self.assertRaisesRegex(ValueError, "MATH_PEDAGOGY_RESEARCH_CONTRADICTION_UNRESOLVED"):
            validate_manifest(doc)

    def test_resolved_contradiction_can_be_promoted(self):
        doc = manifest()
        second = source("PED-WEB-CLAIM-SECOND", ["REPRESENTATION_DESIGN"])
        doc["sources"].append(second)
        doc["decisions"][0]["research_refs"].append(second["research_ref"])
        doc["claims"][0]["evidence_links"].append({
            "research_ref": second["research_ref"],
            "stance": "CONTRADICTS",
            "rationale": "The second source points to a materially different representation choice.",
        })
        doc["claims"][0]["contradiction_resolution"] = (
            "The promoted choice is bounded to this instructional purpose; the conflicting alternative is retained for contexts requiring a different representation bridge."
        )
        seal(doc)
        validate_manifest(doc)

    def test_production_promotion_rejects_low_confidence_claim(self):
        doc = manifest(production=True)
        doc["claims"][0]["confidence"] = "LOW"
        doc["claims"][0]["confidence_basis"] = "Evidence is too uncertain to support production promotion of this claim."
        seal(doc)
        with self.assertRaisesRegex(ValueError, "MATH_PEDAGOGY_RESEARCH_PRODUCTION_LOW_CONFIDENCE_FORBIDDEN"):
            validate_manifest(doc)


if __name__ == "__main__":
    unittest.main(verbosity=2)
