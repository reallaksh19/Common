# Mathematics V2 — Core (2A): purpose-conditioned learner practice

Core (2) remains the governed semantic transfer plan over the **complete original source-question set**. Core (2A) is a derived learner-product stage. It does not simply re-render Core (2): it must first know **why the learner is using the product**.

## Mandatory purpose gate

Before preparing Core (2A), establish exactly one purpose:

```text
STARTER
PRACTICE
REVISION
COMPETITION
```

If purpose is missing, an interactive agent must ask exactly:

> Is this for Starter, Practice, Revision, or Competition?

Batch/CI execution fails with `CORE2A_USER_PURPOSE_REQUIRED`. There is no default to `PRACTICE`.

The executable authority is:

`Grade 9/V2/Mathematics/ProductionKits/Core2A/engine/run_core2a_kit.py`

with shared routing/scaffold/source/answer/provenance machinery under:

`Grade 9/V2/Mathematics/ProductionKits/common/`.

## Source versus benchmark

```text
SOURCE AUTHORITY decides WHAT mathematics is legal.
PURPOSE decides WHY the product is being built.
SCAFFOLD PROFILE decides HOW support is presented.
BENCHMARKS may shape challenge DESIGN but may not expand curriculum scope.
```

Core (2A) consumes governed Core (1)/Core (1A)/Core (2) authority. Competition-mode external references are benchmark-only. The production benchmark registry is:

`ProductionKits/common/registry/benchmark-source-registry.json`

and currently permits official JEE Advanced, HBCSE Mathematics Olympiad and IMO archives only for `STYLE_BENCHMARK` or `ARCHETYPE_DERIVATION`. They are never curriculum authority.

## Purpose-specific product behavior

The product must differ materially by purpose.

### STARTER

- one useful Core (2) anchor per bucket where available;
- at least one fresh `GUIDED_DIRECT` item per bucket;
- full concept recap and high representation density;
- generous staged help;
- no competition benchmark.

### PRACTICE

- preserve all applicable Core (2) source items in the selected scope;
- at least one fresh practice item per bucket;
- repeated problem-family practice plus controlled variation;
- help available but initially hidden;
- no competition benchmark.

### REVISION

- select representative/high-demand Core (2) items rather than reproducing the whole set;
- add invariant recall and method-discrimination prompts;
- compact recap, low repetition and sparse help;
- no competition benchmark required.

### COMPETITION

- use representative Core (2) anchors as baselines;
- require `NEAR_TRANSFER` plus one structural challenge per eligible bucket;
- structural challenges may use hidden information, reversed targets, representation shifts or parameter constraints;
- mixed synthesis is allowed only across taught/approved buckets;
- official competition archives may be cited only as benchmark/archetype sources;
- generated questions must remain fresh and may not require untaught mathematics.

Therefore Core (2A) is not required to reproduce every Core (2) question in every mode. **Core (2) remains the complete immutable source authority.** Whenever a Core (2) question is selected into Core (2A), its ID, stem, givens, options, units, subparts and assessment-safety semantics remain immutable.

## Two item classes

```text
SOURCE_CORE2
  selected original Core (2) item; source shape is immutable

GENERATED_CHALLENGE
  fresh item grounded in taught Core (1A) buckets and approved Core (2) demand
```

Fresh generated items may increase reasoning demand through hidden structure, reversed targets, representation shifts, synthesis or deeper inference. Difficulty must not be inflated merely through larger numbers, uglier fractions or extra arithmetic.

## Answer contract

Every selected or generated item must have a machine-checkable answer contract. The production contract is:

`ProductionKits/common/contracts/math-answer-contract.schema.json`

It requires a canonical answer, accepted equivalents, at least one solution path, independent verification checks, domain conditions, multiplicity semantics and `independent_solver_status = PASS`.

Core (2) source items are also independently cross-checked by the Core2 production kit before becoming legal Core (2A) inputs.

## Citation contract — shown with the question itself

Every learner question must carry:

```text
WHERE THIS QUESTION CAME FROM
```

A consolidated bibliography alone is invalid.

For source questions, the inline note identifies the exact Core (2) source question. For fresh questions, the note distinguishes:

- Core (1A) concept support;
- any Core (2) anchor;
- competition benchmark/archetype role where applicable;
- explicit disclosure that the question is a fresh workbook original.

Generated questions cannot claim official JEE/IOQM/RMO/INMO/IMO provenance unless the exact official source is genuinely being reproduced and verified under a separate exact-source policy.

## Learner-facing help

Use stable child-friendly labels:

```text
TRY IT FIRST
SMALL CLUE
BIGGER CLUE
HOW DO I START?
THINK IT THROUGH
FULL WORKING
QUICK CHECK
WHERE THIS QUESTION CAME FROM
```

Do not expose internal terms such as `reasoning route`, `repair route`, `grounding`, `learning atom`, `demand vector`, `transfer ladder`, registry IDs or publication-engineering terminology.

Core (2) H1/H2/H3 semantics map to:

```text
H0  TRY IT FIRST
H1  SMALL CLUE       — notice useful structure
H2  BIGGER CLUE      — choose the mathematical idea / representation
H3  HOW DO I START?  — first executable mathematical move
```

A generated item's help is validated against the full working so that a clue cannot simply disclose a solution step or answer.

## Production-kit contracts

Core (2A) uses:

- `ProductionKits/common/contracts/math-task-intent.schema.json`
- `ProductionKits/common/contracts/math-source-bundle.schema.json`
- `ProductionKits/common/contracts/math-answer-contract.schema.json`
- `ProductionKits/common/contracts/math-product-blueprint.schema.json`
- `ProductionKits/Core2A/contracts/math-core2a-candidate-set.schema.json`
- `ProductionKits/common/profiles/scaffold-profiles.json`
- `ProductionKits/common/registry/benchmark-source-registry.json`

The existing semantic contract `Core2A/contracts/math-core2a-challenge-plan.schema.json` remains a governed Core2A semantic surface; the production kit adds executable routing, selection, answer checking and purpose differentiation around it.

## Golden fixtures

The production kit ships exactly three cross-mode golden fixtures:

1. `golden/01-starter-hidden-roots.json` — STARTER behavior;
2. `golden/02-practice-vs-revision.json` — same mathematical input, different PRACTICE and REVISION products;
3. `golden/03-competition-theory-of-equations.json` — COMPETITION near-transfer, structural variation and mixed synthesis.

The golden rule is: **copy the process, not the fixture mathematics**.

## Required fail-closed checks

At minimum:

```text
CORE2A_USER_PURPOSE_REQUIRED
CORE2A_PURPOSE_CANDIDATE_COVERAGE_GAP
CORE2A_UNTAUGHT_MATH_REQUIRED
CORE2A_HINT_DISCLOSES_SOLUTION
CORE2A_HINT_DISCLOSES_ANSWER
CORE2A_SOURCE_ANSWER_CONTRACT_MISSING
CORE2A_NEAR_COPY_CHECK_FAILED
CORE2A_QUESTION_CITATION_MISSING
QUESTION_CITATION_NOT_INLINE
GENERATED_ITEM_FALSE_OFFICIAL_ATTRIBUTION
COMPETITION_BENCHMARK_OUTSIDE_COMPETITION_MODE
CORE2A_COMPETITION_BENCHMARK_MISSING
CORE2A_PURPOSE_DIFFERENTIATION_FAILED
```

## Release boundary

Core (2A) inherits upstream legality. It cannot upgrade provisional PCK, change learner diagnosis/treatment, alter source-question validity, invent official exam provenance, introduce untaught mathematics or bypass human review gates.
