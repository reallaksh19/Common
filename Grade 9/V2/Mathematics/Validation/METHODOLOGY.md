# MATH-V2-07 methodology

1. Bind an exact candidate artifact SHA.
2. Evaluate human-quality eligibility before reading any reference.
3. Require engineering PASS, human subject/pedagogy/visual PASS, matching candidate SHA, positive evidence counts, no blocking findings, and benchmark state `NOT_RUN`.
4. If blocked, return named blocking reasons and `reference_read_attempted=false`.
5. Only an eligible candidate may resolve frozen mature Mathematics references.
6. A reference is validation-only authority, never producer or canonical authority.
7. Compare by validation dimensions; do not import a reference layout/template into production.
8. A comparative failure creates `VALIDATION_GAP` bound to exact candidate/reference digests.
9. Never mutate upstream canonical, learner, StudyModel, LearningDesign, semantic-product, or publication objects.
10. Test-only unlocked fixtures may prove mechanics but cannot generate release evidence.
