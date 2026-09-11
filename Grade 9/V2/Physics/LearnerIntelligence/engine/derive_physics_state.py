#!/usr/bin/env python3
import argparse, hashlib, json
from collections import defaultdict
from pathlib import Path
from jsonschema import Draft202012Validator

ROOT=Path(__file__).resolve().parents[1]
PHYSICS=ROOT.parent/'Canonical'
CONTRACTS=ROOT/'contracts'
FORBIDDEN_PRODUCER_TOKENS=('PR #156','PR156','benchmark_reference','benchmark_template','mature_reference')

def load(p): return json.loads(Path(p).read_text())
def canonical(o): return json.dumps(o,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def sha_obj(o): return hashlib.sha256(canonical(o)).hexdigest()
def validate(o,n): Draft202012Validator(load(CONTRACTS/n)).validate(o)

def canonical_maps():
    caps=load(PHYSICS/'registry/capabilities.json')['capabilities']
    rcs=load(PHYSICS/'registry/reasoning_contracts.json')['reasoning_contracts']
    probes=load(PHYSICS/'registry/diagnostic_probes.json')['diagnostic_probes']
    shared=load(PHYSICS/'registry/shared_dependencies.json')['dependencies']
    cap_ids={x['capability_id'] for x in caps}
    probe_ids={x['probe_id'] for x in probes}
    shared_ids={x['dependency_id'] for x in shared}
    cp_to_cap={}
    for rc in rcs:
        for cp in rc['checkpoints']:
            cp_to_cap[cp['checkpoint_id']]=cp['capability_ref']
    obj={'capabilities':caps,'reasoning_contracts':rcs,'diagnostic_probes':probes,'shared_dependencies':shared}
    return cap_ids,cp_to_cap,probe_ids,shared_ids,sha_obj(obj),obj

def derive(evidence,policy,interface):
    validate(evidence,'learner-evidence.schema.json')
    validate(policy,'inference-policy.schema.json')
    validate(interface,'interface-fixture.schema.json')
    raw=json.dumps({'evidence':evidence,'policy':policy,'interface':interface},sort_keys=True)
    if any(t in raw for t in FORBIDDEN_PRODUCER_TOKENS): raise ValueError('benchmark/reference contamination')
    if policy.get('benchmark_inputs'): raise ValueError('benchmark inputs forbidden')
    if interface['descriptive_only'] is not True: raise ValueError('interface must remain descriptive')
    if set(interface['forbidden_owned_decisions'])!={'STUDY_TREATMENT','TEACHING_CHOREOGRAPHY','SCHEDULING','PUBLICATION','BENCHMARK_VALIDATION'}:
        raise ValueError('learner intelligence interface acquired downstream authority')

    cap_ids,cp_to_cap,probe_ids,shared_ids,canon_digest,canon_obj=canonical_maps()
    canon_before=sha_obj(canon_obj)
    amap=policy.get('ambiguity_probe_map',{})
    for cap,probe in amap.items():
        if cap not in cap_ids or probe not in probe_ids: raise ValueError('ambiguity probe mapping has unknown canonical ref')

    valid=defaultdict(set); invalid=defaultdict(set); ambig=defaultdict(set); refs=defaultdict(set)
    external_raw=[]; seen_attempts=set()
    for att in evidence['attempts']:
        aid=att['attempt_id']
        if aid in seen_attempts: raise ValueError('duplicate attempt id')
        seen_attempts.add(aid)
        if att['independent_attempt'] is not True: raise ValueError('corroboration fixture requires independent attempts')
        for ob in att['checkpoint_observations']:
            cp=ob['checkpoint_ref']
            if cp not in cp_to_cap: raise ValueError('unknown canonical checkpoint '+cp)
            cap=cp_to_cap[cp]; refs[cap].add(aid+':'+cp)
            if ob['status']=='VALID': valid[cap].add(aid)
            elif ob['status']=='INVALID': invalid[cap].add(aid)
            else: ambig[cap].add(aid)
        for eo in att['external_dependency_observations']:
            if eo['dependency_ref'] not in shared_ids: raise ValueError('unknown shared dependency')
            external_raw.append({'dependency_ref':eo['dependency_ref'],'status':eo['status'],'evidence_ref':aid+':EXTERNAL'})

    states=[]
    for cap in sorted(cap_ids):
        pv,ni,na=len(valid[cap]),len(invalid[cap]),len(ambig[cap]); probes=[]
        if na:
            if cap not in amap: raise ValueError('ambiguous capability lacks canonical probe mapping: '+cap)
            probes=[amap[cap]]
        if ni>=policy['repair_required_min_independent_invalid_attempts']:
            state,evid,misc='REPAIR_REQUIRED','CORROBORATED','SUSPECTED'
        elif ni:
            state,evid,misc='DEVELOPING','SUSPECTED','SUSPECTED'
        elif pv>=policy['ready_min_independent_valid_attempts']:
            state,evid,misc='READY','DEMONSTRATED',('AMBIGUOUS' if na else 'NONE')
        elif na:
            state,evid,misc='UNKNOWN','AMBIGUOUS','AMBIGUOUS'
        else:
            state,evid,misc='UNKNOWN','NONE','NONE'
        row={'capability_ref':cap,'state':state,'evidence_status':evid,'positive_attempt_count':pv,'invalid_attempt_count':ni,'ambiguous_attempt_count':na,'evidence_refs':sorted(refs[cap]),'probe_refs':probes,'misconception_status':misc}
        validate(row,'capability-state.schema.json'); states.append(row)

    by={x['capability_ref']:x for x in states}
    for cap in ('PHY-REFERENCE-FRAME','PHY-PROJECTILE-COMPONENT-DECOMPOSITION','PHY-MODEL-SELECTION','PHY-STATE-VARIABLE-MEANING'):
        if by[cap]['state']!='READY': raise ValueError('positive Physics evidence was not preserved: '+cap)
    signed=by['PHY-SIGNED-DISPLACEMENT-INTERPRETATION']
    if signed['state'] not in ('UNKNOWN','DEVELOPING') or signed['probe_refs']!=['PHY-PROBE-SIGNED-DISPLACEMENT']:
        raise ValueError('signed displacement ambiguity policy violation')
    if 'PHY-PROBE-APEX-COMPONENTS' not in by['PHY-PROJECTILE-COMPONENT-DECOMPOSITION']['probe_refs']:
        raise ValueError('apex ambiguity probe missing')

    ext_group=defaultdict(lambda:{'statuses':[],'refs':[]})
    for x in external_raw:
        ext_group[x['dependency_ref']]['statuses'].append(x['status']); ext_group[x['dependency_ref']]['refs'].append(x['evidence_ref'])
    external=[]
    for dep,v in sorted(ext_group.items()):
        status='INVALID' if 'INVALID' in v['statuses'] else ('AMBIGUOUS' if 'AMBIGUOUS' in v['statuses'] else 'VALID')
        external.append({'dependency_ref':dep,'status':status,'evidence_refs':sorted(v['refs'])})

    handoff_refs=sorted(r for r in refs['PHY-MOTION-PROPAGATE-STATE'] if r.endswith(':PHY-SP-06'))
    apex_refs=sorted(r for r in refs['PHY-PROJECTILE-COMPONENT-DECOMPOSITION'] if r.endswith(':PHY-PJ-02') and r.split(':')[0] in ambig['PHY-PROJECTILE-COMPONENT-DECOMPOSITION'])
    cases=[
      {'diagnostic_case_id':'PHY-DC-HANDOFF-001','case_type':'LOCALIZED_FAILURE','target_ref':'PHY-MOTION-PROPAGATE-STATE','evidence_refs':handoff_refs,'status':'CORROBORATED','probe_refs':[],'broad_topic_conclusion':False},
      {'diagnostic_case_id':'PHY-DC-SIGNED-001','case_type':'AMBIGUITY','target_ref':'PHY-SIGNED-DISPLACEMENT-INTERPRETATION','evidence_refs':sorted(refs['PHY-SIGNED-DISPLACEMENT-INTERPRETATION']),'status':'PROBE_REQUIRED','probe_refs':['PHY-PROBE-SIGNED-DISPLACEMENT'],'broad_topic_conclusion':False},
      {'diagnostic_case_id':'PHY-DC-APEX-001','case_type':'AMBIGUITY','target_ref':'PHY-PROJECTILE-COMPONENT-DECOMPOSITION','evidence_refs':apex_refs,'status':'PROBE_REQUIRED','probe_refs':['PHY-PROBE-APEX-COMPONENTS'],'broad_topic_conclusion':False}
    ]
    for x in external:
        if x['status']=='INVALID': cases.append({'diagnostic_case_id':'PHY-DC-EXTERNAL-'+x['dependency_ref'],'case_type':'EXTERNAL_DEPENDENCY','target_ref':x['dependency_ref'],'evidence_refs':x['evidence_refs'],'status':'EXTERNAL','probe_refs':[],'broad_topic_conclusion':False})
    for x in cases: validate(x,'diagnostic-case.schema.json')

    payload={'snapshot_id':'PHY-V2-02-STATE-SYN-001','fixture_class':'PUBLIC_SYNTHETIC','canonical_semantic_digest':canon_digest,'policy_id':policy['policy_id'],'capability_states':states,'diagnostic_cases':cases,'external_dependency_observations':external,'forbidden_inferences':sorted(policy['forbidden_inferences'])}
    result={'schema_version':'1.0.0',**payload,'semantic_digest':sha_obj(payload)}
    validate(result,'learner-state-snapshot.schema.json')
    if sha_obj(canonical_maps()[-1])!=canon_before: raise AssertionError('learner state mutated canonical truth')
    return result

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--evidence',required=True); ap.add_argument('--policy',required=True); ap.add_argument('--interface',required=True); ap.add_argument('--out',required=True)
    a=ap.parse_args(); r=derive(load(a.evidence),load(a.policy),load(a.interface)); Path(a.out).write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'READY','semantic_digest':r['semantic_digest']},sort_keys=True))
if __name__=='__main__': main()
