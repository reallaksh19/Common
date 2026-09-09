#!/usr/bin/env python3
"""Render a schema-validated Physics model. Exact figures use data, never prompts."""
import argparse, json, math
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

ROOT = Path(__file__).resolve().parents[1]
W,H = landscape(A4)
NAVY='#17384E'; TEAL='#087E83'; BLUE='#276FA1'; RED='#AF4E36'; INK='#233743'; GREY='#546975'; PALE='#EAF5F3'
# Keyed off each hint's own tier (validate_v2.py enforces H1/H2/H3 order), not array position - see
# grade9-physics-publication/SKILL.md's hint-numbering note.
_HINT_LABEL={'H1':'H1 Notice','H2':'H2 Model','H3':'H3 Start'}
for name,file in [('Body','DejaVuSans.ttf'),('Bold','DejaVuSans-Bold.ttf'),('Italic','DejaVuSans-Oblique.ttf')]:
    pdfmetrics.registerFont(TTFont(name,str(ROOT/'assets/fonts'/file)))
pdfmetrics.registerFontFamily('Body',normal='Body',bold='Bold',italic='Italic',boldItalic='Bold')

class Book:
    def __init__(self, data, output):
        self.d=data
        # questions is bucketed anchors/core_calibrated/challenges (grade9-master.schema.json shape);
        # flatten once here since pagination/layout render them in one sequence regardless of bucket.
        qb=data['questions'];self.all_questions=qb['anchors']+qb['core_calibrated']+qb['challenges']
        self.question_batches=self.batch_questions(self.all_questions)
        by_id={q['id']:q for q in self.all_questions}
        self.mixed_batches=[(test,self.batch_questions([by_id[qid] for qid in test['question_ids']])) for test in data.get('mixed_tests',[])]
        self.concept_titles={c['concept_id']:c['title'] for c in data['concepts']}
        self.c=canvas.Canvas(str(output),pagesize=(W,H),pageCompression=1)
        self.c.setTitle(data['title']);self.c.setAuthor('Physics learning materials')
        self.regions=[]; self.dest={}; self.links=[];self.external_links=[];self.page=0;self.planned={}
        self.c.setSubject(data['band']+' | '+data['edition']+' | original teaching examples')
    @staticmethod
    def batch_questions(questions):
        batches=[];current=[];used=0
        for q in questions:
            demand=2 if q.get('figure') or len(q['question'])>170 else 1
            if current and used+demand>2:batches.append(current);current=[];used=0
            current.append(q);used+=demand
            if used==2:batches.append(current);current=[];used=0
        if current:batches.append(current)
        return batches
    def text(self,text,x,y,w,size=12.0,leading=None,bold=False,color=INK,maxh=None):
        p=Paragraph(text,ParagraphStyle('p',fontName='Bold' if bold else 'Body',fontSize=size,leading=leading or size*1.32,textColor=colors.HexColor(color),spaceAfter=0))
        pw,ph=p.wrap(w,H)
        if maxh is not None and ph>maxh+0.1:raise ValueError(f'Page {self.page}: text needs {ph:.1f}, available {maxh}: {text[:90]}')
        if x<35 or x+w>W-34 or y<24 or y+ph>H-32:raise ValueError(f'Text outside safe bounds on {self.page}: {text[:70]} at {x,y,w,ph}')
        p.drawOn(self.c,x,H-y-ph); self.regions.append({'page':self.page,'kind':'text','box':[x,y,w,ph],'text':text,'size':size});return ph
    def label(self,text,x,y,size=10.5,color=GREY):
        tw=pdfmetrics.stringWidth(text,'Body',size)
        self.regions.append({'page':self.page,'kind':'label','box':[x,y,tw,size*1.15],'text':text,'size':size})
        self.c.setFont('Body',size);self.c.setFillColor(colors.HexColor(color));self.c.drawString(x,H-y-size,text)
    def line(self,x1,y1,x2,y2,color='#CCD9DE',width=1,dash=None):
        c=self.c;c.setStrokeColor(colors.HexColor(color));c.setLineWidth(width);c.setDash(dash or [])
        c.line(x1,H-y1,x2,H-y2);c.setDash([])
    def rect(self,x,y,w,h,fill,stroke=None):
        c=self.c;c.setFillColor(colors.HexColor(fill));c.setStrokeColor(colors.HexColor(stroke or fill));c.rect(x,H-y-h,w,h,fill=1,stroke=bool(stroke))
    def arrow(self,x1,y1,x2,y2,color=TEAL,width=2.3,dash=None):
        self.line(x1,y1,x2,y2,color,width,dash);a=math.atan2(y2-y1,x2-x1)
        for turn in [-0.45,0.45]:self.line(x2,y2,x2-8*math.cos(a+turn),y2-8*math.sin(a+turn),color,width)
    def anchor(self,id,y=100):
        if id in self.dest:raise ValueError('Duplicate anchor '+id)
        self.c.bookmarkPage(id,fit='Fit');self.dest[id]=self.page
    def link(self,label,target,x,y,w=160):
        label=label.rstrip(' →')+' · p. '+str(self.planned.get(target,'?'))
        self.text(label,x,y,w,10.5,color=TEAL,maxh=15)
        self.c.linkAbsolute(label,target,Rect=(x,H-y-16,x+w,H-y),thickness=0)
        self.links.append({'page':self.page,'target':target})
    def external_link(self,label,url,x,y,w,kind,object_id):
        self.text(label,x,y,w,10.5,color=TEAL,maxh=16)
        self.c.linkURL(url,(x,H-y-16,x+w,H-y),relative=0,thickness=0)
        self.external_links.append({'page':self.page,'url':url,'kind':kind,'object_id':object_id})
    def start(self,title,kicker,subtitle='',id=None):
        if self.page:self.c.showPage()
        self.page+=1
        self.rect(0,0,W,8,TEAL)
        self.text(kicker.upper(),40,26,750,10.5,bold=True,color=TEAL)
        self.text(title,40,49,760,23,bold=True,color=NAVY,maxh=33)
        if subtitle:self.text(subtitle,40,85,760,11.5,maxh=31)
        self.line(40,116,W-40,116)
        self.label('MOTION  •  '+self.d['learner_label'],40,H-27,9.5)
        self.label(str(self.page),W-60,H-27,9.5)
        if id:self.anchor(id);self.c.addOutlineEntry(title,id,level=0,closed=False)
    def citation(self,q,x,y,w,short=False):
        cite=q.get('source_citation')
        if not cite:return
        label='Source' if short else ('Adapted: ' if q['source_status']=='ADAPTED' else 'Source: ')+cite['title']
        self.external_link(label,cite['url'],x,y,w,'source',q['id'])
    def paragraphs(self,blocks,x,y,w,bottom=429):
        for b in blocks:
            role=b['role'];s=b['text']
            if role=='heading':size=14;col=TEAL;bold=True;gap=6
            elif role=='equation':size=17;col=NAVY;bold=True;gap=10
            else:size=12;col=INK;bold=False;gap=10
            h=self.text(s,x,y,w,size,bold=bold,color=col,maxh=bottom-y);y+=h+gap
        return y
    def figure(self,f,x,y,w,h,assessment=False):
        if f['status']!='FINAL':raise ValueError('Learner figure must be FINAL')
        if h<(95 if f['kind']=='numberline' else 110) or w<190:raise ValueError('Figure component too small')
        first=len(self.regions)
        self.regions.append({'page':self.page,'kind':'figure','id':f['id'],'box':[x,y,w,h]})
        kind=f['kind']
        if kind=='numberline':
            lo,hi=f['range'];px=lambda a:x+25+(a-lo)/(hi-lo)*(w-55)
            compact=h<190
            yy=y+h*(.55 if compact else .65)
            self.arrow(x+15,yy,x+w-12,yy,GREY,1)
            ticks=f.get('ticks',list(range(lo,hi+1)))
            for t in ticks:
                self.line(px(t),yy-4,px(t),yy+4,GREY)
                st=('+' if t>0 else '')+str(t);self.label(st,px(t)-pdfmetrics.stringWidth(st,'Body',10.5)/2,yy+8,10.5)
            self.label('position x (m)',x+18,y+h-(12 if compact else 18),10.5)
            if not compact:self.label('right / east is positive →',x+max(20,w-220),y+3,10.5)
            positions=f.get('positions',[])
            for i,(a,b) in enumerate(zip(positions,positions[1:])):
                ay=y+h*.21+i*h*.16;self.arrow(px(a),ay,px(b),ay,TEAL if i%2==0 else BLUE)
                if f.get('leg_labels'):
                    s=f['leg_labels'][i];tw=pdfmetrics.stringWidth(s,'Body',11);self.label(s,(px(a)+px(b)-tw)/2,ay-20,11,color=TEAL if i%2==0 else BLUE)
            if positions and f.get('show_endpoints',True):
                for a,s,dy in [(positions[0],'start',0),(positions[-1],'finish',0 if compact else 17)]:
                    self.line(px(a),yy-12,px(a),yy+5,INK,1.5)
                    self.label(s,px(a)-14,yy+26+dy,10.5)
            if f.get('displacement') and len(positions)>1 and positions[0]!=positions[-1]:
                ay=yy-24;self.arrow(px(positions[0]),ay,px(positions[-1]),ay,RED,2.4,dash=[6,3])
                self.label('displacement arrow (dashed)',x+30,y+h-39,10.5,RED)
        elif kind=='vt':
            tmin,tmax=f['trange'];vmin,vmax=f['vrange'];l=x+44;r=x+w-26;top=y+31;bot=y+h-39
            px=lambda t:l+(t-tmin)/(tmax-tmin)*(r-l)
            py=lambda v:bot-(v-vmin)/(vmax-vmin)*(bot-top)
            for t in f['tticks']:
                self.line(px(t),top,px(t),bot,'#DCE6E9',.5)
                self.label(str(t),px(t)-3,bot+8,10.5)
            for v in f['vticks']:
                self.line(l,py(v),r,py(v),'#DCE6E9',.5)
                st=('+' if v>0 else '')+str(v);self.label(st,l-31,py(v)-6,10.5)
            if f.get('shade') and not assessment:
                for t1,v1,t2,v2 in f['segments']:
                    p=self.c.beginPath();p.moveTo(px(t1),H-py(0));p.lineTo(px(t1),H-py(v1));p.lineTo(px(t2),H-py(v2));p.lineTo(px(t2),H-py(0));p.close()
                    self.c.setFillColor(colors.HexColor('#CDEAE6' if v1+v2>=0 else '#F5D9CE'));self.c.drawPath(p,fill=1,stroke=0)
            self.line(l,bot,l,top,GREY,1)
            self.line(l,py(0),r,py(0),GREY,1.3)
            for a,b,c,d in f['segments']:self.line(px(a),py(b),px(c),py(d),BLUE,2.6)
            for t,v,label in f.get('annotations',[]):self.label(label,px(t),py(v),10.5,INK)
            self.label('velocity v (m/s)',l-28,y+2,11,color=NAVY)
            self.label('time t (s)',r-68,bot+25,11,color=NAVY)
        elif kind=='tiles':
            cols,rows=f['cols'],f['rows'];cell=min((w-75)/cols,(h-75)/rows,55)
            bx=x+40;by=y+32
            for i in range(cols):
                for j in range(rows):self.rect(bx+i*cell,by+j*cell,cell,cell,'#DBF0EC',TEAL)
            for i in range(cols):self.label(str(i+1)+' s',bx+i*cell+10,by+rows*cell+9,10.5)
            self.label('Each column: '+str(rows)+' m travelled in 1 s',x+22,y+h-24,11,color=TEAL)
            self.label('Each cell represents 1 m',x+22,y+2,11)
        elif kind=='compare':
            for i,child in enumerate(f['figures']):
                cell=h/len(f['figures']);self.label(child['title'],x+10,y+i*cell,11,color=TEAL)
                self.figure(child,x,y+17+i*cell,w,cell-20)
        elif kind=='blank':
            self.rect(x,y,w,h,'#FAFCFC','#D7E1E5')
            for yy in range(int(y+32),int(y+h-10),24):self.line(x+15,yy,x+w-15,yy,'#D7E1E5',.5)
            self.label(f['instruction'],x+12,y+6,10.5)
        else:raise ValueError('Unsupported figure kind: '+kind)
        for region in self.regions[first+1:]:
            rx,ry,rw,rh=region['box']
            if rx<x-.1 or ry<y-.1 or rx+rw>x+w+.1 or ry+rh>y+h+.1:
                raise ValueError(f'Figure {f["id"]} bounds escape: {region}')
    def lesson(self,p):
        self.start(p['title'],p['kicker'],p['intro'],p['id'])
        self.figure(p['figure'],40,139,430,253)
        self.text(p['caption'],48,402,414,11.5,color=GREY,maxh=40)
        self.paragraphs(p['blocks'],502,138,300,bottom=436)
        self.rect(40,457,W-80,74,PALE)
        self.text(p['takeaway'],54,469,W-108,12,bold=True,maxh=50)
        for i,target in enumerate(p.get('practice_ids',[])):
            self.link(('Check ' if target.startswith('solution-') else 'Try ')+target.split('-')[-1],target,40+i*180,539,170)
    def question_page(self,qs,idx,bank=False):
        title='Try these before looking at the hints' if bank else 'Appendix A · Questions'
        original=all(q['source_status']=='ORIGINAL' for q in self.all_questions)
        subtitle=('Original questions · ' if original else 'Source-linked practice · ')+'Use diagrams and explain your reasoning.' if bank else 'Use the diagrams you need. A correct number needs a physical explanation.'
        self.start(title,f'Practice set {idx} / {len(self.question_batches)}',subtitle,f'questions-{idx}')
        for j,q in enumerate(qs):
            y=134+j*200;self.anchor(q['id'],y)
            self.text(f"{q['label']}  ·  {q['task_type']}",40,y,730,13,bold=True,color=TEAL)
            self.text(q['question'],40,y+25,410,12,maxh=100)
            if q.get('figure'):self.figure(q['figure'],476,y+12,320,155,assessment=True)
            else:
                self.text(q['workspace'].replace('\n','<br/>'),486,y+24,297,10.5,color=GREY,maxh=58)
                for z in range(3):self.line(486,y+87+25*z,791,y+87+25*z,'#CBDADD',.7)
            self.link('Hints →','hint-'+q['id'],40,y+167,130)
            self.link('Solution →','solution-'+q['id'],191,y+167,170)
            self.citation(q,40,y+143,410)
            if j==0:self.line(40,y+192,W-40,y+192)
    def mixed_test_pages(self):
        for test,batches in self.mixed_batches:
            for page_index,questions in enumerate(batches,1):
                anchor=f"mixed-{test['set_id']}-{page_index}"
                self.start('Mixed transfer · Concepts hidden',f"{test['set_id']} · set {page_index} / {len(batches)}",'Work from the physical situation. Concept and task labels appear only after marking.',anchor)
                positions={qid:i+1 for i,qid in enumerate(test['question_ids'])}
                for row,q in enumerate(questions):
                    y=134+row*200
                    self.text(f"Question {positions[q['id']]}",40,y,730,13,bold=True,color=TEAL)
                    self.text(q['question'],40,y+25,410,12,maxh=100)
                    if q.get('figure'):self.figure(q['figure'],476,y+12,320,155,assessment=True)
                    else:
                        self.text(q['workspace'].replace('\n','<br/>'),486,y+24,297,10.5,color=GREY,maxh=58)
                        for z in range(3):self.line(486,y+87+25*z,791,y+87+25*z,'#CBDADD',.7)
                    self.link('Check later →','solution-'+q['id'],40,y+167,150)
                    if row==0:self.line(40,y+192,W-40,y+192)
    def handout(self):
        self.start('Appendix B · Keep the picture, rebuild the rule','One-page handout','Right is positive. Cover the words and explain each diagram aloud.', 'handout')
        self.text('1  Distance and displacement',40,132,365,15,bold=True,color=TEAL)
        self.text('2  Reading a velocity–time graph',445,132,355,15,bold=True,color=TEAL)
        self.figure(self.d['handout']['route'],40,163,360,150)
        self.figure(self.d['handout']['graph'],438,163,360,150)
        self.paragraphs(self.d['handout']['left'],40,330,360,bottom=528)
        self.paragraphs(self.d['handout']['right'],445,330,353,bottom=528)
    def hint_pages(self):
        for k in range(0,len(self.all_questions),4):
            self.start('Hints · Read one step, then try again','Optional help','Cover the rows below the hint you are reading.',f'hints-{k//4+1}')
            for i,q in enumerate(self.all_questions[k:k+4]):
                y=133+i*99;self.anchor('hint-'+q['id'],y)
                self.text(q['label'],40,y,48,12,bold=True,color=TEAL)
                for j,hint in enumerate(q['hints']):
                    tag=_HINT_LABEL[hint['tier']]
                    self.text('<b>'+tag+'</b>  '+hint['text'],98,y+j*24,640,11.5,maxh=23)
                self.link('Return →',q['id'],687,y+73,106)
                if i<3:self.line(40,y+94,W-40,y+94)
    def solution_pages(self):
        for k in range(0,len(self.all_questions),2):
            self.start('Solutions · Compare the reasoning, not just the number','Answers at the end','If a step surprised you, revisit the linked lesson and explain its picture.',f'solutions-{k//2+1}')
            for i,q in enumerate(self.all_questions[k:k+2]):
                y=132+i*201;self.anchor('solution-'+q['id'],y)
                self.text('QUESTION RECAP · '+q['label']+'  '+q['recap'],40,y,751,11.5,bold=True,maxh=32)
                blocks=[{'role':'body','text':'<b>WHY THIS WORKS.</b> '+q['solution']['why']},{'role':'body','text':'<b>METHOD.</b> '+q['solution']['method']},{'role':'body','text':'<b>ANSWER / CHECK.</b> '+q['solution']['answer']},{'role':'body','text':'<b>CONCEPT TO KEEP.</b> '+q['solution']['keep']}]
                sf=q.get('solution_figure') or q.get('figure')
                width=438 if sf else 752
                # Solutions have a distinct measured, compact rhythm; body remains 11.5 pt.
                yy=y+37
                for b in blocks:
                    h=self.text(b['text'],40,yy,width,11.5,leading=14.3,maxh=y+173-yy);yy+=h+4
                if sf:self.figure(sf,511,y+36,280,155,assessment=True)
                self.link('Return to '+q['label'],q['id'],40,y+176,135)
                if q['repair_mode']=='LOCAL_LESSON':self.link('Lesson →',q['repair_target'],200,y+176,167)
                elif q['repair_mode']=='EXTERNAL_COMPANION':
                    ref=q['repair_reference'];self.external_link('Core repair · '+ref['locator'],ref['url'],200,y+176,190,'repair',q['id'])
                self.citation(q,405,y+176,78,short=True)
                if i==0:self.line(40,y+197,W-40,y+197)
    def mixed_diagnosis_pages(self):
        by_id={q['id']:q for q in self.all_questions}
        for test,_ in self.mixed_batches:
            self.start('Mixed transfer · Mark and diagnose',test['set_id'],'Reveal this page only after completing the mixed set.',f"diagnosis-{test['set_id']}")
            for index,qid in enumerate(test['question_ids']):
                q=by_id[qid];concept=self.concept_titles[test['diagnosis_map'][qid]];y=135+index*86
                self.text(f"Question {index+1} · {concept}",40,y,500,12,bold=True,color=TEAL)
                self.text('If this answer was weak, use the linked solution and its repair route before retrying.',40,y+24,610,11.5,maxh=34)
                self.link('Solution →','solution-'+qid,650,y+18,140)
    def guided_solutions(self):
        if not self.d.get('guided_solutions'):return
        self.start('Check the small steps','Solutions begin here','Use these pictures to repair a step before trying the complete problems.','guided-solutions')
        for i,g in enumerate(self.d['guided_solutions']):
            y=134+i*200;self.anchor('solution-'+g['id'])
            self.text(g['title'],40,y,750,14,bold=True,color=TEAL)
            self.text(g['text'],40,y+30,438,12,maxh=143)
            self.figure(g['figure'],511,y+24,280,144)
            self.link('Return →',g['id'],40,y+176,150)
            if i==0:self.line(40,y+197,W-40,y+197)
    def render(self):
        # Derive printable page references from the same deterministic pagination plan.
        n=0
        for p in self.d.get('lessons',[]):n+=1;self.planned[p['id']]=n
        for batch in self.question_batches:
            n+=1
            for q in batch:self.planned[q['id']]=n
        for test,batches in self.mixed_batches:
            for page_index,_ in enumerate(batches,1):
                n+=1;self.planned[f"mixed-{test['set_id']}-{page_index}"]=n
        if self.d['product'] in ('core','study_guide'):n+=1;self.planned['handout']=n
        for k in range(0,len(self.all_questions),4):
            n+=1
            for q in self.all_questions[k:k+4]:self.planned['hint-'+q['id']]=n
        if self.d.get('guided_solutions'):
            n+=1
            for g in self.d['guided_solutions']:self.planned['solution-'+g['id']]=n
        for k in range(0,len(self.all_questions),2):
            n+=1
            for q in self.all_questions[k:k+2]:self.planned['solution-'+q['id']]=n
        for test,_ in self.mixed_batches:n+=1;self.planned[f"diagnosis-{test['set_id']}"]=n
        for p in self.d.get('lessons',[]):self.lesson(p)
        for index,batch in enumerate(self.question_batches,1):self.question_page(batch,index,self.d['product'] in ('question_bank','transfer_book'))
        self.mixed_test_pages()
        if self.d['product'] in ('core','study_guide'):self.handout()
        self.hint_pages()
        self.guided_solutions()
        self.solution_pages()
        self.mixed_diagnosis_pages()
        missing=[r for r in self.links if r['target'] not in self.dest]
        if missing:raise ValueError(missing)
        assert all(self.dest[k]==v for k,v in self.planned.items()),'Printed page reference drift'
        self.c.save()
        return {'pages':self.page,'destinations':self.dest,'links':self.links,'external_links':self.external_links,'regions':self.regions}

def main():
    p=argparse.ArgumentParser();p.add_argument('model');p.add_argument('output');a=p.parse_args()
    data=json.loads(Path(a.model).read_text(encoding='utf-8'));from validate_v2 import validate;validate(data)
    result=Book(data,Path(a.output)).render();Path(a.output).with_suffix('.layout.json').write_text(json.dumps(result,indent=2),encoding='utf-8',newline='\n')
    print(f"Rendered {result['pages']} pages: {a.output}")
if __name__=='__main__':main()
