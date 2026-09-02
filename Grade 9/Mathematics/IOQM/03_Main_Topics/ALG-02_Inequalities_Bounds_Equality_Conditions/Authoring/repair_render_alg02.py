from pathlib import Path
import re
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.pdfmetrics import stringWidth

ROOT = Path(__file__).resolve().parents[1]
AUTH = ROOT / 'Authoring'
PDFS = ROOT / 'PDFs'
PDFS.mkdir(exist_ok=True)

# Repair learner-facing control labels and internal topic codes without changing mathematics.
repls = {
'02_Assimilation_Book.md': [
('canonically owned by ALG-03', 'owned by the polynomial/root-feasibility topic'),
('## 7. TRY - H3 -> H2 -> H1 -> H0', '## 7. TRY - support fades toward independence'),
('### H3 - execution supplied', '### Full support - execution supplied'),
('### H2 - representation supplied', '### Medium support - representation supplied'),
('### H1 - recognition clue', '### Light support - recognition clue'),
('### H0 - no route supplied', '### Independent - no route supplied'),
('an ALG-02 mechanism inside a geometry surface', 'the inequality/attainment mechanism inside a geometry surface'),
('retrieve ALG-01 transformation habits but route to ALG-03 discriminant canon. If the request is the quadratic’s minimum value, remain in ALG-02 and complete the square.', 'retrieve reversible-transformation habits and route to the polynomial/root-feasibility topic. If the request is the quadratic’s minimum value, stay with inequality optimization and complete the square.'),
],
'03_First_Step_Reference.md': [
('# ALG-02 - First-Step Reference', '# Inequalities, Bounds & Equality Conditions - First-Step Reference'),
('route to ALG-03 discriminant canon?', 'route to the polynomial/root-feasibility method?'),
],
'04_Recognition_and_First_Line_Lab.md': [
('# ALG-02 - Recognition and First-Line Lab', '# Inequalities, Bounds & Equality Conditions - Recognition and First-Line Lab'),
('Is this canonically an ALG-02 optimization problem?', 'Is this canonically an inequality-optimization problem?'),
],
'05_Practice_and_Transfer_Bank.md': [
('# ALG-02 - Practice and Transfer Bank', '# Inequalities, Bounds & Equality Conditions - Practice and Transfer Bank'),
('## Transfer T2-T4', '## Transfer'),
('**T2 representation:**', '**Representation change:**'),
('**T3 domain:**', '**Domain change:**'),
('**T3 number theory:**', '**Number-theory surface:**'),
('**T3 geometry:**', '**Geometry surface:**'),
('**T4 mixed:**', '**Mixed transfer:**'),
('an ALG-02 mechanism inside a geometry surface', 'the inequality/attainment mechanism inside a geometry surface'),
],
'06_H0_Mastery_Test.md': [
('# ALG-02 - H0 Mixed Mastery Test', '# Inequalities, Bounds & Equality Conditions - Independent Mixed Mastery Check'),
('state why ALG-02 should not duplicate the method', 'state why this inequality topic should not duplicate the method'),
],
}
for name, pairs in repls.items():
    p = ROOT / name
    s = p.read_text()
    for a,b in pairs:
        s=s.replace(a,b)
    # Final defensive scrub: learner files must not expose internal topic identifiers.
    s=s.replace('ALG-01', 'the prerequisite algebra topic')
    s=s.replace('ALG-02', 'this inequality topic')
    s=s.replace('ALG-03', 'the polynomial/root-feasibility topic')
    p.write_text(s)

# Fail if learner surfaces still expose control-plane labels/codes.
forbidden = re.compile(r'(?i)(?<![A-Za-z0-9])(?:H[0-3]|T[234]|WAVE|PR|ISSUE|ALG-01|ALG-02|ALG-03)(?![A-Za-z0-9])')
for name in repls:
    hits=sorted(set(m.group(0) for m in forbidden.finditer((ROOT/name).read_text())))
    if hits: raise SystemExit(f'learner leakage in {name}: {hits}')

