import sys
import unittest
from pathlib import Path

ENGINE = Path(__file__).resolve().parents[1] / "engine"
if str(ENGINE) not in sys.path:
    sys.path.insert(0, str(ENGINE))

import compile_bound_product_page_blueprint as bp
from materialize_intrinsic_depth import materialize_uniform_depth, depth_obligations


def make_pages():
    cap = ["MATH-CAP-TEST"]
    model = bp.block("C1A-MODEL", "CASE_ANALYSIS", "DERIVED_MATHEMATICS", cap, [bp.node("PARAGRAPH", "The governed relation connects the quantities."), bp.node("STEP", "Preserve the relation before calculating.")])
    ex1 = bp.block("C1A-EX1", "WORKED_EXAMPLE", "DERIVED_MATHEMATICS", cap, [bp.node("QUESTION", "Example one?"), bp.node("STEP", "Use the governed relation."), bp.node("ANSWER", "Answer one")])
    ex2 = bp.block("C1A-EX2", "WORKED_EXAMPLE", "DERIVED_MATHEMATICS", cap, [bp.node("QUESTION", "Example two?"), bp.node("STEP", "Use the same relation in a changed case."), bp.node("ANSWER", "Answer two")])
    counter = bp.block("C1A-COUNTER", "COUNTEREXAMPLE", "DERIVED_MATHEMATICS", cap, [bp.node("PARAGRAPH", "This tempting route violates the governed condition.")])
    verify = bp.block("C1A-VERIFY", "VERIFICATION", "ANSWER_IDENTITY", cap, [bp.node("CHECK", "Substitute the result back into the condition.")])
    t1 = bp.ttu("TTU-C1A-1", cap, "Reconstruct example one.", "C1A-EX1", "C1A-VERIFY", fading="GUIDED")
    c1a = bp.page("C1A-P01", "CORE1A", "TEACHING", "Teach test capability", [model, ex1, ex2, counter, verify], [], [bp.representation("REP-C1A-1", cap, ["Show the governed relation."], ["Do not erase constraints."])], [t1])

    open_b = bp.block("C1B-OPEN", "OPEN_TASK", "INSTRUCTION", cap, [bp.node("QUESTION", "Reconstruct the relation.")], transform="RECONSTRUCT")
    work_b = bp.block("C1B-WORK", "TECHNICAL_WORKSPACE", "INSTRUCTION", cap, [bp.node("PARAGRAPH", "Write the first move.")], upstream="C1B-OPEN", transform="RECONSTRUCT")
    contrast_b = bp.block("C1B-COUNTER", "COUNTEREXAMPLE", "DERIVED_MATHEMATICS", cap, [bp.node("PARAGRAPH", "Diagnose the invalid route.")], upstream="C1B-OPEN", transform="CONTRAST")
    answer_b = bp.block("C1B-ANSWER", "ANSWER_DERIVATION", "DERIVED_MATHEMATICS", cap, [bp.node("ANSWER", "Canonical completion")], upstream="C1B-OPEN", transform="VERIFY")
    verify_b = bp.block("C1B-VERIFY", "VERIFICATION", "ANSWER_IDENTITY", cap, [bp.node("CHECK", "Check against the original condition.")], upstream="C1B-ANSWER", transform="VERIFY")
    tb = bp.ttu("TTU-C1B-1", cap, "Reconstruct before reveal.", "C1B-ANSWER", "C1B-VERIFY", source="TTU-C1A-1", transform="RECONSTRUCT", fading="FADED")
    c1b = bp.page("C1B-P01", "CORE1B", "OPEN_TUTOR", "Reconstruct test capability", [open_b, work_b, contrast_b, answer_b, verify_b], [], [bp.representation("REP-C1B-1", cap, ["Rebuild the relation."], ["Do not reveal the answer first."])], [tb], [{"workspace_id": "WS-C1B-1", "purpose": "RECONSTRUCTION", "math_refs": cap}])
    return [c1a, c1b]


def make_book():
    return {
        "buckets": [
            {
                "capability_units": [
                    {
                        "capability_ref": "MATH-CAP-TEST",
                        "lesson_id": "LESSON-TEST",
                        "practice": {
                            "TRANSFER": {
                                "prompt": "Transfer the governed relation to a changed case.",
                                "hints": ["Find the invariant.", "State the relation.", "Verify the result."],
                                "answer": "A valid transfer preserves the governed relation.",
                                "governed_example_asset_ref": "GEX-MATH-TEST",
                            }
                        },
                    }
                ]
            }
        ]
    }


class IntrinsicDepthMaterializerTests(unittest.TestCase):
    def test_medium_materializes_derivation_and_symbol_bridge(self):
        pages = materialize_uniform_depth(make_pages(), "MEDIUM", make_book())
        c1a = pages[0]
        self.assertTrue(any(x["kind"] == "DERIVATION" for x in c1a["technical_blocks"]))
        self.assertTrue(any("SYMBOL-BRIDGE" in x["representation_id"] for x in c1a["representations"]))
        rows = depth_obligations("MEDIUM", pages)
        self.assertTrue(all(x["disposition"] == "SATISFIED" for x in rows if x["stage"] in {"CORE1A", "CORE1B"}))

    def test_hard_materializes_multiple_representations_ttus_and_transfer(self):
        pages = materialize_uniform_depth(make_pages(), "HARD", make_book())
        c1a, c1b = pages
        self.assertGreaterEqual(len(c1a["representations"]), 3)
        self.assertGreaterEqual(len(c1b["representations"]), 2)
        self.assertGreaterEqual(len(c1a["reconstructable_ttus"]), 2)
        self.assertGreaterEqual(len(c1b["reconstructable_ttus"]), 2)
        self.assertTrue(any(x["block_id"].endswith("-TRANSFER-BRIDGE") for x in c1a["technical_blocks"]))
        rows = depth_obligations("HARD", pages)
        required = [x for x in rows if x["obligation_id"] not in {"INVERSE_USE", "ALTERNATIVE_METHOD"}]
        self.assertTrue(all(x["disposition"] == "SATISFIED" for x in required))


if __name__ == "__main__":
    unittest.main()
