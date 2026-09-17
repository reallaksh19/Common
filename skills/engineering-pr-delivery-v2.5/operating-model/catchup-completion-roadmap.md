# V2.5 catch-up / completion roadmap

## Purpose

Complete Engineering Relay V2.5 without rewriting V2 or encoding downstream-specific behavior.

PR #396 delivered WP-00 through WP-09 and was explicitly merged at `fb28a0817cab109a1120e3826ce11439b49586de`. Remaining completion work continues on draft PR #409 from that merge basis.

> First make the baton trustworthy. Then prove a replacement can pick it up. Then prove engineering qualification. Then make the relay complete, legible, and internally consistent.

## Current program state

```text
CP-R001  WP-00 Kernel baseline / object matrix      COMPLETE
CP-R002  WP-01 Semantic Execution Package           COMPLETE
CP-R003  WP-02 Baton readiness / Takeover Cert      COMPLETE
CP-R004  WP-03 Strong qualification                 COMPLETE
CP-R005  WP-04 Progress / handover / next-work      COMPLETE
CP-R006  WP-05 GitHub Program Projection            COMPLETE
CP-R007  WP-06 Quality Procedure Library            COMPLETE
CP-R008  WP-07 Human Communication                  COMPLETE
CP-R009  WP-08 Owner Change Intake                  COMPLETE
CP-R010  WP-09 End-to-end Relay Certification       COMPLETE
CP-R011  WP-10 Self-consistency Audit               CONDITIONAL — exact-head CI required
   |
   v
WP-11    PR Readiness                               NEXT AFTER CP-R011 CI PASS
```

## Progress Basis

| Work package | Weight | Status |
| --- | ---: | --- |
| WP-00 Kernel baseline / object matrix | 5 | COMPLETE — CP-R001 |
| WP-01 Semantic Execution Package | 18 | COMPLETE — CP-R002 |
| WP-02 Baton readiness + Takeover Certification | 18 | COMPLETE — CP-R003 |
| WP-03 Strong phase/boundary qualification | 12 | COMPLETE — CP-R004 |
| WP-04 Full progress / handover / next-work | 12 | COMPLETE — CP-R005 |
| WP-05 GitHub Program Projection operations | 8 | COMPLETE — CP-R006 |
| WP-06 Quality Procedure Library | 10 | COMPLETE — CP-R007 |
| WP-07 Human Communication | 6 | COMPLETE — CP-R008 |
| WP-08 Owner Change Intake | 3 | COMPLETE — CP-R009 |
| WP-09 End-to-end Relay Certification Matrix | 5 | COMPLETE — CP-R010 |
| WP-10 Self-consistency Audit | 2 | CONDITIONAL — CP-R011 exact-head CI pending |
| WP-11 PR Readiness | 1 | WAITING |
| **Total** | **100** | |

**Earned completion remains 97% until CP-R011's exact checkpoint/program-state head passes. Target after that gate: 99%.** Progress is acceptance/checkpoint-derived.

## Delivered system through CP-R010

```text
semantic EP / typed inputs-oracles / DSTEP discovery
→ BATON_READY
→ repository-only DISC / QSET / QUAL / TC
→ TAKEOVER_CERTIFIED(route,candidate)
→ live MATERIAL_WRITE_READY
→ implementation
→ applicability-routed quality procedures / QRV
→ exact-basis checkpoint
→ calculated progress / exact next work
→ roadmap / issue reconciliation
→ crash-safe GitHub GHGEN/GHOP projection
→ report / technical / Owner / Owner-change derived views
→ ZERO_CONTEXT_RECONSTRUCTION
→ A → B → C zero-chat release certification
```

CP-R010's final canonical predecessor head `581735fb302cae9a1d8ccd0d518c3a463bb68a4c` passed workflow `35192761449`: compile, 7 root units, and 135 repository-neutral synthetic stress tests.

## WP-10 — Self-consistency Audit

WP-10 adds an executable cross-surface audit and resolves stale normative surfaces rather than changing relay semantics. Findings/resolutions are recorded in `wp-10-self-consistency-audit.md`.

Key corrections:

- authority matrix reconciled from its old CP-R002 view through CP-R010;
- relay-conformance docs reconciled through qualification, progress/report, GitHub operations, QRV, human communication, Owner-change, and zero-context release certification;
- top-level `SKILL.md` and command index expose the delivered zero-context and self-consistency entrypoints;
- stable `quality-procedures.md` separates current operating policy from historical WP-06 implementation evidence;
- portability audit is generic and contains no downstream-repository exception logic;
- scoped CI runs self-consistency before root unit and dedicated stress suites.

Red-to-green evidence:

```text
8c7cbc7d7b03688e59de89dd380e83639d965391
workflow 35197070033 — expected FAIL
16 consistency errors / 3 warnings

3beae3849550fb0cd28abe658c63d1d770d9d3fa
workflow 35197671662 — PASS
self-consistency: 0 warnings
root units: 7 PASS
stress: 135 PASS

f741a54da9e22e6a2f75aa15f54fd53563ee69de
workflow 35197914544 — PASS
self-consistency: PASS
root units: PASS
stress: PASS
```

`CP-R011` exists, but formal 99% completion requires the workflow to pass again on the exact head containing CP-R011 plus this program-state reconciliation.

## CI evidence rule

A whole-suite claim requires all of:

```text
python skills/engineering-pr-delivery-v2.5/scripts/self_consistency_audit.py .
python -m unittest discover -s skills/engineering-pr-delivery-v2.5/tests -p 'test*.py' -v
python -m unittest discover -s skills/engineering-pr-delivery-v2.5/tests/stress -p 'test*.py' -v
```

Historical pre-correction workflow interpretation remains documented in `ci-evidence-correction.md`.

## Remaining dependency topology

```text
CP-R011 exact-head verification
   |
   v
WP-11 PR Readiness
```

Serial execution remains default. Defined future work is not executable work.

## Final completion gates

```text
[x] Semantic EP
[x] BATON_READY / independent takeover certification
[x] live write-readiness gate
[x] evaluated qualification on material boundary change
[x] calculated progress / exact next work / source-derived reports
[x] crash-safe GitHub operations
[x] scoped procedural QRV quality system
[x] plain-language Owner communication
[x] Owner change-intake projection
[x] lifecycle certification matrix
[x] A → B → C zero-chat relay
[~] schema/template/validator/renderer/docs self-consistency — CP-R011 pending exact-head CI
[ ] WP-11 portability / V2-isolation / final readiness cleanup
[ ] final exact-head generic CI at 100%
```

PR #409 remains draft. Do not merge it automatically; final merge remains an explicit Owner action/authorization.
