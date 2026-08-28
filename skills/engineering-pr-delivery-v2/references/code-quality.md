# Code Quality and Maintainability

Use this policy for production implementation under `engineering-pr-delivery-v2`.

The objective is maintainable engineering software, not mechanical compliance with arbitrary line counts. Size thresholds are review triggers. Responsibility, authority ownership, testability, and engineering correctness are the stronger rules.

## 1. Default size thresholds

Use these defaults unless a stricter repository-local rule applies:

```text
new production module     normally <= 300 physical lines
function / method          normally <= 40 logical lines
```

Exceeding a threshold does not automatically make code invalid. It requires an explicit review:

```text
THRESHOLD EXCEEDED
  -> identify responsibilities
  -> identify independent test seams
  -> identify authority / state boundaries
  -> split when a meaningful boundary exists
  -> otherwise retain with concise justification
```

Do not create artificial `part1` / `part2` files, pass-through wrappers, or arbitrary helper fragmentation merely to satisfy a line count.

Generated files, controlled source tables, vendored code, migrations, declarative schemas, and other structurally exceptional files may use repository-specific rules. Record the exception rather than silently treating it as ordinary production code.

## 2. Module design

Prefer high cohesion and low coupling.

A production module should normally have one clear responsibility and one clear ownership domain. Split a module when it mixes independently changeable concerns such as:

```text
source parsing
canonical model construction
engineering applicability / authority classification
load / coordinate transformation
numerical evaluation
stress / result recovery
benchmark / oracle construction
release / publication authorization
UI / presentation formatting
persistence / transport
```

For engineering software, modularity should follow engineering authority and state ownership before cosmetic file-size goals.

Avoid god modules that coordinate, calculate, validate, persist, and render the same engineering state.

## 3. Function design

Prefer functions that:

- perform one coherent operation;
- have explicit inputs and outputs;
- expose units, coordinate frames, sign conventions, end conventions, or tolerances where those affect meaning;
- are pure when mutation is unnecessary;
- keep branching shallow enough to review;
- avoid mode flags that switch between unrelated responsibilities;
- make failure behavior explicit.

Extract a function when a block has an independent invariant, test seam, failure mode, or domain meaning. Do not extract trivial one-line wrappers without a real abstraction purpose.

## 4. State and side effects

- Prefer pure calculation functions.
- Keep mutation at explicit store, transaction, session, UI, runtime, persistence, or solver-assembly ownership boundaries.
- No hidden globals.
- No implicit singleton authority.
- No mutation-heavy shared-object designs where ownership cannot be identified.
- Do not let preview, renderer, cache, fixture, or UI state become engineering authority.

State ownership must be reviewable from the code path.

## 5. Dependencies and abstractions

- Prefer explicit imports and dependencies.
- Avoid circular ownership.
- No speculative infrastructure.
- Every new adapter, resolver, service, session, store, registry, provider, abstraction, or production module must have a real production consumer in the same PR unless the approved mission explicitly authorizes a staged prerequisite.
- New unused production modules: `0` by default.
- Avoid abstractions that only rename or forward calls without enforcing a real contract, authority boundary, reuse point, or test seam.
- Prefer existing repository patterns when they remain valid; do not create a parallel architecture for convenience.

## 6. Engineering authority separation

Keep these separable unless the approved methodology explicitly requires coupling:

```text
engineering source authority
applicability / classification authority
canonical input transformation
solver / numerical mechanics
benchmark / independent oracle
acceptance tolerances
result recovery
publication / release authority
UI / presentation
```

A change to one domain must not silently create authority in another.

Examples:

- production output cannot become its own independent benchmark;
- a UI formatter cannot redefine solver sign convention;
- a source parser cannot silently authorize an engineering method;
- a benchmark fixture cannot become runtime default engineering data;
- release metadata cannot create numerical qualification.

## 7. Duplication

Avoid duplicate engineering calculation paths.

Before adding new logic, search for the current owner implementation. If equivalent behavior already exists, either use it or explicitly explain why it cannot own the new behavior.

Do not copy formulas, tolerance tables, sign mappings, unit conversions, or authority classifiers into multiple production locations when one governed owner can serve them.

When duplication is intentionally retained for independent verification, label it as an independent oracle/check rather than a second production authority.

## 8. Error handling and fail-closed behavior

- Do not swallow engineering-significant errors.
- Do not silently substitute fallback engineering data.
- Do not convert unresolved authority into a permissive default.
- Keep error context sufficient to identify the first failing boundary.
- Prefer typed/structured failure where the repository architecture supports it.
- Preserve `NOT_RUN`, `UNRESOLVED`, `UNQUALIFIED`, and out-of-domain states distinctly from PASS/authorized states.

## 9. Testing and testability

Production structure should expose meaningful test seams.

Where applicable, validate separately:

```text
pure calculation
boundary / adapter
authority decision
negative / fail-closed path
integration with the real production consumer
```

Prefer behavior and invariant tests over tests coupled to private implementation details.

For engineering numerics, keep implementation-coupled checks distinct from analytical, authoritative-reference, experimental, or cross-solver evidence.

## 10. Refactoring discipline

Refactor when required to implement or validate the approved mission safely.

Do not use a focused engineering PR as an excuse for broad cleanup.

Avoid:

- unrelated renames;
- unrelated formatting churn;
- unrelated dependency upgrades;
- whole-tree style migrations;
- speculative framework introduction;
- splitting stable large legacy files solely to meet the new-file threshold.

If a legacy file is already large, modify the smallest coherent owner region unless a structural split is necessary for the requested capability or defect repair.

## 11. Pre-implementation code-quality check

Before material production coding, establish:

```text
[ ] existing owner implementation searched
[ ] intended module responsibility identified
[ ] engineering / software authority boundary identified
[ ] state / mutation owner identified
[ ] expected new or modified file sizes reviewed
[ ] independently testable seams identified
[ ] no speculative abstraction planned
[ ] every new abstraction has a named production consumer
[ ] no duplicate calculation / source / tolerance authority planned
[ ] refactor scope is necessary for the approved mission
```

A missing answer is a design question to resolve before adding architecture.

## 12. Post-implementation code-quality gate

For any leg that changes production code, record the following in the endpoint or PR evidence:

```text
[ ] new modules normally <= 300 physical lines, or exception justified
[ ] functions normally <= 40 logical lines, or exception justified
[ ] no god module / mixed authority owner introduced
[ ] no hidden global or implicit singleton authority introduced
[ ] mutation boundaries remain explicit
[ ] no circular ownership introduced
[ ] new unused production modules = 0, unless explicitly staged/authorized
[ ] no duplicate production engineering calculation path introduced
[ ] calculation / source / oracle / publication / presentation boundaries preserved
[ ] failure behavior remains explicit and fail-closed where required
[ ] focused tests cover the new responsibility and negative path where applicable
[ ] no unrelated refactor or formatting churn
```

Size exceptions must identify why a meaningful split would make the design worse or less reviewable. `It was faster` is not sufficient.

## 13. Review priority

When rules conflict, review in this order:

```text
engineering correctness and source authority
-> safety / fail-closed behavior
-> clear authority and state ownership
-> testability and independent validation
-> modular responsibility boundaries
-> maintainability / duplication
-> size thresholds
-> stylistic preference
```

A 220-line module with mixed engineering authority can be worse than a justified 330-line cohesive numerical kernel. Use the thresholds to expose design questions, not to game metrics.
