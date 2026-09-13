# Physics V2 Blueprint — evidence-adaptive orchestration

This directory is the orchestration layer above the existing Physics role-specific production kits.

It exists to make execution order, authority, routing and handoff discipline machine-enforceable without collapsing Core1, Core2 and Core1A into one monolithic schema.

## Blueprint v1 implemented slice

The first executable tranche now freezes and tests five things:

1. architecture invariants;
2. a common typed packet envelope;
3. normalized evidence state;
4. deterministic first-role routing with three golden fixtures;
5. the independent second-pass protocol that prevents self-validation and hides upstream claims during the ground-truth-only pass.

Next implementation slices are: Core1×Core2 Join, learner/purpose resolution, the Core1A assimilation state machine, Motion-in-2D topic pilot, and finally the publication compiler.

## Authority model

```text
ORIGINAL GROUND TRUTH
syllabus / authoritative source / questions / figures / answers
        |
        v
      CORE0
normalized evidence + route decision
        |
        +---------------------+
        |                     |
        v                     v
      CORE1                 CORE2
        |                     |
        +----------+----------+
                   |
          independent second pass
                   |
                   v
                 JOIN
                   |
                   v
                CORE1A
          assimilation compiler
                   |
                   v
             taught-state receipts
                   |
                   v
                CORE2A
       PLACEHOLDER / DISABLED in v1
```

Execution order is not authority order. Core2 may execute first when the question corpus is the strongest evidence; Core1 remains the semantic-intelligence role. Core1 may execute first when syllabus/source authority is strong; Core2 still performs its own assessment-intelligence pass.

## Independent second-pass protocol

The second role is always a fresh instance. Its validation session is forced through:

```text
PASS 1  GROUND_TRUTH_ONLY
        upstream claims hidden
        -> independent claims digest locked

PASS 2  COMPARE_UPSTREAM
        upstream packet revealed
        -> frozen Pass-1 digest carried forward

PASS 3  EMIT_VALIDATION
        CONFIRMED / REFINED / MISSING / UNSUPPORTED /
        CONTRADICTED / OUT_OF_SCOPE / UNKNOWN
```

A validator instance may not equal any upstream producer instance. A Pass-1 manifest containing an upstream packet fails machine QA.

## Non-negotiable v1 invariants

- Original evidence is authority; packets are claims.
- First role is evidence-adaptive, never topic-name hard-coded.
- Core1 and Core2 are distinct epistemic roles.
- Reusing a specialist profile never means reusing the same agent instance.
- The second role independently re-grounds before seeing upstream claims.
- Every handoff contains at most three subtopics; learning-atom count is not bounded by that transport rule.
- Absence of assessment evidence remains absence of evidence, never a claim of low importance.
- Owner control may alter execution but may not rewrite historical evidence or prior system findings.
- Core1A manuscript generation is downstream of assimilation reasoning, not a substitute for it.
- Core2A is explicitly present only as a disabled placeholder until a semantic contract is approved.

## Running the implemented slice

```bash
python "Grade 9/V2/Physics/Blueprint/contracts/validate_contracts.py"
python "Grade 9/V2/Physics/Blueprint/engine/run_golden_fixtures.py"
python "Grade 9/V2/Physics/Blueprint/tests/test_blueprint_routing.py"
python "Grade 9/V2/Physics/Blueprint/tests/test_blueprint_independence.py"
```

The routing goldens prove three different evidence conditions:

- strong semantic authority and no questions -> `CORE1_FIRST`;
- absent syllabus with a rich/resolved question corpus -> `CORE2_FIRST`;
- weak/ambiguous evidence on both sides -> `BLOCK`.

These are architecture proofs, not topic-specific exceptions.