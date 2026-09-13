# Chemistry V2 — Core (2A): purpose-specific practice + governed challenge transfer

Core (2) remains the source-transfer authority. Core (2A) is a purpose-specific learner product and must not default to being Core (2) again with more scaffolding or more pages.

## Resolve purpose before authoring

Before any Core (2A) is authored, the user purpose must be explicit:

```text
STARTER
PRACTICE
REVISION
COMPETITION
```

If the purpose is unresolved, ask the user. Do not infer it silently.

```text
CORE2A_PURPOSE_UNRESOLVED
```

The selected purpose must materially change question selection, support density, workspace, challenge mix and page density.

## Source belongs on Sheet 1 of every question

Every Core (2A) attempt sheet must show the question's source/provenance basis on Sheet 1. A bibliography or book-level construction-reference page is not sufficient.

For `SOURCE_CORE2`, show the exact human-readable source locator beside or immediately before the question.

For `GENERATED_ORIGINAL`, show the construction references used to shape the question plus the governed Chemistry content anchor. The Sheet-1 wording must distinguish a construction reference from an official question source. A fresh question may not be presented as an official NCERT/Olympiad/exam item.

```text
CORE2A_SHEET1_SOURCE_MISSING
```

## Competition mode

Competition mode defaults to fresh transfer rather than replaying the complete Core (2) source set. Difficulty should come from reasoning form: reversed targets, hidden information, constraint chaining, comparison/ranking, error diagnosis, representation switching and other governed challenge archetypes.

Before fresh Competition questions are authored, inspect at least two authoritative/official external school-science competition sources and record what was learned at the construction-pattern level. Useful benchmark forms include:

- particle-composition tables;
- multi-statement selection;
- coded-species deduction;
- reverse electron/charge inference;
- integer reconstruction;
- error diagnosis from plausible wrong work.

Do not copy benchmark question text. The existing near-copy gate still applies. Store benchmark URLs or stable refs in machine custody and show the applicable construction references on every generated question's Sheet 1.

## Two-page default

A learner question should normally occupy no more than two physical pages:

```text
PAGE 1 — ATTEMPT
source / construction references
+ question
+ demand-sized workspace
+ 1–2 technical clues at the bottom, usable only if stuck

PAGE 2 — CHECK AND SOLUTION
QUICK CHECK
+ FULL WORKING
+ question-specific KEY RELATION / DECISION RULE
+ independent CONSISTENCY CHECK
```

A clue state is not automatically a clue page. A working area is not automatically a dedicated blank page. Any exception above two pages requires a specific reason.

Technical clues must tell the learner what equation, relation, count, comparison or falsification test to execute next. Generic encouragement or a generic “competition start rule” does not satisfy the clue requirement.

Answer-page sidebars must be question-specific. A generic statement such as “the formula unit is neutral” is insufficient unless it is instantiated with the current symbols/numbers (for example, `2q_X + 3(-2) = 0`). The consistency check must independently recompute or test the current result.

Repeated learner-facing slogans, generic repair footers and repeated “not an official question” disclaimers are forbidden.

## Core (2A) lanes

When source practice is explicitly needed, Core (2A) can still realize the governed source lane:

```text
SOURCE_CORE2
  preserve the governed source question and its integrity state
```

Fresh challenge practice uses:

```text
GENERATED_ORIGINAL
  fresh transfer grounded in taught Chemistry
```

The lanes do not share provenance semantics and must not be conflated.

## Answer closure

Compression never weakens self-study closure:

```text
CLOSED QUESTION
= QUICK CHECK
= FULL WORKING

GENUINELY OPEN RESPONSE
= EXPECTED RESPONSE RUBRIC
```

## Generated challenge custody

Generated questions must be grounded in:

- taught Core (1)/Core (1A) authority;
- an active governed problem family;
- an approved Chemistry competitive archetype;
- independent Chemistry verification;
- passed near-copy checking against governed source stems and custodied external benchmarks;
- per-question Sheet-1 construction-reference provenance.

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

Families without a governed recipe + independent validator are skipped with a recorded reason rather than free-written.

## Hint pre-teaching

Learner labels map to internal support semantics:

```text
SMALL CLUE       = H1 key Chemistry concept/criterion
BIGGER CLUE      = H2 representation/model
HOW DO I START?  = H3 first executable symbolic/quantitative move
```

For Competition mode, the rendered attempt page normally exposes only one or two compact technical clues after the workspace rather than the full H1/H2/H3 stack. The underlying reveals must still bind to already-taught Core (1A) evidence.

## Reasoning visuals

Core (2A) does not choose diagrams during page rendering. Its representation binding points to already-taught Core1A/C-H evidence. The learner renderer invokes selected Chemistry vector primitives when required semantic data is available.

A governed visual obligation cannot silently become decoration or disappear. An item requiring visual reasoning cannot close with zero realized reasoning visuals.

## Production kit

`../ProductionKit/` provides the executable task router, source/answer contracts, scaffold profiles, learning-representation builder/validator, product-packet builder, and multi-product golden fixtures. Core (2A) Sheet-1 source custody and the two-page budget are enforced there before rendering.

## Physical-PDF gate and release boundary

C-LP-23 checks actual PDFs for page geometry, font floor, clipping/overlap, extracted-text internal-ID leakage, reasoning-visual closure and raster rendering. C-LP-24/25 then freeze final audit and handoff hashes.

Core (2A) cannot upgrade provisional upstream Chemistry/PCK authority, alter learner treatment, change source validity, invent official provenance, introduce untaught Chemistry or bypass human subject/pedagogy/assessment/visual review.

**Machine PASS is not learner-product release.** Human subject correctness, pedagogy, assessment design, actual-size visual usability and mature-design quality remain independent gates.
