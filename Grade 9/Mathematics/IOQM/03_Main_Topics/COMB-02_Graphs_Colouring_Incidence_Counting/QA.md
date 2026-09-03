# COMB-02 — Production QA

Status: `BENCHMARK_STATIC_ARTIFACT_PASS_ONE_SOURCE_PAGE_VISUAL_GATE_PENDING`

| Gate | State | Evidence |
|---|---|---|
| issue #85 scope | PASS | graph modelling, degree/handshaking, colouring constraints, incidence double counting, grid/knight graphs and Ramsey-style inevitability retained |
| production-head compatibility | PASS | branch remains topic-only from `grade9-ioqm-90q-corpus-v1@4b30638f984076d41998dcd2c68f4b3830a7d59c` before merge |
| COMB-01 provider | PASS_ACCEPTED | exact `COMB01_Stable_Counting_Model_Interface_v1.md` consumed |
| provider boundary | PASS | generic P&C, complement and inclusion-exclusion are retrieved rather than duplicated |
| source anchors | PASS_6 | `IOQM-2025-Q08,Q29`; `IOQM-2024-Q09,Q19`; `IOQM-2023-Q16,Q22` |
| exact source stems | PASS_6 | all six controlled stems checked against organizer/controlled paper sources |
| historical answers | PASS_6 | `48,19,48,12,94,77` independently re-derived |
| source/figure custody | PASS_5_PLUS_1_FAIL_CLOSED | Q08 page visual closed and text-only; Q16 page visual closed and text-only; Q22 exact stem/key/math closed but organizer page-image confirmation remains pending |
| Q22 learner promotion | PASS_FAIL_CLOSED | `IOQM-2023-Q22` remains source-map/teacher controlled and is not promoted verbatim into the student bank |
| microstream interfaces | PASS_7 | modelling; degree/handshaking; colouring; incidence; grid/knight; Ramsey; source audit |
| topic-lead integration | PASS | `Authoring/Lead_Integration_Map.md` |
| integrated Assimilation Book | PASS | modelling precedes terminology; graph/degree/colour/incidence/Ramsey journey is integrated |
| First-Step Reference | PASS | compact modelling/degree/colour/incidence/Ramsey router |
| Recognition/First-Line Lab | PASS_16 | recognition and first mathematical line only |
| practice ladder | PASS_22 | F0→F4 support fading with source-safe historical transfer |
| first mastery attempt | PASS | `06_H0_Mastery_Test.md` is unlabelled/unhinted |
| mastery items | PASS_12 | degree parity, colouring, knight graph, incidence, Ramsey and game-state boundaries |
| benchmark assimilation lab | PASS | RECONNECT, error diagnosis, ADOPT first moves, changed-surface transfer and six-question assimilation |
| benchmark lab teacher key | PASS | deterministic answers/routes independently recomputed |
| Quadratics-v2 pedagogy comparison | PASS_ARCHITECTURE | `Authoring/Quadratics_v2_Benchmark_Comparison.md` |
| teacher key synchronization | PASS | core Teacher Diagnostic Key plus benchmark-lab key |
| required contrasts | PASS | unrestricted vs proper colouring; direct edge count vs degree sum; ordered vs unordered; linear vs cyclic; static graph vs game state |
| metadata schema | PASS_85 | canonical 31-column `Item_Metadata.csv`, 85 promoted/control rows |
| answer verification flag | PASS | every metadata row has `answer_verified_independently=true` |
| canonical renderer | PASS | `Authoring/render_comb02_pdfs.py`; canonical GitHub Actions execution passed |
| student PDF preflight | PASS_14 | 14 A4 pages, text-based/openable, unencrypted |
| student PDF visual inspection | PASS_14 | exact repository binary inspected at 200 dpi; no clipping, overlap, broken glyphs or accidental blank pages |
| teacher PDF custody | PASS_6 | 6 A4 pages, preflighted and visually inspected |
| repository PDF custody | PASS | custody commit `adee63ac889e9ba02377ab965f6292f26fbcd21c`; hashes/blob IDs in `PDF_Custody.md` |
| exact-binary render regression | PASS_ZERO_DIFF | repository custody pages are pixel-identical at 200 dpi to the approved final audit candidate: student 0/14 changed; teacher 0/6 changed |
| learner control-plane scrub | PASS_STATIC_RENDERED | no learner-facing issue/PR/branch/wave/agent/H/F/metadata/interface workflow labels |
| Quadratics-v2 final static equivalence | QUALIFIED_PASS | pedagogy/math/metadata/rendered-artifact class matches benchmark; one non-promoted historical source page visual gate remains explicitly open |
| classroom timing/readability | NOT_RUN | evidence-dependent classroom gate |
| longitudinal retention | NOT_RUN | evidence-dependent |
| psychometric calibration | NOT_RUN | evidence-dependent |
| qualification/pass-mark calibration | NOT_RUN | unsupported by static authoring |
| publication approval | NOT_RUN | separate human decision |

## Benchmark judgment

COMB-02 matches the Grade 9 Quadratics v2 benchmark on the learner-facing static artifact class: partial-knowledge diagnosis, missing-link repair, contrast/decision boundaries, attempt-before-hint, fading, first-move independence, changed-surface transfer, error diagnosis, six-question assimilation, independent mathematics, canonical metadata, canonical rendering, structural preflight, learner scrub, exact-binary repository custody and page-by-page visual inspection are all closed.

The stronger unqualified `BENCHMARK_READY_NOT_CLASSROOM_CALIBRATED` label is withheld because `IOQM-2023-Q22` still lacks exact organizer page-image confirmation. That item remains fail-closed outside the promoted student historical bank, so this debt does not contaminate the rendered student package.

## Static disposition

`BENCHMARK_STATIC_ARTIFACT_PASS_ONE_SOURCE_PAGE_VISUAL_GATE_PENDING`

The user explicitly authorized merging this qualified state on 2026-09-03. This merge authorization does not convert the Q22 source-page gate, classroom timing/readability, retention, psychometric calibration, qualification/pass-mark calibration or publication approval into PASS states.
