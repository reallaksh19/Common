---
main_topic_id: IOQM-G9-NT-02
microstream_id: W2-B
microstream_title: Legal modular operations and reduction
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-NT-02
prerequisite_interfaces: [IOQM-G9-NT-01]
source_cutoff: 2026-09-02
---

## A. Scope boundary
Included: addition, subtraction, multiplication, positive integer powers and early residue reduction. Excluded: unconditional division/cancellation and advanced ring language.
## B. Learner-state model
PRIOR_KNOWLEDGE: arithmetic operations. LIKELY_HALF_KNOWLEDGE: knows “take mod” at the end but not that legal operations preserve residue classes. MISSING_BRIDGE: reduction can happen before computation. OWNERSHIP_TARGET: replace large representatives early without changing the modular target.
## C. Mathematical invariant / governing structure
If `a congruent b (mod m)` and `c congruent d (mod m)`, then sums, differences and products are congruent; positive integer powers preserve congruence.
## D. Representation inventory
| Representation | What it exposes | First move | Condition | Nearby wrong choice |
|---|---|---|---|---|
| large arithmetic expression | reducible state | reduce each factor/term mod m | fixed modulus | compute huge integer first |
| polynomial in a residue | operation closure | substitute congruent representative | integer coefficients | divide coefficients mod m |
| negative representative | shorter arithmetic | replace by convenient congruent value | fixed modulus | force only nonnegative values too early |
## E. Decision boundaries
| Similar surface | Route A | Route B | Discriminating question | Why wrong route is tempting |
|---|---|---|---|---|
| legal multiplication vs division | multiply/reduce | test invertibility before division | is an inverse required? | ordinary algebra permits cancellation |
| compute-first vs reduce-first | direct arithmetic | residue-state arithmetic | is only a residue requested? | full values feel safer |
## F. Misconception/diagnosis catalogue
ERROR_CODE: NT02-B-01
WRONG_MOVE: expand a huge power or product before reducing modulo m.
WHY_TEMPTING: standard arithmetic habit.
MISSING_LINK_CLASS: REPRESENTATION
REPAIR_INVARIANT: legal operations depend only on residue classes.
FALSIFIER_OR_CONTRAST: reducing `12345` modulo 7 before squaring gives the same final residue with far less work.
## G. First-move cues
If the target is “mod m,” reduce every large input before doing more arithmetic.
## H. H3 -> H0 fading plan
H3: identify each reduced representative. H2: cue “reduce before compute.” H1: ask which information the target retains. H0: mixed expression with no operation hint.
## I. Validated IOQM source anchors
The power/residue anchors in W2-G require legal early reduction; no source introduces a broader algebraic doctrine.
## J. Source-independent mathematical trace
Promoted examples are checked both by direct integer computation on small cases and by residue reduction.
## K. Contrast-pair candidates
full value vs residue; positive vs negative representative; multiplication vs division; late vs early reduction.
## L. Transfer candidates
polynomial residues, digit sums, parity filters, finite-state transitions.
## M. Candidate mastery items
reduce a large integer; reduce a product; justify a powered congruence; identify an illegal division step; choose a convenient negative representative.
## N. Dependency declarations
REQUIRES: congruence meaning W2-A. BRIDGE_REQUIRES: divisibility equivalence from prior interface. APPLIES: cycles, last digits and simultaneous congruences.
## O. Lead integration notes
Teach operational legality immediately after semantic meaning; defer inverses/cancellation to W2-C.
## P. Independent QA status
DERIVATIONS_CHECKED: PASS
PROMOTED_NUMERICAL_ANSWERS_CHECKED: PASS
SOURCE_IDS_VERIFIED: PASS
DEPENDENCY_CONFLICTS: NONE
OPEN_ISSUES: regenerate learner PDF after source-label repair
