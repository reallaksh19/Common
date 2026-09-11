---
main_topic_id: IOQM-G9-NT-02
microstream_id: W2-C
microstream_title: Inverses and conditional cancellation
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-NT-02
prerequisite_interfaces: [IOQM-G9-NT-01]
source_cutoff: 2026-09-02
---

## A. Scope boundary
Included: modular inverses, invertibility test, legal cancellation and counterexamples. Excluded: re-teaching Euclidean algorithm or full linear-congruence theory beyond Grade-9 depth.
## B. Learner-state model
PRIOR_KNOWLEDGE: gcd and ordinary cancellation. LIKELY_HALF_KNOWLEDGE: cancels any common factor in a congruence. MISSING_BRIDGE: cancellation requires an inverse modulo the chosen modulus. OWNERSHIP_TARGET: ask `gcd(c,m)=1?` before cancelling c.
## C. Mathematical invariant / governing structure
A residue c has a multiplicative inverse modulo m iff `gcd(c,m)=1`. From `ac congruent bc (mod m)`, cancellation of c is valid when c is invertible modulo m.
## D. Representation inventory
| Representation | What it exposes | First move | Condition | Nearby wrong choice |
|---|---|---|---|---|
| `cx congruent d (mod m)` | inverse/cancellation question | compute gcd(c,m) | integers, m>0 | divide by c immediately |
| small modulus | inverse search | test products until 1 | gcd=1 | invoke heavy theorem |
| non-coprime coefficient | multiple solution classes or incompatibility | solve via direct residue analysis | gcd>1 | force unique inverse |
## E. Decision boundaries
| Similar surface | Route A | Route B | Discriminating question | Why wrong route is tempting |
|---|---|---|---|---|
| ordinary cancellation vs modular cancellation | divide in equality | test invertibility | is modulus involved? | algebra habit transfers automatically |
| inverse exists vs no inverse | multiply by inverse | enumerate/normalize classes | gcd(c,m)=1? | coefficient is nonzero |
## F. Misconception/diagnosis catalogue
ERROR_CODE: NT02-C-01
WRONG_MOVE: cancel 2 from `2x congruent 2y (mod 6)`.
WHY_TEMPTING: common factor cancellation is automatic over ordinary equality.
MISSING_LINK_CLASS: LEGALITY
REPAIR_INVARIANT: 2 has no inverse mod 6.
FALSIFIER_OR_CONTRAST: `2*1 congruent 2*4 (mod 6)` but `1` is not congruent to `4 (mod 6)`.
## G. First-move cues
Before modular division or cancellation, test the candidate divisor against the modulus with a gcd.
## H. H3 -> H0 fading plan
H3: provide the gcd/inverse check. H2: cue “is the coefficient invertible?” H1: ask what must be true before cancelling. H0: mixed legal/illegal cases with no label.
## I. Validated IOQM source anchors
Cancellation legality supports the topic’s general toolkit; exact historical anchors are audited in W2-G.
## J. Source-independent mathematical trace
All promoted inverse claims are checked by direct multiplication; illegal-cancellation examples are verified by explicit residue counterexamples.
## K. Contrast-pair candidates
legal vs illegal cancellation; nonzero vs invertible; unique class vs several classes; equality division vs congruence division.
## L. Transfer candidates
linear congruences, simultaneous systems, modular equations arising from digit restrictions.
## M. Candidate mastery items
find an inverse; reject a cancellation; solve a coprime-coefficient congruence; analyze a non-coprime coefficient; produce a counterexample.
## N. Dependency declarations
REQUIRES: W2-A meaning, W2-B operations and prior gcd retrieval. BRIDGE_REQUIRES: gcd computation only. Do not duplicate Euclidean algorithm teaching.
## O. Lead integration notes
Use a falsifying counterexample before formalizing the invertibility criterion; this is the key legal/illegal contrast.
## P. Independent QA status
DERIVATIONS_CHECKED: PASS
PROMOTED_NUMERICAL_ANSWERS_CHECKED: PASS
SOURCE_IDS_VERIFIED: PASS
DEPENDENCY_CONFLICTS: NONE
OPEN_ISSUES: regenerate learner PDF after source-label repair
