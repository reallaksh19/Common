# Durable Execution Lineage and Projection (DELP) — V3.2

Status: **normative for V3.2 as an Owner-directed additive amendment** of the otherwise frozen V3.2 tree (see [Amendment of V3.2](#amendment-of-v32)). Implemented by `scripts/delp_projection_v32.py`, validated by `schemas/delp-*-v32.schema.yaml` and pinned by `tests/test_delp_projection_v32.py`. The same contract is the active design of V3.5 (`skills/engineering-pr-delivery-v3.5/operating-model/durable-execution-lineage-projection-v35.md`); the two modules are identical apart from their protocol-line and schema-id constants.

## The rule

> **Agents publish facts. Everything else is recomputed from those facts.**
>
> An agent states, about its own leaf responsibility only: which declared units it reports complete, the verification result, the durable evidence refs, the candidate those refs cover, and the next unit. It never writes a percentage, a title, a weight, a frontier count, an activity epoch, an evidence-health verdict or any parent/programme number. Those are projections; the DELP projector derives them, and any facts record that tries to author one is **rejected and cannot move any number**.

This is not a title-formatting rule. It is an execution identity, lineage, evidence, projection and concurrency rule: a fresh or interrupted executor must be able to answer *what exactly am I working on, which parent does it belong to, which PR and candidate does the latest evidence cover, how complete is it, is that progress actually evidenced, and what happens next* from durable truth, never from conversation memory.

## Three authorities (never merged)

```text
PROGRAMME AUTHORITY   Human Owner / explicitly delegated programme authority
                      -> owns scope, priority, the execution graph (plan) and its denominators
EXECUTION CUSTODY     the agent currently performing ONE bounded leaf responsibility
                      -> owns facts about that leaf, nothing above it
STATUS PROJECTION     deterministic reconstruction from graph + facts + observed material truth
                      -> owns no engineering authority; disposable and rebuildable
```

A parent issue needs no permanently assigned agent. A projection never grants permission. An agent never owns programme truth.

## What an agent publishes — `CHECKPOINT_FACTS_V1`

Inside a `TASK_EVIDENCE` comment (the publication family is unchanged; this is the machine-readable core of the existing `TASK_EVIDENCE — CHECKPOINT`), one fenced YAML block:

````text
TASK_EVIDENCE — CHECKPOINT

<free prose for humans: claim, consequence, negative knowledge ...>

```yaml
CHECKPOINT_FACTS_V1:
  responsibility: {issue: Common#592, id: P3-I-R2}
  material: {pr: Common#593, candidate_sha: 0123456789abcdef0123456789abcdef01234567}
  units:
    - id: U04
      state: COMPLETE                    # COMPLETE | IN_PROGRESS | NOT_STARTED
      result: VERIFIED                   # VERIFIED | PARTIAL | FAILED | NOT_RUN | PENDING
      evidence_refs: [Common#592#issuecomment-12345]
  next: {unit: U05, action: negative replay}
  blocker: NONE
  owner_action: NONE
```
````

Allowed fields: `responsibility`, `material`, `units[]` (`id`, `state`, `result`, `evidence_refs`, optional `candidate_sha`, `contract_digest`), `gates[]` (reviewer/super-reviewer delivery gates: `id`, `result`, `evidence_refs`), `activity` (`ACTIVE`, `WAITING_CI`, `WAITING_TOOL`, `WAITING_EXTERNAL`, `WAITING_PROVIDER_VISIBILITY`, `RECOVERING`, `PAUSED`), `next`, `blocker`, `owner_action`, `result` (scope + `responsibility_complete`, optional `superseded_by`).

**Rejected, recursively, at any depth:** `progress`, `percent`, `p`/`e`/`d`, `title`, `parent_progress`, `programme_progress`, `frontier(_count)`, `activity_epoch`, `evidence_health`, `projection`, `light`, `denominator`, `weight(s)`, `reserve(_weight)`, `evidenced`, and any string that contains projection notation (`R:P…/E…`, `Φ:D…/E…`, `Π:D…/E…`, `{P…% · E…%`). `QUIET` and `STALE` can never be declared: a dead executor cannot report its own death, so liveness comes only from an external observer. Weights are plan authority and live only in the execution graph.

`python scripts/delp_projection_v32.py validate-facts <file>` exits non-zero on any violation. The projector applies the same validation to every ledger record: an invalid record is listed under `rejected_facts` and contributes nothing.

**Who may publish facts.** Anyone can comment on a public issue, so `sync-github` believes a facts block only from a trusted author: an explicit `programme.fact_authors` login list in the execution graph, or, when absent, a repository `OWNER`/`MEMBER`/`COLLABORATOR`. A block from anyone else is kept in the ledger, rejected with `author … is not a trusted fact author` and counted nowhere. Facts must also name a declared **leaf** (and the planned `responsibility_id` when both exist); a record for a parent issue or an unknown issue is rejected.

## The execution graph (plan authority)

```yaml
schema: relay-v3.2-delp-execution-graph
programme: {id: COMMON-PROD-CONTROL-V1, root: Common#527}
nodes:
  - {ref: Common#527, kind: ROOT}
  - {ref: Common#588, kind: INTERMEDIATE, parent: Common#527, weight: 3}
  - ref: Common#592
    kind: LEAF
    parent: Common#588
    weight: 3
    responsibility_id: P3-I-R2
    primary_pr: Common#593          # or candidate_ref: <branch> while there is no PR
    critical: true
    units: [{id: U01, weight: 20}, {id: U02, weight: 30}, {id: U03, weight: 25}, {id: U04, weight: 25}]
```

- Lineage and denominators are typed and explicit; nothing is inferred from titles or free-text "related" lists.
- **Parent issues are not execution workspaces.** Material work is a `LEAF`; a facts record addressed to a non-leaf issue is rejected.
- A split conserves weight; progressive decomposition consumes an explicit `reserve_weight`, which counts as zero progress and blocks `COMPLETE`; true scope expansion changes the denominator by editing the graph (record it as `PLAN_UPDATE — SCOPE_EXPANSION`). A percentage may legitimately fall; the projector never renormalises to preserve one.
- `delivery_gates` (+ `coder_weight`, default 60 when gates exist) keep Coder `P100` from meaning delivery `D100`: reviewer acceptance, super review and final hand-off add delivery weight only with their own current evidence.
- A leaf also carries its **decomposition contract** (`outcome`, `size_budget`, `write_surface`, `depends_on`, a `verify` step per unit). The progress maths never reads it; the [decomposition gate](#decomposition-gate--small-verifiable-collision-free-leaves) judges it.

## How numbers are computed

```text
leaf P  = Σ weight(units whose latest claim is COMPLETE)            / Σ weight(units)
leaf E  = Σ weight(COMPLETE units with CURRENT evidence)            / Σ weight(units)      (E <= P by construction)
leaf D  = (coder_weight·P  + Σ weight(gates PASSED))                / (coder_weight + Σ weight(gates))
leaf DE = (coder_weight·E  + Σ weight(gates PASSED with current evidence)) / same denominator
node  D = Σ(wᵢ · Dᵢ) / (Σ wᵢ + reserve)       node E = Σ(wᵢ · DEᵢ) / (Σ wᵢ + reserve)       (recomputed, never incremented)
```

`CURRENT evidence` for a unit means *all* of: latest claim is `COMPLETE`; `result` is in the leaf's accepted verification set (default `VERIFIED`); at least one evidence ref; the claim's `candidate_sha` **equals the live candidate** (primary PR head, or `candidate_ref` head); the claim names the planned PR; and, when the graph pins one, the `contract_digest` matches. Otherwise the unit is a visible gap with a named reason (`NO_EVIDENCE_REFS`, `RESULT_NOT_ACCEPTED(x)`, `CANDIDATE_MISMATCH`, `CANDIDATE_UNOBSERVED`, `PR_MISMATCH`, `CONTRACT_DIGEST_MISMATCH`). A moved candidate therefore lowers `E` without touching `P`, until the evidence is replayed on the new head — evidence for an older candidate never silently certifies the new one. An unobservable candidate is treated conservatively by the pure engine (`UNVERIFIABLE`, `E` not counted), but `sync-github` aborts the whole pass — no writes, non-zero exit — when a live candidate cannot be read, so a provider outage never publishes a misleading drop.

Display percent is exact-rational → half-up, and never shows `100` unless exactly full or `0` unless exactly empty. Exact ratios (`"9/16"`) are kept in the projection for audit.

Evidence health: `CURRENT`, `GAP`, `STALE_CANDIDATE`, `UNVERIFIABLE`. Complete is earned only when the leaf result says `RESPONSIBILITY`/`YES`, every unit is complete **with current evidence**, and every delivery gate is passed **with current evidence**; a premature `YES` is ignored and flagged (`RESULT_CLAIMS_COMPLETE_BUT_UNITS_OPEN`, `COMPLETE_CLAIM_WITHOUT_CURRENT_EVIDENCE`, `COMPLETE_CLAIM_WITH_OPEN_DELIVERY_GATES`, `COMPLETE_CLAIM_WITH_UNEVIDENCED_DELIVERY_GATES`). `activity`, `next`, `blocker` and `owner_action` take the most recent *stated* value, so a reviewer's gates-only record never resets the Coder's blocker or next unit.

## Title grammar (generated; never authored)

```text
leaf          🟢 [#527 › #588 › #592 → PR#593] R:P65/E65 · U04 · ACTIVE — <responsibility>
intermediate  🟢 [#527 › #588 → #592/PR#593] Φ:D60/E58 · F2 · ACTIVE — <phase>
programme     🟢 [#527] Π:D72/E70 · F3 · ACTIVE — <programme>
```

`›` is ownership/hierarchy; `→` is the material PR relation (a PR is not another programme child). `P`/`D` are semantic/delivery progress, `E` is the evidenced part of it, `F` is the number of active frontier leaves under the node. The scope letter is mandatory: a bare `P56% / E56%` is invalid. Active-unit token: the agent's `next.unit` if it names a declared incomplete unit, otherwise the first incomplete unit.

State words → light: `ACTIVE 🟢`; `WAITING_* / WAITING 🔵`; `EVIDENCE_GAP`, `EVIDENCE_STALE`, `QUIET`, `RECOVERING`, `NOT_RELEASEABLE`, `PLAN_GAP 🟡`; `STALE 🔴`; `COMPLETE ✅`; `NOT_STARTED`, `PAUSED`, `SUPERSEDED`, `IDLE ⚪`. Ancestor state is derived from the subtree without averaging colours: red if a `critical` leaf is stale; yellow for any evidence gap/stale, critical quiet/recovering or non-critical stale; blue if only critical work is waiting; green while frontier work is active; `PLAN_GAP` (yellow) only when the decomposition gate is `ENFORCED`, nothing is active and a leaf below fails the gate; `COMPLETE` only when every leaf is terminal, delivery is 100 and no reserve remains.

The human part (`— <responsibility>`) is the only thing an agent or Owner edits. The projector splits an existing title into generated prefix + base, recognising the legacy forms `🟢 {P42% · E31% · A07 · U03 · ACTIVE} <title>` and `<title> {P50% · E50% · UNIT-02 · IMPLEMENTING}`, so migration is automatic at the next pass. Titles are capped at 250 characters by truncating the human base, never the projection. `A<n>` (activity epoch) is no longer in the title; it is `activity_epoch` in `LIVE_STATUS_V1`.

**Drift correction.** GitHub cannot stop a hand edit, so DELP makes it non-authoritative and self-healing: every pass recomputes the expected title; a differing title is classified (`STALE_OR_HAND_EDITED`, `MISSING_PROJECTION`, `LEGACY_FORMAT`), rewritten, and the write reports `title_corrected: true`. `verify-titles` exits `2` when any title drifted.

## Worked lifecycle (pinned by `test_documented_lifecycle_walkthrough`)

Graph: programme #527 → phase #588 (weight 3: leaf #592 weight 3 with units 20/30/25/25 and PR #593; leaf #594 weight 1) and phase #610 (weight 1). Only #592 is shown; #594 and #610 are untouched.

| Event | Evidence (what an agent publishes) | Leaf title | Phase #588 | Programme #527 |
|---|---|---|---|---|
| Leaf created | nothing | `⚪ [#527 › #588 › #592 → PR#593] R:P0/E0 · U01 · NOT_STARTED` | `⚪ … Φ:D0/E0 · F0 · IDLE` | `⚪ [#527] Π:D0/E0 · F0 · IDLE` |
| U01+U02 done, verified @A | facts: U01,U02 `COMPLETE/VERIFIED` + refs | `🟢 … R:P50/E50 · U03 · ACTIVE` | `🟢 … Φ:D38/E38 · F1 · ACTIVE` | `🟢 [#527] Π:D28/E28 · F1 · ACTIVE` |
| U03 done, evidence forgotten | facts: U03 `COMPLETE`, no refs | `🟡 … R:P75/E50 · U04 · EVIDENCE_GAP` | `🟡 … Φ:D56/E38 · F1 · EVIDENCE_GAP` | `🟡 [#527] Π:D42/E28 · F1 · EVIDENCE_GAP` |
| Next `continue` → recovery evidence | facts: U03 refs added | `🟢 … R:P75/E75 · U04 · ACTIVE` | `🟢 … Φ:D56/E56 · F1 · ACTIVE` | `🟢 [#527] Π:D42/E42 · F1 · ACTIVE` |
| PR head moves A→B (a push) | nobody publishes anything | `🟡 … R:P75/E0 · U04 · EVIDENCE_STALE` | `🟡 … Φ:D56/E0 · F1 · EVIDENCE_GAP` | `🟡 [#527] Π:D42/E0 · F1 · EVIDENCE_GAP` |
| Replay verified @B | facts: U01–U03 @B | `🟢 … R:P75/E75 · U04 · ACTIVE` | `🟢 … Φ:D56/E56 · F1 · ACTIVE` | `🟢 [#527] Π:D42/E42 · F1 · ACTIVE` |
| U04 done @B + `RESPONSIBILITY`/`YES` | facts: U04 + result | `✅ … R:P100/E100 · COMPLETE` | `⚪ … Φ:D75/E75 · F0 · IDLE` | `⚪ [#527] Π:D56/E56 · F0 · IDLE` |
| Test rerun, nothing changed | – | unchanged | unchanged | unchanged (same `input_digest` ⇒ no write) |

## `LIVE_STATUS_V1` and compare-and-swap

Each node has one managed comment (`<!-- relay-delp:live-status:start -->`) carrying a JSON document and a marker `<!-- relay-delp:version=N digest=sha256:… -->`. The document is derived, disposable, never edited by agents, and valid against `schemas/delp-live-status-v32.schema.yaml` (identity/lineage, material, execution state, evidence health and gaps, progress, frontier, `activity_epoch`, `next`, `blocker`, `owner_action`, warnings, `projection.version`, `projection.input_digest`).

Writes are **not last-writer-wins**. The writer reads version *N*, recomputes, and writes *N+1* only if the surface still shows *N*; it re-reads before writing, writes, then reads back version and digest. A lost race (stale expected version, or a readback that shows another writer's version) raises `ProjectionConflict`; the caller drops cached inputs, recomputes from fresh truth and retries (bounded). Identical `input_digest` and title ⇒ `UNCHANGED`, no write. GitHub offers no conditional comment/title update, so this is detect-and-retry; because a projection is a pure function of durable inputs, a retried write converges to the same value. Provider failure is observability debt only and never blocks engineering.

## Continuation admission

`continue`, `proceed`, `next`, `resume`, `reconcile`, `take over`, `keep going` are classified by `owner_commands.py` as `CONTINUE_RECONCILE` (and `Proceed next …` workflows gain the same barrier). They mean *reconstruct and reconcile before continuing*:

```text
resolve leaf -> resolve lineage -> observe live candidate -> read latest valid facts -> compare evidence frontier
 -> repair any evidence gap FIRST -> reproject -> compare-and-swap + read back -> compact checkpoint -> execute exactly the next bounded unit
```

```text
python scripts/delp_projection_v32.py admit --graph graph.yaml --facts facts.md --observations obs.json --leaf Common#592 --command continue
```

```text
CONTINUE CHECKPOINT

PATH: #527 → #588 → #592 → PR#593
CHILD: R:P75/E75 · U04 · ACTIVE
EVIDENCE: CURRENT @ aaaaaaa
PARENT: #588 Φ:D56/E56
ROOT: #527 Π:D42/E42
BLOCKER: NONE
OWNER_ACTION: NONE
NEXT: U04 — negative replay
```

With a gap the barrier forces recovery first (`NEXT: RECOVER_EVIDENCE before new coding — U03:NO_EVIDENCE_REFS`, `recovery_required: true`). When the decomposition gate is `ENFORCED` and the leaf's plan fails it, the barrier answers `FIX_PLAN` before anything else (see [the gate](#decomposition-gate--small-verifiable-collision-free-leaves)); an evidence gap is still reported alongside it. Admission is pure: `authority_effects` is always empty — a continuation never changes the parent, denominator, scope, priority or merge authority; a genuine priority change is an explicit custody transition (`PAUSED` at an exact durable frontier, successor `ACTIVE` after fresh reconstruction).

## Decomposition gate — small, verifiable, collision-free leaves

DELP keeps progress honest *after* a plan exists. The gate makes the plan itself fit to hand to an agent *before* work starts, with the same discipline: the Coordinator authors the plan, a pure function judges it, the verdict is derived and disposable, and an agent cannot argue with it by publishing a fact (a facts record carrying a `plan` field is rejected: it is not an allowed field). **The gate never moves a percentage**; it only adds a `plan` block, the states `NOT_RELEASEABLE` / `PLAN_GAP` and the admission action `FIX_PLAN`.

### The leaf contract

```yaml
programme:
  total_weight: 10000                 # display scale for "unit points"; never changes a percentage
  decomposition_policy: {mode: ENFORCED}   # OFF (default) | ADVISORY | ENFORCED
nodes:
  - ref: Common#594
    kind: LEAF
    parent: Common#588
    weight: 1
    primary_pr: Common#595
    work_class: PRODUCT               # PRODUCT (default) | MECHANICAL | GATE
    outcome: Replay results are published as TASK_EVIDENCE with durable refs.
    size_budget: {target_loc: 400, hard_loc: 900, target_minutes: 12, hard_minutes: 18}
    write_surface: [src/replay/, docs/replay.md]   # files, or directories ending in '/'; no globs
    depends_on: [Common#592]          # ordering between leaves
    units:
      - {id: V1, weight: 40, verify: the publisher emits CHECKPOINT_FACTS_V1}
      - {id: V2, weight: 30, verify: evidence refs resolve to the replay artefacts}
      - {id: V3, weight: 30, verify: docs/replay.md matches the shipped command}
```

| Rule (defaults) | Finding | Severity |
|---|---|---|
| 3–8 units per `PRODUCT` leaf | `UNITS_BELOW_MIN`, `UNITS_ABOVE_MAX` (the ceiling applies to every class) | blocker |
| no unit above 40% of the leaf (exact integer comparison) | `UNIT_SHARE_OVER` | blocker |
| every unit names how it is verified | `UNIT_VERIFY_MISSING` | blocker |
| the leaf states one observable outcome | `OUTCOME_MISSING` | blocker |
| the leaf declares its write surface | `WRITE_SURFACE_MISSING` | blocker |
| the leaf declares all four `size_budget` keys | `SIZE_BUDGET_MISSING`, `SIZE_BUDGET_INCONSISTENT` (target above hard) | blocker |
| declared hard cap within 1500 LOC / 20 min | `SIZE_OVER_HARD`, with the number of leaves it would take at target size | blocker |
| declared target within 700 LOC / 15 min | `SIZE_OVER_TARGET` | advisory |
| `PRODUCT` leaf target of at least 50 LOC | `LEAF_TOO_SMALL` (an issue and a PR cost more than the work) | advisory |
| overlapping write surfaces are ordered by `depends_on` (transitively) or declared `parallel_ok` | `WRITE_SURFACE_COLLISION` on both leaves | blocker |
| `parallel_ok` carries a `parallel_ok_basis` | `PARALLEL_BASIS_MISSING` | blocker |

`MECHANICAL` and `GATE` leaves (rote batch work, review-only leaves) are exempt from the unit-count floor and the share cap **only**; every other rule still applies, and `decompose-check` prints how many leaves use each class so an over-used exemption is visible in review. Leaves that are `COMPLETE` or `SUPERSEDED` are history and are not judged, and they do not collide with anything (the projection always knows which they are; `decompose-check` knows when given `--facts`). Write surfaces are matched as repo-relative paths: a file equals itself, a directory prefix (trailing `/`) covers everything beneath it, and `src/59/` does not cover `src/592/`.

**Why these defaults.** They follow the written budgets in `PROGRAMME_DECOMPOSITION_PROGRESS.md` (700 target / 1500 hard changed lines, 15 / 20 minutes) and sit near the Young/Daly interval `√(2·δ·M)` for work that is interrupted at random: δ is the cost of a checkpoint and M the mean time between interruptions. Informative, not normative: on the Common executors on 6–7 October 2026 roughly nine interruption episodes (connection loss, stream errors, usage waits) occurred in under seven hours and a checkpoint cost about four minutes, so `√(2·4·45) ≈ 19` minutes. Recompute it with your own rates and override `decomposition_policy.leaf_budget`; `graph-diff` turns any loosening into a recorded Owner decision.

### Modes and what each one changes

| Mode | `decompose-check` | Projection | Admission |
|---|---|---|---|
| `OFF` (default) | informational, exit 0 | no `plan` block, state, title or warning is added; node output is identical to a graph without a policy | unchanged |
| `ADVISORY` | exit 0 | `plan` block and `DECOMPOSITION_BLOCKERS:…` / `DECOMPOSITION_ADVISORIES:…` warnings; no state or title change | `PLAN: WOULD_BLOCK (advisory) — …` line; action unchanged |
| `ENFORCED` | exit 1 on any blocker | a failing leaf becomes `NOT_RELEASEABLE` 🟡 (it replaces `NOT_STARTED` and `ACTIVE` only; every other state is more urgent or already means the leaf is not being worked, and stays); an ancestor shows `PLAN_GAP` only when nothing below it is active and no more urgent state applies | `FIX_PLAN before coding — <code (detail)>… — request a plan update (split or reweight) from the Coordinator; do not start or continue units` |

A leaf that is `NOT_RELEASEABLE` keeps its real `lifecycle` and still counts on the frontier if it is active. Adopt it in three steps: leave it `OFF`; run `decompose-check --mode ADVISORY` to see every finding with no effect; fix the plan; then set `ENFORCED`. `require: {outcome: false, …}` lets a programme enforce only part of the contract while it adopts the rest.

### Re-planning must conserve progress — `graph-diff`

A split, merge, reweight or drop is a plan change and the easiest place to manufacture or lose progress. Every unit and delivery gate has an exact **share of the whole programme**:

```text
share(unit) = Π (sibling weight / (Σ sibling weights + reserve)) down the lineage × leaf coder share × (unit weight / Σ unit weights)
points      = share × programme.total_weight                      (display only)
```

The shares plus every reserve sum to 1, so any change that does not conserve a share moves somebody else's. `graph-diff --old <plan being replaced> --new <proposed plan>` compares them per item (a moved unit is followed through `moved_from: <old leaf>`, same unit id):

| Finding | Meaning | Severity |
|---|---|---|
| `POINTS_DRIFT` | a persisting unit or gate changed share and no covering **new** plan update exists | blocker |
| `UNIT_LOST` | a unit or gate disappeared with no covering `UNIT_DROPPED` / `SCOPE_REDUCTION` | blocker |
| `MOVE_ORIGIN_UNKNOWN`, `MOVE_DUPLICATE` | `moved_from` names work the old plan never had, or one old unit is claimed twice | blocker |
| `PLAN_UPDATE_UNAUTHORISED` | a new update lacks `owner_authorized: true` or an `owner_basis` | blocker |
| `PLAN_HISTORY_CHANGED` | an earlier update was edited or removed (`plan_updates` is append-only) | blocker |
| `POLICY_WEAKENED` | mode, limits or `require` loosened without a `POLICY_CHANGE` update | blocker |
| `PLAN_UPDATE_UNUSED` | a new update covers nothing in this change | advisory |

A conserving split needs no update. Worked example (pinned by `PlanConservation`): leaf #592 (weight 3, units U01 20 / U02 30 / U03 25 / U04 25) under #588 beside #594 (weight 1). Move U03 and U04 into a new sibling #620 and rescale the siblings so the parent's denominator is unchanged: #592 keeps weight 3 with U01/U02, #594 becomes weight 2, #620 gets weight 3 with U03/U04 (`moved_from: Common#592`). Every unit keeps its share (U03 stays 9/64 of the programme, 1406.25 points), so the diff reports `CONSERVED` with `moved 2`. Give #620 weight 1 instead and every unit under #588 drifts — U03 falls to 625 points — and the diff names each one. Decomposing `reserve_weight` into new leaves at the same total conserves the existing shares and needs no update; adding scope dilutes everybody and is declared once:

```yaml
plan_updates:                         # append-only
  - id: PU-2026-10-07-01
    kind: SCOPE_EXPANSION             # SCOPE_EXPANSION | SCOPE_REDUCTION | UNIT_REWEIGHT | UNIT_DROPPED | POLICY_CHANGE
    nodes: [Common#588]               # name the node whose denominator changed (and/or units: [Common#592:U04, Common#592:gate:REVIEWER])
    reason: new replay lane added to the phase
    owner_authorized: true
    owner_basis: "Owner instruction in chat, 2026-10-07: …"
```

A `UNIT_DROPPED` update also covers the re-normalisation of the remaining units of the leaf it drops from; a `UNIT_REWEIGHT` or a node-level update covers every unit beneath the node it names. `total_weight` is a display scale: changing it is never drift.

### Where it bites

1. **Plan time (CI).** `decompose-check --graph G` fails the pull request that edits the graph; `graph-diff --old <base version> --new <head version>` fails a re-plan that does not conserve shares:

   ```text
   python scripts/delp_projection_v32.py decompose-check --graph relay/DELP_EXECUTION_GRAPH.yaml
   git show "$BASE_SHA:relay/DELP_EXECUTION_GRAPH.yaml" > /tmp/base-graph.yaml
   python scripts/delp_projection_v32.py graph-diff --old /tmp/base-graph.yaml --new relay/DELP_EXECUTION_GRAPH.yaml
   ```
2. **Task start.** Every `continue`/`proceed` passes `admit`; under `ENFORCED` an unreleasable leaf answers `FIX_PLAN` and an agent has no unit to start.
3. **Title.** `🟡 [#527 › #588 › #594 → PR#595] R:P0/E0 · V1 · NOT_RELEASEABLE` is visible to the Owner without opening anything.
4. **Mid-flight.** An agent that finds its leaf bigger than planned publishes `blocker:` text and stops at an exact frontier; the Coordinator splits the leaf and the `graph-diff` result is the evidence that no progress was created or lost.

## Multi-agent concurrency

Each agent writes facts only to its own leaf. No agent authors parent or programme state; any context may trigger `sync-github`, which reads the graph, the ledger and live PR heads, recomputes leaves first and the programme last, and writes each node with compare-and-swap. Events (`TASK_EVIDENCE` published or recovered, PR created/replaced/merged, candidate moved, unit completed, responsibility materialised/complete/superseded, dependency or denominator change, owner command admission) trigger *reprojection*, which is not the same as *progress*: a PR opening changes a title and not `P/E`; a commit can lower `E`; a rerun changes nothing.

## Operating it

```text
validate-graph --graph G                         plan is structurally valid
validate-facts F...                              reject agent-authored projections (exit 1)
project --graph G --facts F... --observations O  deterministic projection JSON (+ expected titles)
admit --graph G --facts F --observations O --leaf L --command continue
decompose-check --graph G [--mode M] [--facts F --observations O]   judge the plan against the decomposition policy (exit 1 on blockers when ENFORCED)
graph-diff --old G0 --new G1                     a re-plan must conserve every unit's share and record its scope changes (exit 1 otherwise)
verify-titles --graph G --facts F --observations O --actual-titles T     (exit 2 on drift)
sync-github --graph G --repository owner/repo    observe PR heads + CHECKPOINT_FACTS_V1 comments, write titles + LIVE_STATUS with compare-and-swap
sync-github ... --dry-run                        read-only first run: drift, rejected facts and the exact titles it would write
```

The runner (Coordinator tick or a scoped workflow) is the **only** writer of generated titles. Agents without script access are unaffected: they publish the facts block and keep working. `templates/delp-cron-workflow-v32.yml` is an inert example of a scheduled runner; it is not an active workflow.

## Legacy and compatibility

- `scripts/continuity_projection.py` snapshots now carry `projection_mode`. `init` defaults to `DERIVED_FROM_FACTS`: `unit-update --evidenced` is rejected, `E` is computed from `evidence_refs` plus an `evidence_candidate` equal to the observed head, and `sync-github` never patches the title (one title writer). `LEGACY_AGENT_ASSERTED` remains readable and behaves exactly as before, rendered with an explicit historical-warning line; a missing value is read as legacy. Nothing historical is rewritten.
- The earlier candidate title forms in `OWNER_CHECKPOINT_PROJECTION.md`, `PROGRAMME_DECOMPOSITION_PROGRESS.md` and `CHECKPOINT_AND_LIVENESS_CONTRACT.md` are superseded by this grammar; their other content (three-view architecture, information budget, checkpoint thresholds, liveness model) is unchanged.
- The compact Owner chat checkpoint (`TASK_EVIDENCE — CHECKPOINT … UNIT / DELTA / BLOCKER / OWNER_ACTION / NEXT / EVIDENCE`) is unchanged and is rendered from the same projection; the `CONTINUE CHECKPOINT` above is the admission-time form.

## Amendment of V3.2

`skills/engineering-pr-delivery-v3.2/**` was frozen by #492/#494 and is guarded in CI. The Owner explicitly instructed that this fix land in both V3.2 and V3.5. The V3.2 changes are therefore an **additive amendment**: new `delp_projection_v32.py`, its schemas and tests, the DERIVED mode of `continuity_projection.py`, the `CONTINUE_RECONCILE` intent, and the documentation updates. The freeze guard permits exactly the paths listed in `skills/Local_PR_Deliverty_v1.1/integration/frozen-v32-amendments.yaml` and fails on any other change. Governance-critical: merge remains Owner-controlled.

## Invariants (each is pinned by a test)

1. Every artifact resolves to exactly one owning leaf; every leaf resolves to exactly one programme lineage.
2. Every percentage carries its scope; a bare percentage is invalid.
3. Leaf `P/E` come from declared weighted units; `E <= P`; evidence progress never exceeds semantic progress.
4. Parent/programme `D/E` are recomputed from children, never incremented, never authored.
5. Candidate movement cannot silently preserve stale evidence qualification.
6. Missing evidence stays visible (`EVIDENCE_GAP`) until recovered; material work after a gap starts with recovery.
7. Agents publish facts on their own leaf only; agent-authored projections are rejected and inert.
8. Same inputs ⇒ same projection and same titles; concurrent writers cannot use last-writer-wins.
9. Continuation commands reconstruct before executing and never change programme semantics.
10. Parent issues with material work materialise explicit child leaves.
11. Titles and `LIVE_STATUS_V1` are disposable projections, never authority; if every title and status disappeared they would be rebuilt from durable sources.
12. The decomposition gate judges the plan only: it never reads facts, never moves a percentage, and with the mode `OFF` adds nothing to any node or admission output.
13. Under `ENFORCED`, a leaf whose plan fails the gate is never admitted to new work (`FIX_PLAN`), and a re-plan that moves any unit's programme share without a covering, authorised, append-only plan update is rejected by `graph-diff`.

## Not claimed

DELP cannot technically prevent a human or agent from hand-editing a GitHub title or comment; it makes that edit non-authoritative, detectable and self-correcting. It does not verify that an agent's evidence ref is truthful (that remains review, `NOT_RUN` integrity and the evidence gate); it verifies that evidence exists, is typed, and is bound to the current candidate. It does not grant or infer merge, acceptance or programme authority.

The decomposition gate checks that a plan is self-consistent, sized within policy and collision-free *as declared*; it cannot know whether a size estimate is honest or whether a declared `write_surface` matches the diff that is eventually pushed (comparing the two is a separate, runtime check). It checks that a `verify` step is present, not that it is a good one. A `MECHANICAL` or `GATE` classification is a Coordinator declaration, made visible by the class counts but not independently verified. `owner_authorized` and `owner_basis` in a plan update are a durable, reviewable record, not proof of who wrote them: the Owner's review of the pull request that edits the graph remains the control, and verifying the cited basis against the repository's own comments is future work.
