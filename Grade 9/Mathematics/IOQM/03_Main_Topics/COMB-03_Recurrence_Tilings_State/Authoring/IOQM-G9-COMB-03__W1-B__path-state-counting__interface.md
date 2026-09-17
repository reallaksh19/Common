---
main_topic_id: IOQM-G9-COMB-03
microstream_id: W1-B
microstream_title: Path and state counting
status: PRODUCTION_INTERFACE_PASS
canonical_teaching_owner: IOQM-G9-COMB-03
source_cutoff: 2026-08-31
---

# A. Scope boundary
Owns state-based counting of paths/strings by first or last transition. Does not reteach generic addition/multiplication counting or generic sequence algebra.

# B. Learner-state model
Learner can enumerate short paths but may count histories and states interchangeably or infer a formula from a short prefix.

# C. Governing invariant / structure
Every counted path enters exactly one first/last-transition class, and each class maps to a defined predecessor/smaller state.

# D. Representation inventory
Length state, predecessor state, last-symbol state, or small tuple when local history changes legal continuations.

# E. Decision boundaries
Path count vs state count; one-state vs finite-memory; direct gap/symmetry count vs recurrence.

# F. Misconception / diagnosis catalogue
Double-counted histories, omitted predecessor, path/state identity confusion, insufficient last-step memory and recurrence-by-pattern.

# G. First-move cues
Classify by first or last legal step/symbol and name the smaller state reached after removing it.

# H. Support fading
Fade from supplied predecessor classes to independent state and transition design; mastery has no method cue.

# I. Validated source anchors
Bridge evidence includes the COMB-03 state-count anchors; source ownership is not inflated by secondary tags.

# J. Source-independent mathematical trace
Binary-string, staircase and composition counts are checked by independent enumeration/DP after final wording.

# K. Contrast-pair candidates
No-consecutive-1 one-state decomposition vs no-consecutive-1 plus parity finite-memory state.

# L. Transfer candidates
Staircases, strings, compositions and directed path counts.

# M. Candidate mastery items
Exactly-once predecessor proof, state sufficiency diagnosis and changed-surface path recurrence.

# N. Dependency declarations
Retrieve object identity/disjointness from COMB-01 and recurrence notation/initialization from ALG-04.

# O. Lead integration notes
Keep path-versus-state identity explicit and learner language free of production codes.

# P. Independent QA status
`STRUCTURE_PASS`; promoted numerical answers independently audited; human evidence gates `NOT_RUN`.
