# Golden example — TASK_RESULT

```text
TASK_RESULT

OUTCOME
ACHIEVED for the bounded child responsibility.
Parent programme remains open.

EXACT MATERIAL
- PR #235
- lifecycle: MERGED
- base: <sha>
- merged/current-main head: <sha>

CHANGED SURFACES
- tests/test_gates.py → bounded falsifier registration
- generated manifest → deterministic refresh

VALIDATION
- declared falsifier: PASS
- neighboring mutation: PASS
- generated freshness: PASS
- full discovery: FAIL only on independent sibling work

PROVED
- AC-F-01 PASS
- AC-F-02 PASS
- AC-F-03 PASS
- AC-F-04 PASS

NOT PROVED
- parent EXIT-P5
- sibling #233/#234

NEGATIVE ASSURANCE
No canonical subject truth, runtime, workflow or Relay authority changed.

CONSUMER CONSEQUENCE
#215 may consume this merged producer output now.

REMAINING CHILD ENGINEERING
NONE

NEXT
Route the result to #215; do not equate this child completion with programme completion.
```
