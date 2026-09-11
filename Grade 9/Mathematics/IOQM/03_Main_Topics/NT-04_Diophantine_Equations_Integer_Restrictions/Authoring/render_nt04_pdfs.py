#!/usr/bin/env python3
from pathlib import Path
import html,re
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle,getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import BaseDocTemplate,Frame,PageTemplate,PageBreak,Paragraph,Spacer,Table,TableStyle,KeepTogether
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'PDFs'; OUT.mkdir(exist_ok=True)
TITLE='Diophantine Equations & Integer Restrictions'; SHORT='NT04'
STUDENT=OUT/f'{SHORT}_Student_Pack_v1.pdf'; TEACHER=OUT/f'{SHORT}_Teacher_Key_v1.pdf'
base=getSampleStyleSheet()
S={
 'title':ParagraphStyle('title',parent=base['Title'],fontName='Helvetica-Bold',fontSize=21,leading=25,textColor=colors.HexColor('#183153'),alignment=TA_CENTER,spaceAfter=12),
 'subtitle':ParagraphStyle('subtitle',parent=base['Normal'],fontName='Helvetica',fontSize=10.5,leading=15,textColor=colors.HexColor('#49627A'),alignment=TA_CENTER),
 'h1':ParagraphStyle('h1',parent=base['Heading1'],fontName='Helvetica-Bold',fontSize=15,leading=18,textColor=colors.HexColor('#183153'),spaceBefore=7,spaceAfter=6),
 'h2':ParagraphStyle('h2',parent=base['Heading2'],fontName='Helvetica-Bold',fontSize=12,leading=15,textColor=colors.HexColor('#176B87'),spaceBefore=6,spaceAfter=4),
 'h3':ParagraphStyle('h3',parent=base['Heading3'],fontName='Helvetica-Bold',fontSize=10,leading=13,textColor=colors.HexColor('#2D4356'),spaceBefore=4,spaceAfter=3),
 'body':ParagraphStyle('body',parent=base['BodyText'],fontName='Helvetica',fontSize=8.2,leading=10.7,textColor=colors.HexColor('#202A33'),spaceAfter=3.2),
 'bullet':ParagraphStyle('bullet',parent=base['BodyText'],fontName='Helvetica',fontSize=8.0,leading=10.4,leftIndent=10,firstLineIndent=-6,spaceAfter=2.3),
 'small':ParagraphStyle('small',parent=base['BodyText'],fontName='Helvetica',fontSize=7.0,leading=8.8,textColor=colors.HexColor('#425466')),
}
def ascii_math(t):
 repl={'→':'->','←':'<-','↔':'<->','⇒':'=>','⇔':'<=>','≡':' congruent to ','≤':'<=','≥':'>=','≠':'!=','±':'+/-','×':'x','·':'*','÷':'/','√':'sqrt','²':'^2','³':'^3','⁴':'^4','–':'-','—':'-','−':'-','’':"'",'‘':"'",'“':'"','”':'"','…':'...','∈':' in ','∤':' does-not-divide ','∣':' divides '}
 for a,b in repl.items(): t=t.replace(a,b)
 return t.encode('ascii','replace').decode('ascii')
def inline(t):
 t=html.escape(ascii_math(t.strip()))
 t=re.sub(r'`([^`]+)`',r"<font name='Helvetica-Bold'>\1</font>",t)
 t=re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',t)
 return t
def story(path):
 lines=path.read_text(encoding='utf-8').splitlines(); out=[]; para=[]; table=[]; code=False
 def fp():
  if para: out.append(Paragraph(inline(' '.join(para)),S['body'])); para.clear()
 def ft():
  if not table:return
  rows=[]
  for row in table:
   if all(set(c.strip())<={'-',':'} for c in row):continue
   rows.append([Paragraph(inline(c),S['small']) for c in row])
  if rows:
   n=max(len(r) for r in rows); w=(letter[0]-1.0*inch)/n
   t=Table(rows,colWidths=[w]*n,repeatRows=1,hAlign='LEFT')
   t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#E8F3F7')),('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('VALIGN',(0,0),(-1,-1),'TOP'),('GRID',(0,0),(-1,-1),0.3,colors.HexColor('#B7C9D6')),('LEFTPADDING',(0,0),(-1,-1),3),('RIGHTPADDING',(0,0),(-1,-1),3),('TOPPADDING',(0,0),(-1,-1),2.5),('BOTTOMPADDING',(0,0),(-1,-1),2.5)]))
   out.append(KeepTogether([t,Spacer(1,3)]))
  table.clear()
 for raw in lines:
  line=raw.rstrip()
  if line.startswith('```'): fp();ft();code=not code;continue
  if code: out.append(Paragraph(inline(line) or '&#160;',S['small']));continue
  if line.startswith('|') and line.endswith('|'): fp();table.append([x.strip() for x in line.strip('|').split('|')]);continue
  ft()
  if not line.strip():fp();continue
  m=re.match(r'^(#{1,3})\s+(.*)$',line)
  if m: fp();out.append(Paragraph(inline(m.group(2)),S['h'+str(len(m.group(1)))]));continue
  if re.match(r'^[-*]\s+',line): fp();out.append(Paragraph('- '+inline(re.sub(r'^[-*]\s+','',line)),S['bullet']));continue
  if re.match(r'^\d+[.)]\s+',line): fp();out.append(Paragraph(inline(line),S['bullet']));continue
  if line.startswith('---'):fp();out.append(Spacer(1,4));continue
  para.append(line)
 fp();ft();return out
def footer(c,d):
 c.saveState();c.setStrokeColor(colors.HexColor('#D6E1E8'));c.line(.5*inch,.45*inch,letter[0]-.5*inch,.45*inch);c.setFont('Helvetica',7);c.setFillColor(colors.HexColor('#607789'));c.drawString(.5*inch,.27*inch,'IOQM Grade 9 | '+TITLE);c.drawRightString(letter[0]-.5*inch,.27*inch,f'Page {d.page}');c.restoreState()
def dc(*a,**kw): kw['invariant']=1;kw['pageCompression']=1;return Canvas(*a,**kw)
def build(path,title,subtitle,sources):
 doc=BaseDocTemplate(str(path),pagesize=letter,leftMargin=.5*inch,rightMargin=.5*inch,topMargin=.45*inch,bottomMargin=.55*inch,title=title,author='IOQM Grade 9')
 fr=Frame(doc.leftMargin,doc.bottomMargin,doc.width,doc.height,id='n');doc.addPageTemplates(PageTemplate(id='m',frames=fr,onPage=footer))
 st=[Spacer(1,1.3*inch),Paragraph(title,S['title']),Paragraph(subtitle,S['subtitle']),Spacer(1,.55*inch),Paragraph('RECONNECT -> DISCOVER -> MAKE SENSE -> TRY -> DIAGNOSE -> FADE -> ADOPT -> TRANSFER',S['subtitle']),PageBreak()]
 for i,s in enumerate(sources):
  if i:st.append(PageBreak())
  st.extend(story(ROOT/s))
 doc.build(st,canvasmaker=dc)
def main():
 build(STUDENT,TITLE,'Student Assimilation Pack | recognition, first move, check and transfer',['02_Assimilation_Book.md','03_First_Step_Reference.md','04_Recognition_and_First_Line_Lab.md','05_Practice_and_Transfer_Bank.md','06_H0_Mastery_Test.md'])
 build(TEACHER,TITLE+' - Teacher Diagnostic Key','Verified answers, source custody and diagnostic routes',['Teacher_Diagnostic_Key.md'])
if __name__=='__main__':main()
