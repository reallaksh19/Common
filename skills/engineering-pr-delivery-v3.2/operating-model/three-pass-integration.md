# V3.2 — Standalone Three-Pass for broad unplanned reconstruction

## Correct situation

For **planned** continuity while Agent A still works, use [Buddy Runner Stage 1](../runner/STAGE1_RECONSTRUCT.md) followed by a **technical handover transaction** and [Buddy Stage 2](../runner/STAGE2_RECONCILE.md). The normal `PLAN_HANDOVER` operation does not create a Three-Pass request.

For **unplanned Agent A termination** when an independent *broader application/roadmap reassessment and improvement* is actually requested or justified, a **separate external prompt-design agent** may use the standalone [Three-Pass generator](../../../three-pass-prompt-generator/SKILL.md) and [its canonical schema](../../../three-pass-prompt-generator/schema.md). This is **not** the default for ordinary stream-loss recovery. Focused repo/task recovery uses the independently requested standalone [Two-Pass generator](../../../two-pass-prompt-generator/SKILL.md). See [method routing](continuity-method-routing-v32.md).

## Three conceptual passes, exactly five prompts

- **Prompt 0.5 — Global/programme IMAGINE:** Original broad purpose, what the full application should make possible, and possible missed user outcomes, without copying today's implementation.
- **Prompt 1 — Local/issue IMAGINE:** Independently reason about the actual issue/task purpose and boundaries, still quarantining the current implementation or PR's proposed answer.
- **Prompt 2 — UNDERSTAND:** Independently reconstruct actual live application/repository source, consumers, issue/PR/evidence and current behavior.
- **Prompt 2.5 — RECONCILE:** Compare both imagined destinations against verified reality, identify necessary corrections or genuinely evidence-supported improvements.
- **Prompt 3 — REVALIDATE AND MOVE FORWARD:** Recheck changed material/Owner authority, perform only the smallest **already authorized** change if any, and leave source-grounded handover/continuity evidence.

**Generator invariants:** `THREE_PASS_ONLY` mode; the current canonical standalone schema controls the exact prompt contract; this V3.2 document does not recreate a five-prompt schema, append an extra certification stage, import Two-Pass's approval protocol into Three-Pass, or grant execution authority. An external helper must not turn a focused issue into an unrelated programme redesign without the Owner's broader-improvement intent.

## Interruption is not a planned predecessor handover

An unavailable Agent A cannot be made to sign a final plan or explain an unrecorded HOW after termination. Obtain past checkpoints, issue history and actual current source from independent material/provider evidence, mark gaps UNKNOWN, and keep retrospective third-party reconstruction separate from actual predecessor statements. Continue the V3.2 `TASK_EVIDENCE — RECOVERY` obligation if a real recovered executor will modify material.

## Why older redirect remains historically true

V3.1 replaced **automatic handover reasoning generation** with optional standalone Two-Pass. That historical compatibility fact does **not** forbid a distinctly requested standalone Three-Pass for **unplanned broad recovery/improvement**. Neither generator is automatically launched by `PLAN_HANDOVER` or stream loss. The user's chosen purpose, scope and actual authorization select the independent reasoning mode.
