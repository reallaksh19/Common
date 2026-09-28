# RLL_CODEX_LOCAL_BLUEPRINT_V1

Use this blueprint when a V3.1 agent needs to stage or migrate unattended local execution to **RLL-1 + CODEX_LOCAL_V1**.

This blueprint is reusable across repositories. It defines transport topology, security boundaries, smoke gates, machine contract, execution envelopes, and review/authority boundaries. It does not create engineering scope, Owner approval, merge authority, release authority, or acceptance criteria.

Canonical references:

- `skills/engineering-pr-delivery-v3.1/SKILL.md`
- `skills/engineering-pr-delivery-v3.1/operating-model/transports/RLL-1.md`
- `skills/engineering-pr-delivery-v3.1/templates/plan-for-local-agent.md`

## 1. Use this blueprint when

This blueprint is **conditional**, not an automatic replacement for repository-local protocol.

First inspect the target repository's existing V3.1 local-agent/RLL implementation.

Use this blueprint to scaffold or repair the missing delta when all relevant conditions are true:

- V3.1 is the live engineering coordination/recording protocol;
- the engineering task is already bounded by an issue/plan/Owner decision;
- unattended local execution is desired;
- Codex is the selected or explicitly requested executor;
- the existing repository protocol is absent, stale/incompatible, or missing one or more required CODEX_LOCAL_V1 invariants;
- provider control must remain deterministic and outside the model process;
- source-writing execution, when required, can run under WSL2/Linux or another qualified Linux environment.

If the repository already has a current compatible Codex/RLL protocol satisfying this blueprint's invariants, **reuse it**. In that case the blueprint is a conformance checklist and should not create duplicate scripts, schedulers, state machines, labels, or authority.

Do not use this blueprint to invent engineering scope, force an executor migration, replace compatible repository-specific integration, or bypass an Owner/governance decision.

## 2. Canonical invariant

> V3.1 governs engineering authority. RLL-1 transports already-authorized execution. CODEX_LOCAL_V1 performs bounded repository engineering only. Git material truth outranks RLL operational state. Merge/release remains outside RLL.

## 3. Required inputs

Resolve these before instantiation:

```yaml
protocol:
  relay: V3.1
  common_sha: <current-or-approved Common SHA>
  two_pass_revision: <revision>

repository:
  name: <owner/repo>
  main_sha: <current main SHA>
  governing_issue: <issue number>
  owned_branch: <branch|null>
  exact_head: <sha|null>
  approved_base: <sha>

engineering:
  purpose: <bounded owned outcome>
  source_truth:
    - <source path / issue / PR / artifact>
  first_falsifier_or_reason: <text>
  protected:
    - <must not change>
  validation:
    - <required engineering evidence>

owner_authority:
  source_write_authorized: true|false
  merge_authorized: false
  release_authorized: false
```

If the engineering contract is not recoverable, stop and repair the V3.1 issue/plan first.

## 4. Blueprint output contract

A V3.1 agent using this blueprint should produce one instantiated object:

