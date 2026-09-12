# Physics V2 — P-I Core2 transfer, hint ladder and Core1 linkage

P-I implements issue #257 under the #320 catch-up. It turns scope-eligible external
transfer items into learner-facing Core2 pages with a graded hint ladder, a First-Step
Reference, and an explicit link back to the Core1 lesson that taught the capability.

```text
P-I external transfer corpus       (source bodies, preserved exactly)
+ P-I external corpus classification (learner-independent eligible denominator)
+ P-G Core1 study plan               (what was actually taught)
+ P-F capability records             (structural obligations of the primary capability)
+ P-I authoring profile / badge policy / concept segregation
→ PhysicsCore2TransferPlan
```

## H1 Notice → H2 Model → H3 Start

The ladder is graded **by construction, then re-checked**. Each level declares what it may
not contain, and both the builder and the validator run the same content rules:

| level | job | may not contain |
|---|---|---|
| `H1_NOTICE` | direct attention to the decisive physical feature | relation, substitution, result, option label |
| `H2_MODEL` | name the model and the assumption that must hold | substitution, result, option label |
| `H3_START` | give only the first physically meaningful move | result, option label |

On top of the per-level rules, no hint may contain the text of the source answer option.
`HINT_REVEALS_ANSWER`, `HINT_LADDER_COLLAPSES_TO_SOLUTION` and `H1_NOTICE_SKIPPED` are all
falsifier-tested.

Hint content is composed from the P-D reasoning route and the P-F structural obligations of
the primary capability — the attention clause, model clause and first move are derived from
whether the capability carries frame/sign, multiphase, graph or model-validity obligations.
There is no per-topic hint table.

## First-Step Reference

One entry per problem family, derived from the same structure
(`first_step_reference_source` in the authoring profile). Every transfer page references
one, and a family without an entry fails `FIRST_STEP_REFERENCE_MISSING`.

## Core1 linkage and concept segregation

Every page names its `primary_capability_ref` and the Core1 lesson that taught it, and
distinguishes it from `supporting_links`. A page may not require a capability Core1 never
taught unless `physics-concept-segregation.json` declares it as a transfer extension **with
an explicit Core1 bridge lesson** — otherwise `CORE2_REQUIRES_UNTAUGHT_CONCEPT`.

## Source-body custody

External bodies are carried through byte-identically: stem, options, figure semantics and
source link are compared against the corpus digest on every validation pass.
`SOURCE_BODY_REWRITTEN`, `MCQ_OPTION_LOST`, `SOURCE_FIGURE_LOST` and
`SOURCE_LINK_MISSING_OR_WRONG` are falsifier-tested.

## The corpus is synthetic and says so

`fixtures/physics-external-transfer-source.fixture.json` declares
`production_claim: false` and an explicit provenance note: these are Grade 9 Physics
transfer items authored for this repository's P-I proof, not extracted from any real
examination paper. A corpus that claims production status fails
`SYNTHETIC_CORPUS_CLAIMED_AS_PRODUCTION`. Nine candidates are classified, eight eligible;
the ninth is deliberately out of scope (an electricity item) and must not be published,
which proves the eligibility gate actually excludes.

## Attempt invariance

Classification happens before any learner evidence is read, so the eligible denominator,
the page set and the family mapping are identical in the no-attempt and attempt-present
runs (`ATTEMPT_RUN_CHANGES_EXTERNAL_ELIGIBILITY`).

## Running

```bash
python "Grade 9/V2/Physics/Core2Transfer/contracts/validate_contracts.py"
python "Grade 9/V2/Physics/Core2Transfer/tests/test_physics_core2_transfer.py"
```

## Non-claims

P-I authors transfer semantics. Subject, pedagogy and assessment expert review remain
`PENDING`; `release_authority_state` is `PILOT_ONLY_HUMAN_EXPERT_RELEASE_NOT_GRANTED`. The
guide-demand badge describes how much scaffolding a page supplies, not a measured item
difficulty and not a learner ability claim. PR #156 is not a producer input here.
