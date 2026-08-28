# Polynomial & Root Structure — PYQ Source Coverage Map v1

## Purpose

Trace each teaching mechanism in the P0 Polynomial & Root Structure unit to solution-qualified Bhaskara Preliminary evidence.

This is mechanism grounding, not reproduction of full paper statements.

## Provenance vocabulary

- `CLEAN_SCORED_ANCHOR` — scored item, mathematically qualified, source clean enough for mechanism use; exact figure may still be separately gated if relevant.
- `BONUS_EVIDENCE` — authentic paper mathematics but not ordinary scored recurrence.
- `SOURCE_CONFLICT_EVIDENCE` — useful for source-QC/contrast only; not a canonical exercise.
- `BRIDGE_EVIDENCE` — nearby mechanism supports the teaching transition but is not the exact named syllabus concept.

---

## Coverage table

| Teaching mechanism | PYQ ID | Evidence role | Grounded first move / invariant |
|---|---|---|---|
| high-power reduction from quadratic relation | `NMTC-BH-P-2018-Q06` | `CLEAN_SCORED_ANCHOR` | convert relation to `x^2+x+1=0`; reduce target modulo it |
| high-power reduction from quadratic relation | `NMTC-BH-P-2023-Q03` | `CLEAN_SCORED_ANCHOR` | use `x+1/x` / low-degree relation to collapse higher powers |
| high-power reduction from quadratic relation | `NMTC-BH-P-2024-Q01` | `CLEAN_SCORED_ANCHOR` | use `x^2=1-x`; generate only required recurrence |
| polynomial remainder modulo `x^2-1` | `NMTC-BH-P-2019-Q08` | `CLEAN_SCORED_ANCHOR` | use `x^2≡1` rather than long division |
| polynomial divisibility by quadratic | `NMTC-BH-P-2024-Q05` | `CLEAN_SCORED_ANCHOR` | remainder must vanish modulo `x^2+1` |
| quotient/remainder periodicity | `NMTC-BH-P-2024-Q16` | `CLEAN_SCORED_ANCHOR` | track sign/power cycle under `x^2+1` division |
| transformed-root Vieta | `NMTC-BH-P-2024-Q14` | `CLEAN_SCORED_ANCHOR` | recover original coefficients, then use root sum/product without explicit roots |
| positive roots + equality collapse | `NMTC-BH-P-2024-Q17` | `CLEAN_SCORED_ANCHOR` | Vieta fixes sum/product; AM-GM equality forces all roots equal |
| shifted function roots | `NMTC-BH-P-2024-Q22` | `CLEAN_SCORED_ANCHOR` | shift argument first, then use root structure |
| structural quartic factorization | `NMTC-BH-P-2024-Q24` | `CLEAN_SCORED_ANCHOR` | test simple rational roots; factor residual quadratic |
| symmetric high-degree reduction | `NMTC-BH-P-2019-Q25` | `CLEAN_SCORED_ANCHOR` | replace large symmetric expressions by sum/product style variables |
| common-root elimination | `NMTC-BH-P-2023-Q16` | `BONUS_EVIDENCE` | eliminate powers/parameter between two equations sharing a root |
| repeated-root discriminant | `NMTC-BH-P-2018-Q07` | `BONUS_EVIDENCE` | repeated root -> discriminant zero; recovered paper marks item bonus |
| cubic positive-integer root structure | `NMTC-BH-P-2025-Q20` | `SOURCE_CONFLICT_EVIDENCE` | Vieta + positive-integer partition gives roots `1,2,3`; printed constant/key sign conflict blocks canonical use |
| integer equation via discriminant | `NMTC-BH-P-2023-Q13` | `BRIDGE_EVIDENCE` | treat equation as quadratic, force admissible discriminant/integer cases |
| factor theorem / candidate-factor checking | `NMTC-BH-P-2018-Q03` | `BONUS_EVIDENCE` | test candidate linear factors; recovered paper explicitly marks bonus |

---

# Concept coverage by unit

## Unit 1 — equivalent polynomial views

