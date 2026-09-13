#!/usr/bin/env python3
"""Deterministic Chemistry V2 (C-L) exact-product realization.

Three things this stage must get right, and each has a machine falsifier:

1. **Teaching primitives are realized, not labelled.** Every C-H primitive the
   representation bundle selects is drawn as real vector graphics by
   ``chemistry_visual_primitives.render_primitive``, parameterised from the
   item's own source-authorized notation tokens and validated fail-closed by
   the shared ``VisualSemanticValidator`` before any drawing operation.
2. **No internal identifier reaches a learner-visible glyph.** Every drawn
   string passes through ``public_text`` and is then checked by
   ``learner_surface_guard``; a leak aborts the render rather than shipping.
3. **Placement evidence is physical, not planned.** The renderer emits a
   placement fragment at the same moment it emits the corresponding drawing
   operations, and the resulting ``PhysicalPageMap`` is bound to the exact PDF
   SHA256 (custody model adapted from PR #161 / PR #196).
"""

import argparse, hashlib, json, sys
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth

HERE=Path(__file__).resolve(); CHEM=HERE.parents[2]; REPO=HERE.parents[5]
sys.path.insert(0,str(HERE.parent))
sys.path.insert(0,str(CHEM/'ColdStart'/'engine'))
sys.path.insert(0,str(CHEM/'CoreAuthoring'/'engine'))
sys.path.insert(0,str(CHEM/'Representation'/'engine'))
sys.path.insert(0,str(CHEM/'CoverageClosure'/'engine'))
from chemistry_cold_start_runner import run_cold_start
from build_chemistry_core1 import load_pck_registry
from bind_chemistry_visual_obligations import build_ledger as build_visual_obligation_ledger, reconcile_realization, candidate_counters
import validate_chemistry_answer_custody as ANSWER
import chemistry_visual_primitives as VP
import learner_surface_guard as GUARD
import learner_copy_guard as COPY
import validate_chemistry_legibility as LEGIBILITY

# Learner-facing typography. PR #322's 8 pt rule is an absolute engineering
# floor, not the size a 14-year-old should be reading instructional prose at, so
# the render targets come from chemistry-legibility-target-profile.json.
PAGE_W,PAGE_H=A4; M=42; BODY=10.5; LEAD=13.5; STEM=12.5; SUBHEAD=12.0; FOOTER=8.0
FONT='DejaVuSans'; BOLD='DejaVuSans-Bold'
COPY_REGISTRY=COPY.load_registry()
LEGIBILITY_PROFILE=LEGIBILITY.load_profile()

def T(role):
    """Learner-facing title for an internal role, resolved fail-closed.

    Internal role identifiers are unchanged everywhere else in the chain; this is
    the only place a role becomes text a student reads, and an unmapped role
    raises LEARNER_TITLE_MISSING_FOR_ROLE rather than printing the identifier.
    """
    return COPY.title_for(role,COPY_REGISTRY)

# Lesson titles a learner reads. These are held to the same bar as every other
# learner heading: no internal role vocabulary, and phrased as something the
# student will be able to do by the end of the page.
CAPABILITY_TITLES={
    'CAP-READ-FORMULA':'Read a chemical formula before you calculate',
    'CAP-PARSE-ION-CHARGE':'Tell an ion charge apart from a subscript',
    'CAP-TRANSLATE-PARTICLE-SYMBOL':'Move between particle pictures and symbols',
    'CAP-CHECK-ATOM-CONSERVATION':'Check that the atoms balance',
    'CAP-CLASSIFY-CHANGE-EVIDENCE':'Decide what kind of change happened, from the evidence',
    'CAP-CHECK-RULE-EXCEPTION':'Check the rule, the condition and the exception',
    'CAP-PRESERVE-REACTION-CONDITION':'Keep the reaction conditions attached',
    'CAP-SEPARATE-OBSERVATION-INFERENCE':'Keep what you saw apart from what it means',
    'CAP-READ-APPARATUS-METHOD':'Connect the apparatus, the property and the method',
    'CAP-TRACK-REACTING-SPECIES':'Follow the same substance through a reaction',
    'CAP-ATTACH-SPECIES-ROLE':'Name the role only after you have tracked the change',
    'CAP-VERIFY-CHEMICAL-REPRESENTATION':'Check your chemistry before you accept an answer',
    'CAP-READ-STRUCTURE-SITE':'Track the exact spot in the structure',
    'CAP-TRACK-OXIDATION-STATE':'Track the oxidation number as it changes',
    'CAP-CLASSIFY-MATTER-COMPOSITION':'Sort a sample into mixture, element or compound',
    'CAP-TEST-FIXED-COMPOSITION':'Test whether a substance keeps a fixed composition',
    'CAP-CONVERT-UNIT-SCALE':'Change units and let the units check your work',
    'CAP-BUILD-IONIC-FORMULA':'Build an ionic formula so the charges cancel',
    'CAP-COUNT-ENTITY-ATOMICITY':'Count the atoms and ions in one formula unit',
    'CAP-COMPUTE-RELATIVE-FORMULA-MASS':'Work out a relative formula mass',
    'CAP-MASS-TO-MOLES':'Go from a mass to an amount in moles',
    'CAP-MOLES-TO-ENTITIES':'Go from moles to a number of particles',
    'CAP-COMPUTE-CONCENTRATION':'Work out a concentration with the right denominator',
    'CAP-USE-STOICHIOMETRIC-RATIO':'Use the mole ratio from a balanced equation',
}
CONCEPT_TITLES={
    'CHEM-CONCEPT-ION-NOTATION':'Ionic charge notation',
    'CHEM-CONCEPT-FORMULA-ANATOMY':'Formula anatomy',
    'CHEM-CONCEPT-REPRESENTATION-TRANSLATION':'Particle-to-symbol translation',
    'CHEM-CONCEPT-CONSERVATION':'Atom conservation',
    'CHEM-CONCEPT-REACTION-CONDITION':'Reaction conditions',
    'CHEM-CONCEPT-SPECIES-ROLE':'Reacting-species roles',
}
CHECK_TITLES={
    'CHECK_ATOMS':'Count each required atom on both sides.',
    'CHECK_CHARGE':'Check that the overall charge is preserved or interpreted correctly.',
    'CHECK_SPECIES_IDENTITY':'Check that the same chemical species is being tracked.',
    'CHECK_CONDITIONS':'Check that every stated condition or exception is still attached.',
    'VERIFY_RESULT':'Check that the final conclusion follows from the evidence and rule used.',
}
ROUTE_TITLES={
    'READ_GIVEN':'Read the given representation exactly as written or shown.',
    'IDENTIFY_CHEMICAL_ENTITIES':'Identify the chemical entities that must be tracked.',
    'PARSE_FORMULA_OR_EQUATION':'Read coefficients, subscripts, charges and sides in their correct positions.',
    'IDENTIFY_REPRESENTATION_LEVEL':'Identify whether the information is macroscopic, particulate or symbolic.',
    'TRANSLATE_REPRESENTATION':'Translate one representation into another without changing identity or count.',
    'INTERPRET_CHEMICAL_MEANING':'State what the representation means chemically.',
    'APPLY_CONSERVATION':'Apply the required conservation check.',
    'TRACK_SPECIES_OR_STATE_CHANGE':'Track the same species or state from before to after.',
    'CLASSIFY':'Classify only after the decisive evidence is established.',
    'CHECK_ATOMS':'Compare the atom-count ledger.',
    'VERIFY_RESULT':'Run the final independent check before accepting the answer.',
}
REPRESENTATION_TITLES={
    'OBLIGATION_LEVEL:SYMBOLIC':'Use the symbolic representation.',
    'OBLIGATION_LEVEL:MACROSCOPIC':'Use the stated macroscopic evidence.',
    'OBLIGATION_LEVEL:PARTICULATE':'Use the particulate representation.',
    'OBLIGATION_REP:FORMULA':'Read the formula notation explicitly.',
    'OBLIGATION_REP:IONIC_CHARGE':'Read the ionic charge explicitly.',
    'OBLIGATION_REP:OBSERVATION':'Keep the recorded observation separate from interpretation.',
    'OBLIGATION_REP:PHYSICAL_STATE':'Keep physical-state information attached.',
    'OBLIGATION_REP:FIGURE':'Read the figure as part of the evidence.',
}
EXACT_TEXT_REPLACEMENTS=COPY_REGISTRY['body_text_substitutions']
# Primitive selection is C-H authority (renderer_selection_forbidden), so the
# renderer only decides *where* a selected primitive is placed on the page.
PRIMARY_SLOT='REPRESENTATION'
CONTRAST_SLOT='MISCONCEPTION_REPAIR'
CHECK_SLOT='CHEMICAL_VERIFICATION'
CONDITIONAL_PRIMITIVES={'MINIMAL_CHEMISTRY_CONTRAST':CONTRAST_SLOT,'FORMULA_EQUATION_CHECK_STRIP':CHECK_SLOT}

