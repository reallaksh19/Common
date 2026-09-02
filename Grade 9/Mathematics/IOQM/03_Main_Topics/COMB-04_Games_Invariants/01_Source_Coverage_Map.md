# COMB-04 Source Coverage Map

Status: `WAVE0_SOURCE_SET_FROZEN`

## Governing source / verification authority

- 90Q corpus ledger: `Grade 9/Mathematics/IOQM/01_Corpus/IOQM_2023_2025_90Q_Ledger_v1.csv`, blob `11750884227b9205615a46cce011d7f1ee754be0`.
- answer-verification ledger: `.../Verification/IOQM_2023_2025_Answer_Verification_Ledger_v1.csv`, blob `67ef9d3d47e3964620b8136d226718e3d5c495e5`.
- independent verification batch C: `.../Verification/IOQM_Independent_Answer_Verification_Batch_C_Q21_Q30_v1.md`, blob `d127a93352add0bbe1366177b26da4e87d95936e`.
- source-provenance rules remain governed by the IOQM architecture; historical IDs and exact figures/wording remain source-controlled.

## Primary historical anchors

| Stable ID | Source/key authority | Verified answer | COMB-04 role | Figure custody | Verification |
|---|---|---:|---|---|---|
| `IOQM-2025-Q22` | HBCSE official paper + final official key | 66 | impartial adversarial game; backward W/L classification | no | independent batch C PASS |
| `IOQM-2025-Q25` | HBCSE official paper + final official key | 36 | parity/exponent obstruction + recursive construction | no | independent batch C PASS |
| `IOQM-2023-Q28` | HBCSE-linked MTAI paper with embedded key | 67 | triangular-grid toggle reachability; mod-2/colour invariant | **yes — source controlled** | independent batch C PASS |

### `IOQM-2025-Q22`

Corpus mechanism: impartial game / winning states.  
Visible structure: remove-one-marble play with last-red win condition.  
First authoring route: define terminal outcomes and evaluate states backward; do not infer strategy from a single sample path.  
Frozen answer: `66`.

### `IOQM-2025-Q25`

Corpus mechanism: pairing invariant; parity; perfect-square product.  
Independent verification route: `n=1` impossible; constructions for `n=2,3`; if a construction exists for `n`, pair the four new numbers as `(2n+1,2n+4)` and `(2n+2,2n+3)`, yielding equal added sums and hence a square factor; therefore all `2<=n<=37` work, i.e. `36` values.  
Frozen answer: `36`.

### `IOQM-2023-Q28`

Corpus mechanism: invariant game / linear algebra mod 2.  
Independent verification route: model triangle flips over `F_2`; the dual unit-triangle equations force a period-3 vertex pattern; the all-heads to all-tails target is compatible iff `3` does not divide `n`; among `1<=n<=100`, this gives `100-floor(100/3)=67`.  
Frozen answer: `67`.

Historical diagram/figure custody remains with the validated source. Learner-created variants may use newly authored diagrams, but must not silently reproduce/relabel the official figure as an exact source image.

## Topic/source use rules

- Historical question ID stays `IOQM-YYYY-QNN`.
- Promoted historical answer must remain tied to verification authority.
- Author-created examples receive no historical ID.
- Exact source figures and wording are not reconstructed from memory and labelled as exact.
- Secondary COMB/NT/GEO tags are transfer/navigation evidence, not official topic-weightage claims.
- The 90-question corpus does not establish official IOQM topic weightage.

## Downstream source-design targets

Wave 1 source audit must produce:

1. exact anchor-to-mechanism mapping;
2. independent mathematical trace for every promoted historical anchor;
3. explicit necessary/sufficient distinction for invariant reachability;
4. figure/source-integrity check for 2023-Q28;
5. at least one changed-surface transfer per major mechanism;
6. provenance labels for every author-created item.

## Evidence-state boundary

`SOURCE_IDS_VERIFIED: PASS_STATIC`  
`PROMOTED_HISTORICAL_ANSWERS: PASS_STATIC`  
`SOURCE_KEY_MISMATCHES: 0`  
`CLASSROOM_TIMING_READABILITY: NOT_RUN`  
`RETENTION: NOT_RUN`  
`PSYCHOMETRICS: NOT_RUN`  
`QUALIFICATION_PROBABILITY: NOT_RUN`  
`PERCENTILE_PASS_MARK_CALIBRATION: NOT_RUN`  
`PUBLICATION_APPROVAL: NOT_RUN`

`WAVE0_SOURCE_SET_FROZEN`