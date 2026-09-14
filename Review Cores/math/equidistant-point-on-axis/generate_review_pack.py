#!/usr/bin/env python3
from pathlib import Path
import json, hashlib, sys, math
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, black, white
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.lib.units import mm

W,H=A4; M=18*mm
BLUE=HexColor('#17324D'); GRAY=HexColor('#65727E'); GRID=HexColor('#D6DEE5')
PALE=HexColor('#EEF5FA'); PALE2=HexColor('#F6F8FA'); GREEN=HexColor('#E9F5EE'); AMBER=HexColor('#FFF6DD'); RED=HexColor('#FDEEEE')
TOPIC='A point on an axis equidistant from two fixed points'

def wrap(t,size=9,maxw=470,font='Helvetica'):
    out=[]; cur=''
    for w in str(t).split():
        s=w if not cur else cur+' '+w
        if stringWidth(s,font,size)<=maxw: cur=s
        else:
            if cur: out.append(cur)
            cur=w
    if cur: out.append(cur)
    return out

def box(c,x,y,w,h,fill=PALE2):
    c.setFillColor(fill); c.setStrokeColor(GRID); c.roundRect(x,y,w,h,6,fill=1,stroke=1)

def header(c,kicker,title,sub,page):
    c.setFillColor(BLUE); c.setFont('Helvetica-Bold',8); c.drawString(M,H-M+2,kicker.upper())
    c.setFont('Helvetica-Bold',18); c.drawString(M,H-M-22,title)
    c.setFillColor(GRAY); c.setFont('Helvetica',9); y=H-M-38
    for line in wrap(sub,9,W-2*M): c.drawString(M,y,line); y-=11
    c.setStrokeColor(GRID); c.line(M,H-M-52,W-M,H-M-52)
    c.setFont('Helvetica',7); c.drawString(M,10*mm,'Mathematics V2 - six-core review fixture'); c.drawRightString(W-M,10*mm,str(page))

def cover(c,code,title,subtitle,bullets):
    c.setFillColor(BLUE); c.rect(0,H-78*mm,W,78*mm,fill=1,stroke=0)
    c.setFillColor(white); c.setFont('Helvetica-Bold',12); c.drawString(M,H-28*mm,code)
    c.setFont('Helvetica-Bold',23); c.drawString(M,H-42*mm,title)
    c.setFont('Helvetica',10); y=H-53*mm
    for line in wrap(subtitle,10,W-2*M): c.drawString(M,y,line); y-=13
    y=H-96*mm; c.setFillColor(BLUE); c.setFont('Helvetica-Bold',11); c.drawString(M,y,'This sample demonstrates:'); y-=19
    c.setFont('Helvetica',9.5)
    for b in bullets:
        c.setFillColor(BLUE); c.circle(M+3,y+3,2,fill=1,stroke=0); c.setFillColor(black)
        for line in wrap(b,9.5,W-2*M-15): c.drawString(M+13,y,line); y-=12
        y-=5
    box(c,M,33*mm,W-2*M,28*mm,PALE)
    c.setFillColor(BLUE); c.setFont('Helvetica-Bold',9.5); c.drawString(M+10,53*mm,'Sample topic')
    c.setFillColor(black); c.setFont('Helvetica',10); c.drawString(M+10,46*mm,TOPIC)
    c.setFillColor(GRAY); c.setFont('Helvetica',8); c.drawString(M+10,39*mm,'Generated review fixture - not an official exam source')
    c.showPage()

