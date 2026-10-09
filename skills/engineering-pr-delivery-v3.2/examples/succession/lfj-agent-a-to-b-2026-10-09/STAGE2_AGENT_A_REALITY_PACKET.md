# STAGE 2 — Agent A real-state reconciliation packet (release only AFTER Runner B freezes Stage 1)

**CASE_ID:** `v32-succession-lfj-real-2026-10-09`  
**ACCESS_CLASS:** `STAGE2_ONLY`  
**AUTHORITY:** `READ_RECONCILE_ONLY` — neither product write nor executor promotion  
**SNAPSHOT_DATE:** 2026-10-09; all GitHub states below are historical snapshots and MUST be refreshed by the successor after Stage 1 freeze.

## The binding gate

Controller must first read back a Runner-B-authored **independent** Stage 1 plan at a *distinct issue or immutable location* and verify its content digest. Then release this packet. Any access to this file, issue #1147 or its comment #6080011972, current PR metadata, or Agent A's implementation **before** that immutable freeze contaminates this Runner-B session.

```yaml
controller_gate_at_fixture_creation:
  runner_b_independent_plan_frozen: false
  plan_sha256: null
  plan_issue: null
  stage1_source_access_restricted: not_enforced_by_repository_text
  stage2_released: false
  agent_a_write_revoked: false
  agent_b_execution_epoch: null
```

Never fill these placeholders with imaginary success in a test. A real controller must supply signed/read-back evidence in a separate instance-specific custody ledger.

## Actual Agent A work — inspect, critique, reject as appropriate

