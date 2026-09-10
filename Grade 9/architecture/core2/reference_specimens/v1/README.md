# Core (2) Golden Product-First Reference Specimen v1

## Purpose

This folder defines the intended onboarding/review surface for cold-start publisher agents.

The reference specimen is not another subject authority and is not a replacement for schemas. It demonstrates how the frozen Core (1) material becomes an ordered learner product.

Use it as:

```text
RULES        -> architecture / subject profile
SHAPE        -> JSON schemas
STRUCTURE    -> PublicationStructure JSON
EXAMPLE      -> learner-facing product-first PDF
ENFORCEMENT  -> validators / CI
```

## Structural basis

The morphology is distilled from the mature Physics PR #156 Motion production pattern and the PR #157 Chemistry production contract. It preserves the reusable structural invariants rather than chapter-specific wording or artwork.

The key inherited behavior is:

```text
LOWER BASELINE / BRIDGE
physical situation or depiction
-> notice
-> say/build meaning
-> reconstruct relation
-> worked reasoning
-> Guided 1
-> Guided 2 with fading
-> independent transfer
-> retrieval

HIGH BASELINE / REFERENCE
contrast / compact depiction
-> decisive notice or model boundary
-> reconstruct/compress relation
-> independent transfer
-> retrieval
```

The same frozen ResearchPackage must be reusable for both profiles.

## Practice / help topology

Static mature learner products use:

```text
ATTEMPT
-> OPTIONAL HELP LATER
   H1 NOTICE
   H2 MODEL
   H3 START
-> COMPLETE SOLUTIONS LATER
-> MIXED DIAGNOSIS AFTER ATTEMPT/SOLUTIONS
```

Do not place all H1/H2/H3 immediately below the question in a static PDF. The learner must be able to attempt without involuntarily reading the start hint.

Solutions preserve:

```text
QUESTION RECAP
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

A PDF with zero broken internal links but no required links is not sufficient evidence of this topology.

## Machine examples

The canonical structure examples currently live with the contract so schema CI can validate them:

- `../../contracts/v1/examples/publication-structure.bridge.example.json`
- `../../contracts/v1/examples/publication-structure.reference.example.json`

Both use the same illustrative ResearchBundle ID and package digest but materially different ordered learning arcs. This is intentional: Bxx changes learner treatment, not Core (1) research identity.

## Core (1) boundary

Do not move this structure into the frozen Core (1) schemas. Core (1) owns scope, claims, conditions, evidence, formal objects, representations and research-grounded methods/misconceptions. Core (2) owns page sequence, support progression, disclosure timing, learner-facing connective prose and layout relationships.

If a structure step requires subject truth that is absent upstream, return `CORE1_RESEARCH_GAP`; do not fill it from the reference specimen.

## Current maturity note

`publication-structure.schema.json` plus the bridge/reference examples establish the machine contract for product morphology. The deterministic `run_core2.py` remains a conservative contract falsifier and is not itself the visual authority for PR156/PR157 morphology.

The remaining retirement gate for the old reference implementations is an exact-PDF, product-first reference specimen whose final bytes are reconciled against the declared PublicationStructure and whose production renderer/validator can enforce that morphology. See conformance row `C38`.
