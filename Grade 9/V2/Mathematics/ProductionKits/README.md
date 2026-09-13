# Grade 9 Mathematics Production Kits

This directory contains executable production adapters for the four governed product stages:

- `Core1` — capability-level instructional authority (implemented upstream in `Core1Authoring`);
- `Core1A` — bucketed learner-facing teaching realization;
- `Core2` — source-faithful transfer authority (implemented upstream in `Core2Transfer`);
- `Core2A` — purpose-conditioned learner practice / revision / starter / competition realization.

These kits do **not** replace semantic authority and they are not the top-level orchestration contract.

The Mathematics adaptive orchestration authority is:

`Grade 9/V2/Mathematics/MathBlueprint/`

`MathBlueprint` owns immutable ground-truth binding, run identity/state, evidence-adaptive Core1/Core2 routing, independent re-grounding, claim-level cross-validation and, in later increments, Join and assimilation compilation. ProductionKits consume validated upstream products and turn them into executable product blueprints/audits.

## Governing split

```text
GROUND TRUTH decides what evidence actually exists.
MATH BLUEPRINT decides runtime ordering and admissible state transitions.
CORE1 / CORE2 reconstruct different forms of intelligence from ground truth.
ASSIMILATION decides what must change in the learner.
SOURCE AUTHORITY decides WHAT mathematics is legal.
PURPOSE ROUTER decides WHY the learner product is being built.
SCAFFOLD PROFILE decides HOW much support is shown.
BENCHMARK REGISTRY informs challenge DESIGN only.
ANSWER CONTRACT proves the mathematics.
REPRESENTATION CONTRACT proves the teaching representation.
RENDERER may not invent any of the above.
```

## Core2A purpose gate

A Core2A run must declare exactly one purpose:

```text
STARTER
PRACTICE
REVISION
COMPETITION
```

If purpose is absent, interactive agents must ask:

> Is this for Starter, Practice, Revision, or Competition?

Batch/CI execution fails with `CORE2A_USER_PURPOSE_REQUIRED`. There is no default to `PRACTICE`.

## Production rule

Each kit follows the same shape:

```text
validated upstream authority
  -> source-bundle validator
  -> stage builder / selector
  -> answer + representation + scaffold contracts where applicable
  -> stage product / blueprint
  -> audit
```

The shared `common/` package contains executable primitives and machine contracts. The stage kits use those primitives but retain their original authority boundaries.
