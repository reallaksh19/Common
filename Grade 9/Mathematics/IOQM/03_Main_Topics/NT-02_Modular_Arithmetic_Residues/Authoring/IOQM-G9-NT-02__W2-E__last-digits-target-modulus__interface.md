---
main_topic_id: IOQM-G9-NT-02
microstream_id: W2-E
microstream_title: Last digits and target-modulus selection
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-NT-02
prerequisite_interfaces: [IOQM-G9-NT-01]
source_cutoff: 2026-09-02
---

## A. Scope boundary
Included: choosing mod 10, 100, 1000 from requested terminal digits and using residue/cycle structure. Excluded: full place-value/divisibility canon belonging to later number-theory work.
## B. Learner-state model
PRIOR_KNOWLEDGE: decimal notation. LIKELY_HALF_KNOWLEDGE: uses mod 10 for any “last digits” request. MISSING_BRIDGE: number of requested terminal digits determines a power-of-10 modulus. OWNERSHIP_TARGET: translate surface wording into the correct residue target before computation.
## C. Mathematical invariant / governing structure
The last k decimal digits of an integer are determined by its residue modulo `10^k`.
## D. Representation inventory
| Representation | What it exposes | First move | Condition | Nearby wrong choice |
|---|---|---|---|---|
| last digit | residue mod 10 | set modulus 10 | decimal representation | expand power |
| last two digits | residue mod 100 | set modulus 100 | decimal representation | use mod 10 |
| stabilizing power | fixed terminal state | inspect small exponents | verified pattern | assume a cycle without checking |
## E. Decision boundaries
| Similar surface | Route A | Route B | Discriminating question | Why wrong route is tempting |
|---|---|---|---|---|
| last digit vs last two digits | mod 10 | mod 100 | how many terminal digits are requested? | “last digit” habits persist |
| cycle vs stabilization | periodic orbit | fixed residue after threshold | do residues rotate or become constant? | both avoid expansion |
## F. Misconception/diagnosis catalogue
ERROR_CODE: NT02-E-01
WRONG_MOVE: compute last two digits using only mod 10.
WHY_TEMPTING: mod 10 is strongly associated with decimal endings.
MISSING_LINK_CLASS: TARGET
REPAIR_INVARIANT: two terminal digits are exactly a residue modulo 100.
FALSIFIER_OR_CONTRAST: 25 and 65 share last digit but not last two digits.
## G. First-move cues
Translate “last k digits” into modulus `10^k` before looking at the exponent.
## H. H3 -> H0 fading plan
H3: state the target modulus. H2: cue “how many digits?” H1: ask what information mod 10 loses. H0: mixed terminal-digit requests with no modulus cue.
## I. Validated IOQM source anchors
`IOQM-2024-Q03` gives the verified `5^k mod 100` stabilization at 25 for k>=2, yielding answer 25.
## J. Source-independent mathematical trace
The Q03 finish is checked directly: `5^2=25`, and multiplying any number ending in 25 by 5 gives a number ending in 25 for subsequent powers.
## K. Contrast-pair candidates
mod 10 vs mod 100; periodic vs stable; terminal digits vs full value; structural cycle vs expansion.
## L. Transfer candidates
place-value filters, digital endings, divisibility constraints, cyclic clock states.
## M. Candidate mastery items
last digit of a huge power; last two digits; identify correct modulus; prove stabilization; contrast two numbers sharing only one terminal digit.
## N. Dependency declarations
REQUIRES: W2-B/D. BRIDGE_REQUIRES: none. Later place-value topics may retrieve target-modulus selection without moving ownership of digit canon here.
## O. Lead integration notes
Teach target-modulus choice as a representation decision, then apply the cycle toolkit.
## P. Independent QA status
DERIVATIONS_CHECKED: PASS
PROMOTED_NUMERICAL_ANSWERS_CHECKED: PASS
SOURCE_IDS_VERIFIED: PASS
DEPENDENCY_CONFLICTS: NONE
OPEN_ISSUES: regenerate learner PDF after source-label repair
