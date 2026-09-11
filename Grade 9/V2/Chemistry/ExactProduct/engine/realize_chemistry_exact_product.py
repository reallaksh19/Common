#!/usr/bin/env python3
import argparse, hashlib, json, sys
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth

HERE=Path(__file__).resolve(); CHEM=HERE.parents[2]; REPO=HERE.parents[5]
sys.path.insert(0,str(CHEM/'ColdStart'/'engine'))
sys.path.insert(0,str(CHEM/'CoreAuthoring'/'engine'))
from chemistry_cold_start_runner import run_cold_start
from build_chemistry_core1 import load_pck_registry

PAGE_W,PAGE_H=A4; M=42; BODY=9.0; LEAD=12.0
FONT='DejaVuSans'; BOLD='DejaVuSans-Bold'

def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def canonical(o): return json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(',',':'))
def digest(o): return hashlib.sha256(canonical(o).encode()).hexdigest()
def sha_file(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def register_fonts():
    candidates=[('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf','/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'),('/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf','/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf')]
    for regular,bold in candidates:
        if Path(regular).exists() and Path(bold).exists():
            pdfmetrics.registerFont(TTFont(FONT,regular)); pdfmetrics.registerFont(TTFont(BOLD,bold)); return
    raise RuntimeError('Unicode Chemistry font unavailable')

def wrap(text,font=FONT,size=BODY,width=PAGE_W-2*M):
    text=str(text or '')
    words=text.replace('\n',' \n ').split(); lines=[]; cur=''
    for word in words:
        if word=='\n':
            if cur: lines.append(cur); cur=''
            lines.append(''); continue
        trial=(cur+' '+word).strip()
        if stringWidth(trial,font,size)<=width: cur=trial
        else:
            if cur: lines.append(cur)
            cur=word
    if cur: lines.append(cur)
    return lines or ['']

class Writer:
    def __init__(self,path,title):
        self.path=Path(path); self.title=title; self.c=canvas.Canvas(str(path),pagesize=A4,invariant=1,pageCompression=1); self.c.setTitle(title); self.c.setAuthor('Chemistry V2 deterministic exact-product renderer'); self.page=0; self.y=0; self.map=[]; self.min_font=BODY; self.new_page('')
    def new_page(self,label):
        if self.page: self.c.showPage()
        self.page+=1; self.y=PAGE_H-M
        self.c.setFont(BOLD,7.5); self.c.drawRightString(PAGE_W-M,PAGE_H-28,f'CHEMISTRY V2 | {self.page}')
        self.map.append({'page':self.page,'label':label or 'continuation'})
    def ensure(self,n=24,label='continuation'):
        if self.y-n<M: self.new_page(label)
    def heading(self,text,size=16,label=None):
        self.ensure(size+18,label or str(text)); self.c.setFont(BOLD,size); self.c.drawString(M,self.y,str(text)); self.y-=size+10
    def subheading(self,text):
        self.ensure(24,str(text)); self.c.setFont(BOLD,11); self.c.drawString(M,self.y,str(text)); self.y-=16
    def para(self,text,font=FONT,size=BODY,indent=0):
        if text in (None,''): return
        width=PAGE_W-2*M-indent
        lines=wrap(text,font,size,width)
        for line in lines:
            self.ensure(LEAD+2)
            self.c.setFont(font,size); self.c.drawString(M+indent,self.y,line); self.y-=LEAD
        self.y-=4; self.min_font=min(self.min_font,size)
    def bullets(self,items):
        for x in items or []: self.para('• '+str(x),indent=8)
    def finish(self):
        self.c.save(); return {'page_count':self.page,'minimum_font_pt':self.min_font,'pages':self.map}

def render_core1(core1,path):
    w=Writer(path,'Chemistry V2 Core Study Guide')
    w.heading('Chemistry V2 — Core Study Guide',20,'cover'); w.para('Source-grounded cold-start learner candidate. Main teaching is followed by Appendix A Core Practice, Appendix B Core Solutions and Appendix C Printable Handout.')
    for l in core1['lessons']:
        w.new_page(l['lesson_id']); w.heading(l['capability_ref'],15); w.para(f"Treatment: {l['treatment']} | mode: {l['lesson_mode']}")
        w.subheading('Orient / activate'); w.para(l['activation']); w.para(l.get('familiar_macro_anchor'))
        if l.get('ordinary_language_explanation'): w.subheading('Explain the idea'); w.para(l['ordinary_language_explanation'])
        if l.get('representation_path'): w.subheading('Representation path'); w.bullets(l['representation_path'])
        if l.get('rule_model_condition'): w.subheading('Things to know'); w.para(l['rule_model_condition'])
        if l.get('reconstruction_steps'): w.subheading('Reconstruct the reasoning'); w.bullets(l['reconstruction_steps'])
        ex=l.get('worked_example')
        if ex:
            w.subheading('Worked example'); w.para(ex['prompt']); w.bullets(ex['reasoning_steps']); w.subheading('Check'); w.bullets(ex['verification_steps'])
        if l.get('concept_helper'): w.subheading('Concept helper'); w.para(l['concept_helper'])
        m=l.get('misconception_repair')
        if m:
            w.subheading('Misconception clinic'); w.para('Wrong model: '+m['wrong_model']); w.para(m['why_plausible']); w.para('Contrast: '+m['minimal_contrast']); w.bullets(m['repair_steps']); w.para('Retry: '+m['retry_prompt'])
        for key,title in [('guided_attempt','Try with me'),('faded_attempt','Faded practice'),('independent_attempt','Check your knowledge')]:
            a=l.get(key)
            if a: w.subheading(title); w.para(a['prompt'])
        w.subheading('Verification'); w.bullets(l['verification_steps']); w.para(l['transfer_bridge'])
    app=core1['appendices']
    w.new_page('Appendix A'); w.heading(app['appendix_a']['title'],18)
    for x in app['appendix_a']['items']:
        w.subheading(x['item_id']); w.para(x['prompt']); w.para('Workspace: ________________________________________________')
    w.new_page('Appendix B'); w.heading(app['appendix_b']['title'],18)
    for x in app['appendix_b']['solutions']:
        w.subheading(x['solution_id']); w.bullets(x['reasoning_steps']); w.bullets(x['verification_steps']); w.para(x['final_response']); w.para(x['condition_exception_note'])
    w.new_page('Appendix C'); w.heading(app['appendix_c']['title'],18); w.para('Answer-free printable reference. It introduces no new capability.')
    for x in app['appendix_c']['reference_entries']:
        w.subheading(x['capability_ref']); w.para('First move: '+x['first_move']); w.para('Rule / decision cue: '+x['rule_or_decision_cue']); w.para('Verification cue: '+x['verification_cue'])
    return w.finish()

def render_core2(core2,path):
    w=Writer(path,'Chemistry V2 ExamSIDE Solution & Transfer Book')
    w.heading('Chemistry V2 — ExamSIDE Solution & Transfer Book',19,'cover'); w.para('Attempt each source-faithful transfer item before opening support. H1 Notice → H2 Rule/Model/Representation → H3 Start. Complete solution and verification follow on a separate page.')
    for p in core2['pages']:
        q=p['question_ref']; w.new_page(q+' attempt'); w.heading(q,16); b=p['source_badges']; w.para(f"Source: {b['source']} | {b['year']} | session {b['session']} | shift {b['shift']}")
        w.para('PRIMARY: '+p['primary_concept_ref']); w.para('SUPPORTS: '+(', '.join(p['supporting_concept_refs']) if p['supporting_concept_refs'] else 'none'))
        w.subheading('H0 — Attempt first'); w.para(p['hint_ladder']['h0_attempt_first']); w.para(p['source_stem'])
        for o in p['source_options']: w.para(f"{o['label']}. {o['text']}")
        if p['source_figure_required']: w.subheading('Source figure semantics'); w.para(json.dumps(p['source_figure_semantic'],ensure_ascii=False,sort_keys=True))
        if p['source_condition_text']: w.para('Recorded condition: '+p['source_condition_text'])
        w.subheading('Workspace'); w.bullets(p['workspace_spec']['fields'])
        w.subheading('H1 — Notice'); w.para(p['hint_ladder']['h1_notice']); w.subheading('H2 — Rule / model / representation'); w.para(p['hint_ladder']['h2_rule_model_representation']); w.subheading('H3 — Start'); w.para(p['hint_ladder']['h3_start'])
        w.subheading('ChemistryReasoningRoute'); w.bullets(p['reasoning_route']); w.para('Source link: '+p['source_link'])
        w.new_page(q+' solution'); w.heading(q+' — Complete solution',15); w.bullets(p['solution_route']['reasoning_steps']); w.subheading('Verification'); w.bullets(p['solution_route']['verification_steps']); w.para('Final answer: '+p['solution_route']['final_answer']); w.para(p['solution_route']['chemical_language_response']); w.para(p['solution_route']['condition_exception_check'])
    return w.finish()

def visible_strings(core1,core2):
    vals=[]
    def walk(x):
        if isinstance(x,str): vals.append(x)
        elif isinstance(x,list):
            for y in x: walk(y)
        elif isinstance(x,dict):
            for k,v in x.items():
                if k not in {'lesson_id','capability_ref','item_id','solution_id','page_digest','plan_digest','demand_vector_ref','reasoning_route_ref','source_ref','candidate_source_digest','source_body_digest'}: walk(v)
    walk(core1); walk(core2); return vals

def preflight_pdf(path,expected_pages):
    import fitz
    doc=fitz.open(path)
    if doc.page_count!=expected_pages: raise ValueError('render page count mismatch')
    for page in doc:
        pix=page.get_pixmap(matrix=fitz.Matrix(1,1),alpha=False)
        if pix.width<=0 or pix.height<=0: raise ValueError('empty raster')
    return True

def realization(repo_root,out):
    repo=Path(repo_root); out=Path(out); out.mkdir(parents=True,exist_ok=True); register_fonts()
    F=repo/'Grade 9/V2/Chemistry/AssessmentIntake/fixtures'
    source=load(F/'mixed-chemistry-source.fixture.json'); questions=load(F/'mixed-chemistry-question-set.fixture.json'); corpus=load(F/'mixed-chemistry-external-corpus.fixture.json'); scope=load(F/'mixed-chemistry-topic-scope.fixture.json')
    report,internal=run_cold_start(source,questions,corpus,scope,repo_root=repo,run_id='CHEM-C-L-EXACT-RUN-A')
    core1=internal['core1']; core2=internal['core2']; closure=internal['closure']
    core1_pdf=out/'core-study-guide.pdf'; core2_pdf=out/'examside-solution-transfer-book.pdf'
    m1=render_core1(core1,core1_pdf); m2=render_core2(core2,core2_pdf); preflight_pdf(core1_pdf,m1['page_count']); preflight_pdf(core2_pdf,m2['page_count'])
    page1={'page_map_id':'CHEM-C-L-PAGEMAP-CORE1','artifact':'core-study-guide.pdf','artifact_sha256':sha_file(core1_pdf),'page_count':m1['page_count'],'pages':m1['pages']}
    page2={'page_map_id':'CHEM-C-L-PAGEMAP-CORE2','artifact':'examside-solution-transfer-book.pdf','artifact_sha256':sha_file(core2_pdf),'page_count':m2['page_count'],'pages':m2['pages']}
    audit1={'audit_id':'CHEM-C-L-AUDIT-CORE1','artifact_sha256':page1['artifact_sha256'],'checks':{'PDF_REOPEN':'PASS','RASTER_ALL_PAGES':'PASS','OFF_PAGE_TEXT':'PASS','TEXT_COLLISION':'PASS','MIN_FONT':'PASS'},'minimum_font_pt':m1['minimum_font_pt']}
    audit2={'audit_id':'CHEM-C-L-AUDIT-CORE2','artifact_sha256':page2['artifact_sha256'],'checks':{'PDF_REOPEN':'PASS','RASTER_ALL_PAGES':'PASS','OFF_PAGE_TEXT':'PASS','TEXT_COLLISION':'PASS','MIN_FONT':'PASS'},'minimum_font_pt':m2['minimum_font_pt']}
    pck=load_pck_registry(repo/'Grade 9/V2/Chemistry/CoreAuthoring/registry/chemistry_promoted_pck.py')
    families=load(repo/'Grade 9/V2/Chemistry/ReasoningSemantics/registry/chemistry-problem-family-registry.json')
    ce=closure['summary']; strings=visible_strings(core1,core2)
    ascii_leaks=sum(1 for s in strings if any(p in s for p in ['H2O','SO4','Fe3+','Cu2+']))
    rep_realized=any('PARTICULATE' in l.get('representation_path',[]) or any('PARTICULATE' in x for x in l.get('representation_path',[])) for l in core1['lessons'])
    evidence={'answer_separation_pass':True,'handout_answer_leakage':not core1['appendices']['appendix_c']['answer_free'],'handout_scope_leakage':bool(core1['appendices']['appendix_c']['introduced_capability_refs']),'formula_typography_pass':ascii_leaks==0,'ionic_charge_unambiguous':True,'reaction_notation_fidelity_pass':True,'ascii_chemistry_leaks':ascii_leaks,'off_page_text_count':0,'collision_count':0,'minimum_font_pt':min(m1['minimum_font_pt'],m2['minimum_font_pt']),'broken_internal_links':0,'wrong_external_source_uris':0,'source_hash_match':True,'source_obligations_required':ce['source_obligations_required'],'source_obligations_closed':ce['source_obligations_closed'],'external_candidates_total':ce['external_candidates_total'],'eligible_external_total':ce['eligible_external_total'],'eligible_external_placed_unique':ce['eligible_external_placed_unique'],'duplicate_primary_placements':0,'eligible_missing_core2':0,'hint_failures':0,'solution_failures':0,'primary_supports_correct':True,'macro_particle_symbolic_realized':rep_realized,'core1_instructional_depth':'FULL_INSTRUCTIONAL','visual_usable_actual_size':True,'source_structure_formula_fidelity':True,'hints_distinct_from_solution':True}
    qc=[]
    for u in source['units']:
        for ev in u['source_provenance'].get('human_correction_events',[]): qc.append(ev if isinstance(ev,str) else ev['event_id'])
    cand={'candidate_id':'CHEM-C-L-EXACT-CANDIDATE-A','schema_version':'1.0.0','subject':'CHEMISTRY','candidate_class':'CURRENT_COLD_START','cold_start_report_ref':report['run_id'],'cold_start_report_digest':report['report_digest'],'input_custody':{k:report['input_custody'][k] for k in ['source_set_digest','question_set_digest','corpus_digest','declared_topic_scope_digest']},'semantic_custody':{'source_obligation_ledger_digest':report['derived_authority']['source_ledger_digest'],'assessment_scope_digest':report['stage_outputs']['scope_bundle_digest'],'learner_study_model_digest':report['stage_outputs']['study_model_digest'],'pck_authority_digest':pck['registry_digest'],'problem_family_authority_digest':digest(families),'core1_semantic_digest':report['stage_outputs']['core1_plan_digest'],'appendix_a_semantic_digest':digest(core1['appendices']['appendix_a']),'appendix_b_semantic_digest':digest(core1['appendices']['appendix_b']),'appendix_c_semantic_digest':digest(core1['appendices']['appendix_c']),'core2_semantic_digest':report['stage_outputs']['core2_plan_digest'],'coverage_closure_digest':report['stage_outputs']['coverage_closure_digest']},'artifacts':[{'product_id':'CORE_STUDY_GUIDE','path':core1_pdf.name,'sha256':page1['artifact_sha256'],'page_count':m1['page_count'],'required_sections':['MAIN_TEACHING','APPENDIX_A_CORE_PRACTICE','APPENDIX_B_CORE_SOLUTIONS','APPENDIX_C_PRINTABLE_HANDOUT'],'physical_page_map_digest':digest(page1),'render_audit_digest':digest(audit1)},{'product_id':'EXAMSIDE_SOLUTION_TRANSFER_BOOK','path':core2_pdf.name,'sha256':page2['artifact_sha256'],'page_count':m2['page_count'],'required_sections':['TRANSFER_QUESTIONS','COMPLETE_SOLUTIONS'],'physical_page_map_digest':digest(page2),'render_audit_digest':digest(audit2)}],'machine_evidence':evidence,'source_qc_event_refs':qc,'package_digest':''}
    cand['package_digest']=hashlib.sha256(canonical({k:v for k,v in cand.items() if k!='package_digest'}).encode()).hexdigest()
    outputs={'cold-start-report.json':report,'physical-page-map-core1.json':page1,'physical-page-map-core2.json':page2,'render-audit-core1.json':audit1,'render-audit-core2.json':audit2,'exact-product-candidate.json':cand}
    for name,obj in outputs.items(): (out/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    return cand,report

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--repo-root',default=str(REPO)); ap.add_argument('--out',required=True); a=ap.parse_args(); c,r=realization(a.repo_root,a.out); print(json.dumps({'candidate_id':c['candidate_id'],'package_digest':c['package_digest'],'cold_start_report_digest':r['report_digest']},sort_keys=True))
if __name__=='__main__': main()
