#!/usr/bin/env python3
import argparse, hashlib, json
from pathlib import Path
from jsonschema import Draft202012Validator
ROOT=Path(__file__).resolve().parents[1]; CONTRACTS=ROOT/'contracts'
FORBIDDEN_TOKENS=('PR #156','PR156','benchmark_template','benchmark_reference','mature_reference')
FORBIDDEN_KEYS={'page_layout','page_position','renderer','pdf','pagination','study_calendar','schedule','allocation_percent','benchmark_refs','reference_artifact'}

def load(p): return json.loads(Path(p).read_text())
def cb(o): return json.dumps(o,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def sh(o): return hashlib.sha256(cb(o)).hexdigest()
def sid(prefix,o): return prefix+sh(o)[:14].upper()
def validate(o,n): Draft202012Validator(load(CONTRACTS/n)).validate(o)
def walk(o,path=''):
    if isinstance(o,dict):
        for k,v in o.items():
            if k in FORBIDDEN_KEYS: raise ValueError('forbidden design input key: '+k)
            walk(v,path+'.'+k)
    elif isinstance(o,list):
        for i,v in enumerate(o): walk(v,f'{path}[{i}]')
    elif isinstance(o,str) and any(t in o for t in FORBIDDEN_TOKENS): raise ValueError('benchmark/reference contamination')

def reqmap(d): return {r['kind']:r['requirement_id'] for r in d.get('study_requirements',[])}
def crefs(d):
    s=set(d.get('canonical_refs',[]))
    for r in d.get('study_requirements',[]): s.update(r.get('canonical_refs',[]))
    s.update(d.get('probe_refs',[])); return sorted(s)
def block(order,target,role,canonical_refs,obligation_refs,support_level,payload):
    seed={'o':order,'t':target,'r':role,'c':canonical_refs,'q':obligation_refs,'p':payload}
    return {'block_id':sid('PHY-LD-B-',seed),'order':order,'target_id':target,'role':role,'canonical_refs':sorted(set(canonical_refs)),'obligation_refs':sorted(set(obligation_refs)),'support_level':support_level,'payload':payload}

def design(study_result,policy):
    walk(study_result); walk(policy); validate(policy,'physics-learning-design-policy.schema.json')
    if policy['benchmark_inputs']: raise ValueError('benchmark inputs forbidden')
    if study_result.get('status')!='PASS': raise ValueError('StudyModel must be PASS')
    m=study_result['learner_study_model']; decisions={d['target_id']:d for d in m['target_decisions']}
    required={'PHY-REFERENCE-FRAME','PHY-MODEL-SELECTION','PHY-STATE-VARIABLE-MEANING','PHY-PROJECTILE-COMPONENT-DECOMPOSITION','PHY-MOTION-PROPAGATE-STATE','PHY-SIGNED-DISPLACEMENT-INTERPRETATION'}
    if set(decisions)!=required: raise ValueError('unexpected/missing StudyModel targets')
    bindings=[{'target_id':d['target_id'],'engagement_mode':d['engagement_mode'],'readiness_mode':d['readiness_mode'],'source_capability_state':d['source_capability_state'],'probe_refs':d['probe_refs']} for d in sorted(decisions.values(),key=lambda x:x['target_id'])]
    blocks=[]; o=1
    for t in ('PHY-REFERENCE-FRAME','PHY-MODEL-SELECTION','PHY-STATE-VARIABLE-MEANING'):
        d=decisions[t]; rm=reqmap(d); role='ENTRY_POINT' if d['engagement_mode']=='USE_AS_ENTRY_POINT' else 'COMPLETION_EVIDENCE'
        payload={'instruction':'Activate the demonstrated Physics meaning without reteaching it.','preserve_source_state':d['source_capability_state']}
        blocks.append(block(o,t,role,crefs(d),list(rm.values()),1,payload)); o+=1
    for t in ('PHY-PROJECTILE-COMPONENT-DECOMPOSITION','PHY-SIGNED-DISPLACEMENT-INTERPRETATION'):
        d=decisions[t]; rm=reqmap(d); probe=d['probe_refs'][0]
        if d['readiness_mode']!='PROBE_FIRST': raise ValueError('probe-first treatment drift')
        payload={'probe_ref':probe,'correction_before_probe':False,'purpose':'Resolve the specific semantic ambiguity before any corrective branch.'}
        blocks.append(block(o,t,'DIAGNOSTIC_PROBE',[t,probe],[rm['DIAGNOSTIC_PROBE']],0,payload)); o+=1
    d=decisions['PHY-MOTION-PROPAGATE-STATE']; rm=reqmap(d)
    if d['readiness_mode']!='REPAIR_BEFORE': raise ValueError('state-handoff treatment drift')
    journey=[
      ('PREDICT',['CONCEPTUAL_BRIDGE'],2,{'prompt':'Before equations, predict which state variables persist across the phase boundary and what physical event could make one discontinuous.','requires_answer_before_explanation':True}),
      ('REPRESENTATION',['REPRESENTATION_MEANING'],2,{'representation':'BOUNDARY_STATE_TABLE','columns':['phase','terminal_state','next_initial_state','continuity_reason'],'semantic_payload':['system','reference_frame','phase_boundary','continuous_state_variables']}),
      ('RECONSTRUCTION',['RECONSTRUCTION'],2,{'rule':'For each continuous state variable, terminal value of phase n = initial value of phase n+1 unless an explicit impulse/discontinuity changes it.','symbolic_example':'v_(2,0) = v_(1,end) when no impulse acts at the boundary'}),
      ('MINIMAL_CONTRAST',['MISCONCEPTION_CONTRAST'],2,{'invariants':['same system','same reference frame','same phase-1 terminal state','same boundary event','same phase-2 model conditions'],'option_A':'Reset phase-2 initial velocity to a default/unrelated value.','option_B':'Carry phase-1 terminal velocity into phase 2 as its initial velocity.','focal_difference':'boundary-state handoff only','prediction_first':True}),
      ('WORKED_REASONING',['WORKED_REASONING'],2,{'situation':'A ball leaves a moving platform and then follows projectile motion.','reasoning_steps':['identify system and frame','state phase-1 terminal velocity','mark the boundary event','carry continuous velocity into phase-2 initial state','apply the new phase model','interpret sign/direction physically','check continuity and plausibility'],'answer_only':False,'verification_embedded':True}),
      ('GUIDED_ATTEMPT',[],2,{'prompts':['mark the phase boundary','write the terminal-state vector','state which entries persist into the next phase'],'conceptual_hint':True,'preselected_next_state':False}),
      ('FADED_ATTEMPT',[],1,{'prompts':['mark the boundary and write the next initial state'],'conceptual_hint':False,'preselected_next_state':False}),
      ('INDEPENDENT_ATTEMPT',[],0,{'prompt':'Solve a two-phase motion problem and show the state handoff at the boundary.','conceptual_hint':False,'preselected_next_state':False}),
      ('VERIFICATION',['VERIFICATION'],0,{'checks':['state continuity at boundary','units','sign/direction in fixed frame','physical plausibility'],'learner_must_apply':True}),
      ('TRANSFER',['TRANSFER'],0,{'situation':'A ball rolls off a table: constrained horizontal motion becomes projectile motion.','structural_changes':['phase type changes from supported motion to free flight','acceleration model changes at the boundary','two-dimensional representation becomes necessary'],'numbers_only_change':False}),
      ('COMPLETION_EVIDENCE',['COMPLETION_EVIDENCE'],0,{'evidence':'Independent solution explicitly carries continuous boundary state, selects the next model, and self-checks continuity/plausibility.','fresh_task_required':True})]
    for role,kinds,level,payload in journey:
        obligations=[rm[k] for k in kinds]
        blocks.append(block(o,d['target_id'],role,crefs(d),obligations,level,payload)); o+=1
    ext=[]
    for x in m['external_dependency_decisions']:
        b=block(o,x['dependency_ref'],'ACCESS_SUPPORT',x['canonical_refs'],[],1,{'scope':'execution_access_only','does_not_define_semantics':True,'does_not_replace_physics_repair':True}); blocks.append(b); o+=1
        ext.append({'dependency_ref':x['dependency_ref'],'readiness_mode':x['readiness_mode'],'semantics_owner':x['semantics_owner'],'block_id':b['block_id']})
    allreq={r['requirement_id'] for d in decisions.values() for r in d['study_requirements']}; coverage=[]
    for q in sorted(allreq):
        bids=[b['block_id'] for b in blocks if q in b['obligation_refs']]
        if not bids: raise ValueError('StudyModel obligation dropped: '+q)
        coverage.append({'requirement_id':q,'block_ids':bids})
    static={'schema_version':'1.0.0','source_study_model_id':m['study_model_id'],'source_study_input_digest':study_result['input_digest'],'policy_version':policy['version'],'target_bindings':bindings,'blocks':blocks,'obligation_coverage':coverage,'external_dependency_support':ext,'support_assets':policy['support_assets']}
    design_id=sid('PHY-LD-',static); payload={**static,'design_id':design_id}; digest=sh(payload); plan={**payload,'static_design_digest':digest}
    validate(plan,'physics-learning-design-plan.schema.json'); return plan

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--study-result',required=True); ap.add_argument('--policy',required=True); ap.add_argument('--out',required=True); a=ap.parse_args()
    r=design(load(a.study_result),load(a.policy)); Path(a.out).write_text(json.dumps(r,indent=2,sort_keys=True)+'\n'); print(json.dumps({'design_id':r['design_id'],'static_design_digest':r['static_design_digest']},sort_keys=True))
if __name__=='__main__': main()
