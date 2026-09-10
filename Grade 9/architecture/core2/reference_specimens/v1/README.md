# Core (1) / Core (2) Golden Reference Specimen v1

## Purpose

This folder defines the cold-start onboarding/review surface for publisher agents. It is **not** curriculum authority, **not** a production release package, and **not** a replacement for the normative schemas.

Use the reference system as:

```text
RULES        -> architecture / subject profile
SHAPE        -> production JSON schemas
EXAMPLE      -> clearly labelled reference-example JSON + human PDFs
STRUCTURE    -> PublicationStructure JSON
ENFORCEMENT  -> validators / CI
```

## State vocabulary — do not blur these

Every specimen object must use one of these meanings:

- `REFERENCE_EXAMPLE` — a concrete, internally coherent example that demonstrates the contract.
- `NOT_EXERCISED` — the architecture supports the feature, but this miniature intentionally does not instantiate it. This is **not** PASS.
- `PARTIAL` — the specimen demonstrates part of an invariant but does not prove full production closure.
- `PLACEHOLDER` — forbidden in material truth/evidence fields.

A missing production fact, source, right, representation semantic, or question-custody object is never represented as `TODO`/`TBD`. The production path must block or return `CORE1_RESEARCH_GAP`.

## Canonical machine reference files

Read in this order:

1. `core1-reference.example.json` — compact Core (1) ResearchPackage example.
2. `core2-reference.example.json` — B40/B90 product morphology and practice topology over the exact same ResearchPackage.
3. `coverage-checklist.json` — explicit `COVERED` / `PARTIAL` / `NOT_EXERCISED` feature inventory.
4. `validate_reference_specimen.py` — verifies digest linkage, no material placeholder tokens, same-research B40/B90 reuse, morphology difference, and state vocabulary.
5. `../../contracts/v1/publication-structure.schema.json` and the bridge/reference examples under `../../contracts/v1/examples/`.

The JSON is the primary agent reference. Human PDFs are the visual/product-grammar review surface when attached to the task.

## Structural basis

The morphology is distilled from the mature Physics PR #156 Motion production pattern and the PR #157 Chemistry production contract. It preserves reusable structural invariants rather than chapter-specific wording or artwork.

Lower-baseline / BRIDGE example:

```text
physical situation or depiction
-> NOTICE
-> SAY IN WORDS / CONCEPT
-> build/reconstruct relation
-> WORKED EXAMPLE
-> GUIDED 1
-> GUIDED 2 with fading
-> INDEPENDENT TRANSFER
-> RETRIEVAL CHECK
```

High-baseline / REFERENCE example:

```text
contrast / compact depiction
-> decisive NOTICE or MODEL BOUNDARY
-> reconstruct/compress relation
-> INDEPENDENT TRANSFER
-> RETRIEVAL CHECK
```

The same frozen ResearchPackage is reused. Bxx changes learner treatment, not Core (1) truth or package identity.

## Appendix namespaces

The Core (1) human reference may use **Research Appendix A/B/C** for evidence/source custody, representation/reasoning obligations, and handoff/coverage reporting. These are reference-specimen research appendices only; they are not learner products.

Core (2) retains the normative learner appendices:

```text
Appendix A — Core Practice
Appendix B — Core Solutions
Appendix C — Printable Handout
```

Do not confuse the two namespaces.

## Practice / help topology

Static mature learner products use:

```text
ATTEMPT
-> OPTIONAL HELP LATER
   H1 NOTICE
   H2 MODEL
   H3 START
-> COMPLETE SOLUTIONS LATER
-> MIXED DIAGNOSIS AFTER SOLUTIONS when applicable
```

Do not place all H1/H2/H3 immediately below a question in a static PDF. The learner must be able to attempt without involuntarily reading the start hint.

Solutions preserve:

```text
QUESTION RECAP
REPRESENTATION when material
WHY THIS WORKS
METHOD
ANSWER / CHECK
CONCEPT TO KEEP
RETURN TO QUESTION
RETURN / REPAIR TO LESSON when applicable
```

## Navigation

For mature profiles the product structure declares:

```text
question -> hint
question -> solution
solution -> question
solution -> lesson / repair target
```

A PDF with zero broken internal links but no required navigation routes is not sufficient evidence.

## Production packaging remains unchanged

The human Core (2) reference PDF may be composite for agent onboarding. That is explicitly a `REFERENCE_EXAMPLE` convenience and does not change production packaging.

Where `delivery_contract = FULL_TOPIC_PAIR`, production still requires two reciprocal learner products:

```text
CORE_STUDY_GUIDE
+
EXAMSIDE_SOLUTION_TRANSFER
```

with shared research identity and reciprocal pair identity.

## Core (1) boundary

Do not move learner morphology into frozen Core (1). Core (1) owns scope, claims, conditions, evidence, formal objects, representation semantics and research-grounded reasoning/misconceptions. Core (2) owns sequence, fading, disclosure timing, page intent, navigation and learner-facing connective structure.

If a structure step needs subject truth absent upstream, return `CORE1_RESEARCH_GAP`; never fill it from this specimen.

## Current maturity note

The reference specimen deliberately covers many high-value requirements while marking some capabilities `PARTIAL` or `NOT_EXERCISED`. Use `coverage-checklist.json`; never infer full PR #156/#157 conformance merely because an example file exists.