def graph(c,x,y,w,h,pts,xlim=(-3,8),ylim=(-1,6)):
    xmin,xmax=xlim; ymin,ymax=ylim
    sx=lambda v:x+(v-xmin)/(xmax-xmin)*w; sy=lambda v:y+(v-ymin)/(ymax-ymin)*h
    c.setFillColor(PALE2); c.setStrokeColor(GRID); c.rect(x,y,w,h,fill=1,stroke=1)
    c.setStrokeColor(HexColor('#E7ECEF')); c.setLineWidth(.4)
    for xv in range(math.ceil(xmin),math.floor(xmax)+1): c.line(sx(xv),y,sx(xv),y+h)
    for yv in range(math.ceil(ymin),math.floor(ymax)+1): c.line(x,sy(yv),x+w,sy(yv))
    c.setStrokeColor(GRAY); c.setLineWidth(.8); c.line(x,sy(0),x+w,sy(0)); c.line(sx(0),y,sx(0),y+h)
    for name,(px,py) in pts.items():
        c.setFillColor(HexColor('#A33B20') if name=='P' else BLUE); c.circle(sx(px),sy(py),3,fill=1,stroke=0)
        c.setFont('Helvetica-Bold',7); c.drawString(sx(px)+4,sy(py)+3,f'{name}({px:g},{py:g})')

def cards(c,rows,start_y,h=45):
    y=start_y
    for a,b in rows:
        box(c,M,y-h,W-2*M,h,PALE2); c.setFillColor(BLUE); c.setFont('Helvetica-Bold',8.5); c.drawString(M+9,y-14,a)
        c.setFillColor(black); c.setFont('Helvetica',8.5); yy=y-29
        for line in wrap(b,8.5,W-2*M-20): c.drawString(M+9,yy,line); yy-=10
        y-=h+8
    return y

def make_core1(p):
    c=canvas.Canvas(str(p),pagesize=A4)
    cover(c,'CORE1 - SEMANTIC / PCK AUTHORITY','Equidistant Point on an Axis','Core1 independently reconstructs the mathematics: object, dependencies, equation anatomy, representations, validity and misconception boundaries.',['The object is axis constraint + equal-distance locus, not a midpoint recipe.','Equation authority comes from PA=PB -> PA^2=PB^2.','The symmetry shortcut is a derived special case with a visible validity condition.','Core1 hands semantic claims downstream; it does not choose final learner pages.'])
    header(c,'Core1','1. Object, invariant and representation','What is mathematically true before pedagogy is designed?',2)
    graph(c,M,H-116*mm,W-2*M,62*mm,{'A':(1,2),'B':(5,2),'P':(3,0)},(-1,7),(-1,4))
    cards(c,[('K-CONCEPT','P is constrained to one axis; one coordinate is fixed.'),('K-INVARIANT','PA=PB, equivalently PA^2=PB^2 because distances are non-negative.'),('K-REPRESENTATION','x-axis -> P=(x,0); y-axis -> P=(0,y).')],H-130*mm,40)
    c.showPage()
    header(c,'Core1','2. Dependency + equation anatomy','No important equation is allowed to appear as a naked rule.',3)
    cards(c,[('PREREQUISITE','Ordered-pair and axis semantics.'),('PARENT LAW','d^2=(x2-x1)^2+(y2-y1)^2.'),('MODEL','(x-a)^2+b^2=(x-c)^2+d^2.'),('WHY LEGITIMATE','Squared distances preserve equality for non-negative distances.'),('INTERPRETATION','Solution is the axis point on the perpendicular-bisector locus.'),('CHECK','Substitute the final point and verify PA^2=PB^2.')],H-78*mm,46)
    c.showPage()
    header(c,'Core1','3. Validity + misconception boundaries','Shortcuts are admissible only when their structural condition is named.',4)
    cards(c,[('SPECIAL CASE','A=(a,b), B=(c,b), P=(x,0) -> common b^2 cancels -> x=(a+c)/2.'),('VALIDITY LIMIT','The x-midpoint shortcut is not general when A and B have different heights.'),('WRONG CHAIN','“P is on x-axis, so average x-coordinates.”'),('CORRECT CHAIN','Represent P -> compare squared distances -> simplify -> solve -> check.'),('REPRESENTATION RISK','A symmetry sketch may over-suggest midpoint use unless unequal-height contrast is also shown.')],H-78*mm,52)
    c.showPage(); c.save()

