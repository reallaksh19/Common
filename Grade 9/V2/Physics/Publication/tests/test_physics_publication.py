#!/usr/bin/env python3
import copy, importlib.util, json, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def loadmod(name,p):
    s=importlib.util.spec_from_file_location(name,p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
buildmod=loadmod('build',ROOT/'engine/build_semantic_product.py')
realmod=loadmod('real',ROOT/'engine/realize_physics_publication.py')
valmod=loadmod('val',ROOT/'validator/validate_candidate.py')
TARGET=json.loads((ROOT/'fixtures/publication_target.synthetic.json').read_text())
POLICY=json.loads((ROOT/'fixtures/publication_policy.synthetic.json').read_text())
PROBES={'diagnostic_probes':[
 {'probe_id':'PHY-PROBE-APEX-COMPONENTS','prompt':'At the apex, state vx and vy qualitatively. Is total speed zero?','expected_discrimination':'components vs total','target_capability_ref':'PHY-PROJECTILE-COMPONENT-DECOMPOSITION'},
 {'probe_id':'PHY-PROBE-SIGNED-DISPLACEMENT','prompt':'East is positive. Move from +3 m to -2 m. State displacement and sign meaning.','expected_discrimination':'directed displacement','target_capability_ref':'PHY-SIGNED-DISPLACEMENT-INTERPRETATION'}]}
def B(i,t,r,c,p,l=0): return {'block_id':f'PHY-LD-B-{i:014d}','order':i,'target_id':t,'role':r,'canonical_refs':c,'obligation_refs':[],'support_level':l,'payload':p}
def fake_design():
    i=1; bs=[]
    def add(t,r,c,p,l=0):
        nonlocal i; bs.append(B(i,t,r,c,p,l)); i+=1
    add('PHY-REFERENCE-FRAME','COMPLETION_EVIDENCE',['PHY-REFERENCE-FRAME'],{'instruction':'preserve'},1)
    add('PHY-MODEL-SELECTION','ENTRY_POINT',['PHY-MODEL-SELECTION'],{'instruction':'preserve'},1)
    add('PHY-STATE-VARIABLE-MEANING','ENTRY_POINT',['PHY-STATE-VARIABLE-MEANING'],{'instruction':'preserve'},1)
    add('PHY-PROJECTILE-COMPONENT-DECOMPOSITION','DIAGNOSTIC_PROBE',['PHY-PROJECTILE-COMPONENT-DECOMPOSITION','PHY-PROBE-APEX-COMPONENTS'],{'probe_ref':'PHY-PROBE-APEX-COMPONENTS','correction_before_probe':False},0)
    add('PHY-SIGNED-DISPLACEMENT-INTERPRETATION','DIAGNOSTIC_PROBE',['PHY-SIGNED-DISPLACEMENT-INTERPRETATION','PHY-PROBE-SIGNED-DISPLACEMENT'],{'probe_ref':'PHY-PROBE-SIGNED-DISPLACEMENT','correction_before_probe':False},0)
    t='PHY-MOTION-PROPAGATE-STATE'; c=[t,'PHY-SP-06']
    add(t,'PREDICT',c,{'prompt':'predict persistence','requires_answer_before_explanation':True},2)
    add(t,'REPRESENTATION',c,{'representation':'BOUNDARY_STATE_TABLE','columns':['phase','terminal_state','next_initial_state','continuity_reason'],'semantic_payload':['system','reference_frame','phase_boundary','continuous_state_variables']},2)
    add(t,'RECONSTRUCTION',c,{'rule':'terminal = next initial if continuous','symbolic_example':'v_(2,0) = v_(1,end)'},2)
    add(t,'MINIMAL_CONTRAST',c,{'invariants':['same system','same reference frame','same phase-1 terminal state','same boundary event','same phase-2 model conditions'],'option_A':'reset next state','option_B':'carry terminal state','focal_difference':'boundary-state handoff only','prediction_first':True},2)
    add(t,'WORKED_REASONING',c,{'situation':'platform to flight','reasoning_steps':['identify system and frame','state phase-1 terminal velocity','mark the boundary event','carry continuous velocity into phase-2 initial state','apply the new phase model','interpret sign/direction physically','check continuity and plausibility'],'answer_only':False,'verification_embedded':True},2)
    add(t,'GUIDED_ATTEMPT',c,{'prompts':['mark boundary'],'conceptual_hint':True,'preselected_next_state':False},2)
    add(t,'FADED_ATTEMPT',c,{'prompts':['mark boundary'],'conceptual_hint':False,'preselected_next_state':False},1)
    add(t,'INDEPENDENT_ATTEMPT',c,{'prompt':'solve','conceptual_hint':False,'preselected_next_state':False},0)
    add(t,'VERIFICATION',c,{'checks':['state continuity at boundary','units','sign/direction in fixed frame','physical plausibility'],'learner_must_apply':True},0)
    add(t,'TRANSFER',c,{'situation':'rolls off table','structural_changes':['phase type changes','acceleration model changes','representation dimensionality changes'],'numbers_only_change':False},0)
    add(t,'COMPLETION_EVIDENCE',c,{'evidence':'fresh','fresh_task_required':True},0)
    add('SHARED-ARITHMETIC-EXECUTION','ACCESS_SUPPORT',['SHARED-ARITHMETIC-EXECUTION'],{'scope':'execution_access_only','does_not_define_semantics':True,'does_not_replace_physics_repair':True},1)
    return {'schema_version':'1.0.0','source_study_model_id':'PHY-STUDY-X','source_study_input_digest':'a'*64,'policy_version':'P','target_bindings':[],'blocks':bs,'obligation_coverage':[],'external_dependency_support':[],'support_assets':[],'design_id':'PHY-LD-TEST0000000000','static_design_digest':'b'*64}
def expect_fail(fn):
    try: fn()
    except Exception: return
    raise AssertionError('expected failure')
def mutate_file(path,fn):
    o=json.loads(path.read_text()); fn(o); path.write_text(json.dumps(o,indent=2,sort_keys=True)+'\n')
def main():
    d=fake_design(); original=copy.deepcopy(d); product=buildmod.build(d,PROBES)
    assert d==original and len(product['content_items'])==15
    bad=copy.deepcopy(d); next(b for b in bad['blocks'] if b['role']=='REPRESENTATION')['payload']['semantic_payload']=['phase_boundary']; expect_fail(lambda: buildmod.build(bad,PROBES))
    bad=copy.deepcopy(d); next(b for b in bad['blocks'] if b['role']=='WORKED_REASONING')['payload']['reasoning_steps'].remove('carry continuous velocity into phase-2 initial state'); expect_fail(lambda: buildmod.build(bad,PROBES))
    bad=copy.deepcopy(d); next(b for b in bad['blocks'] if b['role']=='FADED_ATTEMPT')['support_level']=2; expect_fail(lambda: buildmod.build(bad,PROBES))
    bad=copy.deepcopy(d); next(b for b in bad['blocks'] if b['role']=='INDEPENDENT_ATTEMPT')['payload']['conceptual_hint']=True; expect_fail(lambda: buildmod.build(bad,PROBES))
    bad=copy.deepcopy(d); next(b for b in bad['blocks'] if b['role']=='TRANSFER')['payload']['numbers_only_change']=True; expect_fail(lambda: buildmod.build(bad,PROBES))
    bad=copy.deepcopy(d); bad['blocks']=[b for b in bad['blocks'] if b['role']!='VERIFICATION']; expect_fail(lambda: buildmod.build(bad,PROBES))
    bad=copy.deepcopy(d); next(b for b in bad['blocks'] if b['target_id']=='SHARED-ARITHMETIC-EXECUTION')['payload']['does_not_define_semantics']=False; expect_fail(lambda: buildmod.build(bad,PROBES))
    badp=copy.deepcopy(product); badp['content_items'][0]['source_design_block_ids']=['PHY-LD-B-99999999999999']; expect_fail(lambda: realmod.realize(badp,TARGET,POLICY,d,tempfile.mkdtemp()))
    badp=copy.deepcopy(product); badp['content_items'][0]['title']='PR #156 template'; expect_fail(lambda: realmod.realize(badp,TARGET,POLICY,d,tempfile.mkdtemp()))
    p0=copy.deepcopy(product); d0=copy.deepcopy(d)
    with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
        realmod.realize(product,TARGET,POLICY,d,a); realmod.realize(product,TARGET,POLICY,d,b)
        valmod.run(a)
        assert Path(a,'candidate.pdf').read_bytes()==Path(b,'candidate.pdf').read_bytes()
        assert Path(a,'publication_manifest.json').read_bytes()==Path(b,'publication_manifest.json').read_bytes()
        assert product==p0 and d==d0
        pol=copy.deepcopy(POLICY); pol['page_groups'][-1]['content_refs'].remove('PC15'); expect_fail(lambda: realmod.realize(product,TARGET,pol,d,tempfile.mkdtemp()))
        c=Path(a); orig=(c/'physical_page_map.json').read_text()
        mutate_file(c/'physical_page_map.json',lambda o:o['content_placements'].pop()); expect_fail(lambda: valmod.run(a)); (c/'physical_page_map.json').write_text(orig)
        mutate_file(c/'physical_page_map.json',lambda o:o['content_placements'].append(copy.deepcopy(o['content_placements'][0]))); expect_fail(lambda: valmod.run(a)); (c/'physical_page_map.json').write_text(orig)
        mutate_file(c/'physical_page_map.json',lambda o:o['content_placements'][0].update({'x1':999})); expect_fail(lambda: valmod.run(a)); (c/'physical_page_map.json').write_text(orig)
        mutate_file(c/'physical_page_map.json',lambda o:o['content_placements'][0].update({'renderer_emitted':False})); expect_fail(lambda: valmod.run(a)); (c/'physical_page_map.json').write_text(orig)
        s_orig=(c/'publication_structure.json').read_text()
        mutate_file(c/'publication_structure.json',lambda o:o['page_intents'][0].update({'content_refs':['PC03','PC01','PC02']})); expect_fail(lambda: valmod.run(a)); (c/'publication_structure.json').write_text(s_orig)
        m_orig=(c/'publication_manifest.json').read_text()
        mutate_file(c/'publication_manifest.json',lambda o:o['quality_states'].update({'SUBJECT_CORRECTNESS':'PASS'})); expect_fail(lambda: valmod.run(a)); (c/'publication_manifest.json').write_text(m_orig)
        mutate_file(c/'publication_manifest.json',lambda o:o.update({'package_digest':'0'*64})); expect_fail(lambda: valmod.run(a)); (c/'publication_manifest.json').write_text(m_orig)
        au_orig=(c/'publication_audit.json').read_text()
        mutate_file(c/'publication_audit.json',lambda o:o.update({'artifact_sha256':'0'*64})); expect_fail(lambda: valmod.run(a)); (c/'publication_audit.json').write_text(au_orig)
        pdf=Path(c/'candidate.pdf'); pb=pdf.read_bytes(); pdf.write_bytes(pb+b'\nDRIFT'); expect_fail(lambda: valmod.run(a)); pdf.write_bytes(pb)
    print('20 PHY-V2-05 publication falsifiers = PASS')
if __name__=='__main__': main()
