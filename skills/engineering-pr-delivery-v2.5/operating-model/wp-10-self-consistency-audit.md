# WP-10 — Self-consistency Audit

## Status

IN PROGRESS

## Basis

- predecessor: CP-R010 / merged PR #396
- merged basis: `fb28a0817cab109a1120e3826ce11439b49586de`
- completion before WP-10: 97%
- scope: repository-neutral V2.5 skill only

## Audit objective

Prove that V2.5 has one coherent control model across schemas, templates, validators, renderers, operator documentation, tests, and `SKILL.md` before final PR-readiness cleanup.

The audit must identify and either resolve or explicitly classify:

1. schema ↔ template ↔ procedural-validator drift;
2. producer ↔ consumer gaps and unread durable fields;
3. orphan validators/renderers/scripts not reachable from aggregate conformance or documented operator flows;
4. obsolete names or retired concepts still presented as current;
5. silent defaults that can change authority/readiness/lifecycle semantics;
6. duplicate or competing authority claims;
7. lifecycle/material-authority inconsistencies;
8. progress/acceptance/report projection inconsistencies;
9. issue/roadmap/projection ownership inconsistencies;
10. discovery/qualification/takeover/readiness inconsistencies;
11. generated-view claims that conflict with repository authority;
12. downstream-specific logic or V2 contamination.

## Required surfaces

```text
SKILL.md
operating-model/**
templates/**
schemas/**
scripts/**
blueprints/**
tests/**
.github/workflows/engineering-pr-delivery-v2.5.yml
```

## Classification

Every finding is recorded as one of:

```text
FIXED
DOCUMENTED_INTENTIONAL
DEFER_TO_WP11
BLOCKING
```

WP-10 is not complete while any `BLOCKING` finding remains.

## Exit criteria

- a deterministic self-consistency audit can run against the skill tree;
- retired vocabulary and stale future-tense delivery claims are removed or deliberately historical;
- aggregate conformance/operator documentation cover all material validators and projections;
- durable object producer/consumer ownership is documented;
- no multiple-source authority conflict remains;
- no downstream-specific logic is introduced;
- root unit + dedicated stress suites pass on the exact checkpoint head;
- CP-R011 advances the completion program from 97% to 99% and makes WP-11 the only successor.
