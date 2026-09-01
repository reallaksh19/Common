---
main_topic_id: IOQM-G9-ALG-01
microstream_id: W1-C
microstream_title: Symmetric identities and reconstruction
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-ALG-01
prerequisite_interfaces: []
source_cutoff: 2026-08-31
---

## A. Scope boundary
Included: reconstruct symmetric targets from sums/products/differences without solving individual variables. Excluded: Vieta/discriminant canon (ALG-03) and inequality equality doctrine (ALG-02).
## B. Learner-state model
PRIOR_KNOWLEDGE: identities. LIKELY_HALF_KNOWLEDGE: solves for variables unnecessarily. MISSING_BRIDGES: target expressed directly in symmetric invariants. OWNERSHIP_TARGET: reconstruct only what the target needs.
## C. Mathematical invariant / governing structure
Symmetric expressions can often be written in terms of `s=a+b` and `p=ab`, e.g. `a^2+b^2=s^2-2p`, `a^3+b^3=s^3-3ps`.
## D. Representation inventory
| Representation | What it exposes | First move | Condition | Nearby wrong choice |
|---|---|---|---|---|
| sum/product data | symmetric invariants | rewrite target in s,p | symmetric target | solve a,b |
| difference/product data | sum square | `(u+v)^2=(u-v)^2+4uv` | squared target | choose sign prematurely |
| reciprocal sum | symmetric powers | define S_n | nonzero variable | solve roots individually |
## E. Decision boundaries
| Similar surface | Route A | Route B | Discriminating question | Why wrong route is tempting |
|---|---|---|---|---|
| symmetric target vs individual values | reconstruct | solve variables | is target invariant under swap? | roots feel concrete |
| signed difference vs squared difference | insufficient sign | invariant magnitude | is order specified? | magnitude looks like value |
| sum/product algebra vs Vieta canon | direct identities | polynomial-root theory | is polynomial theory needed? | same formulas resemble Vieta |
## F. Misconception/diagnosis catalogue
ERROR_CODE: ALG01-C-01
WRONG_MOVE: solve individual variables before evaluating a symmetric target.
WHY_TEMPTING: complete solution feels safer.
MISSING_LINK_CLASS: INVARIANT
REPAIR_INVARIANT: express target directly in known symmetric data.
FALSIFIER_OR_CONTRAST: swap variables; target stays unchanged.
## G. First-move cues
If the target is unchanged by swapping variables, try sum/product reconstruction before root solving.
## H. H3 -> H0 fading plan
H3: provide identity. H2: cue sum/product. H1: ask whether target is symmetric. H0: changed context with no hint.
## I. Validated IOQM source anchors
`IOQM-2024-Q11` is a target-reconstruction anchor; source custody is W1-F.
## J. Source-independent mathematical trace
All promoted symmetric identities are algebraically expanded/rechecked; signed-target limitations are explicit.
## K. Contrast-pair candidates
symmetric vs signed target; reconstruct vs solve; sum/product vs difference/product; root theory vs elementary identities; reciprocal powers vs individual roots.
## L. Transfer candidates
rectangle perimeter/area; reciprocal powers; zero-sum cubic; signed-difference boundary; downstream polynomial bridge.
## M. Candidate mastery items
recognition; first-line identity; full reconstruction; WHY-NOT root solving; insufficient-sign diagnosis.
## N. Dependency declarations
REQUIRES: identities and F0 algebra. BRIDGE_REQUIRES: none. APPLIES: power reduction and source anchors. Downstream may assume elementary symmetric reconstruction only.
## O. Lead integration notes
Do not rebrand elementary reconstruction as Vieta; keep ALG-03 ownership clean.
## P. Independent QA status
DERIVATIONS_CHECKED: PASS
PROMOTED_NUMERICAL_ANSWERS_CHECKED: PASS
SOURCE_IDS_VERIFIED: PASS
DEPENDENCY_CONFLICTS: NONE
OPEN_ISSUES: current PDF must be regenerated after source repair
