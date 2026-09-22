# Engineering Relay V3.1 delta

## Purpose

V3.1 preserves the copied execution-safety model and adds missing continuity at actor/task boundaries. It is intentionally not a redesign of execution packages, checkpoints, controls, material drift, or delivery authority.

## Base mantra

A runner must leave the baton more useful than it received it. If another actor must act, the receiver needs an executable contract rather than a status paragraph. If the current actor releases unfinished custody, the repository must retain enough verified context for a qualified successor to continue without reconstructing intent from chat.

## Communication modes

### STATUS

Reports current truth. No recipient action is implied.

### REQUEST

Another actor is expected to perform bounded work. A request must carry purpose, exact material basis, steps, success/stop conditions, prohibited actions, and a return contract.

### HANDOVER

Continuation responsibility is ending or moving. Graceful release requires current handover context and explicit reconciliation of programme/parent-issue consequences.

A REQUEST must not be answered with STATUS-only prose.

## Local execution

LOCAL_EXECUTION_EXPORT produces YAML plus a human-readable runnable packet. VALIDATE_ONLY is the default mode. The helper verifies exact HEAD before running steps and returns one of PASS, FAIL, BLOCKED, NOT_RUN_ENVIRONMENT, NOT_RUN_INFRASTRUCTURE, or HEAD_MISMATCH.

LOCAL_EXECUTION_RETURNED is evidence only. The original owner resumes responsibility and decides whether the evidence supports checkpoint, control, roadmap, or delivery changes.

## Graceful release

HANDOFF release validates:

1. current STATE/EP/lease against HANDOVER_CONTEXT;
2. current material head and digests;
3. task/improvement projection digests;
4. committed HANDOVER_PLANNED evidence;
5. explicit roadmap reconciliation rather than UNKNOWN;
6. parent-issue disposition when a parent issue exists.

ADMINISTRATIVE release remains an explicitly non-graceful recovery path.

## Human status and value

Quantitative task/parent/programme status is projected from existing V3.1 read models. It is not treated as evidence of technical value. IMPROVEMENT_VIEW separately reports evidence-bound capability/evidence/understanding/downstream changes and unresolved proof.

## Roadmap feedback

RECONCILE_ROADMAP accepts a proposed reconciliation but mutates the existing ROADMAP and STATE transactionally. NO_CHANGE cannot hide a mutation. A changing disposition requires a new roadmap revision, and an active EP may not be orphaned.

## Parent-issue lineage

Provider observations can state NO_CHANGE, UPDATE, LINK, TRANSFER, SPLIT, SUPERSEDE, CLOSE, or UNKNOWN and carry typed relationships such as TRANSFERS_TO, SPLIT_INTO, and SUPERSEDED_BY. TASK_SNAPSHOT and handover preserve that lineage.

## Non-goals

V3.1 does not:
- weaken checkpoint acceptance;
- make generated views authoritative;
- transfer task custody to local helpers;
- make issue/provider state execution authority;
- silently select itself as the repository protocol;
- import or link implementation/schema files from the V3 skill tree.
