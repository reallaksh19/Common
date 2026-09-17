# Mathematics Technical Engineering Gate Registry (Grades 9–11)

**Canonical Registry ID:** `REG-MATH-TECH-GATE-V1`  
**Current canonical gate count:** **45**  
**Maturity:** `ENGINEERING`  
**Boundary:** upstream technical/epistemic authority before Blueprint product design  
**Psychometric status:** no unvalidated psychometric claims are promoted into Engineering truth

This document describes the current technical contract. The executable Engineering data, schemas, generic validators, extension catalog and depth policy are authoritative.

## 1. Architectural invariant

```text
MATHEMATICAL TOPIC KNOWLEDGE
        lives in Engineering data
                ↓
generic Engineering validation
                ↓
exact identity + prerequisite closure + custody
                ↓
Blueprint generic orchestration
```

Blueprint/runtime code must not contain topic-specific branches, topic-specific extension filenames, remembered topic aliases, fuzzy title mappings or hidden semantic fallbacks.

A new mathematical gate may require new Engineering data. It must **not** require a new Blueprint implementation for that mathematical topic.

## 2. Canonical source composition

The canonical Engineering graph is assembled deterministically from:

```text
policies/mathematics-technical-engineering-gates.v1.json
        canonical base registry
                +
policies/mathematics-engineering-extension-catalog.v1.json
        ordered digest-bound extension references
                +
referenced Engineering extension data
                ↓
engine/engineering_registry_composition.py
                ↓
REG-MATH-TECH-GATE-V1
```

The composer contains no topic-specific extension path. The catalog binds to the exact base Git blob and to the exact Git blob of each extension. Every extension additionally binds to the stable registry identity, expected pre-extension gate count and expected composed gate count. Stale custody, duplicate gate IDs and count drift fail closed.

The current graph happens to contain one post-base extension and 45 total gates. Those are current repository facts, not composition-engine constants.

## 3. Gate structure

Each Engineering gate is schema-closed and must carry the technical object required by `contracts/mathematics-technical-engineering-gate.schema.json`, including:

1. canonical `subtopic_id` and learner title;
2. chapter/curriculum provenance;
3. authority tier and `ENGINEERING` maturity;
4. declared technical readiness;
5. provenance and claim status;
6. canonical concept identities;
7. prerequisite gate identities;
8. linked curriculum buckets;
9. linked problem-family identities;
10. technical-core invariant statements;
11. equations/formal relations with symbol meaning and validity conditions;
12. mathematical representations;
13. model conditions and validity boundaries;
14. expert reasoning sequence;
15. required transformations across Core roles;
16. misconception traps with counterexamples and repairs;
17. independent verification obligations;
18. problem-family recognition and first moves;
19. intrinsic difficulty profile;
20. release checklist;
21. badges; and
22. explicit falsification cases.

A fluent explanation or topic label without the required technical object is not an Engineering-ready gate.

## 4. Mathematical invariants are data, not validator branches

Gate-specific mathematical invariants live in:

`policies/mathematics-engineering-gate-invariants.v1.json`

The production validator understands generic invariant categories only:

```text
required_concept_ids
required_equation_ids
required_representation_ids
required_misconception_ids
required_prerequisite_ids
```

The validator does **not** contain `if gate == <named topic>` logic. Current gate IDs and mathematical requirements may appear in the Engineering invariant data because that file is part of mathematical authority; adding or changing those requirements does not require a Python topic branch.

The invariant profile participates in `validator_contract_digest`, so an invariant change automatically stales downstream custody.

## 5. Global graph and readiness invariants

Before Blueprint may consume Engineering authority, the generic validator requires at least:

- schema validity;
- globally unique gate, concept, equation, representation and misconception IDs;
- all Mathematics prerequisite gate identities to resolve;
- no self-dependency or prerequisite cycle;
- linked problem-family IDs to resolve inside their owning gate;
- the external mathematical invariant profile to pass;
- intrinsic difficulty dimensions to remain within their allowed range;
- every declared READY gate to have an internally complete release checklist;
- source scope not to be held; and
- the requested Engineering depth profile to pass.

Declared `technical_readiness` is therefore necessary but cannot self-authorize missing mathematical structure.

## 6. Engineering depth is independent of gate identity

An Engineering request chooses:

```text
FOUNDATION | STANDARD | RESEARCH
```

The executable depth rules live in:

`policies/mathematics-engineering-depth-policy.v1.json`

