#!/usr/bin/env python3
"""Executable Pydantic schema plus physics/relationship checks. No self-attested PASS."""
import hashlib,json,math,re,sys
from pathlib import Path
from typing import Literal,Optional
from pydantic import BaseModel,ConfigDict,Field,model_validator
def _words(s):return set(re.findall(r"[a-zA-Z]+",s.lower()))
class Strict(BaseModel):
    model_config=ConfigDict(extra='forbid')
class Block(Strict):
    role:Literal['heading','body','equation'];text:str=Field(min_length=1)
# `kind` selects this renderer's specific drawing implementation (still Motion-flavored: only 5 kinds have
# a working renderer). `dependency_class` classifies the SAME figure against question-contract.md's already
# subject-agnostic vocabulary, so a coverage auditor or another subject can reason about "does this need a
# GRAPH/DIAGRAM/TABLE" without knowing this renderer's specific kind names (finding H). Adding a new
# dependency_class value here does not add renderer support for it - see SKILL.md's crosswalk note.
_DEP_CLASS_FOR_KIND={'numberline':'NUMBER_LINE','vt':'GRAPH','tiles':'DIAGRAM','compare':'MIXED','blank':'NONE'}
class Figure(Strict):
    id:str;kind:Literal['numberline','vt','tiles','compare','blank'];status:Literal['FINAL']
    dependency_class:Literal['NONE','GRAPH','DIAGRAM','TABLE','TIMELINE','NUMBER_LINE','OPTION_FIGURES','STATEMENT_SET','MIXED']
    range:Optional[list[float]]=None;positions:Optional[list[float]]=None;displacement:bool=False
    leg_labels:Optional[list[str]]=None;ticks:Optional[list[float]]=None
    show_endpoints:bool=True
    trange:Optional[list[float]]=None;vrange:Optional[list[float]]=None
    segments:Optional[list[list[float]]]=None;tticks:Optional[list[float]]=None;vticks:Optional[list[float]]=None
    shade:bool=False;annotations:Optional[list[list]]=None;cols:Optional[int]=None;rows:Optional[int]=None
    figures:Optional[list['Figure']]=None;title:Optional[str]=None;instruction:Optional[str]=None
    @model_validator(mode='after')
    def data_complete(self):
        assert self.dependency_class==_DEP_CLASS_FOR_KIND[self.kind],f"dependency_class must be {_DEP_CLASS_FOR_KIND[self.kind]} for kind={self.kind}"
        if self.kind=='numberline':
            assert self.range and len(self.range)==2 and self.range[0]<self.range[1],'numberline range'
            assert self.positions is not None,'numberline positions required'
            assert all(self.range[0]<=p<=self.range[1] for p in self.positions),'position outside axis'
            if self.leg_labels:assert len(self.leg_labels)==len(self.positions)-1,'leg label count'
        if self.kind=='vt':
            assert self.trange and self.vrange and self.tticks is not None and self.vticks is not None and self.segments,'complete graph data required'
            assert self.trange[0]<self.trange[1] and self.vrange[0]<=0<self.vrange[1],'axis ranges'
            previous=None
            for s in self.segments:
                assert len(s)==4 and s[0]<s[2],'segment length/time'
                assert self.trange[0]<=s[0]<s[2]<=self.trange[1],'time out of bounds'
                assert self.vrange[0]<=min(s[1],s[3])<=max(s[1],s[3])<=self.vrange[1],'velocity out of bounds'
                assert previous is None or math.isclose(s[0],previous),'gaps or overlaps in graph'
                previous=s[2]
            assert self.segments[0][0]==self.trange[0] and self.segments[-1][2]==self.trange[1],'full interval represented'
        if self.kind=='tiles':assert self.cols and self.rows and self.cols>0 and self.rows>0,'tile dimensions'
        if self.kind=='compare':assert self.figures and len(self.figures)==2,'comparison needs two figures'
        if self.kind=='blank':assert self.instruction,'workspace purpose required'
        return self
class Lesson(Strict):
    id:str;title:str;kicker:str;intro:str;figure:Figure;caption:str
    blocks:list[Block]=Field(min_length=2);takeaway:str;concept_ids:list[str];source_refs:list[str]
    practice_ids:list[str]=Field(default_factory=list)
class Solution(Strict):
    why:str=Field(min_length=10);method:str=Field(min_length=10);answer:str=Field(min_length=3);keep:str=Field(min_length=10)
