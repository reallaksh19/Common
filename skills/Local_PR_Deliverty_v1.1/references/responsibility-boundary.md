# Common / project responsibility boundary

## Common owns process truth

Common v1.1 defines and validates:

- role/principal authority and forward-only stage responsibility;
- one-writer workspace safety;
- exact candidate, target ref/base, merge base, integration-tree and dependency identity;
- context reconciliation and freshness;
- review-lease semantics;
- evidence provenance and independence classes;
- result semantics and Owner-waiver semantics;
- trusted required-check/provider identity;
- merge readiness and post-merge canonical-target evidence.

Common does **not** decide whether a CAD arc, database transaction, browser frame, compiler output, or any other domain behavior is correct.

## Project protocol owns engineering truth

The pinned project protocol declares:

- acceptance criteria;
- verification-method IDs;
- which criteria require Super Review;
- protected Super Review harnesses;
- protected fixtures/baselines/oracles;
- external gates;
- escaped-defect regressions.

A project may strengthen Common. It may not weaken Common authority, evidence, freshness, candidate-identity, no-backflow, or fail-closed rules.

## Role production responsibilities

Coder produces the initial/next implementation and author evidence.

Reviewer is the next independent production pass. Reviewer inspects, diagnoses, fixes product defects within authority, adds regression coverage, reruns affected checks, records the lesson, and hands an improved candidate forward.

Coordinator / Super Reviewer consumes full parent/dependency context, executes the pinned project acceptance contract, fixes project/integration product defects within authority, reruns the unchanged protected acceptance surface, records project learning, and issues the engineering outcome.

Ordinary internal defects never route responsibility backward. An external/Owner/protected-policy boundary may pause forward production, but “the earlier role should fix it” is not a valid boundary.

## Independence boundary

Product material may change during Reviewer and Super Reviewer production.

The active acceptance surface may not be weakened to certify those changes. If the project protocol, harness, fixture, baseline, oracle or acceptance policy must change, that creates a new acceptance epoch with a new digest and fresh evidence.

