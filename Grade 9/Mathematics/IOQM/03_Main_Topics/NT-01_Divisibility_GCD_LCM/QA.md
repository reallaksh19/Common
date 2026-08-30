# NT-01 - QA

Status: `BENCHMARK_READY_NOT_CLASSROOM_CALIBRATED`

Static QA was repeated against the current NT-01 sources rather than inherited from the earlier preview claim. The audit covers source custody, mathematical correctness, pedagogy/ownership, student-export hygiene, metadata conformance, and the final rendered PDF.

## Gate table

| Gate | State | Evidence |
|---|---|---|
| G0 source authority | PASS_STATIC | HBCSE official 2025 paper and final key recorded in `01_Source_Coverage_Map.md`; historical IDs remain `IOQM-2025-Q02` and `IOQM-2025-Q27`; no Grade-9-only syllabus or weightage claim. |
| G1 dependency | PASS_STATIC | `00_Concept_and_Dependency_Map.md` tags G9 core/IOQM bridge/deferred boundaries; NT-02 and NT-03 canon are excluded. |
| G2 one governing model | PASS_STATIC | `TARGET -> DIVISOR/MULTIPLE -> DIFFERENCE/REDUCTION -> GCD/LCM -> CHECK`. |
| G3 ownership/overlap | PASS_STATIC | NT-01 owns divisibility/gcd/lcm/Euclid; NT-02 owns congruence legality/cycles; NT-03 owns prime-exponent/divisor-count canon. |
| G4 research-interface discipline | PASS_STATIC | `Authoring/Microstream_Interfaces.md` is authoring-only and does not publish adjacent student chapters. |
| G5 lead integration | PASS_STATIC | one integrated Assimilation Book; no microstream chapter concatenation or agent boundaries in student material. |
| G6 deduplication | PASS_STATIC | definitions/derivations have one canonical teaching location; later files compress/retrieve rather than re-onboard. |
| G7 cross-boundary contrasts | PASS_STATIC | 9 explicit decision contrasts in the concept map, including all four required contrasts; First-Step strip revisits the boundaries compactly. |
| G8 attempt-before-help/fading | PASS_STATIC | TRY requires an attempt first; scaffolding is `H3 execution -> H2 structure -> H1 recognition -> H0 independent`. |
| G9 integrated First-Step | PASS_STATIC | one topic-wide `03_First_Step_Reference.md`, written as compression after the integrated book. |
| G10 H0 mastery | PASS_STATIC | 16 unlabelled items cover notice/first line, full mixed solve, same-surface/different-decision, changed-surface transfer, and WHY-NOT. |
| G11 independent mathematics | PASS_STATIC_FRESH_REAUDIT | all promoted numerical/proof answers in the Teacher Key were independently rechecked; both historical anchors were independently recomputed. |
| G12 source custody | PASS_STATIC | Q02/Q27 paper/key authority and stable IDs are explicit; author-created items have no fabricated historical attribution. |
| G13 student-export hygiene | PASS_STATIC | leakage scan across all student sources/PDF source found no Issue/PR/Wave/agent/microstream/interface/QA-state terminology. |
| G14 one render authority | PASS_STATIC | one deterministic PDF production path from the consolidated student sources; one page/header/typography system. |
| G15 render/preflight | PASS_STATIC | 5/5 pages rendered and visually inspected; structural preflight passes; page count/hash recorded below. |
| G16 transfer quality | PASS_STATIC | T2 representation, T3 context, and T4 downstream/cross-topic transfer surfaces are present; number changes alone are not treated as transfer. |
| G17 six-question ownership | PASS_STATIC | major mechanisms include mechanism/why, trigger, near-neighbour boundary, first line, independent solve, and changed-surface use across the integrated book/lab/bank/H0 paper. |
| G18 evidence-dependent gates | NOT_RUN | classroom timing/readability, longitudinal retention, psychometric difficulty/discrimination, qualification probability, percentile/pass-mark calibration. |

## Fresh source and mathematics audit

### IOQM-2025-Q02

Official target: positive integers `n<=100` divisible by 3 but not by 2.

Independent computation:

`floor(100/3)-floor(100/6)=33-16=17`.

Final official key: `17`.

Result: `PASS`.

### IOQM-2025-Q27

Let

`x=gcd(a,c)`, `y=gcd(b,c)`.

Using `lcm(t,c)=tc/gcd(t,c)`, the source relation reduces to

`a(27/x-26)+b(27/y-26)=0`.

For positive integer gcd values, `27/t-26` is positive only at `t=1`, so exactly one of `x,y` equals 1. Suppose `x=1`, `y>1`. Then

