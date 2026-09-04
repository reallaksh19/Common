from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.units import mm
from reportlab.pdfbase.pdfmetrics import stringWidth
import fitz, os, hashlib, shutil

OUT_FRONT='/mnt/data/Algebra_3Day_Simple_Navigator_4pp.pdf'
SRC='/mnt/data/Algebra_IOQM_Grade9_Strong_Reference_Book_v3.pdf'
OUT='/mnt/data/Algebra_IOQM_Grade9_Reference_Book_Simple_3Day_v4.pdf'

# fonts
font_reg='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
font_bold='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
pdfmetrics.registerFont(TTFont('DV', font_reg))
pdfmetrics.registerFont(TTFont('DVB', font_bold))

W,H=A4
M=16*mm
NAVY=colors.HexColor('#18324B')
BLUE=colors.HexColor('#315F7D')
LIGHT=colors.HexColor('#EEF3F6')
LIGHT2=colors.HexColor('#F7F8F9')
MID=colors.HexColor('#D7E0E6')
TEXT=colors.HexColor('#1F2933')
MUTED=colors.HexColor('#53636F')
GREEN=colors.HexColor('#28784E')
YELLOW=colors.HexColor('#9A6A10')
RED=colors.HexColor('#A33A3A')

styles={
 'body': ParagraphStyle('body', fontName='DV', fontSize=9.1, leading=12, textColor=TEXT),
 'small': ParagraphStyle('small', fontName='DV', fontSize=7.9, leading=10.3, textColor=TEXT),
 'tiny': ParagraphStyle('tiny', fontName='DV', fontSize=7.1, leading=9.0, textColor=MUTED),
 'head': ParagraphStyle('head', fontName='DVB', fontSize=17, leading=20, textColor=NAVY),
 'subhead': ParagraphStyle('subhead', fontName='DVB', fontSize=11.2, leading=14, textColor=NAVY),
 'center': ParagraphStyle('center', fontName='DVB', fontSize=9, leading=11, textColor=NAVY, alignment=TA_CENTER),
}

def p(txt, style='body'):
    return Paragraph(txt, styles[style])

def header(c, title, page):
    c.setFillColor(NAVY)
    c.rect(0,H-12*mm,W,12*mm,fill=1,stroke=0)
    c.setFillColor(colors.white)
    c.setFont('DVB',9.2)
    c.drawString(M, H-7.8*mm, 'IOQM Grade 9 - Algebra | 3-Day Simple Navigator')
    c.setFont('DV',7.5)
    c.drawRightString(W-M, H-7.8*mm, f'{page} / 4')
    c.setFillColor(TEXT)
    c.setFont('DVB',17)
    c.drawString(M,H-23*mm,title)

def footer(c):
    c.setStrokeColor(MID); c.line(M,10*mm,W-M,10*mm)
    c.setFillColor(MUTED); c.setFont('DV',6.8)
    c.drawString(M,6.5*mm,'Use this navigator to decide where to go. The reference core teaches the mathematics.')

def draw_box(c,x,y,w,h,title,body,accent=BLUE):
    c.setFillColor(colors.white); c.setStrokeColor(MID); c.roundRect(x,y-h,w,h,3*mm,fill=1,stroke=1)
    c.setFillColor(accent); c.setFont('DVB',9.3); c.drawString(x+4*mm,y-6*mm,title)
    frame = Paragraph(body, styles['small'])
    frame.wrapOn(c,w-8*mm,h-14*mm); frame.drawOn(c,x+4*mm,y-h+4*mm)

c=canvas.Canvas(OUT_FRONT,pagesize=A4)
c.setTitle('Algebra 3-Day Simple Navigator - 4 Page Student Version')
c.setAuthor('OpenAI')

# PAGE 1
header(c,'Exam in 3 days? Start here.',1)
y=H-31*mm
c.setFillColor(TEXT); c.setFont('DVB',12.5); c.drawString(M,y,'Do not read this book from beginning to end.')
y-=7*mm
c.setFont('DV',9.5); c.drawString(M,y,'First find the topics where you get stuck. Then jump only to those parts of the guide.')
y-=12*mm
steps=[('1','QUICK CHECK','Find weak topics'),('2','FIX','Study only weak core skills'),('3','PRACTISE','Use H1 -> H2 -> H3 only if stuck'),('4','MIXED TEST','Try without hints')]
boxw=(W-2*M-9*mm)/4
for i,(n,t,b) in enumerate(steps):
    x=M+i*(boxw+3*mm)
    c.setFillColor(LIGHT); c.setStrokeColor(MID); c.roundRect(x,y-31*mm,boxw,31*mm,2.5*mm,fill=1,stroke=1)
    c.setFillColor(NAVY); c.circle(x+7*mm,y-7*mm,3.6*mm,fill=1,stroke=0)
    c.setFillColor(colors.white); c.setFont('DVB',8.5); c.drawCentredString(x+7*mm,y-8.1*mm,n)
    c.setFillColor(NAVY); c.setFont('DVB',8.3); c.drawString(x+4*mm,y-16*mm,t)
    para=p(b,'tiny'); para.wrapOn(c,boxw-8*mm,10*mm); para.drawOn(c,x+4*mm,y-28*mm)
