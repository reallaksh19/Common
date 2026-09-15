# Physics Engineering Readiness Kernel — canonical consumption boundary

## Purpose

The Engineering Kernel is the mandatory boundary between broad subject research and downstream learner-product consumption.

Its governing rule is:

> **Discovery is permissive; promotion and consumption are strict.**

Agents may search broadly, inspect external sources, create candidate mappings, and build RESEARCH dossiers while the final prerequisite graph is incomplete. Missing authority must remain visible, but it must not stop discovery itself. A downstream technical consumer may proceed only from an aggregate Engineering Readiness Envelope.

## Canonical lifecycle

```text
ENGINEERING REQUEST
        ↓
DISCOVERY / RECONCILIATION
        ↓
CANONICAL V3 GATE SOURCES
        ↓
PHYSICS TECHNICAL CLOSURE ─────────────┐
        ↓                              │
RESEARCH DOSSIER + CLAIM LEDGER        │ when depth = RESEARCH
                                       │
CROSS-DOMAIN PREREQUISITE CLOSURE ────┤
                                       ↓
                       ENGINEERING READINESS ENVELOPE
                                       ↓
                         consumer-specific permission
                                       ↓
                         CCU / Core1A / Core1B /
                         Core2A / Core2B
```

The Engineering Passport remains a useful internal-Physics projection. It is not sufficient consumer authority because it does not own another domain's prerequisite readiness. The aggregate Engineering Readiness Envelope is the consumer boundary.

## Readiness dimensions

The envelope exposes four independent dimensions:

- `physics_technical` — canonical Physics gates and recursive Physics prerequisite closure;
- `research_provenance` — `READY`, `BLOCKED`, or `NOT_REQUIRED` according to engineering depth;
- `external_prerequisites` — authoritative-domain receipts only;
- `source_authority` — independent source/legal state, never silently collapsed into technical readiness.

A technical consumer is `ALLOWED` only when Physics technical closure is READY and external prerequisite closure is READY. Publication is always `NOT_AUTHORIZED` by engineering alone.

This prevents contradictory user-facing states such as `CCU ALLOWED` while Mathematics prerequisites remain `HELD_NO_DOMAIN_RECEIPT`.

## Adding a new topic such as Thermodynamics

Do not begin by creating teaching prose or a one-off workflow. Create an Engineering Request at the requested depth and perform discovery/reconciliation first.

Typical candidate capabilities may include temperature, thermal equilibrium, heat capacity, calorimetry, phase change, internal energy, gas work, the first law, P-V representations and heat transfer. Discovery may also identify external Mathematics capabilities or reusable Physics gates.

Each candidate is reconciled as one of:

`REUSE | EXTEND | CREATE_CHILD | CREATE_NEW | OUT_OF_SCOPE | UNRESOLVED`

Only reviewed candidates are promoted to canonical `engineering-gates/**/PHY-*.v3.json` authority. The manifest declares direct requested gates; `compile_engineering_closure.py` derives recursive Physics prerequisites. `compile_domain_prerequisite_closure.py` derives external-domain demands. `compile_engineering_readiness.py` joins both without allowing either layer to impersonate the other.

## Adding one research-depth subtopic

For a request such as gravitational field at `RESEARCH` depth:

1. create/update the Engineering Request;
2. perform broad discovery and human-reviewed reconciliation;
3. build the Research Dossier and claim-level Claim Ledger;
4. create or reuse canonical v3 gates;
5. declare only the direct requested gates in the manifest;
6. compile Physics prerequisite closure;
7. compile external-domain prerequisite closure;
8. compile the aggregate Engineering Readiness Envelope;
9. allow downstream consumption only if that consumer is `ALLOWED`.

A held Mathematics prerequisite does not stop steps 1–8. It does stop step 9.

## Minimum promotion criteria

Every promoted gate must have, where applicable:

- stable subject capability identity;
- explicit scope and authority basis;
- explicit Physics and external prerequisites;
- core scientific concepts/laws/relations;
- symbol, dimensional and frame/sign semantics for equations;
- model validity conditions and failure consequences;
- at least one verification/falsification route;
- contradiction, cycle and duplicate-authority checks;
- explicit cross-domain ownership rather than consumer self-certification.

The following are conditional rather than bureaucratic quotas: dedicated diagrams, misconception models, transformations, problem-family count and research source count. They are required when the capability needs them, not merely to fill a schema.

`RESEARCH` additionally requires a release-ready Research Dossier and Claim Ledger. Research depth is evidence depth; it does not automatically increase learner difficulty.

## Generic CI rule

New ordinary topics/subtopics should be data additions, not new validators or bespoke workflows.

`compile_all_engineering_readiness.py` discovers canonical v3 request/manifest pairs and compiles each through the same readiness pipeline. A new topic should require new Python code only when it introduces a genuinely new class of invariant that the Engineering Kernel cannot express.

CI compilation does not fail merely because a legitimate authority is held. Held states are valid governed outputs. Consumer-specific validation fails when a blocked consumer attempts to proceed.

## User visibility

Author/reviewer interfaces should project the envelope as a compact engineering map:

```text
Physics technical        READY
Research provenance      READY
External prerequisites   HELD (2)
Source authority         HELD
Core1A consumption       BLOCKED
Publication              NOT AUTHORIZED
```

Learner-facing products should translate this into subject language (dependencies, model limits, fragile reasoning points, common traps) and must not expose internal receipt IDs or digest machinery.