# tier is explicit data, not array position: render_v2.py keys its H1/H2/H3 label off tier, and
# grade9-physics-examside's reconcile.py matches ledger h1/h2/h3 by tier, not by list index (finding
# hint-numbering-unification). Still `"type":"array"` at the top level, so grade9-master.schema.json's
# question.hints={"type":"array"} conformance is unaffected - only the item shape gets richer.
class HintStep(Strict):
    tier:Literal['H1','H2','H3'];text:str=Field(min_length=1)
class Citation(Strict):
    title:str=Field(min_length=1,max_length=65)
    url:str
    locator:str=Field(min_length=1)
    verification:Literal['VERIFIED']
    source_document:str=Field(min_length=1)
    source_sha256:str=Field(pattern=r'^[0-9a-f]{64}$')
    source_page:int=Field(ge=1)
    raw_stem:str=Field(min_length=1)
    raw_answer:str=Field(min_length=1)
    values_units:list[str]
    options:list[str]
    figure_locator:Optional[str]=None
    figure_semantics:list[str]
    target_ids:list[str]=Field(min_length=1)
    adaptation_note:Optional[str]=None
# `difficulty` is the cognitive-profile vector (grade9 router rule 3 / grade9-physics difficulty vector),
# named to match question.difficulty in ../../../shared/grade9-master.schema.json (deliberately generic
# there: "Subject skills define the most useful dimensions" - grade9-workflow.md S6). No derived
# Easy/Medium/Hard badge: core-teaching.md explicitly forbids inventing mastery/exam-difficulty badges
# without empirical calibration.
class Difficulty(Strict):
    physical_model_selection:Optional[int]=None;conceptual_reasoning:Optional[int]=None
    representation_translation:Optional[int]=None;vector_spatial_reasoning:Optional[int]=None
    equation_construction:Optional[int]=None;experimental_data_reasoning:Optional[int]=None
    constraints_cases:Optional[int]=None
    @model_validator(mode='after')
    def dims_in_range(self):
        for k,v in self.__dict__.items():
            assert v is None or 0<=v<=10,f'{k} out of 0-10 range'
        return self
_EXTERNAL_PROVENANCE={'USER_UPLOADED_ANCHOR','OFFICIAL_PYQ','SECONDARY_VERIFIED_PYQ','PUBLISHED_REFERENCE','RECONSTRUCTED_FROM_SCAN'}
class RepairReference(Strict):
    title:str=Field(min_length=1);url:str;locator:str=Field(min_length=1)
class Question(Strict):
    id:str;label:str
    question:str=Field(min_length=15)  # named to match grade9-master.schema.json's question.question
    primary_concept_id:str;secondary_concept_ids:list[str]
    recap:str;solution:Solution;hints:list[HintStep]=Field(min_length=3,max_length=3)
    repair_mode:Literal['LOCAL_LESSON','EXTERNAL_COMPANION','SELF_CONTAINED'];repair_target:str
    repair_reference:Optional[RepairReference]=None
    figure:Optional[Figure]
    task_type:Literal['Apply','Explain','Connect','Transfer','Compare']
    difficulty:Optional[Difficulty]=None
    difficulty_source:Literal['AUTHOR_HEURISTIC','SOURCE_ANALYSIS','EXPERT_CALIBRATED','EMPIRICAL']
    workspace:str
    source_status:Literal['ORIGINAL','SOURCE_VERIFIED','ADAPTED']
    transcription_status:Optional[Literal['VERIFIED_TRANSCRIPTION','RECONSTRUCTED','QC_ALERT','SOURCE_UNRESOLVED']]=None
    provenance_class:Literal['USER_UPLOADED_ANCHOR','OFFICIAL_PYQ','SECONDARY_VERIFIED_PYQ','PUBLISHED_REFERENCE','ORIGINAL_CALIBRATED','RECONSTRUCTED_FROM_SCAN']
    answer:str=Field(min_length=3)  # mirrors solution.answer; validated equal below, not independently authored
    source_refs:list[str];numeric_check:Optional[dict]
    source_citation:Optional[Citation]=None
    solution_figure:Optional[Figure]=None
    @model_validator(mode='after')
    def master_schema_conformance(self):
        if self.source_status=='ORIGINAL':
            assert self.provenance_class=='ORIGINAL_CALIBRATED','original questions require ORIGINAL_CALIBRATED provenance'
            assert self.transcription_status is None,'original questions have no transcription state'
        else:
            assert self.provenance_class in _EXTERNAL_PROVENANCE,'external questions require independently grounded provenance'
            assert self.transcription_status in ('VERIFIED_TRANSCRIPTION','RECONSTRUCTED'),'published external questions require resolved transcription'
        assert self.answer==self.solution.answer,'top-level answer must mirror solution.answer, not diverge from it'
        assert [h.tier for h in self.hints]==['H1','H2','H3'],'hints must progress H1 (Notice) -> H2 (Model) -> H3 (Start), by tier not just position'
        return self
