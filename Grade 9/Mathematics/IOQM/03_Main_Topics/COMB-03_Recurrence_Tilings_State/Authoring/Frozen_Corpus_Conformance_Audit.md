# COMB-03 — Frozen Corpus Conformance Audit

Status: `PASS_STATIC`

Purpose: verify that the COMB-03 research package has not drifted from the frozen 90Q corpus/verification authority while waiting for the COMB-01 provider interface. This is an ownership/provenance audit, not a substitute for the existing independent mathematical audit.

## Authority checked

- `01_Corpus/IOQM_2023_2025_90Q_Ledger_v1.csv`
- `01_Corpus/Verification/IOQM_2023_2025_Answer_Verification_Ledger_v1.csv`
- frozen production ownership under PR #67

## Item-level conformance

| Anchor | Frozen answer | Frozen COMB-03 mechanism / first move | Current PR #95 research representation | Verdict |
|---|---:|---|---|---|
| `IOQM-2024-Q14` | 80 | state evolution; near-edge target `(79,80)` sharply restricts histories; work backward and use the fact that only one non-right step is possible | sparse-history / near-boundary state collapse; one exceptional transition among 80 positions | PASS |
| `IOQM-2024-Q20` | 10 | state graph; reverse search; operations `n -> 2n` or `n -> n-3`; backward BFS from 121 toward 11 | deterministic state graph; forward-vs-reverse contrast; explicit shortest-path audit | PASS |
| `IOQM-2023-Q08` | 59 | tiling recurrence/state decomposition for a `2 x 7` board with dominoes and at most one `2 x 2` tile; leftmost decomposition | one-state domino recurrence plus position/state split for the optional square | PASS |
| `IOQM-2023-Q21` | 15 | partitions; monotone functions; represent monotone sequence as Ferrers/partition shape and separate maximal triangular baseline from residual | recurrence-not-forced contrast; residual/partition representation; baseline 2016 leaves residual 7 | PASS |
| `IOQM-2023-Q26` | 19 | restricted binary representations; coefficients `0,1,2`; process binary digits of 100 with carry state | carry-state DP / digit-state representation | PASS |

## Independent-answer verification join

All five anchors are `PASS`, `answer_verified_independently=true`, and `source_or_metadata_status=CLEAN` in the frozen verification ledger:

- `IOQM-2024-Q14 = 80`
- `IOQM-2024-Q20 = 10`
- `IOQM-2023-Q08 = 59`
- `IOQM-2023-Q21 = 15`
- `IOQM-2023-Q26 = 19`

No COMB-03 anchor is affected by the metadata-correction events recorded for other corpus items.

## Drift tests

The research package would fail this audit if any of the following occurred:

1. **owner drift** — an anchor is reassigned away from `IOQM-G9-COMB-03` without an authority update;
2. **answer drift** — a research/teacher artifact uses a value different from the verified answer;
3. **mechanism drift** — the package recasts an anchor around a mechanism not supported by the frozen ledger/source;
4. **boundary drift** — AP/GP/generic algebraic recurrence is retaught here instead of retrieved from ALG-04;
5. **counting-foundation drift** — addition/multiplication/complement/IE foundations are silently authored here before COMB-01 exports them;
6. **game drift** — adversarial strategy is introduced into deterministic state evolution rather than routed to COMB-04;
7. **representation inflation** — a recurrence is forced where a partition/residual or other simpler representation is the actual mechanism.

Current result: all seven drift tests PASS.

## Important wording control

For `IOQM-2024-Q20`, the corpus phrase “min steps 11 to121” is interpreted as “minimum number of steps from 11 to 121”; the verified numeric answer is 10. PR #95 keeps the problem endpoints separate from the step count and therefore does not inherit the ambiguous compact wording.

For `IOQM-2023-Q21`, the package deliberately does not force a recurrence. The frozen ledger itself identifies partition representation as the hidden invariant, so the representation-choice contrast is canonical rather than an extension beyond source authority.

## Promotion implication

`FROZEN_CORPUS_CONFORMANCE = PASS_STATIC`

This clears provenance/ownership drift as a blocker. The remaining blocker is still external and singular:

`COMB01_PRODUCTION_INTERFACE_NOT_LOCATED`

No integrated student prose is authorized until that provider interface passes `C01-1..C01-10` and `T1..T6` in `COMB01_Interface_Acceptance_Contract.md`.
