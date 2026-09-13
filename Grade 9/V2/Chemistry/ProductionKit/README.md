# Chemistry V2 Production Kit

This directory is an executable production layer for Core (1), Core (2), Core (1A), and Core (2A). It is deliberately not a prose-only schema package.

It provides:

- an executable task router;
- source and answer contracts;
- purpose-sensitive scaffold profiles;
- a learning-representation builder/validator that consumes the existing Chemistry representation registries;
- product-packet realization with page-budget and provenance checks;
- fail-closed source/answer closure validation;
- multiple golden fixtures spanning Core (1), Core (2), Core (1A), and all four Core (2A) purposes;
- executable falsifier tests wired into CI.

## Production entrypoint

```bash
python 'Grade 9/V2/Chemistry/ProductionKit/engine/run_production_kit.py' \
  --task task.json \
  --questions questions.json \
  --answers answers.json \
  --out-dir /tmp/chemistry-production-kit
```

The entrypoint emits:

```text
route_plan.json
source_answer_audit.json
representation_plan.json
product_packet.json
production_manifest.json
```

## Core (2A) purpose is mandatory

Core (2A) cannot be authored without one of:

```text
STARTER
PRACTICE
REVISION
COMPETITION
```

Unresolved purpose fails with `CORE2A_PURPOSE_UNRESOLVED`.

The chosen purpose materially changes selection, support density, clue density, workspace, transfer mix, and page density. It is not a cover-label switch.

## Sheet-1 source rule

Every Core (2A) question must display its source/provenance basis on Sheet 1.

For a governed source question, Sheet 1 shows the exact human-readable source locator.

For a fresh/generated question, Sheet 1 shows the construction references used to shape the question and the governed content anchor. The learner-facing line must distinguish `construction reference` from `official question source`; a generated question may not be presented as an official past question.

Failure code: `CORE2A_SHEET1_SOURCE_MISSING`.

## Page budget

Default Core (2A) budget:

```text
one learner question <= two physical pages
```

Sheet 1 contains the attempt, demand-sized workspace, source line, and mode-appropriate technical clues. Sheet 2 contains the quick check, full working, and an independent current-question verification.

## Existing authority reused

This kit does not replace the mature Chemistry semantic layers. It routes into and validates against the existing authorities:

- `CoreAuthoring` for Core (1);
- `Core2Transfer` for Core (2);
- `Core1A` for assimilation buckets and pre-teaching;
- `Core2A` for purpose-specific transfer;
- `ReasoningSemantics` for canonical problem families;
- `Representation` for primitive selection and semantic validation;
- `LearnerProduct` for final render/preflight/freeze machinery.

The kit's job is to make those pieces operable from a single production request while enforcing product-specific invariants before rendering.

## Golden fixtures

`golden/fixtures.json` contains positive goldens for:

- Core (1): formula/charge teaching and conservation teaching;
- Core (2): source-faithful MCQ and constructed response;
- Core (1A): formula/charge assimilation and conservation assimilation;
- Core (2A): Starter, Practice, Revision, and Competition.

The tests also include negative falsifiers for unresolved Core (2A) purpose, missing Sheet-1 source, missing answer closure, and unknown representation capability.