class GuidedSolution(Strict):
    id:str;title:str;text:str;figure:Figure
class Handout(Strict):
    route:Figure;graph:Figure;left:list[Block];right:list[Block]
# Concept/Source/Misconception/Project/QA field names and required keys match
# ../../../shared/grade9-master.schema.json exactly (additionalProperties:true there permits the
# Physics-specific extras alongside them: claim, canonical_concept_id, provenance_class detail, etc.) so a
# generic Grade 9 tool reading concepts[]/sources[]/misconceptions[]/project/qa works unmodified across
# subjects, per grade9-workflow.md S12: "generated from ... grade9-master.schema.json or a compatible
# extension."
# SRU-01..15 (grade9-physics/references/concept-book-see-realize-understand.md). Several dimensions -
# prediction_required, reconstruction_test, transfer_required - are genuine pedagogical judgment calls,
# not structural facts a schema can compute. Per this project's own no-self-attested-PASS convention
# (validate_v2.py's docstring), this type makes the gate machine-checkable and ready to record an
# independent reviewer's finding; it must not be pre-filled by whoever authored the content being judged.
# validate() below enforces that: any populated dimension requires `reviewer` to be set.
# Field -> rubric code (concept-book-see-realize-understand.md, which also carries the reverse mapping):
# SRU-01 no_naked_equation, SRU-02 every_symbol_speaks, SRU-03 every_term_has_origin,
# SRU-04 explains_unusual_mathematics, SRU-05 verbalize_before_calculating, SRU-06 prediction_required,
# SRU-07 misconception_confrontation, SRU-08 reconstruction_test, SRU-09 source_traceability,
# SRU-10 no_silent_source_repair, SRU-11 symbolic_depth, SRU-12 assumptions_stated,
# SRU-13 representation_translation, SRU-14 scaling_reasoning, SRU-15 transfer_required.
class SRUAcceptance(Strict):
    no_naked_equation:Optional[bool]=None;every_symbol_speaks:Optional[bool]=None
    every_term_has_origin:Optional[bool]=None;explains_unusual_mathematics:Optional[bool]=None
    verbalize_before_calculating:Optional[bool]=None;prediction_required:Optional[bool]=None
    misconception_confrontation:Optional[bool]=None;reconstruction_test:Optional[bool]=None
    source_traceability:Optional[bool]=None;no_silent_source_repair:Optional[bool]=None
    symbolic_depth:Optional[bool]=None;assumptions_stated:Optional[bool]=None
    representation_translation:Optional[bool]=None;scaling_reasoning:Optional[bool]=None
    transfer_required:Optional[bool]=None
    reviewer:Optional[str]=None;notes:Optional[str]=None
class Concept(Strict):
    concept_id:str;title:str;claim:Optional[str]=None
    canonical_concept_id:str  # crosswalk to the chapter source authority (CB1..CB12 for Motion), checked below
    primary_anchor_ids:list[str]=Field(default_factory=list)
    prerequisites:list[str]=Field(default_factory=list)
    same_level_question_ids:list[str]=Field(default_factory=list)
    challenge_question_ids:list[str]=Field(default_factory=list)
    misconception_ids:list[str]=Field(default_factory=list)
    mastery_path:list[str]=Field(default_factory=list)
    sru:Optional[SRUAcceptance]=None
class Source(Strict):
    source_id:str;title:str
    provenance_class:Literal['USER_UPLOADED_ANCHOR','OFFICIAL_PYQ','SECONDARY_VERIFIED_PYQ','PUBLISHED_REFERENCE','ORIGINAL_CALIBRATED','RECONSTRUCTED_FROM_SCAN']
    location:Optional[str]=None;notes:Optional[str]=None
