# Repository Agent Policy — shared engineering-pr-delivery-v2 rules

This is the reusable cross-repository policy for `engineering-pr-delivery-v2`. Repository-root `AGENTS.md` files are **project overlays**, not copies of this protocol.

For new material legs, `reality-check-p0.md` is a binding amendment. Where older wording conflicts with it, the P0 amendment wins.

## 1. Policy layering

```text
explicit current Owner instruction
→ repository project overlay (`AGENTS.md`)
→ this shared repository-agent policy + reality-check-p0 amendment
→ engineering-pr-delivery-v2 `SKILL.md` + references
```

A project overlay may be stricter for its domain. It may not silently weaken qualification, source/oracle custody, validation truth, owner-roadmap authority, chain/custody controls, work-item exclusivity, anti-gaming rules or merge authority.

Downstream `AGENTS.md` should contain only project identity/criticality, repository-specific roadmaps/sources, protected solver/method/data/publication domains, local validation commands/benchmarks, project-specific AUTO hard stops and stricter workflow/release restrictions. Do not duplicate the generic relay state machine, qualification sequence, Q1–Q5 schema, canonical chain paths, generic AUTO semantics, generic merge rules or crash-recovery procedure.

## 2. Protocol-adoption gate — before every new material leg

Before material coding, source-governance mutation, benchmark/oracle mutation, engineering-result publication work or AUTO progression into another material leg, re-ground live Common and record:

```text
COMMON_PROTOCOL: engineering-pr-delivery-v2
COMMON_PROTOCOL_BASIS: <live Common commit SHA actually read>
COMMON_PROTOCOL_STATUS: CURRENT | STALE_PROTOCOL | UNKNOWN
CHAIN_STATE_VERSION: 3
```

An inherited endpoint pin is historical evidence, not permission to keep using an old Common basis.

Fail closed:

```text
STALE_PROTOCOL | UNKNOWN
→ NO_MATERIAL_CODING
→ NO_AUTO_PROGRESSION
→ READ_ONLY protocol reconciliation
```

New-material adoption also requires the P0 fields defined in `reality-check-p0.md`: exact work-item identity, UUID-backed agent instance, handover protocol 2, reporting contract, Owner-baseline discovery and qualification profile version 2.

## 3. Canonical relay paths

For every new chain, takeover migration or new material leg:

```text
agents/chains/<CHAIN_ID>/ACTIVE.md
agents/chains/<CHAIN_ID>/endpoints/<ENDPOINT_ID>.md
agents/qualifications/<CHAIN_ID>/**
```

Use `CHAIN_STATE_VERSION: 3`.

Legacy `agents/agentchain*`, PR workreports, status and claims files remain READ/CITE/RECOVER/MIGRATION-PROVENANCE only. Do not create new mutable endpoints or AUTO custody there.

## 4. Exact work-item custody — before semantic overlap

Every new material leg records:

```text
WORK_ITEM_KEY: <stable identity, e.g. github:owner/repo#1535>
WORK_ITEM_MODE: EXCLUSIVE | PARTITIONED
AGENT_INSTANCE_ID: <agent-class>:<UUID>
```

A model family/name is not a unique agent instance. For `EXCLUSIVE`, a second non-terminal chain with the same work-item key is blocked before path/authority overlap is considered. The second agent joins/takes over the existing chain or stops.

`PARTITIONED` requires distinct `WORK_ITEM_PARTITION` values and `WORK_ITEM_PARTITION_AUTHORITY: OWNER:<locator>`. Semantic path/authority/benchmark/release overlap remains an additional gate after exact work-item admission.

Read `chain-concurrency.md`.

## 5. Handover-ready before work, not after work

Crash readiness is write-ahead control. Before each material batch, the accepted endpoint already contains the exact next action, hypothesis/falsifier, protected authority boundaries, expected changed domains, inputs/benchmarks/sources/production/validation paths and a current expert Q1–Q5 pack.

```text
PROTOCOL ADOPTION GATE
→ PRE-WORK V3 ENDPOINT
→ Q1–Q5 QUALITY + OWNER-BASELINE VALIDATION
→ MATERIAL WORK
→ VALIDATION TRUTH
→ MATERIAL RECEIPT / SUCCESSOR ENDPOINT
→ only then another material batch
```

Do not code first and manufacture the takeover exam afterward. AUTO pauses before mutation if the work-ahead endpoint, Q pack, baseline coverage or handover readiness is invalid.

## 6. Expert Q1–Q5 and Owner no-downgrade floor

The five questions are a competence examination for the next unresolved implementation boundary, never a task checklist.

Before authoring them, inspect current Owner instructions, issue appendix/questions, Owner roadmaps and accepted handovers for Owner-authored technical questions/challenges. Record baseline discovery. If Owner questions exist, they are the minimum difficulty/coverage floor.

The active pack may reorganize or strengthen them but may not silently remove supplied numerical values, coordinates, loads, geometry, materials, integration points, requested derivations, required mechanisms, independent oracles, falsifiers or negative controls. Bind a JSON coverage manifest under the chain and validate it with `validate_owner_qualification_baseline.py`.

