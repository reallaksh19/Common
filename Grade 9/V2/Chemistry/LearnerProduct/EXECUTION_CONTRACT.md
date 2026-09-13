# Chemistry V2 Learner Product — canonical Core (1A) / Core (2A) execution contract

This document is the repository-authoritative execution contract for Chemistry Core (1A) and Core (2A). A future agent must be able to run the learner-product process from repository inputs without reconstructing decisions from chat history, PR comments, screenshots, or intuition.

The governing rule is:

```text
IF A PRODUCTION DECISION MUST BE INFERRED, THE CONTRACT IS INCOMPLETE.
```

## Product meaning

```text
C-F LearnerStudyModel
        ↓
C-G Core (1) semantic teaching authority
        ↓
Core (1A) bucket synthesis + learner assimilation
        ↓
C-I Core (2) source-transfer authority
        ↓
Core (2A) source practice + fresh governed challenge practice
```

Core (1A) and Core (2A) are downstream learner-product layers. They may improve teaching sequence, representation, practice, scaffolding and transfer. They may not change source truth, chemistry scope, learner diagnosis/treatment, source-question validity, or release legality.

## Authority order

Lower authorities may not override higher authorities.

```text
1. Source/item integrity and validity
2. C-F LearnerStudyModel / learner treatment
3. C-G Core (1) chemistry and instructional authority
4. C-H representation semantic authority
5. Core (1A) bucket + assimilation authority
6. C-I Core (2) source-transfer authority
7. competitive-archetype authority
8. Core (2A) realization
9. renderer / page composition
```

If authorities conflict, fail closed. Do not repair by guessing.

## Canonical execution order

Every Chemistry learner-product run uses this exact sequence:

```text
C-LP-00 VALIDATE_UPSTREAM_BINDINGS
C-LP-01 FREEZE_SOURCE_DENOMINATOR
C-LP-02 CLASSIFY_SOURCE_INTEGRITY
C-LP-03 SYNTHESIZE_CORE1A_BUCKETS
C-LP-04 BIND_LEARNER_TREATMENT
C-LP-05 DECOMPOSE_LEARNING_ATOMS
C-LP-06 BUILD_REPRESENTATION_SEQUENCE
C-LP-07 BUILD_PROBLEM_FAMILIES
C-LP-08 CLOSE_CORE2_HINT_PRETEACH
C-LP-09 REALIZE_CORE1A
C-LP-10 MAP_CORE2_TO_CORE1A
C-LP-11 REALIZE_SOURCE_CORE2A_ITEMS
C-LP-12 SELECT_CHALLENGE_TARGETS
C-LP-13 GENERATE_CHALLENGE_CANDIDATES
C-LP-14 VALIDATE_CHEMISTRY
C-LP-15 VALIDATE_TAUGHT_SCOPE
C-LP-16 VALIDATE_NEAR_COPY
C-LP-17 BIND_PROVENANCE
C-LP-18 AUTHOR_STAGED_HELP
C-LP-19 AUTHOR_QUICK_CHECK
C-LP-20 AUTHOR_FULL_WORKING
C-LP-21 VALIDATE_ANSWER_CLOSURE
C-LP-22 RENDER_LEARNER_PRODUCTS
C-LP-23 VISUAL_PREFLIGHT
C-LP-24 FINAL_AUDIT
C-LP-25 FREEZE_HANDOFF
```

A stage may be skipped only when its governing policy records `NOT_APPLICABLE` with a reason. Silent skipping is forbidden.

## Stage contract pattern

Every stage is defined as:

```text
CONSUMES -> OPERATION -> EMITS -> PASS GATE / FAIL CLOSED
```

### C-LP-00 — Validate upstream bindings

Consumes exact C-F LearnerStudyModel, C-G Core1Plan, C-H RepresentationBundle, C-I Core2Plan and C-J coverage closure references/digests, plus the competitive registry when fresh challenges are requested.

Pass only when all references, digests, semantic-run relationships and source-denominator custody agree.

### C-LP-01 — Freeze source denominator

Required counters:

