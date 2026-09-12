# Physics V2 — Core (1A) Difficulty-Aware Learner Assimilation

> **Future agents: start with `AGENT_RUNBOOK.md`, not this README.**

Core (1A) is the learner-teaching assimilation layer between semantic **Core (1)** and learner transfer in **Core (2)**. It remains the existing `CORE_STUDY_GUIDE` learner product; it is not a third product.

Core (1) answers **what must be taught**: source concepts, physical models, equations, examples and capability boundaries.

Core (1A) answers **how a Grade-9 learner at a declared readiness level can acquire, recognise and use that knowledge inside a stable Subtopic Bucket Assimilation (SBA) unit**.

The governing question is:

> Given this bucket, its intrinsic difficulty, the learner's usable prior knowledge, and the exact Core (2) demands, what teaching and transfer sequence is required before independent practice is reasonable?

## Architecture

```text
SOURCE / CORE (1)
what physics is authorised
        ↓
SBA INDEX
what belongs together and which Core (2) questions it owns
        ↓
DIFFICULTY × READINESS
how much support the learner needs
        ↓
LEARNING ATOMS
small conceptual steps + staged visuals + misconceptions
        ↓
CORE (2) HINT PRETEACH AUDIT
H1 / H2 / H3 must already be taught
        ↓
PROBLEM-FAMILY ASSIMILATION
recognise → numbered method → independent practice → optional hints
        ↓
READINESS GATE
recognise → represent → first move → finish
        ↓
CORE (2)
protected transfer
```

## Stable SBA indexing

Use semantic IDs such as `M2D-SBA-03`, never PDF page numbers as concept identifiers.

Every Revised Core (2) v2 question has exactly one **primary** SBA owner. A question may still be **HELD** until a prerequisite bucket is complete.

For the current production queue:

- buckets with primary Core (2) questions are `ACTIVE` and receive dedicated SBA PDFs;
- buckets with zero primary questions remain in the chapter map as `SKIP_NO_PRIMARY_CORE2` and are not built as dedicated PDFs.

## Difficulty and learner readiness

Difficulty and prior knowledge are independent.

```text
                      learner readiness
                    ~20%              ~50%

D1 FOUNDATION       rebuild basics     activate basics
D2 THINK CAREFULLY  high support       moderate support
D3 CHALLENGE        maximum support    high support
D4 STRETCH          full bridge        focused bridge
```

Core (1A) currently prioritises medium/hard buckets for learners at or below 50% usable prior knowledge.

A 20%-knowledge bucket should normally move from intuitive/pictorial understanding to independent transfer rather than from formula summary directly to Core (2).

## Mandatory learner sequence

The exact process is machine-tracked by per-bucket build manifests. The default macro-order is:

`SBA INDEX → FOUNDATION/PRETRAINING → CONCEPT BUILD → PICTORIAL STAGES → PICTURE-TO-MATHS → MISCONCEPTION → WATCH ONE → COMPLETE ONE → PROBLEM-FAMILY ROUTINE(S) → INDEPENDENT PRACTICE → HINTS → READINESS → CORE (2) TRANSFER SUMMARY`

### Independent practice

Independent practice is mandatory for every released problem family. The learner must attempt before seeing H2/H3-style support.

### Readiness

Each released family checks four abilities:

1. **RECOGNISE** the problem family;
2. **REPRESENT** the model;
3. choose the **FIRST MOVE** without H2/H3;
4. **FINISH** a fresh analogous problem and check it.

Recommended release: 4/4 without H2/H3.

## Core (2) hint pre-teaching

Core (2) uses:

- H1 — key physics;
- H2 — representation/model;
- H3 — first mathematical move.

Every reveal must trace backward to prior Core (1A) teaching evidence. A topic-level link alone is insufficient.

## Question-load scaling

Core (1A) elaboration must grow with the number of distinct Core (2) demands, not just with intrinsic concept difficulty.

- 1–2 primary questions: `LOW` load;
- 3–5: `MEDIUM`;
- 6–9: `HIGH`;
- 10+: `VERY_HIGH`.

For HIGH/VERY_HIGH loads, cluster questions into problem families and expand the transfer section. Do not compress many questions into one end-page list.

Reference cases:

- SBA-03 — LOW load;
- SBA-04 — HIGH load;
- SBA-05 — VERY_HIGH load.

## Source and authority boundary

Core (1A) may reorganise and scaffold authorised physics, add prerequisite refreshers, staged visuals, worked/guided/independent practice and explanatory bridges.

Core (1A) may not invent a new law, unsupported problem family, fake source citation, fabricated Core (2) link, or silently correct a source issue. Source/Core (1) remains semantic authority.

## Learner UI

See `CORE1A_UI_SPEC.md` for the normative learner-facing layout grammar. Important rules include:

- hard concept = more pictures and fewer jumps;
- pictures support teaching, not replace it;
- real Greek/subscript/superscript/fraction/radical typography;
- no raw learner strings like `sqrt(...)` or `theta`;
- independent practice before hints;
- readiness before release;
- exact `Qxx` links and explicit HELD prerequisites.

## Durable handoff state

A future agent must not infer progress from chat history.

Read:

