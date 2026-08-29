# Repository Agent Policy — shared engineering-pr-delivery-v2 rules

This file is the reusable cross-repository policy for repositories adopting `engineering-pr-delivery-v2`. Repository-root `AGENTS.md` files are **project overlays**, not copies of this protocol.

## 1. Policy layering

The authority order is:

```text
explicit current Owner instruction
→ repository project overlay (`AGENTS.md`)
→ this shared repository-agent policy
→ engineering-pr-delivery-v2 `SKILL.md` + references
```

A project overlay may be stricter for its own domain. It may not silently weaken qualification, source/oracle custody, validation truth, owner-roadmap authority, chain/custody controls, anti-gaming rules, or merge authority.

Repository overlays should contain only project-specific facts such as:

- project identity and engineering criticality;
- repository-specific roadmaps and source authorities;
- protected solver/method/data/publication domains;
- project-specific validation commands and benchmarks;
- project-specific AUTO hard stops;
- local workflow/release restrictions that are stricter than Common.

Do **not** duplicate the reusable relay state machine, qualification sequence, Q1–Q5 schema, canonical chain paths, generic AUTO semantics, generic merge rules, or crash-recovery procedure into downstream `AGENTS.md` files. Duplicated generic policy becomes stale authority.

## 2. Protocol-adoption gate — before every new material leg

Before material coding, source-governance mutation, benchmark/oracle mutation, engineering-result publication work, or AUTO progression into a new leg, re-ground the reusable protocol.

Record in the active endpoint:

```text
COMMON_PROTOCOL: engineering-pr-delivery-v2
COMMON_PROTOCOL_BASIS: <live Common commit SHA>
COMMON_PROTOCOL_STATUS: CURRENT | STALE_PROTOCOL | UNKNOWN
CHAIN_STATE_VERSION: 3
```

`COMMON_PROTOCOL_BASIS` is the Common commit actually read for this leg, not an inherited endpoint pin.

If the repository project overlay declares a minimum acceptable Common basis, the live/read basis must contain that basis or a later compatible revision. A failed network transport does not authorize falling back to an old protocol when another repository-access channel is available.

Fail closed:

```text
STALE_PROTOCOL | UNKNOWN
→ NO_MATERIAL_CODING
→ NO_AUTO_PROGRESSION
→ READ_ONLY protocol reconciliation
```

## 3. Canonical relay paths

For every new chain, takeover migration, or new material leg that is not explicitly grandfathered history:

```text
agents/chains/<CHAIN_ID>/ACTIVE.md
agents/chains/<CHAIN_ID>/endpoints/<ENDPOINT_ID>.md
agents/qualifications/<CHAIN_ID>/**
```

Use `CHAIN_STATE_VERSION: 3`.

Legacy history is read-only evidence:

```text
agents/agentchain.md
agents/agentchain/<CHAIN_ID>/**
agents/PR*_workreport.md
agents/status/**
agents/claims/**
```

Allowed on legacy artifacts:

```text
READ / CITE / RECOVER / MIGRATION-PROVENANCE
```

Not allowed for a new material leg:

```text
NEW ENDPOINT
NEW ACTIVE POINTER
NEW AUTO LEG
NEW TAKEOVER CUSTODY
```

Do not update a legacy shared index merely to announce a new v3 endpoint. Discover active traffic from `agents/chains/*/ACTIVE.md`. Historical files are not deleted or mass-rewritten.

## 4. Handover-ready before work, not after work

Crash readiness is a write-ahead control.

Before each material engineering batch, the accepted active endpoint must already contain:

- the intended bounded `Exact next action`;
- hypothesis and falsifier;
- protected authority/engineering boundaries;
- expected changed domains;
- inputs, benchmarks, governing docs, sources, production and validation paths;
- a current, expert Q1–Q5 pack for a replacement agent.

Sequence:

```text
PROTOCOL ADOPTION GATE
→ PRE-WORK V3 ENDPOINT
→ Q1–Q5 QUALITY VALIDATION
→ MATERIAL WORK
→ VALIDATION TRUTH
→ SUCCESSOR ENDPOINT BEFORE NEXT MATERIAL BATCH
```

Do not code first and manufacture the takeover exam afterward.

If the pre-work endpoint or Q pack is missing/invalid, AUTO MODE pauses before mutation.

## 5. Expert Q1–Q5 requirements

Use the qualification standard in `qualification.md`. The five questions are a competence examination for the **next unresolved implementation boundary**, never a task checklist.