Grounding support:

- 2024 Q24 demonstrates root/factor view selection;
- 2024 Q14 demonstrates coefficient/root view selection.

Author-created foundation examples are required because PYQs assume this fluency rather than teaching it.

## Unit 2 — power reduction

Grounding strength: **VERY STRONG**.

Clean scored years: 2018, 2023, 2024.

Canonical anchor preference:

1. 2018 Q06 — simplest clean relation-to-remainder bridge;
2. 2024 Q01 — stronger Preliminary transfer;
3. 2023 Q03 — advanced reciprocal/high-power variant.

## Unit 3 — Remainder / Factor Theorem

Grounding strength: **STRONG**.

Use author-created derivation examples first; then:

- 2019 Q08;
- 2024 Q05.

Do not use 2018 Q03 as a normal scored example; it is bonus evidence with a defective ordinary option set.

## Unit 4 — polynomial modular reduction

Grounding strength: **STRONG**.

Use sequence:

`x^2-1 -> x^2+1 -> x^2+x+1 -> unfamiliar quadratic divisor`.

Anchors:

- 2019 Q08;
- 2024 Q05;
- 2024 Q16.

## Unit 5 — Vieta without explicit roots

Grounding strength: **STRONG**.

Primary clean anchor:

- 2024 Q14.

Equality/positive-root extension:

- 2024 Q17.

## Unit 6 — transformed roots / shifts

Grounding strength: **MODERATE_STRONG**.

Clean anchor:

- 2024 Q22.

Author-created transfer must include reciprocal roots and squared roots because these are syllabus-natural transformations even when exact five-year PYQ recurrence is lower.

## Unit 7 — integer/positive root constraints

Grounding strength: **MODERATE**, high transfer value.

Use:

- 2024 Q17 as clean anchor;
- 2023 Q13 as integer/discriminant bridge;
- 2025 Q20 only as a source-QC contrast.

## Unit 8 — higher-degree reduction

Grounding strength: **STRONG**.

Use:

- 2019 Q25;
- 2024 Q24.

Do not teach general cubic/quartic formulas as the default Preliminary route.

## Unit 9 — common roots

Grounding strength: **BONUS-SUPPORTED** in current qualified corpus.

Use author-created scored-level foundation/transfer questions. 2023 Q16 may be shown only with explicit `BONUS_EVIDENCE` labeling.

---

# Missing or low-evidence areas that still require teaching

PYQ recurrence is not the whole syllabus.

The following need author-created foundation/transfer coverage even if no clean scored anchor is currently strong:

- formal derivation of Factor Theorem from Remainder Theorem;
- discriminant interpretation across `>0`, `=0`, `<0`;
- equation formation from transformed roots;
- remainder for a general linear divisor `ax+b`;
- relationship between common roots and polynomial gcd/factor ideas at Grade IX/X depth.

These are permitted because they are concept prerequisites/extensions, but must be labeled `AUTHOR_CREATED_FOUNDATION` or `AUTHOR_CREATED_TRANSFER`, never PYQ.

---

# Source-QC teaching opportunities

## 2018 bonus items

Q03/Q07 demonstrate why scoring disposition matters. They must not inflate scored recurrence.

## 2025 Q20

Use only in a teacher/source-integrity box:

1. derive the result from the printed sign;
2. compare with provisional key;
3. identify the single sign reversal that would reconcile them;
4. conclude `SOURCE_CONFLICT` rather than rewriting the question silently.

This trains mathematical verification as well as source custody.

---

# Publication readiness

Current source coverage status:

- power reduction: `READY_FOR_AUTHORING`;
- remainder/divisibility: `READY_FOR_AUTHORING`;
- Vieta/transformed roots: `READY_FOR_AUTHORING`;
- higher-degree structural factorization: `READY_FOR_AUTHORING`;
- common-root elimination: `AUTHOR_CREATED_CORE + BONUS_PYQ_EXTENSION`;
- full student publication: `NOT_READY` until worked pages, transfer items, mastery test and QA gates are completed.
