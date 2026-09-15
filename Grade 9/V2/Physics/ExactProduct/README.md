# Physics V2 — P-L Exact-product quality gate

P-L implements issue #260 under the #320 catch-up. It is the publication-quality firewall
after P-K cold-start generation, and it is **fail-closed**.

```text
P-K exact artifacts (two PDFs + page maps + run report + coverage closure)
-> machine exact-product gate
-> AI pre-review (advisory only)
-> authorized Physics subject review        [PENDING]
-> authorized pedagogy review               [PENDING]
-> authorized assessment review             [PENDING]
-> authorized visual/usability review       [PENDING]
-> frozen PR #156 mature-design comparison  [NOT_RUN]
-> V2_MATURE_INSTRUCTIONAL_PRODUCT
```

## Seven states, tracked independently

```text
PUBLICATION_ENGINEERING   machine-settable
SUBJECT_CORRECTNESS       authorized human only
PEDAGOGICAL_DESIGN        authorized human only
ASSESSMENT_DESIGN         authorized human only
VISUAL_USABILITY          authorized human only
MATURE_DESIGN_QUALITY     derived, never declared
REFERENCE_COMPARABILITY   derived, and the comparator may only run last
```

No state may impersonate another. A machine pass with no attestation cannot make a human
state `PASS` (`MACHINE_GREEN_CLAIMED_AS_PEDAGOGY_PASS`), an AI review cannot satisfy a
human state (`AI_PRE_REVIEW_COUNTED_AS_HUMAN_REVIEW`), and `MATURE_DESIGN_QUALITY` is
computed from the others rather than set (`MATURE_CLAIMED_WITH_A_PENDING_REVIEW`,
`MATURE_CLAIMED_WITH_A_FAILED_REVIEW`).

## Exit codes

```text
0  PASS     exact product and every required release gate resolved PASS
1  FAIL     a machine or review gate failed
2  BLOCKED  machine gates green, but a required authorized review or exact artifact is missing
```

Machine-green with missing human review returns **2**, never 0
(`BLOCKED_REPORTED_AS_PASS`).

## Current honest state

```bash
python "Grade 9/V2/Physics/ExactProduct/engine/evaluate_physics_exact_product.py" \
  --run-dir /tmp/physics-v2-cold-start/with-attempts
```

```text
PHY P-L exact product: BLOCKED — BLOCKED_PENDING_AUTHORIZED_REVIEW_OR_EXACT_ARTIFACT
  machine gate: PASS (0 findings)
  PUBLICATION_ENGINEERING    PASS
  SUBJECT_CORRECTNESS        PENDING
  PEDAGOGICAL_DESIGN         PENDING
  ASSESSMENT_DESIGN          PENDING
  VISUAL_USABILITY           PENDING
  MATURE_DESIGN_QUALITY      PENDING
  REFERENCE_COMPARABILITY    NOT_RUN
```

**No authorized human reviewer has examined any Physics V2 artifact.** The Physics product
is not mature and this gate says so. Chemistry's C-L (#274) was closed by marking things
complete despite a FAIL pre-review and zero human review; that is precisely what this gate
is built to make impossible here.

`learning_effectiveness` defaults to `STUDY_REQUIRED` and can never be `VALIDATED` from a
rendered PDF (`LEARNING_EFFECTIVENESS_CLAIMED_FROM_A_POLISHED_PDF`).

## Machine gates

Twenty machine failure codes are checked against the real artifacts, including handout
answer leakage, internal-token leakage onto the learner surface, label-only figures,
off-page text, minimum font size, physical-page custody, exact artifact hash binding,
source and external-corpus coverage reconciliation, missing Core2 pages, thin hint ladders
and solutions without verification. All are falsifier-tested by mutating the real run.

## The AI pre-review is advisory and says so

`audit_physics_exact_candidate.py` produces an `AI_ASSISTED_REFERENCE_REVIEW` record bound
to the exact PDF hashes, carrying `authority: ADVISORY_ONLY`, `sets_quality_states: false`
and `may_set_mature_classification: false`. Its concern list always includes
`NO_HUMAN_HAS_READ_THIS_PRODUCT`. Any record claiming more is rejected.

## PR #156

PR #156 is the frozen mature-design comparator and is admissible **only** at
`REFERENCE_COMPARABILITY`, after all four human gates pass. It is never a producer input:
the P-K manifest does not declare it, and reading it fails
`PR156_USED_AS_PRODUCER_INPUT_BEFORE_FINAL_COMPARISON`. Because the human gates are
`PENDING`, `REFERENCE_COMPARABILITY` is `NOT_RUN` and running it early fails
`REFERENCE_COMPARISON_RUN_BEFORE_HUMAN_GATES`.

## Running

```bash
python "Grade 9/V2/Physics/ExactProduct/contracts/validate_contracts.py"
python "Grade 9/V2/Physics/ExactProduct/tests/test_physics_exact_product.py"
```

The four `PASS` attestations that appear in the test are **synthetic fixtures exercising
the state machine**. They are not recorded anywhere as review, and no shipped run carries
them.
