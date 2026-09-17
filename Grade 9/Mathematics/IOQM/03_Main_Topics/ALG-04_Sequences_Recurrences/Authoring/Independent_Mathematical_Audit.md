# ALG-04 — Independent Mathematical Audit

Status: `PASS_STATIC_SECOND_ROUTE`

Purpose: recompute the mathematics after the teaching draft was frozen. This audit is separate from the explanatory routes in the student book. It is a static mathematical/source check, not classroom or psychometric evidence.

## Historical anchor A — IOQM-2025-Q26

Frozen mechanism:
- increasing 4-term averages -> `a_{i+4}>a_i`;
- decreasing 7-term averages -> `a_{i+7}<a_i`.

### Upper bound at 11 terms

For 11 terms, chain the required strict inequalities:

`a_1<a_5<a_9<a_2<a_6<a_10<a_3<a_7<a_11<a_4<a_8<a_1`.

This is impossible because it gives `a_1<a_1`.

Hence length `11` is impossible.

### Independent length-10 construction

Take

`(a_1,...,a_10)=(2,5,8,0,3,6,9,1,4,7)`.

Check 4-shifts:
- `a_5>a_1`: `3>2`;
- `a_6>a_2`: `6>5`;
- `a_7>a_3`: `9>8`;
- `a_8>a_4`: `1>0`;
- `a_9>a_5`: `4>3`;
- `a_10>a_6`: `7>6`.

Check 7-shifts:
- `a_8<a_1`: `1<2`;
- `a_9<a_2`: `4<5`;
- `a_10<a_3`: `7<8`.

Therefore length 10 exists and length 11 does not.

Independent answer: `10`.

Matches final official/verified authority: PASS.

## Historical anchor B — IOQM-2023-Q10

Validated paper data:
- `a_0=1`;
- `a_1=-4`;
- `a_{n+2}=-4a_{n+1}-7a_n` for `n>=0`;
- target: divisor count of `a_50^2-a_49a_51`.

Define

`D_n=a_n^2-a_{n-1}a_{n+1}`.

For a general recurrence
`a_{n+2}=p a_{n+1}+q a_n`,

`D_{n+1}=-qD_n`.

Here `q=-7`, so
`D_{n+1}=7D_n`.

Compute only the initial invariant:
`a_2=-4(-4)-7(1)=9`.

Thus:
`D_1=(-4)^2-(1)(9)=7`.

Therefore:
`D_50=7^50`.

A prime power `7^50` has `50+1=51` positive divisors.

Independent answer: `51`.

Matches embedded historical key and 90Q verification authority: PASS.

## Author-created numerical audit

| Item | Independent result | Check |
|---|---|---|
| Practice 1 | 46 | AP direct recomputation |
| Practice 2 | 384 | GP direct recomputation |
| Practice 3 | `a_n=2n` | exact finite difference |
| Practice 7 | `20/21` | exact telescope |
| Practice 9 | `a_n=4n-3` | exact finite difference |
| Practice 10 | `a_8=3281` | recurrence iteration cross-check + difference GP |
| Practice 11 | `(n-1)/n` | exact telescope |
| Practice 14 | `D_20=7^19`, divisor count 20 | invariant + exact initial value |
| Practice 15 | `a_n=2T_{n-1}+2` | algebraic subtraction |
| Practice 16 | `n/(2n+1)` | exact partial fractions |
| Practice 17 | `a_10=1535` | exact recurrence iteration cross-check |
| Practice 18 | `a_99=4` | period-4 residue |
| Practice 19 | `3n^2-3n+1` | exact finite difference |
| Practice 21 | `10n-4` | exact finite difference |
| Practice 23 | `1/2-1/n` | exact telescope |
| Practice 26 | layer cost `n` | exact finite difference |
| Practice 27 | ratio `-3` | general invariant |
| H0 5 | `8n-3` | exact finite difference |
| H0 6 | `a_8=16384` | recurrence iteration cross-check |
| H0 7 | `50/51` | exact telescope |
| H0 8 | `a_99=4` | period-4 residue |
| H0 9 | divisor count 20 | invariant cross-check |
| H0 14 | `Q_{n+1}=-3Q_n` | symbolic invariant derivation |

## Identity audit

Verified algebraically:
- `1/[k(k+1)]=1/k-1/(k+1)`;
- `1/[k(k-1)]=1/(k-1)-1/k`;
- `1/[(2k-1)(2k+1)]=(1/2)[1/(2k-1)-1/(2k+1)]`;
- for `a_{n+2}=p a_{n+1}+q a_n`,
  `D_{n+1}=-qD_n`;
- equal adjacent `k`-term windows imply `a_{i+k}=a_i`;
- strictly increasing adjacent `k`-term windows imply `a_{i+k}>a_i`.

## Verification audit for explicit recurrence formula

For
`a_n=3*2^(n-1)-2`:
- initial values give `a_1=1,a_2=4`;
- symbolic substitution satisfies
  `a_{n+2}=3a_{n+1}-2a_n`
  for every allowed `n`.

PASS.

## Source/provenance audit

- `IOQM-2025-Q26`: clean official historical source; final official answer 10; independent upstream verification PASS.
- `IOQM-2023-Q10`: clean validated historical source; embedded key 51; exact paper initialization checked; independent upstream verification PASS.
- No metadata-correction overlay event applies.
- No COMB-03 anchor is relabelled as ALG-04 primary evidence.
- All non-historical exercises are author-created.

## Evidence boundaries

- static mathematical correctness: PASS;
- source/key join: PASS;
- classroom timing/readability observation: NOT_RUN;
- longitudinal retention: NOT_RUN;
- psychometric difficulty/discrimination: NOT_RUN;
- publication approval: NOT_RUN.
