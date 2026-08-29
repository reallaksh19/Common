# QA - Quadratics Transformed Roots, Integer Roots & Structural Reduction
## Issue #39

Completion state: `BENCHMARK_READY_NOT_CLASSROOM_CALIBRATED`

This QA covers the static teaching artifacts, mathematical audit, source custody, PDF render/preflight, and benchmark-method comparison. It does **not** claim classroom timing, learner readability, retention, or longitudinal transfer evidence.

---

# 1. Authority / input audit

Read before authoring:

- Issue #39 controlling brief;
- `Grade 9/skills/grade9-math/SKILL.md`;
- partial-knowledge assimilation concept map;
- Quadratics assimilation concept map;
- Polynomial/Root Structure source coverage map;
- `grade9-math-assimilation/SKILL.md`;
- `concept-book-see-realize-understand-adopt.md`;
- Quadratics v2 retrace runbook;
- Quadratics subtopic prompt pack;
- benchmark PR #34, including its supersession/merge trail;
- benchmark manifest/README and canonical benchmark teaching sources.

Current `main` authority at start of work: `d2469be2c3160a5e2a0edbee16289cd218a87efe`.

Result: **PASS**.

---

# 2. Concept-map-before-prose proof

Dedicated branch:

`issue-39-quadratics-transformed-integer-reduction`

Commit order:

1. concept map first: `6e0815212e9b6f14c768c2fd3a36508ad0aae7f3`;
2. assimilation prose/module: `a986115112ad32436c9fe9bab45f5271e796b7dd`;
3. First-Step compression after teaching: `17c2f774366ace5d56d6b945636482b8749d81d2`;
4. independently audited answer/diagnostic key: `650db3978d4ffced80fec13eed3bb865766a8940`.

The concept map includes required node classes: prior knowledge, likely half-knowledge, missing bridges, invariants/structure, representations, decision boundaries, misconception traps, first moves, H3->H0 fade, transfer endpoints, source custody, and downstream #40 interface.

Result: **PASS**.

---

# 3. Scope coverage

## Strand A - transformed roots

Covered:

- shifted roots `alpha+h, beta+h`;
- reciprocal roots with `P != 0` domain check;
- squared roots;
- formation of new quadratic from transformed sum/product;
- transformed roots vs `f(x+h)=0` input shift;
- mechanism grounding to `NMTC-BH-P-2024-Q22`.

Result: **PASS**.

## Strand B - positive / integer roots

Covered:

- `P>0` as same-sign logic for real roots;
- `S` used to select positive vs negative;
- reality kept as a separate gate;
- positive-integer factor-pair restrictions;
- parity and divisibility filters;
- AM-GM equality collapse;
- clean grounding to `NMTC-BH-P-2024-Q17`;
- bridge evidence `NMTC-BH-P-2023-Q13` kept as bridge evidence, not inflated;
- `NMTC-BH-P-2025-Q20` retained as source-conflict evidence only.

Result: **PASS**.

## Strand C - structural power reduction

Covered:

- quadratic relation treated as a rewriting machine;
- derivation of `x^n = p x^(n-1) + q x^(n-2)` from `x^2=px+q`;
- reduction to `Ax+B`;
- cycle recognition;
- reciprocal-power recurrence;
- explicit WHY-NOT contrast against automatic root solving;
- clean mechanism grounding to `NMTC-BH-P-2018-Q06`, `NMTC-BH-P-2023-Q03`, `NMTC-BH-P-2024-Q01`.

Result: **PASS**.

---

# 4. Decision-boundary audit

Required boundaries present:

1. transformed roots vs shifted function input;
2. positive real roots vs positive integer roots;
3. explicit quadratic solving vs reduce-powers-first;
4. valid/clean source mathematics vs source/key conflict.

Additional close contrasts included:

5. reciprocal-root equation vs reciprocal-sum-only target;
6. equality collapse vs ordinary factor-pair enumeration.

