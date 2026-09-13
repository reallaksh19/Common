# Chemistry V2 — Core (2A): source practice + governed challenge practice

Core (2) remains the source-transfer authority. Core (2A) is the learner-facing practice realization.

Core (2A) has two strictly separated lanes:

```text
SOURCE_CORE2
  preserve the governed source question and its integrity state

GENERATED_ORIGINAL
  add fresh competitive-style transfer grounded in taught Chemistry
```

The lanes may share learner-support presentation, but they do not share provenance semantics.

## Source lane

A source item must preserve source identity, order, stem, givens, options, subparts, units, source-integrity/QC state and approved attempt-before-solution structure.

Core (2A) may add:

```text
TRY IT FIRST
SEE THE IDEA
WRITE THIS FIRST
SMALL CLUE
BIGGER CLUE
HOW DO I START?
WATCH FOR THIS
THINK IT THROUGH
CHECK YOUR CHEMISTRY
QUICK CHECK
FULL WORKING
WHERE THIS QUESTION CAME FROM
```

It may not silently rewrite damaged/ambiguous source chemistry. Source normalization requires an explicit QC record.

## Generated challenge lane

Generated questions must be fresh/original instances grounded in:

- taught Core (1)/Core (1A) authority;
- one or more mature problem families;
- an approved Chemistry competitive archetype;
- independently verified Chemistry and answer;
- a passed near-copy check;
- inline provenance.

Generated questions must never claim official NCERT/Olympiad/exam provenance unless an exact official source is independently verified.

Challenge difficulty must come from Chemistry reasoning, representation or transfer demand, not bigger numbers, uglier decimals/exponents or extra arithmetic alone.

## Deterministic challenge selection

Selection is based on problem families, not raw source-question count.

Default policy:

```text
1 NEAR_TRANSFER per eligible problem family
1 structural variation for eligible D2/D3 families when a valid alternate reasoning direction exists
MIXED_SYNTHESIS only when at least two compatible mature taught buckets exist
```

The canonical details live in `../LearnerProduct/policies/chemistry-core2a-execution-policy.json` and `chemistry-competitive-challenge-policy.json`.

## Hint pre-teaching

Learner labels map to internal support semantics:

```text
SMALL CLUE       = H1 key Chemistry concept/criterion
BIGGER CLUE      = H2 representation/model
HOW DO I START?  = H3 first executable symbolic/quantitative move
```

Every reveal must bind to already-taught Core (1A) evidence. A question whose hint contains new Chemistry is not ready.

## Mandatory answer path

No learner-facing question may be published without a way for the learner to check the work.

For objectively checkable questions:

```text
QUESTION
= QUICK CHECK
= FULL WORKING
```

For genuinely open-ended questions:

```text
QUESTION
= EXPECTED RESPONSE rubric
```

The quick check is concise; it is not a duplicate full solution. The full working must expose the complete Chemistry method, equations/steps, units/notation and verification.

## Per-question provenance

Every question carries its own `WHERE THIS QUESTION CAME FROM` block. A bibliography at the end does not satisfy this requirement.

Source items identify the exact Core (2) source. Generated items distinguish concept support, Core (2) anchor if used, competition benchmark role, and fresh/original status.

## Independent Chemistry validation

Generated items and worked solutions should be machine-checked where applicable for:

```text
formula charge neutrality
atom/reaction conservation
ionic charge preservation
molar mass
unit/dimensional consistency
particle/entity multipliers
concentration denominator
stoichiometric mole ratio
oxidation-number sums/changes
redox direction
```

## Release boundary

Core (2A) cannot upgrade provisional upstream Chemistry/PCK authority, alter learner treatment, change source validity, invent official provenance, introduce untaught Chemistry or bypass human subject/pedagogy/assessment/visual review.

The canonical cross-product order is defined in `../LearnerProduct/EXECUTION_CONTRACT.md`.
