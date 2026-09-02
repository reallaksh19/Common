---
main_topic_id: IOQM-G9-NT-01
microstream_id: W1-B
microstream_title: Euclidean algorithm
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-NT-01
prerequisite_interfaces: [IOQM-G9-NT-01__W1-A__divisibility-algebra__interface.md]
source_cutoff: 2026-08-31
---

## A. Scope boundary
Included: Euclidean reduction, gcd invariance under remainder replacement and efficient computation. Excluded: prime factorization as a required route and extended-Euclid coefficient canon beyond what local divisibility arguments need.
## B. Learner-state model
PRIOR_KNOWLEDGE: division algorithm. LIKELY_HALF_KNOWLEDGE: knows HCF by factor lists. MISSING_BRIDGES: why replacing `(a,b)` by `(b,r)` preserves gcd. OWNERSHIP_TARGET: see Euclid as structural reduction, not a memorized table.
## C. Mathematical invariant / governing structure
If `a=qb+r`, then `gcd(a,b)=gcd(b,r)` because common divisors of a,b are exactly common divisors of b,r.
## D. Representation inventory
| Representation | What it exposes | First move | Condition | Nearby wrong choice |
|---|---|---|---|---|
| division equation | smaller remainder | replace pair by `(b,r)` | integers; 0<=r<|b| | fully factor both numbers |
| gcd chain | monotone size reduction | continue until remainder 0 | b nonzero | stop at first small remainder |
| common-divisor proof | invariant | use `r=a-qb` and `a=qb+r` | integers | cite algorithm without reason |
## E. Decision boundaries
| Similar surface | Route A | Route B | Discriminating question | Why wrong route is tempting |
|---|---|---|---|---|
| Euclid vs prime factorization | remainder reduction | factorization | are numbers large/awkward? | factor method is familiar |
| computation vs proof | iterate | show common-divisor equivalence | is justification requested? | same steps appear |
| gcd vs lcm | Euclid | reconstruct lcm later | which target is primary? | gcd/lcm are paired in textbooks |
## F. Misconception/diagnosis catalogue
ERROR_CODE: NT01-B-01
WRONG_MOVE: completely factor `123456` and `7890` before finding gcd.
WHY_TEMPTING: school HCF procedure.
MISSING_LINK_CLASS: REPRESENTATION
REPAIR_INVARIANT: use repeated division because gcd survives remainder replacement.
FALSIFIER_OR_CONTRAST: Euclid reaches gcd 6 directly.
## G. First-move cues
For a large gcd target, divide the larger integer by the smaller and keep the remainder.
## H. H3 -> H0 fading plan
H3: give first division equation. H2: cue remainder replacement. H1: ask what smaller pair has the same gcd. H0: changed large-number gcd.
## I. Validated IOQM source anchors
No historical anchor is owned solely by Euclid in this package; source custody remains W1-F.
## J. Source-independent mathematical trace
The gcd-invariance proof is reconstructed from common-divisor equivalence; authored numerical gcds in the key are independently checked.
## K. Contrast-pair candidates
Euclid vs factorization; division equation vs gcd statement; proof vs procedure; gcd target vs lcm target; remainder zero vs nonzero continuation.
## L. Transfer candidates
large-number gcd; same-remainder difference gcd; coefficient elimination pre-reduction; gcd reconstruction; algorithmic proof.
## M. Candidate mastery items
recognition; first division line; full Euclid computation; WHY-NOT full factorization; proof of invariant.
## N. Dependency declarations
REQUIRES: W1-A divisibility algebra and division algorithm. BRIDGE_REQUIRES: none. APPLIES: all gcd computations. Downstream may assume Euclidean reduction and its invariant.
## O. Lead integration notes
Teach proof once, then compress to efficient use. Do not turn this into an algorithm-only reference sheet.
## P. Independent QA status
DERIVATIONS_CHECKED: PASS
PROMOTED_NUMERICAL_ANSWERS_CHECKED: PASS
SOURCE_IDS_VERIFIED: PASS
DEPENDENCY_CONFLICTS: NONE
OPEN_ISSUES: current PDF must be regenerated after learner-source repair
