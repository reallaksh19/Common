# NT-02 - QA

Status: `BENCHMARK_READY_NOT_CLASSROOM_CALIBRATED`

This record certifies the current source state and the exact student/teacher PDF blobs after the Euler/Fermat coverage-hardening patch. Static promotion claims stop at repository/render QA; classroom, retention, psychometric and qualification-probability evidence remain `NOT_RUN`.

## Gate table

| Gate | State | Evidence |
|---|---|---|
| G0 source authority | PASS_STATIC | Q03/Q23/Q20 source/key custody retained; no topic-weightage claim. |
| G1 dependency | PASS_HARDENED | NT-01 divisibility/gcd and Euclid's Lemma are retrieved without re-teaching their canon. |
| G2 governing model | PASS_HARDENED | `TARGET MODULUS -> REDUCE STATE -> SHORT CYCLE / THEOREM -> LEGAL OPERATIONS -> CHECK`. |
| G3 ownership/overlap | PASS_HARDENED | modular legality/cycles and the bounded Euler bridge are owned here; Fermat is a labelled prime-modulus companion, not a separate topic. |
| G4 per-microstream interface schema | PASS_REPAIRED | seven `IOQM-G9-NT-02__W2-*__*__interface.md` files use the mandatory header and A-P contract; `Microstream_Interfaces.md` is index-only. |
| G5 lead integration | PASS | one integrated Assimilation Book and vocabulary. |
| G6 deduplication | PASS_HARDENED | prior divisibility facts are retrieved briefly; no duplicate canonical derivation. |
| G7 contrasts | PASS_HARDENED | equality/congruence, divisibility/congruence, cycle/brute force, cycle/Euler, legal/illegal cancellation and compatible/incompatible simultaneous congruences are explicit. |
| G8 attempt-before-help/fading | PASS_REPAIRED | learner-facing support uses descriptive scaffolding; H3-H0 remains authoring-control terminology only. |
| G9 integrated First-Step | PASS_HARDENED | topic-wide reference includes Euler's theorem, minimal totient meaning, coprimality gate, proof idea, cycle-vs-Euler boundary and Fermat companion. |
| G10 mastery | PASS_REPAIRED | learner title is `Independent Mixed Mastery Check`; 16 items; no H0 control label on learner surface. |
| G11 independent mathematics | PASS_STATIC_SECOND_ROUTE | Q03=25, Q23=31 and Q20=42 independently reconstructed; theorem hypotheses and authored cancellation/compatibility items independently checked. |
| G12 source custody | PASS | author-created items have no historical IDs; historical anchors preserve stable source IDs and verified statements. |
| G13 student-export hygiene | PASS_REPAIRED | learner source/PDF excludes H0-H3, T2-T4, Wave/PR/Issue and internal topic-code control labels. |
| G14 render authority | PASS_CURRENT_SOURCE | deterministic Pandoc/XeLaTeX render generated from canonical student and teacher inputs. |
| G15 structural preflight | PASS_CURRENT_BLOBS | both exact PDFs are openable, unencrypted, no forms/XFA, US Letter. |
| G16 exact-blob visual QA | PASS_13_OF_13 | all 9 student pages and 4 teacher pages rendered and inspected; no clipping, overlap, blank/orphan page, broken glyph or answer leakage. Multi-character exponent/totient rendering was explicitly checked after repair. |
| G17 learner inventory | PASS | Practice 1-30 and Independent Mastery 1-16 present in extracted text. |
| G18 transfer quality | PASS_HARDENED | short-cycle vs named-theorem selection and theorem-hypothesis checks are explicit without exposing internal topic codes. |
| G19 evidence-dependent | NOT_RUN | classroom timing/readability, retention, psychometrics, qualification probability, percentile/pass-mark calibration. |

## Historical anchor audit

- `IOQM-2024-Q03`: `5^k mod 100` stabilizes at 25 for `k>=2`; answer **25**.
- `IOQM-2024-Q23`: moduli below 31 fail by pigeonhole or explicit collision; fourth-power residues for 1 through 14 are distinct modulo 31; answer **31**.
- `IOQM-2025-Q20`: a universal period for `n^n mod 7` must preserve positions modulo 7 and the nonzero exponent period 6; minimum **42**.

