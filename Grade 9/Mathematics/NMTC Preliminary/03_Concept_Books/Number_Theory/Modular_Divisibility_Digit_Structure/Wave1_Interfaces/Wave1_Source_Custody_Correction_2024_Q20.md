# Issue #47 — Wave 1 Source-Custody Correction: 2024 Q20

`STATUS: AUTHORITATIVE_FOR_ISSUE47`

This note supersedes the Wave-0 inventory row that classified `NMTC-BH-P-2024-Q20` as a clean simultaneous-congruence anchor.

## What the repository previously said

The older 2024 qualification summary and topic source map represented Q20 as if the same number satisfied:

- remainder 3 modulo 5;
- remainder 2 modulo 6;
- remainder 2 modulo 7;

while also retaining keyed answer 43.

That interpretation is mathematically impossible for 43 because `43 mod6 = 1` and `43 mod7 = 1`.

## Exact-source recheck during Wave 1

The reproduced 2024 stem says Simon was asked to divide a number by 120 and “divided the number by 5, 6 and 7 and got 3, 2 and 2 as remainders respectively.”

The 2024 Junior answer key records Q20 as `43*`.

A published solution interprets the wording as successive quotient division:

`N=5q1+3`

`q1=6q2+2`

`q2=7q3+2`

which gives:

`N=210q3+73`.

The solution then chooses the first value above 120 (`q3=1`, `N=283`) and reports `283 mod120 = 43`. The reproduced stem does not state the additional condition needed to force that choice; for example `q3=0` gives `N=73`.

## Issue-47 disposition

Therefore:

`NMTC-BH-P-2024-Q20 = SOURCE_CONFLICT_EVIDENCE — BLOCKED_EXACT_ANCHOR`

Allowed uses:
- source-QC case;
- representation-boundary contrast between direct simultaneous remainders and successive quotient remainders;
- evidence that a key/solution cannot override missing mathematical conditions.

Forbidden uses:
- clean simultaneous-congruence anchor;
- canonical solved student exercise;
- ordinary scored recurrence for the simultaneous-congruence mechanism.

## Updated source counts for Issue #47

- clean scored core mechanism IDs: **16**;
- additional clean scored ceiling/transfer bridge IDs: **4**;
- total clean scored mechanism IDs: **20**;
- source-sensitive blocked: `NMTC-BH-P-2023-Q12`;
- source-conflict blocked: `NMTC-BH-P-2024-Q20`;
- topic-specific bonus evidence: **0**.

## Upstream debt

The global `2024_Bhaskara_Preliminary_Qualification_v1.md` summary still describes Q20 as simultaneous congruences. That upstream row should be corrected separately. For Issue #47 teaching and QA, this correction note and the corrected topic Source Coverage Map are authoritative.

`SOURCE_CUSTODY_CORRECTION_GATE: PASS`