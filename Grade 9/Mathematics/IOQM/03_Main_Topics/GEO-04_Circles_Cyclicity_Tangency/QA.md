# GEO-04 — Production QA

Status: `BENCHMARK_PEDAGOGY_MATH_SOURCE_METADATA_PASS_PDF_AUDIT_RUNNING`

| Gate | State | Evidence |
|---|---|---|
| issue #84 scope | PASS | centre/inscribed angles, cyclicity, tangency, alternate segment, power, chords/secants and representation choice retained |
| GEO-02 provider | PASS_ACCEPTED | exact frozen `GEO02_Stable_Angle_Polygon_Interface_v1.md` consumed |
| provider boundary | PASS | generic angle/quadrilateral canon retrieved; circle canon taught here |
| source anchors | PASS_5 | `IOQM-2025-Q19,Q23,Q30`; `IOQM-2024-Q17`; `IOQM-2023-Q15` |
| historical answers | PASS_5 | `29,03,10,25,03` independently re-derived |
| exact source/page visual custody | PASS_5 | official/controlled printed pages inspected for all five anchors |
| historical printed figure dependency | PASS_NONE | exact page inspection confirms no printed problem diagram in any of the five anchor statements |
| Q23 canonical interpretation | PASS_REQUIRED | non-degenerate branch preserved; final-key committee rejected the degenerate branch that makes concyclicity vacuous |
| microstream interfaces | PASS_7 | circle angles; cyclicity; tangency; alternate segment; power; chords/secants; source audit |
| topic-lead integration | PASS | recognition-chain sequence frozen in `Authoring/Lead_Integration_Map.md` |
| integrated Assimilation Book | PASS | structure/legal-hypothesis first, then theorem selection and representation choice |
| First-Step Reference | PASS | same-chord/cyclicity/tangent/power/common-chord/coordinate router |
| Recognition/First-Line Lab | PASS_16 | first-move recognition and theorem-legality checks |
| practice ladder | PASS_22 | direct recognition through mixed historical-style transfer |
| first mastery attempt | PASS | `06_H0_Mastery_Test.md` is unlabelled and unhinted |
| mastery items | PASS_12 | circle angles, cyclicity, tangent/power, common chord, route choice and WHY-NOT trap |
| benchmark assimilation lab | PASS | RECONNECT, error lab, ADOPT, changed-surface transfer and six-question assimilation test |
| teacher key synchronization | PASS | core Teacher Diagnostic Key and benchmark-lab key independently checked |
| Quadratics-v2 pedagogy comparison | PASS_ARCHITECTURE | `Authoring/Quadratics_v2_Benchmark_Comparison.md` |
| metadata schema | PASS_84 | canonical 31-column `Item_Metadata.csv`; 84 controlled rows |
| answer verification flag | PASS | every metadata row records `answer_verified_independently=true` |
| canonical renderer | PASS_COMMITTED | `Authoring/render_geo04_pdfs.py` |
| candidate PDF build audit | RUNNING | one-shot GitHub Actions audit performs metadata validation, render, preflight and learner scrub before any binary custody commit |
| student PDF custody | PENDING | candidate not yet approved/committed |
| teacher PDF custody | PENDING | candidate not yet approved/committed |
| page-by-page visual QA | PENDING | candidate artifact must be inspected before custody promotion |
| classroom timing/readability | NOT_RUN | evidence-dependent classroom gate |
| longitudinal retention | NOT_RUN | evidence-dependent |
| psychometric calibration | NOT_RUN | evidence-dependent |
| qualification/pass-mark calibration | NOT_RUN | unsupported by static authoring |
| publication approval | NOT_RUN | separate human decision |

## Current benchmark judgment

GEO-04 now matches the Grade 9 Quadratics v2 benchmark on pedagogy, independent mathematics, source custody, theorem-legality diagnostics, learner assimilation loop, teacher synchronization and canonical metadata.

The final static-artifact label is withheld until the canonical student/teacher PDFs pass structural preflight, learner-control scrub, exact-binary repository custody and page-by-page visual inspection.

Classroom effectiveness and calibration claims remain outside this static QA record.