`a=b(26y-27)/y`.

Writing `b=yt` gives `a=(26y-27)t`; the bound `a<=50` forces `y=2`, `t=1`, hence `(a,b)=(25,2)`. Then `c=2s<=50` and `gcd(25,c)=1`, so among `s=1,...,25`, 20 values survive. The symmetric pair `(2,25)` contributes another 20.

Independent total: `40`.

Final official key: `40`.

Result: `PASS`.

### Author-created material

Static re-audit checked:

- Euclidean reductions and gcd values;
- all lcm/common-multiple reconstructions;
- complete positive-divisor lists where requested;
- gcd/lcm pair reconstruction and coprimality;
- divisibility-chain implications;
- linear-combination restrictions and attainability where a set of divisors is claimed;
- same-remainder unknown-divisor vs unknown-number boundary;
- H0 answers and final-condition checks.

No promoted numerical discrepancy remains in the current Teacher Key.

## Metadata QA

`Item_Metadata.csv` conforms to `IOQM_G9_Question_Metadata_Schema_v1.csv`:

- columns: 31/31;
- data rows: 64;
- malformed-width rows: 0;
- historical rows: 2;
- author-created rows: 62;
- historical anchors retain official source/key metadata;
- unmeasured difficulty/psychometric fields remain `NOT_RUN`.

## Stable prerequisite interface

`Authoring/NT01_Prerequisite_Interface.md` is frozen as `FROZEN_V1_FOR_DOWNSTREAM_RETRIEVAL` and records:

- prerequisites;
- concepts owned;
- retrieval cues;
- first-move rules;
- decision boundaries;
- misconception traps;
- reusable identities;
- downstream assumptions for NT-02, NT-03, NT-04 and COMB-04.

Downstream status: `READY_FOR_RETRIEVAL`.

## Student-export scrub

Source scan across:

- `02_Assimilation_Book.md`;
- `03_First_Step_Reference.md`;
- `04_Recognition_and_First_Line_Lab.md`;
- `05_Practice_and_Transfer_Bank.md`;
- `06_H0_Mastery_Test.md`;
- consolidated render source;

found no student-visible production-control terminology. Teacher/authoring artifacts retain control-plane information intentionally.

## Final PDF artifact

- path: `PDFs/NT01_Student_Pack_v1.pdf`
- render authority: deterministic ASCII-safe compact PDF builder from the corrected integrated student canon; complete companion student source files remain authoritative for the extended practice bank
- page size: 612 x 792 pt
- page count: **5**
- SHA-256: **`fad8b2f4fd7013c6a24185e12518c405cb06d2a3fd7234108aa394c7dc97858e`**
- encrypted: no
- openable by PyMuPDF: yes
- likely scanned: no
- XFA: no
- form fields: 0
- attachments: 0
- annotations: 0
- fonts: standard Type1 core fonts (Helvetica, Helvetica-Bold, Courier, Helvetica-Oblique), not embedded; student source is ASCII-only and visual QA found no glyph loss

### Page-by-page visual inspection

All **5/5** final pages were rendered to PNG at 180 dpi and inspected. Dense practice/mastery pages 4–5 were additionally checked at full page scale and remained legible. Result:

- clipping: none observed;
- overlapping text: none observed;
- broken/missing glyphs: none observed;
- equations outside margins: none observed;
- table overflow: none observed;
- student/teacher answer leakage: none observed.

`WAVE6_STATIC_RENDER_QA_PASS`.

## Explicit NOT_RUN / non-claims

The following are not inferred from static production QA:

- classroom timing/readability: `NOT_RUN`;
- longitudinal retention: `NOT_RUN`;
- psychometric difficulty/discrimination: `NOT_RUN`;
- qualification probability: `NOT_RUN`;
- percentile/pass-mark calibration: `NOT_RUN`;
- official IOQM topic weightage from the 90-question corpus: **not claimed**.

## Promotion and handoff state

```text
WAVE0_ARCHITECTURE_FROZEN
WAVE1_INTERFACES_COMPLETE
WAVE2_INTEGRATED_ASSIMILATION_PASS
WAVE3_FIRST_STEP_PASS
WAVE4_H0_MASTERY_PASS
WAVE5_INDEPENDENT_QA_PASS
WAVE6_STATIC_RENDER_QA_PASS
BENCHMARK_READY_NOT_CLASSROOM_CALIBRATED
```

NT-01 is statically handover-ready and its prerequisite interface is frozen for downstream retrieval. This is not a claim of classroom calibration or final publication approval.
