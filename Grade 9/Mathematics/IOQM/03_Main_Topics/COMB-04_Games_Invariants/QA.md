# COMB-04 QA

Overall static state: `WAVE5_PREAUDIT_COMPLETE__FORMAL_INDEPENDENT_GATE_BLOCKED`

Target completion state remains: `BENCHMARK_READY_NOT_CLASSROOM_CALIBRATED`.

## Current gate ledger

| Gate | Status | Evidence / blocker |
|---|---|---|
| G0 source authority | PASS_STATIC | `01_Source_Coverage_Map.md`; production corpus and verification ledgers re-read in Wave 5 pre-audit |
| G1 dependency | PASS_STATIC | `00_Concept_and_Dependency_Map.md`; NT-01/NT-02/COMB-03 acceptance contracts |
| G2 single governing model | PASS_STATIC | `STATE -> MOVE EFFECT -> INVARIANT / MONOVARIANT / W-L CLASS -> PROOF -> STRATEGY OR OBSTRUCTION` |
| G3 ownership/overlap | PASS_STATIC | `Authoring/Overlap_and_Ownership_Ledger.md`; no conflict found in second pass |
| G4 research interfaces | PASS_STATIC | seven A-P interfaces `READY_FOR_LEAD`; Wave-1 audit |
| G5 lead integration | PASS_STATIC | one integrated `02_Assimilation_Book.md`; Wave-2 audit |
| G6 deduplication | PASS_SECOND_PASS | full teaching remains in `02`; `03` is compression/retrieval; `04-06` are assessment |
| G7 cross-boundary contrasts | PASS_STATIC | invariant/monovariant, reachability/forceability, W/L quantifiers, construction/obstruction, deterministic/adversarial contrasts present |
| G8 attempt-before-help/fading | PASS_STATIC | H3->H0 design in interfaces; mastery first attempt unhinted |
| G9 integrated First-Step | PASS_STATIC | one topic-wide `03_First_Step_Reference.md` after Wave 2 |
| G10 H0 mastery | PASS_STATIC | mixed `06_H0_Mastery_Test.md`, no default method labels/hints |
| G11 independent mathematics | **BLOCKED_FRESH_REVIEWER_REQUIRED** | current custodian authored/materialized Waves 0-4; second-pass checks found no defect but cannot truthfully assert fresh-reviewer independence |
| G12 source custody | PASS_SECOND_PASS | Q22=66, Q25=36, 2023-Q28=67 match live source + independent verification ledgers; Q28 figure remains source-controlled |
| G13 student-export hygiene | PASS_SECOND_PASS | no Issue/PR/Wave/agent/interface/QA-state leakage in learner files; concise stable source IDs allowed in provenance map |
| G14 one render authority | NOT_RUN | Wave 6 only after G11 pass |
| G15 render/preflight | NOT_RUN | no PDFs rendered yet |
| G16 transfer quality | PASS_STATIC | representation/context/strategy/WHY-NOT transfer present |
| G17 six-question ownership | PASS_STATIC | notice/why/clue/contrast/first-line/changed-surface support present across integrated book/reference/practice |
| G18 human evidence | NOT_RUN | no classroom, retention, psychometric, qualification-probability or percentile evidence |

## Wave records

- Wave 0: `PASS__WAVE0_ARCHITECTURE_FROZEN`.
- Wave 1: `PASS_STATIC` — seven complete A-P interfaces.
- Wave 2: `PASS_STATIC_WAVE2` — integrated Assimilation Book.
- Wave 3: `PASS_STATIC_WAVE3` — integrated First-Step Reference + learner scrub.
- Wave 4: `PASS_STATIC_WAVE4` — recognition/first-line, transfer, mastery, teacher key and 31-column metadata.
- Wave 5 second-pass pre-audit: `NO_DEFECT_FOUND`; formal independent gate remains blocked by reviewer separation.
- Wave 6: `NOT_RUN`.

## Mathematics/source audit summary

Second-pass recomputation checked all authored answer classes and proof obligations represented in `R01..R06`, `L01..L06`, `P01..P12`, `M01..M10`.

Verified examples include:

- removal `{1,2}` -> losing `0 mod 3`;
- removal `{1,3,4}` -> losing `{0,2} mod 7`;
- removal `{2,5}` -> losing `{0,1,4} mod 7`;
- six-cycle triple toggles -> period-3 invariant vectors `101101`, `011011`;
- triple move permutation `(2,-1,-1)` -> pairwise mod-3 coordinate differences invariant;
- `1..8` pairing product `65^2`;
- `1..10` pairing product `270^2`;
- Euclidean-subtraction and adjacent-inversion processes -> strict nonnegative integer monovariants.

No defect was found in the second-pass computations. See `Authoring/Wave5_Fresh_Review_PreAudit.md` for the complete verification index.

## Metadata truth

`Item_Metadata.csv` uses the frozen 31-column schema and has 37 data rows: 34 authored + 3 historical anchors.

Authored rows remain `answer_verified_independently=false` until G11 is satisfied by a fresh reviewer. This is intentional validation truth, not missing bookkeeping.

Historical rows retain independent Batch-C verification only:

- `IOQM-2025-Q22 = 66`;
- `IOQM-2025-Q25 = 36`;
- `IOQM-2023-Q28 = 67`.

## PDF / render status

`PDF_PRODUCTION: BLOCKED_UNTIL_G11_PASS`

Not run:

- unified render authority;
- student PDF;
- teacher PDF;
- complete learner pack PDF;
- page rendering to images;
- every-page visual inspection;
- structural PDF preflight;
- student/teacher leakage render scrub;
- page counts;
- SHA-256 hashes;
- PDF Git blob receipts.

These are Wave-6 obligations and must not be represented as complete before the formal independent audit gate passes.

## Human-evidence truth

The following remain `NOT_RUN`:

- classroom timing/readability;
- longitudinal retention;
- psychometric calibration;
- qualification probability;
- pass-mark/percentile calibration;
- publication approval.

## Exact next action

Obtain a fresh reviewer, independent of the Wave-0-to-Wave-4 authoring/materialization pass, to recompute all promoted authored answers/proofs and source-condition claims. If that reviewer records `WAVE5_INDEPENDENT_QA_PASS`, immediately proceed to Wave 6 unified PDF/render production and page-by-page QA.