y-=42*mm
c.setFillColor(NAVY); c.setFont('DVB',11.2); c.drawString(M,y,'Your 3-day plan')
y-=6*mm
rows=[
 [p('<b>DAY 1 - RECOGNIZE</b>','small'),p('Do the Quick Check. Learn only the weak high-value topics.','small')],
 [p('<b>DAY 2 - PRACTISE</b>','small'),p('Work on the important weak topics. Use hints only when needed.','small')],
 [p('<b>DAY 3 - MIX</b>','small'),p('Mixed questions, little or no help. No big new topic late in the day.','small')]
]
t=Table(rows,colWidths=[46*mm,120*mm],rowHeights=[15*mm]*3)
t.setStyle(TableStyle([
 ('BACKGROUND',(0,0),(0,-1),LIGHT),('BOX',(0,0),(-1,-1),0.5,MID),('INNERGRID',(0,0),(-1,-1),0.35,MID),
 ('VALIGN',(0,0),(-1,-1),'MIDDLE'),('LEFTPADDING',(0,0),(-1,-1),4*mm),('RIGHTPADDING',(0,0),(-1,-1),4*mm)
]))
t.wrapOn(c,W-2*M,45*mm); t.drawOn(c,M,y-45*mm)
y-=56*mm
c.setFillColor(LIGHT2); c.setStrokeColor(MID); c.roundRect(M,y-40*mm,W-2*M,40*mm,2.5*mm,fill=1,stroke=1)
c.setFillColor(NAVY); c.setFont('DVB',10.2); c.drawString(M+5*mm,y-7*mm,'Three rules')
rules=['Do not try to finish every question.','If a topic is already strong, move on.','Night before: review triggers and mistakes; do not start a major new method.']
for i,r in enumerate(rules):
    c.setFillColor(TEXT); c.setFont('DVB',8.5); c.drawString(M+6*mm,y-(15+i*8)*mm,'•')
    c.setFont('DV',8.7); c.drawString(M+11*mm,y-(15+i*8)*mm,r)
footer(c); c.showPage()

# PAGE 2 QUICK CHECK
header(c,'Quick Check - What would you try first?',2)
c.setFont('DV',8.8); c.setFillColor(MUTED)
c.drawString(M,H-31*mm,'Spend about 1-2 minutes on each. Do not fully solve. Mark:   [OK] knew the move   [?] unsure   [X] no idea')
items=[
('1','You know x+y and xy, and need x^2+y^2. What would you name first?'),
('2','The same product xyz appears in three nonlinear equations. What single variable would you set?'),
('3','A quadratic must not have two distinct real roots. What condition do you write first?'),
('4','A cubic has exactly two distinct real roots. What must the repeated root satisfy?'),
('5','P(m)=P(3) for an integer-coefficient cubic. What expression should you factor?'),
('6','The first three terms are in AP and the last three in GP. How would you represent the AP terms?'),
('7','A recurrence asks for a huge index. What should you search for before calculating many terms?'),
('8','An equation contains powers with a common exponential base. What substitution makes it polynomial?'),
('9','x+y+z is fixed and the target is a maximum/minimum. What structural idea should you test?'),
('10','A rational equation has poles in symmetric pairs around one midpoint. What shift should you try?')]
colw=(W-2*M-5*mm)/2
starty=H-43*mm
for i,(num,txt) in enumerate(items):
    col=0 if i<5 else 1; row=i if i<5 else i-5
    x=M+col*(colw+5*mm); top=starty-row*43*mm
    c.setFillColor(colors.white); c.setStrokeColor(MID); c.roundRect(x,top-38*mm,colw,37*mm,2.3*mm,fill=1,stroke=1)
    c.setFillColor(NAVY); c.setFont('DVB',9.3); c.drawString(x+4*mm,top-7*mm,f'T{num}')
    para=p(txt,'small'); para.wrapOn(c,colw-8*mm,20*mm); para.drawOn(c,x+4*mm,top-26*mm)
    c.setFillColor(MUTED); c.setFont('DV',7.6); c.drawString(x+4*mm,top-33*mm,'[ ] OK     [ ] ?     [ ] X')
