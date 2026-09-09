# Motion: B30 and B80 review package

**Status: draft for human review.** This is the two-subtopic teaching rebuild requested after review of the earlier B30/B80 PDFs. Review explanation and depiction before scaling production.

| Read | Purpose |
|---|---|
| [Review guide](REVIEW_GUIDE.md) | Page-indexed routes, reviewer roles and comment format |
| [B30 learner book](Motion_B30_Rebuilt.pdf) | 27 pages: pictures, prerequisite repair, guided work, independent practice and concept-hidden mixed transfer |
| [B80 learner book](Motion_B80_Rebuilt.pdf) | 22 pages: explanatory depictions, model comparison, transfer and post-marking diagnosis |
| [Optional-hint practice](Motion_Optional_Hint_Practice.pdf) | 16-page original-question layout demonstration with mixed-transfer surface |
| [Review and adaptation record](Physics_Rebuild_Review.md) | Reference comparison, retained/rejected skill rules, findings and repairs |
| [Concept map](CONCEPT_REVIEW_MAP.md) | Same four concept claims across both support profiles |
| [Reproduction instructions](REPRODUCE.md) | Build, schema, model, numerical and PDF checks |
| [Audit](Physics_Rebuild_Audit.json) | Frozen PDF/model hashes and prior review evidence |
| [Machine evidence](review_evidence.json) | Real command results bound to exact dependency and artifact hashes |
| [Visual evidence](visual_review_evidence.json) | Reviewer attestation bound to exact PDF hashes, page counts and render DPI |
| [Delivery record](DELIVERY_RECORD.md) | Repository basis, packaging checks, scope and next action |

## Skills and PDF schema

- [Physics Core/publication skill](../../../skills/grade9-physics-publication/SKILL.md)
- [Core teaching contract](../../../skills/grade9-physics-publication/references/core-teaching.md)
- [PDF schema](../../../skills/grade9-physics-publication/references/physics-publication-v2.schema.json)
- [Schema, placeholders, layout, badges and links](../../../skills/grade9-physics-publication/references/schema-and-layout.md)
- [Review and anti-drift gates](../../../skills/grade9-physics-publication/references/review-and-anti-drift.md)
- [Physics ExamSIDE workflow](../../../skills/grade9-physics-examside/SKILL.md)

The new skills adapt existing Physics/publication authorities. They do not replace the chapter's 68-question source map. This pilot covers **distance/displacement** and **signed velocity–time area** with authored examples. The practice PDF is not an assimilated ExamSIDE/PYQ corpus. B30/B80 denote provisional support profiles, not measured mastery. The skill specifies B90 depiction requirements; this batch contains no B90 PDF. Board-specific Grade 9–11 coverage and classroom effectiveness remain unverified. Mathematics and Chemistry await separate approval.

## Originals and backup

- [Reference Unit 9 PDF](sources/Reference_Motion_Unit9_Full_Batch.pdf)
- [Original B30](sources/Original_Motion_B30.pdf) and [original B80](sources/Original_Motion_B80.pdf)
- [Original Physics skill](sources/Original_Physics_SKILL.md) and [complete attachment](sources/Original_Physics_Skill_and_Drafts.zip)
- [Historical architecture note](sources/Original_Architecture_Concept_Note.docx), [extracted text](sources/Original_Architecture_Concept_Note_text.md) and [original archive](sources/Original_Architecture_Concept_Note.zip)
- [Before-rebuild backup](Physics_Before_Rebuild_Backup.zip), including prior approval drafts and a hash manifest

Historical files are comparison evidence, not active instructions for the new renderer. [FILE_MANIFEST.json](FILE_MANIFEST.json) records SHA-256 hashes for the live skill tree, shared contracts, router/install validators, and the complete Motion package; it excludes itself and the historical delivery record to avoid self-reference. `run_review_checks.py` captures the focused test executions, `record_visual_review.py` binds human inspection to exact PDFs, and `verify_review_package.py` recomputes the dependency/evidence/model/PDF/audit/summary/manifest chain.

Related work: [PR #151](https://github.com/reallaksh19/Common/pull/151) carries four encoded Motion publication chunks. This package does not modify those files or claim their source coverage. Reconcile the two efforts before merging them into one publication workflow.
