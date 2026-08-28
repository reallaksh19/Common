# Owner Roadmap Template

Use this structure for domain roadmaps such as `docs/roadmaps/Overallroadmap_wrc.md`.

```text
# <Domain> Overall Roadmap

ROADMAP_ID: <DOMAIN>-OVERALL
ROADMAP_REVISION: 1
ROADMAP_STATE: ACTIVE
ROADMAP_AUTHORITY: OWNER_CONTROLLED
ROADMAP_WRITE_POLICY: EXPLICIT_OWNER_AUTHORIZATION_REQUIRED
DOMAIN: <WRC / LAFEA / LoadCalc / ...>
APPLIES_TO: <paths / authority domains / products>
LAST_OWNER_DECISION_REF: <agents/chains/.../roadmap-decisions/RD-xxxx.md | INITIAL_OWNER_BASELINE>
LAST_AUTHORIZED_UPDATE: <timestamp / commit / PR>

## 1. Purpose and owner intent

State the long-horizon engineering/product objective and what successful completion means.

## 2. Authority and reading rules

- Owner intent is authoritative until Owner changes it.
- Observed status must be re-grounded against live repository evidence before relying on it.
- Agents may propose changes but may not mutate this roadmap without explicit Owner authorization.
- This roadmap does not replace codes, authoritative sources, independent benchmarks, or live repository truth.

## 3. Scope and exclusions

### In scope

### Explicitly excluded / deferred

## 4. Architecture / concept direction

Describe intended conceptual architecture, responsibility boundaries, authority boundaries, and non-negotiable design principles.

## 5. Phase / capability status

| Phase | Owner intent | Observed status | Evidence / last verified | Exit criteria |
|---|---|---|---|---|

Observed status is descriptive and may become stale. Agents must verify claims used to scope new work.

## 6. Benchmark and qualification roadmap

| Benchmark / family | Purpose | Independence class | Status | Required before |
|---|---|---|---|---|

Include closed-form, published, standards-based, cross-solver, experimental, or project benchmarks as applicable.

## 7. Source / methodology authority roadmap

| Authority item | Required source | Current state | Blocker / decision |
|---|---|---|---|

## 8. Dependencies and sequencing

| Item | Depends on | Blocks | Owner sequencing intent |
|---|---|---|---|

## 9. Acceptance / release gates

Define objective conditions required to advance major phases or declare strategic closure.

## 10. Known strategic risks

Record durable risks that affect sequencing or architecture, not ordinary PR-level defects.

## 11. Owner decisions

| Decision | Date / ref | Effect |
|---|---|---|

## 12. Agent proposals awaiting owner decision

Optional navigation only. Do not edit this section merely because a proposal exists unless Owner authorized a roadmap refresh. Proposal artifacts remain under the originating chain.

## 13. Roadmap change log

| Revision | Owner decision ref | Change | Commit / PR |
|---:|---|---|---|
```

## Design guidance

Prefer concise phase tables plus evidence links over a narrative that duplicates workreports/endpoints.

Keep these distinct:

```text
OWNER INTENT
  strategic direction, sequencing, required benchmarks, acceptance gates

OBSERVED STATUS
  current implementation state, which agents must verify before use
```

A stale observed-status row does not grant permission to rewrite the roadmap. It triggers a proposal.