```text
TOTAL_SCANNED
ELIGIBLE_IN_TOPIC
PLACED_UNIQUE
EXCLUDED_WITH_REASON
MISSING
DUPLICATE_PRIMARY
```

Required closure:

```text
ELIGIBLE_IN_TOPIC == PLACED_UNIQUE
MISSING == 0
DUPLICATE_PRIMARY == 0
```

No later stage may silently change this denominator.

### C-LP-02 — Classify source integrity

Every retained source question carries one of:

```text
CLEAN
TYPOGRAPHIC_OR_OCR_AMBIGUITY
SOURCE_TRUNCATED_OR_INCOMPLETE
CHEMICAL_OR_DOMAIN_ISSUE
CONTEXT_AMBIGUITY
```

Do not silently repair source text. Any normalized display form preserves the source identity and QC record.

### C-LP-03 — Synthesize Core1A buckets

Group Core1 capabilities only when they share a grounded Chemistry teaching invariant/problem family. Preserve every required capability exactly once under one governed bucket home. Core1 capability is not automatically a learner textbook bucket.

### C-LP-04 — Bind learner treatment

Intrinsic difficulty and learner readiness are separate. Core1A consumes the exact C-F learner state/treatment and may not invent a parallel readiness taxonomy.

### C-LP-05 — Decompose learning atoms

A learning atom is the smallest teachable move required before a linked Core2 demand can legitimately be attempted. Every atom is grounded in upstream lesson/PCK/problem-family authority; missing teaching cannot be patched with free-form agent prose.

### C-LP-06 — Build representation sequence

Default Chemistry representation sequence:

```text
SEE_THE_PHENOMENON
SEE_THE_PARTICLES
SEE_THE_CHEMICAL_STRUCTURE
SEE_THE_SYMBOLS
CONNECT_THE_QUANTITIES
DO_THE_CHEMISTRY
VERIFY_THE_RESULT
CONNECT_TO_CORE2
```

A stage may be `NOT_APPLICABLE` only with a reason. Decorative illustration does not satisfy a reasoning-visual obligation.

### C-LP-07 — Build problem families

Cluster source demands by recognition signal, representation, first move and solution routine rather than by surface wording alone. Active families carry recognition signals, setup, method steps, verification, readiness and exact Core2 release targets.

### C-LP-08 — Close Core2 hint pre-teaching

Internal support semantics:

```text
H1 = key chemistry concept/criterion
H2 = representation/model
H3 = first executable symbolic/quantitative move
```

Every H1/H2/H3 reveal must bind to earlier Core1A teaching evidence. If a hint teaches new Chemistry, the question is not releasable.

### C-LP-09 — Realize Core1A

Realize the bucket plan as a semantic learner manuscript with teaching sections, governed visual refs, problem-family routines, practice and readiness checks. Every learner-facing practice item receives the governed answer path before page rendering.

### C-LP-10 — Map Core2 to Core1A

Every Core2 question receives exact primary bucket/problem-family bindings and H1/H2/H3 teaching bindings. Duplicate primary placement is forbidden.

### C-LP-11 — Realize source Core2A items

Preserve source identity, order, stem/givens/options/subparts/units and QC state. Add learner support around the source without silently rewriting it. Every item carries per-question provenance.

### C-LP-12 — Select challenge targets

Use the Chemistry competitive-challenge policy. Selection is problem-family based and deterministic. Unsupported families are skipped with an explicit reason rather than free-written.

### C-LP-13 — Generate challenge candidates

Generate only from taught Chemistry authority plus an approved competitive archetype. Competition style may shape reasoning demand but may not add curriculum authority.

### C-LP-14 — Validate chemistry

Generated items and worked solutions must be independently checked where applicable. The current family validators cover notation roles, particle/coefficient translation, atom conservation, condition preservation and electron-transfer role logic; additional families require their own governed validators before generation.

### C-LP-15 — Validate taught scope

Every generated demand, helper and solution step must be supported by the taught Core1/Core1A scope and bound problem-family authority. Untaught Chemistry fails closed.

### C-LP-16 — Validate near-copy

