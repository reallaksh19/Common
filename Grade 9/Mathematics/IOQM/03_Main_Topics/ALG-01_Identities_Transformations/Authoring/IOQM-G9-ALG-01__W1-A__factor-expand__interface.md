---
main_topic_id: IOQM-G9-ALG-01
microstream_id: W1-A
microstream_title: Factor versus expand
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-ALG-01
prerequisite_interfaces: []
source_cutoff: 2026-08-31
---

## A. Scope boundary
Included: target-led choice between factorisation and expansion, difference-of-squares structure, zero-product use and coefficient extraction. Excluded: polynomial remainder/Vieta canon (ALG-03).
## B. Learner-state model
PRIOR_KNOWLEDGE: routine expand/factor skills. LIKELY_HALF_KNOWLEDGE: manipulates before reading the target. MISSING_BRIDGES: representation choice by target. OWNERSHIP_TARGET: ask which form makes the requested target cheapest.
## C. Mathematical invariant / governing structure
Equivalent algebraic forms are tools; the target determines which representation exposes the needed invariant with least work.
## D. Representation inventory
| Representation | What it exposes | First move | Condition | Nearby wrong choice |
|---|---|---|---|---|
| difference of squares | product/zeros/numeric shortcut | factor | exact pattern | expand both squares |
| product of linear factors | zeros | keep factored | equation equals zero | expand first |
| product target coefficient | coefficient information | selective expansion | coefficient requested | factor more |
## E. Decision boundaries
| Similar surface | Route A | Route B | Discriminating question | Why wrong route is tempting |
|---|---|---|---|---|
| expand vs factor | coefficients | zeros/product | what is requested? | both are familiar |
| full vs selective expansion | expand all | expose only target coefficient | how much information is needed? | procedural habit |
| factor identity vs solving individual values | preserve structure | solve | can target be read directly? | solving feels complete |
## F. Misconception/diagnosis catalogue
ERROR_CODE: ALG01-A-01
WRONG_MOVE: expand before inspecting the target.
WHY_TEMPTING: expansion is algorithmic.
MISSING_LINK_CLASS: RECOGNITION
REPAIR_INVARIANT: target chooses representation.
FALSIFIER_OR_CONTRAST: `1004^2-996^2` is cheaper as a product.
## G. First-move cues
Square difference or zero product: test factorisation before expansion. Coefficient target: expand only enough to expose it.
## H. H3 -> H0 fading plan
H3: state representation. H2: cue target type. H1: ask “zeros, value or coefficient?” H0: changed-surface selection.
## I. Validated IOQM source anchors
`IOQM-2025-Q01` and `IOQM-2025-Q21` support target/representation selection; exact custody is W1-F.
## J. Source-independent mathematical trace
All factor/expand identities are independently algebra-checked; historical numerical results remain in source audit.
## K. Contrast-pair candidates
expand vs factor; selective vs full expansion; zeros vs coefficients; target transform vs solve variable; identity vs solution-only relation.
## L. Transfer candidates
numeric shortcut; coefficient extraction; integer factor bridge; inequality representation choice; high-power reduction entry.
## M. Candidate mastery items
recognition; first-line form choice; full solve; WHY-NOT oversized expansion; constructed counterexample.
## N. Dependency declarations
REQUIRES: F0 algebra. BRIDGE_REQUIRES: none. APPLIES: substitutions/symmetry/relation rewrite. Downstream may assume target-led representation choice.
## O. Lead integration notes
Teach governing question once and reuse. Avoid downstream polynomial canon.
## P. Independent QA status
DERIVATIONS_CHECKED: PASS
PROMOTED_NUMERICAL_ANSWERS_CHECKED: PASS
SOURCE_IDS_VERIFIED: PASS
DEPENDENCY_CONFLICTS: NONE
OPEN_ISSUES: current PDF must be regenerated after source repair
