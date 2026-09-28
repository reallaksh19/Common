# Golden example — programme root with provenance reconstruction

```text
ISSUE_ROLE: PROGRAM_ROOT
AUTHORING_PROFILE: PROGRAMME
PROGRAM_ID: PGM-READINESS
PROGRAMME_BASIS_REVISION: PB-0003
RELAY_PROTOCOL: V3.1_ONLY
ORIGINAL_INTENT_ISSUE: github:owner/repo#201
RELAY_HANDOVER_ISSUE: github:owner/repo#202
```

## Owner outcome

Prove one coherent end-to-end readiness journey on exact production evidence while preserving the Owner's original intent and making later agent reasoning reconstructible.

## Original Intent source

- `github:owner/repo#201`
- historical verbatim Owner source;
- supplied examples/inputs/expected outputs;
- `NO_EP: true`;
- later Owner decisions are represented by programme amendments, not by rewriting #201.

## Owner requirement ledger

| ID | Requirement | Source | Current state |
| --- | --- | --- | --- |
| TASK-001 | preserve reusable producer work | Original Intent #201 | ACTIVE |
| TASK-002 | prove one exact-main joined path | Original Intent #201 | ACTIVE |
| TASK-003 | do not add a new execution gate | Owner decision OA-002 | ACTIVE |

## Governing Roadmap / authority

| ID | Ref | Meaning | Authority |
| --- | --- | --- | --- |
| RM-001 | `RM-READINESS@3` | current programme route | OWNER |
| RM-002 | `EVT-ROADMAP-17 / ROADMAP_RECONCILED` | producer B output now available | DERIVED CHRONOLOGY |

## Why now / governing witness

Independent producer lanes exist, but programme closure requires one exact-head consumer proof. An earlier coordinator summary was stale relative to live PR material.

Observed main: `0123456789012345678901234567890123456789`

## Non-goals

- no bulk subject authoring;
- no new execution/admission gate;
- no fixture promotion to canonical truth;
- no duplicate Roadmap, EP, Local Agent or RLL protocol.

## Canonical input/source registry

| ID | Ref/source | Meaning | Authority | Kind |
| --- | --- | --- | --- | --- |
| INPUT-001 | `src/contracts.json` | joined contract | PRODUCTION | PRODUCTION |
| INPUT-002 | Owner fixture A | discriminating witness | OWNER | OWNER_SUPPLIED |

## Common benchmark / oracle registry

| ID | Type | Source | Meaning | Independent? |
| --- | --- | --- | --- | --- |
| BM-001 | AUTHORITATIVE_REFERENCE | frozen contract fixture | expected joined result | YES |
| BM-002 | PRODUCT_REGRESSION | existing unit suite | neighbor behavior | NO |

## Common validation registry

| ID | Requirement | Evidence |
| --- | --- | --- |
| VAL-001 | exact-main joined route executes | runtime/test ref |
| VAL-002 | stale producer identity is rejected | negative test |

## Programme success / exit criteria

| ID | Requirement | Responsible workstreams | Evidence | Status |
| --- | --- | --- | --- | --- |
| EXIT-P1 | Core contract holds | A/E | test refs | OPEN |
| EXIT-P2 | Atlas contract holds | B/E | test refs | OPEN |
| EXIT-P3 | Navigation holds | C/E | browser refs | OPEN |
| EXIT-P4 | Standalone host holds | D/E | offline refs | OPEN |
| EXIT-P5 | One exact-main joined proof passes | E + producer debts | exact-main discovery | OPEN |

## Workstream registry

| Workstream | Child / EP | Outcome | Consumers |
| --- | --- | --- | --- |
| A | #210 / EP.210.1 | producer contract | E |
| B | #211 / EP.211.1 | atlas output | E |
| E | #215 / EP.215.1 | joined integration proof | programme |

## Reconstruction topology

```text
Original Intent
  #201

current Roadmap / Owner amendments
  RM-READINESS@3
  OA-002
  ROADMAP_RECONCILED EVT-ROADMAP-17

EP / child responsibility
  #215 / EP.215.1

primary-agent reasoning
  #215 comment CX-215-004
  IMPLEMENTATION_PLAN rev 2

Local Agent / OFFLOAD
  OFFLOAD-215-003
  governed helper issue #219

RLL transport
  #215 RLL_EXECUTION_V1
  #215 RLL_WORKER_STATE_V1
  transport only; not acceptance

material truth
  PR #237 / exact head / tests

derived current views
  issue-local Task Snapshot
  [Relay Handover] #202
```

## Producer / consumer contract

### OUT-001 — atlas producer result

**Producer:** B

**Consumers:** E

**Meaning:** exact canonical atlas output at the referenced material head.

**Consumers must not infer:** programme integration PASS.

## Dependency contract

### DEP-001 — joined producer output

**Producer:** B

**Consumer:** E

**Why required:** integration proof consumes the canonical producer result.

**Satisfaction evidence:** PR/material ref, not issue closure.

**Independent work:** E may prepare unrelated integration harness assertions while waiting.

## Dedicated operational ledger

`[Relay Handover] #202` indexes:
- Original Intent #201;
- current Roadmap basis/amendments;
- EP/workstream refs;
- primary reconciliation refs;
- OFFLOAD/Local Agent refs;
- RLL refs;
- every nonterminal PR;
- exact material heads;
- expected next observations.

It does not copy transcript bodies or grant authority.

## Decision surface

Engineer: implementation choices inside owned responsibility.

Coordinator: cross-agent consequences, useful parallelism, re-observation and routing.

Owner: genuine human/product/programme choices only.
