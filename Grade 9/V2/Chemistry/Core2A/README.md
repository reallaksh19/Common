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

## Current implementation status

Both lanes now have executable semantic planners.

- `engine/build_chemistry_core2a_source.py` realizes the governed `SOURCE_CORE2` denominator with source-fidelity, Core1A hint bindings, learner support, answer closure and inline provenance.
- `engine/build_chemistry_core2a_challenges.py` deterministically selects and realizes `GENERATED_ORIGINAL` challenges from supported problem families, performs an independent Chemistry recomputation, applies a near-copy gate, binds answer/provenance contracts and fails closed when a family lacks an authorized generation/validation recipe.

This is still pre-rendering. Passing these semantic planners does not establish mature learner-product visual quality or any pending human release gate.

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

The generated-lane engine is intentionally fail-closed. A problem family is generated only when `policies/chemistry-core2a-challenge-realization-policy.json` names both a governed transformation recipe and an independent validator. Unsupported families are recorded as skipped rather than being free-written by an agent.

The first validator-backed family set is:

```text
PF-FORMULA_CHARGE_PARSE
  → notation-role verification

PF-MACRO_PARTICLE_SYMBOL_TRANSLATION
  → particle identity/count/coefficient verification

PF-CONSERVATION_LEDGER
  → independent formula parse + atom-ledger recomputation

PF-CONDITION_VALIDITY
  → source-condition preservation verification

PF-AGENT_ROLE_ASSIGNMENT
  → electron-loss / reacting-species role recomputation
```

## Deterministic challenge selection

Selection is based on problem families, not raw source-question count.

Default policy:

```text
1 NEAR_TRANSFER per eligible supported problem family
1 structural variation for eligible D2/D3 families when an explicit alternate-direction recipe exists
MIXED_SYNTHESIS only when explicit compatibility/maturity authority exists
```

`MIXED_SYNTHESIS` is therefore not inferred merely because two buckets happen to exist. Until compatibility authority is present, its generated count must remain zero.

The canonical details live in `../LearnerProduct/policies/chemistry-core2a-execution-policy.json`, `../LearnerProduct/policies/chemistry-competitive-challenge-policy.json`, the competitive archetype registry, and `policies/chemistry-core2a-challenge-realization-policy.json`.

## Near-copy gate

Every fresh prompt is compared against all governed source stems, not only its anchor. Exact normalized copies are forbidden. The challenge-realization policy also sets deterministic sequence-similarity and token-Jaccard ceilings.

A failed near-copy check is a hard stop. The item is not relabelled as “fresh” and released anyway.

## Hint pre-teaching

Learner labels map to internal support semantics:

```text
SMALL CLUE       = H1 key Chemistry concept/criterion
BIGGER CLUE      = H2 representation/model
HOW DO I START?  = H3 first executable symbolic/quantitative move
```

Every reveal must bind to already-taught Core (1A) evidence. Generated items reuse those governed bindings rather than inventing a second hint curriculum.

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

This invariant applies equally to source and generated lanes.

## Per-question provenance

Every question carries its own `WHERE THIS QUESTION CAME FROM` block. A bibliography at the end does not satisfy this requirement.

Source items identify the exact Core (2) source. Generated items identify Core1A concept support, the Core (2) transfer anchor and the fresh/original origin disclosure. Generated items set `official_past_question_claim=false` unless an independently verified exact official source exists; the current generator never upgrades a fresh item into an official claim.

## Independent Chemistry validation

Generated items and worked solutions should be machine-checked where applicable for:

```text
formula/charge notation roles
particle identity and entity multipliers
atom/reaction conservation
reaction-condition preservation
species/electron-transfer role direction
formula charge neutrality
ionic charge preservation
molar mass
unit/dimensional consistency
concentration denominator
stoichiometric mole ratio
oxidation-number sums/changes
```

Only the first five families above currently have executable generated-lane validators. The remaining checks are roadmap obligations, not silently claimed as implemented.

## Release boundary

Core (2A) cannot upgrade provisional upstream Chemistry/PCK authority, alter learner treatment, change source validity, invent official provenance, introduce untaught Chemistry or bypass human subject/pedagogy/assessment/visual review.

The canonical cross-product order is defined in `../LearnerProduct/EXECUTION_CONTRACT.md`.
