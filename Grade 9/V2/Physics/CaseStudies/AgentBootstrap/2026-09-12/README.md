# Physics learner-product case-study handoff

This directory is a **draft agent bootstrap / case-study handoff**, produced independently while reviewing Physics PR #332. It exists so a future agent can inspect concrete learner artifacts, audits, and the available generator source instead of restarting the product-quality exploration from scratch.

It is **not** a canonical release and does not supersede the repository's P-A -> P-L authority chain. Treat the PDFs as worked design evidence and regression fixtures. Reconcile any future production build back to the repository's source/scope/semantics contracts.

## Start here

The repository keeps the binary handoff as `physics-agent-bootstrap-2026-09-12.zip` so the case-study PDFs, audits, and available generator can travel together without scattering binary fixtures across the main tree. **Download/extract that bundle first**; paths such as `artifacts/final/...`, `audits/...`, and `scripts/...` below refer to paths inside the extracted bundle. The README and manifest are also committed separately for browsing.

Bundle SHA-256: `ad36facc746b715f5b10a76c851c0fa01eaf7a2bb1090afe79ab821eb177a034`.

1. Read this README and `physics-agent-bootstrap-manifest.json`.
2. For Chapters 2-5, inspect the final Core (1)/Core (2) pairs under `artifacts/final/`.
3. For Motion in 1D Core (1), prefer `physics-motion-1d-core1-visual-concept-atlas-final.pdf`; it is the latest teaching-surface rebuild and intentionally supersedes the older Core (1) answer-custody artifact.
4. Inspect `scripts/build_motion1d_visual_core1.py` for the available reproducible ReportLab implementation and visual primitives.
5. Read the audits before reusing an artifact as a regression fixture.
6. Do not copy or vendor the benchmark/reference PDFs that were supplied in chat. The case study used them to expose missing product contracts; the work here should remain independently authored.

## What this handoff captures

The rebuild sequence exposed a consistent distinction between **structural correctness** and **learner-product maturity**. The most important recovered contracts are:

- **Source reconciliation before authoring.** Freeze the topic denominator and classify every source item; concept coverage alone is not source completeness.
- **Atomic learner competencies.** Parent chapter concepts are too coarse for remediation. Core (1) needs smaller teachable competencies with exact repair targets.
- **Equation as model compression.** Teach the physical state/representation first; equations are selected only after model validity, target, and unnecessary-variable analysis.
- **Authoritative reasoning route.** Hints, full solutions, quick checks, and repair links should project from one semantic route rather than drift as separately authored prose.
- **Core (1) -> Core (2) closure.** No transfer step may require untaught reasoning; every important Core (1) competency should face transfer pressure in Core (2).
- **Progressive support.** Worked -> guided -> faded -> reverse/contrast -> controlled mutation -> pre-transfer -> mixed transfer.
- **Answer custody.** Every learner-facing question must resolve to an explicit answer artifact. A self-check, rubric, or verification is not the answer.
- **Three check layers.** Sanity check, item-specific quick check, and genuinely independent verification have different jobs.
- **Hint information budgets.** H1 notices the decisive feature; H2 selects model/representation; H3 performs only the first executable transition and must not resolve the requested result.
- **Representation is pedagogy.** Spatial/vector/state/graph problems should use domain-native diagrams/tables/graphs rather than prose when the representation carries the reasoning.
- **Concrete-state diagrams.** Avoid generic labels such as `phase 1 -> boundary state -> phase 2` when the physical events and boundary values are known. Show the actual event, state, local/global clock, and continuity relation.
- **Visual concept atlas standard.** Difficult ideas need state-sequence diagrams, sign/state labels, equation-selection tables, graph decoders, boundary-state strips, dual-track timelines, and annotated vertical-motion stages.
- **Responsive figure variants.** FULL / COMPACT / MICRO / ICON are different semantic renderings, not merely scaled versions of one figure.
- **Layout must be measured.** Compute row heights from wrapped text/figure bounds; width-only scaling and fixed hint heights are unsafe.
- **Intra-primitive collision detection.** Outer bbox containment does not prove a figure is readable; track text/geometry occupancy and reject invalid overlaps.
- **Figure/question state binding.** A rendered diagram must derive its values/labels from the same authoritative problem state as the question.
- **Learner typography.** A catastrophic PDF floor is not a learner body-text floor. Body, equation, caption, and micro-label sizes should be validated by role.
- **Appendix roles.** Appendix A = deliberate practice; B = question-context + worked repair; C = answer-free operational atlas. Reviewer provenance should not compete with learner reference surfaces.

## Maintained learner artifacts

### Chapter 2 - Vectors
- `artifacts/final/physics-vectors-core1-answer-custody-final.pdf`
- `artifacts/final/physics-vectors-core2-answer-custody-final.pdf`

### Chapter 3 - Motion in 1D
- `artifacts/final/physics-motion-1d-core1-visual-concept-atlas-final.pdf` **(preferred/latest Core 1)**
- `artifacts/final/physics-motion-1d-core2-answer-custody-final.pdf`

### Chapter 4 - Motion in 2D
- `artifacts/final/physics-motion-2d-core1-answer-custody-final.pdf`
- `artifacts/final/physics-motion-2d-core2-answer-custody-final.pdf`

### Chapter 5 - Newton's Laws of Motion
- `artifacts/final/physics-nlm-core1-answer-custody-final.pdf`
- `artifacts/final/physics-nlm-core2-answer-custody-final.pdf`

### Later case-study topics
- Gravitation Core (1)/(2), retained as source-completeness evidence.
- Work & Energy Core (1)/(2), retained as responsive-layout / micro-figure evidence.

## Motion in 1D visual Core (1): latest case study

