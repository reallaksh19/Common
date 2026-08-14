# Git and PR Policy

- Keep assignment work on one PR unless explicitly redirected.
- Establish current remote/base/HEAD/PR state before mutable claims.
- Prefer commits aligned with logical implementation stages.
- Keep implementation and corresponding report state synchronized where practical.
- Do not leave a commit whose report describes an older repository state.
- Do not merge unless explicitly instructed.
- Do not enable auto-merge unless explicitly instructed.
- Do not add or modify `.github/workflows/*` unless explicitly authorized.
- Do not force-push or rewrite shared history unless explicitly authorized and justified.
- Do not silently rebase a branch whose state another agent may rely on.
- Do not commit unrelated files, backup files, generated churn, or formatting-only changes outside scope.

Before PR completion compare the report's changed-file ledger to GitHub's actual changed-file list. Every discrepancy requires explanation or correction.
