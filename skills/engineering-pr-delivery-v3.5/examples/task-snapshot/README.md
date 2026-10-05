# Task Snapshot golden cases

These are canonical **reporting examples**, not engineering authority.

Use the structured JSON cases with `scripts/render_task_snapshot.py`.

## Cases

### `review-ready-parent-open.json`

Use when implementation is complete on a review-ready/unmerged PR but a child criterion or programme criterion remains open.

Expected interpretation:

```text
#215 PARTIAL
implementation complete
delivery REVIEW_READY / UNMERGED
child acceptance PARTIAL
programme contribution PARTIAL
sibling failure origin is explicit
```

Never summarize this as simply "Done".

### `merged-child-parent-open.json`

Use when the bounded child is technically delivered and merged but its parent programme is still open.

Expected interpretation:

```text
#232 COMPLETE
child acceptance SATISFIED
delivery MERGED
provider issue may still be OPEN
programme contribution PARTIAL
```

### `not-run-infrastructure.json`

Use when material review is strong but required executable validation never ran.

Expected interpretation:

```text
#302 PARTIAL
verification PARTIAL
certification NOT_RUN
reason INFRASTRUCTURE
delivery DRAFT
no code-failure claim
```

`NOT_RUN` must never be rewritten as `FAIL`.

### `active-task.json`

Normal in-progress engineering with a real acceptance denominator.

### `complete-task.json`

All mapped plan/task/child/programme criteria are satisfied and delivery is merged.

## Rules demonstrated

- implementation != verification;
- verification != delivery;
- child completion != programme completion;
- provider issue state != engineering completion;
- sibling/pre-existing/infrastructure failures remain separately attributed;
- percentages appear only from a real criterion/weight denominator;
- missing denominator renders `UNKNOWN`, never an invented percentage.