The latest rebuild raises Core (1) from a revision-note surface toward a concept-breakdown atlas. Major concepts now receive concrete visual teaching frames such as:

- signed number-line path/displacement models;
- average-speed/average-velocity journey structures;
- velocity/acceleration sign-state sequences for speeding up, slowing down, and reversal;
- an operational UVATS equation table indexed by the **missing quantity** and model gate;
- equation reconstruction from acceleration definition and `v-t` area;
- separate `x-t`, `v-t`, `a-t`, `v-x`, and `v^2-x` graph literacy;
- concrete multiphase boundary-state strips;
- vertical launch/rise/top/fall/return state sequences;
- delayed-start and catch-up dual-track timelines using a shared event line and explicit local clock.

A key regression rule from this rebuild is:

> A diagram must represent the actual problem state. A generic schematic with abstract labels is not instructionally sufficient when concrete state information is known.

## Recommended next-agent workflow

For a new topic or a revision:

1. **Freeze source scope** and build a question-level ledger.
2. **Define parent concepts and atomic competencies** before pages.
3. For each competency, define recognition cues, native representation, mechanism, validity boundary, misconception/anti-trigger, reconstruction, guided/faded tasks, and answer artifacts.
4. Build a Core (2) matrix mapping each transfer item to exact Core (1) competencies and a D1-D4 difficulty level.
5. Render attempt pages with answer protection, then a results-only key, then full solutions with explicit final answers, checks, verification, and repair links.
6. Render every PDF to images; inspect high-risk pages manually; run text/bbox/collision checks.
7. Treat audit failures as contract failures, not page-specific styling issues.

## Known limitations of this handoff

- Only the Motion in 1D visual Core (1) generator source was still present in the workbench and is included here. The other PDF artifacts are retained as concrete design evidence but do not yet have their independent generator scripts in this handoff.
- These are independent case-study artifacts, not outputs of the canonical PR #332 cold-start runner.
- Human subject/pedagogy/assessment/visual review states remain outside this handoff.
- Historical intermediate PDFs are intentionally not vendored; this directory contains the maintained/final case-study artifacts plus audits, so an agent starts from the best-known state rather than from obsolete iterations.

## File integrity

| File | Bytes | SHA-256 |
|---|---:|---|
| `physics-vectors-core1-answer-custody-final.pdf` | 121632 | `1148cbdaebff7db6b36214b1a9cc2cc54d3db32500013471958965c579a3b957` |
| `physics-vectors-core2-answer-custody-final.pdf` | 145254 | `0dc83b9f65d2e8100ef4a1b923f937346cba7137112803d6b5301d8b8a24e319` |
| `physics-motion-1d-core1-visual-concept-atlas-final.pdf` | 140175 | `531929d459353f5ae23c567c825347a768f9e13ab853829ae0be4b6cd13d2bde` |
| `physics-motion-1d-core2-answer-custody-final.pdf` | 146815 | `0e61b6d6f7840cb16991afbd0c5727dc5b00ef0842757137eefbe2b83e352525` |
| `physics-motion-2d-core1-answer-custody-final.pdf` | 127143 | `d0de1c1cad3292059dff13c9d86efc7031d00e5f55e5e0af5da560380ba7115b` |
| `physics-motion-2d-core2-answer-custody-final.pdf` | 146393 | `70e14375fc768626a766c713743c03526bbffaa2386b29dfa15d5711735213c8` |
| `physics-nlm-core1-answer-custody-final.pdf` | 128345 | `7c3a5de9b083c014235093e54cf3ad8c518ecb6d3c6d6b4ef8456eda7866cb98` |
| `physics-nlm-core2-answer-custody-final.pdf` | 149719 | `6afcdd37d527278639d75a55f8be650c13edce5428590b09905f163992e54574` |
| `physics-gravitation-core1-source-complete-study-guide.pdf` | 116245 | `a28866a6c63d5cbcb07ff79aa124d37f31ecef302a6e5b9962d8ab5e245593f3` |
| `physics-gravitation-core2-diagrammatic-transfer-book.pdf` | 131600 | `90acbf1ca24326f4e2b0788045f96a01b6f464e505d6878f2685be8208b97125` |
| `physics-work-energy-core1-robust-layout-v2.pdf` | 130626 | `c6a171e35838b2493559ec908edff2a435ebcbe730830a7a8a74f4bc292dd839` |
| `physics-work-energy-core2-robust-layout-v2.pdf` | 147892 | `ae1b8d9f6a73b6a5d6a5f666c6bc9aaf6c987720e4b192cd721e1dc4aceba594` |
| `physics-foundation-ch2-5-answer-custody-consolidated-audit.json` | 3512 | `1ebd8833607859acbef81a0323f5c505e99a378c8f75ea71f2855975408fa508` |
| `physics-motion-1d-core1-visual-concept-atlas-audit.json` | 562 | `e7af3641a2f95b7ea33dc8002994f281d1a8a1f7a646e7f967d54211537663a5` |
| `physics-gravitation-source-complete-audit.json` | 1894 | `853f5d4b6683c0484162339d2baebfb65302e5814c5e613b130608a07de7a9ad` |
| `physics-work-energy-robust-layout-v2-audit.json` | 5029 | `2e420602ab04bcedb2a272ca81df5dc747cf42a2fe77d51563156dda8869f976` |
| `build_motion1d_visual_core1.py` | 50073 | `5d1a6103de9a4d0cacb1ce52726db50c5a69db3af18a4e8811e8df61b326f7db` |

## Relationship to PR #332

PR #332 contains the canonical P-G -> P-L implementation and honesty/custody machinery. The artifacts here were produced as independent controls to discover learner-product gaps that structural gates did not yet catch. The consolidated case-study comment on #332 should be treated as the implementation target; this handoff provides concrete examples and regression material for that contract.
