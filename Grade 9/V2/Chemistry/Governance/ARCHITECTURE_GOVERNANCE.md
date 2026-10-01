# Chemistry Architecture Governance

This file governs how topic-specific proofs interact with the Chemistry V2 architecture and how superseded review surfaces are retired without losing generic mechanisms.

## Non-negotiable authority rule

A topic-specific case is evidence **about** the architecture. It is not the architecture's ground truth.

For the current stress case:

```text
REDOX
= STRESS_TEST / REGRESSION / SOURCE-SCOPE EXERCISE
!= GROUND TRUTH
!= CANONICAL DOMAIN AUTHORITY
!= GENERIC ENGINE DESIGN INPUT
!= DEFAULT POLICY BASIS
```

A Redox case may expose a defect, falsify a generic contract, prove that a generic contract handles a difficult case, or exercise source-scope custody. It may not create a new generic rule merely because the rule is convenient for Redox.

## Required direction of authority

```text
subject-wide Chemistry contracts / registries
        ↓
generic engineering + Blueprint engines
        ↓
topic manifest / source scope / stress fixture
        ↓
Redox (or any other topic) execution
        ↓
PASS / FAIL / blocker evidence
```

The reverse direction is forbidden. Generic engines must not branch on topic names, import committed stress/golden fixtures as producer authority, infer Chemistry scope from a stress case, or promote stress-test success into canonical subject authority.

## Generic-engine constraints

Generic production engines are driven by stable IDs, contracts, registries, manifests, capability/gate data, source-scope records and explicit policy inputs. Topic-specific data belongs at the edge of the system and enters through contracts as data.

A failing stress test can justify a **generic** change only when the defect is stated independently of the topic and the repair is expressed over generic contract fields such as `gate`, `manifest`, `source_scope`, `CCBOM`, `TTU` or `custody`.

## Pull-request consolidation doctrine

`chemistry-pr-consolidation.v1.json` is the machine-readable migration ledger. No PR is closed merely because a newer PR exists. Supersession requires one of:

1. the useful generic authority/mechanism is already present in the active lineage;
2. it has been explicitly ported and validated;
3. it is intentionally retained only as regression/migration evidence.

Historical topic bundles, PDFs, frozen candidate hashes and product snapshots do not become current authority simply because they remain reachable in ancestry.

## Current target stack

```text
#371 Blueprint + product-control + governance root
  ↓
#384 complete Grade 9–11 technical gate registry
  ↓
#387 generic source audit + topic-neutral Engineering Workbench v2
  ↓
#385 Redox stress test (blocked / non-authoritative until rebuilt on #387)
```

#377 and #381 are superseded by #387. #322, #346, #360, #362, #370 and #375 are closed review surfaces with explicit retention/migration dispositions. #386 is being absorbed into #371 so governance is enforced by the same root it governs.

## Publication and product boundaries

Machine engineering PASS never substitutes for subject correctness, pedagogy, assessment, visual usability or mature-design review. The inherited ExactProduct publication-engineering validators may validate current artifacts, but historical exact-product candidate bytes and hashes are not current product authority.

Likewise, a topic stress test can falsify architecture but cannot establish Chemistry-wide completeness. Passing Redox proves only the declared generic contracts against that stress case.