That policy contains structural thresholds, not topic names. The same gate can therefore pass `STANDARD` and fail `RESEARCH` when its Engineering data lacks the generic research-depth structure.

This distinction prevents unnecessary registry proliferation:

```text
same mathematical capability, greater rigor
    → same gate + stronger engineering_depth

new mathematical capability
    → new Engineering gate data

existing gate merely added to a product/exam scope
    → scope/crosswalk membership change only
```

## 7. Stable validation failures

Production validation emits stable machine-readable codes, including:

```text
MATH_GATE_SCHEMA_VIOLATION
MATH_GATE_DUPLICATE_ID
MATH_GATE_INVALID_SUBTOPIC_ID
MATH_GATE_MATURITY_OVERREACH
MATH_GATE_UNRESOLVED_PREREQUISITE
MATH_GATE_DEPENDENCY_CYCLE
MATH_GATE_CROSS_REFERENCE_INTEGRITY_FAIL
MATH_GATE_MISSING_REQUIRED_CONCEPT
MATH_GATE_MISSING_MANDATORY_EQUATION
MATH_GATE_MISSING_MANDATORY_REPRESENTATION
MATH_GATE_MISSING_MISCONCEPTION_TRAP
MATH_GATE_INVALID_DIFFICULTY_PROFILE
MATH_GATE_RELEASE_CHECKLIST_INCOMPLETE
```

The composition layer separately rejects stale catalog/base/extension custody and duplicate extension identity before Engineering admission can proceed.

## 8. Data-derived falsification

`engine/validate_mathematics_engineering_gates.py` generates mutation falsifiers from the current invariant profile rather than maintaining a topic-coded mutation list.

Current CI evidence catches **29 data-derived mutations** through the production validator. The number is evidence from the current Engineering data, not a fixed architecture constant: it may change as invariant data changes.

Generic additional mutations test cross-reference integrity, global identity uniqueness and READY/release-checklist consistency.

This is important because adding a newly governed gate or invariant should extend the falsification surface through data rather than requiring another Python `if` block.

## 9. Generic extension proof

`tests/test_engineering_registry_composition.py` proves the extension mechanism itself, including:

- canonical catalog composition has unique gate IDs;
- stale base-blob custody fails;
- wrong pre-extension gate count fails;
- duplicate extension gate identity fails;
- stale crosswalk/base custody fails; and
- a completely new synthetic Mathematics gate can be created in extension data, composed after the current catalog and validated by the production validator **without modifying production Python for that gate**.

That last test is the architectural acceptance test for topic independence.

## 10. AssessmentScope coverage

AssessmentScope and Engineering use separate canonical vocabularies. Their bridge is exact, versioned and fail-closed.

Historical base crosswalk:

`policies/math-assessment-engineering-crosswalk.mixed-grade9.v1.json`

Current patch:

`policies/math-assessment-engineering-crosswalk.mixed-grade9.v2.patch.json`

The patch may reference a canonical extension only when that extension is present in the current extension catalog and its exact Git blob matches. The crosswalk compiler does not know the mathematical meaning of that extension.

Current mixed Grade-9 evidence is:

```text
required capabilities: 30
Engineering-covered:   30
Engineering gaps:       0
```

These counts describe the current fixture/scope and are not hard-coded production requirements.

## 11. Adding a new subtopic systematically

For a genuinely new mathematical capability:

```text
1. Author Engineering gate data to the schema.
2. Declare prerequisites by exact Engineering gate ID.
3. Add gate-specific mathematical invariants to the invariant data when required.
4. Add the extension file to the digest-bound extension catalog.
5. Run generic composition + Engineering validation + mutation falsification.
6. If an AssessmentScope capability needs the gate, update the exact-ID crosswalk data.
7. Request FOUNDATION/STANDARD/RESEARCH through the generic Workbench.
8. Allow Blueprint to consume only the resulting exact closure receipt/binding.
```

No Blueprint topic branch is added in any of those steps.

If the requested change is only greater depth for an existing mathematical capability, do **not** create a duplicate topic gate by default. Use the existing gate with the appropriate generic Engineering depth profile and enrich the Engineering data if that profile exposes a real structural gap.

## 12. Blueprint boundary

Blueprint computes deterministic closure and product authorization from validated Engineering receipts. It does not maintain a second mathematical truth graph.

The governing invariant is:

> **Engineering owns mathematical truth, gate-specific requirements and topic data. Blueprint owns generic orchestration. New topics, subtopics and rigor levels flow from Engineering data through generic validation and custody; they never become remembered or hard-coded Blueprint cases.**
