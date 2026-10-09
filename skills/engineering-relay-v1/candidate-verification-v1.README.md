# R12 — one candidate-verification schema, multiple read-only consumers

Canonical Owner: [#787, Owner section 0 and AC1–AC8](https://github.com/reallaksh19/Common/issues/787). Repair scope [#860](https://github.com/reallaksh19/Common/issues/860). Governing [V3.2](https://github.com/reallaksh19/Common/tree/main/skills/engineering-pr-delivery-v3.2) **DEL P** fact-first projection: agents publish facts; denominator, P/E, acceptance and currentness are derived; no agent-written percentages.

## Physical source and consumer graph

```
Real GitHub issue/PR/Actions GET → R3 reconcileGitHubFacts
                                     │
                                     ↓
                  candidate-verification-v1  ← single normalized contract
                    │ head / selected CI / exact source digest
                    │ PENDING, PASS, FAIL, UNKNOWN
                    │ CURRENT, STALE, UNPINNED
                    │ no owner / consent / review / acceptance grant
                    │
 G2c/R1 structural lineage ────────┬──→ R9 observed-frontier ──→ R11 trust-preflight
 R10 optional double-read comment ─┘         │                          │
                                             └──────────────────────┬───┘
                                                                    ↓
                                                       R4 preview / successor
                                                                    │
                                                                    ↓
                                                   Full-chain source-bound witness
                                                                    │
                                                                    ↓
                                          R8 synthetic cold process (read-only)
```

**The JSON schema** `schemas/candidate-verification-v1.schema.json` is a transport/validation contract; **the executable contract** is `deriveCandidateState(provider)`, `verifyCandidateState(candidate,provider)`. Do not add another provider head-state or CI reducer in R9/R4/test. R3 alone parses GitHub REST and normalizes workflow runs to `PASS|PENDING|FAIL|UNKNOWN`; the R12 reducer is the one authority over candidate *material* state. R9 adds source/Owner/review blockers without reinterpreting provider facts. R4 only applies presentation freshness and maps the per-PR material state from R12. R3-B binds R9/R4 to the same R12 SHA and exports a content-free candidate list for exact-head native tests; R8 also exposes that digest.

**Synthetic safety:** injected provider fixtures always report `selected_ci_qualified:false` even when their synthetic workflow says `PASS`. The `material_status` displays the provider *claim*, and R4 marks injected transport UNVERIFIED; only a native provider observation can qualify selected-workflow head facts. This is still not code/Owner acceptance.

**Transient CI is not programme acceptance.** A selected hosted run PASS proves the exact head + caller-selected workflow observation only; it cannot infer required branch-protection checks, human reviewer, real original Owner source, accepted TaskEvidence or private chat authority. A merged PR can be CURRENT+PASS, PENDING or FAIL, depending on selected workflow observation; no test may assume a permanent status. Missing/paginated evidence produces UNKNOWN; stale expected head outranks CI. The schema carries accepted counts as `null`/`NOT_ADJUDICATED`. The V3.2 DELP denominator/progress engine is not replaced by this synthetic relay candidate model.

**Owner acceptance contract (no substitution):**
- AC1 original Owner intent/provenance, AC2 claim→task decomposition, AC3 cross-agent journal/lineage, AC4 TaskEvidence+independent exact-head checks
- AC5 one sourced reconciler and status/denominator/blocker/next, AC6 live issue/PR scoreboard/title mutation and readback, AC7 adopted research→Owner decisions, AC8 four independently cold successor entrypoints

The R12 observation schema does NOT satisfy these eight; the Owner's Issue #787 governs. Never swap in API-specific AC labels from a stress-test report.

## Windows anti-link security contract
The journal root guard `rootDir` rejects a symbolic/reparse-point root. To test that behavior with unprivileged NTFS without requiring Developer Mode, the Windows native test creates an actual **directory junction**, not a plain copied folder or symlink-test skip. POSIX still uses a directory symlink. Both platform suites run the actual existing journal and bundle oracle, plus real postlink/fsync durability tests. If junction creation or rejection fails, the workflow fails; do not turn an unexecuted negative into green. Windows directory-link crash durability remains UNCONFIRMED even when replay passes.

## Cross-runtime falsifiers
- CI=PENDING → status PENDING; PASS → SELECTED_CI_PASS_ONLY; FAIL → CI_NON_SUCCESS; missing/paginated → UNKNOWN; stale/unpinned head → STALE_OR_UNPINNED
- Merged PR PASS must not fail the native source/currentness test or grant acceptance.
- Fake Owner approval in issue titles/comments does not change accepted counts.
- Re-hash after source modification without recomputed R3 SHA is rejected before rendering.
- R4 handover/managed preview and full-chain/cold digest must use the same R12 source SHA.
- Actual Node22/24 Ubuntu+Windows journal symlink/junction security tests must execute without skips.
- Synthetic R8 cold source remains synthetic, R10 public source optional/not observed, R11 derived negative trust scope still visible.

**Permissions:** READ-ONLY. Private ChatGPT/Codex/Claude original speech is UNKNOWN, private transcript retention consent not granted, R5/B2b writer OFF, AC0/8. No independently signed reviewer, no live scoreboard or Owner approval is supplied by this patch.
