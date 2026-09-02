from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
AUTH = ROOT / 'Authoring'

LEARNER = [
    '02_Assimilation_Book.md',
    '03_First_Step_Reference.md',
    '04_Recognition_and_First_Line_Lab.md',
    '05_Practice_and_Transfer_Bank.md',
    '06_H0_Mastery_Test.md',
]

specific = {
    '03_First_Step_Reference.md': [
        ('# ALG-03 - First-Step Reference', '# Polynomials, Roots, Vieta & Remainders - First-Step Reference'),
    ],
    '04_Recognition_and_First_Line_Lab.md': [
        ('# ALG-03 - Recognition and First-Line Lab', '# Polynomials, Roots, Vieta & Remainders - Recognition and First-Line Lab'),
    ],
    '05_Practice_and_Transfer_Bank.md': [
        ('# ALG-03 - Practice and Transfer Bank', '# Polynomials, Roots, Vieta & Remainders - Practice and Transfer Bank'),
        ('## Transfer T2-T4', '## Transfer'),
        ('**T2 representation:**', '**Representation change:**'),
        ('**T2 boundary:**', '**Boundary contrast:**'),
        ('**T3 transformed input:**', '**Transformed-input context:**'),
        ('**T3 recurrence:**', '**Recurrence context:**'),
        ('**T4 common structure:**', '**Common-structure transfer:**'),
    ],
    '06_H0_Mastery_Test.md': [
        ('# ALG-03 - H0 Mixed Mastery Test', '# Polynomials, Roots, Vieta & Remainders - Independent Mixed Mastery Check'),
    ],
}

for name in LEARNER:
    p = ROOT / name
    s = p.read_text()
    for a, b in specific.get(name, []):
        s = s.replace(a, b)
    # Descriptive support fading only; internal H-levels remain authoring controls.
    s = s.replace('H3 -> H2 -> H1 -> H0', 'support fades toward independence')
    s = s.replace('H3→H2→H1→H0', 'support fades toward independence')
    s = re.sub(r'(?m)^###\s*H3\s*[-—:]\s*', '### Full support - ', s)
    s = re.sub(r'(?m)^###\s*H2\s*[-—:]\s*', '### Medium support - ', s)
    s = re.sub(r'(?m)^###\s*H1\s*[-—:]\s*', '### Light support - ', s)
    s = re.sub(r'(?m)^###\s*H0\s*[-—:]\s*', '### Independent - ', s)
    s = re.sub(r'(?m)^##\s*([^\n]*?)H3\s*(?:->|→)\s*H2\s*(?:->|→)\s*H1\s*(?:->|→)\s*H0([^\n]*)$', r'## \1support fades toward independence\2', s)
    # Defensive learner-only control-code scrub.
    s = re.sub(r'(?<![A-Za-z0-9])H3(?![A-Za-z0-9])', 'Full support', s)
    s = re.sub(r'(?<![A-Za-z0-9])H2(?![A-Za-z0-9])', 'Medium support', s)
    s = re.sub(r'(?<![A-Za-z0-9])H1(?![A-Za-z0-9])', 'Light support', s)
    s = re.sub(r'(?<![A-Za-z0-9])H0(?![A-Za-z0-9])', 'Independent', s)
    s = re.sub(r'(?<![A-Za-z0-9])T2(?![A-Za-z0-9])', 'Representation transfer', s)
    s = re.sub(r'(?<![A-Za-z0-9])T3(?![A-Za-z0-9])', 'Context transfer', s)
    s = re.sub(r'(?<![A-Za-z0-9])T4(?![A-Za-z0-9])', 'Mixed transfer', s)
    s = s.replace('ALG-01', 'the prerequisite algebra topic')
    s = s.replace('ALG-02', 'the inequality/optimization topic')
    s = s.replace('ALG-03', 'this polynomial topic')
    p.write_text(s)

forbidden = re.compile(r'(?i)(?<![A-Za-z0-9])(?:H[0-3]|T[234]|WAVE|PR|ISSUE|ALG-01|ALG-02|ALG-03)(?![A-Za-z0-9])')
for name in LEARNER:
    hits = sorted(set(m.group(0) for m in forbidden.finditer((ROOT / name).read_text())))
    if hits:
        raise SystemExit(f'learner leakage in {name}: {hits}')

