# IOQM 2023–2025 — Metadata Correction Overlay v1

Status: `ACTIVE_UNTIL_DETAILED_LEDGER_REGENERATED`

This file corrects **repository metadata extraction/classification strings only**. It does not alter the historical papers or answer keys.

## IOQM-2023-Q04

### Stale classifier metadata

The first-pass ledger flattened the printed exponent and represented the relation as though it contained `x/4`.

### Validated paper statement used for verification

The relevant relation contains:

`x^4 = (x-1)(y^3-23) - 1`.

### Independent check

`x^4+1=(x-1)(y^3-23)`. Reducing modulo `x-1` gives `x-1 | 2`; the admissible positive-integer case is `x=3,y=4`, hence answer `07`.

### Disposition

- historical source: CLEAN;
- answer: independently verified;
- repository classifier metadata: correction required;
- source-conflict flag: **do not use**.

## IOQM-2025-Q28

### Stale classifier metadata

The first-pass ledger flattened the nested radical into a difference of simple radicals.

### Validated paper statement used for verification

`√(x - √(x+a)) = √a - y`.

### Independent check

The radical/domain structure forces `y=0`; then with `t=√(x+a)=x-a`, one obtains `a=t(t-1)/2`. The largest admissible nonsquare `a<100` is obtained at `t=14`, giving `a=91`.

### Disposition

- historical source: CLEAN_OFFICIAL;
- answer: independently verified;
- repository classifier metadata: correction required;
- source-conflict flag: **do not use**.

## Consumption rule

Until `IOQM_2023_2025_90Q_Ledger_v1.csv` is regenerated from exact validated stems, any agent or tool using either ID must consult:

1. the official/validated paper;
2. this overlay;
3. the independent-answer verification ledger.

Do not silently rewrite historical source custody because a repository extraction string was wrong.