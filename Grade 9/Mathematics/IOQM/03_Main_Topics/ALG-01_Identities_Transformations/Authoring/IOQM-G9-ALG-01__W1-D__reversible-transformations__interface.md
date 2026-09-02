---
main_topic_id: IOQM-G9-ALG-01
microstream_id: W1-D
microstream_title: Reversible transformations and branch preservation
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-ALG-01
prerequisite_interfaces: []
source_cutoff: 2026-08-31
---

## A. Scope boundary
Included: equivalence-preserving algebraic rewrites, excluded values, zero-branch preservation, difference-of-squares equivalence and candidate verification after genuinely implication-only steps. Excluded: principal-root/radical domain doctrine, canonically owned by ALG-06.
## B. Learner-state model
PRIOR_KNOWLEDGE: equation solving. LIKELY_HALF_KNOWLEDGE: cancels factors or clears denominators without preserving conditions. MISSING_BRIDGES: classify transformation as equivalent or implication-only. OWNERSHIP_TARGET: preserve the solution set while changing form.
## C. Mathematical invariant / governing structure
An algebraic transformation is safe when it is reversible under recorded domain conditions. Division by an expression may discard a zero branch; clearing a denominator requires its excluded values. The repaired ALG-01 learner items use domain-neutral equivalence examples and do not require radical doctrine.
## D. Representation inventory
| Representation | What it exposes | First move | Condition | Nearby wrong choice |
|---|---|---|---|---|
| zero product | branches | preserve every zero factor | real algebra | divide by a factor |
| rational equation | excluded denominator values | record restrictions | denominator nonzero | clear first |
| equality of squares | difference of squares | subtract and factor | polynomial identity | import square-root conditions |
## E. Decision boundaries
| Similar surface | Route A | Route B | Discriminating question | Why wrong route is tempting |
|---|---|---|---|---|
| factor then zero-product vs divide | preserve branches | discard zero factor | can divisor be zero? | division simplifies |
| clear denominator vs unrestricted multiply | equivalent under restriction | illegal at excluded value | has nonzero restriction been recorded? | multiplication looks reversible |
| square-equality factorization vs radical equation | algebraic equivalence | domain/candidate doctrine | is there a radical at all? | both mention squares |
## F. Misconception/diagnosis catalogue
ERROR_CODE: ALG01-D-01
WRONG_MOVE: divide `x(x-4)=0` by x.
WHY_TEMPTING: cancellation simplifies.
MISSING_LINK_CLASS: DOMAIN_CONDITION
REPAIR_INVARIANT: protect the zero branch before division.
FALSIFIER_OR_CONTRAST: x=0 solves the original but disappears after division.

ERROR_CODE: ALG01-D-02
WRONG_MOVE: teach principal-root conditions inside ALG-01.
WHY_TEMPTING: radical equations are familiar examples of implication-only steps.
MISSING_LINK_CLASS: PREREQUISITE
REPAIR_INVARIANT: use domain-neutral equivalence examples here; route radical doctrine to ALG-06.
FALSIFIER_OR_CONTRAST: repaired Lab #6, Practice #12/#20 and mastery #5 require no square-root knowledge.
## G. First-move cues
Before dividing or clearing denominators, record what could be zero/excluded. For equality of polynomial squares, subtract and factor.
## H. H3 -> H0 fading plan
H3: state restriction/branch explicitly. H2: cue reversibility. H1: ask what information could be lost. H0: changed rational/zero-product/square-equality item.
## I. Validated IOQM source anchors
No radical anchor is promoted in ALG-01. Source anchors are audited in W1-F and do not require importing ALG-06 doctrine.
## J. Source-independent mathematical trace
Repaired learner items were checked algebraically: `(2x+3)^2=x^2` gives x=-3,-1; `(x+6)^2-x^2=20` gives x=-4/3; `(3x+4)^2=(x+2)^2` gives x=-1,-3/2. Each route is equivalence-preserving.
## K. Contrast-pair candidates
cancel vs preserve branch; denominator restriction vs unrestricted clearing; equivalent rewrite vs implication-only step; equality of squares vs radical equation; verify candidate vs no new candidate.
## L. Transfer candidates
rational equation; zero-product branch; square-equality factorization; substitution restriction; downstream radical handoff.
## M. Candidate mastery items
recognition of branch risk; first-line restriction; full reversible solve; WHY-NOT cancellation; ownership-boundary explanation.
## N. Dependency declarations
REQUIRES: F0 algebra. BRIDGE_REQUIRES: none. APPLIES: all transformations. `IOQM-G9-ALG-06` owns principal-root/radical-domain doctrine and is not required by repaired ALG-01 learner items.
## O. Lead integration notes
Use this stream to teach equivalence discipline without radicals. Keep H0/control codes in teacher metadata only.
## P. Independent QA status
DERIVATIONS_CHECKED: PASS
PROMOTED_NUMERICAL_ANSWERS_CHECKED: PASS
SOURCE_IDS_VERIFIED: PASS
DEPENDENCY_CONFLICTS: NONE_AFTER_REPAIR
OPEN_ISSUES: current PDF must be regenerated after source repair