```yaml
schema: rll-codex-local-blueprint/v1

protocol_basis:
  relay: V3.1
  common: <sha>
  two_pass: <revision>

repository:
  name: <owner/repo>
  main: <sha>
  governing_issue: <number>

adapter:
  status: PRESENT_CURRENT | PRESENT_STALE | ABSENT
  action: REUSE | UPDATE | SCAFFOLD
  required_common_basis: <sha>
  consumer_files:
    rule: .agents/rules/rll-1.md
    worker: scripts/rll1-codex-worker.ps1
    installer: scripts/install-rll1-codex-task.ps1
    docs: docs/RLL1_CODEX_LOCAL_AUTOMATION.md
    source_guard: <path|null>

executor:
  worker_id: codex-local
  common_launcher: skills/engineering-pr-delivery-v3.1/scripts/rll_worker.py
  executor: codex
  host_scheduler: WINDOWS_TASK_SCHEDULER
  write_runtime: WSL2_LINUX
  codex_user: <dedicated local user>
  codex_home: <dedicated CODEX_HOME>

security:
  github_mcp: false
  codex_provider_access: false
  codex_github_credentials: false
  github_token_env: forbidden
  web_search: disabled
  workspace_network: disabled
  approval_policy: never
  approvals_reviewer: user
  dangerous_sandbox_bypass: forbidden
  launcher_owns_provider_state: true
  launcher_owns_git_refs: true
  launcher_owns_commit_push: true

execution:
  mode: BRANCH_RESUME | EXACT_HEAD_EVIDENCE
  local_execution_request: <V3.1-LOCAL_EXECUTION-request-id|null>
  branch: <branch|null>
  head_sha: <sha|null>
  base_sha: <sha>
  material_write: true|false
  allowed_paths:
    - <repository-relative path>
  commit_message: <launcher-owned message|null>

engineering_contract:
  purpose: <bounded outcome>
  first_falsifier_or_reason: <text>
  protected:
    - <invariant>
  validation:
    - <required command/evidence>
  return_contract: <typed engineering evidence>

activation:
  fresh_smoke_issue_required: true
  scheduler_cadence_minutes: 10
  smoke_mode_first: true
  exact_head_smoke_required: true
  branch_write_smoke_required: <true for source-writing use>
  source_write_enable_after: <all required smoke gates pass>
  ready_label_after: <condition>

stop_conditions:
  - exact-head mutation
  - Codex moves Git HEAD
  - changed path outside allowed_paths
  - native-Windows BRANCH_RESUME
  - remote governed branch advances during Codex execution
  - GitHub/provider credentials visible to Codex
  - required protected-surface change
  - engineering scope requires new Owner authority

merge_release_authority: false
```

For `EXACT_HEAD_EVIDENCE`, `allowed_paths` is empty and material writes are false.

For Codex `BRANCH_RESUME`, `allowed_paths` is mandatory.

### 4.1 V3.1 local-execution correlation

When the repository has a native V3.1 `LOCAL_EXECUTION_EXPORT` for the bounded work, that generated packet is the canonical derived recipient contract. Do not create a parallel `TASK.md` or RLL-specific engineering task specification.

Record the generated `request.id` as `local_execution_request` in `RLL_EXECUTION_V1`. The deterministic launcher must propagate that correlation into executor context and `TASK_EVIDENCE`. The correlation does not create authority and does not replace the governing issue/programme, approved plan, exact Git material truth, or independent review.

If no native V3.1 local-execution packet exists, `local_execution_request` may be null and the existing issue/plan reconstruction path remains valid.

## 5. Machine topology

The preferred topology is:

```text
Windows Task Scheduler
  |
  | every 10 minutes
  v
thin consumer PowerShell wrapper
  |
  v
WSL2/Linux provider/launcher identity
  |-- git
  |-- gh / OS credential store
  |-- Common rll_worker.py --executor codex
  |
  +--> dedicated Codex OS identity
         |-- dedicated CODEX_HOME
         |-- codex exec
         |-- repository worktree access only
         |-- no GitHub credential store
         |-- no provider-control authority
```

The deterministic launcher owns:

- issue discovery;
- local mutex;
- GitHub lease/state;
- directive filtering;
- repository/worktree preparation;
- durable issue context retrieval;
- Codex invocation;
- Git postflight;
- changed-path confinement;
- launcher-owned commit/push for authorized branch writes;
- durable `TASK_EVIDENCE` publication;
- RLL labels/state.

Codex owns only bounded repository inspection/edit/test reasoning.

## 6. Codex execution policy

Use non-interactive `codex exec`.

Required policy shape:

```text
--json
--output-schema <schema>
--output-last-message <file>
--sandbox read-only|workspace-write
approval_policy="never"
approvals_reviewer="user"
web_search="disabled"
sandbox_workspace_write.network_access=false
```

Never use a dangerous approval/sandbox bypass.

The launcher removes these from the Codex environment:

```text
GH_TOKEN
GITHUB_TOKEN
GH_ENTERPRISE_TOKEN
GITHUB_ENTERPRISE_TOKEN
```

The prompt must tell Codex:

- durable GitHub issue context has already been supplied;
- do not invoke `gh`;
- do not call GitHub APIs;
- do not use GitHub MCP;
- do not use network/web research;
- do not inspect provider credentials;
- do not commit, push, rebase, merge, or mutate Git refs;
- do not infer Owner authority;
- preserve truthful PASS/FAIL/BLOCKED/NOT_RUN semantics.

## 7. Execution-envelope templates

