#!/usr/bin/env python3
import argparse, json
from pathlib import Path
from jsonschema import Draft202012Validator

ROOT=Path(__file__).resolve().parents[1]
def load(p): return json.loads(Path(p).read_text())
def validate(o,n): Draft202012Validator(load(ROOT/'contracts'/n)).validate(o)

def one(blocks,target,role):
    xs=[b for b in blocks if b['target_id']==target and b['role']==role]
    if len(xs)!=1: raise ValueError(f'expected one {target}/{role}, found {len(xs)}')
    return xs[0]

def item(cid,primitive,blocks,title,body,job,support,metadata=None):
    refs=sorted({r for b in blocks for r in b.get('canonical_refs',[])})
    return {'content_id':cid,'materiality':'MATERIAL','primitive':primitive,
            'source_design_block_ids':[b['block_id'] for b in blocks],
            'canonical_refs':refs,'title':title,'body':body,'learner_job':job,
            'support_level':support,'metadata':metadata or {}}

def build(design, probes):
    blocks=design['blocks']
    probe_defs={p['probe_id']:p for p in probes['diagnostic_probes']}
    apex=one(blocks,'PHY-PROJECTILE-COMPONENT-DECOMPOSITION','DIAGNOSTIC_PROBE')
    disp=one(blocks,'PHY-SIGNED-DISPLACEMENT-INTERPRETATION','DIAGNOSTIC_PROBE')
    expected=[('PHY-PROBE-APEX-COMPONENTS',apex),('PHY-PROBE-SIGNED-DISPLACEMENT',disp)]
    for ref,b in expected:
        if b['payload']['probe_ref']!=ref or ref not in probe_defs: raise ValueError('probe binding drift: '+ref)
    entry=[one(blocks,'PHY-REFERENCE-FRAME','COMPLETION_EVIDENCE'),
           one(blocks,'PHY-MODEL-SELECTION','ENTRY_POINT'),
           one(blocks,'PHY-STATE-VARIABLE-MEANING','ENTRY_POINT')]
    roles={r:one(blocks,'PHY-MOTION-PROPAGATE-STATE',r) for r in
           ['PREDICT','REPRESENTATION','RECONSTRUCTION','MINIMAL_CONTRAST','WORKED_REASONING',
            'GUIDED_ATTEMPT','FADED_ATTEMPT','INDEPENDENT_ATTEMPT','VERIFICATION','TRANSFER','COMPLETION_EVIDENCE']}
    access=[b for b in blocks if b['target_id']=='SHARED-ARITHMETIC-EXECUTION' and b['role']=='ACCESS_SUPPORT']
    if len(access)!=1: raise ValueError('shared arithmetic support missing/duplicated')
    if not roles['WORKED_REASONING']['payload'].get('verification_embedded'): raise ValueError('worked reasoning lost verification')
    if roles['GUIDED_ATTEMPT']['support_level']!=2 or roles['FADED_ATTEMPT']['support_level']!=1 or roles['INDEPENDENT_ATTEMPT']['support_level']!=0:
        raise ValueError('fading invariant lost')
    if roles['TRANSFER']['payload'].get('numbers_only_change'): raise ValueError('transfer is number-only')

    ap=probe_defs['PHY-PROBE-APEX-COMPONENTS']; sd=probe_defs['PHY-PROBE-SIGNED-DISPLACEMENT']
    rep=roles['REPRESENTATION']['payload']; con=roles['MINIMAL_CONTRAST']['payload']; worked=roles['WORKED_REASONING']['payload']
    required_sem={'system','reference_frame','phase_boundary','continuous_state_variables'}
    if rep.get('representation')!='BOUNDARY_STATE_TABLE' or not required_sem.issubset(set(rep.get('semantic_payload',[]))): raise ValueError('boundary representation lost state semantics')
    if 'carry continuous velocity into phase-2 initial state' not in worked.get('reasoning_steps',[]): raise ValueError('worked reasoning lost explicit handoff')
    if roles['GUIDED_ATTEMPT']['payload'].get('conceptual_hint') is not True or roles['FADED_ATTEMPT']['payload'].get('conceptual_hint') is not False or roles['INDEPENDENT_ATTEMPT']['payload'].get('conceptual_hint') is not False or roles['INDEPENDENT_ATTEMPT']['payload'].get('preselected_next_state') is not False: raise ValueError('fading payload invariant lost')
    if access[0]['payload'].get('does_not_define_semantics') is not True or access[0]['payload'].get('does_not_replace_physics_repair') is not True: raise ValueError('shared arithmetic ownership drift')
    contents=[
      item('PC01','DIAGNOSTIC_PROBE_PANEL',[apex],'Probe first: velocity at the apex',
           [ap['prompt'],'Do not read a correction first. Commit to your component meanings before moving on.'],
           'Reveal whether horizontal and vertical velocity-component meaning is secure.',0,
           {'probe_ref':ap['probe_id'],'correction_before_probe':False,'expected_discrimination':ap['expected_discrimination']}),
      item('PC02','DIAGNOSTIC_PROBE_PANEL',[disp],'Probe first: signed displacement',
           [sd['prompt'],'Use the fixed east-positive frame. Explain the physical meaning of the sign, not only the subtraction.'],
           'Reveal whether directed displacement meaning is secure.',0,
           {'probe_ref':sd['probe_id'],'correction_before_probe':False,'expected_discrimination':sd['expected_discrimination']}),
      item('PC03','ENTRY_ANCHOR_PANEL',entry,'Start from what already works',
           ['Keep the demonstrated frame, model-selection, and state-variable meanings active.',
            'The repair target is the handoff between phases - not a restart of all kinematics.'],
           'Use preserved Physics reasoning as the entry point to a localized state-handoff repair.',1,
           {'preserved_strengths':['PHY-REFERENCE-FRAME','PHY-MODEL-SELECTION','PHY-STATE-VARIABLE-MEANING']}),
      item('PC04','PREDICT_BOX',[roles['PREDICT']],'Predict what crosses the boundary',
           [roles['PREDICT']['payload']['prompt'],
            'Write: persists / changes / cannot decide yet for velocity, position, acceleration model, and reference frame.'],
           'Predict continuous versus changed state before calculation.',2,{'prediction_before_explanation':True}),
      item('PC05','BOUNDARY_STATE_TABLE',[roles['REPRESENTATION']],'Make the handoff visible',
           ['Fill a boundary-state table with columns: phase | terminal state | next initial state | continuity reason.',
            'Record the system and reference frame above the table. Mark the physical boundary event explicitly.',
            'A value may jump only when the physical model includes a discontinuity such as an impulse.'],
           'Represent terminal and next-initial state in a phase-aware table.',2,
           {'representation':rep['representation'],'semantic_payload':rep['semantic_payload'],'columns':rep['columns']}),
      item('PC06','RECONSTRUCTION_LADDER',[roles['RECONSTRUCTION']],'Reconstruct the continuity rule',
           [roles['RECONSTRUCTION']['payload']['rule'],
            'Example structure: '+roles['RECONSTRUCTION']['payload']['symbolic_example'],
            'Say what physical event would justify breaking this equality.'],
           'Reconstruct why continuous state variables carry across a phase boundary.',2,
           {'continuity_rule':True}),
      item('PC07','MINIMAL_CONTRAST_PANEL',[roles['MINIMAL_CONTRAST']],'One difference: reset or carry?',
           ['Hold fixed: '+', '.join(con['invariants'])+'.',
            'A: '+con['option_A'],'B: '+con['option_B'],
            'Predict which handoff is physically valid and name the one focal difference before resolving.'],
           'Discriminate invalid reset from valid continuous handoff while all other dimensions stay fixed.',2,
           {'prediction_first':con['prediction_first'],'focal_difference':con['focal_difference'],'invariants':con['invariants']}),
      item('PC08','WORKED_REASONING_TRACE',[roles['WORKED_REASONING']],'Worked reasoning: state first, equation second',
           [worked['situation']]+['Step '+str(i+1)+': '+s for i,s in enumerate(worked['reasoning_steps'])]+
           ['Final check: continuity at the boundary, units, sign/direction, and physical plausibility.'],
           'Follow an explicit multi-phase state-propagation chain rather than answer-only substitution.',2,
           {'answer_only':worked['answer_only'],'verification_embedded':worked['verification_embedded']}),
      item('PC09','GUIDED_WORKSPACE',[roles['GUIDED_ATTEMPT']],'Guided handoff',
           ['A cart reaches a ramp boundary with velocity +4 m/s in a fixed right-positive frame. No impulse occurs at the boundary.',
            'Mark the boundary, write the terminal-state vector, then write the next initial state.',
            'Use the prompts from the design; do not change the model until the new phase begins.'],
           'Carry state across one explicit boundary with conceptual prompts.',2,{'conceptual_hint':True}),
      item('PC10','FADED_WORKSPACE',[roles['FADED_ATTEMPT']],'Faded handoff',
           ['A cyclist leaves a powered section and coasts on a new slope. The frame stays fixed and no impulse occurs at the transition.',
            'Mark the boundary and write the next initial state before applying the new acceleration model.'],
           'Choose the handoff with reduced conceptual support.',1,{'conceptual_hint':False}),
      item('PC11','INDEPENDENT_WORKSPACE',[roles['INDEPENDENT_ATTEMPT']],'Independent two-phase motion',
           ['Solve a two-phase motion problem and show the state handoff at the boundary.',
            'Your solution must identify the system, frame, phase boundary, terminal state, next initial state, and next model.'],
           'Solve independently with no conceptual hint or preselected next state.',0,
           {'conceptual_hint':False,'preselected_next_state':False}),
      item('PC12','PHYSICAL_VERIFICATION_STRIP',[roles['VERIFICATION']],'Check the physics, not only the arithmetic',
           ['Before moving on, check: '+', '.join(roles['VERIFICATION']['payload']['checks'])+'.',
            'If a state variable jumps, point to the physical event in your model that causes the discontinuity.'],
           'Apply continuity and plausibility checks to the completed reasoning.',0,
           {'checks':roles['VERIFICATION']['payload']['checks'],'learner_must_apply':True}),
      item('PC13','TRANSFER_CHALLENGE',[roles['TRANSFER']],'Transfer: supported motion becomes free flight',
           [roles['TRANSFER']['payload']['situation'],
            'Structural changes: '+'; '.join(roles['TRANSFER']['payload']['structural_changes'])+'.',
            'Carry the boundary state before choosing the free-flight model.'],
           'Transfer state-handoff reasoning when the phase type, acceleration model, and representation change.',0,
           {'numbers_only_change':False,'structural_changes':roles['TRANSFER']['payload']['structural_changes']}),
      item('PC14','COMPLETION_EVIDENCE_PANEL',[roles['COMPLETION_EVIDENCE']],'Finish with fresh evidence',
           ['Fresh task: a puck moves on a powered conveyor, leaves its edge, and then travels freely.',
            'Give an independent solution that carries the continuous boundary state, selects the next model, and checks continuity/plausibility.',
            'When you believe the solution is complete, stop.'],
           'Produce observable independent completion evidence on a fresh physical structure.',0,
           {'fresh_task_required':True}),
      item('PC15','ACCESS_SUPPORT_PANEL',access,'Execution support stays separate',
           ['If arithmetic execution blocks the Physics reasoning, use a short execution check without changing the Physics state model.',
            'This support does not define Physics semantics and does not replace the state-handoff repair.'],
           'Use execution support without reclassifying or rewriting Physics meaning.',1,
           {'dependency_ref':'SHARED-ARITHMETIC-EXECUTION','semantics_owner':'EXTERNAL_CANONICAL_DEPENDENCY'})
    ]
    product={'schema_version':'1.0.0','semantic_product_id':'PHY-SEMANTIC-PRODUCT-SYN-001','subject':'PHYSICS',
             'learning_design_id':design['design_id'],'learning_design_digest':design['static_design_digest'],
             'fixture_class':'PUBLIC_SYNTHETIC','authority':'LEARNER_SEMANTIC_PRODUCT','content_items':contents}
    validate(product,'physics-learner-semantic-product.schema.json')
    return product

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--design-plan',required=True); ap.add_argument('--canonical-probes',required=True); ap.add_argument('--out',required=True); a=ap.parse_args()
    p=build(load(a.design_plan),load(a.canonical_probes)); Path(a.out).write_text(json.dumps(p,indent=2,sort_keys=True)+'\n')
if __name__=='__main__': main()
