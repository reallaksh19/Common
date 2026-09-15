# Chemistry V2 — Engineering → Blueprint → Four-Core Compilation

This layer closes the gap between the topic-neutral Engineering Workbench and the four learner-product modes.

It is an **authority/custody compiler**, not a Chemistry author. Engineering assets become explicit Blueprint obligations; they do not become learner prose by themselves.

## Canonical flow

```text
ENGINEERING REQUEST + DIRECT-GATE MANIFEST
        ↓
WORKBENCH v2 CLOSURE + AUTHORIZATION BINDING
        ↓
ENGINEERING → BLUEPRINT OBLIGATION PACKET
        ↓
SEMANTIC CORE PAYLOAD
        ↓
UNIFIED CORE AUTHORITY
  CORE1A | CORE1B | CORE2A | CORE2B
        ↓
CORE SOURCE-SCOPE CONTRACT
  ATOM | MODULE | ITEM
        ↓
UNIFIED CORE PRODUCT CUSTODY
        ↓
DETERMINISTIC RENDERER
        ↓
PHYSICAL PDF PREFLIGHT
```

## Engineering → Blueprint obligation packet

`engine/compile_chemistry_blueprint_obligations.py` recompiles the current Workbench closure and authorization binding before emitting an obligation packet.

The packet is bound to the exact:

- request and manifest;
- engineering authorization binding and digest;
- closure receipt and digest;
- engineering gate registry and digest.

Each closure gate is projected into typed obligations for canonical concepts, equations, representations, model conditions, reasoning steps, transformations, misconceptions, verifications, problem families and engineering difficulty evidence.

Prerequisite-gate obligations remain engineering authorization context. A prerequisite is **not automatically learner-product content**. Direct-gate obligations fail closed according to the compilation policy.

Transformation routing is taken from the engineering gate's serialized `target_core_role`; generic compiler code does not infer the destination from a topic name.

## Unified core authority

`engine/compile_chemistry_core_authority.py` accepts an already-authored semantic payload plus the current obligation packet.

It does not create missing Chemistry. It verifies that:

- every claimed obligation exists in the current packet;
- every claimed obligation is authorized for the selected core mode;
- every required direct-gate obligation for that mode is explicitly realized;
- the semantic payload passes the mode-specific boundary;
- the exact payload bytes are digest-bound.

A-layer adapters preserve the existing production machinery:

```text
CORE1A -> existing Core1A manuscript + representation bundle
CORE2A -> existing Core2A source/challenge plans + representation bundle
```

B-layer adapters use the current static boundary:

```text
CORE1B -> intrinsic-difficulty-controlled reconstruction module
CORE2B -> frozen Core2A item + learner-conditioning-controlled support
```

Core1B/Core2B may not introduce new Chemistry or live adaptive runtime state.

## Source-scope units

The earlier product-custody path used Core1A `learning_atoms` as its universal source-scope denominator. That is retained for compatibility, but it is not used as the four-core abstraction.

The unified source-scope contract uses neutral units:

```text
CORE1A -> ATOM
CORE1B -> MODULE
CORE2A -> ITEM
CORE2B -> ITEM
```

Every authority scope unit must receive exactly one authorized source tier. Held transformations retain explicit detection guards. A `STRESS_TEST_SOURCE_AUDIT` can exercise the compiler but cannot establish product custody.

## Unified product custody

`engine/compile_chemistry_core_product_custody.py` recompiles the current Workbench closure/binding at custody time and rejects stale packets, stale authorities, stale source audits and stress-only source evidence.

Custody binds the exact:

```text
engineering binding
+ closure
+ gate registry
+ Blueprint obligation packet
+ core authority
+ core source-scope contract
+ production source audit
```

A renderer may run only from `CORE_PRODUCT_CUSTODY_READY`.

## Rendering

`LearnerProduct/engine/run_chemistry_core_product.py` is the common artifact entrypoint.

- Core1A/Core2A delegate to the existing deterministic A-layer renderer.
- Core1B/Core2B use the governed static-B renderer.
- All modes bind the current learner-render policy and exact custody/authority digests.
- All modes enter the same physical PDF preflight for artifact digest, A4 geometry, blank-page rejection, font floor and learner-surface identifier leakage.

The static-B renderer projects internal hint levels into learner-readable labels; internal H-level names are not learner surface.

## v1 direct-gate boundary

A v1 core product is compiled for **one direct engineering gate**. Recursive prerequisites may contain many gates, but one artifact has one direct product gate.

A multi-direct-gate request fails explicitly with:

```text
CHEM_CORE_CUSTODY_MULTI_DIRECT_GATE_UNSUPPORTED
```

This prevents a multi-gate topic request from silently pretending that one source-scope contract covers all direct gates. A future multi-gate product compiler must define an explicit per-gate source-scope/custody aggregation contract before this restriction is removed.

## Topic-neutrality rule

Generic compiler, custody and renderer-control code may not branch on Redox or any other Chemistry topic name. Topic-specific source audits and semantic payloads enter only as governed data at the edge.

## Non-claims

A machine-complete core artifact does not establish learner efficacy, mastery, subject-review approval, pedagogical approval, assessment approval, visual-usability approval or publication authorization. Those remain separate governed gates.