def make_core1a(p):
    c=canvas.Canvas(str(p),pagesize=A4)
    cover(c,'CORE1A - BUILD UNDERSTANDING','Learn the Idea','Core1A turns validated obligations into a teaching sequence. It is not forced into the Core1B open-ended/self-help pattern.',['See the object before symbols.','Bridge picture -> words -> coordinates -> equation.','Derive the shortcut condition.','Contrast the tempting wrong shortcut.','Move worked -> guided -> independent.'])
    header(c,'Core1A','1. See and represent','P can move only along the x-axis, so write P=(x,0).',2)
    graph(c,M,H-115*mm,W-2*M,60*mm,{'A':(1,2),'B':(5,2),'P':(3,0)},(-1,7),(-1,4))
    cards(c,[('WORDS -> SYMBOLS','“P lies on x-axis” becomes P=(x,0).'),('GEOMETRY -> EQUATION','PA=PB becomes (x-a)^2+b^2=(x-c)^2+d^2.'),('MEANING','The equation describes the same geometric constraint in an algebraic representation.')],H-128*mm,45)
    c.showPage()
    header(c,'Core1A','2. Derive, contrast, practise','The learner sees why the shortcut works before using it independently.',3)
    cards(c,[('DERIVATION','If A=(a,b), B=(c,b): vertical terms cancel, giving x=(a+c)/2.'),('CONTRAST','A=(-1,4), B=(7,2): P=(3,0) fails because PA^2=32 and PB^2=20.'),('GENERAL METHOD','(x+1)^2+16=(x-7)^2+4 -> x=9/4.'),('GUIDED','A=(0,5), B=(6,1), P on x-axis. Start P=(x,0). Check P=(1,0).'),('INDEPENDENT','A=(-4,3), B=(2,1), P on y-axis. Find P. Check P=(0,5).')],H-78*mm,52)
    c.showPage(); c.save()

HELP=[('SMALL CLUE','Which coordinate of P is fixed by the axis?'),('BIGGER CLUE','Use equality of squared distances.'),('HOW DO I START?','Write P=(x,0) or P=(0,y), then form PA^2=PB^2.')]
def qpage(c,num,title,prompt,answer,pts=None):
    header(c,'Core1B - open-ended self-guided',f'{num}. {title}','Attempt first. Use only as much help as needed. Detailed answer stays at the bottom.',num+1)
    y=H-78*mm; box(c,M,y-58,W-2*M,58,AMBER); c.setFillColor(BLUE); c.setFont('Helvetica-Bold',9); c.drawString(M+10,y-16,'TRY IT FIRST')
    c.setFillColor(black); c.setFont('Helvetica',9.5); yy=y-34
    for line in wrap(prompt,9.5,W-2*M-20): c.drawString(M+10,yy,line); yy-=12
    y-=74; c.setStrokeColor(GRID)
    for _ in range(8): c.line(M,y,W-M,y); y-=15
    for lab,txt in HELP:
        box(c,M,y-28,W-2*M,28,PALE2); c.setFillColor(BLUE); c.setFont('Helvetica-Bold',8); c.drawString(M+9,y-12,lab); c.setFillColor(black); c.setFont('Helvetica',8.2); c.drawString(M+95,y-12,txt); y-=34
    y0=19*mm; h=62*mm; box(c,M,y0,W-2*M,h,GREEN); c.setFillColor(BLUE); c.setFont('Helvetica-Bold',9); c.drawString(M+9,y0+h-15,'CHECK AFTER YOU TRY - DETAILED ANSWER')
    c.setFillColor(black); c.setFont('Helvetica',8.3); yy=y0+h-31; tw=(W-2*M)*(.58 if pts else 1)-18
    for line in wrap(answer,8.3,tw): c.drawString(M+9,yy,line); yy-=10
    if pts: graph(c,M+(W-2*M)*.63,y0+12,(W-2*M)*.33,38*mm,pts)
    c.showPage()

