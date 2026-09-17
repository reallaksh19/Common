# V2.5 catch-up / completion roadmap

## Purpose

Complete Engineering Relay V2.5 without rewriting V2 or encoding downstream-specific behavior.

PR #396 delivered WP-00 through WP-09 and was explicitly merged at `fb28a0817cab109a1120e3826ce11439b49586de`. WP-10/WP-11 completion work is isolated on PR #409.

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
CP-R011  WP-10 Self-consistency Audit               COMPLETE
CP-R012  WP-11 PR Readiness                         CONDITIONAL — exact canonical-head CI required
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
| WP-10 Self-consistency Audit | 2 | COMPLETE — CP-R011 |
| WP-11 PR Readiness | 1 | CONDITIONAL — CP-R012 exact-head CI pending |
| **Total** | **100** | |

**Acceptance/checkpoint earned work is 100%; formal program completion is pending the exact canonical-head workflow required by CP-R012.**

## Delivered relay

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

## WP-10 evidence

WP-10 converted consistency review into an executable CI gate. Its red-to-green audit is recorded in `wp-10-self-consistency-audit.md` and checkpointed by CP-R011. The CP-R011 checkpoint/program-state head passed workflow `35198273521` with self-consistency, root units and dedicated stress discovery.

## WP-11 readiness

WP-11 adds no protocol semantics. It closes release/operator readiness:

- PR #409 changed paths restricted to the scoped V2.5 workflow and `skills/engineering-pr-delivery-v2.5/**`;
- V2 and downstream repositories remain untouched;
- `architecture-index.md` provides stable navigation;
- `operator-quick-start.md` gives the zero-chat operating sequence;
- `synthetic-relay-example.md` demonstrates the repository-neutral relay transaction;
- `self_consistency_audit.py` requires those release surfaces;
- no unresolved PR review threads or submitted review obligations existed at readiness review;
- release-documentation head `5455bb90895461ba1d7476af10c84863f979fb93` passed workflow `35205304623`.

`CP-R012` now exists. Formal 100% completion requires the scoped workflow to pass on the exact canonical head containing CP-R012 plus this reconciliation.

## Final CI evidence rule

A whole-suite completion claim requires all of:

```text
python skills/engineering-pr-delivery-v2.5/scripts/self_consistency_audit.py .
python -m unittest discover -s skills/engineering-pr-delivery-v2.5/tests -p 'test*.py' -v
python -m unittest discover -s skills/engineering-pr-delivery-v2.5/tests/stress -p 'test*.py' -v
```

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
[x] schema/template/validator/renderer/docs self-consistency — CP-R011
[x] WP-11 portability / V2-isolation / release navigation — CP-R012
[ ] final exact canonical-head generic CI
```

PR #409 remains draft until that final exact-head gate passes. After it passes, the PR may be marked ready for review. Merge remains an explicit Owner decision.
