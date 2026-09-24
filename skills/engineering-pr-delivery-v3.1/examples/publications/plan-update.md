# Golden example — PLAN_UPDATE

```text
PLAN_UPDATE — rev 2

CHANGED BECAUSE
Live source inspection showed the current test oracle is generated from canonical owner-extension records; the hard-coded expectation is the stale surface.

PREVIOUS ASSUMPTION
The expected owner-extension set could be patched directly.

NEW EVIDENCE
<exact source/test refs>

NEW APPROACH
Derive/audit the expected identity set from the canonical owner-extension records and preserve the non-curriculum-authority invariant.

UNCHANGED
- owned child outcome
- canonical source authority
- consumer contract
- parent mapping
- negative authority test

EXPECTED NEXT OBSERVABLE
Exact source-derived identity set + focused negative-authority test result.
```
