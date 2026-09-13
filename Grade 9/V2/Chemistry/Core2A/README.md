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

## Current implementation

Both semantic lanes are executable and are now wired into the canonical learner-product runner through C-LP-21.

`SOURCE_CORE2` preserves every governed C-I item in order, including source text/options/subparts, figure semantics, conditions/states/units, source-QC state and source-fidelity custody. It binds each item to exactly one Core1A bucket and the exact pre-taught H1/H2/H3 evidence.

`GENERATED_ORIGINAL` deterministically selects validator-backed challenge targets by problem family. Unsupported families are skipped with a recorded reason rather than free-written. Generated items reuse taught Core1A capability/hint evidence, pass an independent Chemistry validator, pass an all-source near-copy gate, and disclose fresh/original provenance.

The canonical semantic runner emits both plans and an answer-closure audit before stopping at the page-render boundary.

## Source lane learner flow

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
- a passed near-copy check against every governed source stem;
- inline provenance.

Generated questions must never claim official NCERT/Olympiad/exam provenance unless an exact official source is independently verified.

Challenge difficulty must come from Chemistry reasoning, representation or transfer demand, not bigger numbers, uglier decimals/exponents or extra arithmetic alone.

## Deterministic challenge selection

Selection is based on problem families, not raw source-question count.

```text
1 NEAR_TRANSFER per supported problem family
1 structural variation for eligible D2/D3 families when an explicit family recipe authorizes it
MIXED_SYNTHESIS only when explicit bucket-compatibility/maturity authority exists
```

Current validator-backed families are:

```text
PF-FORMULA_CHARGE_PARSE
PF-MACRO_PARTICLE_SYMBOL_TRANSLATION
PF-CONSERVATION_LEDGER
PF-CONDITION_VALIDITY
PF-AGENT_ROLE_ASSIGNMENT
```

Families without a governed recipe + independent validator are not generated yet.

## Hint pre-teaching

Learner labels map to internal support semantics:

```text
SMALL CLUE       = H1 key Chemistry concept/criterion
BIGGER CLUE      = H2 representation/model
HOW DO I START?  = H3 first executable symbolic/quantitative move
```

Every reveal must bind to already-taught Core (1A) evidence. A question whose hint contains new Chemistry is not ready.

## Mandatory answer path

No learner-facing objective Core2A question may be published without:

```text
QUESTION
= QUICK CHECK
= FULL WORKING
```

Genuinely open-ended questions instead require an explicit `EXPECTED RESPONSE` rubric.

The quick check is concise; it is not a duplicate full solution. The full working exposes the complete Chemistry method, equations/steps, notation and verification.

## Per-question provenance

Every question carries its own `WHERE THIS QUESTION CAME FROM` block. A bibliography at the end does not satisfy this requirement.

Source items identify the exact Core (2) source. Generated items disclose Core1A concept support, the Core2 anchor when used, and `GENERATED_ORIGINAL` status. Non-web internal custody links are forbidden from learner provenance.

## Independent Chemistry validation

Current generated-item validators independently recompute the applicable Chemistry rather than trusting the authored answer. The roadmap can expand validators for molar mass, units/dimensions, entity multipliers, concentration, stoichiometric ratios and additional redox/charge cases only when matching governed problem families are available.

## Release boundary

Core (2A) cannot upgrade provisional upstream Chemistry/PCK authority, alter learner treatment, change source validity, invent official provenance, introduce untaught Chemistry or bypass human subject/pedagogy/assessment/visual review.

The semantic plans are not rendered learner pages. C-LP-22 page rendering and downstream visual/final/handoff gates remain separate and pending.
