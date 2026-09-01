# ALG-03 - QA

Status: `BENCHMARK_READY_NOT_CLASSROOM_CALIBRATED`

| Gate | State |
|---|---|
| G0 source authority | PASS - 4 stable historical anchors with validated paper/key URLs |
| G1 dependency / prerequisite interface | PASS - consumes frozen ALG-01 interface; no prerequisite inversion |
| G2 governing model | PASS - THE REQUESTED INFORMATION CHOOSES THE REPRESENTATION |
| G3 canonical overlap ownership | PASS - Vieta/discriminant/remainder/reduction canon owned here; optimization routed to ALG-02 |
| G4 research interfaces | PASS |
| G5 single integrated student book | PASS |
| G6 deduplicated teaching | PASS |
| G7 mandatory decision boundaries | PASS - roots/invariants, discriminant/minimum, root-shift/input-shift, high-power/reduction, remainder/factor and common-root elimination |
| G8 attempt-before-help / H3->H0 | PASS_STATIC |
| G9 one First-Step layer | PASS |
| G10 mixed unlabelled H0 mastery | PASS |
| G11 independent mathematics | PASS - `Authoring/Independent_Mathematics_Audit.md` |
| G12 source custody | PASS - verified anchor answers 22, 53, 50, 18 |
| G13 student-export hygiene | PASS |
| G14 one render authority | PASS - reproducible ReportLab A4 renderer at `Authoring/render_alg03_pdfs.py`, 18 mm side margins |
| G15 page-by-page render QA | PASS - 13/13 pages inspected after repository materialization |
| G16 T2-T4 transfer | PASS_STATIC |
| G17 six-question ownership | PASS_STATIC |
| classroom timing/readability | NOT_RUN |
| longitudinal retention/transfer | NOT_RUN |
| psychometric calibration | NOT_RUN |
| qualification probability | NOT_RUN |

## Mathematical closure

Vieta is derived from factor expansion only here. Discriminant root behavior, transformed-root sign discipline, remainder/factor theorem, polynomial reduction and common-root elimination have been independently checked. The canonical remainder of `x^20` modulo `x^2+x+1` is normalized to `-x-1`.

`Authoring/ALG03_Stable_Prerequisite_Interface_v1.md` is frozen for downstream consumption.

## Render evidence

Repository binary custody: `PASS`. Both artifacts are generated from the canonical Markdown by the committed render authority, are present under `PDFs/`, and were structurally and visually rechecked after materialization. The earlier unattached local hashes are superseded because those bytes were never in repository custody and could not be independently recovered.

Student PDF:
- repository path: `PDFs/ALG03_Student_Pack_v1.pdf`
- pages: 10
- page size: A4
- SHA-256: `34a0ff155c3c3132aecd858145d70c3a2d72eb756bc99912b67892f1602c0713`
- structural preflight: PASS - openable, unencrypted, non-scanned, no XFA
- visual QA: PASS - 10/10 pages, no clipping/overlap/broken-glyph or teacher-answer leakage observed

Teacher PDF:
- repository path: `PDFs/ALG03_Teacher_Key_v1.pdf`
- pages: 3
- page size: A4
- SHA-256: `784a283037ef0c96ec12a6c9674693706bd2ee26fb64939482112537b87fbe52`
- structural preflight: PASS
- visual QA: PASS - 3/3 pages, no clipping or overlap observed

## Promotion state

`BENCHMARK_READY_NOT_CLASSROOM_CALIBRATED`
