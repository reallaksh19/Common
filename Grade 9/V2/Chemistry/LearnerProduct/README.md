# Chemistry V2 LearnerProduct — Core (1A) / Core (2A)

This directory is the deterministic learner-product layer downstream of the governed Chemistry semantic chain.

It adapts two repository patterns without copying their subject semantics:

- Physics Core (1A): bucket assimilation, problem-family routines, hint pre-teaching closure, readiness gates and durable handoff.
- Mathematics Core (1A)/(2A): explicit execution contract, schema/policy/engine/golden separation, dual Core2A lanes, per-question provenance and fail-closed orchestration.

Chemistry consumes its own C-F learner model, C-G Core1 authority, C-H representation bundle, C-I Core2 authority and C-J coverage closure.

## Current implementation status

The current branch implements the machine learner-product chain through **C-LP-25 `FREEZE_HANDOFF`**:

- canonical C-LP-00..25 execution order;
- exact run/provenance/answer-path contracts;
- deterministic Core1A bucket synthesis from real C-F/C-G/C-H/C-I outputs;
- durable Core1A build-state custody;
- Core1A semantic manuscript realization;
- `SOURCE_CORE2` Core2A realization with exact source fidelity;
- `GENERATED_ORIGINAL` challenge selection/generation for validator-backed problem families;
- independent Chemistry recomputation for generated challenges;
- all-source near-copy gating;
- per-question learner-safe provenance with internal source identifiers retained only in custody data;
- staged helper support bound to pre-taught H1/H2/H3 evidence;
- answer-path closure for source, generated and Core1A practice;
- deterministic Core1A/Core2A A4 PDF realization;
- actual-PDF visual preflight;
- machine final audit;
- frozen reusable handoff manifest;
- a Some Basic Concepts process golden under `golden/some-basic-concepts/`.

A machine-complete run is **not** a learner-product release. Subject correctness, pedagogical design, assessment design, actual-size human visual usability and mature-design approval remain independent human gates and remain `PENDING`.

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

Full machine learner-product execution through C-LP-25 uses the same arguments without `--semantic-only`:

```bash
python 'Grade 9/V2/Chemistry/LearnerProduct/engine/run_chemistry_learner_product.py' \
  --run-manifest /path/to/run.json \
  --study-model /path/to/study-model.json \
  --core1-plan /path/to/core1-plan.json \
  --representation-bundle /path/to/representation-bundle.json \
  --core2-plan /path/to/core2-plan.json \
  --coverage-closure /path/to/coverage-closure.json \
  --out-dir /tmp/chemistry-learner-product
```

The full run leaves reusable semantic, render and audit custody including:

```text
core1a_bucket_plan.json
core1a_build_state.json
core1a_manuscript.json
core2a_source_plan.json
core2a_challenge_plan.json
answer_closure_audit.json
semantic_package_manifest.json
chemistry_core1a.pdf
chemistry_core2a.pdf
render_manifest.json
visual_preflight.json
final_audit.json
handoff_manifest.json
learner_product_stage_evidence.json
learner_product_manifest.json
raster-proof/*.png
```

## Rendering contract

`policies/chemistry-learner-render-policy.json` currently requires A4 portrait pages with:

```text
body              10.5 pt
question stem      12.5 pt
small labels        9.25 pt
section heading    13.5 pt
chapter heading    19 pt
minimum visible     9 pt
```

The renderer consumes the closed semantic package and C-H representation authority. It may place a selected primitive but may not select new Chemistry representations or invent chemical content.

Every learner-visible text run passes through the existing Chemistry learner-surface guard. Internal IDs remain in machine custody and must not appear on learner pages.

## Actual-PDF preflight

C-LP-23 validates the physical PDF rather than trusting the page plan. It checks:

```text
PDF hash and page count
A4 page geometry
font floor
physical text/primitive page bounds
clipping
text/primitive overlap
internal-identifier leakage in extracted PDF text
required reasoning-visual closure
first/middle/last raster proof at 144 dpi
blank-page detection
```

Raster proof is machine evidence that pages actually render and are nonblank. It is not a substitute for human actual-size visual review.

## Golden fixture boundary

`golden/some-basic-concepts/expected-semantic-slice.json` freezes a small formula/charge, particle↔symbol and conservation process slice.

`golden/some-basic-concepts/build_render_golden.py` executes the synthetic process fixture through C-LP-25 and produces the exact PDFs, raster proofs, audits and handoff manifest used for render regression. CI uploads these as:

```text
chemistry-core1a-core2a-render-process-golden
```

The rendered golden is retained for human actual-size inspection. It explicitly has no production, official-source or human-release claim. It does not replace the 68-question Some Basic Concepts denominator in the authoring handoff.

## Non-negotiable rules

```text
Core1A consumes learner treatment; it does not invent learner state.
Core1A must pre-teach every Core2 H1/H2/H3 reveal.
Visuals must carry reasoning, not decoration.
Core2A source and generated lanes have different provenance semantics.
Generated challenge difficulty must be conceptual/representational, not arithmetic ugliness.
Every learner-facing question must have a checkable answer path.
Every generated item must pass an independent Chemistry validator and near-copy gate.
Internal source identifiers must not leak into learner provenance or page text.
Every completed run leaves durable semantic, rendered and audit custody.
Machine PASS cannot upgrade pending human subject/pedagogy/assessment/visual gates.
```

## Current boundary

The machine implementation is complete for the synthetic cold-start/golden path through C-LP-25. Remaining programme work is broader Chemistry coverage and authorized review:

- extend independent validators to future problem families as they become supported;
- add governed mixed-synthesis compatibility before generating mixed challenges;
- exercise the production authoring-handoff topics/denominators rather than only the synthetic process fixture;
- run authorized Chemistry subject, pedagogy, assessment and actual-size visual review on exact frozen artifacts.
