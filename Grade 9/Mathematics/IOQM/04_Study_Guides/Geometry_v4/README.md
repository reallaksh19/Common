# IOQM Grade 9 Geometry — Question-Driven Visual Study Guide v4

Repository source/data package for the Grade 9 IOQM Geometry rebuild produced against the question-driven study-guide contract merged through PR #140.

## Canonical learner source

- `Geometry_Study_Guide_v4.md` — text-source representation of the 68-page learner guide. Figure locations are preserved as placeholders; the visual asset map is in `Figures/manifest.json`.

## Build/data

- `Build/geometry_v4_data.json` — supplied-question inventory, skill mapping, hint depth, answers, and other build data.
- `Build/geometry_skill_content.json` — stable Geometry skill-card content.
- `Build/geometry_bridges_content.json` — Advanced Worked Bridge content.
- `Build/appendixB_v4.json` — Appendix B mixed-transfer/audit set.
- `Build/build_geometry_v4_data.py` — data preparation source.
- `Build/create_geometry_v4_docx.py` — DOCX build source.

## Visual data

- `Figures/manifest.json` — figure-to-core/question/Appendix-B mapping used by the build.
- Raster figure assets and the final PDF/DOCX remain part of the complete release package generated from this source; the repository keeps the reproducible text/data layer and asset manifest alongside the audit records.

## Review/audit

- `Review/Question_to_Method_Matrix.md`
- `Review/Self_Sufficiency_Audit.md`
- `Review/Appendix_B_Method_Coverage.md`
- `Review/Sources_and_Citations.md`
- `Review/PR140_Alignment.md`
- `QA/QA.md`
- `QA/MANIFEST.sha256`

## Release identity

Final PDF from the complete package:

- Pages: 68
- Page size: US Letter
- SHA-256: `8a70fc24f8356f0272023c084713b4474b9a8cbfd7d7b09c1868fdc60029b409`

Editable DOCX SHA-256:

- `4729c52ed74b1a38a0c82170ad21366f66c77af209105c5430eb3f692c5ed119`

The optional 72-Hour Exam Navigator is not included because short-horizon mode was not requested for this build.