# Physics V2 — Core (1A) Difficulty-Aware Learner Publication

Core (1A) is the learner-teaching assimilation layer between semantic **Core (1)** and the learner-facing Core study-guide PDF.

Core (1) answers **what must be taught**: source concepts, physical models, equations, examples, and capability boundaries.

Core (1A) answers **how a Grade-9 learner can actually acquire and use that knowledge** at the required subtopic level. It decomposes the chapter into stable **Subtopic Bucket Assimilation (SBA)** units, classifies intrinsic difficulty, models learner readiness (currently 20% and 50% usable prior knowledge), builds the necessary learning atoms, and verifies that every linked Core (2) hint reveal has already been taught before transfer.

Core (1A) remains the existing `CORE_STUDY_GUIDE` product. It is not a third learner product.

```text
P-G CoreAuthoring
PhysicsCore1StudyPlan
        │
        ├──────────────┐
        ▼              ▼
source inventory    Core (2) linkage
        │              │
        └──────┬───────┘
               ▼
P-GA Core1A
Subtopic Bucket Assimilation (SBA)
difficulty × prior knowledge × learning atoms
               │
               ▼
PhysicsCore1APublicationPlan
               │
               ▼
Core1A renderer
               │
               ▼
physics-core-study-guide.pdf
```

## Core (1) versus Core (1A)

Core (1) is the semantic/pedagogical authority for the physics content.

Core (1A) is not a prettier copy of Core (1), and it is not a reverse-engineered answer key for Core (2). It may expand a Core (1) concept into the prerequisite rebuilding, staged visuals, model conditions, misconception resolution, worked examples, guided examples, retrieval checks, and transfer bridges needed by a low-readiness learner. It may also build an explicit explanatory bridge for a source-visible practice/formula topic when the supplied theory is incomplete, provided the bridge does not invent new physics or silently claim that the missing theory existed in the source.

The governing question is:

> Given this specific subtopic bucket, its intrinsic difficulty, the learner's usable prior knowledge, and the Core (2) demands, what teaching sequence is required so the learner can understand and use it?

## Subtopic Bucket Assimilation (SBA)

Each chapter has stable bucket IDs such as:

```text
M2D-SBA-03
M2D-SBA-04
...
```

PDF page numbers are not semantic identifiers and may change during layout revision.

Each SBA bucket records:

- source/Core (1) basis;
- intrinsic difficulty (`D1`–`D4`);
- prerequisite buckets;
- primary Revised Core (2) v2 questions;
- 20% and/or 50% prior-knowledge pathways;
- learning atoms;
- required visual stages;
- misconception targets;
- worked/guided/retrieval evidence;
- Core (2) H1/H2/H3 pre-teaching coverage;
- question-specific release prerequisites.

Every Revised Core (2) v2 question belongs to exactly one **primary** SBA bucket. Secondary prerequisite buckets may also be required.

For the current SBA production queue, buckets with **zero primary Core (2) questions are retained in the chapter map but do not receive a dedicated SBA PDF**. Their status is `SKIP_NO_PRIMARY_CORE2`.

## Difficulty × prior knowledge

Difficulty and readiness are separate variables.

Core (1A) currently optimises especially for **medium/hard concepts with 50% or less usable prior knowledge**.

```text
                      learner readiness
                    ~20%              ~50%

D1 FOUNDATION       rebuild basics     activate basics
D2 THINK CAREFULLY  high support       moderate support
D3 CHALLENGE        maximum support    high support
D4 STRETCH/BRIDGE   full bridge        focused bridge
```

A 20%-knowledge D3 bucket normally needs:

```text
FOUNDATION / PRETRAINING
→ STORY / PHENOMENON
→ STAGED PICTURE
→ WHAT CHANGED PHYSICALLY?
→ PICTURE-TO-MATHS BRIDGE
→ MISCONCEPTION RESOLUTION
→ WATCH ONE
→ COMPLETE ONE
→ TRY ONE WITH HINTS
→ RETRIEVAL GATE
→ CORE (2)
```

The badge is not decorative. Difficulty and readiness determine the minimum teaching support.

## Core (2) hint pre-teaching rule

Core (2) uses protected hints:

```text
H1 — key physics
H2 — representation/model
H3 — first mathematical move
```

Core (1A) must pre-teach each reveal.

```text
Core (2) Qxx
│
├── H1 ──> earlier Core (1A) learning atom + check
├── H2 ──> earlier Core (1A) learning atom + representation
└── H3 ──> earlier Core (1A) worked/guided first move
```