class Misconception(Strict):
    id:str;wrong_model:str;observable_error:str;diagnostic_question:str
    repair_explanation:str;micro_example:str;transfer_check:str
class Project(Strict):
    grade:Literal[9]=9;subject:str;chapter:str
    target_level:Optional[str]=None;core_question_count:Optional[int]=None
    challenge_question_count:Optional[int]=None;version:Optional[str]=None
class QA(Strict):
    source_qc_complete:bool;answers_verified:bool;concept_links_verified:bool
    difficulty_checked:Optional[bool]=None;pdf_render_checked:Optional[bool]=None
    pdf_links_checked:Optional[bool]=None;notes:list[str]=Field(default_factory=list)
class CanonicalConceptRegistry(Strict):
    registry_id:str=Field(min_length=1);source_locator:str=Field(min_length=1)
    source_sha256:str=Field(pattern=r'^[0-9a-f]{64}$')
    allowed_ids:list[str]=Field(min_length=1)
class MixedTest(Strict):
    test_id:str=Field(min_length=1);set_id:str=Field(min_length=1)
    study_mode:Literal['MIXED_TRANSFER'];concept_hidden:Literal[True]
    question_ids:list[str]=Field(min_length=2);diagnosis_map:dict[str,str]
    @model_validator(mode='after')
    def stable_identity(self):
        assert self.test_id==self.set_id,'mixed test test_id/set_id identity drift'
        return self
# Bucketed exactly like grade9-master.schema.json's questions object (anchors/core_calibrated/challenges)
# instead of a flat array, so a generic Grade 9 tool reading `model.questions.core_calibrated` etc. works
# unmodified across subjects. This pilot has no external anchors and no next-level appendix yet, so those
# two buckets are empty lists, not absent - the master schema requires all three keys present.
class Questions(Strict):
    anchors:list[Question];core_calibrated:list[Question];challenges:list[Question]
    def all(self):return self.anchors+self.core_calibrated+self.challenges
# 'core' keeps the original merged Student-Core-with-Appendices shape (still valid: this is a profile
# choice, not a deprecation). 'study_guide'/'transfer_book' are the selectable split matching
# grade9-physics-subtopic-book-builder's STUDY_GUIDE + TRANSFER_BOOK product pair (finding E: Appendix
# A/B, hints and solutions were mandatory inside every Core book; audit/self-check content must be able
# to live outside the learner Core without being considered lost).
class Model(Strict):
    schema_version:Literal['2.0'];edition:str;title:str;band:Literal['B30','B80','B90'];learner_label:str
    product:Literal['core','question_bank','study_guide','transfer_book'];status:Literal['FOR_USER_REVIEW','RELEASE_CANDIDATE']
    project:Project;grade_scope:dict;placement:dict;concepts:list[Concept]
    canonical_concept_registry:CanonicalConceptRegistry;topic_ids:list[str];frozen_questions:int
    lessons:list[Lesson];questions:Questions;lesson_ids:list[str];sources:list[Source]
    misconceptions:list[Misconception]=Field(default_factory=list)
    mixed_tests:list[MixedTest]=Field(default_factory=list)
    handout:Optional[Handout]=None;source_claim:Optional[str]=None  # required only for core/study_guide, enforced in validate()
    guided_solutions:list[GuidedSolution]=Field(default_factory=list)
    qa:QA

def areas(segments):
    disp=distance=0.0
    for t1,v1,t2,v2 in segments:
        dt=t2-t1;disp+=dt*(v1+v2)/2
        if v1*v2<0:
            cut=dt*abs(v1)/(abs(v1)+abs(v2))
            distance+=abs(v1)*cut/2+abs(v2)*(dt-cut)/2
        else:distance+=dt*(abs(v1)+abs(v2))/2
    return distance,disp