Compare every generated prompt against all governed source stems. Exact normalized copies are forbidden; configured sequence-similarity/token-overlap ceilings must pass.

### C-LP-17 — Bind provenance

Every question carries learner-visible provenance. Source questions identify their source in learner-readable form while retaining exact machine custody separately. Generated items state fresh/original status and may not falsely claim official past-question provenance.

### C-LP-18 — Author staged help

Support is attempt-first and bound to the already-closed H1/H2/H3 evidence. Learner labels use governed language such as `SMALL CLUE`, `BIGGER CLUE` and `HOW DO I START?` rather than internal registry jargon.

### C-LP-19 — Author quick check

Every objectively checkable learner question receives a concise `QUICK CHECK` suitable for self-correction after the attempt.

### C-LP-20 — Author full working

Every objectively checkable learner question receives complete `FULL WORKING` with Chemistry reasoning, notation/quantities where applicable and independent verification. Open/procedural tasks instead receive an `EXPECTED RESPONSE` rubric.

### C-LP-21 — Validate answer closure

Hard invariant:

```text
objective questions == quick checks == full workings
open questions == expected-response rubrics
```

No learner-facing question is allowed to disappear from the answer denominator.

### C-LP-22 — Render learner products

Consumes only the closed semantic manuscript/plans and the exact C-H RepresentationBundle.

Required behavior:

- deterministic A4 Core (1A) and Core (2A) PDFs;
- governed learner typography from `chemistry-learner-render-policy.json`;
- source and generated lanes remain visibly distinct;
- attempt pages do not expose their quick/full answers;
- C-H selects representations; the renderer only realizes selected primitives;
- every visible string passes the learner-surface identifier firewall;
- physical text/primitive rectangles and artifact hashes are recorded.

Emits `chemistry_core1a.pdf`, `chemistry_core2a.pdf` and `render_manifest.json`.

### C-LP-23 — Visual preflight

Validate the **actual PDFs**, not only the layout plan.

Machine checks include:

```text
artifact hash + page-count custody
A4 physical page geometry
visible-font floor
physical text/primitive page bounds
unintended text/primitive overlap
internal-identifier leakage in extracted PDF text
reasoning-visual obligation closure
first/middle/last raster proof at governed DPI
blank sampled-page detection
```

The raster proof confirms that pages can be rendered and are nonblank. It does not establish mature visual design.

Emits `visual_preflight.json` and raster proof images.

### C-LP-24 — Final audit

Require semantic closure, answer closure, successful PDF realization and C-LP-23 machine preflight. Recompute artifact hashes and emit explicit machine-gate status.

The audit must also preserve the independent human gates:

```text
SUBJECT_CORRECTNESS = PENDING
PEDAGOGICAL_DESIGN = PENDING
ASSESSMENT_DESIGN = PENDING
VISUAL_USABILITY = PENDING
MATURE_DESIGN_QUALITY = PENDING
```

A machine PASS must set `release_authorized=false` until those gates are granted by authorized review.

### C-LP-25 — Freeze handoff

Freeze a reusable handoff containing exact semantic refs/digests, rendered artifact hashes/page counts, final audit ref/digest and the files required for a new agent to continue without chat history.

Required status before human review:

```text
MACHINE_COMPLETE_HUMAN_REVIEW_PENDING
```

The handoff must say what review/action is next; it may not relabel machine publication engineering as expert release approval.

## Golden process fixture

`golden/some-basic-concepts/` contains a deliberately small synthetic formula/particle/conservation process golden. `build_render_golden.py` runs it through C-LP-25 and CI uploads the resulting PDFs, raster proofs and manifests for actual-size human inspection.

The golden explicitly makes no production, NCERT-provenance or human-release claim and does not replace the 68-question Some Basic Concepts denominator preserved in the authoring handoff.

## Release rule

A Chemistry learner product is machine-complete only when all C-LP stages applicable to the requested products pass and the frozen handoff exists. It is **release-complete only after the separately governed human subject, pedagogy, assessment and visual/mature-design gates are granted**.
