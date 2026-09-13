# Grade 9 V2 — Learning Blueprint v0

This directory is the cross-subject control/evidence layer above subject-specific Core1/Core2/Core1A/Core2A production systems.

Blueprint v0 deliberately does **not** author teaching prose, choose diagrams, infer misconceptions, or generate questions. Its job is to make the first architectural invariants executable:

1. original evidence and derived claims are different namespaces;
2. Core1-first and Core2-first are both legal routes;
3. routing is selected from evidence state rather than hard-coded subject order;
4. missing evidence remains missing/unknown rather than becoming zero importance;
5. handoff bundles contain at most three subtopics, without limiting later learning-atom decomposition;
6. owner overrides change operational action while preserving the system finding;
7. conflicts and uncertainty may block execution instead of being silently reconciled.

## v0 executable flow

```text
GROUND-TRUTH MANIFEST
        ↓
freeze_ground_truth.py
        ↓
ROUTING INPUT (SA/SS/QE/QR/UA/CI + <=3 subtopics)
        ↓
route_evidence.py
        ↓
SYSTEM ROUTE
        ↓
optional apply_owner_override.py
        ↓
FINAL OPERATIONAL ROUTE
```

The convenience entrypoint is:

```bash
python 'Grade 9/V2/LearningBlueprint/engine/run_blueprint_v0.py' \
  --ground-truth path/to/ground-truth.json \
  --routing-input path/to/routing-input.json \
  --out-dir build/blueprint-v0
```

Add `--override path/to/override.json` only when the owner intentionally changes an operational decision.

## What v0 does not claim

Blueprint v0 does not yet implement Core1/Core2 independent passes, claim-level V packets, the Join compiler, learner-state compilation, Core1A assimilation decomposition, taught-state receipts, or Core2A transfer eligibility. Those are later blueprint milestones. Keeping them out of v0 prevents a prose-only architecture from masquerading as an executable pedagogy system.