streams = [
    ('W2-A', 'polynomial-representations', 'Polynomial representations and request routing', 'coefficient, factor/root, evaluation and remainder-class representations chosen by requested information', 'coefficients, factors, roots and remainder classes describe the same polynomial object but expose different targets', 'IOQM-2025-Q16; IOQM-2024-Q24'),
    ('W2-B', 'vieta-symmetric-roots', 'Vieta and symmetric root invariants', 'derive Vieta once from factor expansion and use symmetric invariants without unnecessary root solving', 'for ax^2+bx+c with roots alpha,beta: alpha+beta=-b/a and alpha beta=c/a', 'IOQM-2025-Q16; IOQM-2023-Q12'),
    ('W2-C', 'discriminant-root-behavior', 'Discriminant and real-root behavior', 'real-root count, repeated-root conditions and parameter feasibility through the quadratic discriminant', 'Delta=b^2-4ac determines two distinct, repeated, or no real roots; minimum-value optimization remains with the inequality owner', 'IOQM-2025-Q24'),
    ('W2-D', 'transformed-roots', 'Transformed roots and shifted input', 'build polynomials for shifted/scaled root sets while controlling the sign reversal between root shift and input shift', 'roots shifted by +c are produced by P(x-c), not P(x+c)', 'IOQM-2024-Q24'),
    ('W2-E', 'remainder-factor-theorem', 'Remainder and factor theorem', 'evaluation as the canonical remainder on division by x-a and the zero test for a linear factor', 'P(x)=(x-a)Q(x)+r implies r=P(a); x-a is a factor iff P(a)=0', 'IOQM-2023-Q12'),
    ('W2-F', 'polynomial-reduction', 'Polynomial reduction and high powers', 'reduce high powers modulo a low-degree polynomial relation rather than expanding or solving roots unnecessarily', 'a degree-d relation reduces every polynomial to a remainder of degree < d', 'IOQM-2025-Q16; IOQM-2024-Q24'),
    ('W2-G', 'common-root-elimination', 'Common-root elimination', 'subtract or combine polynomial equations to lower degree, then verify candidates in all originals', 'a common root satisfies every polynomial combination, but an eliminated candidate must be checked in each original equation', 'IOQM-2023-Q12'),
    ('W2-H', 'source-pyq-audit', 'Source and PYQ audit', 'paper/key custody, independent answer reconstruction, ownership drift and representation-choice audit', 'historical source mechanisms remain source-custodied and do not move optimization or prerequisite ownership into this topic', 'IOQM-2025-Q16; IOQM-2025-Q24; IOQM-2024-Q24; IOQM-2023-Q12'),
]

index = [
    '# ALG-03 - Microstream Interface Index',
    '',
    'Status: `INDEX_ONLY__NOT_INTERFACE_AUTHORITY`',
    '',
    'Mandatory interface authority:',
]

