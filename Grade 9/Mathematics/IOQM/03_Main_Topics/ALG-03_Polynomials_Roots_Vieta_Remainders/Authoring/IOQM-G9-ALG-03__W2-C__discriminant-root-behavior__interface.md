---
main_topic_id: IOQM-G9-ALG-03
microstream_id: W2-C
microstream_title: Discriminant and real-root behavior
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-ALG-03
prerequisite_interfaces: [IOQM-G9-ALG-01]
source_cutoff: 2026-09-02
---

## A. Scope boundary
Included: real-root count, repeated-root conditions and parameter feasibility through the quadratic discriminant. Excluded: canonical inequality/equality/attainment teaching and prerequisite transformation canon.
## B. Learner-state model
PRIOR_KNOWLEDGE: routine factorization and quadratic solving. LIKELY_HALF_KNOWLEDGE: can compute but often chooses a costly representation. MISSING_BRIDGES: route by requested information and distinguish symmetric data from individual roots. OWNERSHIP_TARGET: representation selection before calculation.
## C. Mathematical invariant / governing structure
Delta=b^2-4ac determines two distinct, repeated, or no real roots; minimum-value optimization remains with the inequality owner. The governing principle is `REQUESTED INFORMATION -> CHEAPEST VALID REPRESENTATION -> CALCULATION -> CHECK`.
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
ERROR_CODE: ALG03-W2-C-01
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
IOQM-2025-Q24. Exact paper/key custody and independent reconstruction are recorded in the source coverage and mathematics audit.
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