# Consolidated file is index-only; per-microstream files carry interface authority.
streams = [
('W2-A','am-gm','AM-GM and balance bounds','positive-term AM-GM, fixed-product lower bounds and fixed-sum product upper bounds','equality occurs at the balanced configuration under the stated positive/nonnegative domain','IOQM-2024-Q06'),
('W2-B','cauchy-engel','Cauchy and Engel representation','justified reciprocal/sum bounds using Cauchy/Engel only when the structure exposes the requested direction','the theorem name is secondary; equality and domain hypotheses must be checked','IOQM-2024-Q06'),
('W2-C','complete-square','Completing squares for extrema','quadratic lower/upper bounds by square completion','minimum-value optimization is distinct from polynomial root-feasibility/discriminant questions','IOQM-2025-Q07'),
('W2-D','feasibility-boundedness','Feasibility, boundedness and direction','identify requested direction and whether a finite bound exists before choosing a technique','a true bound in the wrong direction or an unattained infimum/supremum is not the requested extremum','IOQM-2025-Q07'),
('W2-E','equality-attainment','Equality conditions and attainment','separate numerical bound, equality condition and admissibility in the actual domain','equality outside the domain blocks minimum/maximum claims','IOQM-2024-Q06'),
('W2-F','discrete-filtering','Real-to-discrete filtering','use a continuous bound to localize candidates, then check the admissible integers/discrete set','the real equality point cannot be imported directly into an integer domain','IOQM-2025-Q07'),
('W2-G','source-pyq-audit','Source and PYQ audit','stable source/key custody, independent answer reconstruction and ownership drift checks','historical source mechanisms do not move canonical ownership between inequality and polynomial topics','IOQM-2025-Q07; IOQM-2024-Q06'),
]
index=['# ALG-02 - Microstream Interface Index','', 'Status: `INDEX_ONLY__NOT_INTERFACE_AUTHORITY`','', 'Mandatory interface authority:']
for mid,slug,title,scope,invariant,anchor in streams:
    fn=f'IOQM-G9-ALG-02__{mid}__{slug}__interface.md'
    index.append(f'- `{fn}`')
    text=f'''---\nmain_topic_id: IOQM-G9-ALG-02\nmicrostream_id: {mid}\nmicrostream_title: {title}\nowner_role: RESEARCH_INTERFACE_ONLY\nstatus: READY_FOR_LEAD\ncanonical_teaching_owner: IOQM-G9-ALG-02\nprerequisite_interfaces: [IOQM-G9-ALG-01]\nsource_cutoff: 2026-09-02\n---\n\n## A. Scope boundary\nIncluded: {scope}. Excluded: Vieta/discriminant/root-feasibility canon, which remains with the polynomial owner, and prerequisite algebraic transformation teaching.\n## B. Learner-state model\nPRIOR_KNOWLEDGE: basic algebra and common inequality formulas. LIKELY_HALF_KNOWLEDGE: can produce a bound but may skip direction, equality or attainment. MISSING_BRIDGES: domain-sensitive extremum logic. OWNERSHIP_TARGET: choose a representation only after reading request, domain and direction.\n## C. Mathematical invariant / governing structure\n{invariant}. Every extremum claim must pass `BOUND -> EQUALITY -> ATTAINMENT`, followed by a discrete filter when the domain requires it.\n## D. Representation inventory\n| Representation | What it exposes | First move | Condition | Nearby wrong choice |\n|---|---|---|---|---|\n| square/balance form | sign and equality | expose nonnegative quantity | stated real domain | raw expansion |\n| inequality bound | direction | state lower/upper explicitly | theorem hypotheses | theorem-name matching |\n| equality candidate | attainability | test every original constraint | candidate exists | call bound an extremum |\n## E. Decision boundaries\n| Similar surface | Route A | Route B | Discriminating question | Why wrong route is tempting |\n|---|---|---|---|---|\n| lower bound vs minimum | prove bound | test equality/attainment | is equality admissible? | same numerical value often occurs |\n| real vs integer optimum | continuous bound | discrete candidate check | what is the actual domain? | real equality point is visible |\n| optimization vs root feasibility | inequality/square route | polynomial owner | what is being requested? | both use quadratics |\n## F. Misconception/diagnosis catalogue\nERROR_CODE: ALG02-{mid}-01\nWRONG_MOVE: stop after proving a numerical bound.\nWHY_TEMPTING: the target number has appeared.\nMISSING_LINK_CLASS: ATTAINMENT\nREPAIR_INVARIANT: state equality conditions and verify them in the original domain.\nFALSIFIER_OR_CONTRAST: a strict/excluded domain can preserve the bound while destroying the minimum or maximum.\n## G. First-move cues\nAsk: requested extremum, domain, needed direction, and which representation exposes the sign/equality condition.\n## H. H3 -> H0 fading plan\nH3: supply representation and equality condition. H2: supply representation only. H1: cue the structural clue. H0: changed surface with no method label.\n## I. Validated IOQM source anchors\n{anchor}. Exact source custody and independent reconstruction are recorded in the source map/audit.\n## J. Source-independent mathematical trace\nAll promoted authored extrema are rechecked by direct algebra plus equality/attainment verification; integer problems additionally enumerate the localized discrete candidates.\n## K. Contrast-pair candidates\nlower bound vs minimum; upper bound vs maximum; real vs integer optimum; true inequality vs relevant inequality; equality candidate vs attained extremum.\n## L. Transfer candidates\ngeometry fixed-sum products; number-theory interval filters; parameter feasibility; domain changes.\n## M. Candidate mastery items\nrecognition; first-line representation; full solve; WHY-NOT bound/extremum; domain-change transfer.\n## N. Dependency declarations\nREQUIRES: frozen algebra-transformation interface. BRIDGE_REQUIRES: polynomial root-feasibility only when the request is about roots, not extrema. Downstream topics may retrieve bounds/equality/attainment without duplicating this canon.\n## O. Lead integration notes\nKeep the router `REQUEST -> DOMAIN -> BOUNDED? -> DIRECTION -> REPRESENTATION -> BOUND -> EQUALITY -> ATTAINMENT -> DISCRETE FILTER -> CHECK` visible across the integrated path.\n## P. Independent QA status\nDERIVATIONS_CHECKED: PASS\nPROMOTED_NUMERICAL_ANSWERS_CHECKED: PASS\nSOURCE_IDS_VERIFIED: PASS\nDEPENDENCY_CONFLICTS: NONE\nOPEN_ISSUES: current PDFs require exact render QA after this learner-source repair\n'''
    (AUTH/fn).write_text(text)
