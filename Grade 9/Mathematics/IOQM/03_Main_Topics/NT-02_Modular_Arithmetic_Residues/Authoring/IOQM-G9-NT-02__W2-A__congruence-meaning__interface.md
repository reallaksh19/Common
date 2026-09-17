---
main_topic_id: IOQM-G9-NT-02
microstream_id: W2-A
microstream_title: Congruence meaning and residue classes
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-NT-02
prerequisite_interfaces: [IOQM-G9-NT-01]
source_cutoff: 2026-09-02
---

## A. Scope boundary
Included: congruence as equality of residue class and as divisibility of a difference. Excluded: Euclidean algorithm/gcd-lcm canon, which is retrieved from prior divisibility work.
## B. Learner-state model
PRIOR_KNOWLEDGE: remainders and divisibility. LIKELY_HALF_KNOWLEDGE: treats congruence as ordinary equality or as a divisibility test on one number. MISSING_BRIDGE: the modulus defines the equivalence relation. OWNERSHIP_TARGET: move fluently between `a congruent b (mod m)`, equal remainders and `m|(a-b)`.
## C. Mathematical invariant / governing structure
`a congruent b (mod m)` iff `m|(a-b)`. Congruence depends on the modulus and represents membership in the same residue class.
## D. Representation inventory
| Representation | What it exposes | First move | Condition | Nearby wrong choice |
|---|---|---|---|---|
| congruence notation | residue-class equality | subtract representatives | positive modulus | treat as ordinary equality |
| divisibility of difference | proof certificate | factor/check multiple of m | integers | test each number separately |
| residue list | finite state space | reduce to `0,...,m-1` | fixed modulus | retain huge representatives |
## E. Decision boundaries
| Similar surface | Route A | Route B | Discriminating question | Why wrong route is tempting |
|---|---|---|---|---|
| equality vs congruence | exact equality | same residue mod m | is a modulus part of the claim? | equality notation is more familiar |
| divisibility vs congruence | `m|a` | `m|(a-b)` | is the target a number or a difference? | both use divisibility language |
## F. Misconception/diagnosis catalogue
ERROR_CODE: NT02-A-01
WRONG_MOVE: infer `17=5` from `17 congruent 5 (mod 12)`.
WHY_TEMPTING: congruence resembles equality.
MISSING_LINK_CLASS: MEANING
REPAIR_INVARIANT: subtract and recover the modulus-divisibility statement.
FALSIFIER_OR_CONTRAST: `17-5=12` certifies congruence without ordinary equality.
## G. First-move cues
When you see congruence, name the modulus and ask what the difference is divisible by.
## H. H3 -> H0 fading plan
H3: state the difference-divisibility equivalence. H2: cue “subtract the representatives.” H1: ask what same remainder means. H0: changed numbers/modulus with no method label.
## I. Validated IOQM source anchors
`IOQM-2024-Q03`, `IOQM-2024-Q23` and `IOQM-2025-Q20` all rely on residue-class interpretation; exact source custody is W2-G.
## J. Source-independent mathematical trace
Every promoted congruence example is checked by direct difference divisibility or explicit remainder reduction.
## K. Contrast-pair candidates
equality vs congruence; divisibility of one number vs divisibility of a difference; representative vs residue class.
## L. Transfer candidates
collision conditions, parity classes, cyclic state compression, place-value residues.
## M. Candidate mastery items
translate notation; prove a congruence; reject an equality reflex; choose the modulus; compare two equivalent forms.
## N. Dependency declarations
REQUIRES: divisibility meaning from prior number-theory interface. BRIDGE_REQUIRES: none. Downstream may assume congruence/divisibility translation without reteaching gcd/lcm.
## O. Lead integration notes
Use this as the semantic entry point before operational rules. Keep prerequisite retrieval to one concise bridge.
## P. Independent QA status
DERIVATIONS_CHECKED: PASS
PROMOTED_NUMERICAL_ANSWERS_CHECKED: PASS
SOURCE_IDS_VERIFIED: PASS
DEPENDENCY_CONFLICTS: NONE
OPEN_ISSUES: regenerate learner PDF after source-label repair
