# Physics V2 — Core1B / Core2B Product Kit

Status: production-draft for review.

This kit adds learner-runtime layers downstream of the existing Physics A-layers.

```text
Core1  -> Core1A -> Core1B
truth     assimilation governance   learner teaching runtime

Core2  -> Core2A -> Core2B
source    transfer governance       evidence-gated transfer runtime
```

## Boundary

Core1B and Core2B do not change Physics truth, source identity, taught-state custody, validator legality, purpose policy, or provenance. They operationalize the already-authorized content for a learner.

Core1B turns a Core1A assimilation plan into teacher-quality concept construction, representation building, worked/faded practice, targeted repair, and learner evidence.

Core2B consumes only Core2A-legal transfer items and uses learner evidence to govern attempt-first support, transfer distance, repair routing, competitive progression, and retrieval.

## Invariants

1. A-layers decide what is valid; B-layers decide how the learner experiences it.
2. Teaching completion authorizes exposure; learner evidence authorizes escalation.
3. Internal states never leak into learner-facing copy.
4. A formula is treated as compression of a physical model, not a substitute for one.
5. Hints diagnose backward before revealing forward.
6. A wrong answer is not itself a diagnosis.
7. Repair the smallest knowledge structure that explains the error.
8. Competitive difficulty increases reasoning distance before arithmetic ugliness or syllabus distance.
9. Core2B cannot legalize an item rejected or unsupported by Core2A.
10. Core1B cannot invent Physics outside Core1/Core1A authority.

## MVP vertical slice

`Motion in a Plane -> Projectile vertical event` is the golden vertical slice because the upstream branch already contains Core1A coverage and a validator-backed Core2A golden.

The MVP demonstrates:

- prerequisite/atom graph;
- teacher-style Core1B unit;
- learner evidence and release receipts;
- Core2B direct, near-transfer, representation-transfer and reversed-target selection;
- hint routing;
- error classification;
- Core1B repair handoff;
- retrieval-state update;
- executable tests.

See `Core1B/` and `Core2B/` for normative contracts.