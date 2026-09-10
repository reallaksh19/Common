# Physics rebuild — review and approval record

**Decision: the previous B30/B80 drafts needed a teaching rebuild, not cosmetic repair.** The new PDFs are ready for your review. This is an academic and publication review of artifacts, including simulated learner walkthroughs; it is not evidence from real student testing.

The two subtopics remain **distance and displacement** and **reading velocity–time area for displacement and distance**. B30 receives prerequisite repair and guided steps. B80 retains explanatory depictions and adds model comparison and transfer. The reusable skill also imposes a visual minimum for B90.

## What was examined

- The supplied `files (5).zip`, including its Physics publication skill, renderer, auditor and example models.
- The previous Motion B30 and B80 approval PDFs and their models.
- The attached **Motion_Unit9_Full_Batch_FINAL(1).pdf**, all 34 pages in text, with representative teaching, graph/diagram, question and solution pages inspected visually.
- The current Common repository's Physics skill, Physics subtopic book builder, general publication skill and its teaching/layout/question-bank references, Motion concept-book specification and question-bank skill. Repository review was pinned to commit **af4c5c73b87b26187aa6c930b60172cbb1f0f3e2**.

[Reviewed repository snapshot](https://github.com/reallaksh19/Common/tree/af4c5c73b87b26187aa6c930b60172cbb1f0f3e2/Grade%209)

The Unit 9 attachment teaches different, later Motion subtopics: common gravitational acceleration in relative motion, release from a moving platform, impact-speed symmetry and paired flight times. It is a teaching/design benchmark here, not the content denominator for these two introductory subtopics. This rebuild does not claim to reproduce its entire chapter or the repository's 68-question Motion source map.

## Comparison with the attached PDF

Page references in this table mean PDF page numbers, including the attachment's opening page.

| Dimension | Earlier B30/B80 drafts | Attached Unit 9 PDF | Rebuild decision |
|---|---|---|---|
| Physical meaning | Definitions and calculations often preceded any real depiction; placeholders carried the visual burden | P2 shows two bodies with matching gravity arrows; p9 links an upward-moving carrier to the stone's inherited motion | Make the physical relationship visible before introducing its compressed mathematical form |
| Teaching sequence | Blocks existed, but their presence did not establish comprehension | Situation, memory anchor, physical interpretation and guided application form a recognisable teacher sequence | Keep that progression; add explicit one-step and faded tasks for B30 |
| High-band explanation | Too much reliance on compressed statements | Even advanced relative/free-fall ideas retain diagrams | B80/B90 keep the decisive diagram, meanings and model conditions |
| Layout | Repeated cards, small type, production metadata and unfinished figures | Diagrams occupy meaningful space; related explanation sits nearby | Use large functional diagrams, nearby prose, a quiet task badge and a single takeaway |
| Practice and hints | Sparse practice; weak distinction between assistance and independent evidence | Separate transfer pages are useful, but p23 combines H1/H2/H3 and reveals the 50 m result | Separate the attempt, three distinct optional hints, and full solution; keep final answers out of hints |
| Derivation | Some rules were stated without sufficient construction | The paired-time result on pp18–20/34 is stated without enough reconstruction for a weak learner | Build each demonstrated relation from its picture; explain the rectangle and triangular-area factors |
| Core appendices | The earlier contract stopped at Appendix B and misclassified the handout | The attachment's transfer books do not supply the Core appendices | Require Appendix A practice, Appendix B hints/solutions and Appendix C printable handout in every Core Study Guide |
| Provenance | Audit labels could suggest stronger evidence than actually existed | Source/exam links are useful but their presence alone does not verify a claim | Keep original examples clearly identified; verify any actual exam citation separately |

## What was adapted from the attached Physics skill — and what was rejected

| Original skill element | Decision and reason |
|---|---|
| Publication JSON as source of truth | **Retained.** The renderer consumes structured models; the final PDF is not manually patched. |
| Band-aware design | **Retained and revised.** Support changes with the learner, while the underlying concepts remain identical. Percent labels are provisional profiles, not a validated placement rule. |
| Stable IDs, source references and derived page labels | **Retained.** Questions, hints, solutions and repair lessons have working links and printed page references. |
| Reserve → draw → advance | **Retained and enforced.** Text is measured; component bounds and actual PDF text collisions are checked. |
| Math-capable embedded fonts and render review | **Retained.** Equations use proper signs/subscripts; every final page was rendered at 200 dpi. |
| A book being publishable while required concept artwork is still reserved | **Rejected for learner release.** A weak learner cannot learn from an instruction describing a future diagram. Production placeholders may exist separately; the learner renderer requires final figures. |
| Forbidding worked explanation at B80/B90 as “re-teaching” | **Rejected.** A stronger learner still needs a visible concept, model conditions and an intelligible derivation bridge. Compress support selectively; do not ban explanation. |
| Production-state badges on learner pages | **Reduced.** Task labels such as Apply, Explain and Transfer help the learner. Internal audit/source-mapping states belong in the review record. |
| Technical gates interpreted as educational approval | **Rejected.** Numeric/schema/link checks are useful evidence about the artifact, not proof that a student understands it. |

The new implementation does not invoke the superseded placeholder-era renderer or auditor. Their originals remain in the backup.

## The rebuilt learner books

| Component | B30 — Build the picture | B80 — Reason and transfer |
|---|---|---|
| Teaching | Pp1–9: locate position, perform one step, distinguish route/endpoints, handle a nonzero start, read graph axes/duration, count movement, combine signed areas, complete a faded area task, justify a triangular region | Pp1–5: compare journeys, reconstruct signed area, split a zero crossing, interpret rest and initial position, reject the final-height shortcut |
| Appendix A · Core practice | Pp10–15: 8 questions | Pp6–11: 8 questions |
| Mixed attempt | Pp16–18: concepts hidden | Pp12–14: concepts hidden |
| Appendix B · Hints/solutions | Pp19–20 hints; p21 guided feedback; pp22–25 full solutions | Pp15–16 hints; pp17–20 full solutions |
| Post-marking diagnosis | P26 | P21 |
| Appendix C · Handout | P27: printable visual handout | P22: printable visual handout |
| Visual repair | Completed number lines for the vulnerable negative-coordinate and endpoint-change steps | Compact model explanations; graph-dependent solutions repeat the graph |

Shared A1, A2, A3 and A6 provide common comparison points. They are not a validated diagnostic test. B80 additionally changes the origin, contrasts the sign of one interval, interprets a new robot journey and solves an unequal zero-crossing case.

The B30 triangular-area tasks remain above zero; the text explicitly states that only a genuinely triangular region uses ½ × base × height. B80 models a sign-changing straight segment. Neither book introduces calculus or presents itself as the complete Grade 9–11 syllabus.

## Multiple passes and concrete repairs

| Pass | Finding | Change made |
|---|---|---|
| Source/core review | The repository already required physical depiction and explanatory progression; the old drafts did not execute those rules | Rebuilt the teaching models and renderer together |
| Physics teacher | “Velocity × time” was too broadly stated | Restricted the rectangle rule to constant-velocity intervals; derived the triangle geometrically |
| B30 walkthrough | A full nonzero-origin/reversal question arrived before evidence of simpler prerequisite steps | Added G1 location/movement/change tasks and G2 duration/area completion before full practice |
| B30 recovery review | A1/A2 arithmetic could still fail at the turning point or double negative | Added completed number lines, explicit turning position −4 m and a route-based explanation of +5 − (−2) |
| B80 walkthrough | A practice item repeated its worked example exactly | Changed the robot's graph and starting position; its new result is distance 12 m, displacement +4 m, final position −1 m |
| Diagram review | Opening B80 labels collided; a B30 repair diagram ambiguously combined two separate moves | Separated label bands; explicitly labelled the two separate repair arrows |
| Assessment review | Hints and solution navigation needed to work in print as well as on screen | Added distinct hint stages, clickable links and generated page references |
| Publication review | A solution graph crowded adjacent velocity ticks; one displayed equation stranded its unit | Enlarged solution graphs and recomposed the equation |
| Handout review | Standalone notation needed explicit meanings | Defined Δx, initial/final position symbols and the positive direction on the handout |

An independent artifact reviewer inspected both books and rechecked the principal repairs. The final small diagram/wording corrections were rechecked in the produced pages. No real-student outcome is asserted.

## Examside skill and demonstration

A separate **Physics ExamSIDE Practice** skill now defines the complete workflow: frozen source IDs, source/option/figure extraction, verified metadata, primary-concept mapping, H1/H2/H3 semantics, conceptual solutions, Core linkage and per-question audit. It has a runnable ledger checker.

Repository skills: [Physics Publication](../../../skills/grade9-physics-publication/SKILL.md) and [Physics ExamSIDE Practice](../../../skills/grade9-physics-examside/SKILL.md).

The publication model supports verified source citations and explicit adaptations; the renderer puts source links on both question and solution pages. A synthetic test checks those actual PDF links without pretending the fixture is a real exam source.

**Motion_Optional_Hint_Practice.pdf** demonstrates the question-bank layout with eight original questions, optional hints and full end solutions. It is clearly labelled original practice, not an ExamSIDE/PYQ corpus. No claim is made that all eligible external questions have been collected or verified.

## Verification and limits

- All 65 pages across the three final PDFs rendered at 200 dpi; full-book page rhythm and high-risk diagrams, handouts, equations and solutions inspected.
- Zero detected cross-line text collisions and zero words outside page bounds in the final PDFs.
- 47 internal links in B30, 42 in B80 and 32 in the standalone practice book checked against actual PDF destinations; printed page references derive from the same pagination plan.
- Eight Appendix A questions per Core book; primary coverage of all four selected concept claims; question/hint/solution destinations and Appendix A→B→C order checked.
- Twenty-seven targeted invalid-model cases plus pair-identity/difficulty mutations are rejected, including missing figures, missing Appendix C, missing graph, bad answer data, broken repair links, changed question count, missing external citation, missing difficulty badge and broken companion reciprocity. Boundary calculations cover a crossing inside one segment, a negative rectangle and rest.
- Independent recomputation covers seven B30 and six B80 numerical question records; the remaining conceptual/comparison cases and teaching calculations were reviewed directly.
- Both reusable skills have executable code, a detailed teaching contract, examples and validation. Technical checks remain distinct from user approval and classroom evaluation.

The broader Grade 9–11 board-specific syllabus has not been certified here. This is the requested two-subtopic Physics prototype. Mathematics and Chemistry remain outside this approval batch.

## Approval requested

Please judge **the explanation and depiction first**: B30 pp1–9, especially the one-step tasks on pp2/8; B80 pp1–5; then Appendix C and one Appendix A→B repair route. Approval should cover the teaching approach, band differentiation, appendix structure and publication grammar before this is scaled to further Physics subtopics or the next subject.
