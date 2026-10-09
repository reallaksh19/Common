# Common Relay — Buddy Runner Markdown message transport

**Issue:** [Common #889](https://github.com/reallaksh19/Common/issues/889)
**Status:** R1 transport implementation candidate, not a completed controlled successor experiment.
**Scope:** existing Engineering Relay V3.2 transaction recorder, responsibility-scoped Markdown messages. This directory is an operational message *location*, not an independent acceptance/progress system.

## Why this is in relay/

The Owner wants **Relay-operated communication in Markdown**, not hand-pasted chat prompts or loose prompt files. A message here is a durable source record with a native `relay/TRANSACTIONS/TX.<issue>.<serial>/manifest.yaml` when published through the sanctioned transaction operation.

The file path and Markdown header communicate meaning to humans and agents. They **do not** authenticate the author, prove Runner tool blindness, accept Task Evidence, grant source-write permission, or update task progress. GitHub publication/readback must be checked separately after local transaction completion.

## Initial R1 operation — publish immutable Markdown

Example for a responsibility governed by issue #889:

~~~bash
python skills/engineering-pr-delivery-v3.2/scripts/relay_tx.py . buddy-message \
  --issue-number 889 \
  --tx-id TX.889.1 \
  --stage STAGE1_INTAKE \
  --actor relay-operator \
  --markdown /path/to/approved-intake.md
~~~

**Output:** `relay/BUDDY_RUNNER/ISSUE-889/messages/TX.889.1-STAGE1_INTAKE.md` with the native transaction `relay/TRANSACTIONS/TX.889.1/manifest.yaml` containing the message SHA-256, original actor claim and atomic/recoverable operation record. The command rereads the resulting Markdown bytes and prints its digest. The caller must commit/publish both through the existing authorized Git provider route, then independently read back the exact ref. Local `COMMITTED` is not remote receipt.

- Explicit `TX.<issue>.<serial>` prevents accidentally inheriting the old `relay/STATE.yaml` currently associated with #438.
- Only validated stages are allowed: `READINESS`, `STAGE1_INTAKE`, `DISPATCH_REQUEST`, `DISPATCH_OBSERVATION`, `STAGE1_BASELINE`, `STAGE1_PLAN`, `TECHNICAL_HANDOVER`, `STAGE2_RECONCILIATION`, `CONTINUATION_EVIDENCE`.
- A transaction never overwrites an existing message; corrections require a **new** transaction with a new receipt and an explicit reference to the earlier record.
- `relay/STATE.yaml`, `relay/EVENTS.jsonl`, `relay/LEASES/`, `relay/ROADMAP/`, `relay/GENERATED/`, accepted evidence and P/E/D are **not modified**.
- If a transaction is interrupted, use the existing `relay_tx.py . recover` command and inspect the resulting actual receipt. Do not blindly retry the same TX ID or duplicate the message.

## No-repeat dispatch gate — lessons from the Core1B Stage 1 stall

**Observed negative example:** The Core1B Stage 1 packet in `relay/CORE1B_GOLDENS_RUNNER_20261009/STAGE1_RUNNER_INPUT.md` was verified at Common commit `aa1c1f2fc40dfbfb6bbaf47b1847977ad171cb99` (file blob `8746fb911f5f5d63a82e459e5439b2033b7017f1`); nine historical source files were copied into `SOURCE_SNAPSHOT` and verified at `d60c36605e988dcc160647421973f170fd87e0eb`. Further agents repeatedly rechecked the same inputs and reported `RUNNER_LAUNCH_PENDING`, but **no fresh independent Runner executed**. This is a genuine failure of the **dispatch transition**, NOT of the source blob SHA or of B's reasoning.

**One-and-done observation rule:** Once the immutable input/9-file historical bundle has a verified Git receipt, **do not use subsequent handoffs to revalidate the same unchanged blob**. Only redo verification if the input ref/allowlist changed or a real integrity concern is recorded. That invariant frees the next action to be a launch attempt.

**Mandatory next operator decision:** Create a `DISPATCH_REQUEST` message via the same `buddy-message` Relay transaction surface, separate from the Stage 1 inputs. Include *case identity, independent agent execution target/provider, operator identity, original pinned packet/source refs, tool/content isolation method, explicit permitted/forbidden reads, output destination, success/blocked terminal states, and a no-current-PR-read negative probe*. If a model runtime cannot be started, report **`BLOCKED_NO_RUNNER_CAPABILITY`** with the actual missing launch/isolation capability instead of returning `RUNNER_LAUNCH_PENDING` indefinitely.

**Dispatch observation:** A later `DISPATCH_OBSERVATION` message must say one of:

- `RUNNER_EXECUTION_OBSERVED` — exact independent session/run identifier, external launch receipt, tool/snapshot admission proof and where B's genuine output was observed; not merely a Markdown packet or GitHub link.
- `BLOCKED_NO_RUNNER_CAPABILITY` — provider/tool has no fresh-agent launch interface, or operator lacked permission to initiate it. This is a stop state for that operator, not evidence that the job ran.
- `BLOCKED_ISOLATION_UNVERIFIED` — a model ran, or could run, but current GitHub/Agent A information remained readable; mark the run **RESEARCH_REHEARSAL_ONLY**, not clean Stage 1.
- `RUNNER_FAILED_WITH_EVIDENCE` — an actual externally launched run failed, with independent error/source ref; bounded explicit retry decision needed.

A `DISPATCH_OBSERVATION` written by Agent A alone does not attest external execution. The observer must cite external provider/session evidence. A local transaction `COMMITTED` proves only that **this statement was durably recorded**, not that it is true.

**Gate discipline:** `INPUTS_VERIFIED` ≠ `DISPATCH_REQUESTED` ≠ `RUNNER_EXECUTION_OBSERVED` ≠ `STAGE1_PLAN_FROZEN`. Do not disclose Stage 2 based on any of the first three alone. B's independently authored Stage 1A source baseline and Stage 1B plan must be read back/sealed with tool-visibility evidence. Writer promotion is another unrelated gate.

**Physical isolation:** The full Common repository is *not* the Runner's read-restricted workspace. Its `relay/` contains newer PR/handover materials. A GitHub tool that may open arbitrary refs is still an unrestricted tool even if the desired snapshot is pinned to a historical commit. Build a **separate read-only runtime workspace containing only the historical source and sanitized Stage 1 input**, disable arbitrary network/GitHub/current conversation access, and have a distinct operator establish the scope. Merely pointing a fresh chat at the Common folder cannot prove isolation.

**No launcher is supplied by this R1 command.** The `buddy-message` CLI is a transport/recording operation. Until an authorized independent AI-runner runtime exists, the honest next action is to publish `BLOCKED_NO_RUNNER_CAPABILITY` with the exact blocker and a designated human/agent capable of resolving it—not more source SHA checks or fabricated execution.

## Visibility boundaries — not provided by the file extension

| Message purpose | Reader before Stage 1 freeze | Reader after independently verified Stage 1 freeze |
| --- | --- | --- |
| Original source / WHAT-WHY `STAGE1_INTAKE` | Trusted operator + correctly restricted fresh Runner B | A / B / operator |
| Runner's original `STAGE1_BASELINE` and `STAGE1_PLAN` | B can author; independent operator may inspect and freeze | B / operator / authorized A if permitted |
| Agent A's `TECHNICAL_HANDOVER` | Agent A + operator **only** | B on separately admitted Stage 2 |
| `STAGE2_RECONCILIATION` | **Not available to Stage 1** | B after Stage 2 release |

**Do not equate message publication with tool admission.** A model with unrestricted GitHub reads may see every message here, including Stage 2. The external Relay operator must actually enforce a fresh Runner session, an allowlist of immutable original-source reads, and an independent freeze and disclosure procedure. Until this exists, Stage 1 blindness is `NOT_VERIFIED`. For this first coding slice, the transaction type only transports/records Markdown; stage-read isolation and writer transfer remain open in #889 R2–R6.

## Safe human-readable Markdown contents

Every published message should state, in prose:

- Governed responsibility issue/Owner scope; author/role (claimed unless provider-authenticated).
- Stage and intended reader; exact source/fixture basis and reference.
- Factual observation vs claim vs inference vs UNKNOWN.
- Upstream messages/immutable refs depended upon.
- What was tested, what failed or remains unexecuted.
- If a read-isolation, Stage 1 freeze, or executor lease is claimed, an **external verifier ref**; absent evidence is UNKNOWN.

These are **authoring instructions**, not a new YAML or JSON schema or a second official Relay event family.

## What remains for issue #889

- R2: independently sanitized original WHAT/WHY and frozen intake; exclude any Agent A solution hints.
- R3: Stage 1A *original system baseline before plan* and Stage 1B *competing new HOWs*.
- R4: actual tool/context allowlist and freeze/before-disclosure witness, including negative read tests.
- R5: native `PLAN_HANDOVER` technical disclosure and real source/consumer/evidence readback.
- R6: Stage 2 reconciliation and authorized exclusive writer continuation.
- R7: genuine agent A→independent B controlled scenario with real golden/browser tests as applicable.

Never turn this R1 transport into automatic Stage 2 disclosure or a self-certifying replacement for native handover.
