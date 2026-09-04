---
main_topic_id: IOQM-G9-ALG-07
microstream_id: W1-G
microstream_title: Source and PYQ audit
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-ALG-07
prerequisite_interfaces: []
source_cutoff: 2026-08-31
---

## A. Scope boundary
Included: custody, stable IDs, official paper/key authority and independent mathematical traces for promoted historical anchors. Excluded: inventing source IDs, inferring official Grade-9 weightage, or changing official wording/key.

## B. Learner-state model
PRIOR_KNOWLEDGE: not applicable to custody work.
LIKELY_HALF_KNOWLEDGE: not applicable.
MISSING_BRIDGES: lead needs verified source/mechanism linkage without leaking control-plane detail to students.
OWNERSHIP_TARGET: auditable historical provenance.

## C. Mathematical invariant / governing structure
Historical questions are usable only when stable ID, source authority, official key authority and an independent solution trace agree. Topic claims derive from mechanisms, not frequency or unofficial syllabus inference.

## D. Representation inventory
| Representation | What it exposes | First move | Condition | Nearby wrong choice |
|---|---|---|---|---|
| stable ID | exact corpus row | resolve ledger entry | verified corpus | local alias |
| official paper/key URL | source custody | copy canonical URL | HBCSE authority | secondary mirror |
| independent trace | mathematical correctness | recompute without key | promoted anchor | trust key alone |

## E. Decision boundaries
| Similar surface | Route A | Route B | Discriminating question | Why wrong route is tempting |
|---|---|---|---|---|
| official vs secondary source | canonical authority | contextual reference | is source HBCSE official? | mirrors are easier to access |
| mention vs promoted anchor | citation only | independent recomputation | is the item used pedagogically? | answer key seems sufficient |
| mechanism evidence vs weightage claim | local evidence | syllabus claim | is there explicit authority? | recurrence suggests importance |

## F. Misconception/diagnosis catalogue
ERROR_CODE: ALG07-G-01
WRONG_MOVE: infer an official Grade-9 syllabus/weightage from two PYQs.
WHY_TEMPTING: repeated topic occurrence.
MISSING_LINK_CLASS: SOURCE_INTEGRITY
REPAIR_INVARIANT: distinguish corpus evidence from official syllabus authority.
FALSIFIER_OR_CONTRAST: no such authority is present in the anchor custody.

## G. First-move cues
Resolve stable ID and canonical paper/key authority before using historical wording or answer.

## H. H3 -> H0 fading plan
Authoring-only: H3 full source trace; H2 stable ID + authority; H1 ask for custody check; H0 independent recomputation from official statement.

## I. Validated IOQM source anchors
| Stable ID | Year/Q | Source status | Primary/bridge role | Mechanism | Figure? | Key status |
|---|---|---|---|---|---|---|
| IOQM-2024-Q21 | 2024 Q21 | HBCSE_OFFICIAL | primary | invert two floor constraints and intersect digit structure | no | official key verified; answer 91 |
| IOQM-2024-Q26 | 2024 Q26 | HBCSE_OFFICIAL | primary | set `n=floor(x)` and test interval feasibility | no | official key verified; answer 33 |

## J. Source-independent mathematical trace
Q21: `floor(n/9)=111d` gives `999d<=n<=999d+8`; intersecting the admissible four-digit permutation ranges leaves the unique n=8991, hence 91. Q26: with `n=floor(x)`, feasibility of `16+15x+15x^2=n^3` on `[n,n+1)` leaves n=16,17 only; sum 33. Domain, monotonicity and endpoint checks are recorded in `01_Source_Coverage_Map.md`; both agree with the official key.

## K. Contrast-pair candidates
stable ID vs local alias; official source vs secondary mirror; official key vs independent trace; promoted anchor vs mention; corpus evidence vs syllabus claim.

## L. Transfer candidates
T2 stable-ID lookup; T2 source-to-mechanism mapping; T3 cross-topic bridge classification; T3 corrected metadata custody; T4 downstream reuse with original provenance preserved.

## M. Candidate mastery items
Authoring QA only: identify correct stable ID, reproduce numerical checkpoint, explain why key agreement alone is insufficient, verify source authority, detect an unsupported syllabus claim.

## N. Dependency declarations
REQUIRES: frozen corpus and provenance contract. BRIDGE_REQUIRES: none. APPLIES: all topic artifacts. Downstream may reuse verified anchors only with unchanged stable IDs and custody.

## O. Lead integration notes
Keep source-control detail in authoring/teacher materials. Student prose may name year/question where pedagogically useful but must not expose issue/PR/Wave machinery.

## P. Independent QA status
DERIVATIONS_CHECKED: PASS
PROMOTED_NUMERICAL_ANSWERS_CHECKED: PASS
SOURCE_IDS_VERIFIED: PASS
DEPENDENCY_CONFLICTS: NONE
OPEN_ISSUES: none affecting integration