def make_core1b(p):
    c=canvas.Canvas(str(p),pagesize=A4)
    cover(c,'CORE1B - RECONSTRUCT + CONSOLIDATE','Open-Ended Self-Guided Workbook','Core1B stays close to taught mathematics while support fades. Every task begins open-ended and offers staged self-help plus a numeric/graphical bottom check.',['Open question before explanation.','Self-help: small clue -> bigger clue -> how do I start?','Detailed answer on the same page bottom.','No live branching and no learner-state claim.'])
    qpage(c,1,'Two methods','A=(1,2), B=(5,2). P lies on x-axis and PA=PB. Find P using symmetry and the general model.','P=(x,0). Symmetry gives x=(1+5)/2=3. General check: (x-1)^2+4=(x-5)^2+4 -> x=3. Therefore P=(3,0).',{'A':(1,2),'B':(5,2),'P':(3,0)})
    qpage(c,2,'Reject an unsafe shortcut','A=(-1,4), B=(7,2). A student claims P=(3,0) by averaging x-coordinates. Test the claim and find the real P.','At (3,0), PA^2=32 while PB^2=20, so the guess fails. Solve (x+1)^2+16=(x-7)^2+4 -> 16x=36 -> x=9/4. P=(9/4,0).',{'A':(-1,4),'B':(7,2),'P':(2.25,0)})
    qpage(c,3,'Axis changes','A=(2,-1), B=(2,7). P lies on y-axis and PA=PB. Find P and state what changed.','Now P=(0,y). 4+(y+1)^2=4+(y-7)^2 -> y=3. Therefore P=(0,3). The axis changed; the equal-distance invariant did not.',{'A':(2,-1),'B':(2,7),'P':(0,3)})
    c.save()

POOL=[
 ('EQ-D1','M0_DIRECT','P on x-axis, A=(-2,3), B=(4,3). Find P.','P=(1,0).'),
 ('EQ-R1','M2_REPRESENTATION_TRANSFER','A diagram gives A=(-1,4), B=(7,2), P on x-axis. Model and solve.','P=(9/4,0).'),
 ('EQ-I1','M3_INVERSE_TARGET','P=(3,0) is equidistant from A=(1,4) and B=(k,2). Find k.','k=-1 or 7.'),
 ('EQ-H1','M4_HIDDEN_STRUCTURE','Interpret (x+3)^2+16=(x-5)^2+4 geometrically and solve.','P=(1/4,0).'),
 ('EQ-M1','M5_METHOD_DISCRIMINATION','A=(1,5), B=(9,5), P on x-axis. Choose the efficient method and solve.','P=(5,0); symmetry is efficient.'),
 ('EQ-F1','M6_FAMILY_DISCRIMINATION','A gate on y=0 must be equally far from A=(2,4), B=(8,4). Choose the model and solve.','P=(5,0).')]

def make_core2(p):
    c=canvas.Canvas(str(p),pagesize=A4)
    cover(c,'CORE2 - ASSESSMENT INTELLIGENCE','Problem-Family Cognition','Core2 reconstructs what questions demand: cues, hidden state, first move, representation switch, wrong chain, checks, difficulty and transfer envelope.',['Surface wording is separated from problem family.','First non-obvious move is usually axis -> P=(x,0)/(0,y).','Difficulty rises through hidden cues, inverse targets and discrimination.','Core2 hands Core2A a transfer envelope, not a final workbook.'])
    header(c,'Core2','1. Cognitive anatomy','What does the question make the learner recognize and do?',2)
    cards(c,[('SURFACE WORDING','axis/equidistance wording, diagram, equation or context'),('RECOGNITION CUE','axis constraint + two fixed points + equal distance'),('HIDDEN STATE','one coordinate fixed, one unknown'),('FIRST NON-OBVIOUS MOVE','write P=(x,0) or P=(0,y)'),('REPRESENTATION SWITCH','geometry/context -> squared-distance equation'),('WRONG CHAIN','midpoint shortcut used without structural justification'),('CHECK','verify PA^2=PB^2')],H-78*mm,42)
    c.showPage()
    header(c,'Core2','2. Demand + transfer envelope','Safe variation changes the surface or target without importing new mathematics.',3)
    cards(c,[('M0 -> M2','direct -> controlled variation -> representation transfer'),('M3 -> M4','inverse target -> hidden structure'),('M5 -> M6','method discrimination -> family discrimination'),('SAFE','axis change; unequal heights; verbal/diagram/equation shift; inverse coordinate; method choice'),('CONDITIONAL','contextual family discrimination requires model-selection authority'),('FORBIDDEN WITHOUT NEW AUTHORITY','3D distance, new locus theorems, or other mathematics not in the validated boundary')],H-78*mm,48)
    c.showPage(); c.save()