### 7.1 Read-only exact-head evidence

```text
RLL_EXECUTION_V1

transport: RLL-1
worker: codex-local
local_execution_request: <V3.1-LOCAL_EXECUTION-request-id|null>
mode: EXACT_HEAD_EVIDENCE
repository: <owner/repo>
head_sha: <exact-candidate-sha>
base_sha: <comparison-base-sha>
allow_material_write: false
```

Use for diagnostics, certification, reproduction, and immutable-head validation.

Required postflight:

- HEAD equals the declared SHA;
- tracked/untracked repository state is clean;
- Codex returned valid structured output;
- launcher published durable evidence;
- no provider/Git-ref mutation occurred inside Codex.

### 7.2 Governed branch implementation

```text
RLL_EXECUTION_V1

transport: RLL-1
worker: codex-local
local_execution_request: <V3.1-LOCAL_EXECUTION-request-id|null>
mode: BRANCH_RESUME
repository: <owner/repo>
branch: <governed-branch>
base_sha: <approved-base-sha>
allow_material_write: true
allowed_paths: <path/one>; <path/two>; <directory/prefix>
commit_message: <bounded launcher-owned commit message>
```

Use only when source-writing execution is already authorized.

Codex may edit/test only.

On `REVIEW_READY`, the launcher must:

1. verify Codex did not move HEAD;
2. verify every changed path is under `allowed_paths`;
3. run `git diff --check`;
4. stage the bounded changes;
5. commit with the authorized/default launcher-owned message;
6. verify the remote governed branch has not advanced;
7. push without force;
8. re-observe exact Git truth;
9. publish durable evidence.

## 8. Consumer-repository adapter blueprint

Keep the consumer adapter thin.

### `.agents/rules/rll-1.md`

Must state:

- V3.1 remains authority;
- RLL is transport only;
- `BRANCH_RESUME` resumes Git truth;
- `EXACT_HEAD_EVIDENCE` is immutable;
- no merge/release/branch deletion/acceptance weakening;
- no GitHub MCP;
- Codex must not use `gh`/GitHub APIs/provider control;
- Git refs/evidence/commit/push belong to the deterministic launcher.

### `scripts/rll1-codex-worker.ps1`

Should:

- refuse GitHub token env variables;
- require WSL for qualified source-write execution;
- verify required Common basis is an ancestor of the Common checkout;
- invoke Common `rll_worker.py --executor codex`;
- pass `--codex-user` and `--codex-home`;
- support smoke mode;
- not contain merge/release commands.

### `scripts/install-rll1-codex-task.ps1`

Should:

- verify WSL, Python, git, gh, Codex, sudo;
- verify provider `gh auth status`;
- verify dedicated Codex identity/login;
- verify required Common basis;
- create/update the four RLL labels;
- refuse completed/review-ready pilot reuse;
- install a branch-independent wrapper outside the governed checkout;
- create a 10-minute Windows Scheduled Task;
- default to smoke mode;
- require explicit enablement after smoke review;
- persist no GitHub token.

### `docs/RLL1_CODEX_LOCAL_AUTOMATION.md`

Should document:

- topology;
- identity split;
- Common basis;
- WSL paths;
- authentication;
- smoke/install commands;
- execution envelopes;
- `allowed_paths`;
- failure classification;
- rollback;
- merge/release boundary.

### Source guard

A repository-specific source guard should assert at minimum:

- Common basis pin;
- `rll_worker.py --executor codex`;
- WSL usage for writes;
- dedicated Codex user/home;
- 10-minute scheduler;
- no GitHub MCP;
- token-free scheduled runner;
- no dangerous sandbox bypass;
- no merge command;
- `allowed_paths` documented for branch writes.

## 9. Smoke and promotion sequence

Never enable production source-writing execution first.

Required sequence:

