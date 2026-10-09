# V3.2 — Planned succession and unplanned recovery routing

**Class:** Human-operable V3.2 Markdown guidance. This document does not create a new event, schema, ceremony, permission, monitor or generator. Existing V3.2 recorder, exact-head source checks, `TASK_EVIDENCE`, `PLAN_HANDOVER` and Owner/lease authority remain normative.

## Four distinct methods

| Event | Method | Independent thinking | Visibility and outcome |
|---|---|---|---|
| **Planned: Agent A is still coding** | **Buddy Runner — Stage 1** | B reconstructs the **known engineering task** and original WHAT/WHY/HOW from frozen **original** sources, real consumers and fixtures; generates alternatives and a defensible plan. | A's actual HOW/current PR/head/CI hidden until B's plan is independently frozen. A remains primary. |
| **Planned: transition to successor** | **Native technical Handover transaction + Buddy Stage 2** | B compares **its own frozen plan ↔ A's detailed technical disclosure ↔ real current source and Owner obligations**; reconciles, challenges and selects next bounded work. | Native `HANDOVER_CONTEXT` and `HANDOVER_PLANNED` record custody. Read-only reconciliation precedes separately authorized single-writer continuation. |
| **Unplanned: Agent A terminated; focused repo/task recovery** | **Standalone Two-Pass generated with a separate external agent** | Pass 1 understands the **live system without seeing the assigned task**. Pass 2 sees the task, original intent, amendments and material evidence, reconciles/improves and drafts a plan. | Two-Pass prompt generator is authoritative; Pass 2 stops for its explicit Owner plan-approval boundary. No fake predecessor handover. |
| **Unplanned: Agent A terminated; broader app expansion/reassessment requested** | **Standalone Three-Pass generated with a separate external agent** | Prompt 0.5 programme IMAGINE → 1 local IMAGINE → 2 UNDERSTAND live reality → 2.5 RECONCILE → 3 REVALIDATE and authorized move. | Broader destination-first thinking; five prompts, three conceptual passes; no self-approved roadmap expansion or invented Agent A disclosure. |

**Crucial contrasts:** Two-Pass Pass 1 hides the **task**; Buddy Stage 1 **knows the task** and hides the **previous agent's HOW**. Three-Pass is not an automatic handover; it is a broader optional reasoning method. Handover is a material custody transaction, not a prompt generator. None of these mechanisms independently confers execution authority.

## Planned path — Owner says “Prepare for runner”

1. **At the live Agent A conversation**, Owner's exact words “Prepare for runner” trigger immediate preparation of original Owner words, bounded WHAT/WHY, original exact-source START (or honestly UNKNOWN), roadmap/claim, original consumer paths, authentic fixture inputs, pending/known/parked. A must NOT include its current design/PR/test outcomes in the Stage 1 packet.
2. Agent A evaluates readiness at **ordinary `TASK_EVIDENCE` checkpoints**. ~60% consumed usable episode life = PREPARE; ~70% = proactively propose **“Time for Runner”**; ~85% = URGENT. Credible next-unit runway or coherence/interruption warnings can trigger earlier. These percentages are *advisory*. Distinguish provider token measurement, calibrated episode estimate, self-estimate and UNKNOWN; V3.2 P/E/D, progress and seven-component delivery-health are NOT context consumption.
3. A separate operator starts a **fresh** Runner B with a technically restricted original-source read scope. Supply [Stage 1](../runner/STAGE1_RECONSTRUCT.md), not Agent A implementation or [Stage 2](../runner/STAGE2_RECONCILE.md). B must independently trace source→consumers, challenge assumptions, compare two designs, answer source questions, identify falsifiers and freeze its original plan.
4. **Native handover is a technical transaction:** Agent A records its actual changed modules/functions/downstream consumers, HEAD/base and drift, tests on exact commits, golden/Chromium results, accepted and missing evidence, design rationale, failures, pending work, parked proposals, in-flight writes and current authority. Use V3.2 `scripts/plan_handover.py` and `scripts/handover_context.py` without modifying their schema merely for a Runner; see [technical handover instructions](../runner/PLANNED_TECHNICAL_HANDOVER.md).
5. Only after the independent Stage 1 output and permitted read visibility are verified can the controller disclose Agent A's technical packet plus live source and release [Stage 2](../runner/STAGE2_RECONCILE.md). B should correct either agent's mistakes and produce a source-grounded revised plan. Reconcile toward the *same* governed responsibility, not an automatic duplicate issue.
6. Actual execution/custody is controlled by existing Owner/assignment/lease semantics; a new agent identity does not create a new Owner decision gate, P/E/D progress or write permission. Fence concurrent material writers as required.

