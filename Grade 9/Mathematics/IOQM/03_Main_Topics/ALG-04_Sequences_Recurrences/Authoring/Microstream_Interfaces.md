# ALG-04 — Wave-1 Microstream Interfaces

Authoring-only.

## A. AP/GP recognition
- AP invariant: first difference constant;
- GP invariant: ratio constant where terms are nonzero;
- misconception: choosing a formula from surface wording.

## B. Term vs partial sum
- canonical identity: `a_n=S_n-S_{n-1}` for `n>=2`, with `a_1=S_1`;
- first move: identify whether the symbol is a term or accumulated sum.

## C. Recurrence reading
- recurrence gives a dependency, not necessarily the cheapest computation route;
- first move: write two adjacent-index copies and compare.

## D. Window differences
- if `W_i=a_i+...+a_{i+k-1}`, then `W_{i+1}-W_i=a_{i+k}-a_i`;
- same for averages after multiplying by fixed window length;
- key anchor: `IOQM-2025-Q26`.

## E. Telescoping
- clue: factors like `k(k+1)` or consecutive denominators;
- first move: partial-fraction into consecutive differences;
- invariant: internal terms cancel, leaving boundaries.

## F. Sequence invariants
- clue: recurrence with products/squares/symmetric neighboring terms;
- first move: compute the candidate combination at adjacent indices, not many raw terms;
- anchor: `IOQM-2023-Q10`.

## G. Source audit
- both primary anchors independently verified;
- no metadata correction overlay required.

## Lead integration rule

Do not organize the student book as “AP chapter, GP chapter, recurrence chapter...” with repeated onboarding. Repeatedly use one question: **what local comparison cancels the most?**
