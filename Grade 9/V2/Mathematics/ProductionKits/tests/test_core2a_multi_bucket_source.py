#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'common' / 'engine'))

spec = importlib.util.spec_from_file_location('run_core2a_kit_multi', ROOT / 'Core2A' / 'engine' / 'run_core2a_kit.py')
c2a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c2a)


class Core2AMultiBucketSourceTests(unittest.TestCase):
    def test_source_question_may_belong_to_multiple_buckets(self):
        plan = {
            'buckets': [
                {'bucket_id': 'B1', 'member_capability_refs': ['CAP-A'], 'core2_question_refs': ['Q12']},
                {'bucket_id': 'B2', 'member_capability_refs': ['CAP-B'], 'core2_question_refs': ['Q12']},
            ]
        }
        buckets, qmap = c2a.bucket_maps(plan)
        self.assertEqual(set(buckets), {'B1', 'B2'})
        self.assertEqual(qmap['Q12'], ['B1', 'B2'])
        page = {'question_ref': 'Q12', 'capability_refs': ['CAP-A', 'CAP-B']}
        c2a.validate_source_question_scope(page, qmap['Q12'], buckets)

    def test_multi_bucket_selection_deduplicates_source_identity(self):
        pages = {'Q12': {'question_ref': 'Q12', 'source_order': 12}}
        selected = {'B1': ['Q12'], 'B2': ['Q12']}
        self.assertEqual(c2a.unique_selected_source_ids(selected, pages), ['Q12'])

    def test_multi_bucket_union_still_blocks_untaught_math(self):
        plan = {
            'buckets': [
                {'bucket_id': 'B1', 'member_capability_refs': ['CAP-A'], 'core2_question_refs': ['Q12']},
                {'bucket_id': 'B2', 'member_capability_refs': ['CAP-B'], 'core2_question_refs': ['Q12']},
            ]
        }
        buckets, qmap = c2a.bucket_maps(plan)
        page = {'question_ref': 'Q12', 'capability_refs': ['CAP-A', 'CAP-C']}
        with self.assertRaisesRegex(ValueError, 'CORE2A_SOURCE_UNTAUGHT_MATH_REQUIRED:Q12:CAP-C'):
            c2a.validate_source_question_scope(page, qmap['Q12'], buckets)


if __name__ == '__main__':
    unittest.main(verbosity=2)
