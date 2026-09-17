---
main_topic_id: IOQM-G9-NT-01
microstream_id: W1-D
microstream_title: Same remainder and differences
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-NT-01
prerequisite_interfaces: [IOQM-G9-NT-01__W1-A__divisibility-algebra__interface.md]
source_cutoff: 2026-08-31
---

## A. Scope boundary
Included: equal remainders imply divisibility of differences; unknown-divisor problems route to gcd of differences; prescribed-remainder number construction routes to common multiples after subtracting the remainder. Excluded: congruence notation/cycle canon owned by NT-02.
## B. Learner-state model
PRIOR_KNOWLEDGE: division with remainder, gcd/lcm. LIKELY_HALF_KNOWLEDGE: hears “same remainder” and always chooses lcm. MISSING_BRIDGES: distinguish unknown divisor from unknown number. OWNERSHIP_TARGET: correct fork from remainder language to divisor/multiple structure.
## C. Mathematical invariant / governing structure
If integers a,b leave the same remainder on division by d, then `d|(a-b)`. For many numbers, an unknown common divisor must divide every pairwise difference. If instead N is unknown and leaves prescribed remainder r modulo several divisors, then `N-r` is a common multiple of those divisors.
## D. Representation inventory
| Representation | What it exposes | First move | Condition | Nearby wrong choice |
|---|---|---|---|---|
| same remainder; d unknown | common divisor of differences | subtract numbers | same divisor d | take lcm |
| prescribed remainder; N unknown | common multiple after shift | write `N-r` | fixed r | gcd differences |
| equal spacing/offset | same-remainder model | take position differences | integer units | synchronize via lcm |
## E. Decision boundaries
| Similar surface | Route A | Route B | Discriminating question | Why wrong route is tempting |
|---|---|---|---|---|
| unknown divisor vs unknown number | gcd differences | lcm construction | what is unknown? | both mention remainders |
| largest spacing vs first synchronization | gcd | lcm | divisor target or multiple target? | both are periodic contexts |
| divisibility language vs congruence notation | `d|(a-b)` | NT-02 residue notation | is modular notation needed? | notation is concise |
## F. Misconception/diagnosis catalogue
ERROR_CODE: NT01-D-01
WRONG_MOVE: use lcm for the greatest divisor giving the same remainder on 437,581,725.
WHY_TEMPTING: remainder problems are associated with cycles/multiples.
MISSING_LINK_CLASS: RECOGNITION
REPAIR_INVARIANT: equal remainders make the divisor divide differences.
FALSIFIER_OR_CONTRAST: differences are 144,144, so the greatest divisor is 144.
## G. First-move cues
Ask “Is the unknown the divisor, or the number being constructed?” Unknown divisor: subtract the given numbers. Unknown number with prescribed remainder: subtract the remainder from N.
## H. H3 -> H0 fading plan
H3: state the correct transformed divisibility equation. H2: cue unknown-divisor/unknown-number fork. H1: ask what the unknown represents. H0: changed context with no method label.
## I. Validated IOQM source anchors
No anchor is promoted solely here; the structure supports downstream modular retrieval while source custody remains W1-F.
## J. Source-independent mathematical trace
The equal-remainder implication follows by writing `a=qd+r`, `b=pd+r` and subtracting. Authored gcd/lcm remainder answers in the teacher key are independently checked.
## K. Contrast-pair candidates
same-remainder divisor vs prescribed-remainder number; gcd vs lcm; spacing vs synchronization; difference divisibility vs raw remainder arithmetic; divisibility language vs modular notation.
## L. Transfer candidates
route markings; machine synchronization; equal offsets; prescribed-remainder construction; modular downstream bridge.
## M. Candidate mastery items
recognition fork; first-line difference; full gcd/lcm remainder solve; WHY-NOT wrong operation; context-transfer explanation.
## N. Dependency declarations
REQUIRES: W1-A and elementary gcd/lcm. BRIDGE_REQUIRES: none. APPLIES: spacing and remainder construction. NT-02 may retrieve `d|(a-b)` as the same-residue bridge without requiring NT-01 to teach congruence notation.
## O. Lead integration notes
Make this fork explicit and repeated. Keep internal topic/transfer codes out of student prose.
## P. Independent QA status
DERIVATIONS_CHECKED: PASS
PROMOTED_NUMERICAL_ANSWERS_CHECKED: PASS
SOURCE_IDS_VERIFIED: PASS
DEPENDENCY_CONFLICTS: NONE
OPEN_ISSUES: current PDF must be regenerated after learner-source repair
