# Mathematics Engineering Workbench

## Subject ownership

This Workbench is **MATHEMATICS-only**.

- Canonical implementation PR: **#351**.
- Mathematics Technical Engineering Gate data: **`REG-MATH-TECH-GATE-V1`**.
- Physics artifacts are architecture references only. No Physics gate, manifest, receipt, policy, or remembered mapping is authority in this Workbench.

Every Workbench request, manifest, closure receipt, passport and binding carries `subject = MATHEMATICS`; non-Mathematics artifacts fail closed.

## Authority model

```text
ORIGINAL / VALIDATED MATHEMATICS GROUND TRUTH
                ↓
       Core1 × Core2 validated join
                ↓
        Engineering Request
                ↓
        Engineering Manifest
                ↓
CANONICAL ENGINEERING REGISTRY
(base + digest-bound extension catalog)
                ×
EXTERNAL ENGINEERING INVARIANT PROFILE
                ×
GENERIC ENGINEERING DEPTH POLICY
                ↓
      VALIDATOR-DERIVED ADMISSION
                ↓
     TRANSITIVE PREREQUISITE CLOSURE
                ↓
       ENGINEERING CLOSURE RECEIPT
                ↓
          EXACT CUSTODY BINDING
                ↓
  Canonical Domain Registry / CDAU / SDU / LAU
```

Blueprint does not know mathematical topics. It receives only exact Engineering identities, validated gate state, depth policy results and deterministic prerequisite closure.

## Canonical extension composition

The base registry remains:

`policies/mathematics-technical-engineering-gates.v1.json`

Canonical additions are discovered only through:

`policies/mathematics-engineering-extension-catalog.v1.json`

The catalog binds to the exact base Git blob and to the exact Git blob of every ordered extension. `engine/engineering_registry_composition.py` contains no topic-specific extension filename. An extension binds to the exact base registry ID/blob, expected pre-extension gate count and expected composed gate count; duplicate gate identities fail closed.

Adding a new mathematical subtopic therefore changes governed Engineering data and catalog custody, not Blueprint/runtime topic logic.

## External invariant profile

`policies/mathematics-engineering-gate-invariants.v1.json` holds gate-specific mathematical invariants as **data**. The production validator understands only generic invariant categories:

- required concept IDs;
- required equation IDs;
- required representation IDs;
- required misconception IDs;
- required prerequisite IDs.

There are no `if gate == <topic>` branches in the production validator. Current migrated invariants may name current mathematical gates in the data file, but changing or adding those invariants does not require production Python changes.

The invariant profile is independently included in `validator_contract_digest`, so changing it automatically makes old downstream Engineering custody stale.

## Readiness rule

Declared registry readiness is necessary but never self-authorizing.

```text
ENGINEERING SCHEMA PASS
+ GLOBAL ID / CROSS-REFERENCE / PREREQUISITE GRAPH PASS
+ EXTERNAL INVARIANT PROFILE PASS
+ release_checklist internally consistent with declared READY state
+ technical_readiness == ENGINEERING_GATE_READY
+ source scope not held
+ requested engineering-depth profile PASS
= Blueprint technical admission may proceed
```

A gate cannot rescue missing required content merely by declaring itself READY. Conversely, Blueprint does not invent or upgrade Engineering readiness from memory, titles, examples, fuzzy matching or local special cases.

## Engineering depth

`engineering_depth` is executable, not decorative. Every request selects one of:

```text
FOUNDATION
STANDARD
RESEARCH
```

The generic policy is:

`policies/mathematics-engineering-depth-policy.v1.json`

The policy contains structural thresholds only. It never contains topic names. Current `RESEARCH` admission requires a stronger reasoning/model-condition/misconception/transformation/falsification/provenance structure, including coverage of all four Core transformation roles. If a gate is sufficient for `STANDARD` but insufficient for `RESEARCH`, the same gate is admitted at STANDARD and blocked at RESEARCH with generic failure codes.

This is how a future deep subtopic is handled: Engineering supplies the gate data; the request selects `RESEARCH`; the same generic depth evaluator decides admission. Blueprint is not edited for that subtopic.

## Bounded manifest

The manifest may declare at most three direct gates. The Workbench recursively computes all Mathematics prerequisites. Direct-gate count is a relay bound, not a limit on transitive technical closure.

No title matching, substring matching, semantic matching, LLM matching, conversation memory, or hidden alias may create authority. Exact gate identity and exact registry `linked_buckets` membership are the only Workbench resolution mechanisms.

## Exact closure custody

Downstream consumers do not redeclare prerequisite closure. `mathematics-engineering-binding.schema.json` stores exact custody of:

- request and manifest digests;
- closure receipt ID and digest;
- technical registry digest;
- validator-contract digest;
- exact scope/direct/transitive gate identities;
- named downstream consumer.

The validator-contract digest includes the Engineering schema, validator source, registry composer source, extension catalog, all canonical extension source files, external invariant profile and Engineering depth policy. Any change to those admission inputs makes old custody stale automatically.

`validate_mathematics_engineering_binding.py` recompiles current Workbench closure. Registry, policy, validator, extension or closure drift blocks consumption.

## Authorization boundary

A READY engineering closure means only:

> the requested Mathematics scope satisfies current technical Engineering authority, its requested depth profile and validated prerequisite closure.

It does not prove pedagogy, learner mastery, transfer legality, source legality beyond recorded provenance, visual usability, or publication readiness.

Every Passport therefore carries:

`publication_authorization = NOT_IMPLIED`.

## Generic extensibility proof

The test suite constructs an additional synthetic gate entirely from extension data, composes it after the current canonical extension set and validates the result through the production validator. No production Python is modified for the synthetic gate.

The same suite proves:

- exact-ID resolution without fuzzy/memory fallback;
- recursive prerequisite closure;
- upstream cycle rejection;
- data-driven mathematical invariants;
- catalog/base/blob/count drift rejection;
- duplicate extension gate rejection;
- `STANDARD` versus stricter `RESEARCH` admission without topic-specific branches;
- exact stale-binding rejection.

The architectural invariant is:

> **Engineering owns mathematical truth and gate-specific data. Blueprint owns generic orchestration only. New topics, subtopics and depth changes flow from Engineering data through generic validation; they never become remembered or hard-coded Blueprint cases.**
