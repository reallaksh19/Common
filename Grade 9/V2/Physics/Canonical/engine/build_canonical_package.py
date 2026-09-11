#!/usr/bin/env python3
import argparse, copy, hashlib, json
from pathlib import Path
from jsonschema import Draft202012Validator
ROOT=Path(__file__).resolve().parents[1]
CONTRACTS=ROOT/'contracts'
FORBIDDEN_PRODUCER_TOKENS=('PR #156','PR156','benchmark_reference','benchmark_template','benchmark_page','mature_reference')
def load(p): return json.loads(Path(p).read_text())
def canonical(o): return json.dumps(o,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def sha_obj(o): return hashlib.sha256(canonical(o)).hexdigest()
def validate_schema(obj,name): Draft202012Validator(load(CONTRACTS/name)).validate(obj)
def load_inputs(root=ROOT):
    return {'capabilities':load(root/'registry/capabilities.json'),'shared_dependencies':load(root/'registry/shared_dependencies.json'),'reasoning_contracts':load(root/'registry/reasoning_contracts.json'),'error_signatures':load(root/'registry/error_signatures.json'),'diagnostic_probes':load(root/'registry/diagnostic_probes.json'),'acceptance_cases':load(root/'fixtures/acceptance_cases.synthetic.json')}
def validate_inputs(data):
    caps=data['capabilities']['capabilities']; contracts=data['reasoning_contracts']['reasoning_contracts']; errors=data['error_signatures']['error_signatures']; probes=data['diagnostic_probes']['diagnostic_probes']; cases=data['acceptance_cases']['acceptance_cases']; shared=data['shared_dependencies']['dependencies']
    for x in caps: validate_schema(x,'capability-definition.schema.json')
    for x in contracts: validate_schema(x,'reasoning-contract.schema.json')
    for x in errors: validate_schema(x,'error-signature.schema.json')
    for x in probes: validate_schema(x,'diagnostic-probe.schema.json')
    for x in cases: validate_schema(x,'acceptance-case.schema.json')
    cap_ids=[x['capability_id'] for x in caps]; shared_ids=[x['dependency_id'] for x in shared]
    if len(cap_ids)!=len(set(cap_ids)) or len(shared_ids)!=len(set(shared_ids)): raise ValueError('duplicate capability/dependency id')
    if any(x.startswith('SHARED-') for x in cap_ids): raise ValueError('shared dependency duplicated into Physics capability registry')
    cap_set=set(cap_ids); shared_set=set(shared_ids)
    for c in caps:
        unknown=set(c['external_dependencies'])-shared_set
        if unknown: raise ValueError('unknown external dependency '+str(sorted(unknown)))
    cp_map={}
    for rc in contracts:
        if rc['primary_capability_ref'] not in cap_set: raise ValueError('unknown primary capability')
        ords=[x['ordinal'] for x in rc['checkpoints']]
        if ords!=list(range(1,len(ords)+1)): raise ValueError('checkpoint ordinals must be contiguous')
        for cp in rc['checkpoints']:
            if cp['checkpoint_id'] in cp_map: raise ValueError('duplicate checkpoint id')
            if cp['capability_ref'] not in cap_set: raise ValueError('unknown checkpoint capability')
            cp_map[cp['checkpoint_id']]=cp
    state=next((x for x in contracts if x['contract_id']=='PHY-RC-MULTI-PHASE-STATE-PROPAGATION'),None)
    if not state: raise ValueError('missing state-propagation contract')
    expected=['PHY-SP-%02d'%i for i in range(1,10)]
    if [x['checkpoint_id'] for x in state['checkpoints']]!=expected: raise ValueError('state propagation must have exact 9-checkpoint spine')
    inv=next((x for x in state['invariants'] if x['invariant_id']=='PHY-INV-PHASE-HANDOFF'),None)
    if not inv or not inv['terminal_to_next_initial'] or not inv['discontinuity_exception']: raise ValueError('phase handoff invariant missing')
    if state['checkpoints'][5]['capability_ref']!='PHY-MOTION-PROPAGATE-STATE': raise ValueError('handoff checkpoint must belong to state propagation')
    if state['checkpoints'][-1]['capability_ref']!='PHY-PHYSICAL-VALIDATION': raise ValueError('state propagation must end in physical validation')
    error_ids=set()
    for e in errors:
        if e['error_signature_id'] in error_ids: raise ValueError('duplicate error signature')
        error_ids.add(e['error_signature_id'])
        if not set(e['capability_refs'])<=cap_set: raise ValueError('error references unknown capability')
        if not set(e['checkpoint_refs'])<=set(cp_map): raise ValueError('error references unknown checkpoint')
        if not e['hypothesis_only']: raise ValueError('canonical signature cannot be learner diagnosis')
    probe_ids=set()
    for p in probes:
        if p['probe_id'] in probe_ids: raise ValueError('duplicate probe')
        probe_ids.add(p['probe_id'])
        if p['target_capability_ref'] not in cap_set: raise ValueError('probe target unknown capability')
    required_cases={'PHY-AC-PROJECTILE-PRESERVE','PHY-AC-MULTI-PHASE-RESET','PHY-AC-SIGNED-DISPLACEMENT-AMBIGUOUS','PHY-AC-APEX-SKETCH-AMBIGUOUS','PHY-AC-ARITHMETIC-SEPARATION'}
    by_case={c['case_id']:c for c in cases}
    if set(by_case)!=required_cases: raise ValueError('acceptance case set drift')
    for c in cases:
        obs={x['checkpoint_ref']:x['status'] for x in c['observations']}
        if not set(obs)<=set(cp_map): raise ValueError('acceptance observation unknown checkpoint')
        if not set(c['preserved_capability_refs'])<=cap_set: raise ValueError('preserved capability unknown')
        if not set(c['required_probe_refs'])<=probe_ids: raise ValueError('required probe unknown')
        out=c['localized_outcome']
        if out['kind']=='PHYSICS_CAPABILITY' and out['ref'] not in cap_set: raise ValueError('localized Physics capability unknown')
        if out['kind']=='EXTERNAL_DEPENDENCY' and out['ref'] not in shared_set: raise ValueError('external dependency unknown')
        if out['kind']=='AMBIGUITY' and (out['ref'] not in cap_set or not c['required_probe_refs']): raise ValueError('ambiguity must bind capability and probe')
        if 'KINEMATICS=WEAK' not in c['forbidden_broad_conclusions']: raise ValueError('topic-weak collapse not explicitly forbidden')
    a=by_case['PHY-AC-PROJECTILE-PRESERVE']
    if a['localized_outcome']['ref']!='PHY-MOTION-PROPAGATE-STATE' or a['localized_outcome']['checkpoint_ref']!='PHY-SP-06': raise ValueError('projectile case not localized to handoff')
    if 'PHY-PROJECTILE-COMPONENT-DECOMPOSITION' not in a['preserved_capability_refs']: raise ValueError('projectile success not preserved')
    b=by_case['PHY-AC-MULTI-PHASE-RESET']
    if b['localized_outcome']['checkpoint_ref']!='PHY-SP-06' or 'PHY-MODEL-SELECTION' not in b['preserved_capability_refs']: raise ValueError('phase reset localization failure')
    c=by_case['PHY-AC-SIGNED-DISPLACEMENT-AMBIGUOUS']
    if c['localized_outcome']['kind']!='AMBIGUITY' or c['required_probe_refs']!=['PHY-PROBE-SIGNED-DISPLACEMENT']: raise ValueError('signed displacement ambiguity must probe')
    d=by_case['PHY-AC-APEX-SKETCH-AMBIGUOUS']
    if d['localized_outcome']['kind']!='AMBIGUITY' or d['required_probe_refs']!=['PHY-PROBE-APEX-COMPONENTS']: raise ValueError('apex ambiguity must probe')
    e=by_case['PHY-AC-ARITHMETIC-SEPARATION']
    if e['localized_outcome']!={'kind':'EXTERNAL_DEPENDENCY','ref':'SHARED-ARITHMETIC-EXECUTION','checkpoint_ref':None}: raise ValueError('arithmetic execution must remain external')
    if 'PHY-MODEL-SELECTION' not in e['preserved_capability_refs']: raise ValueError('model selection must survive arithmetic failure')
    scanned=json.dumps(data,sort_keys=True)
    if any(t in scanned for t in FORBIDDEN_PRODUCER_TOKENS): raise ValueError('benchmark/reference contamination in producer input')
    if data['acceptance_cases'].get('fixture_class')!='PUBLIC_SYNTHETIC': raise ValueError('only public synthetic fixture allowed')
    return True
def build_package(data):
    validate_inputs(data)
    components={k:sha_obj(v) for k,v in sorted(data.items())}
    semantic={'package_id':'PHY-V2-01-CANONICAL-PACKAGE','schema_version':'1.0.0','fixture_class':'PUBLIC_SYNTHETIC','components':copy.deepcopy(data)}
    semantic_digest=sha_obj(semantic)
    manifest={'schema_version':'1.0.0','package_id':'PHY-V2-01-CANONICAL-PACKAGE','fixture_class':'PUBLIC_SYNTHETIC','component_digests':components,'semantic_digest':semantic_digest,'benchmark_producer_inputs':0,'real_learner_data':0}
    validate_schema(manifest,'canonical-package-manifest.schema.json')
    return semantic,manifest
def write_package(out,data=None):
    data=data or load_inputs(); semantic,manifest=build_package(data); out=Path(out); out.mkdir(parents=True,exist_ok=True)
    (out/'canonical_package.json').write_text(json.dumps(semantic,indent=2,sort_keys=True)+'\n')
    (out/'canonical_package_manifest.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
    return semantic,manifest
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--out',required=True); a=ap.parse_args(); _,m=write_package(a.out); print(json.dumps({'status':'READY','semantic_digest':m['semantic_digest']},sort_keys=True))
if __name__=='__main__': main()
