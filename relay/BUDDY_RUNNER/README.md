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
- **This R1 transport permits only preparation/Stage 1**: `READINESS`, `STAGE1_INTAKE`, `DISPATCH_REQUEST`, `DISPATCH_OBSERVATION`, `STAGE1_BASELINE`, `STAGE1_PLAN`. It refuses `TECHNICAL_HANDOVER`, `STAGE2_RECONCILIATION` and `CONTINUATION_EVIDENCE` until the native custody/disclosure/continuation gates have been implemented and independently qualified. Use the existing V3.2 native handover transaction for actual technical custody.
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

## R2/R3 — sanitize original intake, then reconstruct baseline BEFORE planning

This is a Relay Markdown communication contract, **not** another copy/paste chat prompt, a separate schema, or an acceptance authority. Operators must provide B a separate restricted runtime with ORIGINAL evidence only. The native transaction now enforces this structural order with earlier committed, unchanged receipts for the same issue and lower transaction serial:

1. **STAGE1_INTAKE:** original Owner words with provenance, approved task WHAT/WHY, original immutable source cutoff and file/fixture allowlist; distinguish real Agent A START from historical research cutoff. Unknown stays UNKNOWN. Operator must quarantine Agent A implementation/diagnosis and expected solutions.
2. **DISPATCH_REQUEST:** name responsible operator, independent Runner execution target, frozen input refs and SHA, permitted and forbidden reads, expected output destination and negative probe. A request does **not** launch B.
3. **DISPATCH_OBSERVATION:** either a blocker/failure, or heading `# RUNNER_EXECUTION_OBSERVED` with `Session ref: ...` and `Read-scope ref: ...`. These two fields are **claimed references**, not provider-authenticated runtime or tool-visibility proofs. Operator must independently inspect them.
4. **STAGE1_BASELINE:** B independently establishes a real original input → producer function → consumer → output path, a positive example, an adversarial case, semantic invariants, failure vs legitimate absence, and explicit source unknowns. Merely listing paths or restating Owner text does NOT pass.
5. **STAGE1_PLAN:** Only AFTER baseline publication, B proposes at least two different feasible mechanisms, concrete counterexamples, falsifiable test/golden acceptance, downstream impacts, high-ROI next bounded action and parked medium-ROI scope. The two messages are one Stage 1 research episode, NOT an extra Two/Three-Pass prompt.

The transaction operation requires a **native committed Relay receipt** for each prerequisite. Copying a loose `.md` file into the directory is insufficient. A blocked dispatch cannot produce Stage 1 baseline. A Stage 1 plan cannot appear before baseline. Existing messages are immutable; corrections are new transactions, not retroactive edits.

### Sanitization review — do not confuse original WHAT/WHY with Agent A HOW

| Give B as original evidence | Keep operator-only until Stage 2 |
| --- | --- |
| Original Owner sentences, approved scope and acceptance outcomes with historical source | Agent A's selected design, current failure diagnosis, exact fix module or new priorities |
| Original immutable source/consumer functions and authentic input fixtures | Current PR/CI, later source, current test results or expected golden answers |
| Neutral unresolved user-visible requirements independently grounded in original material | Agent A's rejected experiments, found implementation defect, solution-shaped “known risks” |
| Genuine unresolved historical gaps and UNKNOWN provenance | Unverified claim disguised as original task-start SHA or accepted user-observable result |

For every line in the original intake, the operator must ask **who knew it, when, from which original source, and whether it suggests the previous agent's HOW**. If uncertain, quarantine rather than quietly injecting into B. This is a source/authority judgment; simplistic keyword filters or a Markdown parser cannot reliably determine semantic leakage.

**Negative examples:** Inject “Agent A found algorithm P failing in module Q” → reject from B's intake. An original Owner report “buttons do not work” → keep as a WHAT need without suggesting a repair. A later PR URL or sealed expected output → quarantine. Unreceipted prior intake → dispatch rejected. Blocked dispatch followed by fake baseline → rejected. A good Stage 1 plan with no baseline → rejected.

**Claimed-role continuity check:** The Relay transaction actor recorded for `STAGE1_BASELINE` must differ from the operator who recorded `DISPATCH_OBSERVATION`; the `STAGE1_PLAN` actor must match the baseline author. This prevents accidental self-relabeling or a different Runner silently inheriting the prior baseline. Actor strings are *claims*, not proof of distinct model sessions or identities; R4 still requires external provider observations and a genuinely isolated workspace.

**Limits:** even a correctly ordered claim `RUNNER_EXECUTION_OBSERVED` can be fabricated. This message transport NEVER proves independent Runner tool isolation, B authorship, Stage 1 qualification, Stage 2 disclosure rights or new writer authority. These require independent external evidence/admission under later R4–R6. Do not count a structural transaction as a successful engineering reconstruction.

## Visibility boundaries — not provided by the file extension

| Message purpose | Reader before Stage 1 freeze | Reader after independently verified Stage 1 freeze |
| --- | --- | --- |
| Original source / WHAT-WHY `STAGE1_INTAKE` | Trusted operator + correctly restricted fresh Runner B | A / B / operator |
| Runner's original `STAGE1_BASELINE` and `STAGE1_PLAN` | B can author; independent operator may inspect and freeze | B / operator / authorized A if permitted |
| Agent A's native technical handover (`PLAN_HANDOVER`/`HANDOVER_CONTEXT`) | Agent A + operator **only** | B on separately admitted Stage 2; **not** published through this R1 message channel |
| Stage 2 reconciliation (future controlled operation) | **Not available to Stage 1** | B after independently verified release; not a currently permitted R1 stage |

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
