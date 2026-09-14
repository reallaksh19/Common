#!/usr/bin/env python3
import importlib.util
import json
import unittest
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'common'/'engine'))

def load_module(name,path):
    spec=importlib.util.spec_from_file_location(name,path); mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod

prim=load_module('production_primitives',ROOT/'common'/'engine'/'production_primitives.py')
c2a=load_module('run_core2a_kit',ROOT/'Core2A'/'engine'/'run_core2a_kit.py')

def load(path): return json.loads(Path(path).read_text(encoding='utf-8'))

class ProductionKitTests(unittest.TestCase):
    def test_four_stage_kits_exist(self):
        expected={'Core1':'CORE1','Core1A':'CORE1A','Core2':'CORE2','Core2A':'CORE2A'}
        for folder,stage in expected.items():
            manifest=load(ROOT/folder/'KIT_MANIFEST.json')
            self.assertEqual(manifest['stage'],stage)
            self.assertTrue((ROOT/folder/'engine'/('run_'+folder.lower()+'_kit.py')).exists())

    def test_core2a_missing_purpose_requires_user_question(self):
        routed=prim.route_task({'requested_stage':'CORE2A','purpose':None,'scope':{'scope_type':'TOPIC','scope_ref':'x'}})
        self.assertEqual(routed['status'],'NEEDS_USER_INPUT')
        self.assertEqual(routed['code'],'CORE2A_USER_PURPOSE_REQUIRED')
        self.assertEqual(routed['question'],'Is this for Starter, Practice, Revision, or Competition?')

    def test_profiles_are_materially_different(self):
        profiles=prim.load_scaffold_profiles(ROOT/'common'/'profiles'/'scaffold-profiles.json')
        self.assertEqual(set(profiles),set(prim.PURPOSES))
        self.assertNotEqual(profiles['STARTER']['settings']['concept_recap'],profiles['REVISION']['settings']['concept_recap'])
        self.assertNotEqual(profiles['PRACTICE']['settings']['source_question_policy'],profiles['REVISION']['settings']['source_question_policy'])
        self.assertEqual(profiles['COMPETITION']['settings']['question_mix']['mixed_synthesis'],0.20)
        self.assertEqual(profiles['STARTER']['settings']['question_mix']['competitive'],0.0)

    def test_core2a_knowledge_support_profiles_are_material(self):
        profiles=c2a.load_knowledge_support_profiles(ROOT/'common'/'profiles'/'knowledge-support-profiles.json')
        self.assertEqual(set(profiles),{'FOUNDATION_GUIDED','STANDARD_GUIDED','REDUCED_SUPPORT','ADVANCED_APPLIED'})
        base=prim.build_scaffold_plan('PRACTICE',prim.load_scaffold_profiles(ROOT/'common'/'profiles'/'scaffold-profiles.json'),'B1')
        foundation=c2a.apply_knowledge_support_profile(base,'FOUNDATION_GUIDED',profiles)
        advanced=c2a.apply_knowledge_support_profile(base,'ADVANCED_APPLIED',profiles)
        self.assertNotEqual(foundation['settings']['worked_example_density'],advanced['settings']['worked_example_density'])
        self.assertNotEqual(foundation['settings']['help_visibility'],advanced['settings']['help_visibility'])
        self.assertNotEqual(foundation['scaffold_plan_id'],advanced['scaffold_plan_id'])

    def test_core2a_candidate_demand_ceiling_is_operational(self):
        direct={'slot':'GUIDED_DIRECT'}; hidden={'slot':'HIDDEN_INFORMATION'}; synth={'slot':'MIXED_SYNTHESIS'}
        self.assertTrue(c2a.candidate_within_ceiling(direct,'M1_CONTROLLED_VARIATION'))
        self.assertFalse(c2a.candidate_within_ceiling(hidden,'M3_INVERSE_TARGET'))
        self.assertTrue(c2a.candidate_within_ceiling(hidden,'M4_HIDDEN_STRUCTURE'))
        self.assertFalse(c2a.candidate_within_ceiling(synth,'M6_FAMILY_DISCRIMINATION'))

    def test_benchmark_registry_never_becomes_curriculum_authority(self):
        reg=load(ROOT/'common'/'registry'/'benchmark-source-registry.json')
        self.assertGreaterEqual(len(reg['sources']),3)
        for source in reg['sources']:
            self.assertFalse(source['curriculum_authority'])
            self.assertEqual(source['role'],'COMPETITION_BENCHMARK')
            self.assertTrue(source['url'].startswith('https://'))

    def test_starter_golden(self):
        g=load(ROOT/'golden'/'01-starter-hidden-roots.json')
        pages={p['question_ref']:p for p in g['core2_plan']['pages']}; bucket=g['bucket_plan']['buckets'][0]
        selected=c2a.source_selection('STARTER',bucket,pages)
        self.assertEqual([p['question_ref'] for p in selected],g['expected']['selected_source_refs'])
        buckets={bucket['bucket_id']:bucket}; candidates=g['candidate_set']['items']
        for item in candidates: c2a.validate_candidate(item,'STARTER',buckets)
        c2a.check_candidate_coverage('STARTER',buckets,candidates)

    def test_practice_revision_golden_proves_purpose_difference(self):
        g=load(ROOT/'golden'/'02-practice-vs-revision.json'); bucket=g['bucket_plan']['buckets'][0]; pages={p['question_ref']:p for p in g['core2_plan']['pages']}
        practice=[p['question_ref'] for p in c2a.source_selection('PRACTICE',bucket,pages)]
        revision=[p['question_ref'] for p in c2a.source_selection('REVISION',bucket,pages)]
        self.assertEqual(practice,g['practice']['expected_source_refs']); self.assertEqual(revision,g['revision']['expected_source_refs']); self.assertNotEqual(practice,revision)
        profiles=prim.load_scaffold_profiles(ROOT/'common'/'profiles'/'scaffold-profiles.json')
        self.assertNotEqual(prim.build_scaffold_plan('PRACTICE',profiles,'B1')['profile_id'],prim.build_scaffold_plan('REVISION',profiles,'B1')['profile_id'])

    def test_competition_golden_requires_near_and_structural_each_bucket(self):
        g=load(ROOT/'golden'/'03-competition-theory-of-equations.json'); buckets={b['bucket_id']:b for b in g['bucket_plan']['buckets']}; candidates=g['candidate_set']['items']
        for item in candidates: c2a.validate_candidate(item,'COMPETITION',buckets)
        c2a.check_candidate_coverage('COMPETITION',buckets,candidates)
        self.assertGreaterEqual(len(candidates),g['expected']['minimum_generated'])
        with self.assertRaises(ValueError): prim.validate_provenance(candidates[0]['provenance'],'PRACTICE')

    def test_representation_builder_is_ordered_and_atom_complete(self):
        stages={}
        for i,name in enumerate(prim.REPRESENTATION_STAGES):
            stages[name]={'status':'REQUIRED','learner_job':name.replace('_',' ').title(),'content':f'Content for {name}','atom_refs':['A1'] if i==0 else []}
        plan=prim.build_learning_representation(bucket_ref='B1',purpose='STARTER',stage_inputs=stages,required_atom_refs=['A1'])
        prim.validate_learning_representation(plan,['A1'])
        self.assertEqual([x['stage'] for x in plan['stages']],list(prim.REPRESENTATION_STAGES))
        with self.assertRaises(ValueError): prim.build_learning_representation(bucket_ref='B1',purpose='STARTER',stage_inputs=stages,required_atom_refs=['A2'])

    def test_answer_contract_requires_independent_solver_and_check(self):
        a={'question_ref':'QX','answer_type':'EXACT_VALUE','canonical_answer':2,'accepted_equivalents':[],'solution_paths':[{'path_id':'A','steps':['Compute.']}],'verification_checks':[{'method':'SUBSTITUTE','status':'PASS','evidence':'works'}],'domain_conditions':[],'solution_multiplicity':'SINGLE_CANONICAL','independent_solver_status':'PASS'}
        prim.validate_answer_contract(a)
        bad=dict(a); bad['independent_solver_status']='PENDING'
        with self.assertRaises(ValueError): prim.validate_answer_contract(bad)

    def test_core2a_is_declarative_solution_apprenticeship(self):
        manifest=load(ROOT/'Core2A'/'KIT_MANIFEST.json')
        self.assertEqual(manifest['pedagogy_mode'],'DECLARATIVE')
        self.assertEqual(manifest['learner_role'],'SOLUTION_APPRENTICESHIP')
        self.assertTrue(manifest['source_question_freeze'])
        required={'STRUCTURAL_CUE','REPRESENTATION_CHOICE','FIRST_NON_OBVIOUS_MOVE','STEPWISE_SOLUTION','WHY_KEY_MOVES_WORK','COMMON_WRONG_CHAIN','VERIFICATION','NEARBY_VARIANT'}
        self.assertTrue(required.issubset(set(manifest['solution_apprenticeship_requirements'])))

    def test_core2a_self_teaching_contract_is_bound(self):
        manifest=load(ROOT/'Core2A'/'KIT_MANIFEST.json')
        path=ROOT.parents[0]/'MathBlueprint'/'SELF_TEACHING.md'
        self.assertTrue(path.exists())
        self.assertIn('MathBlueprint/SELF_TEACHING.md',manifest['self_teaching_contract'])

    def test_core2a_requires_generation_calibration(self):
        manifest=load(ROOT/'Core2A'/'KIT_MANIFEST.json')
        self.assertTrue(manifest['knowledge_gate']['required'])
        self.assertTrue(manifest['knowledge_gate']['waivable_by_owner'])
        self.assertTrue(manifest['knowledge_gate']['no_silent_default'])
        self.assertEqual(set(manifest['knowledge_gate']['resolved_controls']),{'CORE2A_SUPPORT_PROFILE','CORE2A_MAX_DEMAND_LEVEL','CORE2B_MAX_DEMAND_LEVEL'})

    def test_exactly_three_golden_fixtures(self):
        self.assertEqual(len(list((ROOT/'golden').glob('*.json'))),3)

if __name__=='__main__': unittest.main(verbosity=2)
