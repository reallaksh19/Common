---
main_topic_id: IOQM-G9-COMB-03
microstream_id: W1-A
microstream_title: Tilings and first unresolved region
status: PRODUCTION_INTERFACE_PASS
canonical_teaching_owner: IOQM-G9-COMB-03
source_cutoff: 2026-08-31
---

# A. Scope boundary
Owns board/strip state definition, exactly-once first-placement decomposition and combinatorial base-state meaning. Generic counting doctrine and supplied-recurrence algebra remain prerequisite retrieval.

# B. Learner-state model
Learner can list small tilings but may guess a recurrence from values or omit what the state counts.

# C. Governing invariant / structure
`STATE -> FIRST UNRESOLVED REGION -> DISJOINT/EXHAUSTIVE PLACEMENTS -> SMALLER STATES -> BASE MEANING -> VERIFY`.

# D. Representation inventory
Board picture, remaining width, and a minimal flag when a special tile/resource changes future legality.

# E. Decision boundaries
One-state vs flagged state; recursive decomposition vs direct count; tiling recurrence vs supplied algebraic recurrence.

# F. Misconception / diagnosis catalogue
Undefined state; overlapping placements; omitted placement; special-tile history forgotten; empty board treated as a magic value.

# G. First-move cues
Freeze the leftmost unresolved cell/column and stop each branch when the remainder is a named smaller state.

# H. Support fading
Fade from supplied state/branch picture to independent state definition and derivation. First mastery remains unlabelled and unhinted.

# I. Validated source anchors
Primary anchor: `IOQM-2023-Q08`, verified answer `59`.

# J. Source-independent mathematical trace
Promoted tiling recurrences are recomputed from direct small-board states after final wording.

# K. Contrast-pair candidates
Domino-only one-state recurrence vs at-most-one-special-tile flagged state; recurrence vs direct position count.

# L. Transfer candidates
Boards -> strips -> staircase paths -> strings with local block restrictions.

# M. Candidate mastery items
State definition, full recurrence derivation, base-state explanation and changed-tile-set transfer.

# N. Dependency declarations
Retrieve counted-object/disjoint-exhaustive semantics from COMB-01 and recurrence notation/initialization from ALG-04 only.

# O. Lead integration notes
Do not export owner codes, dependency labels, wave states or hint codes into learner prose.

# P. Independent QA status
`STRUCTURE_PASS`; final promoted numerical items independently audited; classroom/retention/psychometric/publication gates `NOT_RUN`.