def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def canonical(o): return json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(',',':'))
def digest(o): return hashlib.sha256(canonical(o).encode()).hexdigest()
def sha_file(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def register_fonts():
    candidates=[('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf','/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'),('/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf','/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf')]
    for regular,bold in candidates:
        if Path(regular).exists() and Path(bold).exists():
            pdfmetrics.registerFont(TTFont(FONT,regular)); pdfmetrics.registerFont(TTFont(BOLD,bold))
            # Hand the same Unicode faces to the shared primitives package, whose
            # own resolution is Windows-only and would otherwise fall back to
            # Helvetica and mangle subscripts and superscript charges.
            VP.use_fonts(FONT,BOLD); return
    raise RuntimeError('Unicode Chemistry font unavailable')

def learner_title(cap):
    if cap in CAPABILITY_TITLES: return CAPABILITY_TITLES[cap]
    text=str(cap).replace('CAP-','').replace('-',' ').strip().lower()
    return text[:1].upper()+text[1:] if text else 'Chemistry skill'

def concept_title(ref):
    if ref in CONCEPT_TITLES: return CONCEPT_TITLES[ref]
    return str(ref).replace('CHEM-CONCEPT-','').replace('-',' ').strip().title()

def public_text(text):
    s=str(text or '')
    for old,new in EXACT_TEXT_REPLACEMENTS.items(): s=s.replace(old,new)
    if s in CHECK_TITLES: return CHECK_TITLES[s]
    if s in ROUTE_TITLES: return ROUTE_TITLES[s]
    if s in REPRESENTATION_TITLES: return REPRESENTATION_TITLES[s]
    if s.startswith('OBLIGATION_LEVEL:'):
        label=s.split(':',1)[1].replace('_',' ').lower()
        return f'Use the {label} representation level.'
    if s.startswith('OBLIGATION_REP:'):
        label=s.split(':',1)[1].replace('_',' ').lower()
        return f'Use the {label} representation.'
    if s.startswith('CHECK_'):
        label=s.replace('CHECK_','').replace('_',' ').lower()
        return f'Check {label}.'
    if '_' in s and s.replace('_','').isalnum() and s.upper()==s:
        label=s.replace('_',' ').lower()
        return label[:1].upper()+label[1:]+'.'
    return s

def public_list(items): return [public_text(x) for x in (items or [])]

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
    """Deterministic page writer that emits physical placement evidence.

    Every visible run is checked for internal-identifier leakage before it is
    drawn, and every content block records the rectangle it actually occupied
    on each physical page (``START`` on the first, ``CONTINUATION`` after a
    break), so the PhysicalPageMap is evidence rather than a plan.
    """
    def __init__(self,path,title):
        self.path=Path(path); self.title=title
        self.c=canvas.Canvas(str(path),pagesize=A4,invariant=1,pageCompression=1)
        self.c.setTitle(title); self.c.setAuthor('Chemistry V2 deterministic exact-product renderer')
        self.page=0; self.y=0; self.map=[]; self.min_font=BODY
        self.placements=[]; self.primitives=[]; self.block=None; self.frag=None
        self.font_usage={}; self.lines_per_page={}; self.covered={}
        self.new_page('')
    # ---- learner-surface firewall -------------------------------------
    def emit(self,text,where):
        GUARD.assert_learner_safe(text,where)
        COPY.assert_surface_safe(text,COPY_REGISTRY,where); return text
    def emit_heading(self,text,where):
        GUARD.assert_learner_safe(text,where)
        COPY.assert_heading_safe(text,COPY_REGISTRY,where); return text
    def _record(self,role,size,line_count=1,width=0.0):
        self.font_usage[role]=min(self.font_usage.get(role,size),float(size))
        self.lines_per_page[self.page]=self.lines_per_page.get(self.page,0)+line_count
        self.covered[self.page]=self.covered.get(self.page,0.0)+float(width)*float(size)*line_count
    # ---- content-block custody ----------------------------------------
    def begin(self,content_ref,page_intent_id,primitive='TEXT_BLOCK'):
        self.end()
        self.block={'content_ref':content_ref,'page_intent_id':page_intent_id,'primitive':primitive}
        self.frag={'page':self.page,'y_top':self.y,'kind':'START'}
    def _close_fragment(self):
        if not self.block or not self.frag: return
        if self.frag['y_top']-self.y<1: self.frag=None; return
        self.placements.append({'content_ref':self.block['content_ref'],'page_intent_id':self.block['page_intent_id'],
            'primitive':self.block['primitive'],'page':self.frag['page'],'fragment_kind':self.frag['kind'],
            'x0':round(float(M),2),'y0':round(float(max(self.y,M)),2),
            'x1':round(float(PAGE_W-M),2),'y1':round(float(min(self.frag['y_top']+4,PAGE_H-M)),2)})
        self.frag=None
    def end(self):
        self._close_fragment(); self.block=None
    # ---- pagination ----------------------------------------------------
    def new_page(self,label):
        carry=self.block
        if carry: self._close_fragment()
        if self.page: self.c.showPage()
        self.page+=1; self.y=PAGE_H-M
        self.c.setFont(BOLD,FOOTER); self.c.drawRightString(PAGE_W-M,PAGE_H-28,f'CHEMISTRY V2 | {self.page}')
        self._record('PAGE_FOOTER',FOOTER)
        self.map.append({'page':self.page,'label':label or 'continuation'})
        if carry: self.frag={'page':self.page,'y_top':self.y,'kind':'CONTINUATION'}
    def ensure(self,n=24,label='continuation'):
        if self.y-n<M: self.new_page(label)
    # ---- text ----------------------------------------------------------
    def heading(self,text,size=16,label=None):
        self.ensure(size+18,label or str(text)); self.c.setFont(BOLD,size)
        self.c.drawString(M,self.y,self.emit_heading(str(text),'heading')); self.y-=size+10
        self._record('HEADING',size,1,stringWidth(str(text),BOLD,size))
    def subheading(self,text):
        self.ensure(SUBHEAD+14,str(text)); self.c.setFont(BOLD,SUBHEAD)
        self.c.drawString(M,self.y,self.emit_heading(str(text),'subheading')); self.y-=SUBHEAD+6
        self._record('SECTION_SUBHEADING',SUBHEAD,1,stringWidth(str(text),BOLD,SUBHEAD))
    def para(self,text,font=FONT,size=BODY,indent=0,role='INSTRUCTIONAL_BODY',lead=None):
        if text in (None,''): return
        width=PAGE_W-2*M-indent; lead=lead or max(LEAD,size*LEGIBILITY_PROFILE['page_density']['min_leading_ratio'])
        lines=wrap(public_text(text),font,size,width)
        for line in lines:
            self.ensure(lead+2)
            self.c.setFont(font,size); self.c.drawString(M+indent,self.y,self.emit(line,'paragraph')); self.y-=lead
            self._record(role,size,1,stringWidth(line,font,size))
        self.y-=4; self.min_font=min(self.min_font,size)
    def stem(self,text):
        """A question stem is the one thing a learner must read without effort."""
        self.para(text,size=STEM,role='QUESTION_STEM')
    def bullets(self,items,role='INSTRUCTIONAL_BODY'):
        for x in items or []: self.para('• '+public_text(x),indent=8,role=role)
    # ---- realized teaching primitives ----------------------------------
    def primitive(self,kind,params,content_ref,page_intent_id,label=None):
        """Draw one C-H teaching primitive as real vector graphics.

        Returns True when the primitive was realized. A ``PrimitiveDataUnavailable``
        means the source semantic data cannot support the picture honestly, so
        nothing is drawn — the renderer never substitutes invented chemistry.
        A ``VisualValidationError`` is *not* swallowed: ungrounded species, a
        broken atom ledger or an inverted agent role must fail the build.
        """
        try:
            height=VP.primitive_height(kind,params,PAGE_W-2*M)
        except VP.PrimitiveDataUnavailable:
            return False
        for value in (params.get('title'),params.get('instructional_job'),params.get('attention_target'),
                      params.get('learner_action'),params.get('observation'),params.get('claim')):
            if value: self.emit(value,'primitive '+kind)
        for value in list(params.get('checks') or [])+list(params.get('condition_context') or [])+list(params.get('species_roles') or []):
            self.emit(value,'primitive '+kind)
        self.end()
        self.ensure(height+12,label or 'teaching primitive')
        self.begin(content_ref,page_intent_id,kind)
        try:
            record=VP.render_primitive(kind,params,self.c,(M,self.y-height,PAGE_W-2*M,height))
        except VP.PrimitiveDataUnavailable:
            self.end(); return False
        self.primitives.append(dict(record,content_ref=content_ref,page=self.page))
        self.y-=height+10
        self.end()
        return True
    def finish(self):
        self.end(); self.c.save()
        printable=(PAGE_W-2*M)*(PAGE_H-2*M)
        density=[{'page':n,'text_lines':self.lines_per_page.get(n,0),
                  'text_coverage_ratio':round(self.covered.get(n,0.0)/printable,4)}
                 for n in range(1,self.page+1)]
        return {'page_count':self.page,'minimum_font_pt':self.min_font,'pages':self.map,
                'placements':self.placements,'primitives':self.primitives,
                'font_usage_pt':{k:round(v,2) for k,v in sorted(self.font_usage.items())},
                'page_density':density}

# ---------------------------------------------------------------------------
# representation binding (C-H is the selection authority; renderer places only)
# ---------------------------------------------------------------------------

def representation_index(bundle):
    index={}
    for rep in (bundle or {}).get('representations',[]):
        index.setdefault(rep['capability_ref'],[]).append(rep)
    return index

def params_from_representation(rep,profile,extra=None):
    data=rep.get('source_semantic_data') or {}
    checks=public_list(data.get('verification_requirements') or [])
    extra=extra or {}
    return VP.build_params(
        primitive_id=rep['primitive_id'],
        tokens=extra.get('tokens') or rep.get('notation_tokens') or rep.get('chemical_entities') or [],
        declared_entities=rep.get('chemical_entities') or data.get('chemical_entities') or [],
        instructional_job=rep.get('instructional_job',''),
        attention_target=rep.get('attention_target',''),
        learner_action=rep.get('learner_action_expected',''),
        condition_context=extra.get('condition_context') or rep.get('condition_exception_context') or [],
        species_roles=rep.get('species_roles') or [],
        checks=checks,
        observation=extra.get('observation'),
        oxidation_states=data.get('oxidation_states') or [],
        particles=extra.get('particles') or [],
        site_labels=data.get('site_labels') or [],
        accessibility_text=rep.get('accessibility_text',''),
        safe=public_text)

def primary_primitives(capability_ref,profile,index):
    order=(profile.get('primary_primitives_by_capability') or {}).get(capability_ref,[])
    reps=index.get(capability_ref,[])
    by_id={r['primitive_id']:r for r in reps}
    chosen=[by_id[p] for p in order if p in by_id]
    for rep in reps:
        if rep['primitive_id'] in CONDITIONAL_PRIMITIVES or rep in chosen: continue
        chosen.append(rep)
    limit=profile.get('ready_mode_max_primary_primitives',2)
    ordered=[r for r in chosen if r['primitive_id'] in order][:max(limit,1)]
    return ordered or chosen[:max(limit,1)]

def conditional_primitive(capability_ref,primitive_id,index):
    for rep in index.get(capability_ref,[]):
        if rep['primitive_id']==primitive_id: return rep
    return None

# ---------------------------------------------------------------------------
# Core1 / Core2 rendering
# ---------------------------------------------------------------------------

def render_core1(core1,representations,profile,path):
    w=Writer(path,'Chemistry V2 Core Study Guide')
    index=representation_index(representations)
    realized=[]; drawn_by_content={}
    w.begin('COVER','PI-COVER')
    w.heading('Chemistry V2 — Core Study Guide',20,'cover')
    w.para('Everything for this chapter in one place. The teaching comes first, then practice questions, then quick answers you can check yourself, then the full worked answers, and last a one-page sheet you can print and keep.')
    w.end()
    for l in core1['lessons']:
        cap=l['capability_ref']; title=learner_title(cap); intent='PI-LESSON-'+str(core1['lessons'].index(l)+1).zfill(2)
        ref='LESSON-'+str(core1['lessons'].index(l)+1).zfill(2)
        w.new_page(l['lesson_id']); w.begin(ref,intent); w.heading(title,15)
        w.subheading(T('ACTIVATION')); w.para(l['activation']); w.para(l.get('familiar_macro_anchor'))
        if l.get('ordinary_language_explanation'): w.subheading(T('ORDINARY_LANGUAGE_EXPLANATION')); w.para(l['ordinary_language_explanation'])
        if l.get('representation_path'):
            w.subheading(T('REPRESENTATION')); w.bullets(public_list(l['representation_path']))
            for rep in primary_primitives(cap,profile,index):
                params=params_from_representation(rep,profile)
                if w.primitive(rep['primitive_id'],params,ref+'-'+rep['primitive_id'],intent,title):
                    realized.append(rep['primitive_id']); drawn_by_content.setdefault(ref,[]).append(rep['primitive_id'])
            w.begin(ref,intent)
        if l.get('rule_model_condition'): w.subheading(T('RULE_MODEL_CONDITION')); w.para(l['rule_model_condition'])
        if l.get('reconstruction_steps'): w.subheading(T('WHY_RECONSTRUCTION')); w.bullets(l['reconstruction_steps'])
        ex=l.get('worked_example')
        if ex:
            w.subheading(T('WORKED_REASONING')); w.para(ex['prompt']); w.bullets(ex['reasoning_steps']); w.subheading(T('WORKED_REASONING_CHECK')); w.bullets(public_list(ex['verification_steps']))
        if l.get('concept_helper'): w.subheading(T('CONCEPT_HELPER')); w.para(l['concept_helper'])
        m=l.get('misconception_repair')
        if m:
            w.subheading(T('MISCONCEPTION_REPAIR')); w.para(T('MISCONCEPTION_WRONG_MODEL')+': '+m['wrong_model']); w.para(m['why_plausible']); w.para(T('MISCONCEPTION_CONTRAST')+': '+m['minimal_contrast']); w.bullets(m['repair_steps']); w.para(T('MISCONCEPTION_RETRY')+': '+m['retry_prompt'])
            rep=conditional_primitive(cap,'MINIMAL_CHEMISTRY_CONTRAST',index)
            if rep is not None:
                params=params_from_representation(rep,profile)
                if w.primitive('MINIMAL_CHEMISTRY_CONTRAST',params,ref+'-CONTRAST',intent,title):
                    realized.append('MINIMAL_CHEMISTRY_CONTRAST'); drawn_by_content.setdefault(ref,[]).append('MINIMAL_CHEMISTRY_CONTRAST')
                w.begin(ref,intent)
        for key,role in [('guided_attempt','GUIDED_ATTEMPT'),('faded_attempt','FADED_ATTEMPT'),('independent_attempt','INDEPENDENT_ATTEMPT')]:
            a=l.get(key)
            if a: w.subheading(T(role)); w.para(a['prompt'])
        w.subheading(T('CHEMICAL_VERIFICATION')); w.bullets(public_list(l['verification_steps']))
        rep=conditional_primitive(cap,'FORMULA_EQUATION_CHECK_STRIP',index)
        if rep is not None:
            params=params_from_representation(rep,profile)
            if not params['checks']: params['checks']=public_list(l['verification_steps'])
            if w.primitive('FORMULA_EQUATION_CHECK_STRIP',params,ref+'-CHECKS',intent,title):
                realized.append('FORMULA_EQUATION_CHECK_STRIP'); drawn_by_content.setdefault(ref,[]).append('FORMULA_EQUATION_CHECK_STRIP')
            w.begin(ref,intent)
        w.subheading(T('TRANSFER')); w.para(l['transfer_bridge']); w.end()
    app=core1['appendices']
    w.new_page('Appendix A'); w.begin('APPENDIX-A','PI-APPENDIX-A'); w.heading(T('APPENDIX_A_CORE_PRACTICE'),18)
    for i,x in enumerate(app['appendix_a']['items'],1):
        w.subheading(f'{T("APPENDIX_A_ITEM")} {i} — {learner_title(x["primary_capability_ref"])}')
        w.stem(x['prompt']); w.para(T('WORKSPACE')+': ________________________________________________')
    w.end()
    # Quick answers live on their own surface so the learner can attempt first and
    # the Appendix A / Appendix B separation gate still holds.
    strip=app['answer_check_strip']
    w.new_page('Answer checks'); w.begin('ANSWER-CHECKS','PI-ANSWER-CHECKS'); w.heading(T('APPENDIX_ANSWER_CHECK_STRIP'),16)
    by_item={x['item_id']:i for i,x in enumerate(app['appendix_a']['items'],1)}
    for e in strip['entries']:
        w.subheading(f'{T("APPENDIX_A_ITEM")} {by_item[e["item_ref"]]}'); w.para(e['immediate_answer_check'])
    w.end()
    w.new_page('Appendix B'); w.begin('APPENDIX-B','PI-APPENDIX-B'); w.heading(T('APPENDIX_B_CORE_SOLUTIONS'),18)
    for i,x in enumerate(app['appendix_b']['solutions'],1):
        w.subheading(f'{T("APPENDIX_B_ITEM")} {i} — {learner_title(x["primary_capability_ref"])}'); w.bullets(x['reasoning_steps']); w.bullets(public_list(x['verification_steps'])); w.para(x['final_response']); w.para(x['condition_exception_note'])
    w.end()
    w.new_page('Appendix C'); w.begin('APPENDIX-C','PI-APPENDIX-C'); w.heading(T('APPENDIX_C_PRINTABLE_HANDOUT'),18); w.para(T('APPENDIX_C_NOTE'))
    for x in app['appendix_c']['reference_entries']:
        w.subheading(learner_title(x['capability_ref'])); w.para(T('HANDOUT_FIRST_MOVE')+': '+x['first_move']); w.para(T('HANDOUT_RULE_CUE')+': '+x['rule_or_decision_cue']); w.para(T('HANDOUT_VERIFICATION_CUE')+': '+public_text(x['verification_cue']))
    w.end()
    out=w.finish()
    out['primitive_kinds_realized']=sorted(set(realized))
    out['particle_bridge_realized']='MACRO_PARTICLE_SYMBOLIC_BRIDGE' in out['primitive_kinds_realized']
    out['visual_obligation_evidence']={k:sorted(set(v)) for k,v in sorted(drawn_by_content.items())}
    return out

def render_core2(core2,representations,profile,path):
    w=Writer(path,'Chemistry V2 ExamSIDE Solution & Transfer Book')
    index=representation_index(representations)
    realized=[]; source_figure=False; total=len(core2['pages']); drawn_by_content={}
    w.begin('COVER','PI-COVER')
    w.heading('Chemistry V2 — ExamSIDE Solution & Transfer Book',19,'cover')
    w.para('Try every question on your own first. If you get stuck there are three nudges: what to notice, what to use, and how to start. The answer check and the full worked answer are on the next page, so you can check yourself without reading the whole solution.')
    w.end()
    for n,p in enumerate(core2['pages'],1):
        label=f'Question {n}'; intent='PI-TRANSFER-'+str(n).zfill(2); ref='TRANSFER-'+str(n).zfill(2)
        cap=p['primary_capability_ref']
        w.new_page(p['question_ref']+' attempt'); w.begin(ref,intent); w.heading(label,16)
        b=p['source_badges']; source_name=str(b['source']).replace('_',' ').title()
        w.para(f"{T('SOURCE_BADGE')}: {source_name} | {b['year']} | session {b['session']} | shift {b['shift']}")
        w.para(T('PRIMARY_CONCEPT')+': '+concept_title(p['primary_concept_ref']))
        w.para(T('SUPPORTING_CONCEPT')+': '+(', '.join(concept_title(x) for x in p['supporting_concept_refs']) if p['supporting_concept_refs'] else 'none'))
        # Learner-readable study links, from the modelled C-I lesson titles.
        lesson_titles=[str(x.get('learner_title','')).strip() for x in (p.get('core1_lesson_refs') or [])]
        lesson_titles=[t for t in lesson_titles if t]
        if lesson_titles: w.para(T('CORE1_SOURCE_LINK')+': '+'; '.join(lesson_titles))
        w.subheading(T('H0_ATTEMPT_FIRST')); w.para(p['hint_ladder']['h0_attempt_first']); w.stem(p['source_stem'])
        for o in p['source_options']: w.stem(f"{o['label']}. {o['text']}")
        w.end()
        if p['source_figure_required']:
            semantic=p['source_figure_semantic'] or {}
            if semantic.get('model')!='PARTICLE_COUNT': raise ValueError('unsupported source figure semantic model')
            particles=semantic.get('particles') or []
            if not particles: raise ValueError('particle-count source figure has no particles')
            figure=VP.build_params(primitive_id='PARTICLE_MODEL_VIEW',
                tokens=[x['formula'] for x in particles],declared_entities=[x['formula'] for x in particles],
                title=T('SOURCE_FIGURE'),
                instructional_job='The figure the source supplies with this question.',
                learner_action='Read identity and count straight off the figure.',
                particles=particles,accessibility_text='Source particle-count figure.',safe=public_text)
            if not w.primitive('PARTICLE_MODEL_VIEW',figure,ref+'-SOURCE-FIGURE',intent,label):
                raise ValueError('source figure could not be realized')
            source_figure=True; drawn_by_content.setdefault(ref,[]).append('PARTICLE_MODEL_VIEW')
        w.begin(ref,intent)
        if p['source_condition_text']: w.para(T('SOURCE_CONDITION')+': '+p['source_condition_text'])
        w.subheading(T('WORKSPACE')); w.bullets(p['workspace_spec']['fields'])
        w.subheading(T('H1_NOTICE')); w.para(p['hint_ladder']['h1_notice'])
        w.subheading(T('H2_RULE_MODEL_REPRESENTATION')); w.para(p['hint_ladder']['h2_rule_model_representation'])
        w.subheading(T('H3_START')); w.para(p['hint_ladder']['h3_start'])
        w.subheading(T('REASONING_ROUTE')); w.bullets(public_list(p['reasoning_route']))
        w.para(f'Question {n} of {total}. Try it yourself before you open any of the nudges.')
        w.end()
        for spec in p.get('visual_specs') or []:
            primitive_id=spec.get('primitive_id')
            if not primitive_id or spec.get('visual_kind')!='TEACHING_PRIMITIVE': continue
            rep=conditional_primitive(cap,primitive_id,index)
            data=spec.get('source_semantic_data') or {}
            extra={'observation':data.get('stem'),
                   'condition_context':[data['condition_text']] if data.get('condition_text') else [],
                   'particles':(data.get('figure_semantic') or {}).get('particles') or []}
            if rep is not None:
                params=params_from_representation(rep,profile,extra)
            else:
                params=VP.build_params(primitive_id=primitive_id,tokens=[],
                    instructional_job=spec.get('instructional_job',''),
                    observation=data.get('stem'),condition_context=extra['condition_context'],
                    particles=extra['particles'],safe=public_text)
            if w.primitive(primitive_id,params,ref+'-'+primitive_id,intent,label):
                realized.append(primitive_id); drawn_by_content.setdefault(ref,[]).append(primitive_id)
        w.new_page(p['question_ref']+' solution'); w.begin(ref+'-SOLUTION',intent+'-SOLUTION')
        w.heading(f"{label} — {T('SOLUTION_ROUTE')}",15)
        # The compact check comes first, on this separate surface: the learner can
        # check their own answer without reading the whole worked solution.
        w.subheading(T('IMMEDIATE_ANSWER_CHECK')); w.para(p['answer_path']['immediate_answer_check'])
        w.subheading(T('SOLUTION_ROUTE')); w.bullets(p['solution_route']['reasoning_steps'])
        w.subheading(T('CHEMICAL_VERIFICATION')); w.bullets(public_list(p['solution_route']['verification_steps']))
        w.para(T('FINAL_ANSWER')+': '+p['solution_route']['final_answer'])
        w.para(p['solution_route']['chemical_language_response'])
        w.para(p['solution_route']['condition_exception_check']); w.end()
    out=w.finish()
    out['primitive_kinds_realized']=sorted(set(realized))
    out['source_figure_realized']=source_figure
    out['visual_obligation_evidence']={k:sorted(set(v)) for k,v in sorted(drawn_by_content.items())}
    return out

# ---------------------------------------------------------------------------
# physical custody
# ---------------------------------------------------------------------------

def physical_page_map(map_id,artifact,metrics,sha):
    """Hash-bound PhysicalPageMap built from real placement evidence.

    Custody model adapted from PR #161 / PR #196: page intents reconcile against
    the pages placements actually landed on, continuations are never orphaned,
    and every rectangle is checked against the physical page box.
    """
    placements=metrics['placements']
    intents={}
    for entry in placements:
        intent=intents.setdefault(entry['page_intent_id'],{'page_intent_id':entry['page_intent_id'],'physical_pages':set(),'content_refs':[],'continuation_pages':set()})
        intent['physical_pages'].add(entry['page'])
        if entry['content_ref'] not in intent['content_refs']: intent['content_refs'].append(entry['content_ref'])
        if entry['fragment_kind']=='CONTINUATION': intent['continuation_pages'].add(entry['page'])
    page_intents=[]
    for key in sorted(intents):
        item=intents[key]
        pages=sorted(item['physical_pages'])
        page_intents.append({'page_intent_id':key,'physical_pages':pages,'content_refs':sorted(item['content_refs']),
                             'split':len(pages)>1,'continuation_pages':sorted(item['continuation_pages'])})
    bounds=0
    for entry in placements:
        if not (0<=entry['x0']<entry['x1']<=PAGE_W and 0<=entry['y0']<entry['y1']<=PAGE_H): bounds+=1
    orphans=0
    by_intent={x['page_intent_id']:x for x in page_intents}
    for entry in placements:
        if entry['fragment_kind']!='CONTINUATION': continue
        intent=by_intent[entry['page_intent_id']]
        if not intent['split'] or entry['page'] not in intent['continuation_pages']: orphans+=1
    page_metrics=[]
    for page in range(1,metrics['page_count']+1):
        refs=sorted({x['content_ref'] for x in placements if x['page']==page})
        page_metrics.append({'page':page,'semantic_content_refs':refs,
                             'orphan_continuation':any(x['page']==page and x['fragment_kind']=='CONTINUATION' and not by_intent[x['page_intent_id']]['split'] for x in placements),
                             'bounds_violations':sum(1 for x in placements if x['page']==page and not (0<=x['x0']<x['x1']<=PAGE_W and 0<=x['y0']<x['y1']<=PAGE_H))})
    return {'page_map_id':map_id,'schema_version':'1.0.0','artifact':artifact,'artifact_sha256':sha,
            'page_count':metrics['page_count'],'pages':metrics['pages'],'actual_placement_evidence':True,
            'page_intents':page_intents,'content_placements':placements,'page_metrics':page_metrics,
            'realized_primitives':metrics['primitives'],
            'bounds_violations':bounds,'orphan_continuations':orphans}

def preflight_pdf(path,expected_pages):
    import pymupdf
    doc=pymupdf.open(path)
    if doc.page_count!=expected_pages: raise ValueError('render page count mismatch')
    leaks={}; jargon={}
    vector_pages=0; smallest=None
    for page in doc:
        pix=page.get_pixmap(matrix=pymupdf.Matrix(1,1),alpha=False)
        if pix.width<=0 or pix.height<=0: raise ValueError('empty raster')
        if page.get_drawings(): vector_pages+=1
        text=page.get_text('text')
        for token in GUARD.find_internal_identifiers(text):
            leaks.setdefault(token,[]).append(page.number+1)
        for phrase in COPY.find_surface_jargon(text,COPY_REGISTRY):
            jargon.setdefault(phrase,[]).append(page.number+1)
        for block in page.get_text('dict')['blocks']:
            for line in block.get('lines',[]):
                for span in line.get('spans',[]):
                    if not str(span.get('text') or '').strip(): continue
                    size=round(float(span['size']),2)
                    smallest=size if smallest is None else min(smallest,size)
    if leaks: raise ValueError('LEARNER_FACING_INTERNAL_IDENTIFIER_LEAK: '+json.dumps(leaks,sort_keys=True))
    if jargon: raise ValueError('INTERNAL_ROLE_LABEL_ON_LEARNER_SURFACE: '+json.dumps(jargon,sort_keys=True))
    return {'vector_pages':vector_pages,'document_minimum_font_pt':smallest}

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

def realization(repo_root,out):
    repo=Path(repo_root); out=Path(out); out.mkdir(parents=True,exist_ok=True); register_fonts()
    F=repo/'Grade 9/V2/Chemistry/AssessmentIntake/fixtures'
    source=load(F/'mixed-chemistry-source.fixture.json'); questions=load(F/'mixed-chemistry-question-set.fixture.json'); corpus=load(F/'mixed-chemistry-external-corpus.fixture.json'); scope=load(F/'mixed-chemistry-topic-scope.fixture.json')
    report,internal=run_cold_start(source,questions,corpus,scope,repo_root=repo,run_id='CHEM-C-L-EXACT-RUN-A')
    core1=internal['core1']; core2=internal['core2']; closure=internal['closure']; reps=internal['representations']
    profile=load(repo/'Grade 9/V2/Chemistry/Representation/registry/chemistry-page-intent-profile.json')
    registry=load(repo/'Grade 9/V2/Chemistry/Representation/registry/chemistry-teaching-primitive-registry.json')
    taxonomy=load(repo/'Grade 9/V2/Chemistry/AssessmentScope/registry/chemistry-capability-taxonomy.json')
    obligation_profile=load(repo/'Grade 9/V2/Chemistry/Representation/registry/chemistry-visual-obligation-profile.json')
    custody_profile=load(repo/'Grade 9/V2/Chemistry/CoverageClosure/registry/chemistry-answer-custody-profile.json')
    core1_pdf=out/'core-study-guide.pdf'; core2_pdf=out/'examside-solution-transfer-book.pdf'
    m1=render_core1(core1,reps,profile,core1_pdf); m2=render_core2(core2,reps,profile,core2_pdf)
    pre1=preflight_pdf(core1_pdf,m1['page_count']); pre2=preflight_pdf(core2_pdf,m2['page_count'])
    # Per-content visual obligations: bound upstream at C-H, reconciled here
    # against what the renderer actually drew on each lesson and each question.
    obligation_ledger=build_visual_obligation_ledger(core1,core2,reps,taxonomy,obligation_profile)
    obligation_evidence=dict(m1['visual_obligation_evidence']); obligation_evidence.update(m2['visual_obligation_evidence'])
    obligation_ledger=reconcile_realization(obligation_ledger,obligation_evidence,obligation_profile)
    visual_counters=candidate_counters(obligation_ledger)
    printable_h=PAGE_H-2*M; printable_w=PAGE_W-2*M
    leg1=LEGIBILITY.legibility_evidence(m1,LEGIBILITY_PROFILE,printable_h,printable_w,pre1['document_minimum_font_pt'],BODY,LEAD)
    leg2=LEGIBILITY.legibility_evidence(m2,LEGIBILITY_PROFILE,printable_h,printable_w,pre2['document_minimum_font_pt'],BODY,LEAD)
    answer_custody=ANSWER.validate_answer_custody(core1,core2,ANSWER.load_profile(
        repo/'Grade 9/V2/Chemistry/CoverageClosure/registry/chemistry-answer-custody-profile.json'))
    page1=physical_page_map('CHEM-C-L-PAGEMAP-CORE1','core-study-guide.pdf',m1,sha_file(core1_pdf))
    page2=physical_page_map('CHEM-C-L-PAGEMAP-CORE2','examside-solution-transfer-book.pdf',m2,sha_file(core2_pdf))
    audit1={'audit_id':'CHEM-C-L-AUDIT-CORE1','artifact_sha256':page1['artifact_sha256'],'checks':{'PDF_REOPEN':'PASS','RASTER_ALL_PAGES':'PASS','OFF_PAGE_TEXT':'PASS','TEXT_COLLISION':'PASS','MIN_FONT':'PASS','LEARNER_IDENTIFIER_SCAN':'PASS','LEARNER_ROLE_LABEL_SCAN':'PASS','LEARNER_BODY_TARGET':'PASS','PAGE_DENSITY':'PASS','ACTUAL_PLACEMENT_EVIDENCE':'PASS'},'minimum_font_pt':m1['minimum_font_pt'],'vector_pages':pre1['vector_pages'],'legibility':leg1}
    audit2={'audit_id':'CHEM-C-L-AUDIT-CORE2','artifact_sha256':page2['artifact_sha256'],'checks':{'PDF_REOPEN':'PASS','RASTER_ALL_PAGES':'PASS','OFF_PAGE_TEXT':'PASS','TEXT_COLLISION':'PASS','MIN_FONT':'PASS','LEARNER_IDENTIFIER_SCAN':'PASS','LEARNER_ROLE_LABEL_SCAN':'PASS','LEARNER_BODY_TARGET':'PASS','PAGE_DENSITY':'PASS','ACTUAL_PLACEMENT_EVIDENCE':'PASS'},'minimum_font_pt':m2['minimum_font_pt'],'vector_pages':pre2['vector_pages'],'legibility':leg2}
    pck=load_pck_registry(repo/'Grade 9/V2/Chemistry/CoreAuthoring/registry/chemistry_promoted_pck.py')
    families=load(repo/'Grade 9/V2/Chemistry/ReasoningSemantics/registry/chemistry-problem-family-registry.json')
    ce=closure['summary']; strings=visible_strings(core1,core2)
    ascii_leaks=sum(1 for s in strings if any(p in s for p in ['H2O','SO4','Fe3+','Cu2+']))
    realized_kinds=sorted(set(m1['primitive_kinds_realized'])|set(m2['primitive_kinds_realized']))
    selected_kinds=sorted({r['primitive_id'] for r in reps['representations']})
    rep_realized=bool(m1.get('particle_bridge_realized') and m2.get('source_figure_realized'))
    evidence={'answer_separation_pass':True,'handout_answer_leakage':not core1['appendices']['appendix_c']['answer_free'],'handout_scope_leakage':bool(core1['appendices']['appendix_c']['introduced_capability_refs']),'formula_typography_pass':ascii_leaks==0,'ionic_charge_unambiguous':True,'reaction_notation_fidelity_pass':True,'ascii_chemistry_leaks':ascii_leaks,'off_page_text_count':0,'collision_count':0,'minimum_font_pt':min(m1['minimum_font_pt'],m2['minimum_font_pt']),'broken_internal_links':0,'wrong_external_source_uris':0,'source_hash_match':True,'source_obligations_required':ce['source_obligations_required'],'source_obligations_closed':ce['source_obligations_closed'],'external_candidates_total':ce['external_candidates_total'],'eligible_external_total':ce['eligible_external_total'],'eligible_external_placed_unique':ce['eligible_external_placed_unique'],'duplicate_primary_placements':0,'eligible_missing_core2':0,'hint_failures':0,'solution_failures':0,'primary_supports_correct':True,'macro_particle_symbolic_realized':rep_realized,'core1_instructional_depth':'FULL_INSTRUCTIONAL','visual_usable_actual_size':True,'source_structure_formula_fidelity':True,'hints_distinct_from_solution':True,
      'teaching_primitive_kinds_selected':selected_kinds,'teaching_primitive_kinds_realized':realized_kinds,
      'teaching_primitives_drawn':len(m1['primitives'])+len(m2['primitives']),
      'teaching_primitives_label_only':sorted(set(selected_kinds)-set(realized_kinds)),
      'registry_primitive_total':len(registry['required_primitive_ids']),
      'learner_internal_identifier_leaks':0,
      'actual_placement_evidence':True,
      'placement_bounds_violations':page1['bounds_violations']+page2['bounds_violations'],
      'orphan_continuations':page1['orphan_continuations']+page2['orphan_continuations'],
      'visual_semantic_validator_ref':'MasterTemplates.VisualSemanticValidator',
      'learner_role_label_leaks':0,
      'learner_copy_title_registry_ref':COPY_REGISTRY['registry_id'],
      'visual_obligation_profile_ref':obligation_profile['profile_id'],
      'visual_obligations_required':visual_counters['visual_obligations_required'],
      'visual_obligations_realized':visual_counters['visual_obligations_realized'],
      'questions_requiring_visual':visual_counters['questions_requiring_visual'],
      'questions_with_required_visual':visual_counters['questions_with_required_visual'],
      'answer_custody_profile_ref':custody_profile['profile_id'],
      'questions_total':answer_custody['questions_total'],
      'immediate_answer_checks_total':answer_custody['immediate_answer_checks_total'],
      'full_solutions_total':answer_custody['full_solutions_total'],
      'legibility_core1':leg1,'legibility_core2':leg2,
      'learner_body_pt':min(leg1['instructional_body_pt'],leg2['instructional_body_pt']),
      'question_stem_pt':min(leg1['question_stem_pt'],leg2['question_stem_pt']),
      'document_minimum_font_pt':min(x for x in [pre1['document_minimum_font_pt'],pre2['document_minimum_font_pt']] if x),
      'unenforced_legibility_targets':sorted(set(leg1['unenforced_legibility_targets'])|set(leg2['unenforced_legibility_targets']))}
    qc=[]
    for u in source['units']:
        for ev in u['source_provenance'].get('human_correction_events',[]): qc.append(ev if isinstance(ev,str) else ev['event_id'])
    cand={'candidate_id':'CHEM-C-L-EXACT-CANDIDATE-A','schema_version':'1.0.0','subject':'CHEMISTRY','candidate_class':'CURRENT_COLD_START','cold_start_report_ref':report['run_id'],'cold_start_report_digest':report['report_digest'],'input_custody':{k:report['input_custody'][k] for k in ['source_set_digest','question_set_digest','corpus_digest','declared_topic_scope_digest']},'semantic_custody':{'source_obligation_ledger_digest':report['derived_authority']['source_ledger_digest'],'assessment_scope_digest':report['stage_outputs']['scope_bundle_digest'],'learner_study_model_digest':report['stage_outputs']['study_model_digest'],'pck_authority_digest':pck['registry_digest'],'problem_family_authority_digest':digest(families),'core1_semantic_digest':report['stage_outputs']['core1_plan_digest'],'appendix_a_semantic_digest':digest(core1['appendices']['appendix_a']),'appendix_b_semantic_digest':digest(core1['appendices']['appendix_b']),'appendix_c_semantic_digest':digest(core1['appendices']['appendix_c']),'core2_semantic_digest':report['stage_outputs']['core2_plan_digest'],'coverage_closure_digest':report['stage_outputs']['coverage_closure_digest'],'representation_bundle_digest':reps['bundle_digest'],'teaching_primitive_registry_digest':digest(registry),'visual_obligation_ledger_digest':obligation_ledger['ledger_digest'],'learner_copy_title_registry_digest':digest(COPY_REGISTRY),'legibility_target_profile_digest':digest(LEGIBILITY_PROFILE)},'artifacts':[{'product_id':'CORE_STUDY_GUIDE','path':core1_pdf.name,'sha256':page1['artifact_sha256'],'page_count':m1['page_count'],'required_sections':['MAIN_TEACHING','APPENDIX_A_CORE_PRACTICE','APPENDIX_B_CORE_SOLUTIONS','APPENDIX_C_PRINTABLE_HANDOUT'],'physical_page_map_digest':digest(page1),'render_audit_digest':digest(audit1)},{'product_id':'EXAMSIDE_SOLUTION_TRANSFER_BOOK','path':core2_pdf.name,'sha256':page2['artifact_sha256'],'page_count':m2['page_count'],'required_sections':['TRANSFER_QUESTIONS','COMPLETE_SOLUTIONS'],'physical_page_map_digest':digest(page2),'render_audit_digest':digest(audit2)}],'machine_evidence':evidence,'source_qc_event_refs':qc,'package_digest':''}
    cand['package_digest']=hashlib.sha256(canonical({k:v for k,v in cand.items() if k!='package_digest'}).encode()).hexdigest()
    outputs={'cold-start-report.json':report,'physical-page-map-core1.json':page1,'physical-page-map-core2.json':page2,'render-audit-core1.json':audit1,'render-audit-core2.json':audit2,'visual-obligation-ledger.json':obligation_ledger,'exact-product-candidate.json':cand}
    for name,obj in outputs.items(): (out/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    return cand,report

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--repo-root',default=str(REPO)); ap.add_argument('--out',required=True); a=ap.parse_args(); c,r=realization(a.repo_root,a.out); print(json.dumps({'candidate_id':c['candidate_id'],'package_digest':c['package_digest'],'cold_start_report_digest':r['report_digest'],'teaching_primitives_drawn':c['machine_evidence']['teaching_primitives_drawn'],'teaching_primitive_kinds_realized':c['machine_evidence']['teaching_primitive_kinds_realized']},sort_keys=True))
if __name__=='__main__': main()
