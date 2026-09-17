from pathlib import Path
import re
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, KeepTogether
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT=Path(__file__).resolve().parents[1]
PDFS=ROOT/'PDFs'; PDFS.mkdir(exist_ok=True)
font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'; bold='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
if Path(font).exists():
    pdfmetrics.registerFont(TTFont('DV',font)); pdfmetrics.registerFont(TTFont('DVB',bold)); BODY='DV'; BOLD='DVB'
else: BODY='Helvetica'; BOLD='Helvetica-Bold'
styles=getSampleStyleSheet()
base=ParagraphStyle('Body',parent=styles['BodyText'],fontName=BODY,fontSize=8.4,leading=10.6,spaceAfter=3)
h1=ParagraphStyle('H1',parent=base,fontName=BOLD,fontSize=15,leading=18,spaceBefore=5,spaceAfter=8)
h2=ParagraphStyle('H2',parent=base,fontName=BOLD,fontSize=11.4,leading=14,spaceBefore=7,spaceAfter=4)
h3=ParagraphStyle('H3',parent=base,fontName=BOLD,fontSize=9.5,leading=12,spaceBefore=5,spaceAfter=3)
small=ParagraphStyle('Small',parent=base,fontSize=7.5,leading=9.2)
cover=ParagraphStyle('Cover',parent=h1,fontSize=22,leading=26,alignment=TA_CENTER,spaceAfter=14)
subtitle=ParagraphStyle('Sub',parent=base,fontSize=11,leading=14,alignment=TA_CENTER)

def esc(s):
    s=s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
    s=s.replace('**','').replace('`','')
    return s

def flow(paths,title):
    story=[Spacer(1,55*mm),Paragraph(esc(title),cover),Paragraph('Integrated Grade-9 learner pack',subtitle),PageBreak()]
    for fi,name in enumerate(paths):
        if fi: story.append(PageBreak())
        lines=(ROOT/name).read_text().splitlines(); i=0
        while i<len(lines):
            raw=lines[i].rstrip(); s=raw.strip()
            if not s: story.append(Spacer(1,2.4*mm)); i+=1; continue
            if s.startswith('```'):
                i+=1; block=[]
                while i<len(lines) and not lines[i].strip().startswith('```'):
                    block.append(lines[i]); i+=1
                story.append(Paragraph(esc(' / '.join(x.strip() for x in block if x.strip())),small)); i+=1; continue
            if s.startswith('|'):
                block=[]
                while i<len(lines) and lines[i].strip().startswith('|'):
                    row=lines[i].strip()
                    if not re.fullmatch(r'[| :\-]+',row): block.append(' | '.join(x.strip() for x in row.strip('|').split('|')))
                    i+=1
                for row in block: story.append(Paragraph(esc(row),small))
                continue
            if s.startswith('# '): story.append(Paragraph(esc(s[2:]),h1))
            elif s.startswith('## '): story.append(Paragraph(esc(s[3:]),h2))
            elif s.startswith('### '): story.append(Paragraph(esc(s[4:]),h3))
            elif s.startswith('> '): story.append(Paragraph(esc(s[2:]),ParagraphStyle('Quote',parent=base,leftIndent=6*mm,rightIndent=6*mm,fontName=BOLD)))
            elif re.match(r'^\d+\.\s',s): story.append(Paragraph(esc(s),base))
            elif s.startswith('- '): story.append(Paragraph(esc('• '+s[2:]),base))
            else: story.append(Paragraph(esc(s),base))
            i+=1
    return story

def footer(canvas,doc,label):
    canvas.saveState(); canvas.setFont(BODY,6.4); canvas.drawString(16*mm,8*mm,label); canvas.drawRightString(A4[0]-16*mm,8*mm,f'Page {doc.page}'); canvas.restoreState()

def build(out,paths,title,label):
    doc=SimpleDocTemplate(str(out),pagesize=A4,leftMargin=16*mm,rightMargin=16*mm,topMargin=15*mm,bottomMargin=14*mm,title=title,author='OpenAI-assisted curriculum production',pageCompression=1,invariant=1)
    story=flow(paths,title)
    doc.build(story,onFirstPage=lambda c,d:footer(c,d,label),onLaterPages=lambda c,d:footer(c,d,label))

build(PDFS/'COMB01_Student_Pack_v1.pdf',['02_Assimilation_Book.md','03_First_Step_Reference.md','04_Recognition_and_First_Line_Lab.md','05_Practice_and_Transfer_Bank.md','06_H0_Mastery_Test.md'],'Basic Counting, Restrictions & Inclusion-Exclusion','IOQM Grade 9 | Basic Counting')
build(PDFS/'COMB01_Teacher_Key_v1.pdf',['Teacher_Diagnostic_Key.md'],'Basic Counting - Teacher Diagnostic Key','IOQM Grade 9 | Teacher Diagnostic Key')
