# Chemistry V2 generation contract

`GENERATION_CONTRACT.json` beside this file is the authoritative machine-readable
version. This page is the human companion; if the two ever disagree, the JSON wins.

## Why this exists

PR #322 made the Chemistry *page* contracts real: notation safety, realized vector
primitives, identifier-leak guards, placement custody, frozen candidates. What it
did not yet give a cold-start producer was a machine-checkable **orchestration**
contract. A compliant renderer could therefore emit a semantically correct but
instructionally thin page, because the upstream obligations — *which capability,
what depth, which visual, what answer* — were discoverable only by repository
archaeology.

A fresh agent must not have to go looking. Every phase, the registries it needs,
the engines that run it and the order they run in are declared here, and the
cold-start gate **refuses to proceed** if any of them is missing.

```bash
python 'Grade 9/V2/Chemistry/GenerationContract/engine/validate_chemistry_generation_contract.py'
python 'Grade 9/V2/Chemistry/GenerationContract/engine/validate_chemistry_generation_contract.py' \
  --execution-log path/to/execution-log.json
```

## Required phase order

```text
SOURCE_INGESTION -> SOURCE_SCOPE_CLASSIFICATION -> CAPABILITY_DERIVATION -> CORE1_STUDY_MODEL
-> INSTRUCTIONAL_AUTHORING -> PROBLEM_AUTHORING -> PCK_BINDING -> VISUAL_OBLIGATION_BINDING
-> CORE2_PRIMARY_OWNERSHIP -> REALIZATION -> VISUAL_AND_LEGIBILITY_PREFLIGHT -> COVERAGE_CLOSURE
-> CUSTODY_FREEZE
```

| # | Phase | Legacy stage | The obligation this phase owns |
|---:|---|---|---|
| 1 | `SOURCE_INGESTION` | C-A, C-B | Scan the whole supplied corpus and **freeze the denominator before authoring starts**. |
| 2 | `SOURCE_SCOPE_CLASSIFICATION` | C-C | In-scope / out-of-scope with an explicit reason for every exclusion. |
| 3 | `CAPABILITY_DERIVATION` | C-D | Derive what the learner must *do*. Chapter-generic capabilities only; a topic name is never a capability. |
| 4 | `CORE1_STUDY_MODEL` | C-E, C-F | Learner scope and treatment. Never invent a weakness without authorized evidence. |
| 5 | `INSTRUCTIONAL_AUTHORING` | C-G | The full Core 1 teaching spine at competitive-study depth, not summary notes. |
| 6 | `PROBLEM_AUTHORING` | C-G | Practice plus answer custody: an immediate check **and** a full solution, or an explicit rubric. |
| 7 | `PCK_BINDING` | C-G | Actionable helper microcopy. A hint that only names a method is invalid. |
| 8 | `VISUAL_OBLIGATION_BINDING` | C-H | Upstream picks the primitive **before** prose. The renderer places; it never selects or invents. |
| 9 | `CORE2_PRIMARY_OWNERSHIP` | C-I | Exactly one canonical primary page per eligible source item. |
| 10 | `REALIZATION` | C-L | Draw both products deterministically; unrealizable primitives are recorded, never faked. |
| 11 | `VISUAL_AND_LEGIBILITY_PREFLIGHT` | C-L | Inspect the rendered bytes at actual output size against the *learner* target, not just the floor. |
| 12 | `COVERAGE_CLOSURE` | C-J | Reconcile the frozen denominator against what was placed, taught, answered and verified. |
| 13 | `CUSTODY_FREEZE` | C-K, C-L | Freeze exact bytes and semantic custody durably in-repo. |

## Contract-level falsifiers

| Falsifier | Fires when |
|---|---|
| `REQUIRED_PHASE_MISSING` | A phase in `required_phase_order` has no declaration, or a declaration is incomplete. |
| `PHASE_ORDER_VIOLATION` | Declared order differs from the required order, or a dependency points forwards. |
| `REQUIRED_REGISTRY_MISSING` | A declared registry path does not exist in the repository. |
| `REQUIRED_ENGINE_MISSING` | A declared engine path does not exist in the repository. |
| `PHASE_NOT_EXECUTED` | The execution log omits a declared phase, or records it as not executed. |
| `UPSTREAM_PHASE_UNEXECUTED` | A phase ran while one of its declared dependencies had not. |
| `PHASE_EXECUTED_OUT_OF_ORDER` | The execution log order differs from the declared order. |
| `UNDECLARED_PHASE_EXECUTED` | The log contains a phase the contract does not declare. |
| `GENERATION_CONTRACT_DIGEST_DRIFT` | The stored `contract_digest` no longer matches the contract body. |

## What this contract does **not** do

It moves `PUBLICATION_ENGINEERING` only. `SUBJECT_CORRECTNESS`,
`PEDAGOGICAL_DESIGN`, `ASSESSMENT_DESIGN` and `VISUAL_USABILITY` stay `PENDING`
and can only be moved by an authorized human reviewer bound to exact artifact
bytes. The contract encodes that rule in `human_gate_states` and the validator
rejects any other value.
