# WP-01 — Semantic Execution Package implementation

## Outcome

WP-01 converts the V2.5 Execution Package from a mostly structural forward contract into a repository-enforced semantic baton. It does not implement candidate-specific takeover certification; that remains WP-02.

## Delivered enforcement

### Semantic EP validator

`validate_ep_semantics.py` now validates serial active EPs through aggregate conformance and every approved parallel lane EP through `validate_parallel_plan.py`.

It enforces:

- non-placeholder outcome/context needed for zero-context continuation;
- `DSTEP-*` executable repository-discovery instructions with question, expected outputs, receipt requirement and failure/reconciliation behavior;
- typed inputs with authority/source/type/units/editability/applicability/resolution/consumers/validation/staleness;
- current-required inputs cannot be deferred, stale, invalid or missing while an EP claims `EXECUTABLE | ACTIVE`;
- typed benchmarks/oracles with source, oracle class, payload, expected result, tolerance, independence, applicability/resolution, verification mappings and stale conditions;
- semantic scope split into allowed writes, allowed reads, protected, prohibited and Owner-reserved domains;
- structured anti-drift restrictions and invalidation rules;
- implementation steps with exact targets/reads/writes/input IDs/acceptance IDs/test IDs/expected state/stop conditions;
- cross-reference validation from implementation steps to EP inputs, acceptance and tests;
- source-bound report reconciliation payloads for every mandatory report section;
- durable successor-output requirements.

### Discovery namespace

The architecture namespace is now implemented:

```text
DSTEP-* = forward EP discovery instruction
DISC-*  = future candidate Discovery Receipt
```

Legacy `DISC-*` discovery-step IDs fail semantic validation.

### Repository discovery prerequisites

`validate_repo_profile.py` is now part of aggregate conformance. Missing or malformed `REPO_PROFILE.yaml` therefore prevents a repository from claiming a clean relay conformance state.

`validate_repo_state.py` and `repo-state.schema.yaml` now require:

```yaml
relay_protocol:
  version: "2.5"
  basis_ref: "<explicit pinned Common ref>"
```

Placeholder/unbound `basis_ref` values fail procedural validation.

### Report contract

`validate_report_contract.py` no longer stops at required Markdown headings. Every mandatory section must have a payload contract with:

```text
id
section
source objects
required reconciliation fields
```

The generated report remains a projection, never an authority source.

## Canonical template/schema

`templates/EP.yaml` and `schemas/execution-package.schema.yaml` now model the semantic contract used by the procedural validator. `schemas/repo-profile.schema.yaml` and `schemas/repo-state.schema.yaml` were strengthened for the WP-01 repository-admission changes.

Procedural semantic validation remains the enforcement layer. Comprehensive executable JSON-Schema convergence remains BA-003/WP-10 work.

## Regression coverage

`tests/stress/test_semantic_ep.py` proves rejection of:

1. semantically empty current-required inputs;
2. unresolved current-required input while claiming executable state;
3. semantically empty required benchmark/oracle payloads;
4. vague discovery plus `DISC-*` instruction namespace collision;
5. empty executable write scope;
6. unstructured/empty anti-drift rules;
7. vague implementation steps without concrete mappings;
8. report headings without reconciliation payloads;
9. missing repository profile;
10. placeholder protocol basis.

The core serial fixture and reusable parallel-lane fixture were also upgraded to the semantic EP format so old tests exercise the stronger contract instead of bypassing it.

## Boundary intentionally retained

WP-01 proves **baton semantic sufficiency**, not candidate comprehension. It does not add:

- `DISC-*` Discovery Receipt schema/validator;
- `TC-*` Takeover Certification;
- `TAKEOVER_CERTIFIED`;
- `MATERIAL_WRITE_READY` candidate predicate;
- evaluated `QUAL-*` qualification receipts;
- Owner-facing progress/handover redesign;
- GitHub operations or quality-review artifacts.

Those remain in their dependency-ordered successor work packages.

## Acceptance assessment

```text
AC-01-01 rich standalone serial EP passes semantic validation                 PASS
AC-01-02 approved parallel lane EPs pass the same semantic validator          PASS
AC-01-03 hollow required input fails                                           PASS
AC-01-04 hollow required benchmark/oracle fails                                PASS
AC-01-05 vague/legacy discovery instruction fails                              PASS
AC-01-06 empty executable scope fails                                          PASS
AC-01-07 unstructured/empty anti-drift fails                                   PASS
AC-01-08 vague implementation step fails                                       PASS
AC-01-09 headings-only report contract fails                                   PASS
AC-01-10 REPO_PROFILE is admitted by aggregate conformance                     PASS
AC-01-11 relay_protocol version/basis binding is procedurally enforced         PASS
AC-01-12 existing generic kernel regressions remain green before checkpoint    PASS
```

Final WP-01 completion still requires CP-R002 plus scoped CI PASS on the exact commit containing that checkpoint.
