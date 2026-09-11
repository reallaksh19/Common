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

    table_headers=['Phase','Terminal state','Next initial state','Why']
    table_rows=[
      ['Phase 1','v_end = (6,0) m/s','v_0,2 = (6,0) m/s','No impulse at boundary'],
      ['Phase 2','projectile begins','same carried velocity','Model changes; state does not reset']]
    worked_values=['v_(1,end)=(+6.0,0) m/s','v_(2,0)=(+6.0,0) m/s','a_2=(0,-9.8) m/s^2','v_2(0.50s)=(+6.0,-4.9) m/s']
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
           ['System: ball that leaves a moving platform. Frame: east = +x, up = +y.',
            'Use the labeled table to separate the phase-1 terminal state from the phase-2 initial state and explain why each value is carried or changed.'],
           'Represent terminal and next-initial state in a phase-aware table.',2,
           {'representation':rep['representation'],'semantic_payload':rep['semantic_payload'],'columns':rep['columns'],
            'table_headers':table_headers,'table_rows':table_rows,'support_level':2}),
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
      item('PC08','WORKED_REASONING_TRACE',[roles['WORKED_REASONING']],'Worked trace: carry the state, then change the model',
           ['A ball moves east with a platform at 6.0 m/s and leaves a horizontal edge. Take east as +x and up as +y; neglect air resistance.',
            'Phase 1 terminal: v_(1,end) = (+6.0, 0) m/s.',
            'Boundary: contact is lost, so the force/model changes; no impulse acts, so velocity is continuous.',
            'Phase 2 initial: v_(2,0) = v_(1,end) = (+6.0, 0) m/s.',
            'Phase 2 model: a = (0, -9.8) m/s^2. After 0.50 s, v = (+6.0, -4.9) m/s.',
            'Check: the horizontal component is continuous, units are consistent, downward vertical velocity has the expected sign, and the motion is physically plausible.'],
           'Follow a concrete multi-phase state-value trace rather than answer-only substitution.',2,
           {'answer_only':False,'verification_embedded':True,'state_handoff_explicit':True,'worked_trace_values':worked_values,'support_level':2}),
      item('PC09','GUIDED_WORKSPACE',[roles['GUIDED_ATTEMPT']],'Guided handoff',
           ['A puck crosses into a rough patch moving right at +5.0 m/s. The frame stays fixed and no impulse acts at the boundary. In the rough patch a = -2.0 m/s^2.',
            'Find the velocity 1.5 s after the puck enters the rough patch.',
            'Hint: write the boundary handoff v_(2,0) = v_(1,end) before using the phase-2 model.'],
           'Carry state across one explicit boundary with conceptual prompts.',2,
           {'support_level':2,'conceptual_hints':['Write the boundary handoff before applying the new acceleration.'],'preselected_next_state':False}),
      item('PC10','FADED_WORKSPACE',[roles['FADED_ATTEMPT']],'Faded handoff',
           ['A cyclist is moving east at +8.0 m/s when braking begins. Use the same east-positive frame. During braking a = -1.5 m/s^2 for 3.0 s.',
            'Mark the phase boundary, write the carried phase-2 initial velocity, then calculate the velocity after 3.0 s.',
            'Reminder: keep one reference frame across the boundary.'],
           'Choose and use the state handoff with reduced conceptual support.',1,
           {'support_level':1,'conceptual_hints':['Keep the same reference frame across the boundary.'],'preselected_next_state':False}),
      item('PC11','INDEPENDENT_WORKSPACE',[roles['INDEPENDENT_ATTEMPT']],'Independent two-phase motion',
           ['An elevator is moving upward at +2.5 m/s when a braking phase begins. Upward remains positive and no impulse occurs at the transition. During braking a = -1.0 m/s^2 for 4.0 s.',
            'Find the elevator velocity after 4.0 s and its displacement during the braking phase.',
            'Show the phase-1 terminal state, the phase-2 initial state, the model used in phase 2, and your final physical interpretation.'],
           'Solve independently with no conceptual hint or preselected next state.',0,
           {'support_level':0,'conceptual_hints':[],'preselected_next_state':False}),
      item('PC12','PHYSICAL_VERIFICATION_STRIP',[roles['VERIFICATION']],'Check the physics, not only the arithmetic',
           ['For your independent solution, verify the boundary state before checking the arithmetic result.',
            'Check continuity at the boundary, units, sign/direction in the fixed frame, and physical plausibility.',
            'If a state variable jumps, identify the physical event in your model that causes the discontinuity.'],
           'Apply continuity and plausibility checks to completed reasoning.',0,
           {'checks':roles['VERIFICATION']['payload']['checks'],'learner_must_apply':True}),
      item('PC13','TRANSFER_CHALLENGE',[roles['TRANSFER']],'Transfer: supported motion becomes free flight',
           ['A parcel rides a horizontal conveyor at 3.0 m/s and leaves the edge 1.80 m above the floor. Take +x along the conveyor and +y upward; use g = 9.8 m/s^2.',
            'Write the carried velocity at the boundary, then determine the flight time and horizontal displacement before the parcel hits the floor.',
            'Explain which parts of the state stay continuous and which part of the model changes when support is lost.'],
           'Transfer state-handoff reasoning when phase type, acceleration model, and representation dimensionality change.',0,
           {'numbers_only_change':False,'structural_changes':roles['TRANSFER']['payload']['structural_changes'],'support_level':0}),
      item('PC14','COMPLETION_EVIDENCE_PANEL',[roles['COMPLETION_EVIDENCE']],'Finish with fresh evidence',
           ['Fresh task: a sled moves down a ramp at +6.0 m/s, then crosses onto a horizontal rough surface with no impulse at the boundary. Keep the same forward-positive frame. On the rough surface a = -2.0 m/s^2 for 2.0 s.',
            'Determine the velocity and displacement during the rough-surface phase. Show the terminal state from the ramp, the next initial state, and the phase-2 model.',
            'When you believe the solution is complete, stop.'],
           'Produce observable independent completion evidence on a fresh physical structure.',0,
           {'fresh_task':True,'fresh_task_required':True,'support_level':0,'conceptual_hints':[],'preselected_next_state':False}),
      item('PC15','ACCESS_SUPPORT_PANEL',access,'Execution support stays separate',
           ['If arithmetic execution blocks the Physics reasoning, use a short execution check without changing the Physics state model.',
            'This support does not define Physics semantics and does not replace the state-handoff repair.'],
           'Use execution support without reclassifying or rewriting Physics meaning.',1,
           {'dependency_ref':'SHARED-ARITHMETIC-EXECUTION','semantics_owner':'EXTERNAL_CANONICAL_DEPENDENCY'})
    ]
    product={'schema_version':'1.0.0','semantic_product_id':'PHY-SEMANTIC-PRODUCT-SYN-002','subject':'PHYSICS',
             'learning_design_id':design['design_id'],'learning_design_digest':design['static_design_digest'],
             'fixture_class':'PUBLIC_SYNTHETIC','authority':'LEARNER_SEMANTIC_PRODUCT','content_items':contents}
    validate(product,'physics-learner-semantic-product.schema.json')
    return product

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--design-plan',required=True); ap.add_argument('--canonical-probes',required=True); ap.add_argument('--out',required=True); a=ap.parse_args()
    p=build(load(a.design_plan),load(a.canonical_probes)); Path(a.out).write_text(json.dumps(p,indent=2,sort_keys=True)+'\n')
if __name__=='__main__': main()