**Original application baseline:** `reallaksh19/3D_Converters@1205639a43e9ce1589360479d2558678aebcfab7`  
**Protocol candidate:** `reallaksh19/Common@13989969f6b7e432c4f7c1ddfe975449dba53593`  
**Programme:** [LFJ parent #1042](https://github.com/reallaksh19/3D_Converters/issues/1042).  
**Recovery coordination:** [#1147](https://github.com/reallaksh19/3D_Converters/issues/1147).  
**R13 real Resolver product owner:** [#1104](https://github.com/reallaksh19/3D_Converters/issues/1104); deployed docs ownership [#1097](https://github.com/reallaksh19/3D_Converters/issues/1097), source store [#1096](https://github.com/reallaksh19/3D_Converters/issues/1096). These leases cannot be claimed from an experiment.

Four *DRAFT and UNMERGED* stacked experimental PRs, NOT four newly earned product responsibilities:

| PR | Exact Agent A handover SHA | Agent A's advertised investigation | Source/scope limit |
| --- | --- | --- | --- |
| [#1148](https://github.com/reallaksh19/3D_Converters/pull/1148) | `1fcd6561a677fbb44ad175bdab6c98214ed37df4` | Lossless full original occurrence catalog in native Worker/packed IndexedDB pages | Source-only, no product selection or crash custody |
| [#1149](https://github.com/reallaksh19/3D_Converters/pull/1149) | `8579c8c8c1f003bf6a3069f48d55532f907ef5e4` | Bounded `ALL/RANGES/NONE` paged queries over source catalog | Research API only, not production R08/R09 |
| [#1150](https://github.com/reallaksh19/3D_Converters/pull/1150) | `4f5110d48db370e8dbd452edbb7c823211769fd2` | Consumer field projection from per-original-branch span; original Resolver semantics | Flat source assumptions, <=1 MiB branch, re-reads source |
| [#1151](https://github.com/reallaksh19/3D_Converters/pull/1151) | `b674765a74507e4ce528dd4bfecc2d934a17a5d7` | Actual legacy Resolver XML matching and both shipped CSV serializers through sparse-facts view | No genuine served UI Build/download; latest head NOT executed |

The four PRs are research-only opt-in `lfj/qualification/experiments/**` and test workflows; production XML→CII Standalone, Preview, Weight, Enrichment, stable LFJ storage and served docs have not been changed by this investigation. The LFJ V4 24-responsibility / 130-point programme denominator was NOT extended by these experiments.

## Evidence worth accepting and source-verifying

**W2 existing throughput RED:** authentic 733,806-byte JSON 23,754 occurrences, ~60.94 s and ~31 MB browser storage; genuine 10,232,634-byte JSON 328,156 occurrences FAILED after ~300.81 s, not complete. [W2 native Action #37899290405](https://github.com/reallaksh19/3D_Converters/actions/runs/37899290405). This is source-only W2 and NOT actual app.

**Compact catalog GREEN:** [Action #37910231523](https://github.com/reallaksh19/3D_Converters/actions/runs/37910231523) source-only 10.23MB, 328,156 / 328,156 occurrences, ~9.49 s, ~11.39 MB storage measured. Compared to experimental per-record 10MB ~178.6 s. **Not apples-to-apples with complete original W2 pipeline**: query/export obligations not part of catalog benchmark.

**Source query GREEN:** [Action #37911778280](https://github.com/reallaksh19/3D_Converters/actions/runs/37911778280) 10.23MB source, complete `ALL` 328,156 occurrence union at both 64 and 256 rows/page, 69 explicit selected ordinals, source hash and stale source negatives; tests not semantic branch matching.

**Consumer projection GREEN:** [Action #37915127723](https://github.com/reallaksh19/3D_Converters/actions/runs/37915127723) 10MB, 4,320 legacy source engineering facts and 2,814 spatial groups identical by full normalized fact digest, including original alias configuration. RED→repair history: branch-local fallback node numbering incorrectly reset original global node number; another helper created Error but did not throw. The second genuine fail-open mistake was corrected and guarded.

**Real output parity GREEN at an *EARLIER* #1151 commit:** [Action #37915926502](https://github.com/reallaksh19/3D_Converters/actions/runs/37915926502) at `9e08d07a6e0c13b3e35a6f2c9b53c611aa65be36`. Native Chromium+original JSON fixture+existing Resolver and two actual CSV exporters, 4/4 tests. Test-side independently processed full original JSON, including **explicitly labeled synthetic source-derived XML controls**. Those controls yield exactly 1 `RESOLVED_POS`, 1 `RESOLVED_PS_FALLBACK`, 1 `UNRESOLVED`, 546 B nonempty Evidence Tree and 823 B Node-wise CSV with exact full-output hashes. This is NOT a real Owner-authored XML positive source match or deployed click/download.

**Original XML negative pairing caveat:** `Benchmarks/1885Sjson/ExpectedXML` + Sjson gives 174/174 `UNRESOLVED`; `Benchmarks/1885_NC/1885_NC.topology.input.xml` + large JSON gives 3,429/3,429 `UNRESOLVED` even in *original legacy engine*. Matching two header-only Evidence Tree CSVs (103 B) is a valid negative check and insufficient positive acceptance.

**Potential real positive pair discovered:** `Benchmarks/1885Sjson/FirstpassXML` and Sjson. FirstpassXML contains 216 XML Node tags. Agent A's direct source coordinate/branch co-location probe found 164/216 candidates within 6mm under same canonical branch, but **this is NOT evidence of 164 engineering matches**. A positive *legacy* Resolver oracle and actual Browser CSV match are still needed.

**Latest exact-head blocker:** [GitHub Actions #37916468898](https://github.com/reallaksh19/3D_Converters/actions/runs/37916468898) on latest PR #1151 `b674765a74507e4ce528dd4bfecc2d934a17a5d7`: 5-case original-XML+changed-configuration test, 3 attempts, all five jobs failed **before runner/checkout/test steps**; job records empty runner and zero steps, no executable logs. This is `NOT_RUN_INFRASTRUCTURE`, neither code RED nor GREEN. It is impermissible to transfer prior-head GREEN to this SHA.

## Agent A current suggested next order — hypothesis to critique

A recommends qualifying exact newest 5-matrix browser test, authentic FirstpassXML positive status and config digest negative; only then seeking actual R13 / deploy-writer lease to integrate the proven source adapter into live Build/two CSV downloads. Distinct crash/cancel/source reopen/multi-scope hierarchy/30MB+ and Enrichment responsibilities remain. **Do not adopt this plan automatically**: it may contain unnecessary experimental layers, redundant source-byte reads, narrow flat-hierarchy support or safety holes. A valid successor could simplify, reject, replace or park parts after independent code/Owner reconciliation.

## Stage 2 output (Runner B)

1. Read B's pre-frozen plan unchanged; refer to its immutable digest.
2. Independently fetch LIVE source and evidence at exact heads; do not rely on Agent A summaries or PR title.
3. Produce a delta table `STAGE1_HYPOTHESIS → LIVE_FINDING → VERIFIED_SOURCE → CONFIRMED | DISPROVED | UNKNOWN | MISSCOPED | UNNECESSARY → PLAN_CHANGE`.
4. Identify unnecessary modifications, missed medium-ROI work and high-ROI requirements now absorbed. Park low ROI without altering Owner intent.
5. Reconcile existing R12/R13/docs/STORE writer leases and original 24/130 denominator; decompose only claim-preserving semantic work through proper V3.x owner approval.
6. Update B's separate plan as a **revision**, preserving the original Stage-1 frozen bytes/digest. Do not author progress percentages or take over scope by assertion.
7. Stop at `STAGE2_RECONCILED_AWAITING_CONTROLLER`. A real controller must revoke A's write authority and issue an exclusive B execution epoch before B can mutate production.

**Promotion at fixture creation:** `A_WRITE_REVOKED=false`, `B_EPOCH_GRANTED=false`, `STAGE1_PLAN_FROZEN=false`, `STAGE2_RECONCILIATION_OCCURRED=false`. No implicit permission from publishing this file.
