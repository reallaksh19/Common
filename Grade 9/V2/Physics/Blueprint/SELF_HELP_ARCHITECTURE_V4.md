# Physics Self-Help Architecture V4 — technically explicit, family-first, asymmetric A/B

V4 keeps the V3 family-first architecture and fixes two failures exposed by the M2D-SBA-23 pilot:

1. a Hard Core1B can still degrade into a prose worksheet unless technical reconstruction is mandatory;
2. a generated PDF can still contain unusable figure/text collisions unless visual layout integrity is fail-closed.

## Canonical authoring order

```text
SUBTOPIC / SBA BUCKET
        ↓
HIDDEN INVARIANT(S)
        ↓
PREREQUISITE BRIDGES
        ↓
INFERENTIAL JUMPS
        ↓
PROBLEM FAMILIES
        ↓
TECHNICAL REPRESENTATIONS
        ↓
MISCONCEPTIONS + CHECKS
        ↓
        ├── CORE1A  declarative-dominant technical teaching
        └── CORE1B  generative-dominant technical reconstruction
```

For Core2, frozen question authority and legal-pool custody remain unchanged. Student knowledge % or owner override adapts support/selection only.

## Hard means technical closure, not prose depth

For a Hard Physics bucket, long explanation is not enough.

When material, the learner product must visibly expose:

- formal notation;
- equations / transformations;
- vector or component constructions;
- diagrams / graphs / event lines;
- worked intermediate algebra;
- model conditions;
- sign / physical / dimensional / limiting checks.

A prose-only Hard release is noncompliant whenever an expert solution depends on one of those technical forms.

## Core1A

Core1A remains declarative-dominant.

Its job is to make the technical model complete:

`IDEA → NOTATION → REPRESENTATION → EQUATIONS → WORKED TECHNICAL REASONING → PROBLEM FAMILY → CHECK`

The 10/20/30 Easy/Medium/Hard page values remain soft Core1A capacity ceilings, not targets.

## Core1B

Core1B remains smaller and selective, but "selective" must not mean "prose-only".

For each fragile checkpoint, ask:

> What technical representation would an expert construct here?

Then make the learner reconstruct it.

Examples:

- label / complete a velocity triangle;
- fill missing component equations;
- sketch both frame-dependent trajectories;
- complete a free-body diagram;
- build an event timeline;
- derive or rearrange the governing relation.

A Hard Core1B consisting mainly of prose prompts + blank lines is a release failure.

The full H1→H2→H3 ladder remains conditional on substantive tasks. Representation tasks may use:

`INCOMPLETE REPRESENTATION → LEARNER COMPLETES → TECHNICAL CHECK → EXPLAIN KEY FEATURE`

## Core2A / Core2B

Core2A must show expert technical working for representative legal problem families. Core2B must make the learner select or construct the needed representation/model before solution reveal when that representation is part of the transfer demand.

Knowledge % / owner override changes support density and item progression only; it never changes legality.

## Layout integrity

Learner PDFs are not released merely because a PDF file was generated.

Production layout must be flow-based or otherwise collision-validated. Figures are isolated layout blocks with explicit bounds. Free-canvas text labels may not overlap headings/body text.

Every new layout is rendered page-by-page and fails closed on:

- text/text overlap;
- text/figure overlap;
- clipped labels;
- unreadable equations;
- broken glyphs;
- header/figure collision.

## Normative policies

- `Blueprint/policy/self-help-core-publication.v4.json`
- `Blueprint/policy/technical-density-and-figure-contract.v1.json`
- `Blueprint/policy/pdf-layout-integrity.v1.json`
- `Blueprint/policy/core1ab-bucket-authoring.v2.json`
- `Blueprint/policy/core2ab-knowledge-routing.v1.json`

V4 supersedes the V3 assumption that representation sufficiency alone was enough. For Hard Physics, fragile technical representations must be learner-visible and reconstructable where material.
