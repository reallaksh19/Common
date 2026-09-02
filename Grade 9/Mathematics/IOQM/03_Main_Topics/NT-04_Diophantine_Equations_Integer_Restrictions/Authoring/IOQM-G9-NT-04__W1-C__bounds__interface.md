---
main_topic_id: IOQM-G9-NT-04
microstream_id: W1-C
microstream_title: Bounds before Enumeration
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-NT-04
prerequisite_interfaces: [NT03, ALG01, ALG03(narrow bridge)]
source_cutoff: 2026-09-02
---

# Bounds before Enumeration - Research Interface

## A. Scope boundary
Included: monotone bounds, positivity, factor-pair extrema.

Excluded: general inequality canon or continuous optimization as final answer. Overlap mechanisms remain with their declared canonical owners and appear here only as retrieval or a narrow bridge.

## B. Learner-state model
PRIOR_KNOWLEDGE: integer arithmetic, basic algebra, factors/multiples, and routine school procedures.
LIKELY_HALF_KNOWLEDGE: can execute familiar examples but may not choose the cheapest representation or preserve all conditions.
MISSING_BRIDGES: recognition, representation choice, finite-case discipline, and independent verification.
OWNERSHIP_TARGET: Bounds before Enumeration as part of one integrated topic journey.

## C. Mathematical invariant / governing structure
**prove a finite interval or factor range before searching**

Derivation/reconstruction: translate the visible condition into the representation above; prove that the transformation preserves every admissible solution (or mark it candidate-generating); reduce to a finite/checkable structure; then verify candidates against the original condition.

## D. Representation inventory
| Representation | What it exposes | First move | Condition | Nearby wrong choice |
|---|---|---|---|---|
| factor/divisor cases | finite candidates | set product factors equal to divisors | integer factors | expand and scan |
| constraint-normalized form | cheap filter | apply parity/gcd/bound before solving | preserve domain | solve reals first |
| reconstructed original variables | verification | substitute back | all side conditions | accept transformed candidate |

## E. Decision boundaries
| Similar surface | Route A | Route B | Discriminating question | Why wrong route is tempting |
|---|---|---|---|---|
| equation with product structure | factor cases | brute force | does integrality make factors divisors? | school habit is to expand |
| quadratic-looking integer equation | square/discrete filter | real-root analysis | is integrality stronger than reality? | quadratic formula is familiar |
| finite list | prove complete | sample cases | does every solution map to exactly one case? | several examples feel convincing |

## F. Misconception/diagnosis catalogue
ERROR_CODE: W1-C-E1
WRONG_MOVE: search a wide range without a bound
WHY_TEMPTING: integer problems invite experimentation
MISSING_LINK_CLASS: DISCRETE_FILTER
REPAIR_INVARIANT: derive factor/bound/parity structure first
FALSIFIER_OR_CONTRAST: a valid solution outside the searched range defeats the method

ERROR_CODE: W1-C-E2
WRONG_MOVE: drop sign/gcd/parity conditions after transformation
WHY_TEMPTING: the transformed equation looks simpler
MISSING_LINK_CLASS: DOMAIN_CONDITION
REPAIR_INVARIANT: carry every original condition into each case
FALSIFIER_OR_CONTRAST: a reconstructed candidate violating the original side condition

ERROR_CODE: W1-C-E3
WRONG_MOVE: stop after finding one candidate
WHY_TEMPTING: contest answers are often unique
MISSING_LINK_CLASS: EXECUTION
REPAIR_INVARIANT: state exhaustiveness and check all cases
FALSIFIER_OR_CONTRAST: a second valid factor branch

## G. First-move cues
- fixed integer product -> name the factor pair variable
- integer extremum -> bound or locate divisors near the real optimum
- candidate-generating step -> schedule an original-equation check

## H. H3 -> H0 fading plan
- H3: give the executable relation and ask the learner to complete one controlled step.
- H2: name only the representation/structure to expose.
- H1: give only the visible clue or boundary question.
- H0: use a changed-surface item with no method label; require the learner to choose and justify the first line.
All candidate numerical items used by the lead are independently checked before promotion.

## I. Validated IOQM source anchors
| Stable ID | Year/Q | Source status | Primary/bridge role | Mechanism | Figure? | Key status |
|---|---|---|---|---|---|---|
| - | - | - | - | - | - | - |

## J. Source-independent mathematical trace
Source-independent authored traces in the practice/mastery banks were recomputed by direct enumeration, algebraic reconstruction, or exact rational arithmetic; see Independent_Math_Audit.md.

## K. Contrast-pair candidates
- factor pair vs real-variable solving
- positive factors vs signed shifted factors
- real root vs integer root
- decimal proximity vs exact cross-product gap
- sampled cases vs exhaustive parametrisation

## L. Transfer candidates
- AUTHOR_CREATED_TRANSFER: integer rectangle -> divisor-pair extremum
- AUTHOR_CREATED_TRANSFER: reciprocal equation -> shifted factor product
- AUTHOR_CREATED_TRANSFER: rational closeness -> determinant 1 condition
- AUTHOR_CREATED_TRANSFER: quadratic square -> difference of squares

## M. Candidate mastery items
- recognition-only: identify the cheapest discrete filter
- first-line-only: expose the factor/determinant/square condition
- full solve: prove finite-case completeness
- WHY-NOT: explain why real solving or decimal testing is insufficient
- verification: reject an extraneous reconstructed candidate

## N. Dependency declarations
- REQUIRES: NT03, ALG01, ALG03(narrow bridge).
- BRIDGE_REQUIRES: only the minimum explicitly cited overlap result; never the neighbour chapter as a whole.
- APPLIES: previously owned arithmetic/algebra facts as retrieval.
- DOWNSTREAM MAY ASSUME: integer filtering/reconstruction router and finite-case completeness checks.

## O. Lead integration notes
Teach the governing topic router once globally. Compress repeated prerequisite reminders to one-line retrieval cues. Merge this stream with neighbouring streams through explicit contrast pairs. Do not expose interface IDs, hint-level codes, topic codes, QA states, or production terminology to learners. Place this material where the dependency map first needs it, not where the research stream happened to be authored.

## P. Independent QA status
DERIVATIONS_CHECKED: PASS
PROMOTED_NUMERICAL_ANSWERS_CHECKED: PASS
SOURCE_IDS_VERIFIED: PASS
DEPENDENCY_CONFLICTS: NONE
OPEN_ISSUES: NONE affecting static integration