footer(c); c.showPage()

# PAGE 3 STUDY MAP
header(c,'What should I study?',3)
c.setFillColor(TEXT); c.setFont('DV',9.1)
c.drawString(M,H-31*mm,'Use your Quick Check marks. Start with X, then ?. Skip OK topics except for a quick mixed retest.')
y=H-39*mm
map_rows=[
('T1','Sum-Product Trick','Symmetric two-variable systems','Q1, Q8, Q13'),
('T2','Common Product','Three-variable / cyclic systems','Q16, Q33'),
('T3','Root Test','Quadratics / discriminant','Q7'),
('T4','Repeated-Root Test','Polynomial root structure','Q11, Q42'),
('T5','Polynomial Difference','Factor theorem / integer roots','Q15'),
('T6','Mixed Progressions','AP / GP overlap','Q37, Q50'),
('T7','Recurrence Shortcut','Shift / period / pattern','Q24'),
('T8','Exponent Substitution','Indices / transformed roots','Q3'),
('T9','Extremum Method','Inequalities / smoothing','Q17, Q40, Q45'),
('T10','Symmetric Poles','Rational equations / midpoint shift','Q28')]
rows=[[p('<b>Weak check</b>','tiny'),p('<b>Go here first</b>','tiny'),p('<b>Core topic</b>','tiny'),p('<b>Practice</b>','tiny')]]
for r in map_rows:
    rows.append([p(r[0],'tiny'),p('<b>'+r[1]+'</b>','tiny'),p(r[2],'tiny'),p(r[3],'tiny')])
t=Table(rows,colWidths=[18*mm,45*mm,69*mm,35*mm],rowHeights=[9*mm]+[12*mm]*10)
t.setStyle(TableStyle([
 ('BACKGROUND',(0,0),(-1,0),NAVY),('TEXTCOLOR',(0,0),(-1,0),colors.white),
 ('BOX',(0,0),(-1,-1),0.55,MID),('INNERGRID',(0,0),(-1,-1),0.3,MID),
 ('VALIGN',(0,0),(-1,-1),'MIDDLE'),('LEFTPADDING',(0,0),(-1,-1),2.5*mm),('RIGHTPADDING',(0,0),(-1,-1),2*mm),
 ('BACKGROUND',(0,1),(-1,-1),colors.white)
]))
t.wrapOn(c,W-2*M,129*mm); t.drawOn(c,M,y-129*mm)
y-=140*mm
c.setFillColor(NAVY); c.setFont('DVB',10.5); c.drawString(M,y,'Simple priority')
y-=6*mm
priority=[('DO FIRST','Your X topics from the table above, especially symmetry, roots, polynomials, progressions, recurrences and extrema.',RED),
          ('DO NEXT','Your ? topics, then a few mixed questions.',YELLOW),
          ('ONLY IF TIME','Rare advanced methods, duplicate questions, and the unresolved Q29 wording.',MUTED)]
for label,desc,accent in priority:
    c.setFillColor(LIGHT2); c.setStrokeColor(MID); c.roundRect(M,y-15*mm,W-2*M,14*mm,2*mm,fill=1,stroke=1)
    c.setFillColor(accent); c.setFont('DVB',8.3); c.drawString(M+4*mm,y-7*mm,label)
    para=p(desc,'tiny'); para.wrapOn(c,130*mm,9*mm); para.drawOn(c,M+35*mm,y-12*mm)
    y-=18*mm
footer(c); c.showPage()

# PAGE 4 STUCK + 3 DAYS
header(c,'When you get stuck',4)
y=H-34*mm
rows=[
('I do not know what method applies.','Read H1 - Notice.'),
('I know the topic but forgot the method.','Read H2 - Recall.'),
('I know the method but cannot begin.','Read H3 - Start.'),
('I started correctly but got stuck halfway.','Open the linked worked example / Advanced Bridge.'),
('I got an answer but it is wrong.','Check domain, signs, branches, equality, convergence and integer restrictions.')]
for i,(a,b) in enumerate(rows):
    c.setFillColor(colors.white); c.setStrokeColor(MID); c.roundRect(M,y-22*mm,W-2*M,20*mm,2.2*mm,fill=1,stroke=1)
    c.setFillColor(NAVY); c.setFont('DVB',8.9); c.drawString(M+4*mm,y-7*mm,a)
    c.setFillColor(TEXT); c.setFont('DV',8.5); c.drawString(M+4*mm,y-15*mm,'-> '+b)
    y-=25*mm
