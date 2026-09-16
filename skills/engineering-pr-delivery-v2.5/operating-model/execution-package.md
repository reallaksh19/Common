# Execution package (EP)

An EP is a forward-looking executable contract derived from exactly one roadmap frontier work package.

The current kernel already requires the major EP categories. The completion architecture strengthens them from structural presence to semantic sufficiency; see `completion-architecture.md` and WP-01 in `catchup-completion-roadmap.md`.

## One work package per EP

```text
one executable frontier WP -> one EP
```

Defining several future work packages does not make them one EP. Under serial execution, only the current frontier WP receives material execution authority.

## Semantic sufficiency target

A completed V2.5 EP must contain enough durable engineering information that a zero-context candidate can discover the repository, understand the current slice, identify current authoritative/editable inputs, resolve current required benchmarks/oracles, execute bounded implementation steps, verify acceptance, report exact results, and prepare the successor without prior chat.

Required categories remain:

- immutable identity and predecessor baton;
- exact roadmap revision/objective/phase/work-package;
- observable outcome and context capsule;
- executable repository-discovery contract;
- typed inputs with authority/source/value/editability/applicability/resolution/staleness;
- typed benchmarks/oracles with payload/expected result/tolerance/independence/applicability/resolution;
- allowed-write, allowed-read, protected, prohibited and Owner-reserved scope;
- structured anti-drift/staleness conditions;
- executable implementation steps with targets, reads, writes, inputs, tests, acceptance, expected intermediate state and stop conditions;
- quality-blueprint applicability with reasons;
- weighted acceptance and classified validation;
- true stop conditions distinct from evidence/quality limitations;
- exact structured return/report payload;
- checkpoint duties and successor duties.

## Slice-specific readiness

Inputs and benchmarks are not globally blocking merely because they appear in the EP. Each one declares applicability such as:

```text
CURRENT_STEP_REQUIRED
CURRENT_EP_REQUIRED
FUTURE_STEP
INFORMATIONAL
```

and resolution such as:

```text
READY
OWNER_EDITABLE_READY
DEFERRED_NOT_CURRENTLY_REQUIRED
MISSING_BLOCKING
INVALID
STALE
```

Only an unresolved condition applicable to the currently authorized slice can remove current WRITE permission. This preserves evidence truth without recreating an "everything is blocked" workflow.

## Discovery

Discovery is executable, not narrative. A discovery step names an action, target, question, expected outputs, receipt requirement and reconciliation/stop condition. The candidate records results in a `DISC-xxxx` Discovery Receipt during takeover certification.

## Scope and authority

Scope does not silently expand. Protected/prohibited domains and invariants carry reasons. If acceptance requires a prohibited or Owner-reserved change, the EP becomes stale or requires an explicit authority/roadmap transaction.

## Report contract

A list of section names is insufficient. The EP defines the required structured payload for acceptance reconciliation, changed files, evidence, quality findings, discoveries, limitations, roadmap/issue impact and ordered next work. Generated reports remain projections of authority objects; they cannot override the EP, checkpoint or roadmap.

## Failure rule

The EP fails semantic sufficiency if a new candidate needs hidden chat context to resolve a material instruction, authority source, current input, benchmark/oracle, scope boundary, implementation step, required test, acceptance criterion, report obligation, successor duty or staleness condition.

The current kernel validators do not yet enforce all semantics in this document. WP-01 implements that transition and must add negative regressions for deliberately hollow EPs.