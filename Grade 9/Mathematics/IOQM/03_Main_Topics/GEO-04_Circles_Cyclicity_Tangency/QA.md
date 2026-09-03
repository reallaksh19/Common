# GEO-04 — Production QA

Status: `BENCHMARK_READY_NOT_CLASSROOM_CALIBRATED`

| Gate | State | Evidence |
|---|---|---|
| issue #84 scope | PASS | centre/inscribed angles, cyclicity, tangency, alternate segment, power, chords/secants and representation choice retained |
| GEO-02 provider | PASS_ACCEPTED | exact frozen `GEO02_Stable_Angle_Polygon_Interface_v1.md` consumed |
| provider boundary | PASS | generic angle/quadrilateral canon retrieved; circle canon taught here |
| source anchors | PASS_5 | `IOQM-2025-Q19,Q23,Q30`; `IOQM-2024-Q17`; `IOQM-2023-Q15` |
| historical answers | PASS_5 | `29,03,10,25,03` independently re-derived |
| exact source/page visual custody | PASS_5 | official/controlled printed pages inspected for all five anchors |
| historical printed figure dependency | PASS_NONE | all five exact historical problem statements are text-only |
| Q23 canonical interpretation | PASS_REQUIRED | non-degenerate reading preserved; rejected degenerate branch is not promoted |
| microstream interfaces | PASS_7 | circle angles; cyclicity; tangency; alternate segment; power; chords/secants; source audit |
| topic-lead integration | PASS | `Authoring/Lead_Integration_Map.md` |
| integrated Assimilation Book | PASS | structure/legal-hypothesis first, then theorem selection and representation choice |
| First-Step Reference | PASS | same-chord/cyclicity/tangent/power/common-chord/coordinate router |
| Recognition/First-Line Lab | PASS_16 | first-move recognition and theorem-legality checks |
| practice ladder | PASS_22 | direct recognition through mixed historical-style transfer |
| first mastery attempt | PASS | `06_H0_Mastery_Test.md` is unlabelled and unhinted |
| mastery items | PASS_12 | circle angles, cyclicity, tangent/power, common chord, route choice and WHY-NOT trap |
| benchmark assimilation lab | PASS | RECONNECT, error lab, ADOPT, changed-surface transfer and six-question assimilation test |
| teacher key synchronization | PASS | core Teacher Diagnostic Key and benchmark-lab key independently checked |
| Quadratics-v2 pedagogy comparison | PASS_ARCHITECTURE | `Authoring/Quadratics_v2_Benchmark_Comparison.md` |
| metadata schema | PASS_84_ROWS_31_COLUMNS | deterministic generator; 84 controlled rows on the canonical 31-column schema |
| answer verification flag | PASS_84 | every metadata row records `answer_verified_independently=true` |
| canonical renderer | PASS_COMMITTED | `Authoring/render_geo04_pdfs.py` |
| student PDF custody | PASS_17_A4 | exact repository binary in `PDFs/GEO04_Student_Pack_v1.pdf` |
| teacher PDF custody | PASS_6_A4 | exact repository binary in `PDFs/GEO04_Teacher_Key_v1.pdf` |
| structural preflight | PASS | open/text extraction, A4/page counts, encryption NONE, learner scrub |
| page-by-page visual QA | PASS_23 | 17/17 student and 6/6 teacher pages inspected at 200 dpi |
| exact render regression | PASS_ZERO_DIFF | repository binaries vs approved corrected candidate: student 0/17 changed; teacher 0/6 changed |
| classroom timing/readability | NOT_RUN | evidence-dependent classroom gate |
| longitudinal retention | NOT_RUN | evidence-dependent |
| psychometric calibration | NOT_RUN | evidence-dependent |
| qualification/pass-mark calibration | NOT_RUN | unsupported by static authoring |
| publication approval | NOT_RUN | separate human decision |

## Benchmark judgment

GEO-04 meets the same static artifact readiness class as the Grade 9 Quadratics v2 benchmark: source custody, independent mathematics, recognition-first pedagogy, attempt-before-hint/fading architecture, teacher synchronization, canonical metadata, reproducible rendering, repository binary custody and exact page visual QA are closed.

## Static disposition

`BENCHMARK_READY_NOT_CLASSROOM_CALIBRATED`

This is not a claim of classroom effectiveness, retention, psychometric calibration, qualification probability or publication approval.
