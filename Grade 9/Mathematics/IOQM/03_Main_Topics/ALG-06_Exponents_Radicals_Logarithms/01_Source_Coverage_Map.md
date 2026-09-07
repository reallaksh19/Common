# ALG-06 Source Coverage Map

Status: `SOURCE_AND_CORRECTION_OVERLAY_LOCKED`

ALG-06 has only two historical anchors, but one has a known repository metadata extraction defect. This file makes the correction overlay mandatory so the defective flattened radical can never become learner or teacher content.

## Authorities

- 90Q corpus ledger: `IOQM_2023_2025_90Q_Ledger_v1.csv`.
- correction authority: `Verification/IOQM_2023_2025_Metadata_Correction_Overlay_v1.md`.
- independent-answer authority: `Verification/IOQM_2023_2025_Answer_Verification_Ledger_v1.csv`.
- prompt authority: `02_Production/IOQM_G9_Main_Topic_Prompt_Pack_v1.md`.
- prerequisite provider: `ALG01_Stable_Prerequisite_Interface_v1.md`.

## Historical anchors

| ID | exact controlled stem/mechanism | verified answer | source status | topic-lead status |
|---|---|---:|---|---|
| `IOQM-2025-Q28` | **Use overlay, not stale ledger classifier:** `√(x - √(x+a)) = √a - y`. Domain/sign structure forces careful reversible reasoning; the overlay's independent route obtains `y=0`, then `t=√(x+a)=x-a` and `a=t(t-1)/2`. | `91` | `CLEAN_OFFICIAL`; repository classifier metadata correction required | `SOURCE_LOCKED; RE-SOLVE_TO_BE_EMBEDDED_IN_MATH_AUDIT` |
| `IOQM-2023-Q02` | logarithm reciprocity: with `t=log_a b`, use `log_b a=1/t`; `t+6/t=5` gives the admissible exponent relations, then apply integer constraints | `54` | `CLEAN_VALIDATED` | `SOURCE_LOCKED; RE-SOLVE_TO_BE_EMBEDDED_IN_MATH_AUDIT` |

## Q28 correction rule — hard gate

The first-pass 90Q ledger flattened the nested radical into a difference of simple radicals. That classifier string is **not** an admissible historical stem.

The active overlay states the validated paper relation:

`√(x - √(x+a)) = √a - y`.

Consumption order for `IOQM-2025-Q28`:

1. official paper;
2. active metadata-correction overlay;
3. independent-answer verification ledger.

Never silently rewrite historical source custody from the stale classifier string.

## Independent-answer closure

- `IOQM-2025-Q28 = 91` — verification ledger: `PASS,true`, with `REPOSITORY_METADATA_CORRECTION_REQUIRED` recorded.
- `IOQM-2023-Q02 = 54` — verification ledger: `PASS,true,CLEAN`.

## ALG-01 retrieval boundary

Retrieve:

- target-led representation choice;
- identity vs relation-on-solutions distinction;
- equivalence vs implication-only transformation;
- zero-branch protection;
- candidate verification after one-way moves.

ALG-06 must add the canonical doctrine for:

- exponent normalization/common bases;
- principal-root sign/domain;
- conjugation and nested radicals;
- exact equivalence conditions for squaring/root operations;
- logarithm domain and log-as-exponent conversion;
- candidate validation after non-reversible steps.

## Reversibility audit template

Every learner/teacher derivation involving a root, square or logarithm must annotate:

1. current domain;
2. sign information needed for the next operation;
3. whether the operation is `⇔` or only `⇒`;
4. candidate set generated;
5. check in the original equation when any one-way step occurred.

Current disposition: `HISTORICAL_ANSWERS_VERIFIED; Q28_CORRECTION_LOCKED; TOPIC_MATH_AUDIT_NEXT`.
