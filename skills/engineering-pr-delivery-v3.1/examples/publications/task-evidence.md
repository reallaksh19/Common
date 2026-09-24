# Golden example — TASK_EVIDENCE

```text
TASK_EVIDENCE

OBSERVED AT
<timestamp>

EXACT HEAD / BASIS
PR #304 @ <head>
base main@<sha>

CLAIM
The post-hydration rollback evidence gap is closed, but executable certification has not run.

EVIDENCE
- regression test ref
- hosted jobs: steps=null / no logs
- local checkout attempt: repository unavailable

RESULT
PARTIAL

VERIFICATION
- rollback regression: PASS / CURRENT_TASK
- hosted certification: NOT_RUN / INFRASTRUCTURE
- local certification: NOT_RUN / INFRASTRUCTURE

CONSEQUENCE
No further product-code change is justified yet.

DEPENDENCY DISCOVERED
Execution-capable checkout / runner.

PLAN CONSEQUENCE
NONE

EXPECTED NEXT OBSERVABLE
Exact-head certification executes or exposes the first task-owned executable defect.
```