def validate(d):
    Model.model_validate(d)
    ids={c['concept_id'] for c in d['concepts']};sources={s['source_id'] for s in d['sources']}
    canonical_ids=set(d['canonical_concept_registry']['allowed_ids'])
    assert len(canonical_ids)==len(d['canonical_concept_registry']['allowed_ids']),'duplicate canonical concept IDs'
    locator=d['canonical_concept_registry']['source_locator'].split('#',1)[0]
    repository_root=Path(__file__).resolve().parents[4]
    registry_path=(repository_root/locator).resolve()
    assert registry_path.is_relative_to(repository_root) and registry_path.is_file(),'canonical concept authority is missing or outside the repository'
    actual_registry_hash=hashlib.sha256(registry_path.read_bytes()).hexdigest()
    assert actual_registry_hash==d['canonical_concept_registry']['source_sha256'],'canonical concept authority hash drifted'
    source_text=registry_path.read_text(encoding='utf-8')
    concept_block=source_text.split('\nconcepts:\n',1)[1].split('\nquestions:\n',1)[0]
    authoritative_ids={match.group(1) for match in re.finditer(r'^  (CB\d+):',concept_block,re.MULTILINE)}
    assert canonical_ids==authoritative_ids,'declared canonical IDs do not match the chapter authority'
    assert len(ids)==len(d['concepts']),'duplicate concept IDs'
    for c in d['concepts']:
        cc=c.get('canonical_concept_id')
        assert cc in canonical_ids,f"concept {c['concept_id']} has unknown canonical_concept_id {cc!r}"
        sru=c.get('sru')
        if sru and any(v is not None for k,v in sru.items() if k not in('reviewer','notes')):
            assert sru.get('reviewer'),f"concept {c['concept_id']} has SRU dimensions set without a reviewer - cannot self-attest pedagogical acceptance"
    if d['status']=='RELEASE_CANDIDATE':
        required_qa=('source_qc_complete','answers_verified','concept_links_verified','difficulty_checked','pdf_render_checked','pdf_links_checked')
        assert all(d['qa'].get(k) is True for k in required_qa),'RELEASE_CANDIDATE requires every QA gate to PASS'
        for c in d['concepts']:
            sru=c.get('sru') or {}
            dimensions=[v for k,v in sru.items() if k not in ('reviewer','notes')]
            assert sru.get('reviewer') and len(dimensions)==15 and all(v is True for v in dimensions),f"concept {c['concept_id']} lacks complete independent SRU acceptance"
    # Product profile: 'core' keeps both components; 'study_guide'/'question_bank'/'transfer_book' select
    # one, so audit/self-check content can live in a separate document without being "lost" (finding E).
    has_lessons_component=d['product'] in ('core','study_guide')
    has_assessment_component=d['product'] in ('core','question_bank','transfer_book')
    qbuckets=d['questions'];all_qs=qbuckets['anchors']+qbuckets['core_calibrated']+qbuckets['challenges']
    assert len(all_qs)==d['frozen_questions'],'question denominator changed'
    assert not has_assessment_component or len(all_qs)>=4,'question_bank/transfer_book/core requires at least 4 questions'
    assert len({q['id'] for q in all_qs})==len(all_qs),'duplicate question IDs'
    all_qids={q['id'] for q in all_qs}
    for mt in d['mixed_tests']:
        # Concept-hidden mixed test (finding J / grade9-textbook-publisher's "learning mode vs testing
        # mode": mixed tests hide concept labels, then route errors back to exact concept IDs).
        assert set(mt['question_ids'])<=all_qids,f"mixed test {mt['set_id']} references an unknown question"
        assert len(mt['question_ids'])==len(set(mt['question_ids'])),f"mixed test {mt['set_id']} repeats a question"
        dm=mt.get('diagnosis_map') or {}
        assert set(dm.keys())==set(mt['question_ids']),f"mixed test {mt['set_id']} diagnosis_map must cover exactly its question_ids"
        assert set(dm.values())<=ids,f"mixed test {mt['set_id']} diagnosis_map points at an unknown concept"
        by_q={q['id']:q for q in all_qs}
        mismatched=[qid for qid in mt['question_ids'] if by_q[qid]['primary_concept_id']!=dm[qid]]
        assert not mismatched,f"mixed test {mt['set_id']} diagnosis_map disagrees with the question's actual primary_concept_id: {mismatched}"
    assert d['lesson_ids']==[p['id'] for p in d['lessons']],'lesson identity mismatch'
    if has_lessons_component:
        assert d['lessons'] and d.get('handout'),'core/study_guide requires lessons and Appendix B'
        assert {c for p in d['lessons'] for c in p['concept_ids']}==ids,'concept coverage'
        practice_targets=all_qids|{'solution-'+g['id'] for g in d.get('guided_solutions',[])}
        for p in d['lessons']:
            assert set(p['source_refs'])<=sources,'unknown lesson source'
            assert set(p.get('practice_ids',[]))<=practice_targets,f"lesson {p['id']} links a practice_id that resolves to no question or guided solution"
        for g in d.get('guided_solutions',[]):
            assert g['id'] in d['lesson_ids'],f"guided_solutions[{g['id']}] returns to a lesson this document doesn't own"
    else:
        assert not d['lessons'],'question_bank/transfer_book must not also carry lessons - keep the Core as the single lesson owner'
        assert not d.get('guided_solutions'),'question_bank/transfer_book must not carry guided_solutions - they return to lesson pages this document does not own'
    if has_assessment_component and all_qs:
        assert {q['primary_concept_id'] for q in all_qs}==ids,'assessment leaves primary concept untested'
    for q in all_qs:
        assert q['primary_concept_id'] in ids and set(q['secondary_concept_ids'])<=ids,'unknown concept'
        assert set(q['source_refs'])<=sources,'unknown question source'
        if q['source_status']!='ORIGINAL':
            cite=q.get('source_citation');assert cite and cite['verification']=='VERIFIED','external source unresolved'
            from urllib.parse import urlparse
            u=urlparse(cite['url']);assert u.scheme=='https' and u.netloc and not any(c.isspace() for c in cite['url']),'invalid source URL'
            assert q['id'] in cite['target_ids'],'source citation target_ids must include the published question'
            if q['source_status']=='SOURCE_VERIFIED':
                assert cite['raw_stem']==q['question'] and cite['raw_answer']==q['answer'],'verified source text/answer must be published without adaptation'
            if q['source_status']=='ADAPTED':assert cite.get('adaptation_note'),'adaptation must be explicit'
        else:
            assert not q.get('source_citation'),'original questions must not carry an external source citation'
        if q['repair_mode']=='LOCAL_LESSON':
            assert q['repair_target'] in d['lesson_ids'],'local repair target does not resolve'
        elif q['repair_mode']=='EXTERNAL_COMPANION':
            ref=q.get('repair_reference');assert ref,'external repair target requires a companion reference'
            from urllib.parse import urlparse
            u=urlparse(ref['url']);assert u.scheme=='https' and u.netloc,'invalid companion repair URL'
        else:
            assert q['repair_target']=='SELF_CONTAINED_SOLUTION','self-contained repair must use the canonical target'
        assert len({h['text'] for h in q['hints']})==3,'repeated hints'
        # Finding I: `method != answer` alone passes near-duplicates, formula-only routes and answer-copy-
        # with-a-word-changed. Require real word-overlap distance, a minimum route length, and at least
        # some vocabulary the answer doesn't already have (the method must teach the route, not restate it).
        mwords,awords=_words(q['solution']['method']),_words(q['solution']['answer'])
        overlap=len(mwords&awords)/max(1,len(mwords|awords))
        assert overlap<0.85,f"method near-duplicates answer (word overlap {overlap:.2f} >= 0.85)"
        assert len(mwords)>=6,'method too terse to teach a route, not just state the result'
        assert mwords-awords,'method contributes no vocabulary beyond the answer - looks formula-only/answer-copy'
        if 'graph shown' in q['question'] or 'Use the graph' in q['question']:assert q['figure'],'missing dependent graph'
        n=q.get('numeric_check')
        if n:
            if n['kind']=='route':
                ps=n['positions'];distance=sum(abs(b-a) for a,b in zip(ps,ps[1:]));disp=ps[-1]-ps[0]
            else:
                distance,disp=areas(n['segments'])
                if q['figure'] and q['figure']['kind']=='vt':assert q['figure']['segments']==n['segments'],'graph/answer data mismatch'
            assert math.isclose(distance,n['distance']) and math.isclose(disp,n['displacement']),'numeric answer mismatch'
    return {'schema':'Pydantic Model, extra fields forbidden','questions':len(all_qs),'numerically_recomputed':sum(bool(q['numeric_check']) for q in all_qs),'pedagogy':'MANUAL_REVIEW_REQUIRED'}
if __name__=='__main__':
    if sys.argv[1]=='--schema':
        schema=json.dumps(Model.model_json_schema(),indent=2)+'\n'
        if len(sys.argv)==3:Path(sys.argv[2]).write_text(schema,encoding='utf-8',newline='\n')
        else:print(schema,end='')
    else:print(json.dumps(validate(json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))),indent=2))
