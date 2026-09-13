# Chemistry V2 LearnerProduct — Core (1A) / Core (2A)

This directory is the deterministic learner-product layer that sits downstream of the governed Chemistry semantic chain.

It adapts two proven patterns from the repository:

- Physics Core (1A): bucket assimilation, problem-family routines, hint pre-teaching closure, readiness gates and durable agent handoff.
- Mathematics Core (1A)/(2A): explicit execution contract, schema/policy/engine/golden separation, dual Core2A lanes, per-question provenance and fail-closed orchestration.

Chemistry does not copy either subject's semantics. It uses Chemistry's own C-F learner model, C-G Core1 authority, C-H representation bundle, C-I Core2 authority and C-J coverage closure.

## Current implementation status

This foundation slice implements:

- canonical execution order (`EXECUTION_CONTRACT.md`);
- exact learner-product run schema;
- per-question provenance schema;
- mandatory answer-path schema;
- Core1A and Core2A execution policies;
- learner-language, citation, challenge and answer-path policies;
- Chemistry competitive archetype registry;
- fail-closed `run_chemistry_learner_product.py` validation entrypoint;
- contract tests and CI.

It intentionally does **not** claim bucket synthesis, Core2A generation or rendered product realization is implemented yet. A non-`--validate-only` run fails closed until the downstream stage adapters exist.

## Non-negotiable rules

```text
Core1A consumes learner treatment; it does not invent learner state.
Core1A must pre-teach every Core2 H1/H2/H3 reveal.
Visuals must carry reasoning, not decoration.
Core2A source and generated lanes have different provenance semantics.
Generated challenge difficulty must be conceptual/representational, not arithmetic ugliness.
Every learner-facing question must have a checkable answer path.
Every completed run must leave a durable reusable handoff.
```

## Canonical entrypoint

```bash
python 'Grade 9/V2/Chemistry/LearnerProduct/engine/run_chemistry_learner_product.py' \
  --run-manifest /path/to/run.json \
  --out-dir /tmp/chemistry-learner-product \
  --validate-only
```

The next implementation slice should add the Core1A bucket-plan schema/engine, representation obligations, learning atoms, problem-family planning and Core2 hint-preteach closure before any learner PDF generation is attempted.
