#!/usr/bin/env python3
import copy, sys, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'engine'))
from build_canonical_package import load_inputs, validate_inputs, write_package
base=load_inputs(); validate_inputs(copy.deepcopy(base))
def must_fail(mutator):
    d=copy.deepcopy(base); mutator(d)
    try: validate_inputs(d)
    except Exception: return
    raise AssertionError('falsifier accepted')
# 1 projectile strength cannot be erased
must_fail(lambda d:d['acceptance_cases']['acceptance_cases'][0].__setitem__('preserved_capability_refs',['PHY-REFERENCE-FRAME']))
# 2 state propagation cannot be relabeled model selection
must_fail(lambda d:d['acceptance_cases']['acceptance_cases'][0]['localized_outcome'].__setitem__('ref','PHY-MODEL-SELECTION'))
# 3 handoff checkpoint cannot disappear
must_fail(lambda d:d['reasoning_contracts']['reasoning_contracts'][0]['checkpoints'].pop(5))
# 4 arithmetic failure cannot become Physics model failure
must_fail(lambda d:d['acceptance_cases']['acceptance_cases'][4].__setitem__('localized_outcome',{'kind':'PHYSICS_CAPABILITY','ref':'PHY-MODEL-SELECTION','checkpoint_ref':'PHY-SP-03'}))
# 5 apex ambiguity cannot lose its probe
must_fail(lambda d:d['acceptance_cases']['acceptance_cases'][3].__setitem__('required_probe_refs',[]))
# 6 signed displacement ambiguity cannot lose its probe
must_fail(lambda d:d['acceptance_cases']['acceptance_cases'][2].__setitem__('required_probe_refs',[]))
# 7 physical sign capability cannot be replaced by shared arithmetic
must_fail(lambda d:d['acceptance_cases']['acceptance_cases'][2]['localized_outcome'].__setitem__('ref','SHARED-ARITHMETIC-EXECUTION'))
# 8 shared arithmetic cannot be duplicated as Physics capability
must_fail(lambda d:d['capabilities']['capabilities'].append({'capability_id':'SHARED-ARITHMETIC-EXECUTION','authority':'PHYSICS_CANONICAL','name':'bad','description':'bad','reasoning_family':'bad','external_dependencies':[]}))
# 9 error signature unknown checkpoint
must_fail(lambda d:d['error_signatures']['error_signatures'][0]['checkpoint_refs'].append('PHY-NOT-A-CHECKPOINT'))
# 10 probe unknown target
must_fail(lambda d:d['diagnostic_probes']['diagnostic_probes'][0].__setitem__('target_capability_ref','PHY-NOT-REAL'))
# 11 state reasoning cannot skip system/frame-state spine via non-contiguous ordinals
must_fail(lambda d:d['reasoning_contracts']['reasoning_contracts'][0]['checkpoints'][0].__setitem__('ordinal',2))
# 12 verification/plausibility must close state propagation
must_fail(lambda d:d['reasoning_contracts']['reasoning_contracts'][0]['checkpoints'][-1].__setitem__('capability_ref','PHY-MODEL-SELECTION'))
# 13 broad KINEMATICS=WEAK must remain forbidden
must_fail(lambda d:d['acceptance_cases']['acceptance_cases'][0].__setitem__('forbidden_broad_conclusions',['PROJECTILE_MOTION=WEAK']))
# 14 benchmark producer contamination
must_fail(lambda d:d['shared_dependencies']['dependencies'][0].__setitem__('description','Use PR #156 reference'))
# 15 non-synthetic learner fixture
must_fail(lambda d:d['acceptance_cases'].__setitem__('fixture_class','REAL_LEARNER'))
# 16 duplicate capability destabilizer
must_fail(lambda d:d['capabilities']['capabilities'].append(copy.deepcopy(d['capabilities']['capabilities'][0])))
# 17 discontinuity exception/handoff invariant cannot be lost
must_fail(lambda d:d['reasoning_contracts']['reasoning_contracts'][0]['invariants'][0].__setitem__('terminal_to_next_initial',False))
with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
    write_package(a,copy.deepcopy(base)); write_package(b,copy.deepcopy(base))
    assert (Path(a)/'canonical_package.json').read_bytes()==(Path(b)/'canonical_package.json').read_bytes()
    assert (Path(a)/'canonical_package_manifest.json').read_bytes()==(Path(b)/'canonical_package_manifest.json').read_bytes()
print('PHY-V2-01 canonical falsifiers = 17 PASS')
