# Common #527 / P3-SOLO-6 — Unit 4 falsifier and authority map

Candidate: `728a8f0551171f5c7bb1cfd46974bac7dd6cb3ce`  
Base: `a05db7c57fdacc2f5fcb0e55e300d6d76f70e4cd`  
PR: #585  
Production mode: OFF

## Precommitted EG-01..18 mapping

| Falsifier | Executable proof |
| --- | --- |
| EG-01 clean closed candidate -> ADVANCE_ELIGIBLE | `test_eg01_clean_closed_candidate_is_advance_eligible` |
| EG-02 stale binding digest -> REPLAY | `test_eg02_binding_digest_mismatch_replays` |
| EG-03 fresh replay differs from stored source -> REPLAY | `test_eg03_fresh_source_replay_failure_replays` |
| EG-04 critical REFUTED -> REPAIR | `test_eg04_critical_refuted_requires_repair` |
| EG-05 required Common criterion FAIL -> REPAIR | `test_eg05_required_common_criterion_fail_requires_repair` |
| EG-06 project FALSIFIED -> REPAIR | `test_eg06_project_falsified_requires_repair` |
| EG-07 critical UNKNOWN without exhaustion -> REPLAY | `test_eg07_unknown_without_exhaustion_replays` |
| EG-08 critical UNKNOWN with proven exhaustion/boundary -> ESCALATE | `test_eg08_unknown_with_proven_exhaustion_escalates` |
| EG-09 required NOT_RUN/INCONCLUSIVE -> REPLAY | `test_eg09_required_not_run_replays` |
| EG-10 caller “cannot resolve” shortcut cannot manufacture escalation | gate source schema `test_source_rejects_caller_cannot_resolve_shortcut` plus exhausted-record evidence/boundary requirement |
| EG-11 same-principal fresh context stays NONE | principal suite `test_pis01_self_review_same_principal_is_none`, `test_pis08_fresh_context_does_not_upgrade_same_principal` |
| EG-12 legacy DEGRADED is not canonical independence | principal suite `test_pis03_governed_same_principal_degraded_input_canonicalizes_to_none`, `test_pis12_canonical_principal_independence_never_contains_degraded` |
| EG-13 ADVANCE_ELIGIBLE + unresolved critical -> reject | execution-kernel semantic validation of ADVANCE_ELIGIBLE with unresolved rows |
| EG-14 gate candidate mismatch -> reject/replay | gate compiler `test_candidate_binding_mismatch_replays` + kernel `test_gate_candidate_mismatch_is_rejected` |
| EG-15 gate cannot contain engineering PASS/lifecycle/merge/cutover authority | contract tests `test_result_rejects_pass_and_legacy_replay_evidence_tokens`, `test_result_rejects_engineering_pass_authority`, `test_result_rejects_lifecycle_merge_and_cutover_authority` |
| EG-16 current ESCALATE reachable in kernel | `test_gate_escalate_with_unknown_is_reachable` |
| EG-17 current REPAIR reachable in kernel | `test_gate_repair_with_refuted_is_reachable` |
| EG-18 ADVANCE_ELIGIBLE -> REQUEST_STAGE_ADVANCE only | `test_advance_eligible_only_requests_local_stage_advance` + `test_advance_eligible_without_capability_fails_closed` |

## Additional falsifiers

- open blocking finding -> REPAIR;
- incomplete Common review cannot fall through to ADVANCE;
- stored gate result cannot self-certify without fresh source replay;
- REPLAY or ESCALATE cannot hide a critical REFUTED obligation;
- gate NOT_AVAILABLE under CURRENT evidence derives GATE_REQUIRED verification;
- Local capability can deny stage-advance request;
- execution schema does not permit a coordinator-owned ADVANCE_STAGE capability.

## Clean + green-but-wrong qualification

The clean control is EG-01: a closed current denominator reaches `ADVANCE_ELIGIBLE`, while the execution kernel still emits only a request and does not perform a lifecycle transition.

Green-but-wrong/stale controls include:
- self-consistent source binding with wrong digest -> REPLAY;
- stored source whose fresh replay differs -> REPLAY;
- candidate binding mismatch -> REPLAY/reject;
- incomplete/NOT_RUN required review -> REPLAY;
- UNKNOWN without proven local exhaustion -> REPLAY.

The gate therefore does not treat schema/digest shape as semantic acceptance.

## Authority boundaries

The candidate preserves:

```text
gate disposition != engineering PASS
ADVANCE_ELIGIBLE != lifecycle transition
same-principal fresh context != principal independence
NOT_FALSIFIED != PASS
production_mode = OFF
```

No file under Local lifecycle/role-transition authority, frozen v3.2, or Common #570 is modified by this responsibility.
