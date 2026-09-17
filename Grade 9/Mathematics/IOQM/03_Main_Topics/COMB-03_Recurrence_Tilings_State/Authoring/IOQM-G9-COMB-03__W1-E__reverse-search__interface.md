---
main_topic_id: IOQM-G9-COMB-03
microstream_id: W1-E
microstream_title: Reverse-state search
status: PRODUCTION_INTERFACE_PASS
canonical_teaching_owner: IOQM-G9-COMB-03
source_cutoff: 2026-08-31
---

# A. Scope boundary
Owns valid predecessor construction and the forward/reverse representation decision for deterministic reachability or shortest paths.

# B. Learner-state model
Learner tends to follow the story forward even when the target has far fewer predecessors than the start has successors.

# C. Governing invariant / structure
Forward and reverse traversal describe the same directed state graph; reversing requires exact legal predecessor rules, not informal undoing.

# D. Representation inventory
Successor list, predecessor list, reverse breadth layers and residue/parity filters when they arise from the transition rule.

# E. Decision boundaries
Forward vs reverse branching; reachable path vs shortest path; deterministic search vs game strategy.

# F. Misconception / diagnosis catalogue
Illegal predecessor, omitted predecessor, reverse route without forward validation, shortest path asserted from one witness, and game confusion.

# G. First-move cues
For target `y`, invert each operation and state its domain condition; compare predecessor and successor branching before search.

# H. Support fading
Fade from supplied inverse moves to learner-derived predecessors, direction choice and independent minimality proof.

# I. Validated source anchors
Primary anchor: `IOQM-2024-Q20`, verified minimum `10`.

# J. Source-independent mathematical trace
All promoted machine minima are recomputed by breadth-first search independent of the written Teacher Key.

# K. Contrast-pair candidates
Narrative-forward machine with wide branching versus the same graph searched backward from one target.

# L. Transfer candidates
Integer operations, button machines, configuration graphs and deterministic transformation systems.

# M. Candidate mastery items
Derive predecessors, choose direction, exhibit a path and certify no shorter path exists.

# N. Dependency declarations
No adversarial strategy or recurrence algebra is imported into reverse search.

# O. Lead integration notes
A reverse edge is included only when applying the original forward operation reproduces the current state legally.

# P. Independent QA status
`STRUCTURE_PASS`; BFS minima independently audited; human evidence gates `NOT_RUN`.