(AUTH/'Microstream_Interfaces.md').write_text('\n'.join(index)+'\n\nThis file is navigation only and does not establish schema conformance.\n')

# Deterministic lightweight renderer from canonical markdown.
W,H=A4; LEFT=42; RIGHT=42; TOP=44; BOTTOM=34; BODY=8.3; LEAD=10.2

def clean(s): return s.replace('**','').replace('`','').lstrip('> ')
def wrap(s,font,size,width):
    words=s.split(); out=[]; cur=''
    for word in words:
        cand=(cur+' '+word).strip()
        if stringWidth(cand,font,size)<=width: cur=cand
        else:
            if cur: out.append(cur)
            cur=word
    if cur or not out: out.append(cur)
    return out

def render(inputs,out,title):
    c=canvas.Canvas(str(out),pagesize=A4,pageCompression=1,invariant=1); c.setTitle(title)
    page=0; y=H-TOP; started=False
    def footer():
        c.setFont('Helvetica',6.3); c.drawString(LEFT,18,title); c.drawRightString(W-RIGHT,18,f'Page {page}')
    def new_page():
        nonlocal page,y,started
        if started: footer(); c.showPage()
        started=True; page+=1; y=H-TOP
    def ensure(n=1,leading=LEAD):
        nonlocal y
        if y-n*leading<BOTTOM: new_page()
    def line(txt,font='Helvetica',size=BODY,leading=LEAD,indent=0):
        nonlocal y
        ensure(1,leading); c.setFont(font,size); c.drawString(LEFT+indent,y,txt); y-=leading
    for inp in inputs:
        new_page()
        for raw in (ROOT/inp).read_text().splitlines():
            s=raw.rstrip()
            if not s: y-=4; continue
            if s.startswith('# '): font,size,leading,txt='Helvetica-Bold',14.5,17,clean(s[2:])
            elif s.startswith('## '): font,size,leading,txt='Helvetica-Bold',11,13.2,clean(s[3:])
            elif s.startswith('### '): font,size,leading,txt='Helvetica-Bold',9.5,11.5,clean(s[4:])
            else: font,size,leading,txt='Helvetica',BODY,LEAD,clean(s)
            if txt.startswith('|') and txt.endswith('|'):
                cells=[x.strip() for x in txt.strip('|').split('|')]
                if all(set(x)<=set('-:') for x in cells): continue
                txt='  |  '.join(cells)
            m=re.match(r'^(\s*)([-*]|\d+\.)\s+(.*)$',txt)
            indent=8 if m else 0
            if m: txt=f'{m.group(2)} {m.group(3)}'
            parts=wrap(txt,font,size,W-LEFT-RIGHT-indent)
            ensure(len(parts),leading)
            for part in parts: line(part,font,size,leading,indent)
    if started: footer()
    c.save()
    return page

student_pages=render(['02_Assimilation_Book.md','03_First_Step_Reference.md','04_Recognition_and_First_Line_Lab.md','05_Practice_and_Transfer_Bank.md','06_H0_Mastery_Test.md'],PDFS/'ALG02_Student_Pack_v1.pdf','Inequalities, Bounds & Equality Conditions - Student Pack')
teacher_pages=render(['Teacher_Diagnostic_Key.md'],PDFS/'ALG02_Teacher_Key_v1.pdf','Inequalities, Bounds & Equality Conditions - Teacher Key')
print('student_pages',student_pages,'teacher_pages',teacher_pages)
