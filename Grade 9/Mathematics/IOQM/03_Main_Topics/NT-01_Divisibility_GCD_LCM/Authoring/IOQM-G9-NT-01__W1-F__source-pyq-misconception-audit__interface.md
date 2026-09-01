---
main_topic_id: IOQM-G9-NT-01
microstream_id: W1-F
microstream_title: Source, PYQ and misconception audit
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-NT-01
prerequisite_interfaces: []
source_cutoff: 2026-08-31
---

## A. Scope boundary
Included: canonical source custody, independent traces and misconception audit for `IOQM-2025-Q02` and `IOQM-2025-Q27`. Excluded: local historical aliases, unsupported syllabus/weightage claims and downstream modular/prime-exponent canon.
## B. Learner-state model
PRIOR_KNOWLEDGE: not applicable to source custody. LIKELY_HALF_KNOWLEDGE: not applicable. MISSING_BRIDGES: lead needs exact provenance and ownership boundaries separated from student prose. OWNERSHIP_TARGET: auditable source integration.
## C. Mathematical invariant / governing structure
Historical anchors are promoted only when canonical stable ID, exact paper/key authority and an independent mathematical trace agree. A cross-tagged historical problem does not transfer all neighboring canon into NT-01.
## D. Representation inventory
| Representation | What it exposes | First move | Condition | Nearby wrong choice |
|---|---|---|---|---|
| stable ID | exact corpus row | use canonical `IOQM-YYYY-QNN` | historical item | local alias |
| official URLs | source custody | copy frozen ledger fields | HBCSE source | secondary mirror |
| independent trace | mathematical correctness | recompute mechanism | promoted anchor | trust key alone |
## E. Decision boundaries
| Similar surface | Route A | Route B | Discriminating question | Why wrong route is tempting |
|---|---|---|---|---|
| historical relation vs authored variant | preserve exact source | make self-contained new item | is wording historical or author-created? | reference shorthand is convenient |
| NT-01 mechanism vs downstream notation | divisibility/gcd/lcm | NT-02/NT-03 canon | what is decisive mechanism? | source is cross-domain |
| corpus evidence vs official syllabus | evidence only | syllabus claim | is there explicit authority? | recurrence suggests weightage |
## F. Misconception/diagnosis catalogue
ERROR_CODE: NT01-F-01
WRONG_MOVE: author a practice item saying only “the same lcm relation as the 2025 anchor.”
WHY_TEMPTING: avoids restating a long equation.
MISSING_LINK_CLASS: SOURCE_INTEGRITY
REPAIR_INVARIANT: author-created practice must be self-contained; Practice #23 now states `27(lcm(a,c)+lcm(b,c))=26c(a+b)` explicitly.
FALSIFIER_OR_CONTRAST: the repaired item can be solved without opening the historical paper.
## G. First-move cues
Resolve canonical source custody before historical use; for authored transfer items, restate all mathematical premises needed to solve them.
## H. H3 -> H0 fading plan
Authoring-only: full source trace; then stable ID/authority; then ownership cue; finally independent source reconstruction.
## I. Validated IOQM source anchors
| Stable ID | Year/Q | Source status | Primary/bridge role | Mechanism | Figure? | Key status |
|---|---|---|---|---|---|---|
| IOQM-2025-Q02 | 2025 Q02 | HBCSE_OFFICIAL | bridge | divisibility counting | no | FINAL_OFFICIAL; answer 17 |
| IOQM-2025-Q27 | 2025 Q27 | HBCSE_OFFICIAL | primary | lcm equation; gcd normalization; integer triples | no | FINAL_OFFICIAL; answer 40 |
## J. Source-independent mathematical trace
Q02: multiples of 3 up to 100 are 33; those also divisible by 2 are 16 multiples of 6; result 17. Q27: set `x=gcd(a,c)`, `y=gcd(b,c)`, reduce to `a(27/x-26)+b(27/y-26)=0`; exactly one of x,y is 1, the other is forced to 2 under the bound, giving symmetric core pairs and 40 total admissible triples. Both agree with the final official key.
## K. Contrast-pair candidates
canonical ID vs local alias; historical wording vs self-contained authored variant; source key vs independent trace; primary mechanism vs bridge domain; corpus evidence vs syllabus claim.
## L. Transfer candidates
source-to-mechanism mapping; self-contained variant construction; downstream modular bridge; metadata validation; misconception/source-integrity diagnosis.
## M. Candidate mastery items
Authoring QA: verify stable ID; reproduce anchor numerical checkpoint; detect non-self-contained variant; explain ownership boundary; verify official authority.
## N. Dependency declarations
REQUIRES: frozen corpus/provenance contract. BRIDGE_REQUIRES: none. APPLIES: all topic source/metadata artifacts. Downstream reuse must preserve IDs and source authority.
## O. Lead integration notes
Practice #23 is now self-contained. Keep issue/PR/Wave/topic-code and transfer-level labels out of student prose; retain them only in authoring/metadata where needed.
## P. Independent QA status
DERIVATIONS_CHECKED: PASS
PROMOTED_NUMERICAL_ANSWERS_CHECKED: PASS
SOURCE_IDS_VERIFIED: PASS
DEPENDENCY_CONFLICTS: NONE
OPEN_ISSUES: current PDF must be regenerated and independently inspected after learner-source repair
