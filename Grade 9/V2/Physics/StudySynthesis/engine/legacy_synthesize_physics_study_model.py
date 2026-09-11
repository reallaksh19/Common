#!/usr/bin/env python3
import argparse, hashlib, json
from pathlib import Path
from jsonschema import Draft202012Validator

ROOT=Path(__file__).resolve().parents[1]
PHYSICS=ROOT.parent
CANON=PHYSICS/'Canonical'
CONTRACTS=ROOT/'contracts'
FORBIDDEN_KEYS={'raw_attempts','attempts','checkpoint_observations','answers','benchmark_refs','reference_artifact','hint_ladder','lesson_sequence','study_calendar','page_layout','renderer','practice_count','support_fading'}
FORBIDDEN_TOKENS=('PR #156','PR156','benchmark_template','benchmark_reference','mature_reference')
OUTPUT_FORBIDDEN={'hint_ladder','lesson_sequence','study_calendar','page_layout','renderer','practice_count','support_fading','worked_example_count','page_position'}

def load(p): return json.loads(Path(p).read_text())
def canonical_bytes(o): return json.dumps(o,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def sha(o): return hashlib.sha256(canonical_bytes(o)).hexdigest()
def stable(prefix,o): return prefix+sha(o)[:16].upper()
def validate(o,n): Draft202012Validator(load(CONTRACTS/n)).validate(o)

def walk(obj,path=''):
    if isinstance(obj,dict):
        for k,v in obj.items():
            if k in FORBIDDEN_KEYS: raise ValueError('forbidden producer input key: '+(path+'.'+k).strip('.'))
            walk(v,(path+'.'+k).strip('.'))
    elif isinstance(obj,list):
        for i,v in enumerate(obj): walk(v,f'{path}[{i}]')
    elif isinstance(obj,str) and any(t in obj for t in FORBIDDEN_TOKENS):
        raise ValueError('benchmark/reference contamination at '+path)

def canonical_ids():
    caps=load(CANON/'registry/capabilities.json')['capabilities']
    probes=load(CANON/'registry/diagnostic_probes.json')['diagnostic_probes']
    errs=load(CANON/'registry/error_signatures.json')['error_signatures']
    shared=load(CANON/'registry/shared_dependencies.json')['dependencies']
    return {x['capability_id'] for x in caps}|{x['probe_id'] for x in probes}|{x['error_signature_id'] for x in errs}|{x['dependency_id'] for x in shared}

def reason_refs(state,target):
    cap=next((x for x in state['capability_states'] if x['capability_ref']==target),None)
    if not cap: return []
    refs=list(cap.get('evidence_refs',[]))
    refs += ['DIAGNOSTIC:'+x['diagnostic_case_id'] for x in state.get('diagnostic_cases',[]) if x['target_ref']==target]
    return sorted(set(refs))

def external_reason_refs(state,dep):
    refs=[]
    for x in state.get('external_dependency_observations',[]):
        if x['dependency_ref']==dep: refs+=x.get('evidence_refs',[])
    refs += ['DIAGNOSTIC:'+x['diagnostic_case_id'] for x in state.get('diagnostic_cases',[]) if x['target_ref']==dep]
    return sorted(set(refs))

def find_forbidden_output(obj):
    found=[]
    def rec(x,path=''):
        if isinstance(x,dict):
            for k,v in x.items():
                if k in OUTPUT_FORBIDDEN: found.append((path+'.'+k).strip('.'))
                rec(v,(path+'.'+k).strip('.'))
        elif isinstance(x,list):
            for i,v in enumerate(x): rec(v,f'{path}[{i}]')
    rec(obj); return found

def gap(kind,target,refs):
    body={'gap_type':kind,'target_id':target,'required_refs':sorted(set(refs))}
    return {'gap_id':stable('GAP-',body),**body}

def blocked(goal,cks,state,policy,gaps):
    inp={'goal':goal,'cks':cks,'state_digest':state.get('semantic_digest'),'policy':policy}
    out={'schema_version':'1.0.0','status':'BLOCKED','gaps':sorted(gaps,key=lambda x:(x['gap_type'],x['target_id'],x['gap_id'])),'input_digest':sha(inp)}
    validate(out,'physics-study-result.schema.json'); return out

def synthesize(goal,cks,state,policy):
    for x in (goal,cks,state,policy): walk(x)
    validate(cks,'physics-canonical-knowledge-set.schema.json'); validate(policy,'physics-study-policy.schema.json')
    if policy['benchmark_inputs']: raise ValueError('benchmark inputs forbidden')
    if state.get('fixture_class')!='PUBLIC_SYNTHETIC': raise ValueError('only synthetic proof state is allowed here')
    if state.get('canonical_semantic_digest')!=cks['canonical_semantic_digest']:
        return blocked(goal,cks,state,policy,[gap('CANONICAL_IDENTITY_GAP','PHYSICS-CANONICAL',[cks['canonical_knowledge_set_id']])])
    known=canonical_ids(); provided=set(cks['refs'])
    if not provided<=known:
        return blocked(goal,cks,state,policy,[gap('CANONICAL_KNOWLEDGE_GAP','UNKNOWN-REF',provided-known)])
    states={x['capability_ref']:x for x in state['capability_states']}
    required=goal['required_target_ids']; gaps=[]
    for t in required:
        if t not in provided: gaps.append(gap('CANONICAL_KNOWLEDGE_GAP',t,[t]))
        if t not in states or not reason_refs(state,t): gaps.append(gap('LEARNER_STATE_REASON_GAP',t,[state['snapshot_id']]))
    repair_targets={t for t in required if t in states and states[t]['state']=='REPAIR_REQUIRED'}
    entry=set()
    for rt in repair_targets: entry.update(policy['entry_point_dependencies'].get(rt,[]))
    decisions=[]
    for t in sorted(required):
        if any(g['target_id']==t for g in gaps): continue
        cap=states[t]; src=cap['state']; rule=policy['target_rules'].get(src)
        if not rule: gaps.append(gap('STUDY_SYNTHESIS_POLICY_GAP',t,[policy['policy_id']])); continue
        engagement=rule['engagement']; readiness=rule['readiness']
        probes=sorted(cap.get('probe_refs',[]))
        if probes: readiness='PROBE_FIRST'
        if src=='READY' and t in entry: engagement='USE_AS_ENTRY_POINT'
        rr=reason_refs(state,t); reqs=[]
        for template in policy['requirements_by_target'].get(t,[]):
            crefs=sorted(set(template['canonical_refs'])); missing=set(crefs)-provided
            if missing: gaps.append(gap('CANONICAL_KNOWLEDGE_GAP',t,missing)); continue
            seed={'target':t,'kind':template['kind'],'canonical_refs':crefs,'reason_refs':rr}
            reqs.append({'requirement_id':stable('PHY-REQ-',seed),'kind':template['kind'],'canonical_refs':crefs,'learner_state_reason_refs':rr})
        if set(probes)-provided: gaps.append(gap('CANONICAL_KNOWLEDGE_GAP',t,set(probes)-provided))
        decisions.append({'target_id':t,'engagement_mode':engagement,'readiness_mode':readiness,'canonical_refs':[t],'learner_state_reason_refs':rr,'source_capability_state':src,'probe_refs':probes,'study_requirements':reqs})
    ext=[]
    for x in sorted(state.get('external_dependency_observations',[]),key=lambda z:z['dependency_ref']):
        if x['status']!='INVALID': continue
        dep=x['dependency_ref']; rr=external_reason_refs(state,dep)
        if dep not in provided: gaps.append(gap('CANONICAL_KNOWLEDGE_GAP',dep,[dep])); continue
        if not rr: gaps.append(gap('LEARNER_STATE_REASON_GAP',dep,[state['snapshot_id']])); continue
        ext.append({'dependency_ref':dep,'engagement_mode':'ACTIVE_STUDY','readiness_mode':'REPAIR_IN_UNIT','canonical_refs':[dep],'learner_state_reason_refs':rr,'semantics_owner':'EXTERNAL_CANONICAL_DEPENDENCY'})
    if gaps: return blocked(goal,cks,state,policy,gaps)
    seed={'goal_id':goal['goal_id'],'policy_version':policy['version'],'canonical_knowledge_set_id':cks['canonical_knowledge_set_id'],'learner_state_snapshot_id':state['snapshot_id'],'target_decisions':decisions,'external_dependency_decisions':ext}
    model={'schema_version':'1.0.0','study_model_id':stable('PHY-LSM-',seed),**seed}
    if find_forbidden_output(model): raise ValueError('forbidden LearningDesign/publication fields in StudyModel')
    validate(model,'physics-learner-study-model.schema.json')
    inp={'goal':goal,'cks':cks,'state_digest':state['semantic_digest'],'policy':policy}
    out={'schema_version':'1.0.0','status':'PASS','learner_study_model':model,'gaps':[],'input_digest':sha(inp)}
    validate(out,'physics-study-result.schema.json'); return out

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--goal',required=True); ap.add_argument('--cks',required=True); ap.add_argument('--learner-state',required=True); ap.add_argument('--policy',required=True); ap.add_argument('--out',required=True)
    a=ap.parse_args(); r=synthesize(load(a.goal),load(a.cks),load(a.learner_state),load(a.policy)); Path(a.out).write_text(json.dumps(r,indent=2,sort_keys=True)+'\n'); print(json.dumps({'status':r['status'],'input_digest':r['input_digest']},sort_keys=True))
if __name__=='__main__': main()
