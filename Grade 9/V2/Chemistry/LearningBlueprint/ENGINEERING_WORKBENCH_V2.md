# Chemistry Engineering Workbench v2

## Authority boundary

Workbench v2 is topic-neutral engineering control infrastructure. A topic may exercise it, but no topic defines its control flow.

```text
complete Chemistry gate registry
  -> explicit engineering request
  -> explicit direct-gate manifest
  -> recursive prerequisite closure
  -> declared source-audit evidence
  -> RESEARCH dossier + claim ledger when requested
  -> closure receipt
  -> authorization binding
  -> engineering passport
  -> CDAU technical boundary
  -> production source-scope authorization
  -> product engineering custody
  -> PAL
```

## Discovery is not falsely claimed

Workbench v1 declared `AUTO_DISCOVER` but consumed human/agent-supplied `required_gate_ids` directly. Workbench v2 therefore uses:

```text
requested_action = DECLARE_DIRECT_GATES
```

until an independent discovery-decision compiler exists. Recursive prerequisite closure remains deterministic and automatic after the direct roots are declared.

## Source audits are explicit inputs

The manifest contains:

```json
"source_audits": [
  {"gate_id": "CHEM-...", "audit_ref": "..."}
]
```

The closure compiler never loads an audit because it recognizes a topic or gate name. Each declared audit must:

- bind a gate present in the computed closure;
- bind the same registry as the manifest;
- pass the generic source-audit v2 validator;
- carry exact digest custody into the closure receipt and authorization binding.

## Stress audits cannot authorize products

Two audit roles exist:

```text
PRODUCTION_SOURCE_AUDIT
STRESS_TEST_SOURCE_AUDIT
```

A stress audit may be recorded in engineering closure evidence. Its authority effect is always:

```text
NONE_STRESS_TEST_ONLY
```

Product source-scope authorization and engineering custody require `PRODUCTION_SOURCE_AUDIT`. A stress audit therefore cannot become learner-product authority merely because the associated technical gate is READY.

## Source tiers are data, not schema vocabulary

Product source-scope contracts consume tier IDs declared by the bound production audit. Workbench v2 has no built-in Chemistry-topic tier names. Each tier carries `minimum_learner_grade`; higher-grade authorization requires an explicit extension authority and reason.

## Independent authority dimensions

```text
technical engineering closure
!= source-scope authorization
!= learner evidence
!= pedagogical authority
!= publication approval
```

Technical READY may coexist with held or absent production source authorization. CDAU may consume technical engineering authorization while PAL remains blocked until product source-scope and custody are valid.

## Topic-stress rule

Redox remains a stress fixture only. It may falsify Workbench behavior, but generic Workbench engines contain no Redox, permanganate, MnO4, or topic-named branches.
