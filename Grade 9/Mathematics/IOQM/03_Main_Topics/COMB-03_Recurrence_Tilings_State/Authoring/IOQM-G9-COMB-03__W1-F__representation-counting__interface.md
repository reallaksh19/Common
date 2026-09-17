---
main_topic_id: IOQM-G9-COMB-03
microstream_id: W1-F
microstream_title: Representation counting and local state
status: PRODUCTION_INTERFACE_PASS
canonical_teaching_owner: IOQM-G9-COMB-03
source_cutoff: 2026-08-31
---

# A. Scope boundary
Owns finite local memory such as carry/boundary state and the decision to use a residual/partition/direct representation instead of a recurrence. Arithmetic digit rules are prerequisites, not retaught here.

# B. Learner-state model
Learner may enumerate global representations, omit carry, or force recurrence when a symmetry/gap/residual representation is smaller.

# C. Governing invariant / structure
Store exactly the local information that can change future legal choices; state analysis may terminate in a non-recursive representation when that is cheaper.

# D. Representation inventory
Digit position + carry, bounded-part state, gap selection, residual/deficit state and include/exclude partition state.

# E. Decision boundaries
Carry state vs arithmetic digit-rule derivation; recurrence vs direct gaps/symmetry; local state vs unrestricted partition enumeration.

# F. Misconception / diagnosis catalogue
Carry omitted, full earlier digit history retained, arithmetic ownership drift, forced recurrence and order/identity mismatch.

# G. First-move cues
Ask what information from processed positions can affect later legality; for monotone/near-boundary data, test residual or partition compression first.

# H. Support fading
Fade from supplied carry/state coordinates to learner-designed local state or explicit decision not to recurse.

# I. Validated source anchors
Primary anchors: `IOQM-2023-Q21=15` and `IOQM-2023-Q26=19`.

# J. Source-independent mathematical trace
Bounded-power and distinct-part counts are independently recomputed by DP/enumeration after final wording.

# K. Contrast-pair candidates
Carry state vs global partition listing; state recurrence vs gap bijection; recursive representation vs residual partition.

# L. Transfer candidates
Powers-of-two representations, changed bases, gap-constrained words and distinct-part partitions.

# M. Candidate mastery items
Invent a sufficient carry/state, reject an oversized state, and explain when a direct representation dominates recurrence.

# N. Dependency declarations
Digit/place-value/divisibility facts are supplied by arithmetic owners; generic counting identity/order semantics are retrieved from COMB-01.

# O. Lead integration notes
Do not let representation-counting examples become a new digit-arithmetic or partition-theory chapter.

# P. Independent QA status
`STRUCTURE_PASS`; promoted representation counts independently audited; human evidence gates `NOT_RUN`.