def make_core2a(p):
    c=canvas.Canvas(str(p),pagesize=A4)
    cover(c,'CORE2A - GOVERN LEGAL TRANSFER SPACE','Legal Practice Pool - PRACTICE','Purpose is explicitly bound to PRACTICE for this review fixture. Core2A makes concrete items legal, answer-checked and provenance-safe.',['Items remain inside the validated capability/transfer boundary.','Every item has a canonical answer.','All items are PEDAGOGICALLY_GENERATED; no official source claim.','Core2B may select only legal IDs and only below its supplied ceiling.'])
    header(c,'Core2A','1. Legal pool','Internal demand labels are shown here for review; they need not appear to the learner.',2)
    y=H-78*mm
    for q,lvl,stem,ans in POOL:
        box(c,M,y-62,W-2*M,62,PALE2); c.setFillColor(BLUE); c.setFont('Helvetica-Bold',8.5); c.drawString(M+9,y-14,f'{q}  {lvl}')
        c.setFillColor(black); c.setFont('Helvetica',8.3); yy=y-29
        for line in wrap(stem,8.3,W-2*M-20): c.drawString(M+9,yy,line); yy-=10
        c.setFillColor(GRAY); c.setFont('Helvetica',8); c.drawString(M+9,y-51,'Answer contract: '+ans+'  |  PEDAGOGICALLY_GENERATED')
        y-=69
    c.showPage(); c.save()

def make_core2b(p):
    c=canvas.Canvas(str(p),pagesize=A4)
    cover(c,'CORE2B - SELECT + TRANSFER + DISCRIMINATE','Static Transfer Workbook','Core2B selects only from the Core2A legal pool and respects an upstream ceiling of M5_METHOD_DISCRIMINATION. Attempt precedes substantial explanation.',['Selected IDs: EQ-D1, EQ-R1, EQ-I1, EQ-H1, EQ-M1.','Legal M6 item remains excluded by the M5 ceiling.','Internal family/demand labels are hidden from learner pages.','No live repair routing or learner-state mutation.'])
    selected=POOL[:5]
    for i,(q,lvl,stem,ans) in enumerate(selected,1):
        header(c,'Core2B - attempt before explanation',f'{i}. Transfer task','Choose the structure and solve before reading the check.',i+1)
        y=H-78*mm; box(c,M,y-65,W-2*M,65,AMBER); c.setFillColor(BLUE); c.setFont('Helvetica-Bold',9); c.drawString(M+9,y-16,'ATTEMPT FIRST')
        c.setFillColor(black); c.setFont('Helvetica',9.5); yy=y-34
        for line in wrap(stem,9.5,W-2*M-20): c.drawString(M+9,yy,line); yy-=12
        y-=82; c.setStrokeColor(GRID)
        for _ in range(12): c.line(M,y,W-M,y); y-=15
        y0=20*mm; box(c,M,y0,W-2*M,48*mm,GREEN); c.setFillColor(BLUE); c.setFont('Helvetica-Bold',9); c.drawString(M+9,y0+48*mm-15,'AFTER YOUR ATTEMPT - ANSWER CHECK')
        c.setFillColor(black); c.setFont('Helvetica',9); c.drawString(M+9,y0+48*mm-33,ans)
        c.showPage()
    c.save()

