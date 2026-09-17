import sys
import unittest
from pathlib import Path

ENGINE = Path(__file__).resolve().parents[1] / "engine"
if str(ENGINE) not in sys.path:
    sys.path.insert(0, str(ENGINE))

import compile_bound_product_page_blueprint as bp
from materialize_intrinsic_depth import materialize_uniform_depth, depth_obligations
from validate_content_complete_page_blueprint import validate_content_complete_blueprint

CAP = ["MATH-CAP-DEPTH"]


def core1_pages():
    model = bp.block("A-MODEL", "CASE_ANALYSIS", "DERIVED_MATHEMATICS", CAP, [bp.node("PARAGRAPH", "A governed model connects the known quantities."), bp.node("STEP", "Preserve the relation before calculation.")])
    ex1 = bp.block("A-EX1", "WORKED_EXAMPLE", "DERIVED_MATHEMATICS", CAP, [bp.node("QUESTION", "Use the model in case one."), bp.node("STEP", "Apply the governed relation."), bp.node("ANSWER", "Case one complete")])
    ex2 = bp.block("A-EX2", "WORKED_EXAMPLE", "DERIVED_MATHEMATICS", CAP, [bp.node("QUESTION", "Use the model in case two."), bp.node("STEP", "Apply the relation after the controlled change."), bp.node("ANSWER", "Case two complete")])
    counter = bp.block("A-COUNTER", "COUNTEREXAMPLE", "DERIVED_MATHEMATICS", CAP, [bp.node("PARAGRAPH", "This route fails because it drops a governed condition.")])
    verify = bp.block("A-VERIFY", "VERIFICATION", "ANSWER_IDENTITY", CAP, [bp.node("CHECK", "Check the result against the original relation.")])
    a_ttu = bp.ttu("TTU-A-1", CAP, "Reconstruct case one.", "A-EX1", "A-VERIFY", fading="GUIDED")
    a = bp.page("C1A-P01", "CORE1A", "TEACHING", "Build the governed concept.", [model, ex1, ex2, counter, verify], [], [bp.representation("REP-A-1", CAP, ["Expose the relation."], ["Do not erase constraints."])], [a_ttu])

    open_b = bp.block("B-OPEN", "OPEN_TASK", "INSTRUCTION", CAP, [bp.node("QUESTION", "Reconstruct the governed model before checking.")], transform="RECONSTRUCT")
    work_b = bp.block("B-WORK", "TECHNICAL_WORKSPACE", "INSTRUCTION", CAP, [bp.node("PARAGRAPH", "Write the first relation and explain why it applies.")], upstream="B-OPEN", transform="RECONSTRUCT")
    counter_b = bp.block("B-COUNTER", "COUNTEREXAMPLE", "DERIVED_MATHEMATICS", CAP, [bp.node("PARAGRAPH", "Diagnose the route that drops the condition.")], upstream="B-OPEN", transform="CONTRAST")
    answer_b = bp.block("B-ANSWER", "ANSWER_DERIVATION", "DERIVED_MATHEMATICS", CAP, [bp.node("ANSWER", "The canonical reconstruction preserves the condition.")], upstream="B-OPEN", transform="VERIFY")
    verify_b = bp.block("B-VERIFY", "VERIFICATION", "ANSWER_IDENTITY", CAP, [bp.node("CHECK", "Check the reconstructed relation against the model.")], upstream="B-ANSWER", transform="VERIFY")
    b_ttu = bp.ttu("TTU-B-1", CAP, "Reconstruct before reveal.", "B-ANSWER", "B-VERIFY", source="TTU-A-1", transform="RECONSTRUCT", fading="FADED")
    b = bp.page("C1B-P01", "CORE1B", "OPEN_TUTOR", "Reconstruct the governed concept.", [open_b, work_b, counter_b, answer_b, verify_b], [], [bp.representation("REP-B-1", CAP, ["Rebuild the relation."], ["Do not reveal completion first."])], [b_ttu], [{"workspace_id": "WS-B-1", "purpose": "RECONSTRUCTION", "math_refs": CAP}])
    return [a, b]


