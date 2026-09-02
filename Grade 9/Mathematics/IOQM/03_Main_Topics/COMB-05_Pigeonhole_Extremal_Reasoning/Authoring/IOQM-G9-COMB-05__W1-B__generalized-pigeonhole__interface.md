---
main_topic_id: IOQM-G9-COMB-05
microstream_id: W1-B
microstream_title: Generalized pigeonhole
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-COMB-05
prerequisite_interfaces: []
source_cutoff: 2026-09-02
---
## A. Scope boundary
Included: capacity thresholds and ceilings. Excluded: exact occupancy distributions.
## B. Learner-state model
PRIOR_KNOWLEDGE: direct collision. LIKELY_HALF_KNOWLEDGE: uses averages vaguely. MISSING_BRIDGES: negate threshold and total capacity. OWNERSHIP_TARGET: generalized capacity proof.
## C. Mathematical invariant / governing structure
To force at least k in one of m boxes, failure caps total at (k-1)m.
## D. Representation inventory
Capacity table exposes thresholds; ceiling form exposes `ceil(N/m)`; load boxes expose integer discreteness.
## E. Decision boundaries
Average vs capacity; at least k vs exactly k; uniform vs nonuniform caps; existence vs distribution.
## F. Misconception/diagnosis catalogue
ERROR_CODE: C05-B-01; WRONG_MOVE: average alone as proof; WHY_TEMPTING: threshold visible numerically; MISSING_LINK_CLASS: DISCRETE_FILTER; REPAIR_INVARIANT: write the integer failure cap; FALSIFIER_OR_CONTRAST: average 3.2 does not force exactly 4.
## G. First-move cues
Negate desired load and sum maximum failure capacity.
## H. H3 -> H0 fading plan
H3 cap relation; H2 capacity prompt; H1 threshold clue; H0 new load surface.
## I. Validated IOQM source anchors
IOQM-2023-Q27 as extremal-capacity transfer.
## J. Source-independent mathematical trace
4320 is the maximum bad-class capacity; excess 91 is forced good.
## K. Contrast-pair candidates
average/capacity; exact/at-least; uniform/nonuniform; pigeonhole/IE; direct/generalized.
## L. Transfer candidates
birth months, containers, degree/load surfaces, bad-class capacity.
## M. Candidate mastery items
threshold recognition, first-line cap, full generalized proof, average falsifier.
## N. Dependency declarations
REQUIRES integer arithmetic; EXPORTS P05-2/P05-7.
## O. Lead integration notes
Derive once after direct pigeonhole and reuse as capacity language.
## P. Independent QA status
DERIVATIONS_CHECKED: PASS
PROMOTED_NUMERICAL_ANSWERS_CHECKED: PASS
SOURCE_IDS_VERIFIED: PASS
DEPENDENCY_CONFLICTS: NONE
OPEN_ISSUES: classroom/psychometrics NOT_RUN