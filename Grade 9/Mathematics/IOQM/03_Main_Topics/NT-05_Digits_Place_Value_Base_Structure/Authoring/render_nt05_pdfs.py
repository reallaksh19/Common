from pathlib import Path
import html,re
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.pdfgen.canvas import Canvas
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'PDFs'
S0=getSampleStyleSheet()
S={
'title':ParagraphStyle('title',parent=S0['Title'],fontName='Helvetica-Bold',fontSize=20,leading=24,alignment=TA_CENTER,spaceAfter=10),
'h1':ParagraphStyle('h1',parent=S0['Heading1'],fontName='Helvetica-Bold',fontSize=15,leading=18,spaceBefore=6,spaceAfter=5),
'h2':ParagraphStyle('h2',parent=S0['Heading2'],fontName='Helvetica-Bold',fontSize=11.5,leading=14,spaceBefore=5,spaceAfter=3),
'body':ParagraphStyle('body',parent=S0['BodyText'],fontName='Helvetica',fontSize=8.4,leading=11,spaceAfter=3),
'bullet':ParagraphStyle('bullet',parent=S0['BodyText'],fontName='Helvetica',fontSize=8.2,leading=10.5,leftIndent=10,firstLineIndent=-7,spaceAfter=2),
'small':ParagraphStyle('small',parent=S0['BodyText'],fontName='Helvetica',fontSize=7.3,leading=9.2),
}
def inline(t):
 t=html.escape(t.strip()); t=re.sub(r'`([^`]+)`',r'<b>\1</b>',t); t=re.sub(r'\*\*([^*]+)\*\*',r'<b>\1</b>',t); return t
def story(path):
 out=[]; para=[]; table=[]
 def fp():
  if para: out.append(Paragraph(inline(' '.join(para)),S['body'])); para.clear()
 def ft():
  if not table:return
  rows=[]
  for row in table:
   if all(set(c.strip()) <= {'-',':'} for c in row): continue
   rows.append([Paragraph(inline(c),S['small']) for c in row])
  if rows:
   w=(letter[0]-72)/max(len(r) for r in rows); T=Table(rows,colWidths=[w]*max(len(r) for r in rows),repeatRows=1)
   T.setStyle(TableStyle([('GRID',(0,0),(-1,-1),.3,colors.grey),('BACKGROUND',(0,0),(-1,0),colors.whitesmoke),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),3),('RIGHTPADDING',(0,0),(-1,-1),3),('TOPPADDING',(0,0),(-1,-1),2),('BOTTOMPADDING',(0,0),(-1,-1),2)])); out.append(T); out.append(Spacer(1,4))
  table.clear()
 for raw in path.read_text().splitlines():
  line=raw.rstrip()
  if line.startswith('|') and line.endswith('|'): fp(); table.append([x.strip() for x in line.strip('|').split('|')]); continue
  ft()
  if not line.strip(): fp(); continue
  m=re.match(r'^(#{1,2})\s+(.*)',line)
  if m: fp(); out.append(Paragraph(inline(m.group(2)),S['h1' if len(m.group(1))==1 else 'h2']))
  elif re.match(r'^[-*]\s+',line): fp(); out.append(Paragraph('- '+inline(re.sub(r'^[-*]\s+','',line)),S['bullet']))
  elif re.match(r'^(\d+[.)]|[A-D]\.)\s+',line): fp(); out.append(Paragraph(inline(line),S['bullet']))
  else: para.append(line)
 fp(); ft(); return out
def footer(c,d):
 c.saveState(); c.setFont('Helvetica',7); c.setFillColor(colors.grey); c.drawString(36,22,'IOQM Grade 9 | Digits, Place Value & Base Structure'); c.drawRightString(letter[0]-36,22,f'Page {d.page}'); c.restoreState()
def canv(*a,**k): k['invariant']=1; return Canvas(*a,**k)
def build(path,title,files):
 doc=SimpleDocTemplate(str(path),pagesize=letter,leftMargin=36,rightMargin=36,topMargin=34,bottomMargin=34,title=title,author='IOQM Grade 9')
 flow=[Spacer(1,90),Paragraph(title,S['title']),Paragraph('Integrated learning and diagnostic pack',S['body']),PageBreak()]
 for i,f in enumerate(files):
  if i: flow.append(PageBreak())
  flow += story(ROOT/f)
 doc.build(flow,onFirstPage=footer,onLaterPages=footer,canvasmaker=canv)
 # Replace standard 4-byte binary marker in header with ASCII bytes, preserving offsets.
 b=path.read_bytes(); lines=b.split(b'\n',2)
 if len(lines)>=3 and lines[1].startswith(b'%') and any(x>=128 for x in lines[1]):
  marker=lines[1]; repl=b'%' + b'#'*(len(marker)-1); assert len(repl)==len(marker); path.write_bytes(lines[0]+b'\n'+repl+b'\n'+lines[2])
def main():
 OUT.mkdir(exist_ok=True)
 build(OUT/'NT05_Student_Pack_v1.pdf','Digits, Place Value & Base Structure',['02_Assimilation_Book.md','03_First_Step_Reference.md','04_Recognition_and_First_Line_Lab.md','05_Practice_and_Transfer_Bank.md','06_H0_Mastery_Test.md'])
 build(OUT/'NT05_Teacher_Key_v1.pdf','Digits, Place Value & Base Structure - Teacher Diagnostic Key',['Teacher_Diagnostic_Key.md'])
if __name__=='__main__': main()
