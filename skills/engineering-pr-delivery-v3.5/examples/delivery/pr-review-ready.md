# Golden example — PR delivery state

```text
PR DELIVERY

Work issue: #215
PR: #237
Lifecycle: REVIEW_READY
Merged: NO
Mergeability: MERGEABLE
Base: main@<sha>
Head: <sha>

Exact-head verification:
- joined browser oracle: PASS / CURRENT_TASK
- generated freshness: PASS / CURRENT_TASK
- full discovery: FAIL / SIBLING_WORKSTREAM (#233, #234)

Child acceptance:
5/6 satisfied — 83.3% unweighted coverage

Programme contribution:
4/5 satisfied — 80% unweighted coverage

Interpretation:
The PR is review-ready engineering material. The child and programme are not complete.
```
