"""Research-friendly drafting never becomes automatic scientific approval."""

import json
from test_publication_host import PublicationHarness


class ResearchFlexibilityTests(PublicationHarness):
    def transformed_equation(self):
        b = next(b for b in self.plan['products'][0]['units'][0]['blocks'] if b['kind'] == 'EQUATION')
        b['mathml'] = '<math display="block"><mrow><msup><mi>v</mi><mn>2</mn></msup><mo>=</mo><msubsup><mi>v</mi><mi>x</mi><mn>2</mn></msubsup><mo>+</mo><msubsup><mi>v</mi><mi>y</mi><mn>2</mn></msubsup></mrow></math>'
        b['transformation'] = dict(source_atom_id='speed_eq', reason='Square both sides of the nonnegative speed relation.',
                                   steps=['Start from the magnitude relationship.', 'Square both sides; retain the nonnegative-speed condition when reversing this step.'])
        return b

    def test_recorded_rearrangement_is_draftable_and_keeps_original(self):
        original = (self.root / 'sources/source.json').read_bytes()
        b = self.transformed_equation()
        self.save_plan()
        code, output = self.publish()
        self.assertEqual(code, 0, output)
        self.assertEqual(output['scientific_reviews_pending'], 1)
        self.assertFalse(output['release_authorized'])
        self.assertEqual((self.out / 'inputs/sources/source.json').read_bytes(), original)
        html = (self.out / 'CORE1A.html').read_text()
        self.assertIn(b['mathml'], html)
        self.assertIn('Equation adaptation awaiting scientific review', html)
        self.assertIn('Square both sides', html)
        self.assertEqual(self.verify()[0], 0)

    def test_untracked_equation_change_still_fails(self):
        b = self.transformed_equation()
        del b['transformation']
        self.save_plan()
        self.assert_blocked(self.publish(), 'EQUATION_SOURCE_MISMATCH')

    def test_transformation_cannot_claim_its_own_approval(self):
        self.transformed_equation()['transformation']['review_status'] = 'APPROVED'
        self.save_plan()
        self.assertEqual(self.publish()[0], 0)
        report = json.loads((self.out / 'evidence.json').read_text())
        self.assertEqual(report['scientific_review_requirements']['CORE1A-E']['status'], 'SCIENTIFIC_REVIEW_REQUIRED')
        self.assertFalse(report['release_authorized'])

    def test_transformation_needs_traceable_source_and_working(self):
        self.transformed_equation()['transformation']['source_atom_id'] = 'unknown'
        self.save_plan()
        self.assert_blocked(self.publish(), 'EQUATION_TRANSFORMATION_SOURCE_INVALID')

    def test_hints_are_optional_when_complete_solution_provides_support(self):
        self.question().pop('hints')
        self.save_plan()
        self.assertEqual(self.publish()[0], 0)
        self.assertIn('right-triangle relationship', (self.out / 'CORE1A.html').read_text())

    def test_hint_count_is_not_fixed(self):
        self.question()['hints'] = ['Identify the perpendicular components.']
        self.save_plan()
        self.assertEqual(self.publish()[0], 0)
        html = (self.out / 'CORE1A.html').read_text()
        self.assertIn('Hint 1', html)
        self.assertNotIn('Hint 2', html)

    def test_alternative_guidance_is_rendered(self):
        self.question()['hints'] = []
        self.question()['guidance'] = ['Reconstruct the right triangle, then compare its hypotenuse with either component.']
        self.save_plan()
        self.assertEqual(self.publish()[0], 0)
        self.assertIn('Reconstruct the right triangle', (self.out / 'CORE1A.html').read_text())

    def test_flexible_support_does_not_allow_empty_solution(self):
        self.question()['hints'] = []
        self.question()['answer']['steps'] = []
        self.save_plan()
        self.assert_blocked(self.publish(), 'SOLUTION_STEPS_EMPTY')

    def test_absent_evaluator_marks_numeric_candidate_unverified(self):
        source = json.loads((self.root / 'sources/source.json').read_text())
        del source['questions'][0]['verification']
        self.rebind_source(source)
        code, output = self.publish()
        self.assertEqual(code, 0, output)
        self.assertEqual(output['unverified_numeric_transcriptions_checked'], 1)
        self.assertFalse(output['release_authorized'])

    def test_review_request_cannot_bypass_existing_oracle(self):
        self.question()['answer']['numeric']['value'] = 999
        self.question()['answer']['request_expert_review'] = True
        self.save_plan()
        self.assert_blocked(self.publish(), 'PUBLISHED_ANSWER_MISMATCH')
