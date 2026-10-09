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
- Only validated stages are allowed: `READINESS`, `STAGE1_INTAKE`, `STAGE1_BASELINE`, `STAGE1_PLAN`, `TECHNICAL_HANDOVER`, `STAGE2_RECONCILIATION`, `CONTINUATION_EVIDENCE`.
- A transaction never overwrites an existing message; corrections require a **new** transaction with a new receipt and an explicit reference to the earlier record.
- `relay/STATE.yaml`, `relay/EVENTS.jsonl`, `relay/LEASES/`, `relay/ROADMAP/`, `relay/GENERATED/`, accepted evidence and P/E/D are **not modified**.
- If a transaction is interrupted, use the existing `relay_tx.py . recover` command and inspect the resulting actual receipt. Do not blindly retry the same TX ID or duplicate the message.

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
