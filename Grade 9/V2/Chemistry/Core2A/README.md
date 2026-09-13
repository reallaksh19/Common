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

Both lanes are executable and wired through the canonical learner-product runner through C-LP-25.

`SOURCE_CORE2` preserves every governed C-I item in order, including source text/options/subparts, figure semantics, conditions/states/units, source-QC state and source-fidelity custody. It binds each item to exactly one Core1A bucket and the exact pre-taught H1/H2/H3 evidence.

`GENERATED_ORIGINAL` deterministically selects validator-backed challenge targets by problem family. Unsupported families are skipped with a recorded reason rather than free-written. Generated items reuse taught Core1A capability/hint evidence, pass an independent Chemistry validator, pass an all-source near-copy gate, and disclose fresh/original provenance.

The full runner now realizes these semantic plans into deterministic learner PDF pages, runs physical-PDF preflight, freezes the final machine audit and leaves reusable artifact hashes/handoff custody. Machine completion does not grant human release approval.

## Learner flow

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

Source chemistry may not be silently rewritten. Source normalization requires an explicit QC record.

## Attempt-first answer separation

The rendered product deliberately separates attempt and checking surfaces:

```text
attempt page
→ QUICK CHECK on a later page
→ FULL WORKING after the quick check
```

The learner is told where the answer check is. The quick check is concise; it is not a duplicate solution. Full working contains the governed reasoning route and independent Chemistry verification.

No learner-facing objective Core2A question may be published without:

```text
QUESTION
= QUICK CHECK
= FULL WORKING
```

Genuinely open-ended questions instead require an explicit `EXPECTED RESPONSE` rubric.

## Generated challenge lane

Generated questions must be fresh/original instances grounded in:

- taught Core (1)/Core (1A) authority;
- an active governed problem family;
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

## Per-question provenance

Every question carries its own `WHERE THIS QUESTION CAME FROM` block. A bibliography at the end does not satisfy this requirement.

Source items preserve exact machine custody of the Core (2) source, while the learner surface receives a human-readable source locator. Generated items disclose fresh/original status and supporting authority. Internal machine IDs and non-web custody links are forbidden on learner pages.

## Reasoning visuals

Core2A does not choose diagrams during page rendering. Its H2 binding points to already-taught Core1A/C-H representation evidence. The learner renderer invokes those selected Chemistry vector primitives when the required semantic data is available.

A governed visual obligation cannot silently become decoration or disappear. Secondary unavailable primitives are recorded; an item requiring visual reasoning cannot close with zero realized reasoning visuals.

## Independent Chemistry validation

Current generated-item validators independently recompute the applicable Chemistry rather than trusting the authored answer. The roadmap can expand validators for molar mass, units/dimensions, entity multipliers, concentration, stoichiometric ratios and additional redox/charge cases only when matching governed problem families are available.

## Physical-PDF gate and release boundary

C-LP-23 checks actual PDFs for page geometry, font floor, clipping/overlap, extracted-text internal-ID leakage, reasoning-visual closure and raster rendering. C-LP-24/25 then freeze final audit and handoff hashes.

Core (2A) cannot upgrade provisional upstream Chemistry/PCK authority, alter learner treatment, change source validity, invent official provenance, introduce untaught Chemistry or bypass human subject/pedagogy/assessment/visual review.

**Machine PASS is not learner-product release.** Human subject correctness, pedagogy, assessment design, actual-size visual usability and mature-design quality remain independent gates.
