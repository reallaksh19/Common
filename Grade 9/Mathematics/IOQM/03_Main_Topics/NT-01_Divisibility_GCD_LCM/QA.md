# NT-01 — QA

Status: `BENCHMARK_READY_NOT_CLASSROOM_CALIBRATED`

This record certifies the current source state and the exact current student/teacher PDF blobs after the coverage-hardening patch. Static promotion claims stop at repository/render QA; classroom, retention, psychometric and qualification-probability evidence remain `NOT_RUN`.

## Current static gate table

| Gate | State | Evidence / disposition |
|---|---|---|
| G0 source authority | PASS_STATIC | `IOQM-2025-Q02` and `IOQM-2025-Q27` retain official source/key custody and independently verified answers 17 and 40. |
| G1 dependency | PASS_STATIC | Congruence/cycles and prime-exponent/divisor-count canon remain downstream; no prerequisite inversion is introduced. |
| G2 governing model | PASS_STATIC | `TARGET -> DIVISOR/MULTIPLE -> DIFFERENCE/REDUCTION -> GCD/LCM -> THEOREM CHECK -> CHECK`. |
| G3 ownership/overlap | PASS_HARDENED | divisibility, gcd/lcm, Euclidean reduction, same-remainder structure and Euclid's Lemma are NT-01-owned. NT-03 retrieves the lemma rather than reteaching it. |
| G4 research-interface discipline | PASS_STATIC | six separate `IOQM-G9-NT-01__W1-*__*__interface.md` files follow the mandatory filename/header/A-P contract; the consolidated interface file is index-only. |
| G5 lead integration | PASS_STATIC | one integrated learner book; per-stream files remain authoring evidence only. |
| G6 deduplication | PASS_STATIC | downstream interfaces retrieve NT-01 canon rather than duplicating it. |
| G7 decision contrasts | PASS_HARDENED | gcd/lcm, equal-remainder fork, divisibility-test/structural reasoning, Euclid/factorization and prime-vs-composite use of Euclid's Lemma are explicit. |
| G8 attempt-before-help / fading | PASS_STATIC | learner sources use descriptive support rather than internal H/T control labels. |
| G9 First-Step layer | PASS_HARDENED | topic-wide First-Step Reference includes the Euclid's Lemma statement, proof bridge, hypothesis check and composite countercontrast. |
| G10 independent mastery | PASS_STATIC | learner-facing title is `Independent Mastery Check`; internal H0 control remains only in filename/metadata/teacher surfaces. |
| G11 mathematics | PASS_STATIC | source anchors and authored answers remain consistent with the teacher key; Euclid's Lemma proof/check was independently reviewed. |
| G12 source custody | PASS_STATIC | author-created items remain distinct from historical PYQs. |
| G13 student-source hygiene | PASS_STATIC | learner Markdown/PDF is free of learner-facing H/T/Wave/PR/Issue/control labels in promoted surfaces. |
| G14 rendered artifact custody | PASS_CURRENT_BLOBS | the exact inspected run-4 student and teacher PDF bytes are committed in Git. |
| G15 current-blob structural/visual QA | PASS_CURRENT_BLOBS_19_OF_19 | structural preflight PASS; all 14 student pages and 5 teacher pages inspected with no clipping, overlap, broken glyphs, blank/orphan pages or control-label leakage. |
| G16 transfer quality | PASS_STATIC | representation/context/downstream transfer intent remains intact. |
| G17 ownership completeness | PASS_HARDENED | meaning, trigger, hypothesis boundary, proof bridge, first move, independent solve and changed-surface transfer are covered. |
| classroom timing/readability | NOT_RUN | evidence-dependent. |
| longitudinal retention | NOT_RUN | evidence-dependent. |
| psychometrics | NOT_RUN | evidence-dependent. |
| qualification probability / percentile calibration | NOT_RUN | evidence-dependent. |

## Coverage-hardening verification

### Euclid's Lemma

The learner layer now explicitly states the prime-product implication

`p prime and p|ab -> p|a or p|b`

and contrasts it with the invalid composite generalization. The teacher addendum diagnoses missing primality checks and confusion with the Euclidean algorithm. `Authoring/NT01_Prerequisite_Interface.md` exports the lemma for NT-03 retrieval.

### Existing repaired item

Practice #23 remains self-contained and explicitly supplies

`27(lcm(a,c)+lcm(b,c)) = 26c(a+b)`

for positive integers `a,b,c<=50`, then asks the learner to derive the gcd restriction before enumeration. The teacher-key reduction remains valid.

## Current render evidence

Canonical student inputs:

- `02_Assimilation_Book.md`
- `03_First_Step_Reference.md`
- `04_Recognition_and_First_Line_Lab.md`
- `05_Practice_and_Transfer_Bank.md`
- `06_H0_Mastery_Test.md`

Teacher inputs:

- `Teacher_Diagnostic_Key.md`
- `Teacher_Coverage_Hardening_Addendum.md`

Audit authority: GitHub Actions run `33771692797` (`IOQM coverage hardening PDF audit`), all render/preflight/scrub/theorem-inventory/artifact steps PASS. Exact run-4 artifacts were then promoted into Git custody.

### Student artifact

`PDFs/NT01_Student_Pack_v1.pdf`

- Git blob SHA: `f2f64c1bf9ad0c6187ed611f200e763b8ba44e56`
- SHA-256: `3f2a92a462ef1819aba418d3a30659ae66b5de353ba4f3872efc9d90db307041`
- byte size: `102904`
- PDF version: `1.5`
- page size: US Letter, `612 x 792 pt`
- page count: `14`
- encryption: none
- forbidden learner-control scan: PASS
- Practice inventory: items `1-30` present
- mastery inventory: items `1-16` present
- page-by-page visual inspection: PASS `14/14`

### Teacher artifact

`PDFs/NT01_Teacher_Key_v1.pdf`

- Git blob SHA: `872fdba537d0d2c06bd8908ebbb43fc2a7a6bad1`
- SHA-256: `9e2bfe8589451d6df78397efbe5b55605b24565e33a414502294573f34122e18`
- byte size: `65388`
- PDF version: `1.5`
- page size: US Letter, `612 x 792 pt`
- page count: `5`
- encryption: none
- page-by-page visual inspection: PASS `5/5`

The GitHub blob SHAs and byte sizes were re-read from the branch after artifact promotion and match the inspected run-4 files.

## Stable downstream interface

`Authoring/NT01_Prerequisite_Interface.md` remains the downstream retrieval contract. The coverage-hardening revision adds Euclid's Lemma as a controlled export without moving prime-factorisation ownership out of NT-03.

## Current promotion state

```text
WAVE0_ARCHITECTURE_FROZEN
WAVE1_INTERFACES_COMPLETE
WAVE2_INTEGRATED_ASSIMILATION_PASS
WAVE3_FIRST_STEP_PASS_HARDENED
WAVE4_MASTERY_SOURCE_PASS
WAVE5_STATIC_SOURCE_QA_PASS
WAVE6_CURRENT_RENDER_QA_PASS_19_OF_19
BENCHMARK_READY_NOT_CLASSROOM_CALIBRATED
```

No classroom, retention, psychometric, qualification-probability or publication-effectiveness claim is made.