```text
A. adapter/source-guard validation
   -> PASS

B. fresh open RLL smoke issue
   -> worker: codex-local
   -> no prior REVIEW_READY/CANCELLED history

C. deterministic smoke
   -> issue discovery
   -> mutex
   -> singular worker-state mutation
   -> no Codex invocation yet

D. read-only Codex smoke
   -> EXACT_HEAD_EVIDENCE
   -> valid structured output
   -> unchanged exact head
   -> clean tree
   -> launcher-owned TASK_EVIDENCE
   -> rll-review-ready

E. overlap smoke
   -> simultaneous scheduler wake
   -> second process loses to mutex

F. disposable WSL/Linux write smoke
   -> BRANCH_RESUME
   -> one harmless allowed path
   -> Codex edit succeeds
   -> out-of-scope edit is rejected
   -> Codex cannot move Git HEAD
   -> launcher owns commit/push
   -> evidence published

G. production activation
   -> repin consumer adapter to merged/current Common basis
   -> replace paused legacy executor envelope with codex-local
   -> add rll-ready only after all required smoke gates pass
```

Do not reuse a completed smoke issue.

## 10. Failure classification

Use transport and engineering failure domains separately.

### Transport `RETRY_WAIT`

Examples:

- Codex quota/rate limit;
- temporary model/network/runtime interruption;
- missing local prerequisite;
- Codex authentication unavailable;
- source-write requested on native Windows;
- structured output unavailable because of a transient runtime condition.

### Transport `ESCALATION_REQUIRED`

Examples:

- Codex changes Git HEAD;
- changed path escapes `allowed_paths`;
- exact-head worktree becomes dirty;
- remote governed branch advances during the run;
- launcher/provider reconciliation would require reset/rebase/force;
- provider credential isolation is broken;
- a protected surface must change.

### Engineering result

Engineering tests may truthfully return:

```text
PASS
FAIL
BLOCKED
NOT_RUN
NOT_APPLICABLE
```

A truthful engineering FAIL may still produce transport `REVIEW_READY` when the bounded evidence cycle is complete.

## 11. Review boundary

`rll-review-ready` is never acceptance.

Coordinator review must:

1. refresh live V3.1 basis;
2. re-read issue/plan/Owner authority;
3. inspect exact Git material/evidence;
4. independently classify engineering result;
5. stage another bounded task only if no new authority is required;
6. stop for explicit Owner/governance authority when acceptance definitions, frozen baselines, merge, release, or other protected decisions would change.

## 12. Migration from another executor

When replacing Antigravity or another local executor:

```text
existing engineering task
  -> preserve engineering authorization
  -> remove/withhold rll-ready
  -> publish RELAY_DIRECTIVE_V1 / PAUSE
  -> implement Common Codex profile
  -> implement thin consumer adapter
  -> complete read-only + write smoke
  -> post new codex-local execution envelope
  -> restore rll-ready
  -> resume branch/exact-head from Git truth
```

Use only the normative `RELAY_DIRECTIVE_V1` control surface for transport pause/resume. Do not invent a separate `RLL_TRANSPORT_PAUSE` object.

Do not restart or discard legitimate engineering material merely because the executor changed.

## 13. Agent instantiation algorithm

When a V3.1 agent receives **"Plan for local agent"** and Codex may be relevant:

1. refresh current V3.1/Common/Two-Pass basis;
2. reconstruct the governing engineering contract;
3. discover the repository's existing local-agent/RLL protocol and classify it as `PRESENT_CURRENT_COMPATIBLE`, `PRESENT_CURRENT_NEEDS_BLUEPRINT_DELTA`, `PRESENT_STALE_OR_INCOMPATIBLE`, or `ABSENT`;
4. if `PRESENT_CURRENT_COMPATIBLE`, reuse it and use this blueprint only as a conformance checklist;
5. otherwise identify the smallest missing Codex/RLL delta this blueprint must supply;
6. determine whether `EXACT_HEAD_EVIDENCE` or `BRANCH_RESUME` truthfully fits;
7. fill `rll-codex-local-blueprint/v1` only for the selected/repaired Codex path;
8. when native V3.1 `LOCAL_EXECUTION_EXPORT` is available, resolve/export its current request and bind `request.id` as `local_execution_request`;
9. stage/update the thin adapter only when required and authorized;
10. create a fresh smoke issue when activation/smoke is required;
11. publish the matching `RLL_EXECUTION_V1` envelope;
12. install/validate smoke-first activation;
13. do not start source-writing execution unless that engineering write is already authorized;
14. do not infer executor migration authority from the keyword alone;
15. do not merge/release without fresh direct Owner authority.

## 14. Invariant

> Standardize the executor and transport aggressively; preserve engineering authority conservatively.
