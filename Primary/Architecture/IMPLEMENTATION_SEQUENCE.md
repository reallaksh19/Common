# Primary Grades 4–5 implementation sequence

**Canonical semantics track:** Common #162  
**Programme roadmap:** Study-Hub #40

The rollout is intentionally split so that educational meaning is frozen before app transport contracts become authoritative.

## Phase A — Common semantic authority

1. Freeze Primary integrated architecture and repository ownership.
2. Freeze Teacher Runtime vocabulary and invariants.
3. Freeze machine-readable semantic v1 candidate.
4. Wire Grade 4 Math and English skills to the Primary runtime for interactive tutoring.
5. Add source-boundary regression coverage for simplified grammar taxonomies.

Exit gate: a cold-start agent can understand learning state, session state, evidence, diagnosis, support, teacher moves, independent evidence, retention, transfer, and source boundaries without reading Study-Hub or Kani implementation code.

## Phase B — Study-Hub transport adaptation

1. Treat Common as semantic upstream.
2. Refactor Study-Hub PR #51 from canonical pedagogy definitions into adapters/serialization.
3. Keep `kani-content-v1`, `kani-catalog-v1`, `kani-activity-v1`, and `kani-attempt-v1` under Study-Hub transport governance.
4. Add only the minimum Primary evidence envelope required by the transport boundary.
5. Freeze KaniMission / ExperienceManifest serialization without duplicating educational truth.

Exit gate: transport schemas can point to Common semantic IDs and preserve them losslessly.

## Phase C — Grade 4 Math vertical slice

Use fraction equivalence as the first plumbing proof:

```text
Study-Hub teach
→ print independent try
→ Kani mission
→ immutable attempt evidence
→ return to independent task
→ delayed retrieval marker
```

The slice proves identity, provenance, renderer hand-off, attempt evidence, and return-to-learning. It does not claim the Teacher Runtime is correct yet.

## Phase D — Teacher Runtime replay

Replay the Math slice through synthetic learner states:

```text
conceptual confusion
transient/rushing lapse
language/access bottleneck
repeated failure requiring route change
rapid success requiring fade/transfer
return after 3–7 days
```

Exit gate: meaningfully different evidence produces meaningfully different TeacherDecisions/TeacherMoves.

## Phase E — Grade 4 English vertical slice

Use:

- inference/evidence reasoning; and
- adjective-order source-boundary regression.

The runtime must preserve source rules, avoid silent category invention, distinguish oral/written evidence where relevant, and leave the child with a reusable next-step cue.

## Phase F — supervised observation gate

Before broad scaling, observe a small real-child journey for:

```text
QR rushing
willingness to return from Kani
hint leakage
stars/timer/streak effects
instruction clarity
independent return performance
3–7 day retention
```

## Phase G — curriculum and Grade 5 scale

Add IB PYP and NCF-SE/NCERT mappings as overlays over canonical Common learning objects. Extend to Grade 5 through scope/depth profiles rather than duplicating the ontology.

## Deferred competition seam

IMO/IOM and Spell Bee remain later scope. They attach through `STRETCH` / `AssessmentDemandProfile` semantics and may not redefine ordinary curriculum mastery.