#!/usr/bin/env python3
"""Executable Pydantic schema plus physics/relationship checks. No self-attested PASS."""
import json,math,sys
from pathlib import Path
from typing import Literal,Optional
from pydantic import BaseModel,ConfigDict,Field,model_validator
class Strict(BaseModel):
    model_config=ConfigDict(extra='forbid')
class Block(Strict):
    role:Literal['heading','body','equation'];text:str=Field(min_length=1)
class Figure(Strict):
    id:str;kind:Literal['numberline','vt','tiles','compare','blank'];status:Literal['FINAL']
    range:Optional[list[float]]=None;positions:Optional[list[float]]=None;displacement:bool=False
    leg_labels:Optional[list[str]]=None;ticks:Optional[list[float]]=None
    show_endpoints:bool=True
    trange:Optional[list[float]]=None;vrange:Optional[list[float]]=None
    segments:Optional[list[list[float]]]=None;tticks:Optional[list[float]]=None;vticks:Optional[list[float]]=None
    shade:bool=False;annotations:Optional[list[list]]=None;cols:Optional[int]=None;rows:Optional[int]=None
    figures:Optional[list['Figure']]=None;title:Optional[str]=None;instruction:Optional[str]=None
    @model_validator(mode='after')
    def data_complete(self):
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
class Citation(Strict):
    title:str=Field(min_length=1,max_length=65)
    url:str
    locator:str=Field(min_length=1)
    verification:Literal['VERIFIED']
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
# source_status is the finer Physics/ExamSIDE-specific state already used across check_ledger.py and
# question-contract.md; provenance_class is the coarser grade9-master.schema.json enum every subject's
# tooling already reads. Kept in lockstep (not independently authorable) so they cannot drift.
_PROVENANCE_MAP={'ORIGINAL':'ORIGINAL_CALIBRATED','SOURCE_VERIFIED':'SECONDARY_VERIFIED_PYQ','ADAPTED':'RECONSTRUCTED_FROM_SCAN'}
class Question(Strict):
    id:str;label:str
    question:str=Field(min_length=15)  # named to match grade9-master.schema.json's question.question
    primary_concept_id:str;secondary_concept_ids:list[str]
    recap:str;solution:Solution;hints:list[str]=Field(min_length=3,max_length=3);repair_target:str
    figure:Optional[Figure]
    task_type:Literal['Apply','Explain','Connect','Transfer','Compare']
    difficulty:Optional[Difficulty]=None
    workspace:str
    source_status:Literal['ORIGINAL','SOURCE_VERIFIED','ADAPTED']
    provenance_class:Literal['USER_UPLOADED_ANCHOR','OFFICIAL_PYQ','SECONDARY_VERIFIED_PYQ','PUBLISHED_REFERENCE','ORIGINAL_CALIBRATED','RECONSTRUCTED_FROM_SCAN']
    answer:str=Field(min_length=3)  # mirrors solution.answer; validated equal below, not independently authored
    source_refs:list[str];numeric_check:Optional[dict]
    source_citation:Optional[Citation]=None
    solution_figure:Optional[Figure]=None
    @model_validator(mode='after')
    def master_schema_conformance(self):
        assert self.provenance_class==_PROVENANCE_MAP[self.source_status],'provenance_class must match source_status (grade9-master.schema.json conformance)'
        assert self.answer==self.solution.answer,'top-level answer must mirror solution.answer, not diverge from it'
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
class Concept(Strict):
    concept_id:str;title:str;claim:Optional[str]=None
    canonical_concept_id:str  # crosswalk to the chapter source authority (CB1..CB12 for Motion), checked below
    primary_anchor_ids:list[str]=Field(default_factory=list)
    prerequisites:list[str]=Field(default_factory=list)
    same_level_question_ids:list[str]=Field(default_factory=list)
    challenge_question_ids:list[str]=Field(default_factory=list)
    misconception_ids:list[str]=Field(default_factory=list)
    mastery_path:list[str]=Field(default_factory=list)
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
# Bucketed exactly like grade9-master.schema.json's questions object (anchors/core_calibrated/challenges)
# instead of a flat array, so a generic Grade 9 tool reading `model.questions.core_calibrated` etc. works
# unmodified across subjects. This pilot has no external anchors and no next-level appendix yet, so those
# two buckets are empty lists, not absent - the master schema requires all three keys present.
class Questions(Strict):
    anchors:list[Question];core_calibrated:list[Question];challenges:list[Question]
    def all(self):return self.anchors+self.core_calibrated+self.challenges
class Model(Strict):
    schema_version:Literal['2.0'];edition:str;title:str;band:Literal['B30','B80','B90'];learner_label:str
    product:Literal['core','question_bank'];status:Literal['FOR_USER_REVIEW','RELEASE_CANDIDATE']
    project:Project;grade_scope:dict;placement:dict;concepts:list[Concept];topic_ids:list[str];frozen_questions:int
    lessons:list[Lesson];questions:Questions;lesson_ids:list[str];sources:list[Source]
    misconceptions:list[Misconception]=Field(default_factory=list)
    mixed_tests:list[dict]=Field(default_factory=list)
    handout:Handout;source_claim:Optional[str]=None
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
    assert len(ids)==len(d['concepts']),'duplicate concept IDs'
    for c in d['concepts']:
        cc=c.get('canonical_concept_id')
        assert cc and isinstance(cc,str),f"concept {c['concept_id']} missing canonical_concept_id crosswalk"
    qbuckets=d['questions'];all_qs=qbuckets['anchors']+qbuckets['core_calibrated']+qbuckets['challenges']
    assert len(all_qs)==d['frozen_questions'] and len(all_qs)>=4,'question denominator changed'
    assert len({q['id'] for q in all_qs})==len(all_qs),'duplicate question IDs'
    assert d['lesson_ids']==[p['id'] for p in d['lessons']],'lesson identity mismatch'
    if d['product']=='core':
        assert d['lessons'] and d['handout'],'core requires lessons and Appendix B'
        assert {c for p in d['lessons'] for c in p['concept_ids']}==ids,'concept coverage'
        for p in d['lessons']:
            assert set(p['source_refs'])<=sources,'unknown lesson source'
    assert {q['primary_concept_id'] for q in all_qs}==ids,'assessment leaves primary concept untested'
    for q in all_qs:
        assert q['primary_concept_id'] in ids and set(q['secondary_concept_ids'])<=ids,'unknown concept'
        assert set(q['source_refs'])<=sources,'unknown question source'
        if q['source_status']!='ORIGINAL':
            cite=q.get('source_citation');assert cite and cite['verification']=='VERIFIED','external source unresolved'
            from urllib.parse import urlparse
            u=urlparse(cite['url']);assert u.scheme=='https' and u.netloc and not any(c.isspace() for c in cite['url']),'invalid source URL'
            if q['source_status']=='ADAPTED':assert cite.get('adaptation_note'),'adaptation must be explicit'
        if d['product']=='core':assert q['repair_target'] in d['lesson_ids'],'unresolved repair'
        assert len(set(q['hints']))==3,'repeated hints'
        assert q['solution']['method']!=q['solution']['answer'],'method duplicates answer'
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
    if sys.argv[1]=='--schema':print(json.dumps(Model.model_json_schema(),indent=2))
    else:print(json.dumps(validate(json.loads(Path(sys.argv[1]).read_text())),indent=2))
