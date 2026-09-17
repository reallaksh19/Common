---
main_topic_id: IOQM-G9-COMB-03
microstream_id: W1-C
microstream_title: Deterministic state machines
status: PRODUCTION_INTERFACE_PASS
canonical_teaching_owner: IOQM-G9-COMB-03
source_cutoff: 2026-08-31
---

# A. Scope boundary
Owns deterministic transition graphs, reachability and shortest-path representation. Adversarial optimal-play doctrine belongs outside this stream.

# B. Learner-state model
Learner may follow a move sequence but confuse multiple legal moves with a game or preserve irrelevant path history.

# C. Governing invariant / structure
A state is a vertex and every legal operation is a directed edge; reachability/minimum steps are properties of this graph, independent of narrative direction.

# D. Representation inventory
Current-value state, directed transition graph, breadth layers, and predecessor graph.

# E. Decision boundaries
Deterministic branching vs opponent-controlled strategy; current state vs full history; forward vs reverse traversal.

# F. Misconception / diagnosis catalogue
Game confusion, illegal inverse edges, full-history state, unproved shortest path and forward simulation by reflex.

# G. First-move cues
Write the state and legal transitions. For a fixed target, derive valid predecessors before choosing search direction.

# H. Support fading
Fade from supplied graph/inverse rules to independent transition representation and minimality proof.

# I. Validated source anchors
Primary anchors: `IOQM-2024-Q14=80` and `IOQM-2024-Q20=10`.

# J. Source-independent mathematical trace
Promoted machine targets are checked by independent breadth-first search, with explicit witness paths.

# K. Contrast-pair candidates
Forward branching vs reverse predecessors; deterministic reachability vs two-player strategy.

# L. Transfer candidates
Integer machines, button processes, configuration graphs and near-boundary evolution.

# M. Candidate mastery items
Choose state, choose direction, produce a shortest path and justify minimality.

# N. Dependency declarations
No game-strategy canon is imported. Generic recurrence algebra is not required for graph search.

# O. Lead integration notes
Branching alone must never be described as adversarial play in learner materials.

# P. Independent QA status
`STRUCTURE_PASS`; search minima independently audited; human evidence gates `NOT_RUN`.
