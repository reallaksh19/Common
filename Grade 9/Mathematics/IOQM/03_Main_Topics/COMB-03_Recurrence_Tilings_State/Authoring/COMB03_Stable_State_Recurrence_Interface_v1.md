# COMB-03 Stable State / Recurrence Interface v1

Status: `FROZEN_V1_FOR_DOWNSTREAM_RETRIEVAL`
Provider: `IOQM-G9-COMB-03`

This interface exports state-design and combinatorial-recurrence semantics. Downstream topics retrieve these statements without rebuilding the chapter.

## S03-1 - State definition
Before a recurrence or transition equation is written, define exactly what one state counts or records.

## S03-2 - Minimal sufficiency test
A state is sufficient only if two histories assigned to the same state always have the same legal future behavior relevant to the problem. Remove remembered data that never changes future behavior.

Canonical diagnostic question: `Can two histories with this same proposed state have different legal futures?`

## S03-3 - Exactly-once transition decomposition
A counting recurrence may add branch counts only after proving every admissible object enters exactly one branch.

## S03-4 - Smaller-state correspondence
Each recurrence term must come from a branch that maps bijectively, or with an explicitly counted transition multiplicity, to the claimed smaller state.

## S03-5 - Base-state meaning
Initial values must correspond to directly checkable configurations/states. Empty-state counts may equal 1 only when the empty configuration is a legitimate identity object for the decomposition.

## S03-6 - One-state versus finite-memory decision
If current size alone does not determine future legality, add the smallest flag/tuple that does. Scalar recurrence notation is not mandatory when a transition table is clearer.

## S03-7 - Forward/reverse state choice
For deterministic reachability or shortest-path work, forward and reverse traversals describe the same directed state graph. Prefer the direction with simpler legal transitions or smaller branching, provided the predecessor rule is correct.

## S03-8 - Deterministic/game boundary
Multiple legal moves do not create an adversarial game. Game doctrine begins when another player controls choices with an opposing strategic objective.

## S03-9 - Carry/local-state representation
When a representation can be processed locally, carry or boundary memory may replace global enumeration. Arithmetic rules generating the local constraint must come from their arithmetic owner; COMB-03 owns the state-transition count.

## S03-10 - Recurrence-not-always rule
State analysis may end in a direct symmetry, gap, residual, partition, or other compressed representation. Do not force recurrence when a smaller representation proves the count more directly.

## Downstream compatibility tests

- Retrieval test: consumer can invoke `state before recurrence` without reteaching tilings.
- Sufficiency test: consumer can use the two-histories falsifier.
- Exactly-once test: consumer explicitly checks disjointness and exhaustiveness.
- Game-boundary test: deterministic branching is not mislabeled adversarial.
- Direction test: reverse search is used only after valid predecessors are defined.
- Ownership test: consumer does not import generic sequence algebra or generic counting doctrine through this interface.
