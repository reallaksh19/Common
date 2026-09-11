#!/usr/bin/env python3
import argparse, json
from pathlib import Path
REQUIRED={'S02','S04','E01','E02','E04','E06','E07','E08','E09','E10','E11','E12','B01','B03','B05','B06','B07','P01','V01','V02'}

def load(p): return json.loads(Path(p).read_text())
def item(cid,primitive,refs,title,body,job,support=None,metadata=None):
    return {'content_id':cid,'materiality':'MATERIAL','primitive':primitive,'learning_design_refs':refs,'title':title,'body':body,'learner_job':job,'support_level':support,'metadata':metadata or {}}

def build(design_result):
    if design_result.get('status')!='READY': raise ValueError('LearningDesign result not READY')
    plan=design_result['learning_design_plan']; sm={s['step_id']:s for s in plan['steps']}
    missing=sorted(REQUIRED-set(sm))
    if missing: raise ValueError(f'merged LearningDesign missing required steps: {missing}')
    e04=sm['E04']['payload']; e06=sm['E06']['payload']; b01=sm['B01']['payload']; b03=sm['B03']['payload']; p01=sm['P01']['payload']
    if not e06.get('one_legal_operation_per_line'): raise ValueError('E06 lost one-operation-per-line invariant')
    worked=[e06['problem']]
    for line in e06['lines']: worked.append(f"{line['from']}  -- {line['operation']} ->  {line['to']}")
    worked.append('Check: '+e06['self_check'])
    contents=[
      item('C01','ENTRY_ANCHOR_PANEL',['S02'],'Start from a strength',['You already formed a valid system. Keep that setup and use it as the launch point.','Do not restart the modelling; focus on what each legal transformation preserves.'],'Recognize a demonstrated setup as an entry point, not a reteach.',0),
      item('C02','PREDICT_BOX',['E01'],'Predict before you move',[sm['E01']['payload']['prompt'],'Mark LEGAL or NOT LEGAL before writing the next line.'],'Predict whether a proposed algebraic move preserves the same solution set.',1),
      item('C03','RECONSTRUCTION_LADDER',['E02'],'What equality must preserve',[sm['E02']['payload']['meaning']]+['1. '+x for x in sm['E02']['payload']['route']],'Reconstruct equality as an invariant-preserving relation.',2),
      item('C04','MINIMAL_CONTRAST_PANEL',['E04'],'One difference: legal or illegal?',['Shared: '+', '.join(e04['controlled_shared_structure']),'Difference: '+e04['focal_distinction'],'Predict first. Then explain '+e04['discrimination_target']+'.'],'Discriminate two nearly identical transformations using one focal distinction.',2,{'prediction_before_resolution':e04['prediction_before_resolution'],'focal_distinction':e04['focal_distinction']}),
      item('C05','WORKED_REASONING_STACK',['E06'],'Worked reasoning: one legal operation per line',worked,'Follow the equivalence-preserving chain and verify against the original equation.',2,{'one_legal_operation_per_line':True}),
      item('C06','GUIDED_WORKSPACE',['E07'],'Guided attempt',['Solve 3x + 5 = 23.','Write the operation name before each new line.','Support: '+sm['E07']['payload']['conceptual_hints'][0]],'Produce equivalent lines with explicit operation names.',2),
      item('C07','FADED_WORKSPACE',['E08'],'Faded attempt',['Solve 5x - 9 = 2x + 12.','Only reminder: '+sm['E08']['payload']['conceptual_hints'][0]],'Choose and execute legal transformations with reduced support.',1),
      item('C08','INDEPENDENT_WORKSPACE',['E09'],'Independent attempt',['Solve 4(2x - 1) = 3x + 17.','Show one legal mathematical transformation per line.'],'Solve independently with no conceptual hint or preselected operation.',0,{'conceptual_hints':[],'preselected_operation':False}),
      item('C09','SELF_CHECK_STRIP',['E10','V01'],'Check the original relation',[sm['E10']['payload']['prompt'],'Choose a check: '+', '.join(sm['V01']['payload']['methods'])+'.','Do the check before you move on.'],'Initiate and execute an appropriate mathematical verification.',0),
      item('C10','RECONSTRUCTION_LADDER',['B01'],'Square the whole binomial, not only the ends',[b01['meaning']]+['1. '+x for x in b01['route']],'Reconstruct a binomial square from repeated-product structure.',2),
      item('C11','MINIMAL_CONTRAST_PANEL',['B03'],'Where did the middle term go?',['Shared: '+', '.join(b03['controlled_shared_structure']),'Difference: '+b03['focal_distinction'],'Predict which expansion preserves the repeated product before resolving.'],'Discriminate correct expansion from structure loss.',2,{'prediction_before_resolution':True,'focal_distinction':b03['focal_distinction']}),
      item('C12','FADED_WORKSPACE',['B05'],'Faded binomial practice',['Expand (x - 4)^2.','Reminder: '+sm['B05']['payload']['conceptual_hints'][0]],'Expand with only a structural reminder.',1),
      item('C13','INDEPENDENT_WORKSPACE',['B06'],'Independent binomial practice',['Expand (2y - 3)^2 from structure.','No formula cue is supplied.'],'Expand independently from the repeated-product meaning.',0,{'conceptual_hints':[]}),
      item('C14','DIAGNOSTIC_PROBE_PANEL',['P01'],'Probe first: ordered pairs and slope',['No explanation first.','Point A=(2,7), point B=(5,1). Label x1,y1,x2,y2, then write the slope expression before calculating.','Probe ref: '+p01['probe_ref']], 'Reveal whether coordinate-role meaning or execution needs follow-up.',0,{'probe_ref':p01['probe_ref'],'explanation_before_probe':False}),
      item('C15','REPRESENTATION_PANEL',['S04'],'Representation bridge',[f"Source: {sm['S04']['payload']['source']}",f"Destination: {sm['S04']['payload']['destination']}",f"Job: {sm['S04']['payload']['translation_job']}",f"Preserve: {sm['S04']['payload']['invariant']}"],'Translate between representations while preserving the represented quantity.',1),
      item('C16','TRANSFER_CHALLENGE',['E11','B07'],'Transfer: same ideas, different structure',[sm['E11']['payload']['prompt'],'Also use a binomial square inside a geometry-derived equation with symbolic parameters.','Do not rely on number pattern matching.'],'Transfer repaired semantics across structure, representation and task direction.',0,{'number_only':False,'structural_changes':sm['E11']['payload']['structural_changes']+sm['B07']['payload']['structural_changes']}),
      item('C17','COMPLETION_EVIDENCE_PANEL',['E12','V02'],'Finish by proving independence',[sm['E12']['payload']['observable'],sm['V02']['payload']['observable'],'No verification prompt is supplied. Choose and perform the check yourself.'],'Provide observable independent completion evidence, including self-initiated verification.',0,{'prompted':False})
    ]
    return {'semantic_product_id':'MATH-SEMANTIC-PRODUCT-SYN-001','schema_version':'1.0.0','subject':'MATHEMATICS','learning_design_id':plan['learning_design_id'],'learning_design_digest':plan['design_digest'],'fixture_class':'PUBLIC_SYNTHETIC','authority':'LEARNER_SEMANTIC_PRODUCT','content_items':contents}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--design-result',required=True); ap.add_argument('--out',required=True); a=ap.parse_args()
    product=build(load(a.design_result)); Path(a.out).write_text(json.dumps(product,indent=2,sort_keys=True)+'\n')
if __name__=='__main__': main()
