# Chemistry v7 PAL-assured learner products

This directory is a clean downstream realization layer over Chemistry LearningBlueprint v7.
It does not patch or reuse the rejected Core1B/Core2B PDFs.

Validation subtopic: **Observation -> evidence -> chemical inference** (`CAP-SEPARATE-OBSERVATION-INFERENCE`, `PF-EVIDENCE_TO_CLAIM`).

The product build is fail-closed:

1. load canonical authority packet;
2. validate v7 CCBOM coverage;
3. validate Core1 intrinsic difficulty and Core-purpose contracts;
4. validate Core2 learner fit and frozen-question custody;
5. compile four distinct products (Core1A, Core1B, Core2A, Core2B);
6. compute realized non-frozen prose overlap from the actual page model;
7. validate v7 similarity thresholds;
8. render PDFs;
9. validate every mandatory CCBOM realization ref against the emitted page manifest;
10. measure rendered-layout technical-area occupancy and page technical-object counts;
11. preflight PDFs and raster selected pages in CI.

Core1A/Core1B use intrinsic `MEDIUM` depth for this bucket. Core2 uses an explicit validation-fixture owner override because no real learner knowledge percentage is asserted by this product PR.

Source questions retain exact source IDs/locators and learner-visible provenance:
- `CHEM-C2A-SRC-U2Q15C` - NCERT Class IX Science Exemplar, Unit 2 Q15(c)
- `CHEM-C2A-SRC-U2Q35` - NCERT Class IX Science Exemplar, Unit 2 Q35

The Core2 products reuse frozen stems exactly by design. That reuse is source custody, not pedagogical duplication.