Every pair asks the learner to identify why the chosen first move fits and why the tempting alternative is inferior or invalid.

Result: **PASS**.

---

# 5. Pedagogy / fading audit

Required loop implemented:

`RECONNECT -> DISCOVER -> MAKE SENSE -> TRY -> DIAGNOSE -> FADE -> ADOPT -> TRANSFER`

Attempt-before-hint rule implemented: every practice item starts with an H0 attempt. Across each of the three strand ladders the maximum available support fades:

`H3 -> H2 -> H1 -> H0`.

First-Step Reference was authored and committed only after the teaching module. It is explicitly labelled as a compression/revision layer, not the initial teaching mechanism.

Recognition-only laboratory and six-question assimilation check are included.

Result: **PASS**.

---

# 6. Practice-volume audit

Full solve/reasoned items:

- transformed-root ladder A1-A4: 4;
- positive/integer ladder B1-B4: 4;
- structural-reduction ladder C1-C4: 4;
- mixed transfer X1-X10: 10.

Total promoted practice/transfer outcomes: **22**.

This exceeds the Issue #39 minimum of 18. The set includes foundation/direct, disguised, decision-boundary and non-identical transfer surfaces.

Separate recognition-only prompts: 8.

Contrast pairs: 6.

Result: **PASS**.

---

# 7. Independent mathematical answer audit

Every promoted A/B/C/X outcome was recalculated after authoring.

Verification routes included:

- explicit original and transformed roots for A1, A2, A3 and X1 where convenient;
- direct shifted-input expansion for A4;
- exhaustive integer factor-pair enumeration for B/X integer cases;
- AM-GM plus discriminant cross-check for B3;
- discriminant plus Vieta sign conditions for X6;
- polynomial remainders modulo the governing quadratic for C1, C2, C3, X7 and X8;
- reciprocal recurrences for C4 and X9;
- source-integrity contract check for X10.

Audit count: **22 / 22 PASS**.

No answer was promoted solely from the authoring derivation.

Result: **PASS**.

---

# 8. Source integrity audit

Source roles preserved:

| ID | Role | Disposition in this unit |
|---|---|---|
| `NMTC-BH-P-2024-Q22` | `CLEAN_SCORED_ANCHOR` | transformed/input-shift mechanism grounding |
| `NMTC-BH-P-2024-Q17` | `CLEAN_SCORED_ANCHOR` | positive-root/equality grounding |
| `NMTC-BH-P-2023-Q13` | `BRIDGE_EVIDENCE` | admissible integer/discriminant bridge only |
| `NMTC-BH-P-2018-Q06` | `CLEAN_SCORED_ANCHOR` | reduction-before-solving grounding |
| `NMTC-BH-P-2023-Q03` | `CLEAN_SCORED_ANCHOR` | reciprocal/high-power reduction grounding |
| `NMTC-BH-P-2024-Q01` | `CLEAN_SCORED_ANCHOR` | recurrence/cycle grounding |
| `NMTC-BH-P-2025-Q20` | `SOURCE_CONFLICT_EVIDENCE` | source-QC only; never canonicalized or silently repaired |

The 2025 record is not reproduced as a clean exercise. The student QC box says to derive from the print, preserve the printed sign, document the key disagreement, and retain conflict status.

Result: **PASS**.

---

# 9. Rendered PDF QA

## Student pack

Filename:

`Quadratics_Transformed_Integer_Structural_Reduction_Student_Pack.pdf`

- pages: 12;
- A4 page size throughout;
- openable by PyMuPDF: yes;
- encrypted: no;
- likely scanned: no;
- XFA: no;
- SHA-256: `a718f734dba0945446f02bd61ee8f61da0140b45707f587ce30d4a131269eb24`;
- size: 286,583 bytes.

