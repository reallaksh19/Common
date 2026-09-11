#!/usr/bin/env python3
import copy, json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'engine'))
from derive_physics_state import derive, load, canonical_maps, sha_obj

e=load(ROOT/'fixtures/evidence.synthetic.json'); p=load(ROOT/'fixtures/inference_policy.synthetic.json'); i=load(ROOT/'fixtures/learner_intelligence_interface.synthetic.json')
base=derive(copy.deepcopy(e),copy.deepcopy(p),copy.deepcopy(i)); by={x['capability_ref']:x for x in base['capability_states']}
assert by['PHY-PROJECTILE-COMPONENT-DECOMPOSITION']['state']=='READY'
assert by['PHY-MODEL-SELECTION']['state']=='READY'
assert by['PHY-MOTION-PROPAGATE-STATE']['state']=='REPAIR_REQUIRED'
one=copy.deepcopy(e); one['attempts']=[a for a in one['attempts'] if a['attempt_id']!='PHY-ATT-MULTIPHASE-02']
r=derive(one,p,i); b={x['capability_ref']:x for x in r['capability_states']}; assert b['PHY-MOTION-PROPAGATE-STATE']['state']=='DEVELOPING'
assert any(x['target_ref']=='PHY-MOTION-PROPAGATE-STATE' and x['status']=='CORROBORATED' and not x['broad_topic_conclusion'] for x in base['diagnostic_cases'])
assert by['PHY-SIGNED-DISPLACEMENT-INTERPRETATION']['misconception_status']=='AMBIGUOUS'
assert by['PHY-PROJECTILE-COMPONENT-DECOMPOSITION']['misconception_status']=='AMBIGUOUS'
assert by['PHY-SIGNED-DISPLACEMENT-INTERPRETATION']['probe_refs']==['PHY-PROBE-SIGNED-DISPLACEMENT']
assert 'PHY-PROBE-APEX-COMPONENTS' in by['PHY-PROJECTILE-COMPONENT-DECOMPOSITION']['probe_refs']
assert by['PHY-MODEL-SELECTION']['state']=='READY'
assert base['external_dependency_observations'][0]['dependency_ref']=='SHARED-ARITHMETIC-EXECUTION' and base['external_dependency_observations'][0]['status']=='INVALID'
before=sha_obj(canonical_maps()[-1]); derive(copy.deepcopy(e),copy.deepcopy(p),copy.deepcopy(i)); assert sha_obj(canonical_maps()[-1])==before
bad=copy.deepcopy(e); bad['attempts'][0]['checkpoint_observations'][0]['checkpoint_ref']='PHY-NOT-REAL'
try: derive(bad,p,i); raise AssertionError('unknown checkpoint accepted')
except Exception: pass
badp=copy.deepcopy(p); badp['ambiguity_probe_map']['PHY-SIGNED-DISPLACEMENT-INTERPRETATION']='PHY-PROBE-NOT-REAL'
try: derive(e,badp,i); raise AssertionError('unknown probe accepted')
except ValueError: pass
assert 'KINEMATICS' not in json.dumps(base['capability_states']) and 'PHYSICS=WEAK' not in json.dumps(base['capability_states'])
bad=copy.deepcopy(e); bad['unsupported_inference']='attention cause'
try: derive(bad,p,i); raise AssertionError('psychological inference accepted')
except Exception: pass
badp=copy.deepcopy(p); badp['benchmark_inputs']=['PR #156']
try: derive(e,badp,i); raise AssertionError('benchmark input accepted')
except Exception: pass
bad=copy.deepcopy(e); bad['fixture_class']='REAL_LEARNER'
try: derive(bad,p,i); raise AssertionError('real learner accepted')
except Exception: pass
r2=derive(copy.deepcopy(e),copy.deepcopy(p),copy.deepcopy(i)); assert json.dumps(base,sort_keys=True)==json.dumps(r2,sort_keys=True)
rev=copy.deepcopy(e); rev['attempts']=list(reversed(rev['attempts'])); r3=derive(rev,p,i); assert r3['semantic_digest']==base['semantic_digest']
print('PHY-V2-02 learner-state falsifiers = 17 PASS')
