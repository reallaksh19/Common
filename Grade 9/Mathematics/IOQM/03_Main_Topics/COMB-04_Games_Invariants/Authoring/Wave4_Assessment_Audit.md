# COMB-04 Wave-4 Assessment / Transfer Audit

Status: `PASS_STATIC_WAVE4`

Scope: static lead audit of the Wave-4 learner/teacher assessment layer. This is **not** the fresh independent Wave-5 mathematical/source audit and is **not** render QA.

## Required inventory

- `04_Recognition_and_First_Line_Lab.md` — present; 6 recognition + 6 first-line items.
- `05_Practice_and_Transfer_Bank.md` — present; 12 mixed/transfer items.
- `06_H0_Mastery_Test.md` — present; 10 unlabelled/unhinted first-attempt items.
- `Teacher_Diagnostic_Key.md` — present; answers, first-line expectations, diagnostics, and internal ladder map.
- `Item_Metadata.csv` — present; frozen production schema.

Authored item count: `34`.  
Historical anchor rows: `3`.  
Total metadata data rows: `37`.

## Metadata checks

Frozen schema column count: `31`.  
Parsed row-width set during generation: `{31}`.  
Header/schema identity: `PASS_STATIC`.  
Authored item IDs: `COMB04-R01..R06`, `COMB04-L01..L06`, `COMB04-P01..P12`, `COMB04-M01..M10`.  
Duplicate authored IDs: `NONE`.  
Historical IDs are only `IOQM-2025-Q22`, `IOQM-2025-Q25`, `IOQM-2023-Q28`.

New authored rows use:

- `source_integrity_status=AUTHOR_CREATED`;
- `provenance=AUTHOR_CREATED_WAVE4`;
- `answer_verified_independently=false`;
- `classification_review_status=LEAD_STATIC_REVIEWED`.

The three historical rows inherit independent Batch-C verification only; no new independent-review claim is created in Wave 4.

## Learner-export / hint scrub

`06_H0_Mastery_Test.md` first attempt:

- no default method labels;
- no hint blocks;
- no answers;
- no diagnostic codes;
- no F0/F1/F2/F3/F4/XF labels;
- no internal topic IDs or wave controls.

`04` and `05` contain learner-facing mathematical vocabulary where recognition itself is the task, but no internal production/control-plane labels.

Teacher-only controls, answers, difficulty classifications, and diagnostic codes are isolated in `Teacher_Diagnostic_Key.md` and `Item_Metadata.csv`.

## Internal F0 -> F4 -> XF coverage

Authoring-only ladder semantics follow repository convention:

`F0 FOUNDATION -> F1 DIRECT -> F2 STANDARD -> F3 DISGUISED -> F4 PRELIMINARY-SPEED -> XF TRANSFER`.

Coverage evidence:

- foundation/recognition: `R01..R06`, `L01..L06`;
- direct/standard execution: `P01,P02,P04,P05,P07`;
- disguised/close-boundary selection: `P03,P06,P09,P10,P12`;
- changed-surface transfer: `P08,P11` plus mixed mastery;
- unhinted preliminary-speed/mixed selection: `M01..M08`;
- WHY-NOT / verification transfer: `M09,M10`.

These ladder labels are not printed in learner-facing files.

## Static mathematical checks

Lead/static checks performed for promoted authored answers:

- remove `{1,2}` normal-play game: losing class `0 mod 3`; `17` and `2026` are winning with certified moves to multiples of 3;
- remove `{1,3,4}` normal-play game: losing residues `{0,2} mod 7`; `20` is winning via `20 -> 16`;
- remove `{2,5}` normal-play game: losing residues `{0,1,4} mod 7`; `25` is losing;
- `1..8` square-product pairing: sums `5,5,13,13`, product `65^2`;
- `1..10` square-product pairing: sums `3,10,9,15,18`, product `270^2`;
- six-cycle triple-toggle invariant: two period-3 binary weight vectors `101101` and `011011` annihilate every legal move; any singleton has nonzero invariant signature;
- triple move permutation of `(2,-1,-1)`: all coordinates shift equally modulo 3, preserving pairwise residue differences;
- Euclidean subtraction and inversion-swap termination arguments use strict nonnegative integer monovariants.

Static lead result: `PASS`.

Fresh independent recomputation/reviewer status for authored Wave-4 items: `NOT_RUN` — required in Wave 5.

## Boundary / misconception safeguards

- reachability is not forceability: `PASS_STATIC`;
- W proof existential / L proof universal: `PASS_STATIC`;
- invariant compatibility is not sufficiency: `PASS_STATIC`;
- monovariant termination is not winner identity: `PASS_STATIC`;
- examples are not a covering construction: `PASS_STATIC`;
- deterministic branching is not automatically adversarial: `PASS_STATIC`;
- NT-01/NT-02 arithmetic is retrieved, not retaught: `PASS_STATIC`;
- historical Q28 figure is not reproduced: `PASS_STATIC`.

## Historical source custody

- `IOQM-2025-Q22 = 66` — inherited independent verification.
- `IOQM-2025-Q25 = 36` — inherited independent verification.
- `IOQM-2023-Q28 = 67` — inherited independent verification; figure remains source-controlled.

Historical stems are not copied into the new mastery/transfer bank.

## Gates not run

- `V2_VALIDATOR_SCRIPTS: NOT_RUN`
- `INDEPENDENT_TOPIC_WIDE_MATH_SOURCE_AUDIT: NOT_RUN`
- `RENDER_QA: NOT_RUN`
- `PDF_PREFLIGHT: NOT_RUN`
- `STUDENT_TEACHER_LEAKAGE_RENDER_SCRUB: NOT_RUN`
- `CLASSROOM_TIMING_READABILITY: NOT_RUN`
- `RETENTION: NOT_RUN`
- `PSYCHOMETRICS: NOT_RUN`
- `QUALIFICATION_PROBABILITY: NOT_RUN`
- `PASS_MARK_PERCENTILE_CALIBRATION: NOT_RUN`
- `PUBLICATION_APPROVAL: NOT_RUN`

## Promotion result

`WAVE4_ASSESSMENT_LAYER_READY_FOR_INDEPENDENT_AUDIT`

Exact successor boundary: Wave 5 fresh independent mathematical/source/pedagogy audit of every promoted answer/proof, metadata/source identity, dependency order, duplicated teaching, and learner-export hygiene. Do not start render/PDF publication until that audit is accepted.