A topic-level link is insufficient. If a hint rung has no earlier teaching home, the SBA build is incomplete.

A question may have a primary bucket but still be held until another prerequisite bucket is complete. Example: an apex-speed question may be primary in the velocity-event bucket but require the same-height range formula before the full Core (2) item is released.

## Authority boundary

Core (1A) may:

- reorganise Core (1) content into stable SBA teaching units;
- decompose concepts into smaller learner-facing learning atoms;
- add prerequisite refreshers and explanatory bridges using already-authorised physics;
- increase or reduce scaffolding according to difficulty and prior knowledge;
- construct staged schematic visuals from source-authorised concepts without inventing numerical data;
- create worked or guided examples only when the quantities/physics are authorised by the upstream/source contract;
- explicitly teach a source-visible practice/formula bridge while marking the theory-source limitation honestly;
- map Core (2) hints back to exact teaching atoms and delay question release until prerequisites are met;
- report publication-quality and teaching-completeness findings.

Core (1A) may **not**:

- invent a new physical law, model, capability, or unsupported problem family;
- invent source attribution or claim missing source theory exists;
- silently correct a source mathematical inconsistency without a source-QC note;
- fabricate a Core (2) linkage where Revised Core (2) v2 has no matching primary question;
- create a third learner product.

## Learning-page grammar

A mature 20%-knowledge bucket uses textbook teaching rather than a card dump:

```text
BUCKET OPENER / FOUNDATION GATE
→ MODEL CONTRACT / PHYSICS WORDS
→ STAGED ILLUSTRATION
→ WHAT TO NOTICE
→ TURN THE PICTURE INTO MATHS
→ WHY THIS STEP?
→ EASY MISTAKE TO MAKE
→ WATCH ONE
→ COMPLETE ONE
→ TRY ONE WITH HELP
→ INDEPENDENT RETRIEVAL
→ WHERE YOU WILL USE THIS
```

The staged illustration supports the teaching; it does not replace explanatory prose or reasoning.

## Illustration requirements

Illustrations are first-class instructional objects.

- use a stable coordinate frame unless the concept requires a frame change;
- one conceptual change per stage;
- labels anchor to semantic objects, not arbitrary page coordinates;
- keep related words and graphics spatially adjacent;
- D2/D3 concepts require staged visuals rather than one static diagram;
- unresolved label collision or panel overflow is a build failure;
- the renderer treats a completed figure as an atomic bounded object.

A hard concept means **more pictures and fewer inferential jumps**, not smaller text.

## Learner-facing language

Do not expose internal production jargon such as `repair`, `custody`, `falsifier`, `remediation`, or `source-grounded`.

Preferred learner language includes:

- `Where you will use this`
- `Try Core (2)`
- `Need a quick refresher?`
- `Go back to this idea`
- `Easy mistake to make`
- `Does the answer make sense?`
- `Ready to practise?`

Difficulty labels:

- `D1 FOUNDATION`
- `D2 THINK CAREFULLY`
- `D3 CHALLENGE`
- `D4 STRETCH`

## Publication quality

Core (1A) keeps the existing publication QA:

- textbook body target 10.6 pt, hard floor 10.0 pt;
- caption and diagram-label floors;
- A4 page with stable margins;
- no heading/badge collision;
- no text outside page bounds;
- properly rendered Greek symbols, subscripts, superscripts, fractions and radicals;
- no raw learner-facing strings such as `sqrt(...)`, `theta`, `v_A/B`, or `u^2`;
- no orphan headings or accidental half-page voids;
- no worked example split before its result/check;
- figures require captions/provenance mode;
- final PDF remains hash-bound to its authorised inputs.

## Normative files

```text
Core1A/
├── README.md
├── CORE1A_UI_SPEC.md
├── contracts/
│   ├── physics-core1a-publication-plan.schema.json
│   └── physics-core1a-subtopic-bucket.schema.json
├── registry/
│   ├── physics-core1a-publication-policy.json
│   ├── physics-core1a-core2-linkage.json
│   └── physics-core1a-motion-in-a-plane-sba-v1.json
└── tests/
    ├── test_physics_core1a.py
    ├── test_physics_core1a_linkage.py
    └── test_physics_core1a_sba.py
```

## Release claim

Core (1A) can prove publication engineering and SBA teaching-completeness properties. It does not independently redefine subject correctness; source/Core (1) remains the semantic authority, while Core (2) remains the protected transfer surface.
