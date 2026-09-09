---
name: grade9-physics-publication
description: Create and rebuild visual Physics Core books for Grades 9–11 with differentiated B30/B80/B90 teaching, Appendix A questions, Appendix B printable handouts, optional hints and complete solutions at the end. Use for Physics concept review, learner PDF generation, publication schemas and anti-drift audits.
---

# Physics Core and publication

Teach the physical idea before compressing it into notation. A diagram placeholder is not an explanation. Band labels are provisional support profiles, never measured intelligence or validated mastery percentages.

## Establish authority

1. Read the attached skills, books and specified repository first. Back up originals and previous outputs with hashes.
2. Lock the product: source-preserving reconstruction, original teaching, or explicitly authorised rewrite. A design benchmark on different subtopics does not become the content source. Do not call a new replacement a zero-loss reconstruction.
3. Use canonical `grade9-physics`, `grade9-physics-subtopic-book-builder` and `grade9-publication` when available. This skill is their executable Core/publication adapter. Keep subject authority and source IDs; layout must not change physics.
4. Read [core-teaching.md](references/core-teaching.md) before authoring; [schema-and-layout.md](references/schema-and-layout.md) before rendering; [review-and-anti-drift.md](references/review-and-anti-drift.md) before certifying.
5. Use `grade9-physics-examside` for external ExamSIDE/PYQ collections. Original examples must not acquire an exam badge or a claim of complete external coverage.

## Mandatory Core structure

For each subtopic build:

`physical situation → depiction → notice → say in words → build relation → worked reasoning → faded attempt → independent transfer → repair`

Every Core book contains:

- Teaching pages with real concept depictions, including for B80/B90.
- **Appendix A — Questions:** bounded sets, purposeful drawing/working space, optional hints. Test explanation, reconstruction, representation translation and transfer as well as calculation.
- **Appendix B — Handout:** a self-contained, separately printable visual summary with symbol meanings, model conditions and a worked memory anchor.
- Optional hints after the handout: H1 Notice → H2 Model → H3 Start. Keep hints away from the first attempt.
- **Solutions at the very end:** recap, required graph/table, why, executable method, explicit answer/check, transferable idea and return link.

Teaching worked examples may show their answers; unanswered practice must not leak its own result earlier. The handout must not become an answer key. A separate question bank does not replace Core appendices.

## Differentiate teaching, not just arithmetic

- **B30:** repair prerequisites in the lesson; use a stable story; explain axes/signs/units and first-use words; count or depict before operating. Show a full model, then let the learner complete one step, then a whole task. Supply completed visual repairs in solutions.
- **B80:** retain a minimum meaningful diagram; compress familiar steps; require contrasts, sign/origin changes, reconstruction and model choice.
- **B90:** retain the depiction and model conditions. Remove a diagram only when the learner is deliberately asked to construct it independently.
- Keep the same concept claims across bands. Interpret task-level errors; a numerical slip alone does not diagnose conceptual failure.

## Execute the two-topic Motion profile

The bundled profile covers distance/displacement and signed velocity–time area. It is not the complete Grade 9–11 syllabus or a renderer for every Physics representation. Confirm board/year/source before asserting syllabus coverage. Add typed figure support and checks before publishing other representations.

With Python containing ReportLab, Pydantic 2 and PyMuPDF:

```bash
python scripts/make_motion_models.py
python scripts/validate_v2.py examples/motion_B30_v2.json
python scripts/render_v2.py examples/motion_B30_v2.json motion_B30.pdf
python scripts/render_v2.py examples/motion_B80_v2.json motion_B80.pdf
python scripts/audit_v2.py examples/motion_B30_v2.json motion_B30.pdf
python scripts/test_v2.py
```

Edit canonical JSON for a new book, or edit `make_motion_models.py` and regenerate this pilot. The generator overwrites its three named example files. Do not edit both and assume they stay aligned.

The Pydantic validator actually runs before rendering. Its exported [JSON Schema](references/physics-publication-v2.schema.json) is generated from the same classes. The renderer fails if content exceeds its reserved height. Figure primitives draw exact number lines, piecewise-linear v–t graphs, countable tiles and paired comparisons from data. Required final concept figures cannot be placeholders.

## Review and approve

Freeze scope and claims; review as a Physics teacher, B30 learner, B80/B90 learner, assessment editor and publisher. Record concrete observations and fixes. Build representative concept, graph, guided, handout, hint and solution pages before scaling. Execute semantic/layout checks, render all pages at 200 dpi, inspect all quantitative/diagram pages at full size, repair and rerun.

Keep `FOR_USER_REVIEW`, `TECHNICAL_CHECKS_PASSED`, `USER_APPROVED` and `CLASSROOM_EVALUATED` separate. Simulated learner reviews are not actual student evidence. Present the concrete Physics result for approval before Mathematics or Chemistry when the user requests that sequence.