**Degraded planned path:** If B was never launched or read forbidden current information before sealing Stage 1, perform an ordinary technical handover and label independence **NOT_ACHIEVED**. Do not backfill a fake Buddy Stage 1 after exposure.

## Unplanned path — A is unavailable

1. Do the existing V3.2 **fast recovery** first if provider/current-head/last-checkpoint evidence suffices. Re-observe Owner/PROTOCOL_REF and amendments → checkpoint → branch/HEAD/PR/tests → delta → reconcile → `TASK_EVIDENCE — RECOVERY` and readback before next material change as required. This does not need Two-Pass or Three-Pass as a universal gate.
2. Where Owner requests independent reconstruction or recovery evidence is too uncertain for direct continuation, use a **separate external prompt-design agent**. Do not pretend that Agent A supplied a final handover.
3. **Focused repository task** → external agent uses canonical standalone [Two-Pass schema](../../../two-pass-prompt-generator/schema.md) and [launcher](../../../two-pass-prompt-generator/SKILL.md); generates **exactly two prompts**. Pass 1 sees system identity + broad outcome but **NO assigned task/issue/fix/Original Intent**, and inspects live repository reality. Pass 2 reveals the real issue, history, Owner authority, current source/PR evidence and any existing historical handover. Stops at its specified Owner approval boundary before durable plan publication.
4. **Broader product/application future, improvement and recovery** → external agent uses standalone [Three-Pass schema](../../../three-pass-prompt-generator/schema.md) and [launcher](../../../three-pass-prompt-generator/SKILL.md); generates **exactly five prompts**, preserving independent broad imagination, local imagination, source reconstruction, reconciliation and authorized forward action. It may identify adjacent improvements but cannot self-authorize expansion.
5. If A is dead, mark any reconstructed status `THIRD_PARTY_RECONSTRUCTION` or UNKNOWN and verify against live material. A prompt generator cannot prove past intent, accepted progress, actual runner launch or exclusive-write authority.

## Examples that catch conceptual failures

| Observation | Correct treatment | Never claim |
|---|---|---|
| Owner requests preparation before measured 70% | PREPARE immediately, consumed life UNKNOWN if unobservable | Provider-measured 70% |
| Buddy sees A's newest PR before sealing | STAGE1_CONTAMINATED; no blind success | “I forgot it” |
| A is alive and prepares formal handover | Native handover of actual technical evidence; Buddy Stage 2 only if frozen Stage 1 exists | Automatic Two-Pass as part of `PLAN_HANDOVER` |
| A is gone but recent checkpoint supports safe recovery | V3.2 fast recovery, required evidence, authorized continuation | Forced Five-Prompt run |
| A is gone; targeted fresh reconstruction requested | Standalone Two-Pass; hide TASK in Pass 1 | Feeding the assigned issue to Pass 1 |
| A is gone; Owner wants bigger product improvements | Standalone Three-Pass; preserve actual Owner authority and scope | Treat all speculative ideas as approved |
| Agent B independently proposes a better design | Preserve comparison and seek actual governed write permission | Plan quality automatically grants exclusive writer rights |

## Canonical links and ownership

- Planned Buddy instructions **physically in this V3.2 folder:** [Prepare](../runner/PREPARE_FOR_RUNNER.md), [Stage 1](../runner/STAGE1_RECONSTRUCT.md), [Stage 2](../runner/STAGE2_RECONCILE.md), [operator guidance](../runner/OPERATOR_GUIDE.md).
- Technical transaction: [handover instructions](../runner/PLANNED_TECHNICAL_HANDOVER.md), native `handover_context.py` and `plan_handover.py`.
- Focused unplanned reasoning: standalone Two-Pass only. Broader unplanned reasoning: standalone Three-Pass only. Their canonical schemas override any descriptive summary here **for the respective generated prompt artifacts**.
- V3.2 baseline: [SKILL.md](../SKILL.md), [Two-Pass integration](two-pass-integration.md) and [Three-Pass integration](three-pass-integration.md).

No new background watcher, Python/YAML adapter or acceptance percentage is part of this routing clarification. Source, producer context, prompt quality and technical custody remain distinct.
