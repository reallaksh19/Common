---
main_topic_id: IOQM-G9-NT-02
microstream_id: W2-F
microstream_title: Simultaneous congruences and compatibility
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-NT-02
prerequisite_interfaces: [IOQM-G9-NT-01]
source_cutoff: 2026-09-02
---

## A. Scope boundary
Included: solving two small congruences by listing/parametrization, combined period, and gcd compatibility for non-coprime moduli. Excluded: general CRT theorem machinery as required Grade-9 doctrine.
## B. Learner-state model
PRIOR_KNOWLEDGE: residue classes and lcm/gcd retrieval. LIKELY_HALF_KNOWLEDGE: assumes every pair of congruences has a solution or quotes a theorem without checking compatibility. MISSING_BRIDGE: shared-factor moduli require residue agreement modulo the gcd. OWNERSHIP_TARGET: compatibility first, then construct a repeating combined class.
## C. Mathematical invariant / governing structure
If `x congruent a (mod m)` and `x congruent b (mod n)`, compatibility requires `a congruent b (mod gcd(m,n))`; when a solution exists, the solution class repeats modulo `lcm(m,n)`.
## D. Representation inventory
| Representation | What it exposes | First move | Condition | Nearby wrong choice |
|---|---|---|---|---|
| two residue lists | intersection | list one short period | small moduli | search unboundedly |
| parametrized class `x=a+mk` | one-variable reduction | substitute in other congruence | integers k | quote theorem first |
| shared-factor moduli | compatibility | compare residues mod gcd | gcd>1 | assume solution |
## E. Decision boundaries
| Similar surface | Route A | Route B | Discriminating question | Why wrong route is tempting |
|---|---|---|---|---|
| coprime vs non-coprime moduli | construct directly | compatibility then construct | do moduli share a factor? | examples often use coprime moduli |
| existence vs uniqueness class | prove compatibility | find representative and period | does a solution exist first? | solving impulse skips feasibility |
## F. Misconception/diagnosis catalogue
ERROR_CODE: NT02-F-01
WRONG_MOVE: assert a solution to `x congruent 1 (mod 4)`, `x congruent 2 (mod 6)`.
WHY_TEMPTING: memorized CRT reflex.
MISSING_LINK_CLASS: FEASIBILITY
REPAIR_INVARIANT: residues must agree mod `gcd(4,6)=2`.
FALSIFIER_OR_CONTRAST: 1 and 2 disagree mod 2, so no integer can satisfy both.
## G. First-move cues
If two congruences appear, check shared-factor compatibility before constructing a representative.
## H. H3 -> H0 fading plan
H3: provide gcd compatibility check and parametrization. H2: cue “test one class in the other.” H1: ask whether the residue requests agree on shared factors. H0: mixed compatible/incompatible systems.
## I. Validated IOQM source anchors
The core historical anchors are power-residue problems; simultaneous systems are source-independent authored transfer within topic scope and are independently checked.
## J. Source-independent mathematical trace
All promoted simultaneous systems are verified by substitution and by checking the full repeating period modulo the lcm.
## K. Contrast-pair candidates
compatible vs incompatible; coprime vs shared-factor moduli; list vs parametrization; existence vs construction.
## L. Transfer candidates
clock-state intersections, digit constraints, parity-plus-residue filters, scheduling cycles.
## M. Candidate mastery items
solve coprime pair; prove incompatibility; solve shared-factor compatible pair; state combined period; compare two solution methods.
## N. Dependency declarations
REQUIRES: W2-A/B and prior gcd/lcm retrieval. BRIDGE_REQUIRES: gcd/lcm values only. Do not reteach their canonical derivations.
## O. Lead integration notes
Use small constructive methods first. Mention general theorem language only as optional naming after the compatibility idea is secure.
## P. Independent QA status
DERIVATIONS_CHECKED: PASS
PROMOTED_NUMERICAL_ANSWERS_CHECKED: PASS
SOURCE_IDS_VERIFIED: PASS
DEPENDENCY_CONFLICTS: NONE
OPEN_ISSUES: regenerate learner PDF after source-label repair
