# Generic V2.5 stress scenarios

These tests are synthetic. They must not encode names, IDs, branches, formulas, paths or workflow semantics from any downstream project.

Current stress coverage includes:

- infrastructure `NOT_RUN` without automatic hard stop;
- overloaded blocker-state rejection;
- independent material authority (`WRITE | READ_ONLY | NONE`) from execution continuation;
- Owner deferral preserving `PENDING_NOT_SATISFIED` and not granting write authority;
- topology-derived executable frontier;
- progress denominator changes without erasing earned work;
- context-dependent instruction rejection;
- checkpoint → successor EP baton linkage;
- Owner-intent roadmap mutation with frontier/progress-basis reconciliation;
- long-running EP continuity across multiple explicitly unaffected roadmap revisions;
- broken/missing roadmap-continuity revision-chain rejection;
- active contract change forcing `RECONCILE_REQUIRED + READ_ONLY`;
- active use after roadmap-continuity invalidation rejection;
- incoming-phase Q1-Q5 anchor grounding;
- supersession transfer into the successor with acceptance/evidence status and exact basis preserved;
- multi-generation issue supersession A -> B -> C;
- intermediate supersession preserving inherited unresolved acceptance/evidence unchanged;
- explicit durable resolution of inherited supersession items;
- silent supersession lineage drop/status mutation rejection;
- supersession branching, multiple-predecessor and cycle rejection;
- deep `PARENT_OF` issue projection rollups;
- issue projection stale child snapshot rejection;
- multiple-parent and parent/child cycle rejection;
- aggregate parent closure blocked while a direct child remains GitHub OPEN;
- GitHub closure state separated from engineering/work lifecycle;
- issue closure refusing hidden `FAIL`/`NOT_RUN` evidence or unresolved work without an explicit disposition;
- hard-stop/execution consistency;
- terminal/idle relay with empty frontier and no active EP;
- Owner-approved parallel routing, lane isolation and deferred integration;
- lane checkpoint `JOIN` semantics and multi-parent Parallel Join Receipt;
- integration EP creation only after every lane checkpoint converges and integration becomes the sole frontier;
- partial parallel-lane invalidation freezing the old plan and creating a durable `PARALLEL_REPLAN`;
- completed sibling lane checkpoint retention during replan;
- invalidated lane acceptance/evidence transfer to a serial replacement EP without status/basis loss;
- one invalidated predecessor lane split across multiple replacement frontier packages with exact partition preservation;
- transfer duplication, omission and evidence-status mutation rejection;
- replan into a new Owner-approved parallel topology with every new lane bound to `previous_replan`;
- superseded parallel-plan branches/worktrees resolving no executable route after replan;
- multi-generation `PLAN -> REPLAN -> PLAN -> REPLAN` history recovery;
- missing historical replan receipt rejection;
- historical replan forward-link mismatch rejection;
- cyclic replan/plan lineage rejection;
- one-of checkpoint/join/replan predecessor-baton enforcement;
- bootstrap/migration truth preservation;
- lifecycle-aware status/handover rendering, including continuity, join and replan custody;
- required external projection pending/stale without confusing repository recovery with full handover readiness;
- crash-safe projection publication with stable `operation_id` and `PUBLISHED_UNCONFIRMED` recovery;
- stale external projection while repository advances across multiple roadmap generations;
- explicit observed external generation distinct from newest desired generation;
- intermediate desired projection generations retired with no retry authority;
- superseded projection-operation chains required to terminate at the current operation;
- published-but-unconfirmed obsolete generation retaining receipt as history without replay;
- newest projection generation converging `STALE -> PUBLISHED_UNCONFIRMED -> IN_SYNC`;
- in-sync projection binding to the current roadmap revision and current execution reference;
- serial/parallel EP selection from checked-out branch/worktree with ambiguity rejected;
- base drift classified as `DISJOINT | WITHIN_QUALIFIED_BOUNDARY | OVERLAPPING | UNKNOWN`;
- qualified-boundary drift retaining read-only recovery while confirmation remains pending;
- overlapping/unknown drift withholding material-write authority until reconciliation;
- checkpoint PASS/FAIL/NOT_RUN evidence bound to the exact material reference it observed.

Real repositories may be inspected read-only to discover additional failure modes. Every discovered mode must be reduced to a repository-neutral synthetic regression here before changing Common protocol logic. No downstream-project names or semantics belong in these fixtures.
