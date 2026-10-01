# Relay V3.2 responsibility continuity — worth-gated pilot

## Authority

This slice is recorder-first. Git/PR/tests/runtime/artifacts remain material truth; Owner/programme intent remains human authority. Current/progress/provider views are derived. Reporting failure may reduce observability; it must never reduce production agency.

The engineering publication set remains exactly `IMPLEMENTATION_PLAN`, `PLAN_UPDATE`, `TASK_EVIDENCE`, and `TASK_RESULT`.

## Responsibility first

One independently governed engineering responsibility keeps one continuity identity while executors/sessions change. Executor count is execution history, not topology. Programme/RLL/OFFLOAD traversal is conditional on actual references or cross-responsibility dependencies.

## Current responsibility surface

A continuity-managed responsibility has at most one mutable `FURTHER_TASK_SNAPSHOT` with `AUTHORITY: DERIVED_CONTINUITY_ONLY`.

It contains state, plan reference, declared outcome denominator, P completion frontier, E evidence frontier, active/completed/pending units, material and semantic/evidence heads, current/next, Owner decision, and stream-loss/handover state.

Progress must never be inferred from commits, tests, comments, tool calls, tokens, elapsed time, or executor count.

## Mandatory implementation-start event

After a durable implementation plan exists, starting material implementation is an observability event:

```text
IMPLEMENTATION_PLAN present
→ implementation begins
→ implementation-start
→ refresh current responsibility projection
→ best-effort GitHub status/title synchronization
→ continue engineering
```

Starting implementation earns zero progress. The event command automatically synchronizes the configured GitHub responsibility when authenticated `gh` is available. The agent must not hand-author duplicate status prose.

Provider failure is `FAILED_OBSERVABILITY_ONLY`: record/report it and continue engineering. No timer or heartbeat performs this refresh.

## Material vs semantic/evidence frontier

V3.2 exposes independently:

```text
MATERIAL_FRONTIER = live Git/owned-PR material
SEMANTIC_EVIDENCE_FRONTIER = latest durable task evidence basis explaining/proving responsibility state
```

If the semantic head is an ancestor of material HEAD, Git derives the commit distance. Material-ahead distance is reconstruction distance, not progress.

## Abrupt interruption

Default first-line recovery:

```text
1. BASIS — verify responsibility and Owner amendments.
2. LIVE MATERIAL — observe PR/branch/base/HEAD/relevant checks.
3. DELTA — compare semantic/evidence and material frontiers.
4. RECONCILE — validate active/pending units, assumptions and negative knowledge.
5. TASK_EVIDENCE — RECOVERY — durably anchor reconstructed truth.
6. CONTRIBUTE + CONTINUE — resume useful engineering.
```

Escalate to full/deep reconstruction when responsibility identity, human authority, programme dependencies, RLL/OFFLOAD references, negative knowledge, or material/provider state cannot be reconciled.

Minimum recovery evidence:

```text
TASK_EVIDENCE — RECOVERY
RESPONSIBILITY
OBSERVED MATERIAL
LAST TRUSTED SEMANTIC BASIS
RECOVERED DELTA
CURRENT CLAIM
NOT YET PROVED
OPEN WORK
OWNER DECISION
NEXT
```

After a detected recovery, publish/read back this evidence before the next material change. This is semantic continuity discipline, not legacy action permission gating.

## Three-loss escalation

Within one executor lifecycle:

```text
loss 1 → recovery evidence
loss 2 → recovery evidence
loss 3 → recovery evidence + Plan for handover once
loss 4+ → recovery evidence; no repeated auto handover trigger
```

A successor lifecycle resets the count/trigger. This is continuity preparation, not engineering failure or Owner approval.

## Scoped result

`TASK_RESULT` adds:

```text
RESULT_SCOPE: STEP | PRODUCT | RESPONSIBILITY
COVERAGE: <declared denominator coverage>
RESPONSIBILITY_COMPLETE: YES | NO | UNKNOWN
```

`RESPONSIBILITY_COMPLETE: YES` is valid only with `RESULT_SCOPE: RESPONSIBILITY`. Old results without this field map to UNKNOWN. Issue closure or PR merge does not imply responsibility completion.

## P/E progress

For declared units:

```text
P = completed units / denominator
E = evidenced completed units / denominator
```

A unit cannot be evidenced unless complete. Example title cache:

```text
{P77% · E69% · UNIT-09 · RECOVERING}
```

The title is a glanceable cache only. Percentages may decrease after a legitimate denominator change. Do not use subjective partial weights unless governing responsibility explicitly declares them.

## Event-driven provider synchronization

Synchronize only at semantic events such as implementation start, declared outcome completion, evidence/recovery transition, denominator change, genuine Owner-decision state, and task result/completion.

Do not update for timer wake, heartbeat, command, test retry, commit count, tool call, elapsed time, or generic `proceed`.

## Reference implementation

`scripts/continuity_projection.py` implements the pilot.

Initialize:

```bash
python skills/engineering-pr-delivery-v3.2/scripts/continuity_projection.py init \
  --responsibility owner/repo#484 \
  --units declared-units.json \
  --plan-ref issuecomment-... \
  --material-head "$(git rev-parse HEAD)" \
  --github-repository owner/repo \
  --github-issue 484 \
  --output relay/GENERATED/tasks/484.continuity.json
```

Start implementation and automatically refresh GitHub:

```bash
python skills/engineering-pr-delivery-v3.2/scripts/continuity_projection.py implementation-start \
  --snapshot relay/GENERATED/tasks/484.continuity.json \
  --output relay/GENERATED/tasks/484.continuity.json
```

Refresh material frontier:

```bash
python skills/engineering-pr-delivery-v3.2/scripts/continuity_projection.py observe-frontier \
  --snapshot relay/GENERATED/tasks/484.continuity.json \
  --repo-root . \
  --output relay/GENERATED/tasks/484.continuity.json
```

## Worth falsifiers

Remove/revise this mechanism if it cannot be rebuilt against durable provider/material truth, provider sync becomes an engineering gate, clean work acquires heartbeat ceremony, P/E rewards activity rather than outcomes/evidence, or fast recovery hides contradictions that require full reconstruction.