For profile version 2, each detailed question carries `Concrete payload:` and `Required derivation:`. FEA/WRC/Load Calc/fixed-format work requires at least two hand-computable concrete payload questions; Q2/Q4 normally contain actual numerical payload and derivation. Technical vocabulary alone is insufficient.

Minimum set quality remains:

```text
>= 2 numerical/hand or equivalent exact technical reconstructions
>= 3 questions with exact live-repository anchors
>= 1 end-to-end production trace
>= 1 independent engineering oracle
>= 1 explicit falsifier
>= 1 exact safe-patch + NO-PATCH boundary
```

Questions such as `Explain the solver`, `List the claims`, `Describe the benchmark`, `Which file would you inspect?` or `Reconstruct the T6 Jacobian` without known element data are insufficient when stronger evidence is available.

Read `qualification.md`, `qualification-profiles.md` and `owner-qualification-baseline.md`.

## 7. Engineering evidence expectations

Where relevant distinguish source/input authority → geometry/topology → stiffness/load assembly → solver equilibrium → local recovery → transformation/load transport → result contract → presentation/publication.

For structural/FEA discrepancies use as applicable six-DOF equilibrium/residual checks, free-body cuts, `q = K u - f_fixed - f_initial`, DOF ordering, end-I/end-J, local/global axes, moment-reference transport, raw-solver trace and an analytical/authoritative/experimental/independent cross-solver oracle. Do not change several mechanics when a single-factor falsifier can isolate the first wrong boundary.

## 8. Takeover qualification and recovery

On agent loss/custody change:

```text
minimal READ_ONLY locator bootstrap
→ question-set admission
→ TAKEOVER QUALIFICATION FIRST
→ independent PASS_QUALIFIED_READ_ONLY
→ post-basis reconciliation while READ_ONLY
→ drift classification
→ retain / independently confirm / requalify
→ WRITE_ALLOWED only when current-state authority is safe
```

The candidate cannot self-admit its questionable exam, self-verify, self-confirm material qualification coverage or infer write authority from qualification PASS.

## 9. Validation integrity

Every material check distinguishes:

```text
STATUS      = PASS | FAIL | NOT_RUN | NOT_APPLICABLE
OBSERVATION = execution | source inspection | artifact inspection | inference
ORACLE      = implementation-coupled | independent reproduction |
              analytical | authoritative reference | cross-solver | experimental
```

Never promote source inspection, mergeability, compilation not run, empty workflow jobs or transport failure into engineering PASS. Never weaken tolerances because a case fails, replace independent expected values with production output, change implementation and oracle together and call it independent, delete hard benchmarks to obtain green state or hard-code benchmark answers.

## 10. Handover readiness is evidence-derived

New successor endpoints use:

```text
HANDOVER_PROTOCOL_VERSION: 2
HANDOVER_CONTENT_READY: TRUE | FALSE
HANDOVER_VALIDATION_STATUS: PASS | FAIL | NOT_RUN
HANDOVER_VALIDATION_EVIDENCE: <durable evidence or NONE>
HANDOVER_READY: TRUE | FALSE
REPORTING_CONTRACT: ACTIVE_HANDOVER_FIRST
HANDOVER_RESPONSE_REQUIRED: ALWAYS
RESPONSE_DELTA_MODE: DELTA_ONLY
```

`HANDOVER_READY: TRUE` requires content ready + validation PASS + non-empty evidence. If validation is NOT_RUN/FAIL, preserve the baton but keep `HANDOVER_READY: FALSE`.

## 11. User-visible response contract — every bounded repository-work response

Any response that performed, attempted, audited, blocked, resumed, advanced, completed or re-grounded repository work starts with:

```text
# Active handover snapshot
```

No narrative prose precedes it. This includes `proceed next`, AUTO, audit-only turns, blockers, NOT_RUN, PR create/update, review gates, merge gates and task completion.

The State Card targets `<220 words` and excludes the questions. Immediately after it show the **full** active Q1–Q5; do not compress them into topic labels. Then, if needed:

```text
## Changed this turn
```

with at most eight concise bullets unless the Owner explicitly requests a detailed report.

Required State Card information: repo/task/chain/endpoint, PR/branch/head/main/status, merge authority, engineering/custody/qualification/write/AUTO states, protocol, roadmap, inputs/benchmarks/source pointers, blocker, leg diagnosis and exact next action.

It is invalid to say only `the endpoint contains Q1-Q5`.

Read `handover-snapshot.md` and `reality-check-p0.md`.

## 12. Scope, AUTO and merge

One coherent assignment per PR unless Owner changes scope. Keep changes surgical. If intent/authority/commit classification cannot be reconstructed safely, use `CONTINUE | SALVAGE_PARTIAL | SUPERSEDE | ABANDON`.

AUTO progresses only within the approved mission. It does not authorize scope expansion, authority changes, benchmark/oracle changes, roadmap mutation, validation weakening, destructive operations or merge. Merge authority remains independent and Owner-controlled unless explicitly granted.

## 13. Completion

Distinguish `AGENT_LEG_COMPLETE`, `PR_COMPLETE`, and `CHAIN_COMPLETE`. PR merge alone does not imply chain completion.
