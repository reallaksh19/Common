# V2-06 Publication Realization

V2-06 owns the physical realization boundary for the Grade 9–11 V2 producer.

```text
LearnerSemanticProduct
+ PublicationTarget
+ PublicationRealizationPolicy
→ PublicationStructure
→ deterministic renderer
→ exact candidate PDF bytes
→ PhysicalPageMap
→ PublicationAudit
→ PublicationManifest
```

## Authority

Publication Realization may decide structure, page intent, placement, typography/render mechanics, and realization primitives. It may not modify canonical truth, learner diagnosis, StudyModel obligations, or LearningDesign choreography.

## Key invariants

- every `MATERIAL` semantic item is accounted for exactly once;
- structure contains refs, not rewritten subject semantics;
- physical placement evidence is emitted by the renderer while producing the artifact;
- exact PDF SHA256 is bound into `PhysicalPageMap`, audit, and manifest;
- an independent validator recomputes custody from bytes and mappings;
- package digest is deterministic and non-self-referential;
- engineering/custody PASS leaves subject, pedagogy, visual, and benchmark validation unresolved.

## Synthetic proof

`fixtures/learner_semantic_product.synthetic.json` is synthetic and contains no real learner data. CI renders a deterministic minimal PDF solely to exercise custody and physical-placement contracts.

This stage does not claim mature learner-product quality.
