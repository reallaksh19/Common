from __future__ import annotations
import importlib.util, json, sys, unittest
from pathlib import Path

HERE=Path(__file__).resolve().parent
ENGINE_DIR=HERE.parent/'engine'
sys.path.insert(0,str(ENGINE_DIR))
SPEC=importlib.util.spec_from_file_location('build_v7_products',ENGINE_DIR/'build_v7_products.py')
b=importlib.util.module_from_spec(SPEC); assert SPEC.loader; SPEC.loader.exec_module(b)
import assure

class AssuredProductTests(unittest.TestCase):
    def models(self):
        return b.build_page_models(b.AUTH)

    def test_four_product_models_exist_and_are_distinct(self):
        m=self.models()
        self.assertEqual(set(m),{'CORE1A','CORE1B','CORE2A','CORE2B'})
        self.assertNotEqual([p['title'] for p in m['CORE1A']],[p['title'] for p in m['CORE1B']])
        self.assertNotEqual([p['title'] for p in m['CORE2A']],[p['title'] for p in m['CORE2B']])

    def test_actual_nonfrozen_prose_is_within_v7_threshold(self):
        packet=assure.similarity_packet(self.models())
        b.v7.validate_similarity(packet,b.POLICY)
        self.assertLessEqual(packet['non_frozen_prose']['verbatim_5gram_overlap'],0.10)
        self.assertLessEqual(packet['non_frozen_prose']['max_identical_contiguous_words'],35)

    def test_source_hashes_are_recomputed_from_exact_stems(self):
        assure.validate_source_hashes(b.QUESTIONS)

    def test_every_source_question_closes_answer_and_source(self):
        for q in b.QUESTIONS.values():
            r=b.v7.validate_question_custody(assure.question_custody(q),b.POLICY)
            self.assertTrue(r['source_visible']); self.assertTrue(r['answer_closed'])

    def test_core1_uses_intrinsic_difficulty_only(self):
        for mode in ('CORE1A','CORE1B'):
            p=assure.difficulty_packet(mode,b.AUTH)
            self.assertNotIn('knowledge_percent',json.dumps(p))
            r=b.v7.validate_difficulty(p,b.POLICY)
            self.assertEqual(r['derived_badge'],'MEDIUM')

    def test_core2_owner_override_does_not_fabricate_knowledge_percent(self):
        for mode in ('CORE2A','CORE2B'):
            p=assure.learner_fit(mode,'CHEM-C2A-SRC-U2Q35',9,'GUIDED')
            self.assertIsNone(p['conditioning']['knowledge_percent'])
            self.assertEqual(b.v7.validate_learner_fit(p,b.POLICY)['validator_support'],'GUIDED')

    def test_purpose_contracts_close(self):
        for mode in ('CORE1A','CORE1B','CORE2A','CORE2B'):
            self.assertEqual(b.v7.validate_purpose(assure.purpose_packet(mode),b.POLICY)['status'],'PASS')

    def test_badge_policy_closes_without_knowledge_exposure(self):
        for mode in ('CORE1A','CORE1B','CORE2A','CORE2B'):
            p=assure.badge_packet(mode)
            self.assertFalse(p['student_knowledge_percent_visible'])
            self.assertEqual(b.v7.validate_badges(p,b.POLICY)['status'],'PASS')

    def test_ccbom_is_closed(self):
        r=b.v7.validate_ccbom(b.CCBOM,b.POLICY)
        self.assertEqual(r['coverage_ratio'],1.0)

    def test_frozen_questions_are_not_treated_as_generated_examples(self):
        packet=assure.similarity_packet(self.models())
        self.assertEqual(packet['generated_example_comparisons'],[])
        self.assertEqual(len(packet['ab_comparisons']),2)

    def test_core1b_and_core2b_are_attempt_or_reconstruct_first(self):
        m=self.models()
        self.assertTrue(all(p['workspace'] for p in m['CORE1B']))
        self.assertTrue(all(p['workspace'] for p in m['CORE2B']))
        first1=[b['kind'] for b in m['CORE1B'][0]['blocks']]
        first2=[b['kind'] for b in m['CORE2B'][0]['blocks']]
        self.assertIn('PROMPT',first1); self.assertIn('TTU',first1)
        self.assertIn('PROMPT',first2); self.assertIn('TTU',first2)

if __name__=='__main__': unittest.main()
