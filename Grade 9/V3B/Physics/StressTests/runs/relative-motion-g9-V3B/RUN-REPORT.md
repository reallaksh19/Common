# V3B Physics vertical-slice run report — Motion in two dimensions (Grade 9 CBSE, Advanced)

Run id: `STRESS-PHY-RELATIVE-MOTION-G9-V3B`. Executed against `V3B-Stress-Test-Prompt-Template.md` +
`V3B-Motion-Grade9-Example.md`, per `V3B-Pending-Activity-Handover.md`'s "Exact next activity". This is
the first real production run of the template — prior work in this PR was architecture/schema/design
only (`V3B-Design-Validation.md`). Output root: this directory. Architecture basis: PR #364 branch
`draft/core-relay-architecture-review-20260913`, verified live at commit `0dc2872a` (this run's own
commit is later in the same branch).

**This report and everything under this directory is self-review by the same agent line that authored
the content.** Per this project's own contract, self-review is not independent evidence — an actual
independent reviewer (fresh instance, original-source inspection) has not run.

## 1. Owner board summary

| Item | State |
|---|---|
| Scope | Grade 9, CBSE 2026–27, Advanced track, subtopics: Vector representation and subtraction (MEDIUM), Relative velocity in a plane (HARD) |
| Curriculum binding | `OWNER_EXTENSION` / `CANDIDATE` — no exact CBSE curriculum-authority binding exists for quantitative 2D relative velocity; correctly held, not fabricated (matches the parallel #350 track's own empty `physics-curriculum-scope-bindings.v1.json`) |
| Source corpus | No frozen/official corpus. `BUILD_REVIEW_CORPUS`: 8 author-created candidate questions, `AUTHOR_CREATED` provenance throughout |
| Products requested | CORE1, CORE2, CORE1A, CORE1B, CORE2A, CORE2B |
| Products produced | **CORE1A, CORE1B, CORE2A, CORE2B — real, machine-composed, machine-verified HTML** (`publication/*.html`). **CORE1 — candidate compact notes** (`CORE1-notes.md`), instantiated from CORE1A, not independently authored. **CORE2 — HELD** (`CORE2-status.md`), no frozen corpus to preserve |
| Output paths | `publication/CORE1A.html`, `CORE1B.html`, `CORE2A.html`, `CORE2B.html`, `OWNER_BOARD.html`, `evidence.json`, `manifest.json`, `figures/*.svg` (10 files), `CORE1-notes.md`, `CORE2-status.md` (this directory) |
| Basis digest | `e27cbd273f502bb4af65dd448527fbfb14a06d7098ff2637928caa9fa8b7d546` (publish `PASS`; independently re-checked via `verify-publication`, also `PASS`) |
| Implementation gaps | See §6 |

## 2. Source / coverage / answer index

8 questions authored (`inputs/sources/source.json`, source id `AUTHOR`, `AUTHOR_CREATED`):

| ID | Subtopic | Used in | Numeric evaluator | Verified value |
|---|---|---|---|---|
| Q-VEC-A1 | Vector rep. | CORE2A (WORKED_EXAMPLE) | SPEED_FROM_COMPONENTS | 5 m/s |
| Q-VEC-A2 | Vector rep. | *authored, not placed in a product this run* | — | — |
| Q-VEC-B1 | Vector rep. | CORE2B (RECONSTRUCTION_ANCHOR) | SPEED_FROM_COMPONENTS | 10 m/s |
| Q-RELV-A1 | Relative velocity | CORE2A (WORKED_EXAMPLE) | SPEED_FROM_COMPONENTS | 10 m/s |
| Q-RELV-A2 | Relative velocity | CORE2A (PRACTICE) | SPEED_FROM_COMPONENTS | 13 m/s |
| Q-RELV-A3 | Relative velocity | CORE2A (WORKED_TO_FADED) | SPEED_FROM_COMPONENTS | 10 m/s |
| Q-RELV-B2 | Relative velocity (labelled extension) | CORE2B (NEW_TRANSFER) | SPEED_FROM_COMPONENTS | 5 m/s |
| Q-RELV-B3 | Relative velocity | CORE2B (NEW_TRANSFER) | SPEED_FROM_COMPONENTS | 13 m/s |

All 7 placed numeric answers were checked against the **existing Physics evaluator** (`validator.py`,
adapted from PR #350's validator families), not merely hand-arithmetic: `numeric_answers_compared: 7`,
`unverified_numeric_transcriptions_checked: 0`, `scientific_reviews_pending: 0` (see `evidence.json`).
Question targets were `core2a: 8, core2b: 6`; this run produced **4 and 3** respectively — a real gap
against the editable target, reported per the template's `count_policy`, not padded to hit the count.

**Reuse audit** (`evidence.json.reuse_candidates`, 7 questions, 21 pairs compared, all pairs screened):
3 pairs flagged, all correctly disclosed rather than hidden:
- `2A-VEC-Q1`×`2B-VEC-Q1` and `2A-RELV-Q1`×`2A-RELV-Q2`: `INTENTIONAL_REUSE_REVIEW_REQUIRED` (same
  declared family, different learner action — legitimate, flagged for human confirmation).
- `2A-RELV-Q3`×`2B-RELV-Q2`: **`TRANSFER_REVIEW_REQUIRED`** — the audit caught its own author (me)
  labelling `Q-RELV-B3`'s "N relative to M" question `NEW_TRANSFER` while it shares a declared family
  with the earlier `WORKED_TO_FADED` reversal question. This is a live instance of the stress table's
  "rename a worked example and call it unseen transfer → exposure/semantic review disputes the claim"
  row, produced naturally by real content rather than a synthetic corruption. Disposition: plausible as
  transfer (different numeric scenario, same underlying principle applied without being re-derived) but
  genuinely arguable — left for human review, not resolved by this report.

## 3. Microtopic/capability graph

Extended the reviewed candidate library with a new bucket and cross-file prerequisite edge (independently
re-verified, not asserted from memory):

- Added `BUCKET-VECTOR-REPRESENTATION` (MEDIUM) with 3 microtopics + 1 research-boundary microtopic, in
  `V3B-Vector-Representation-Library-Seed.json`.
- Added the prerequisite edge `BUCKET-RELATIVE-MOTION → BUCKET-VECTOR-REPRESENTATION` and
  `MIC-GEOMETRIC-CHECK → MIC-GRAPHICAL-SUBTRACTION` in the existing `V3B-Relative-Motion-Library-Seed.json`
  (reuse, not re-derivation, of the reverse-then-add construction).
- Independently checked (script, not the authoring pass): both files validate against
  `V3B-Microtopic-Library.schema.json` with 0 errors; combined library has **38 unique IDs, 0 duplicates**;
  **143 reference fields checked, 0 unresolved** (one non-ID markdown link correctly excluded); the
  combined prerequisite graph (**18 nodes**) is **acyclic**.
- The Mathematics prerequisite gap (`CAP-SIGNED-PAIR`, `CAP-RIGHT-TRIANGLE`) is **not self-certified**:
  a labelled candidate bridge (`CAP-SIGNED-PAIR-BRIDGE`, `CAP-RIGHT-TRIANGLE-BRIDGE`) was drafted,
  `acceptance_status: PROVIDER_REVIEW_REQUIRED` throughout, per the handover's explicit instruction
  ("Physics cannot self-certify external-domain readiness").

## 4. Cross-Core exposure/differentiation (worked example)

For "A relative to B" (the canonical arithmetic control, A=(6,0), B=(0,8) m/s):

| Core | What was actually produced |
|---|---|
| 1A | Full derivation (path identity → common-interval subtraction → worked numeric result), declarative |
| 1B | "Predict which displacement carries you from B to A" → diagnose the wrong-subtraction-order misconception → reconstruct |
| 2A | Traceable worked example with hints, full steps, evaluator-checked numeric answer, figure |
| 2B | Transfer: three-object boat/current composition (addition, not subtraction) requiring the learner to justify which relation applies |

## 5. Visual/render inspection (real Chromium, not NOT_RUN this time)

Prior V3B sessions reported browser/PDF inspection as `NOT_RUN` ("Playwright package has no browser
executable"). This session has a pre-installed Chromium; a real inspection was run:
- All 4 Core HTML files + `OWNER_BOARD.html` rendered in headless Chromium at 900px viewport, full-page
  screenshots taken, **zero console errors**.
- `CORE1A.html`, `CORE1B.html`, `CORE2A.html` visually reviewed at full resolution: vector figures render
  correctly (equal-axis scale, dashed component projections, arrowheads, correct quadrant/direction for
  every case including the (-5,12) and (6,-8) results), MathML equations render legibly, hints are
  collapsible, worked answers show a bold numeric result plus full reasoning and a check.
- `CORE1A.html` and `CORE2B.html` exported to PDF (A4, print CSS, print-media emulated) — files generated
  successfully (72 KB / 81 KB).
- **Not done**: pixel-level margin measurement across every page and every viewport width, and PDF
  page-by-page inspection beyond confirming successful A4 generation with the print stylesheet applied.
  `visual_review` remains reported as `NOT_RUN` in `evidence.json` because that field reflects the
  pipeline's own build-time state, not this session's separate, after-the-fact inspection — the
  distinction is preserved here rather than silently reclassified.

## 6. Stress results — architecture behaviour (executed, not tabulated)

7 corruption probes executed against isolated temporary copies of the real inputs (never against the
accepted publication); every result matched the architecture's documented invariant:

| Probe | Result | Matches stress-table row |
|---|---|---|
| Empty answer body | `BLOCKED: ANSWER_BODY_EMPTY` | "Delete an answer... closure fails" |
| Mutated frozen question stem | `BLOCKED: SOURCE_STEM_CHANGED` | "Change a frozen value... fails" |
| Numeric answer moved off the evaluator's result | `BLOCKED: PUBLISHED_ANSWER_MISMATCH` | (numeric-custody analogue of "reverse a vector...") |
| Figure atom binding outside the block's declared atoms | `BLOCKED: FIGURE_SOURCE_BINDING_MISSING` | "swap a plausible but incompatible diagram" |
| All hints removed, full answer kept | `PASS` (correctly *not* rejected) | "no fixed-three-hints rejection" |
| `practice_control` knowledge/waiver mode removed | `BLOCKED: KNOWLEDGE_OR_WAIVER_REQUIRED` | "Remove knowledge and owner waiver... held" |
| Unsupported numeric evaluator family | `PASS`, `unverified_numeric_transcriptions_checked: 1`, `scientific_reviews_pending: 1` (no numeric PASS granted) | "Use an unsupported evaluator... no numerical PASS" |
| (naturally occurring, §2) `NEW_TRANSFER` label sharing a family with a `WORKED_TO_FADED` question | Flagged `TRANSFER_REVIEW_REQUIRED` by the real reuse audit | "Rename a worked example and call it unseen transfer... disputes the claim" |

A sanity run of the **unmodified** inputs through the identical harness confirmed `PASS` first, so the
`BLOCKED` results above are attributable to each specific corruption, not to a broken harness.

**Not executed this run** (stress-table rows not attempted, honestly listed rather than omitted):
rearranging an equation with recorded provenance; reusing a source after it changes / reusing an old
packet after an extension (no second run exists yet to reuse against); widening margins or shrinking
labels severely (would require deliberately breaking the CSS — the real layout was inspected in §5 and
found sound, so this probe was not separately forced); requesting an extension outside the declared
syllabus (the boat/current extension in this run was *within* the declared included scope, not a probe
of an out-of-scope request).

**Architecture behaviour verdict**: sound on every probe attempted. **Learner-product quality verdict**:
real Core1A/1B/2A/2B content exists and was visually inspected, but see §7 — this is not independent
academic or pedagogical acceptance.

## 7. Known blockers and non-claims (carried forward, not resolved by this run)

- No independent scientific/pedagogical review has occurred. All teaching content remains author-created
  and `CHECKED_BY_AUTHOR` only.
- The Mathematics bridge capabilities remain `PROVIDER_REVIEW_REQUIRED`; Physics has not self-certified
  them (§3).
- Core2 remains `HELD` — no frozen/official question corpus exists (`CORE2-status.md`).
- Question counts (4/8 CORE2A, 3/6 CORE2B) are below the editable targets; reported, not padded.
- `academic_review` and `visual_review` fields in `evidence.json` are `NOT_RUN` by the pipeline's own
  definition; §5's Chromium inspection is additional, separate evidence, not a substitute for that field.
- This run does not establish CBSE curriculum authority for quantitative 2D relative velocity; it
  remains `OWNER_EXTENSION`/`CANDIDATE`.
- Cold-agent recovery (a genuinely different agent resuming from the packaged inputs alone) has **not**
  been executed in this session — see §8.
- No claim of "any subtopic/research depth/knowledge state" universal capability is made; this is one
  vertical slice on two subtopics.

## 8. Recovery / restart packet

`publication/inputs/` and `publication/runtime/` (written by the pipeline itself) contain the exact
plan/baseline/source inputs and a full runtime/policy snapshot, and are independently regenerable:

```bash
python3 'Grade 9/V3B/Physics/StressTests/runs/relative-motion-g9-V3B/publication/runtime/Physics/ProductionKit/run.py' publish \
  --plan   'Grade 9/V3B/Physics/StressTests/runs/relative-motion-g9-V3B/publication/inputs/plan.json' \
  --baseline 'Grade 9/V3B/Physics/StressTests/runs/relative-motion-g9-V3B/publication/inputs/baseline.json' \
  --source-root 'Grade 9/V3B/Physics/StressTests/runs/relative-motion-g9-V3B/publication/inputs/sources' \
  --out /path/to/another-new-publication
```

This was **not** separately re-run from a relocated copy in this session (process recovery only, per
`test_recovery_uses_only_copied_sources_inputs_and_runtime` in the existing test suite, which does cover
this mechanism). A genuinely independent agent has not resumed from this packet; `cold_agent_resume` is
therefore reported `NOT_RUN`, not `PASS`, for this run.

The source of truth for regenerating everything from scratch is
`build_inputs.py` in this directory (author-created, adapted from the reviewed microtopic library).

## 9. Extension

The run's configured `stress.one_extension` ("a separate research-oriented model-boundary bucket on when
simple relative-velocity subtraction needs frame qualifications") was implemented as
`MIC-FRAME-QUALIFICATION-BOUNDARY` in the microtopic library (§3) — a conceptual note naming rotating
frames and relativistic speeds as the two regimes where `v_A/B = v_A - v_B` needs qualification, without
teaching either regime's mathematics, and explicitly excluded from Grade 9 assessment claims. It was
**not** built into a full six-product Core1A/1B/2A/2B treatment this run — only a documented microtopic
plus a boundary statement — since the template only asks that the extension show "new prerequisites,
affected consumers and retained artifacts," not a second full production pass. Affected/retained: no
existing Core1A/1B/2A/2B content depends on it (it prerequisites *from* `MIC-GEOMETRIC-CHECK`, nothing
depends on it), so nothing already produced is invalidated by its addition.

Separately, the *included*-scope boat/current composition (§4, `Q-RELV-B2`) was fully realized as a
CORE2B product, per `V3B-Motion-Grade9-Example.md`'s explicit inclusion of "one boat/current model as a
labelled extension with conditions."
