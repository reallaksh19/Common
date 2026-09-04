---
main_topic_id: IOQM-G9-ALG-02
microstream_id: W2-C
microstream_title: Completing squares for extrema
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-ALG-02
prerequisite_interfaces: [IOQM-G9-ALG-01]
source_cutoff: 2026-09-02
---

## A. Scope boundary
Included: quadratic lower/upper bounds by square completion. Excluded: Vieta/discriminant/root-feasibility canon, which remains with the polynomial owner, and prerequisite algebraic transformation teaching.
## B. Learner-state model
PRIOR_KNOWLEDGE: basic algebra and common inequality formulas. LIKELY_HALF_KNOWLEDGE: can produce a bound but may skip direction, equality or attainment. MISSING_BRIDGES: domain-sensitive extremum logic. OWNERSHIP_TARGET: choose a representation only after reading request, domain and direction.
## C. Mathematical invariant / governing structure
minimum-value optimization is distinct from polynomial root-feasibility/discriminant questions. Every extremum claim must pass `BOUND -> EQUALITY -> ATTAINMENT`, followed by a discrete filter when the domain requires it.
## D. Representation inventory
| Representation | What it exposes | First move | Condition | Nearby wrong choice |
|---|---|---|---|---|
| square/balance form | sign and equality | expose nonnegative quantity | stated real domain | raw expansion |
| inequality bound | direction | state lower/upper explicitly | theorem hypotheses | theorem-name matching |
| equality candidate | attainability | test every original constraint | candidate exists | call bound an extremum |
## E. Decision boundaries
| Similar surface | Route A | Route B | Discriminating question | Why wrong route is tempting |
|---|---|---|---|---|
| lower bound vs minimum | prove bound | test equality/attainment | is equality admissible? | same numerical value often occurs |
| real vs integer optimum | continuous bound | discrete candidate check | what is the actual domain? | real equality point is visible |
| optimization vs root feasibility | inequality/square route | polynomial owner | what is being requested? | both use quadratics |
## F. Misconception/diagnosis catalogue
ERROR_CODE: ALG02-W2-C-01
WRONG_MOVE: stop after proving a numerical bound.
WHY_TEMPTING: the target number has appeared.
MISSING_LINK_CLASS: ATTAINMENT
REPAIR_INVARIANT: state equality conditions and verify them in the original domain.
FALSIFIER_OR_CONTRAST: a strict/excluded domain can preserve the bound while destroying the minimum or maximum.
## G. First-move cues
Ask: requested extremum, domain, needed direction, and which representation exposes the sign/equality condition.
## H. H3 -> H0 fading plan
H3: supply representation and equality condition. H2: supply representation only. H1: cue the structural clue. H0: changed surface with no method label.
## I. Validated IOQM source anchors
IOQM-2025-Q07. Exact source custody and independent reconstruction are recorded in the source map/audit.
## J. Source-independent mathematical trace
All promoted authored extrema are rechecked by direct algebra plus equality/attainment verification; integer problems additionally enumerate the localized discrete candidates.
## K. Contrast-pair candidates
lower bound vs minimum; upper bound vs maximum; real vs integer optimum; true inequality vs relevant inequality; equality candidate vs attained extremum.
## L. Transfer candidates
geometry fixed-sum products; number-theory interval filters; parameter feasibility; domain changes.
## M. Candidate mastery items
recognition; first-line representation; full solve; WHY-NOT bound/extremum; domain-change transfer.
## N. Dependency declarations
REQUIRES: frozen algebra-transformation interface. BRIDGE_REQUIRES: polynomial root-feasibility only when the request is about roots, not extrema. Downstream topics may retrieve bounds/equality/attainment without duplicating this canon.
## O. Lead integration notes
Keep the router `REQUEST -> DOMAIN -> BOUNDED? -> DIRECTION -> REPRESENTATION -> BOUND -> EQUALITY -> ATTAINMENT -> DISCRETE FILTER -> CHECK` visible across the integrated path.
## P. Independent QA status
DERIVATIONS_CHECKED: PASS
PROMOTED_NUMERICAL_ANSWERS_CHECKED: PASS
SOURCE_IDS_VERIFIED: PASS
DEPENDENCY_CONFLICTS: NONE
OPEN_ISSUES: current PDFs require exact render QA after this learner-source repair
