# Grade 9 Mathematics Production Kits

This directory contains executable production kits for the four governed product stages:

- `Core1` — capability-level instructional authority (implemented upstream in `Core1Authoring`);
- `Core1A` — bucketed learner-facing teaching realization;
- `Core2` — source-faithful transfer authority (implemented upstream in `Core2Transfer`);
- `Core2A` — purpose-conditioned learner practice / revision / starter / competition realization.

These kits do **not** replace the upstream semantic engines. They make production use explicit, reproducible and fail-closed.

## Governing split

```text
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
source bundle
  -> validator
  -> stage builder / selector
  -> answer + representation + scaffold contracts where applicable
  -> stage product / blueprint
  -> audit
```

The shared `common/` package contains executable primitives and machine contracts. The stage kits use those primitives but retain their original authority boundaries.