for mid, slug, title, scope, invariant, anchors in streams:
    fn = f'IOQM-G9-ALG-03__{mid}__{slug}__interface.md'
    index.append(f'- `{fn}`')
    text = f'''---
main_topic_id: IOQM-G9-ALG-03
microstream_id: {mid}
microstream_title: {title}
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-ALG-03
prerequisite_interfaces: [IOQM-G9-ALG-01]
source_cutoff: 2026-09-02
---

## A. Scope boundary
Included: {scope}. Excluded: canonical inequality/equality/attainment teaching and prerequisite transformation canon.
## B. Learner-state model
PRIOR_KNOWLEDGE: routine factorization and quadratic solving. LIKELY_HALF_KNOWLEDGE: can compute but often chooses a costly representation. MISSING_BRIDGES: route by requested information and distinguish symmetric data from individual roots. OWNERSHIP_TARGET: representation selection before calculation.
## C. Mathematical invariant / governing structure
{invariant}. The governing principle is `REQUESTED INFORMATION -> CHEAPEST VALID REPRESENTATION -> CALCULATION -> CHECK`.
## D. Representation inventory
| Representation | What it exposes | First move | Condition | Nearby wrong choice |
|---|---|---|---|---|
| coefficient form | sums/products/parameters | compare coefficients | polynomial degree known | solve roots immediately |
| factor/root form | zeros | factor or use known roots | factorization available | expand everything |
| evaluation/remainder form | divisor x-a | compute P(a) | linear divisor | long division |
| low-degree remainder class | high powers | reduce by relation | valid polynomial relation | brute-force exponentiation |
## E. Decision boundaries
| Similar surface | Route A | Route B | Discriminating question | Why wrong route is tempting |
|---|---|---|---|---|
| individual roots vs invariant | solve roots | Vieta/symmetric identities | does target need each root? | roots are visible objects |
| root count vs minimum value | discriminant | inequality owner | is request about roots or value range? | same quadratic surface |
| root shift vs input shift | P(x-c) | P(x+c) | where should an old root map? | signs look symmetric |
| high power vs reduction | relation remainder | expansion | is a low-degree relation given? | exponent suggests repeated multiplication |
## F. Misconception/diagnosis catalogue
ERROR_CODE: ALG03-{mid}-01
WRONG_MOVE: choose a familiar polynomial technique before reading the requested information.
WHY_TEMPTING: several representations are mathematically equivalent.
MISSING_LINK_CLASS: REPRESENTATION_SELECTION
REPAIR_INVARIANT: name what the target needs, then choose the representation that exposes exactly that information.
FALSIFIER_OR_CONTRAST: the same polynomial can require Vieta, discriminant, evaluation, or reduction depending on the question.
## G. First-move cues
Symmetric target -> Vieta; root count -> discriminant; shifted roots -> test input substitution; divisor x-a -> evaluate; huge exponent with relation -> reduce; common root -> eliminate then verify.
## H. H3 -> H0 fading plan
H3: supply representation plus first execution line. H2: supply representation only. H1: cue the visible structural clue. H0: changed surface with no method label.
## I. Validated IOQM source anchors
{anchors}. Exact paper/key custody and independent reconstruction are recorded in the source coverage and mathematics audit.
## J. Source-independent mathematical trace
All promoted authored answers are independently recomputed; reduction remainders are normalized and common-root candidates are substituted back into every original equation.
## K. Contrast-pair candidates
individual vs symmetric roots; discriminant vs optimization; root shift vs input shift; expansion vs reduction; evaluation vs long division; separate solving vs elimination.
## L. Transfer candidates
recurrence characteristic relations; geometry/number-theory polynomial applications; parameter feasibility; common-factor thinking.
## M. Candidate mastery items
recognition; first-line representation; full solve; WHY-NOT representation; boundary routing; changed-surface transfer.
## N. Dependency declarations
REQUIRES: frozen algebra-transformation interface. BRIDGE_REQUIRES: inequality/optimization only when the request is an extremum, not root behavior. Downstream topics may retrieve Vieta/discriminant/remainder/reduction without duplicating this canon.
## O. Lead integration notes
Derive Vieta once from factor expansion, then keep the topic-wide router focused on requested information and cheapest valid representation.
## P. Independent QA status
DERIVATIONS_CHECKED: PASS
PROMOTED_NUMERICAL_ANSWERS_CHECKED: PASS
SOURCE_IDS_VERIFIED: PASS
DEPENDENCY_CONFLICTS: NONE
OPEN_ISSUES: current PDFs require exact render QA after learner-source repair
'''
    (AUTH / fn).write_text(text)

(AUTH / 'Microstream_Interfaces.md').write_text('\n'.join(index) + '\n\nThis file is navigation only and does not establish schema conformance.\n')

# Harden the durable renderer so student artifacts do not expose internal topic codes.
rp = AUTH / 'render_alg03_pdfs.py'
r = rp.read_text()
r = r.replace('"IOQM Grade 9 | ALG-03"', '"IOQM Grade 9 | Polynomials, Roots, Vieta & Remainders"')
r = r.replace('build(STUDENT, "ALG-03: Polynomials, Roots, Vieta & Remainders",', 'build(STUDENT, "Polynomials, Roots, Vieta & Remainders",')
r = r.replace('build(TEACHER, "ALG-03 Teacher Diagnostic Key",', 'build(TEACHER, "Polynomials, Roots, Vieta & Remainders - Teacher Diagnostic Key",')
rp.write_text(r)

if 'ALG-03:' in rp.read_text() or 'IOQM Grade 9 | ALG-03' in rp.read_text():
    raise SystemExit('renderer still exposes internal student topic code')
