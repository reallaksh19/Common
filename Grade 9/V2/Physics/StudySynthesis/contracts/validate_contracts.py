#!/usr/bin/env python3
import json, importlib.util, sys
from pathlib import Path
from jsonschema import Draft202012Validator
ROOT=Path(__file__).resolve().parents[1]
for p in sorted((ROOT/'contracts').glob('*.schema.json')): Draft202012Validator.check_schema(json.loads(p.read_text()))
PHYS=ROOT.parent; LI=PHYS/'LearnerIntelligence'
spec=importlib.util.spec_from_file_location('li',LI/'engine/derive_physics_state.py'); li=importlib.util.module_from_spec(spec); spec.loader.exec_module(li)
state=li.derive(li.load(LI/'fixtures/evidence.synthetic.json'),li.load(LI/'fixtures/inference_policy.synthetic.json'),li.load(LI/'fixtures/learner_intelligence_interface.synthetic.json'))
sys.path.insert(0,str(ROOT/'engine')); from synthesize_physics_study_model import synthesize, load
r=synthesize(load(ROOT/'fixtures/goal_scope.synthetic.json'),load(ROOT/'fixtures/canonical_knowledge_set.synthetic.json'),state,load(ROOT/'fixtures/study_policy.synthetic.json'))
assert r['status']=='PASS'; print('PHY-V2-03 contracts + reference StudyModel = PASS')
