# Chemistry V2 — Core (1A): bucket synthesis + learner assimilation

Core (1) remains the semantic authority for **what Chemistry must be taught**. Core (1A) answers a different question:

> Given the exact Core (1) capability authority, C-F learner treatment, C-H representation authority and linked Core (2) demands, what coherent teaching buckets and assimilation sequence are required so the learner can independently transfer?

Core (1A) is not a prettier Core (1), not a summary sheet, and not a reverse-engineered Core (2) answer key.

## Current implementation

Core1A now has four executable layers:

```text
build_chemistry_core1a_bucket_plan.py
→ build_chemistry_core1a_build_state.py
→ build_chemistry_core1a_manuscript.py
→ LearnerProduct PDF realization / preflight / handoff
```

The manuscript is the semantic learner-product authority. The downstream learner renderer consumes that manuscript plus the already-selected C-H representation bundle; it does not choose a replacement representation or invent Chemistry.

The current C-G Appendix A practice templates are procedural/open-response tasks rather than fully instantiated single-answer questions. Core1A therefore binds each one to its exact Appendix B reasoning/verification authority as an `EXPECTED RESPONSE` rubric instead of fabricating a fake final answer. Future objectively checkable Core1A questions require both `QUICK CHECK` and `FULL WORKING`.

## Authority

Core (1A) consumes and preserves:

- exact C-F learner state/treatment;
- complete C-G Core (1) capability/scope authority;
- C-H representation semantics;
- C-I Core (2) source-transfer demands;
- source-integrity and coverage closure from the governed Chemistry chain.

It may change teaching order within governed dependencies, explanatory depth, practice staging and page composition. It may not invent Chemistry scope, learner diagnosis, source claims or official provenance.

## Capability != teaching bucket

A capability-centric Core (1) lesson is not automatically a learner textbook bucket. Core (1A) groups capabilities only when they share a grounded teaching invariant, problem family or Chemistry operation/representation.

Shared prerequisites may become bridge buckets so they are taught once rather than duplicated. Every required Core (1) capability has one governed bucket home.

## Learner state vs intrinsic difficulty

Core (1A) may record intrinsic instructional difficulty such as `D1 | D2 | D3`. This is not learner readiness.

Learner readiness/treatment comes only from C-F. Core (1A) must not invent labels such as `20% learner`, `weak learner`, `foundation learner`, `partial learner` or `advanced learner` unless those labels are upstream authority.

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

## Learning atoms and hint pre-teaching

A learning atom is the smallest teachable move needed before a linked Core (2) demand can legitimately be attempted. Each atom is grounded in upstream C-G lesson/PCK/problem-family authority; Core1A cannot patch a missing atom with free-form agent prose.

Internally:

```text
H1 = key Chemistry concept / criterion
H2 = representation / model
H3 = first executable symbolic or quantitative move
```

Every H1/H2/H3 reveal must bind to earlier Core (1A) evidence. If a hint introduces new Chemistry, the linked Core2 question is not ready.

## Problem-family assimilation and readiness

Do not map a large group of source questions as one undifferentiated transfer list. Split when recognition signals, representation choice or first move differ.

Each active family carries recognition signals, representation/setup, method steps, verification, readiness criteria and exact Core2 release targets.

Default readiness requires the learner to RECOGNISE, REPRESENT, choose the FIRST MOVE, and FINISH + VERIFY a fresh analogous item without H2/H3.

## Learner PDF realization

The full LearnerProduct runner now realizes Core1A as deterministic A4 PDF pages from the closed manuscript. The render policy currently uses 10.5 pt body text, 12.5 pt question text and a 9 pt machine floor.

Every governed C-H representation attached to a teaching section is attempted through the existing Chemistry vector primitive renderer. A secondary primitive whose required semantic data is genuinely unavailable is recorded; a visually obligated section cannot silently collapse to zero realized reasoning visuals.

Every learner-visible string passes the Chemistry learner-surface identifier firewall before drawing.

## Answer-path requirement

Every learner-facing Core (1A) practice/check item has a checkable answer path:

```text
closed item → QUICK CHECK + FULL WORKING
open/procedural item → EXPECTED RESPONSE rubric
```

For current open-response Core1A practice, the expected response is placed after the attempt page rather than exposing it beside the task.

## Build state and review boundary

The semantic build state records stable bucket IDs, completed pre-realization gates and `next_active_bucket`. A zero-primary bucket is retained as `SKIP_NO_PRIMARY_CORE2` rather than silently removed.

C-LP-23 independently checks the physical PDF for geometry, clipping/overlap, font floor, extracted-text identifier leaks, reasoning-visual closure and raster rendering. C-LP-24/25 then freeze machine audit and handoff custody.

**Machine PASS is not expert approval.** Subject correctness, pedagogy, assessment design, actual-size visual usability and mature-design quality remain human gates. The canonical cross-product order is defined in `../LearnerProduct/EXECUTION_CONTRACT.md`.