c.setFillColor(NAVY); c.setFont('DVB',10.5); c.drawString(M,y,'Use less help each time')
y-=7*mm
c.setFillColor(LIGHT); c.setStrokeColor(MID); c.roundRect(M,y-25*mm,W-2*M,24*mm,2*mm,fill=1,stroke=1)
para=p('<b>First similar problem:</b> H1/H2/H3 if needed. &nbsp;&nbsp; <b>Next:</b> maximum H2. &nbsp;&nbsp; <b>Then:</b> H1 only. &nbsp;&nbsp; <b>Mixed test:</b> no hints.','small')
para.wrapOn(c,W-2*M-8*mm,18*mm); para.drawOn(c,M+4*mm,y-20*mm)
y-=34*mm
c.setFillColor(NAVY); c.setFont('DVB',10.5); c.drawString(M,y,'Day 1 / Day 2 / Day 3')
y-=6*mm
days=[
('DAY 1 - RECOGNIZE','Quick Check -> fix weak high-value topics -> one or two practice questions each.'),
('DAY 2 - PRACTISE','Return to the same important skills with different questions and less help.'),
('DAY 3 - MIX','Mixed questions without topic labels. Fix only repeated mistakes. No major new topic late in the day.')]
for title,body in days:
    c.setFillColor(LIGHT2); c.setStrokeColor(MID); c.roundRect(M,y-18*mm,W-2*M,17*mm,2*mm,fill=1,stroke=1)
    c.setFillColor(NAVY); c.setFont('DVB',8.6); c.drawString(M+4*mm,y-6.5*mm,title)
    para=p(body,'tiny'); para.wrapOn(c,130*mm,10*mm); para.drawOn(c,M+43*mm,y-14*mm)
    y-=21*mm
c.setFillColor(NAVY); c.setFont('DVB',10.5); c.drawString(M,y,'Night before - 30 minutes only')
y-=6*mm
c.setFillColor(LIGHT); c.setStrokeColor(MID); c.roundRect(M,y-27*mm,W-2*M,26*mm,2*mm,fill=1,stroke=1)
para=p('<b>Review:</b> method triggers, formulas you actually forget, your repeated mistakes, and the final legality checklist. <b>Do not start a difficult new method. Stop at a sensible time and sleep normally.</b>','small')
para.wrapOn(c,W-2*M-8*mm,20*mm); para.drawOn(c,M+4*mm,y-21*mm)
footer(c); c.showPage(); c.save()

# Build full book: 4 new pages + v3 pages 11..57 (0-based 10..56)
front=fitz.open(OUT_FRONT)
src=fitz.open(SRC)
out=fitz.open()
out.insert_pdf(front)
out.insert_pdf(src, from_page=10, to_page=src.page_count-1)
meta=src.metadata or {}
meta.update({'title':'IOQM Grade 9 - Algebra Reference Book v4 (Simple 3-Day Navigator)',
             'subject':'PR #140 Algebra reference core with simplified four-page 3-day navigator',
             'author':'OpenAI / study-guide build',
             'keywords':'IOQM, Grade 9, Algebra, Olympiad, study guide, 3-day navigator, hints'})
out.set_metadata(meta)
for i in range(4, out.page_count):
    page=out[i]
    page.draw_rect(fitz.Rect(0,0,W,20), color=(1,1,1), fill=(1,1,1), overlay=True)
    page.insert_text((M,12.5), 'IOQM Grade 9 - Algebra Reference Book v4', fontsize=6.8, fontname='helv', color=(0.10,0.20,0.30), overlay=True)
    page.insert_text((W-M-72,12.5), 'Reference Core', fontsize=6.8, fontname='helv', color=(0.32,0.39,0.44), overlay=True)
    page.draw_rect(fitz.Rect(0,H-29,W,H), color=(1,1,1), fill=(1,1,1), overlay=True)
    page.draw_line((M,H-19),(W-M,H-19), color=(0.84,0.88,0.90), width=0.4, overlay=True)
    pg=f'Page {i+1} of {out.page_count}'
    page.insert_text((W-M-55,H-8), pg, fontsize=6.5, fontname='helv', color=(0.32,0.39,0.44), overlay=True)

out.save(OUT, garbage=4, deflate=True, clean=True)
front.close(); src.close(); out.close()

for f in [OUT_FRONT, OUT]:
    h=hashlib.sha256(open(f,'rb').read()).hexdigest()
    print(f, os.path.getsize(f), h)
