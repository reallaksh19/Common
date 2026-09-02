---
main_topic_id: IOQM-G9-NT-04
microstream_id: W3-F
microstream_title: Finite-case completeness and integer reconstruction
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-NT-04
prerequisite_interfaces: [IOQM-G9-NT-04__W3-A__factorisation-finite-cases__interface, IOQM-G9-NT-04__W3-B__gcd-parity-filters__interface, IOQM-G9-NT-04__W3-C__bounds-feasibility__interface]
source_cutoff: 2026-09-02
---

# Finite-case completeness and integer reconstruction - Research Interface

## A. Scope boundary
Included: proving a candidate generator is exhaustive; reconstructing original variables; normalising unordered representations; checking necessary vs sufficient conditions; applying final optimization or uniqueness after reconstruction. Includes sum/product representation via multiplicative partitions. Excluded: general combinatorial partition theory and NT-03 prime-factor teaching.

## B. Learner-state model
`PRIOR_KNOWLEDGE:` learner can solve individual candidate cases.

`LIKELY_HALF_KNOWLEDGE:` learner stops after finding one working solution or after a plausible finite list.

`MISSING_BRIDGES:` explicit exhaustiveness argument; normalize equivalent representations; original-equation check after one-way steps; separate existence, uniqueness and optimization.

`OWNERSHIP_TARGET:` finish Diophantine arguments with a completeness certificate, not just examples.

## C. Mathematical invariant / governing structure
**Invariant:** `GENERATOR + FILTERS + RECONSTRUCTION + ORIGINAL CHECK = COMPLETE SOLUTION SET`.

A finite-case proof has four obligations:
1. **Generator:** every true solution determines a parameter from a finite set.
2. **Filters:** necessary sign/parity/gcd/order conditions remove candidates.
3. **Reconstruction:** recover all original variables without losing branches.
4. **Sufficiency check:** substitute survivors into the original conditions.

For sum=product representations, remove all entries equal to 1. The remaining factors `b_i>=2` form an unordered multiplicative partition of n. Once the partition is fixed, the number of ones is forced: `t=n-sum(b_i)`. Thus uniqueness becomes uniqueness of the feasible multiplicative partition after normalising order.

## D. Representation inventory
| Representation | What it exposes | First move | Condition | Nearby wrong choice |
|---|---|---|---|---|
| candidate list | proof obligations | label generator/filter/check | generator exhaustive | "found one" |
| transformed variables | original variables | invert substitution | branch/domain preserved | forget shifted sign |
| unordered factor multiset | representation uniqueness | sort factors/remove ones | product fixed | count permutations as different |
| optimization | finite survivors | evaluate target on all survivors | complete set first | optimize before reconstruction |

## E. Decision boundaries
| Similar surface | Route A | Route B | Discriminating question | Why wrong route is tempting |
|---|---|---|---|---|
| one working solution | existence | complete solution | Does question ask all/max/unique? | success feels final |
| necessary filter | candidate generation | sufficiency | Was the original equation rechecked? | transformed relation is simpler |
| ordered tuple | normalized representation | raw arrangements | Does order matter? | algebra produces ordered variables |
| max/min | evaluate survivors | optimize relaxation | Is feasible set complete? | target invites optimization first |

## F. Misconception / diagnosis catalogue
`NT04-CMP-01`
- WRONG_MOVE: stop after first valid solution.
- WHY_TEMPTING: contest answer may be numerical.
- MISSING_LINK_CLASS: INVARIANT.
- REPAIR_INVARIANT: maximum/uniqueness still requires exclusion of all better/other candidates.
- FALSIFIER_OR_CONTRAST: two candidates can give the same current value.

`NT04-CMP-02`
- WRONG_MOVE: count permutations of one multiplicative partition as distinct representations.
- WHY_TEMPTING: tuples look ordered.
- MISSING_LINK_CLASS: REPRESENTATION.
- REPAIR_INVARIANT: normalize according to the problem's order convention.
- FALSIFIER_OR_CONTRAST: 5*19 and 19*5 are one descending representation.

