from pathlib import Path
import re, hashlib
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, KeepTogether
ROOT=Path(__file__).resolve().parents[1]; PDFS=ROOT/'PDFs'; PDFS.mkdir(exist_ok=True)
styles=getSampleStyleSheet()
body=ParagraphStyle('Body',parent=styles['BodyText'],fontName='Helvetica',fontSize=9.2,leading=12,spaceAfter=4)
h1=ParagraphStyle('H1',parent=body,fontName='Helvetica-Bold',fontSize=16,leading=19,spaceBefore=6,spaceAfter=8)
h2=ParagraphStyle('H2',parent=body,fontName='Helvetica-Bold',fontSize=12,leading=15,spaceBefore=7,spaceAfter=4)
h3=ParagraphStyle('H3',parent=body,fontName='Helvetica-Bold',fontSize=10,leading=13,spaceBefore=5,spaceAfter=3)
cover=ParagraphStyle('Cover',parent=h1,fontSize=22,leading=26,alignment=TA_CENTER,spaceAfter=14)
sub=ParagraphStyle('Sub',parent=body,fontSize=11,leading=14,alignment=TA_CENTER)
small=ParagraphStyle('Small',parent=body,fontSize=7.6,leading=9.4)
def norm(s):
    repl={'→':'->','–':'-','—':'-','−':'-','×':'x','²':'^2','³':'^3','√':'sqrt','∠':'angle ','≤':'<=','≥':'>=','↔':'<->','△':'triangle ','“':'"','”':'"','’':"'"}
    for a,b in repl.items(): s=s.replace(a,b)
    return s
def esc(s):
    s=norm(s); s=s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
    s=s.replace('**','').replace('`','')
    return s
def story(files,title,subtitle):
    out=[Spacer(1,52*mm),Paragraph(esc(title),cover),Paragraph(esc(subtitle),sub),PageBreak()]
    for fi,f in enumerate(files):
        if fi: out.append(PageBreak())
        lines=(ROOT/f).read_text(encoding='utf-8').splitlines(); i=0
        while i<len(lines):
            s=lines[i].strip()
            if not s or s.startswith('<!--'): i+=1; continue
            if s.startswith('|'):
                while i<len(lines) and lines[i].strip().startswith('|'):
                    r=lines[i].strip(); i+=1
                    if re.fullmatch(r'[| :\-]+',r): continue
                    out.append(Paragraph(esc(' | '.join(x.strip() for x in r.strip('|').split('|'))),small))
                continue
            if s.startswith('# '): out.append(Paragraph(esc(s[2:]),h1))
            elif s.startswith('## '): out.append(Paragraph(esc(s[3:]),h2))
            elif s.startswith('### '): out.append(Paragraph(esc(s[4:]),h3))
            elif s.startswith('- '): out.append(Paragraph(esc('- '+s[2:]),body))
            else: out.append(Paragraph(esc(s),body))
            i+=1
    return out
def footer(c,d,label):
    c.saveState(); c.setFont('Helvetica',6.5); c.drawString(16*mm,8*mm,label); c.drawRightString(A4[0]-16*mm,8*mm,f'Page {d.page}'); c.restoreState()
def build(out,files,title,subtitle,label):
    path=PDFS/out
    doc=SimpleDocTemplate(str(path),pagesize=A4,leftMargin=16*mm,rightMargin=16*mm,topMargin=15*mm,bottomMargin=14*mm,title=title,author='IOQM Grade 9')
    doc.build(story(files,title,subtitle),onFirstPage=lambda c,d: footer(c,d,label),onLaterPages=lambda c,d: footer(c,d,label))
    # ReportLab writes a four-byte binary comment after the PDF header. Replace only
    # that comment with same-length ASCII so GitHub text-content transport preserves
    # the final artifact byte-for-byte; xref offsets and rendered content are unchanged.
    data=path.read_bytes()
    if data[9:15].startswith(b'%') and any(b > 127 for b in data[10:14]):
        data=data[:10]+b'ABCD'+data[14:]
        path.write_bytes(data)
build('GEO03_Student_Pack_v1.pdf',['02_Assimilation_Book.md','03_First_Step_Reference.md','04_Recognition_and_First_Line_Lab.md','05_Practice_and_Transfer_Bank.md','06_H0_Mastery_Test.md'],'Similarity, Ratio, Area & Centroid Structure','Integrated Grade-9 learner pack','IOQM Grade 9 | GEO-03')
build('GEO03_Teacher_Key_v1.pdf',['Teacher_Diagnostic_Key.md'],'GEO-03 Teacher Diagnostic Key','Teacher material - answers and diagnostics','IOQM Grade 9 | GEO-03 Teacher')
