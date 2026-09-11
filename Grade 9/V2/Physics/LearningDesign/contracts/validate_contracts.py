#!/usr/bin/env python3
import json, importlib.util, sys
from pathlib import Path
from jsonschema import Draft202012Validator
ROOT=Path(__file__).resolve().parents[1]; PHYS=ROOT.parent
for p in sorted((ROOT/'contracts').glob('*.schema.json')): Draft202012Validator.check_schema(json.loads(p.read_text()))
LI=PHYS/'LearnerIntelligence'; SS=PHYS/'StudySynthesis'
spec=importlib.util.spec_from_file_location('li',LI/'engine/derive_physics_state.py'); li=importlib.util.module_from_spec(spec); spec.loader.exec_module(li)
state=li.derive(li.load(LI/'fixtures/evidence.synthetic.json'),li.load(LI/'fixtures/inference_policy.synthetic.json'),li.load(LI/'fixtures/learner_intelligence_interface.synthetic.json'))
sys.path.insert(0,str(SS/'engine')); import synthesize_physics_study_model as ss
study=ss.synthesize(ss.load(SS/'fixtures/goal_scope.synthetic.json'),ss.load(SS/'fixtures/canonical_knowledge_set.synthetic.json'),state,ss.load(SS/'fixtures/study_policy.synthetic.json'))
sys.path.insert(0,str(ROOT/'engine')); from design_physics_learning import design,load
plan=design(study,load(ROOT/'fixtures/design_policy.synthetic.json'))
assert plan['blocks'] and plan['obligation_coverage']; print('PHY-V2-04 contracts + reference design = PASS')
