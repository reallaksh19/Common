# Physics V2 V10 stress-test invocation — Grade 9 relative motion

This file is a **thin invocation/custody record**, not a hand-authored stress-test receipt and not Physics or Mathematics authority.

The canonical architecture is `Grade 9/V2/Physics/Blueprint/SELF_HELP_ARCHITECTURE_V10.md` on the current PR #350 base. Cross-domain transport/custody is owned by `Grade 9/V2/Shared/CrossDomain/`; subject readiness remains provider-owned.

## Governed request

Executable request:

`Grade 9/V2/Physics/Blueprint/fixtures/stress-tests/relative-motion-grade9-cbse.request.v1.json`

Scope envelope:

`Grade 9/V2/Physics/Blueprint/fixtures/stress-tests/relative-motion-grade9-cbse.scope.v1.json`

The request itself cannot assert `final_verdict`.

## Compiler authority

Single-request compiler:

`Grade 9/V2/Physics/Blueprint/engine/compile_seven_core_stress_test.py`

Governed batch compiler:

`Grade 9/V2/Physics/Blueprint/engine/compile_all_stress_tests.py`

Cross-domain closure compiler:

`Grade 9/V2/Physics/Blueprint/engine/compile_domain_prerequisite_closure.py`

Shared authority receipt contract:

`Grade 9/V2/Shared/CrossDomain/contracts/domain-prerequisite-authority.schema.json`

Shared demand contract:

`Grade 9/V2/Shared/CrossDomain/contracts/domain-prerequisite-demand.schema.json`

Run a local single-request compilation with:

```bash
python "Grade 9/V2/Physics/Blueprint/engine/compile_seven_core_stress_test.py" \
  "Grade 9/V2/Physics/Blueprint/fixtures/stress-tests/relative-motion-grade9-cbse.request.v1.json" \
  --out /tmp/relative-motion-grade9-cbse.stress-receipt.json
```

## CI custody

At exact PR #350 base commit:

`9bb618d21a3f2d4f94603ae07581f4ec945bcb0d`

the canonical `V2 Physics Blueprint` run `34984496911` completed successfully and uploaded:

`physics-blueprint-v10-stress-receipts`

Artifact archive digest:

`sha256:4f0c01cc311aaabbea2a40c2bc51cb7c9fc610594f80102d91cbd02c746ba643`

The archive contains:

- `manifest.json`
- `relative-motion-grade9-cbse.receipt.v1.json`

Compiler-derived manifest digest:

`sha256:ba8ad0a68589670990f766d438ff162b29d6b3e383442400328aa87238d4c3e8`

Compiler-derived stress receipt digest:

`sha256:411f2435bc24d62a27414adcbf8e0399d2dc10e3ef0635b4f67dc30a376cb67c`

## Cross-domain handoff state

The current compiler output keeps Mathematics prerequisites held and emits provider-routed demands rather than allowing Physics to self-certify them:

- `DOMAIN-DEMAND-PHY-M2D-RELATIVE-V1-MATH-GEO-2D`
  - required by `PHY-VEC-BASICS`
  - provider: `MATHEMATICS`
  - status: `OPEN_HELD`
- `DOMAIN-DEMAND-PHY-M2D-RELATIVE-V1-MATH-TRIG-RIGHT`
  - required by `PHY-VEC-COMPONENTS`
  - provider: `MATHEMATICS`
  - status: `OPEN_HELD`

Both generated demands bind `authority_contract_ref` to `Grade 9/V2/Shared/CrossDomain/contracts/domain-prerequisite-authority.schema.json`.

A future READY transition requires a provider-owned repository receipt satisfying that Shared transport contract plus the provider subject's own semantic/review authority. Raw dictionaries or Physics-owned files cannot satisfy this boundary.

## CI proof

Canonical CI executes:

- `tests/test_blueprint_contract_inventory_v10.py`
- `tests/test_blueprint_scope_v10.py`
- `tests/test_blueprint_domain_prerequisites_v10.py`
- `tests/test_blueprint_stress_test_v10.py`
- `tests/test_blueprint_stress_batch_v10.py`

The generated machine-readable receipt is CI-custodied and is not checked into this PR.

## Non-authority rule

Do not copy a previous receipt, previous Markdown report, chat summary, or remembered result into this PR and call it current.

If repository authority changes, rerun the compiler and use the current CI artifact. The compiler output—not this Markdown file—is the current stress-test result.

This PR therefore contains **no self-authored `STRESS_TEST_PASS`** and no duplicate machine-readable receipt.