For engineering-critical numerical work, the pack should normally force the candidate to perform real technical work, not merely explain repository prose. Examples include:

- actual element/node/load-case reconstruction;
- stiffness/load assembly or recovery arithmetic;
- Jacobian / determinant / transformation calculation;
- WRC/local-axis/load-transfer hand calculation;
- equilibrium/free-body/residual reconstruction;
- fixed-format pointer/cardinality/byte-span arithmetic;
- exact parser/state/hash reconstruction;
- independent source or published benchmark calculation.

Where applicable require:

```text
>= 2 numerical/hand or equivalent exact technical reconstructions
>= 3 questions with exact live-repository anchors
>= 1 end-to-end production trace
>= 1 independent engineering oracle
>= 1 explicit falsifier
>= 1 exact safe-patch + NO-PATCH boundary
```

Questions such as `Explain the solver`, `List the claims`, `Describe the benchmark`, `Which file would you inspect?`, or source-reading comprehension without implementation reconstruction are insufficient when stronger implementation/calculation evidence is available.

## 6. Engineering evidence expectations

Where relevant, distinguish:

```text
input/source authority
→ geometry/topology
→ stiffness/load assembly
→ solver equilibrium
→ element/local recovery
→ local/global transformation
→ moment/load transport
→ result contract
→ presentation/publication
```

For structural/FEA discrepancies, require as applicable:

- six-DOF equilibrium/residual checks;
- free-body cuts;
- `q = K u - f_fixed - f_initial` or method-equivalent reconstruction;
- units, DOF ordering and end-I/end-J verification;
- local/global axes and transformation matrices;
- load/moment reference-point transport;
- trace from reported result back to raw solver quantity;
- analytical, authoritative-reference, experimental, or independent cross-solver evidence.

Do not change several mechanics at once when a single-factor falsifier can isolate the first wrong boundary.

## 7. Takeover qualification and recovery

On agent loss or custody change:

```text
minimal READ_ONLY locator bootstrap
→ question-set admission
→ TAKEOVER QUALIFICATION FIRST
→ independent PASS_QUALIFIED_READ_ONLY
→ post-basis reconciliation while READ_ONLY
→ post-basis drift classification
→ retain / independently confirm / requalify
→ WRITE_ALLOWED only when current-state authority is safe
```

The candidate cannot self-admit its own questionable exam, self-verify, self-confirm material qualification coverage, or infer write authority from qualification PASS.

## 8. Validation integrity

Every material check distinguishes:

```text
STATUS      = PASS | FAIL | NOT_RUN | NOT_APPLICABLE
OBSERVATION = execution | source inspection | artifact inspection | inference
ORACLE      = implementation-coupled | independent reproduction |
              analytical | authoritative reference | cross-solver | experimental
```

Never promote source inspection, mergeability, compilation not actually run, empty workflow jobs, or transport failure into engineering PASS.

Never weaken tolerances because a case fails, replace an independent expected value with production output, change implementation and oracle together and call it independent, delete difficult benchmarks to obtain green state, or hard-code benchmark answers into production.

## 9. Scope, damaged work, AUTO and merge

One coherent assignment per PR unless the Owner changes scope. Keep changes surgical and explain each changed file. Do not silently broaden authority.

If intent cannot be reconstructed safely, authority is unclear, commits cannot be classified, or conflict resolution would require guessing engineering intent, use:

```text
CONTINUE | SALVAGE_PARTIAL | SUPERSEDE | ABANDON
```

`AUTO MODE` progresses only within the approved mission. It does not authorize scope expansion, engineering-authority changes, benchmark/oracle changes, roadmap mutation, validation weakening, destructive operations, or merge.

Merge authority is independent and Owner-controlled unless explicitly granted.

## 10. User-visible handover requirement

At every substantive stop, PR creation/update boundary, blocker, owner-decision boundary, merge boundary, or explicit handover, the agent's user-facing response must show the active handover snapshot itself. It is invalid to say only `the endpoint contains Q1–Q5`.

The visible handover must include, concisely:

```text
Repo / task / chain / endpoint
PR / branch / head / main / status
roadmap + inputs + governing/source pointers
engineering/custody/qualification/write state
current blocker + exact next action
Q1
Q2
Q3
Q4
Q5
```

The concise visible snapshot target remains `<300 words`; detailed evidence remains in the endpoint.

## 11. Completion

Distinguish:

```text
AGENT_LEG_COMPLETE
PR_COMPLETE
CHAIN_COMPLETE
```

A completed chain is terminal only when the engineering mission is objectively complete. PR merge alone does not imply chain completion.
