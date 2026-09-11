#!/usr/bin/env python3
import json, sys
from pathlib import Path
from jsonschema import Draft202012Validator
ROOT=Path(__file__).resolve().parents[1]
for p in sorted((ROOT/'contracts').glob('*.schema.json')):
    Draft202012Validator.check_schema(json.loads(p.read_text()))
sys.path.insert(0,str(ROOT/'engine'))
from derive_physics_state import derive, load
r=derive(load(ROOT/'fixtures/evidence.synthetic.json'),load(ROOT/'fixtures/inference_policy.synthetic.json'),load(ROOT/'fixtures/learner_intelligence_interface.synthetic.json'))
assert r['fixture_class']=='PUBLIC_SYNTHETIC'
by={x['capability_ref']:x for x in r['capability_states']}
assert by['PHY-MOTION-PROPAGATE-STATE']['state']=='REPAIR_REQUIRED'
assert by['PHY-PROJECTILE-COMPONENT-DECOMPOSITION']['state']=='READY'
assert by['PHY-MODEL-SELECTION']['state']=='READY'
assert by['PHY-SIGNED-DISPLACEMENT-INTERPRETATION']['probe_refs']==['PHY-PROBE-SIGNED-DISPLACEMENT']
assert 'PHY-PROBE-APEX-COMPONENTS' in by['PHY-PROJECTILE-COMPONENT-DECOMPOSITION']['probe_refs']
print('PHY-V2-02 learner-intelligence contracts + reference state = PASS')
