---
main_topic_id: IOQM-G9-ALG-01
microstream_id: W1-B
microstream_title: Strategic substitutions
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-ALG-01
prerequisite_interfaces: []
source_cutoff: 2026-08-31
---

## A. Scope boundary
Included: naming repeated algebraic blocks when the substitution reduces repetition/degree and preserves recoverable restrictions. Excluded: functional-equation canon (ALG-05) and general polynomial substitution theory.
## B. Learner-state model
PRIOR_KNOWLEDGE: algebraic replacement. LIKELY_HALF_KNOWLEDGE: substitutes cosmetically without reducing complexity. MISSING_BRIDGES: test usefulness by structural compression. OWNERSHIP_TARGET: substitution as a representation decision.
## C. Mathematical invariant / governing structure
A useful substitution turns repeated structure into a lower-complexity expression while preserving enough information to interpret the result.
## D. Representation inventory
| Representation | What it exposes | First move | Condition | Nearby wrong choice |
|---|---|---|---|---|
| repeated `x+1/x` | one recurring block | set `t=x+1/x` | x!=0 retained | rename without compression |
| repeated quadratic block | lower degree in new variable | name block | back-constraints visible | expand every occurrence |
| functional repeated pair | structural target | identify combination goal | do not teach ALG-05 | solve full FE here |
## E. Decision boundaries
| Similar surface | Route A | Route B | Discriminating question | Why wrong route is tempting |
|---|---|---|---|---|
| useful substitution vs renaming | complexity drops | notation only | does degree/repetition decrease? | shorter symbols look useful |
| substitute vs expand | compress repeated block | distribute | which lowers structural cost? | expansion is familiar |
| algebra bridge vs downstream topic | identify block | develop new canon | does solving require downstream theory? | same symbols appear |
## F. Misconception/diagnosis catalogue
ERROR_CODE: ALG01-B-01
WRONG_MOVE: introduce a variable that does not reduce degree or repetition.
WHY_TEMPTING: substitution is remembered as a procedure.
MISSING_LINK_CLASS: REPRESENTATION
REPAIR_INVARIANT: substitution must make the target cheaper.
FALSIFIER_OR_CONTRAST: compare expression complexity before and after.
## G. First-move cues
Repeated identical block: test naming it before expanding.
## H. H3 -> H0 fading plan
H3: provide substitution. H2: highlight repeated block. H1: ask what repeats. H0: changed repeated structure without label.
## I. Validated IOQM source anchors
`IOQM-2024-Q05` and `IOQM-2024-Q11` are substitution/target-reconstruction anchors; custody is W1-F.
## J. Source-independent mathematical trace
Promoted substitutions are checked for legal domain restrictions and actual complexity reduction.
## K. Contrast-pair candidates
substitution vs renaming; substitute vs expand; repeated block vs coincidental similarity; recoverable vs lost restrictions; algebraic block vs functional-equation ownership.
## L. Transfer candidates
reciprocal block; even-power block; functional repeated pair; integer product completion; relation-rewrite handoff.
## M. Candidate mastery items
recognition; first-line substitution; full reduction; WHY-NOT unhelpful substitution; downstream-boundary item.
## N. Dependency declarations
REQUIRES: algebra and domain restrictions already visible in the original expression. BRIDGE_REQUIRES: none. APPLIES: symmetry and hidden relations. Downstream may assume substitution-selection discipline.
## O. Lead integration notes
Keep substitutions target-led; do not import ALG-05 theory.
## P. Independent QA status
DERIVATIONS_CHECKED: PASS
PROMOTED_NUMERICAL_ANSWERS_CHECKED: PASS
SOURCE_IDS_VERIFIED: PASS
DEPENDENCY_CONFLICTS: NONE
OPEN_ISSUES: current PDF must be regenerated after source repair
