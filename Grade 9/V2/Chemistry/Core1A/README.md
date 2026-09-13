# Chemistry V2 — Core (1A): bucket synthesis + learner assimilation

Core (1) remains the semantic authority for **what Chemistry must be taught**. Core (1A) answers a different question:

> Given the exact Core (1) capability authority, C-F learner treatment, C-H representation authority and linked Core (2) demands, what coherent teaching buckets and assimilation sequence are required so the learner can independently transfer?

Core (1A) is not a prettier Core (1), not a summary sheet, and not a reverse-engineered Core (2) answer key.

## Current implementation

The branch now contains three executable Core1A semantic layers:

```text
build_chemistry_core1a_bucket_plan.py
→ build_chemistry_core1a_build_state.py
→ build_chemistry_core1a_manuscript.py
```

The manuscript is a **pre-render semantic learner product**. It realizes the bucket plan into ordered teaching sections, problem-family routines, Core1 practice and readiness metadata, but it does not claim page design or PDF maturity.

The current C-G Appendix A practice templates are procedural/open-response tasks rather than fully instantiated single-answer questions. Core1A therefore binds each one to its exact Appendix B reasoning/verification authority as an `EXPECTED RESPONSE` rubric. It does not invent a fake quick answer. Future objectively checkable Core1A questions must carry both `QUICK CHECK` and `FULL WORKING`.

## Authority

Core (1A) consumes and preserves:

- the exact C-F learner state/treatment;
- complete C-G Core (1) capability/scope authority;
- C-H representation semantics;
- C-I Core (2) source-transfer demands;
- source-integrity and coverage closure from the governed Chemistry chain.

It may change teaching order within governed dependencies, page composition, explanatory depth, number of fresh examples and representation staging. It may not invent Chemistry scope, learner diagnosis, source claims or official provenance.

## Capability != teaching bucket

A capability-centric Core (1) lesson is not automatically a learner textbook bucket. Core (1A) groups capabilities only when they share a grounded teaching invariant, problem family or Chemistry operation/representation.

Shared prerequisites may become bridge buckets so they are taught once rather than duplicated.

Every required Core (1) capability must appear exactly once as a primary/supporting bucket membership under one canonical primary problem-family home.

## Learner state vs intrinsic difficulty

Core (1A) may record intrinsic instructional difficulty such as `D1 | D2 | D3`. This is not learner readiness.

Learner readiness/treatment comes only from C-F. Core (1A) must not invent labels such as `20% learner`, `weak learner`, `foundation learner`, `partial learner` or `advanced learner` unless such labels are upstream authority.

Harder concepts or lower-readiness treatment should result in more staged representations and fewer inferential jumps, not smaller type or denser prose.

## Chemistry representation sequence

The default ordered sequence is:

```text
SEE_THE_PHENOMENON
→ SEE_THE_PARTICLES
→ SEE_THE_CHEMICAL_STRUCTURE
→ SEE_THE_SYMBOLS
→ CONNECT_THE_QUANTITIES
→ DO_THE_CHEMISTRY
→ VERIFY_THE_RESULT
→ CONNECT_TO_CORE2
```

A stage may be `NOT_APPLICABLE` only with an explicit reason. Decorative visuals do not count. The representation should help the learner know what to write, draw, count, compare, cancel, label or track next.

## Learning atoms

A learning atom is the smallest teachable move needed before a linked Core (2) demand can legitimately be attempted.

Each atom is grounded in upstream C-G lesson/PCK/problem-family authority. Core1A cannot patch a missing atom with free-form agent prose.

## Core (2) hint pre-teaching

Internally:

```text
H1 = key Chemistry concept / criterion
H2 = representation / model
H3 = first executable symbolic or quantitative move
```

Every H1/H2/H3 reveal must bind to earlier Core (1A) evidence. If a hint introduces new Chemistry, the question is not ready for release.

## Problem-family assimilation

Do not map a large group of source questions as one undifferentiated transfer list. Split when recognition signals, representation choice or first move differ.

Each active family requires recognition signals, representation/setup, method steps, verification, readiness criteria and exact Core2 release targets.

Readiness requires the learner to RECOGNISE, REPRESENT, choose the FIRST MOVE, and FINISH + VERIFY a fresh analogous item without H2/H3 by default.

## Answer-path requirement

Every learner-facing Core (1A) practice/check item must have a checkable answer path.

Closed items require `QUICK CHECK` and `FULL WORKING`. Genuinely open items require an `EXPECTED RESPONSE` rubric.

## Build state

The semantic build state records stable bucket IDs, completed pre-realization gates and `next_active_bucket`. A zero-primary bucket is retained as `SKIP_NO_PRIMARY_CORE2` rather than silently removed.

Page rendering remains downstream. The canonical cross-product order is defined in `../LearnerProduct/EXECUTION_CONTRACT.md`.