`NT04-CMP-03`
- WRONG_MOVE: infer sufficiency from an isolated divisibility condition.
- WHY_TEMPTING: it produced a tiny candidate set.
- MISSING_LINK_CLASS: DOMAIN_CONDITION.
- REPAIR_INVARIANT: check the original system.
- FALSIFIER_OR_CONTRAST: 2024-Q13 c=14 passes divisibility but violates `a>c` after reconstruction.

## G. First-move cues
- find all / largest / unique -> write the generator and completeness sentence before the final target.
- transformed factor pair -> invert all substitutions explicitly.
- sum equals product -> remove ones and pass to an unordered multiplicative partition.
- candidate survives necessary filters -> substitute into the original conditions.

## H. H3 -> H0 fading plan
- **H3:** complete a table: generator -> filter -> reconstruct -> check.
- **H2:** give factor candidates; learner supplies completeness and original checks.
- **H1:** ask only "what proves there are no other cases?"
- **H0:** changed-surface uniqueness problem requiring normalization of representations.

## I. Validated IOQM source anchors
| Stable ID | Year/Q | Source status | Role | Mechanism | Figure? | Key status |
|---|---|---|---|---|---|---|
| `IOQM-2024-Q13` | 2024/13 | CLEAN_OFFICIAL | primary | reconstruction after divisor cases | no | OFFICIAL_HBCSE_KEY |
| `IOQM-2023-Q11` | 2023/11 | CLEAN_VALIDATED | bridge | reconstruct from factor pairs | no | EMBEDDED_KEY |
| `IOQM-2023-Q29` | 2023/29 | CLEAN_VALIDATED | primary | representation uniqueness | no | EMBEDDED_KEY |

## J. Source-independent mathematical trace
- **2024-Q13:** c=2,6,14 are complete because `c-1|65`; reconstructing a,b and checking positivity/order leaves only a=19.
- **2023-Q11:** factor pairs of 231 are complete; parity/integrality reconstruct exactly four solution pairs, max difference 14.
- **2023-Q29:** representation <-> feasible unordered multiplicative partition is two-way; checking 99,98,97,96 then 95 proves 95 is the largest beautiful number below 100.

## K. Contrast-pair candidates
1. existence vs completeness;
2. candidate vs solution;
3. ordered tuple vs normalized representation;
4. necessary condition vs sufficient original check;
5. optimize first vs optimize after finite reconstruction.

## L. Transfer candidates
- **T2:** integer tiling dimensions reconstructed from a factor multiset.
- **T2:** sum/product equation with forced ones.
- **T3:** encoding context where order equivalence must be normalized.
- **T4:** geometry integer candidates filtered then checked against triangle feasibility.

## M. Candidate mastery items
- Recognition: identify which proposed argument fails because it lacks completeness.
- First-line: state the finite generator for a transformed equation.
- Full solve: classify positive integer solutions to a shifted product plus sum bound.
- Full solve: determine uniqueness of a sum=product representation for a selected n.
- WHY-NOT: reject "I found one representation, therefore unique."
- Verification: reconstruct every original variable and mark which original condition each check closes.

## N. Dependency declarations
`REQUIRES:` all prior NT-04 finite generators and filters.

`BRIDGE_REQUIRES:` NT-03 factor structure for multiplicative partitions.

`APPLIES:` order normalization and optimization.

`EXPORTS:` completeness certificate language and reconstruction/check protocol for downstream integer applications.

## O. Lead integration notes
This stream supplies the ending discipline for every earlier method rather than an isolated final chapter. The integrated book should repeatedly use a short "complete because..." sentence. Sum/product uniqueness belongs late, after factorisation and normalization habits are stable.

## P. Independent QA status
DERIVATIONS_CHECKED: PASS
PROMOTED_NUMERICAL_ANSWERS_CHECKED: PASS
SOURCE_IDS_VERIFIED: PASS
DEPENDENCY_CONFLICTS: NONE
OPEN_ISSUES: NONE