Final 180-dpi all-page render inspected as a 12-page contact sheet. No clipping, overlap, black boxes, broken math glyphs, missing pages, or off-page tables were observed. Final compile had no overfull-box warning; only non-fatal `tcolorbox` break/rerun warnings, with the relevant rendered page visually checked.

Result: **PASS**.

## Teacher key

Filename:

`Quadratics_Transformed_Integer_Structural_Reduction_Teacher_Key.pdf`

- pages: 6;
- A4 page size throughout;
- openable by PyMuPDF: yes;
- encrypted: no;
- likely scanned: no;
- XFA: no;
- SHA-256: `62f3753c314f2090f834ff6cb34974697204c8c2aa3e3e2142068244af777e40`;
- size: 311,178 bytes.

All 6 pages rendered and inspected. No clipping, overlap or broken glyphs were observed. The final compile contains no overfull-box warning.

Result: **PASS**.

---

# 10. Benchmark comparison

The benchmark PR/merge trail, benchmark manifest/README, canonical benchmark teaching source, First-Step architecture and QA expectations were read and used as production/pedagogy comparators only. No benchmark wording or layout was copied.

Compared properties:

- concept map precedes prose;
- partial-knowledge learner model;
- understanding before compression;
- attempt-before-hint and faded support;
- contrast-driven method selection;
- recognition/first-move emphasis;
- independent answer audit;
- separated student and teacher functions;
- explicit source roles/conflict handling;
- static QA separated from classroom calibration.

Architecture/content-quality comparison: **PASS**.

True benchmark-PDF side-by-side rendered visual comparison: **PARTIAL**. The benchmark binary stream was visible through the GitHub connector, but could not be mounted/rendered through the available PDF path in this run; direct web PDF open also failed. Therefore no unsupported claim of pixel/layout equivalence is made. The new PDFs themselves were fully rendered and inspected.

---

# 11. Gate table

| Gate | Evidence | Status |
|---|---|---|
| Required authority inputs read | issue, skills, maps, source map, runbook, prompt pack, benchmark trail | **PASS** |
| Subtopic concept map created before prose | commit `6e0815...` precedes module commit | **PASS** |
| Transformed-root mechanisms complete | shift, reciprocal, square, transformed equation, input-shift boundary | **PASS** |
| Positive/integer-root mechanisms complete | sign, reality, factor pairs, parity/divisibility, equality | **PASS** |
| Structural reduction complete | rewrite rule, recurrence, cycle, reciprocal recurrence | **PASS** |
| Mandatory decision boundaries | 4 required + 2 additional close contrasts | **PASS** |
| H3->H0 fading with attempt first | three ladders, H0 attempt before optional support | **PASS** |
| First-Step only after teaching | separate later commit and later PDF section | **PASS** |
| Minimum practice volume | 22 promoted items vs minimum 18 | **PASS** |
| 2025 source conflict preserved | Q20 conflict-only, no silent repair | **PASS** |
| Independent answer verification | 22/22 second-route audit | **PASS** |
| Production math notation | LaTeX typeset equations in PDF | **PASS** |
| Student PDF preflight/render QA | 12 pages, full render inspected | **PASS** |
| Teacher PDF preflight/render QA | 6 pages, full render inspected | **PASS** |
| Benchmark architecture/content comparison | benchmark trail/manifest/source compared | **PASS** |
| Benchmark PDF side-by-side visual comparison | binary not renderable through available connector path | **PARTIAL** |
| Classroom timing/readability calibration | no observed learner session | **NOT_RUN** |
| Longitudinal retention/transfer calibration | no delayed classroom evidence | **NOT_RUN** |

---

# 12. Final disposition

Static pedagogy, mathematics, source integrity, practice coverage and rendered-artifact QA satisfy Issue #39 acceptance requirements.

**Static artifact readiness: PASS.**

**Classroom calibration: NOT_RUN.**

**Overall completion state: `BENCHMARK_READY_NOT_CLASSROOM_CALIBRATED`.**
