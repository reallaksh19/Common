---
main_topic_id: IOQM-G9-COMB-03
microstream_id: W1-RESEARCH
microstream_title: State definition, recurrence derivation, reverse search and representation counting
owner_role: RESEARCH_FOUNDATION_PRESERVED_AND_PROMOTED
status: WAVE0_ACCEPTED__INTEGRATED_PACKAGE_AUTHORED
canonical_teaching_owner: IOQM-G9-COMB-03
prerequisite_interfaces:
  - IOQM-G9-COMB-01 stable counting/model interface — ACCEPTED
  - IOQM-G9-ALG-04 stable recurrence interface — ACCEPTED
source_cutoff: 2026-08-31
---

# A. Scope boundary

This file preserves the original research foundation while recording the provider-state transition that unblocked production.

COMB-03 owns minimal sufficient state, first/last-step decomposition, tiling/path counting recurrences, deterministic state graphs, reverse search, finite-memory recurrence and representation/carry-state counting.

COMB-03 does not own AP/GP or generic supplied-recurrence algebra, generic permutation/combination/inclusion-exclusion teaching, arithmetic digit-rule derivation, or adversarial game strategy.

# B. Learner-state model

The learner may list small cases and read recurrence notation, but may guess a recurrence from a short numerical prefix, omit base-state meaning, retain too much or too little history, or simulate forward by reflex.

The production bridge is:

`state = exactly the information needed for future legal choices`.

# C. Governing invariant

A combinatorial recurrence is valid only after the counted objects are partitioned into disjoint, exhaustive transition classes that map to previously defined smaller states.

`STATE -> EXACTLY-ONCE TRANSITIONS -> SMALLER STATES -> BASE MEANING -> RECURRENCE -> VERIFY`.

# D. Representation inventory

The research atlas retains: remaining-size state, tuple/flag finite-memory state, predecessor graph, digit/carry state, and residual/partition representation. A representation is rejected when it merges histories with different futures or stores history that never changes future behavior.

# E. Decision boundaries

- supplied algebraic recurrence vs relation derived from counted structure;
- direct count vs recursive decomposition;
- one-state vs hidden-memory recurrence;
- forward vs reverse search;
- deterministic state evolution vs adversarial game;
- recurrence vs smaller symmetry/gap/residual representation.

# F. Misconception catalogue

The original research error set remains active: undefined state, overlapping cases, missing initialization, algebra before model, forward branch explosion, game confusion, state too large and state too small.

# G. First-move cues

Board: freeze the first unresolved region. String/path: first or last symbol/step. Fixed target: write predecessors. Bounded representation: process one position with local carry/state. Near-boundary structure: compress the residual before building a table.

# H. Support fading

The research support ladders were promoted into learner-visible stages without exporting internal hint codes. Independent mastery remains unlabelled and unhinted.

# I. Validated source anchors

The five frozen anchors remain `IOQM-2024-Q14=80`, `IOQM-2024-Q20=10`, `IOQM-2023-Q08=59`, `IOQM-2023-Q21=15`, `IOQM-2023-Q26=19`.

# J. Source-independent math

The original five-anchor audit is preserved. Final author-created promoted items additionally pass `Authoring/Independent_Final_Item_Audit.md`.

# K. Contrast pairs

Production retains the research contrasts: supplied/derived recurrence, recurrence/direct representation, deterministic/game, forward/reverse, sufficient/insufficient state and recurrence/residual representation.

# L. Transfer

Transfer moves across tilings, strings, paths, deterministic machines, partitions and bounded/carry representations while preserving the state-first invariant.

# M. Mastery

The production package contains recognition, first-line, complete derivation, finite-memory diagnosis, shortest-path representation choice, recurrence-not-always WHY-NOT items and a ten-item unlabelled mastery set.

# N. Dependency declarations

COMB-01 is now an accepted provider for counted-object identity, disjoint/exhaustive addition semantics, restriction/state-memory vocabulary and overlap fail-closed rules. ALG-04 is accepted for indexed notation, initialization form, explicit-vs-recursive distinction and algebraic verification only after structural derivation.

# O. Lead integration notes

The earlier `WAIT_FOR_PROVIDER` state is superseded. C01-1..C01-10 and T1..T6 passed against the merged provider; overlap boundaries were revalidated; Wave-0 was legitimately frozen before student authoring. Separate production interfaces now exist for all seven issue-defined microstreams.

# P. Independent QA status

`RESEARCH_FOUNDATION_PRESERVED`: PASS.
`PROVIDER_ACCEPTANCE`: PASS.
`WAVE0_PROMOTION`: PASS.
`INTEGRATED_STATIC_PACKAGE`: PASS.
Classroom timing/readability, longitudinal retention, psychometrics and publication approval: `NOT_RUN`.
