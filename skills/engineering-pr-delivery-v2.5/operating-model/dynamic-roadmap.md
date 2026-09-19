# Dynamic roadmap and material event ledger

## Purpose

The Owner roadmap is a **concept map**, not a task diary.

V2.5 separates three concerns:

```text
OWNER INTENT
    ↓
CONCEPT ROADMAP
    ↓
EXECUTION GRAPH / CURRENT WORK

and alongside execution:

MATERIAL EVENT LEDGER
```

The layers answer different questions:

- **Concept roadmap** — what durable programme outcomes are we trying to achieve?
- **Execution** — what concrete work is currently planned/active to achieve them?
- **Event ledger** — what materially happened while pursuing those concepts?

Do not collapse these layers.

## Concept layer

In the current V2.5 roadmap shape, objectives and phases are the concept-level anchors.

Work packages remain execution units even though they live structurally inside `OVERALL_ROADMAP.yaml`.

Therefore:

```text
concept_refs
    may reference objective / phase ids

execution_refs.work_package
    references WP ids
```

An event that happened during `WP-042` must not make `WP-042` a concept merely for convenience.

The longer-term roadmap hierarchy may evolve, but this separation is normative.

## Execution layer

Execution details change frequently:

- work packages;
- execution packages;
- issues;
- pull requests;
- checkpoints;
- tests/evidence;
- blockers and local/external actions.

Execution changes do **not** automatically imply a concept-roadmap change.

Examples:

```text
WP completed
→ execution/status event
→ concept roadmap unchanged

new benchmark task discovered under an existing verification concept
→ engineering discovery event
→ new execution work may be needed
→ concept roadmap unchanged

Owner adds a materially new desired capability
→ concept change proposed/applied through normal roadmap/ODR authority
```

## ROADMAP_EVENTS.yaml

Optional durable ledger:

```text
agents/relay/roadmap/ROADMAP_EVENTS.yaml
```

It is a **source-bound historical index**, not roadmap authority.

Each event contains:

- stable `EVT-*` identity and append sequence;
- material event class;
- plain-language summary;
- one or more concept refs;
- execution refs;
- durable source/evidence basis;
- concept-change disposition;
- roadmap-revision reference when a concept change was actually applied;
- follow-up classification.

Supported material classes:

```text
TASK_PROGRESS
IMPLEMENTATION_CHANGE
EVIDENCE_PROGRESS
DELIVERY_OR_CUSTODY_PROGRESS
WAITING_OR_MONITORING
ENGINEERING_DISCOVERY
BLOCKER_CHANGE
OWNER_DECISION
ROADMAP_REVISION
```

Do not append routine command execution, polling or repeated retries that produce no material state/evidence change.

## Concept-change semantics

Every event says exactly one:

```text
NO_CONCEPT_CHANGE
CONCEPT_CHANGE_PROPOSED
CONCEPT_CHANGE_APPLIED
```

### NO_CONCEPT_CHANGE

The event matters historically, but programme concepts remain the same.

Typical examples:

- accepted work progressed;
- a check moved NOT_RUN → PASS;
- an implementation route failed;
- a new execution task was discovered under an existing concept;
- custody or delivery changed.

### CONCEPT_CHANGE_PROPOSED

Current engineering evidence suggests the concept map itself may need to change.

This event **does not change the roadmap**.

It must route to:

```text
ROADMAP_PROPOSAL
or
OWNER_DECISION_REQUIRED
```

The normal roadmap transaction/Owner authority decides whether the proposal is applied.

### CONCEPT_CHANGE_APPLIED

A real roadmap revision changed concept truth.

The event must reference the durable roadmap revision id/path.

The event is historical indexing of that revision; it is not the authority that performed the change.

## Append-only producer

Use:

```bash
python skills/engineering-pr-delivery-v2.5/scripts/append_roadmap_event.py \
  <event.yaml> <repo-root>

python skills/engineering-pr-delivery-v2.5/scripts/append_roadmap_event.py \
  <event.yaml> <repo-root> --apply
```

The producer:

- assigns the next sequence;
- rejects duplicate event ids;
- validates concept/execution references;
- appends without rewriting prior event rows;
- increments ledger revision.

Do not hand-edit earlier events to make history look cleaner. Correct later knowledge with a new event and durable basis.

Git/source history is still the strongest protection against malicious rewriting; the append producer supplies the normal protocol path.

## Relationship to roadmap revisions

The normal decision flow is:

```text
material event
    ↓
record event
    ↓
reconcile execution
    ↓
ask whether concept itself changed
    ├── no  → concept roadmap unchanged
    └── yes → proposal / Owner decision / roadmap revision
                          ↓
                     applied event
```

Major-task completion therefore does not automatically cause structural roadmap mutation.

## Owner roadmap projection

`render_roadmap.py` renders:

1. concept roadmap;
2. execution under those concepts;
3. recent material events.

The generated Markdown is non-authoritative.

This deliberately resembles a useful human programme roadmap while keeping machine truth in the structured sources.

## Handover

`Plan for Handover` uses recent events linked to the active objective/phase as **context**.

Events explain:

- why current execution exists;
- important discoveries;
- failed/falsified routes;
- recent material changes.

They do not automatically become successor INTENT.

Successor INTENT still comes from unresolved acceptance, evidence, next-work, checkpoint and Owner-decision truth.

This prevents historical narrative from silently expanding authorized work.