- `registry/physics-core1a-motion-in-a-plane-build-state-v1.json` for current queue state;
- `registry/build-manifests/M2D-SBA-xx-v1.json` for completed-bucket evidence;
- run `python Grade 9/V2/Physics/Core1A/engine/next_sba.py` to derive the next active bucket.

If the derived next bucket disagrees with build-state, the build fails.

## Normative files

```text
Core1A/
├── AGENT_RUNBOOK.md                         # exact execution order
├── README.md                                # architecture summary
├── CORE1A_UI_SPEC.md                        # learner surface contract
├── SOURCE_COMPLETENESS_SPEC.md
├── contracts/
│   ├── physics-core1a-publication-plan.schema.json
│   ├── physics-core1a-subtopic-bucket.schema.json
│   ├── physics-core1a-sba-publication-index.schema.json
│   └── physics-core1a-sba-build-manifest.schema.json
├── registry/
│   ├── physics-core1a-learner-language.json
│   ├── physics-core1a-publication-policy.json
│   ├── physics-core1a-motion-in-a-plane-sba-v1.json
│   ├── physics-core1a-motion-in-a-plane-sba-publication-index-v1.json
│   ├── physics-core1a-motion-in-a-plane-build-state-v1.json
│   ├── physics-core1a-core2-linkage.json
│   ├── ...bucket profile / transfer files...
│   └── build-manifests/
│       ├── M2D-SBA-03-v1.json
│       ├── M2D-SBA-04-v1.json
│       └── M2D-SBA-05-v1.json
├── engine/
│   ├── build_physics_core1a.py
│   ├── next_sba.py
│   ├── physics_learner_copy.py
│   └── render_physics_core1a.py
└── tests/
    ├── test_physics_core1a_sba.py
    └── test_physics_core1a_agent_handoff.py
```

## Wired into P-K

Since P-UPGRADE-2 the P-K cold-start runner publishes the Core study guide **through**
Core (1A): it compiles the P-G plan into a `PhysicsCore1APublicationPlan` and renders that,
instead of calling the old direct product renderer. The artifact name
(`physics-core-study-guide.pdf`), the product id (`CORE_STUDY_GUIDE`), the required
sections and the two-product topology are unchanged.

Because it is now the published product, Core (1A) carries the same custody obligations the
P-K renderer carried:

- every figure is drawn through the P-H `render_primitive` interface, and its **draw-time**
  vector-operation count and ink box are recorded in a `PhysicalPageMap` returned as
  `report["physical_page_map"]` — planned page numbers are never evidence;
- every representation the P-H bundle declares for a capability is physically placed. The
  designed spread takes the first figure of each phase; the rest are placed on balanced,
  adaptively sized "different pictures of the same idea" pages rather than being silently
  dropped;
- `audit_product` (P-K) and the P-L custody gate run against that page map unchanged.

## Learner-facing wording

`registry/physics-core1a-learner-language.json` is the single governed learner vocabulary,
and `engine/physics_learner_copy.py` is the only place that applies it. Both Core (1A) and
the Core (2) transfer book import it, so the two products cannot drift into different
dialects.

The registry already governed the fourteen publication module kinds and a banned-word list.
It now also reaches the roles that table did not: route states (`FRAME`, `REPRESENT`,
`MODEL`, `EXECUTE`, `INTERPRET`, `VERIFY`), hint levels (`H1_NOTICE`, `H2_MODEL`,
`H3_START`), Core (2) solution sections, support stages and readiness roles, plus the
figure headings each teaching primitive is drawn with. Where the registry already defined a
label, that label is kept: this extends the incumbent vocabulary rather than restyling it.

Internal identifiers are **unchanged**. `MISCONCEPTION_REPAIR`, `WORKED`, `GUIDED`,
`EXECUTE`, `H1_NOTICE` and the rest stay exactly as they are in schema fields, JSON enum
values, falsifier names and test assertions. What the registry governs is what a
14-year-old reads.

Three parts, one falsifier:

- `module_labels` / `module_helpers` supply headings and their one-line helpers;
- `phrase_rewrites` supplies body copy, so open-ended upstream wording such as
  `VERIFY_MODEL_VALIDITY` lands in learner words instead of curriculum-design words;
- `learner_copy_violations()` re-scans everything that actually reached the page and raises
  `INTERNAL_ROLE_LABEL_ON_LEARNER_SURFACE` if any internal identifier or banned/clinical
  label survived. The rewrite table is a translation, not a repair: a missing entry is
  reported, not hidden.

The ban list is curriculum-design jargon — "misconception repair", "readiness gate", "model
validity", "custody", "falsifier", "source-grounded" — not ordinary school vocabulary.
"Worked example" and "guided practice" are words a student meets in any textbook and are
deliberately allowed, because the governed labels themselves use them.

## Standalone use

```bash
python "Grade 9/V2/Physics/Core1A/engine/build_physics_core1a.py" \
  --core1 /path/to/physics-core1-study-plan.json \
  --out-dir /tmp/core1a
```

The command writes `physics-core1a-publication-plan.json`, `physics-core-study-guide.pdf`
and `physics-core1a-quality-report.json`. An optional representation bundle can be supplied
with `--representations`.

## Release claim

We cannot guarantee that a future agent will never make a judgement error. The architecture instead makes the important deviations **explicit, machine-checkable and build-failing** so continuity does not depend on hidden memory or chat history.
