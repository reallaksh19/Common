# ALG-07 - QA

Status: `STATIC_SOURCE_REPAIRED__RENDER_REVALIDATION_REQUIRED`

This file records the current branch state after remediation of the independent review findings. Static claims are made only where the current repository sources support them.

## Gate table

| Gate | State | Evidence |
|---|---|---|
| G0 source authority | PASS_STATIC | HBCSE 2024 official paper/key; stable anchors `IOQM-2024-Q21`, `IOQM-2024-Q26`. |
| G1 dependency | PASS_STATIC | general inequality optimization remains ALG-02-owned. |
| G2 governing model | PASS_STATIC | `DISCRETE VALUE -> HALF-OPEN INTERVAL -> CONTINUOUS CONDITION -> INTEGER FILTER -> ENDPOINT CHECK`. |
| G3 ownership/overlap | PASS_STATIC | floor/ceiling interval decoding and discrete filtering remain ALG-07-owned. |
| G4 research-interface discipline | PASS_STATIC_REPAIRED | seven per-microstream files now follow `IOQM_G9_Microstream_Interface_Schema_v1.md` naming, required header and A-P field structure. The old consolidated file is synopsis-only evidence. |
| G5 lead integration | PASS_STATIC | one integrated Assimilation Book and learner vocabulary. |
| G6 deduplication | PASS_STATIC | definitions/derivations taught once; later material retrieves/compresses. |
| G7 cross-boundary contrasts | PASS_STATIC | required floor/truncation, real/integer, equation/algebra and endpoint contrasts present. |
| G8 attempt-before-help/fading | PASS_STATIC | authoring pedagogy follows H3 -> H2 -> H1 -> H0; internal codes are not required as mastery titles. |
| G9 integrated First-Step | PASS_STATIC | one topic-wide First-Step Reference. |
| G10 mastery | PASS_STATIC_REPAIRED | 16-item learner artifact is titled `Independent Mastery Check`; internal H0 control label removed from learner-facing title. |
| G11 independent mathematics | PASS_STATIC_FRESH_REAUDIT | historical anchors and promoted authored answers previously recomputed without discrepancy. |
| G12 source custody | PASS_STATIC | historical IDs/source/key roles explicit; author-created items have no fake attribution. |
| G13 student-export source hygiene | PASS_STATIC_REPAIRED | mastery title no longer exposes H0; further PDF verification is coupled to G15. |
| G14 one render authority | STALE_AFTER_SOURCE_CHANGE | repository PDF predates the repaired mastery source and cannot certify the current source state. |
| G15 render/preflight | NOT_RUN_CURRENT_SOURCE | previous 3-page inspection/hash applies only to the prior blob; regenerate and independently inspect the PDF from current sources. |
| G16 transfer quality | PASS_STATIC | representation, context and downstream discrete-filter transfers remain present. |
| G17 six-question ownership | PASS_STATIC | meaning, trigger, boundary, first line, independent solve and changed-surface use covered. |
| G18 evidence-dependent gates | NOT_RUN | classroom timing/readability, longitudinal retention, psychometrics, qualification probability and percentile/pass-mark calibration. |

## Per-microstream interfaces

Current required interfaces:

- `Authoring/IOQM-G9-ALG-07__W1-A__definition-order__interface.md`
- `Authoring/IOQM-G9-ALG-07__W1-B__endpoint-control__interface.md`
- `Authoring/IOQM-G9-ALG-07__W1-C__negative-inputs__interface.md`
- `Authoring/IOQM-G9-ALG-07__W1-D__translation-reflection-fractional-part__interface.md`
- `Authoring/IOQM-G9-ALG-07__W1-E__equations-inequalities__interface.md`
- `Authoring/IOQM-G9-ALG-07__W1-F__integer-filtering-counting__interface.md`
- `Authoring/IOQM-G9-ALG-07__W1-G__source-pyq-audit__interface.md`

Each is authoring-only research evidence and does not claim ownership of a standalone student chapter.

## Historical source audit

`IOQM-2024-Q21`: independent reconstruction gives unique `n=8991`, hence answer `91`; official key and verification ledger agree.

`IOQM-2024-Q26`: set `n=floor(x)` and use `x in [n,n+1)`; only `n=16,17` are feasible, sum `33`; official key and verification ledger agree.

## Metadata QA

`Item_Metadata.csv` remains the frozen 31-column schema with stable historical IDs. Difficulty/psychometric fields are not used as evidence.

## Stable prerequisite interface

`Authoring/ALG07_Prerequisite_Interface.md` remains the downstream retrieval interface; its mathematical content was not changed by this remediation.

## Render custody

The committed `PDFs/ALG07_Student_Pack_v1.pdf` is now **stale with respect to the current learner source** because the learner-facing mastery heading changed after the previously recorded render/hash. The old 3-page SHA-256 must not be presented as certification of the repaired source.

Required before promotion:

1. regenerate the student PDF from the current canonical sources;
2. record the new Git blob SHA and SHA-256;
3. perform independent current-blob 3/3 (or actual page-count) visual inspection;
4. rerun leakage/preflight checks;
5. then change G14/G15 to PASS only if the exact new artifact passes.

## Explicit NOT_RUN / non-claims

- classroom timing/readability: `NOT_RUN`;
- longitudinal retention: `NOT_RUN`;
- psychometric difficulty/discrimination: `NOT_RUN`;
- qualification probability: `NOT_RUN`;
- percentile/pass-mark calibration: `NOT_RUN`;
- official IOQM topic weightage from corpus recurrence: not claimed.

## Current promotion state

```text
WAVE0_ARCHITECTURE_FROZEN
WAVE1_INTERFACES_COMPLETE_REPAIRED
WAVE2_INTEGRATED_ASSIMILATION_PASS
WAVE3_FIRST_STEP_PASS
WAVE4_MASTERY_SOURCE_PASS
WAVE5_STATIC_SOURCE_QA_PASS
WAVE6_CURRENT_RENDER_QA_NOT_RUN
NOT_READY__RENDER_REVALIDATION_REQUIRED
```
