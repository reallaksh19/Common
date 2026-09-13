# Chemistry V2 LearnerProduct — Core (1A) / Core (2A)

This directory is the deterministic learner-product layer downstream of the governed Chemistry semantic chain.

It adapts two proven repository patterns:

- Physics Core (1A): bucket assimilation, problem-family routines, hint pre-teaching closure, readiness gates and durable handoff.
- Mathematics Core (1A)/(2A): explicit execution contract, schema/policy/engine/golden separation, dual Core2A lanes, per-question provenance and fail-closed orchestration.

Chemistry does not copy either subject's semantics. It consumes Chemistry's C-F learner model, C-G Core1 authority, C-H representation bundle, C-I Core2 authority and C-J coverage closure.

## Current implementation status

The current branch implements the governed semantic chain through **C-LP-21 `VALIDATE_ANSWER_CLOSURE`**:

- canonical C-LP-00..25 execution order;
- exact run/provenance/answer-path contracts;
- deterministic Core1A bucket synthesis from real C-F/C-G/C-H/C-I outputs;
- durable Core1A build-state custody;
- Core1A semantic manuscript realization;
- `SOURCE_CORE2` Core2A realization with exact source fidelity;
- `GENERATED_ORIGINAL` challenge selection/generation for validator-backed problem families;
- independent Chemistry recomputation for generated challenges;
- all-source near-copy gating;
- per-question provenance;
- staged helper support bound to pre-taught H1/H2/H3 evidence;
- answer-path closure for source, generated and Core1A practice;
- semantic package/stage-evidence emission;
- a frozen Some Basic Concepts process golden under `golden/some-basic-concepts/`.

Rendering and publication gates remain intentionally pending. The runner does not convert a semantic pass into a visual/release claim.

## Answer-path rule

```text
OBJECTIVE QUESTION
= QUICK CHECK
= FULL WORKING

GENUINELY OPEN RESPONSE
= EXPECTED RESPONSE RUBRIC
```

Core1A C-G practice templates are currently procedural/open-response tasks, so the semantic manuscript binds each one to its governed Appendix B reasoning/verification criteria as an `EXPECTED RESPONSE` rubric rather than inventing a fake single final answer.

## Canonical runner modes

Contract-only validation:

```bash
python 'Grade 9/V2/Chemistry/LearnerProduct/engine/run_chemistry_learner_product.py' \
  --run-manifest /path/to/run.json \
  --out-dir /tmp/chemistry-learner-product \
  --validate-only
```

Semantic execution through C-LP-21:

```bash
python 'Grade 9/V2/Chemistry/LearnerProduct/engine/run_chemistry_learner_product.py' \
  --run-manifest /path/to/run.json \
  --study-model /path/to/study-model.json \
  --core1-plan /path/to/core1-plan.json \
  --representation-bundle /path/to/representation-bundle.json \
  --core2-plan /path/to/core2-plan.json \
  --coverage-closure /path/to/coverage-closure.json \
  --out-dir /tmp/chemistry-learner-product \
  --semantic-only
```

The semantic run writes:

```text
core1a_bucket_plan.json
core1a_build_state.json
core1a_manuscript.json
core2a_source_plan.json
core2a_challenge_plan.json
answer_closure_audit.json
learner_product_stage_evidence.json
semantic_package_manifest.json
```

A normal run without `--semantic-only` executes the semantic chain and then fails closed with `CHEM_LP_RENDER_STAGE_NOT_IMPLEMENTED` at C-LP-22. This is deliberate: C-LP-22..25 are not silently skipped.

## Golden fixture boundary

`golden/some-basic-concepts/expected-semantic-slice.json` freezes a small pre-render process slice covering:

- formula anatomy / charge;
- particle ↔ symbolic translation;
- atom conservation.

It uses the repository's synthetic cold-start fixture and explicitly has `production_claim=false`. It is a process golden, not an NCERT provenance claim and not a substitute for the 68-question Some Basic Concepts handoff denominator.

## Non-negotiable rules

```text
Core1A consumes learner treatment; it does not invent learner state.
Core1A must pre-teach every Core2 H1/H2/H3 reveal.
Visuals must carry reasoning, not decoration.
Core2A source and generated lanes have different provenance semantics.
Generated challenge difficulty must be conceptual/representational, not arithmetic ugliness.
Every learner-facing question must have a checkable answer path.
Every generated item must pass an independent Chemistry validator and near-copy gate.
Every completed semantic run leaves durable machine-readable outputs.
No semantic pass upgrades pending human subject/pedagogy/assessment/visual gates.
```

## Next implementation boundary

The next slice is page realization: convert the closed semantic manuscript/source/challenge plans into Core (1A) and Core (2A) learner pages, then run actual-size typography, primitive, clipping/overlap, internal-ID-leak and visual-usability preflight before any PDF/release claim.