## Coverage-hardening verification

### Euler's theorem

The learner layer now explicitly states, at bounded Grade-9 depth,

`gcd(a,n)=1 -> a^phi(n) congruent 1 (mod n)`

with a minimal definition of `phi(n)`, an invertible-residue permutation proof idea and a mandatory coprimality check.

### Fermat companion

Fermat's little theorem is explicitly labelled as a curriculum-design prime-modulus companion/corollary. It is not presented as an independently source-requested topic, and its prime/nonzero-base hypotheses are checked.

### Method boundary

A large exponent does not automatically trigger Euler/Fermat: the learner is instructed to prefer a short visible residue cycle when cheaper. This prevents theorem-name matching from replacing method selection.

## Current exact PDF custody

Audit authority: GitHub Actions run `33771692797` (`IOQM coverage hardening PDF audit`), all render/preflight/scrub/theorem-inventory/artifact steps PASS. Exact run-4 artifacts were then promoted into Git custody.

### Student artifact

`PDFs/NT02_Student_Pack_v1.pdf`

- page size: US Letter, `612 x 792 pt`
- page count: **9**
- file size: **76,069 bytes**
- Git blob SHA: **`5ae2d86b4aecdb4063cd8a758a7660a8cb6959a6`**
- SHA-256: **`63ec60c1305d1a7da810be55dbeb81379cf30816928771637b4e14053b972193`**
- PDF version: `1.5`
- encrypted: no
- forms/XFA: none
- forbidden learner-control scan: PASS / NONE
- Practice inventory: 1-30 PASS
- Independent Mastery inventory: 1-16 PASS
- visual inspection: **9/9 PASS**
- explicit notation inspection: `a^{phi(n)}` and multi-digit exponents render as grouped exponents; PASS.

### Teacher artifact

`PDFs/NT02_Teacher_Key_v1.pdf`

- page size: US Letter, `612 x 792 pt`
- page count: **4**
- file size: **60,671 bytes**
- Git blob SHA: **`56845118945081ef9442d55d363a9c79665d3b55`**
- SHA-256: **`bcfb92cde9985aa646f917cb69c690a40d38eff9aaee7b7f42d4aa5835c57cd1`**
- PDF version: `1.5`
- encrypted: no
- forms/XFA: none
- visual inspection: **4/4 PASS**

The GitHub blob SHAs and byte sizes were re-read from the branch after artifact promotion and match the inspected run-4 files.

## Per-microstream interface authority

- `Authoring/IOQM-G9-NT-02__W2-A__congruence-meaning__interface.md`
- `Authoring/IOQM-G9-NT-02__W2-B__legal-operations__interface.md`
- `Authoring/IOQM-G9-NT-02__W2-C__inverses-cancellation__interface.md`
- `Authoring/IOQM-G9-NT-02__W2-D__power-cycles__interface.md`
- `Authoring/IOQM-G9-NT-02__W2-E__last-digits-target-modulus__interface.md`
- `Authoring/IOQM-G9-NT-02__W2-F__simultaneous-congruences__interface.md`
- `Authoring/IOQM-G9-NT-02__W2-G__source-pyq-audit__interface.md`

The consolidated `Authoring/Microstream_Interfaces.md` remains navigation/index evidence only.

## Stable downstream interface

`Authoring/NT02_Prerequisite_Interface.md` is the downstream residue/cycle/theorem-legality interface. It exports reusable facts without moving canonical ownership.

## Explicit NOT_RUN

Classroom timing/readability, longitudinal retention, psychometric difficulty/discrimination, qualification probability and percentile/pass-mark calibration remain `NOT_RUN`. No official IOQM topic weightage is claimed.

## Promotion state

```text
WAVE0_ARCHITECTURE_FROZEN
WAVE1_INTERFACES_COMPLETE_REPAIRED
WAVE2_INTEGRATED_ASSIMILATION_PASS
WAVE3_FIRST_STEP_PASS_HARDENED
WAVE4_MASTERY_PASS
WAVE5_INDEPENDENT_QA_PASS
WAVE6_CURRENT_RENDER_QA_PASS_13_OF_13
BENCHMARK_READY_NOT_CLASSROOM_CALIBRATED
```
