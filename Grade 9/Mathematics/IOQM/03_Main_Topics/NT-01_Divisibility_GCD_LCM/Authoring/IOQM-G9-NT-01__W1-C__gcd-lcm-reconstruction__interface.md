---
main_topic_id: IOQM-G9-NT-01
microstream_id: W1-C
microstream_title: GCD/LCM identities and reconstruction
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-NT-01
prerequisite_interfaces: [IOQM-G9-NT-01__W1-A__divisibility-algebra__interface.md]
source_cutoff: 2026-08-31
---

## A. Scope boundary
Included: `gcd(a,b)lcm(a,b)=ab`, normalization by the gcd, coprime residual factors and lcm reconstruction. Excluded: general prime-exponent/divisor-count canon owned by NT-03.
## B. Learner-state model
PRIOR_KNOWLEDGE: can compute routine gcd/lcm. LIKELY_HALF_KNOWLEDGE: knows product identity as a formula but not when it is enough or how to reconstruct pairs. MISSING_BRIDGES: normalize `a=gu,b=gv`, enforce `gcd(u,v)=1`. OWNERSHIP_TARGET: distinguish product-only target from pair reconstruction.
## C. Mathematical invariant / governing structure
For positive integers, `gcd(a,b)lcm(a,b)=ab`. If `g=gcd(a,b)`, write `a=gu,b=gv` with `gcd(u,v)=1`; then `uv=lcm(a,b)/g`.
## D. Representation inventory
| Representation | What it exposes | First move | Condition | Nearby wrong choice |
|---|---|---|---|---|
| given gcd/lcm | fixed product | use `ab=gL` | positive integers | assume pair is `(g,L)` |
| normalized pair | coprime residual split | set `a=gu,b=gv` | g known | list arbitrary factor pairs |
| one number known | missing partner | use product then verify | positive integers | skip gcd/lcm check |
## E. Decision boundaries
| Similar surface | Route A | Route B | Discriminating question | Why wrong route is tempting |
|---|---|---|---|---|
| product target vs pair target | stop at gL | normalize residuals | what is actually asked? | pair feels more complete |
| arbitrary factors vs coprime split | enforce gcd(u,v)=1 | any uv factorization | must gcd be exactly g? | product condition alone looks sufficient |
| gcd/lcm identity vs NT-03 exponents | elementary identity | prime-exponent canon | are exponent counts needed? | lcm/gcd often taught via primes |
## F. Misconception/diagnosis catalogue
ERROR_CODE: NT01-C-01
WRONG_MOVE: conclude gcd 12 and lcm 420 force `(12,420)` only.
WHY_TEMPTING: endpoints themselves satisfy the product identity.
MISSING_LINK_CLASS: INVARIANT
REPAIR_INVARIANT: normalize by g and split `L/g` into coprime residual factors.
FALSIFIER_OR_CONTRAST: `(60,84)` has the same gcd and lcm.
## G. First-move cues
If only `ab` is requested, write `ab=gcd(a,b)lcm(a,b)` and stop after evaluation. If the pair is requested, normalize by the gcd.
## H. H3 -> H0 fading plan
H3: give product identity and normalization. H2: cue `a=gu,b=gv`. H1: ask whether the target is product or pair. H0: changed gcd/lcm reconstruction problem.
## I. Validated IOQM source anchors
`IOQM-2025-Q27` uses lcm/gcd normalization as its decisive mechanism; exact source audit is W1-F.
## J. Source-independent mathematical trace
Product/reconstruction identities are independently derived from gcd normalization. Q27=40 remains independently verified without importing divisor-count canon.
## K. Contrast-pair candidates
gcd vs lcm; product target vs pair reconstruction; arbitrary factor split vs coprime split; one number known vs both unknown; elementary identity vs prime-exponent method.
## L. Transfer candidates
pair reconstruction; known-partner problem; lcm equation normalization; integer-factor context; downstream prime-exponent handoff.
## M. Candidate mastery items
recognition; first invariant; full pair reconstruction; WHY-NOT `(g,L)` uniqueness; verification of reconstructed pair.
## N. Dependency declarations
REQUIRES: W1-A and elementary gcd/lcm meaning. BRIDGE_REQUIRES: none. APPLIES: source Q27 and reconstruction practice. Downstream may assume product identity and coprime normalization.
## O. Lead integration notes
Teach product identity with decision boundary, not as an isolated formula. Keep NT-03 prime-exponent/divisor canon out.
## P. Independent QA status
DERIVATIONS_CHECKED: PASS
PROMOTED_NUMERICAL_ANSWERS_CHECKED: PASS
SOURCE_IDS_VERIFIED: PASS
DEPENDENCY_CONFLICTS: NONE
OPEN_ISSUES: current PDF must be regenerated after learner-source repair