def core2_pages():
    problem = bp.block("C2A-PROBLEM", "PROBLEM", "IMMUTABLE_SOURCE", CAP, [bp.node("QUESTION", "Solve the governed source problem."), bp.node("SOURCE", "Source Q1")])
    solve = bp.block("C2A-SOLVE", "SOLUTION_CHAIN", "DERIVED_MATHEMATICS", CAP, [bp.node("STEP", "Use the governed model and preserve its condition.")], upstream="C2A-PROBLEM", transform="SOLUTION_ANATOMY")
    why = bp.block("C2A-WHY", "WHY_MOVE_WORKS", "EXPLANATION", CAP, [bp.node("PARAGRAPH", "The move is valid because it preserves the governing relation.")], upstream="C2A-SOLVE", transform="SOLUTION_ANATOMY")
    wrong = bp.block("C2A-WRONG", "WRONG_CHAIN", "DERIVED_MATHEMATICS", CAP, [bp.node("PARAGRAPH", "Dropping the condition changes the problem.")], upstream="C2A-PROBLEM", transform="CONTRAST")
    verify = bp.block("C2A-VERIFY", "VERIFICATION", "ANSWER_IDENTITY", CAP, [bp.node("CHECK", "Check against the source conditions.")], upstream="C2A-SOLVE", transform="VERIFY")
    ta = bp.ttu("TTU-C2A-1", CAP, "Reconstruct the expert route.", "C2A-SOLVE", "C2A-VERIFY", fading="GUIDED")
    a = bp.page("C2A-P01", "CORE2A", "SOLUTION_APPRENTICESHIP", "Study expert solution anatomy.", [problem, solve, why, wrong, verify], [], [bp.representation("REP-C2A-1", CAP, ["Expose the first move."], ["Do not reveal the final answer."])], [ta])

    p2 = bp.block("C2B-PROBLEM", "PROBLEM", "DERIVED_MATHEMATICS", CAP, [bp.node("QUESTION", "Solve a structural sibling without a named method.")], upstream="C2A-PROBLEM", transform="TRANSFER")
    classify = bp.block("C2B-CLASSIFY", "TRANSFER_CLASSIFICATION", "INSTRUCTION", CAP, [bp.node("PARAGRAPH", "Identify the invariant before choosing a method.")], upstream="C2A-PROBLEM", transform="TRANSFER")
    work = bp.block("C2B-WORK", "TECHNICAL_WORKSPACE", "INSTRUCTION", CAP, [bp.node("HINT", "Represent the condition before calculating.")], upstream="C2B-PROBLEM", transform="RECONSTRUCT")
    ans = bp.block("C2B-ANSWER", "ANSWER_DERIVATION", "DERIVED_MATHEMATICS", CAP, [bp.node("ANSWER", "A correct route preserves the same invariant.")], upstream="C2B-PROBLEM", transform="VERIFY")
    ver = bp.block("C2B-VERIFY", "VERIFICATION", "ANSWER_IDENTITY", CAP, [bp.node("CHECK", "Verify independently against the changed conditions.")], upstream="C2B-ANSWER", transform="VERIFY")
    tb = bp.ttu("TTU-C2B-1", CAP, "Select and reconstruct before using help.", "C2B-ANSWER", "C2B-VERIFY", source="TTU-C2A-1", transform="TRANSFER", fading="FADED")
    b = bp.page("C2B-P01", "CORE2B", "TRANSFER_TUTOR", "Transfer the governed structure.", [p2, classify, work, ans, ver], [], [bp.representation("REP-C2B-1", CAP, ["Expose the changed structure."], ["Do not name the hidden family first."])], [tb], [{"workspace_id": "WS-C2B-1", "purpose": "RECONSTRUCTION", "math_refs": CAP}])
    return [a, b]


def book():
    return {"buckets": [{"capability_units": [{"capability_ref": CAP[0], "lesson_id": "LESSON-DEPTH", "practice": {"TRANSFER": {"prompt": "Transfer the relation to a changed case.", "hints": ["Find the invariant.", "State the relation.", "Check the changed condition."], "answer": "Preserve the governed invariant.", "governed_example_asset_ref": "GEX-MATH-DEPTH"}}}]}]}


class IntrinsicDepthFullBlueprintTests(unittest.TestCase):
    def _validate(self, badge):
        pages = materialize_uniform_depth(core1_pages(), badge, book()) + core2_pages()
        doc = {
            "schema_version": "1.0.0",
            "subject": "MATHEMATICS",
            "blueprint_id": "MATH-PAGE-BP-DEPTH-" + badge,
            "difficulty_badge": badge,
            "pages": pages,
            "depth_obligations": depth_obligations(badge, pages),
        }
        audit = validate_content_complete_blueprint(doc)
        self.assertEqual(audit["status"], "PASS")
        return doc

    def test_medium_full_blueprint_passes(self):
        doc = self._validate("MEDIUM")
        self.assertTrue(any(b["kind"] == "DERIVATION" for p in doc["pages"] if p["stage"] == "CORE1A" for b in p["technical_blocks"]))

    def test_hard_full_blueprint_passes(self):
        doc = self._validate("HARD")
        self.assertGreaterEqual(sum(len(p["reconstructable_ttus"]) for p in doc["pages"] if p["stage"] == "CORE1A"), 2)
        self.assertGreaterEqual(sum(len(p["reconstructable_ttus"]) for p in doc["pages"] if p["stage"] == "CORE1B"), 2)


if __name__ == "__main__":
    unittest.main()