def make_validation(p):
    c=canvas.Canvas(str(p),pagesize=A4)
    cover(c,'SIX-CORE VALIDATION','Core1 -> Core1A -> Core1B | Core2 -> Core2A -> Core2B','End-to-end review of authority, pedagogy, static product boundaries and mathematical answer custody for one sample topic.',['Core1 = semantic/PCK authority.','Core1A = build understanding. Core1B = reconstruct/consolidate.','Core2 = assessment cognition. Core2A = legal transfer pool. Core2B = selected static transfer.','Compiled product != learner evidence.'])
    header(c,'Validation','1. Responsibility test','Each layer must answer a different question.',2)
    cards(c,[('Core1','What is mathematically true, connected, valid and easily misconstrued?'),('Core1A','How should required understanding be built?'),('Core1B','Can the static product require reconstruction with fading support?'),('Core2','What does this problem family demand, hide, vary and test?'),('Core2A','Which transfer/practice items are legal to publish?'),('Core2B','How is legal transfer exercised in a fixed workbook under a ceiling?')],H-78*mm,47)
    c.showPage()
    header(c,'Validation','2. Audit result','The architecture is functionally distinct and mathematically consistent for this sample.',3)
    cards(c,[('PASS','Core1 shortcut validity is derived from the general model.'),('PASS','Core1A teaches representation and equation meaning before independent use.'),('PASS','Core1B uses open-ended attempt + staged self-help + detailed bottom answer.'),('PASS','Core2 identifies first move, wrong chain, difficulty and transfer envelope.'),('PASS','Core2A legal items are generated/provenance-safe and answer-checked.'),('PASS','Core2B selects only legal IDs and stays below M5.'),('CORRECTION','EQ-H1 gives x=1/4, not x=1; the review fixture uses the corrected answer.'),('BOUNDARY','Static B products cannot claim learner attempt, learning, retention or transfer-readiness.')],H-78*mm,45)
    c.showPage(); c.save()

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def main(out):
    out.mkdir(parents=True,exist_ok=True)
    files={
      'core1':out/'01_core1_semantic_pck_authority.pdf',
      'core1a':out/'02_core1a_build_understanding.pdf',
      'core1b':out/'03_core1b_open_ended_self_guided.pdf',
      'core2':out/'04_core2_assessment_intelligence.pdf',
      'core2a':out/'05_core2a_legal_practice_pool.pdf',
      'core2b':out/'06_core2b_transfer_workbook.pdf',
      'validation':out/'07_six_core_validation.pdf'}
    make_core1(files['core1']); make_core1a(files['core1a']); make_core1b(files['core1b']); make_core2(files['core2']); make_core2a(files['core2a']); make_core2b(files['core2b']); make_validation(files['validation'])
    manifest={'topic':TOPIC,'purpose':'PRACTICE','purpose_note':'Explicit review-fixture binding; not a silent default.','roles':{'Core1':'semantic/PCK authority','Core1A':'build understanding','Core1B':'open-ended self-guided consolidation','Core2':'assessment intelligence','Core2A':'legal practice/transfer pool','Core2B':'static transfer workbook'},'core2a_legal_ids':[x[0] for x in POOL],'core2b_selected_ids':[x[0] for x in POOL[:5]],'core2b_ceiling':'M5_METHOD_DISCRIMINATION','provenance':'PEDAGOGICALLY_GENERATED sample; no official exam attribution','correction':'EQ-H1: x=1/4, P=(1/4,0)','sha256':{k:sha(v) for k,v in files.items()}}
    (out/'validation_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    readme='''# Mathematics six-core review sample\n\nTopic: **A point on an axis equidistant from two fixed points**.\n\nOrder:\n1. Core1 - semantic/PCK authority\n2. Core1A - build understanding\n3. Core1B - open-ended self-guided consolidation\n4. Core2 - assessment intelligence\n5. Core2A - legal practice/transfer pool (purpose explicitly bound to PRACTICE for this fixture)\n6. Core2B - static transfer workbook, compile ceiling M5\n7. Six-core validation report\n\nGoverning distinction: Core1B asks for reconstruction and independent use of taught mathematics; Core2B asks for recognition, selection and transfer when the surface changes.\n\nAll transfer items are pedagogically generated and carry no official exam attribution. The review fixture corrects EQ-H1 to `x=1/4`, `P=(1/4,0)`.\n'''
    (out/'README.md').write_text(readme)

if __name__=='__main__':
    main(Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parent)
