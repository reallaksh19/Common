# NT-01 — QA

Status: `NOT_READY__RENDER_REVALIDATION_REQUIRED`

This QA record describes the repaired current source state. It intentionally does **not** inherit final-render certification from the earlier PDF because learner-facing source files changed after that artifact was produced and inspected.

## Current static gate table

| Gate | State | Evidence / disposition |
|---|---|---|
| G0 source authority | PASS_STATIC | `IOQM-2025-Q02` and `IOQM-2025-Q27` retain official source/key custody and independently verified answers 17 and 40. |
| G1 dependency | PASS_STATIC | NT-02 congruence/cycles and NT-03 prime-exponent/divisor-count canon remain downstream; current authored repairs introduce no prerequisite inversion. |
| G2 governing model | PASS_STATIC | `TARGET -> DIVISOR/MULTIPLE -> DIFFERENCE/REDUCTION -> GCD/LCM -> CHECK`. |
| G3 ownership/overlap | PASS_STATIC | divisibility/gcd/lcm/Euclid/same-remainder structure remain NT-01-owned. |
| G4 research-interface discipline | PASS_STATIC | six separate files `IOQM-G9-NT-01__W1-A...F__...__interface.md` follow the mandatory filename/header/A–P contract; `Authoring/Microstream_Interfaces.md` is now explicitly index-only. |
| G5 lead integration | PASS_STATIC | one integrated student book; per-stream files remain authoring evidence only. |
| G6 deduplication | PASS_STATIC | downstream interfaces retrieve NT-01 canon rather than duplicating it. |
| G7 decision contrasts | PASS_STATIC | gcd/lcm, equal-remainder fork, divisibility-test/structural reasoning and Euclid/factorization boundaries remain explicit. |
| G8 attempt-before-help / fading | PASS_STATIC_SOURCE | learner source preserves progressive support without exposing internal H/T control codes as learner labels. |
| G9 First-Step layer | PASS_STATIC | topic-wide First-Step Reference remains integrated. |
| G10 independent mastery | PASS_STATIC_SOURCE | learner-facing mastery title is unlabelled; internal H0 control may remain in filenames/metadata/teacher artifacts only. |
| G11 mathematics | PASS_STATIC | source anchors and authored answers remain mathematically consistent with the teacher key after the Practice #23 repair. |
| G12 source custody | PASS_STATIC | author-created items remain distinct from historical PYQs. |
| G13 student-source hygiene | PASS_STATIC | repaired learner Markdown removes internal topic/transfer/support control labels where they were student-facing. |
| G14 rendered artifact custody | NOT_RUN_CURRENT_SOURCE | the committed PDF predates the latest learner-source repairs and is not accepted as current-source render evidence. |
| G15 current-blob structural/visual QA | NOT_RUN | regenerate the student PDF from current sources, record new hash/page count, then inspect every page of that exact blob. |
| G16 transfer quality | PASS_STATIC_SOURCE | representation/context/downstream transfer intent remains intact. |
| G17 ownership completeness | PASS_STATIC_SOURCE | meaning, trigger, boundary, first move, independent solve and transfer remain covered. |
| classroom timing/readability | NOT_RUN | evidence-dependent. |
| longitudinal retention | NOT_RUN | evidence-dependent. |
| psychometrics | NOT_RUN | evidence-dependent. |
| qualification probability / percentile calibration | NOT_RUN | evidence-dependent. |

## Repair verification

### Practice #23

The prior item referred to “the same lcm relation as the validated 2025 anchor” without restating the relation. The current source is self-contained and explicitly supplies

`27(lcm(a,c)+lcm(b,c)) = 26c(a+b)`

for positive integers `a,b,c<=50`, then asks the learner to derive the gcd restriction before enumeration.

The teacher-key reduction remains valid:

- set `x=gcd(a,c)`, `y=gcd(b,c)`;
- use `lcm(t,c)=tc/gcd(t,c)`;
- reduce to `a(27/x-26)+b(27/y-26)=0`;
- exactly one of `x,y` is 1 and, under the bound, the other is forced to 2.

### Wave-1 microstreams

The authoritative interfaces are now separate schema-compliant files:

- `IOQM-G9-NT-01__W1-A__divisibility-algebra__interface.md`
- `IOQM-G9-NT-01__W1-B__euclidean-algorithm__interface.md`
- `IOQM-G9-NT-01__W1-C__gcd-lcm-reconstruction__interface.md`
- `IOQM-G9-NT-01__W1-D__same-remainder-differences__interface.md`
- `IOQM-G9-NT-01__W1-E__divisibility-chains-extremal-divisors__interface.md`
- `IOQM-G9-NT-01__W1-F__source-pyq-misconception-audit__interface.md`

The legacy `Microstream_Interfaces.md` is an index only and carries no certification authority.

## Stable downstream interface

`Authoring/NT01_Prerequisite_Interface.md` remains the downstream retrieval contract for NT-02, NT-03, NT-04 and COMB-04. Its mathematical substance is unaffected by the learner-export repairs.

## Render revalidation requirement

The previously committed `PDFs/NT01_Student_Pack_v1.pdf` is retained in the branch but is **pre-repair render evidence**. It must not be used to assert current `WAVE6_STATIC_RENDER_QA_PASS`.

Required next render pass:

1. generate the student PDF from the current repaired learner sources;
2. verify canonical source/item-set custody against the generated artifact;
3. record current Git blob SHA, SHA-256, page size and page count;
4. run structural preflight;
5. render every page from that exact blob;
6. inspect every page for clipping, overflow, missing glyphs and answer/control-label leakage;
7. only then promote G14/G15 and the static benchmark state.

## Current promotion state

```text
WAVE0_ARCHITECTURE_FROZEN
WAVE1_INTERFACES_COMPLETE
WAVE2_INTEGRATED_ASSIMILATION_PASS
WAVE3_FIRST_STEP_PASS
WAVE4_MASTERY_SOURCE_PASS
WAVE5_STATIC_SOURCE_QA_PASS
WAVE6_CURRENT_RENDER_QA_NOT_RUN
NOT_READY__RENDER_REVALIDATION_REQUIRED
```

No classroom, retention, psychometric, qualification-probability or publication-readiness claim is made.
