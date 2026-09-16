import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "engine"
sys.path.insert(0, str(ENGINE))

from build_chemistry_representations import profile_authorizes_primitive  # noqa: E402


class ChemistryRepresentationTopicNeutralityTests(unittest.TestCase):
    def setUp(self):
        self.primitive = {
            "primitive_id": "SYNTHETIC_SCOPED_PRIMITIVE",
            "capability_refs": ["CAP-SYNTHETIC"],
            "topic_scope_refs": ["SYNTHETIC_TOPIC_LABEL"],
        }
        self.profile = {
            "primary_primitives_by_capability": {
                "CAP-SYNTHETIC": ["SYNTHETIC_SCOPED_PRIMITIVE"],
            },
            "conditional_primitives": {},
        }

    def test_topic_scoped_primitive_is_authorized_by_explicit_capability_page_intent(self):
        self.assertTrue(
            profile_authorizes_primitive(
                self.profile,
                "CAP-SYNTHETIC",
                self.primitive,
            )
        )

    def test_topic_label_alone_cannot_authorize_primitive(self):
        no_mapping = copy.deepcopy(self.profile)
        no_mapping["primary_primitives_by_capability"] = {}
        self.assertFalse(
            profile_authorizes_primitive(
                no_mapping,
                "CAP-SYNTHETIC",
                self.primitive,
            )
        )

    def test_conditional_primitive_requires_capability_compatibility(self):
        conditional = copy.deepcopy(self.profile)
        conditional["primary_primitives_by_capability"] = {}
        conditional["conditional_primitives"] = {
            "SYNTHETIC_CONDITION": "SYNTHETIC_SCOPED_PRIMITIVE"
        }
        self.assertTrue(
            profile_authorizes_primitive(
                conditional,
                "CAP-SYNTHETIC",
                self.primitive,
            )
        )
        self.assertFalse(
            profile_authorizes_primitive(
                conditional,
                "CAP-OTHER",
                self.primitive,
            )
        )

    def test_generic_representation_engine_contains_no_topic_name_branch(self):
        text = (ENGINE / "build_chemistry_representations.py").read_text(encoding="utf-8").lower()
        for forbidden in ("re" + "dox", "perman" + "ganate", "mn" + "o4"):
            self.assertNotIn(forbidden, text)


if __name__ == "__main__":
    unittest.main()
