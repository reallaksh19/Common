# RLL-1 Codex local executor profile

## Status

This profile is an RLL-1 executor/scheduler implementation. It does not create engineering authority.

The governing invariant remains:

> V3.1 governs engineering authority. RLL-1 transports already-authorized execution. Git material truth outranks RLL operational state.

The existing RLL labels, worker-state comment, directives, \`BRANCH_RESUME\`, \`EXACT_HEAD_EVIDENCE\`, mutex, lease, review boundary, and merge/release rules are unchanged.

## Architecture

\`\`\`text
OS scheduler
  -> repository thin adapter
  -> Common rll_codex_worker.py
  -> deterministic RLL core from rll_worker.py
  -> git + gh provider/workspace preparation
  -> isolated codex exec engineering run
  -> deterministic path/postflight checks
  -> launcher-owned commit/push (BRANCH_RESUME only)
  -> launcher-owned TASK_EVIDENCE publication
  -> rll-review-ready
\`\`\`

Codex does not own RLL provider-control mutations.

## Codex invocation

The executor uses non-interactive \`codex exec\` with:

- \`--json\` for JSONL execution events;
- \`--output-schema\` plus \`-o\` for a deterministic terminal object;
- \`--ephemeral\`;
- \`--sandbox read-only\` for \`EXACT_HEAD_EVIDENCE\`;
- \`--sandbox workspace-write\` for authorized \`BRANCH_RESUME\`;
- \`approval_policy="never"\`;
- \`approvals_reviewer="user"\`;
- \`web_search="disabled"\`;
- \`sandbox_workspace_write.network_access=false\`.

The executor never uses \`--dangerously-bypass-approvals-and-sandbox\`.

The Codex terminal object is \`RLL_AGENT_RESULT_V1\`. It is internal agent evidence, not an engineering acceptance record. The deterministic launcher publishes durable \`TASK_EVIDENCE\` and maps the result to the canonical \`RLL_RUN_RESULT_V1\` transport state.

## Provider and credential boundary

The launcher owns:

- \`gh\` issue/PR reads needed for RLL;
- RLL labels;
- the singular \`RLL_WORKER_STATE_V1\` comment;
- durable evidence publication;
- Git fetch/branch/worktree preparation;
- postflight observation;
- authorized commit and push for \`BRANCH_RESUME\`.

The Codex engineering process MUST NOT:

- invoke \`gh\` or GitHub APIs;
- use GitHub MCP;
- receive \`GH_TOKEN\`, \`GITHUB_TOKEN\`, or equivalent environment variables;
- commit, push, rebase, merge, or mutate Git refs;
- merge/release/delete branches or change acceptance authority.

For stronger credential isolation, run Codex under a separate local OS user from the launcher/provider user. \`rll_codex_worker.py\` supports \`--codex-user\` for this split. The Codex user gets its own \`CODEX_HOME\`; the provider user's GitHub CLI credential store remains outside that user's home/permissions.

## Branch-write confinement

Codex \`BRANCH_RESUME\` envelopes require:

\`\`\`yaml
allowed_paths: path/one; path/two; directory/prefix
\`\`\`

The launcher refuses a Codex write job without this field.

After the agent returns, the launcher:

1. verifies HEAD did not move;
2. verifies every dirty path is inside \`allowed_paths\`;
3. runs \`git diff --check\`;
4. verifies the remote governed branch did not advance during execution;
5. commits the bounded work itself;
6. pushes without force;
7. re-observes exact Git truth;
8. publishes \`TASK_EVIDENCE\`.

A path escape, agent Git-head mutation, concurrent remote advance, rejected push, or dirty exact-head worktree escalates instead of being reconciled automatically.

## Exact-head evidence

\`EXACT_HEAD_EVIDENCE\` uses the existing dedicated detached RLL worktree plus Codex \`read-only\` sandboxing.

The run may reach \`REVIEW_READY\` only if:

- the exact declared head is unchanged;
- the worktree is clean;
- durable evidence was generated and published by the launcher.

Any tracked/untracked repository mutation is a sandbox failure and becomes \`ESCALATION_REQUIRED\`.

## Native Windows write restriction

As of September 2026, native-Windows Codex CLI has open reports where \`codex exec --sandbox workspace-write\` behaves effectively read-only even when workspace-write is requested.

Therefore RLL-1 Codex MUST fail closed for native-Windows \`BRANCH_RESUME\`.

The qualified migration path is:

- Windows may host the OS scheduler;
- WSL2/Linux runs the deterministic launcher and Codex write worker;
- a read-only smoke must pass first;
- a disposable Linux/WSL workspace-write smoke must prove actual in-workspace writes and out-of-scope confinement before production branch writes are enabled.

Do not work around a failed workspace-write smoke with unrestricted filesystem access.

## Approval reviewer restriction

Do not configure unattended RLL Codex with \`approvals_reviewer="auto_review"\`.

RLL uses \`approval_policy="never"\` and \`approvals_reviewer="user"\` while relying on the explicit sandbox as the execution boundary. A sandbox/approval mismatch is an environment failure, not permission to escalate.

## Scheduler

Do not depend on an LLM-native scheduler.

Use an OS-level scheduler to invoke the deterministic adapter every ten minutes:

\`\`\`text
*/10 minutes -> one launcher invocation
\`\`\`

On Windows, Task Scheduler may invoke a PowerShell adapter that calls the WSL/Linux worker. The existing atomic RLL mutex remains the same-machine serialization authority, so overlapping scheduler wakes are harmless.

## Authentication

Two identities are intentionally distinct when \`--codex-user\` is used:

1. **provider/launcher user**
   - native \`git\`;
   - \`gh auth login --web\`;
   - GitHub credential storage;
   - no token environment variables.

2. **Codex engineering user**
   - \`codex login\`;
   - dedicated \`CODEX_HOME\`;
   - repository read/write only as required by the sandbox and \`allowed_paths\`;
   - no GitHub credentials.

Never copy GitHub OAuth/PAT material into \`CODEX_HOME\`, prompts, transcripts, task files, or scheduler configuration.

## Failure classification

Examples:

- model quota/rate limit/network interruption -> \`RETRY_WAIT\`;
- missing Codex structured terminal output -> \`RETRY_WAIT\`;
- native Windows branch-write request -> \`RETRY_WAIT\` until Linux/WSL execution is available;
- path-confinement violation -> \`ESCALATION_REQUIRED\`;
- agent changed Git HEAD -> \`ESCALATION_REQUIRED\`;
- remote governed branch advanced during the run -> \`ESCALATION_REQUIRED\`;
- engineering tests fail truthfully -> engineering FAIL evidence; transport may still reach \`REVIEW_READY\` if the bounded evidence cycle is complete.

## Pilot sequence

1. Install a dedicated Codex execution identity/home.
2. Create a fresh open read-only smoke issue with \`worker: codex-local\`.
3. Run scheduler/launcher smoke without agent execution.
4. Enable Codex and prove \`EXACT_HEAD_EVIDENCE\` returns a clean unchanged worktree.
5. Prove overlapping scheduler wakes are rejected by the local mutex.
6. Create a disposable WSL/Linux branch-write smoke with explicit \`allowed_paths\`.
7. Prove Codex can edit only the authorized workspace and cannot move Git HEAD.
8. Prove launcher-owned commit/push and durable evidence publication.
9. Only then migrate an already-authorized production RLL task to \`worker: codex-local\`.

## Review and merge

\`rll-review-ready\` remains only a review boundary.

Independent V3.1 review is still required. Merge/release remains outside RLL and requires fresh direct Owner authority.
