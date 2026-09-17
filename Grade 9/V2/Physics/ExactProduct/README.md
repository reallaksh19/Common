# Physics V2 — P-L Exact-product quality and governed release

P-L is the fail-closed quality/release firewall after P-K code generation. P-K may generate the two learner PDFs; P-L decides whether those exact bytes are eligible to be called a mature instructional product.

```text
P-K exact two-PDF candidate
        ↓
machine exact-product gate
        ↓
AI pre-review — advisory only
        ↓
exact artifact-set review binding
        ↓
Shared V2 HumanReview intake
  SUBJECT      → SUBJECT_CORRECTNESS
  PEDAGOGY     → PEDAGOGICAL_DESIGN
  ASSESSMENT   → ASSESSMENT_DESIGN
  VISUAL       → VISUAL_USABILITY
        ↓
all four governed REAL reviews PASS
        ↓
reference-comparison eligibility guard
        ↓
frozen PR #156 comparator may be accessed only here
        ↓
REFERENCE_COMPARABILITY PASS / FAIL
        ↓
derived MATURE_DESIGN_QUALITY
        ↓
V2_MATURE_INSTRUCTIONAL_PRODUCT
```

## Authority boundary

`evaluate_physics_exact_product.py` remains the machine/state-projection primitive and its synthetic attestation path exists for falsifier tests. It is **not** the real mature-release authority.

`evaluate_physics_governed_release.py` is the canonical real-release authority. A `REAL_RELEASE` decision consumes:

- the exact P-L candidate;
- the exact-byte-bound AI advisory review;
- the deterministic two-PDF HumanReview candidate binding;
- a Shared HumanReview `REAL_RELEASE` projection from the Physics review policy, real reviewer registry and real submissions;
- optionally, a final governed reference-comparison receipt after the human gate opens.

Arbitrary JSON attestations are therefore incapable of authorizing a real P-L release. TEST_ONLY projections may exercise the full state machine but are permanently non-releaseable.

## Seven independent quality states

```text
PUBLICATION_ENGINEERING   machine-settable
SUBJECT_CORRECTNESS       governed authorized human evidence only
PEDAGOGICAL_DESIGN        governed authorized human evidence only
ASSESSMENT_DESIGN         governed authorized human evidence only
VISUAL_USABILITY          governed authorized human evidence only
REFERENCE_COMPARABILITY   final-stage governed comparator only
MATURE_DESIGN_QUALITY     derived, never declared
```

Machine success does not imply any human state. AI pre-review does not imply human review. Human review does not imply reference comparability. Mature quality is derived only after all required states resolve PASS.

## Exact artifact-set custody

Physics P-L is a two-product topology. `build_physics_human_review_binding.py` recomputes a deterministic artifact-set digest from the exact SHA-256 hashes of:

- `physics-core-study-guide.pdf`
- `physics-transfer-solution-book.pdf`

Every Shared HumanReview submission must bind the same complete artifact-hash set. The governed release engine recomputes the set digest again before consuming review evidence.

## Human review intake

`review-intake/` contains:

- the four-dimension review policy;
- repository-backed subject, pedagogy, assessment and visual rubrics;
- the REAL reviewer authorization registry;
- a TEST_ONLY reviewer registry;
- the real submissions directory and submission instructions.

The **REAL reviewer registry is intentionally empty**. No authorized human Physics V2 review currently exists. Therefore the current real projection is:

```text
SUBJECT_CORRECTNESS    PENDING
PEDAGOGICAL_DESIGN     PENDING
ASSESSMENT_DESIGN      PENDING
VISUAL_USABILITY       PENDING
```

and `release_evidence_eligible=false`.

Adding a real reviewer or real review submission is an explicit governance event. CI, AI, ChatGPT, synthetic fixtures or an unregistered person cannot create reviewer authorization.

## Final reference-comparison boundary

PR #156 is the frozen mature-design comparator and is forbidden as P-A…P-K producer input. `check_physics_reference_eligibility.py` proves ordering by returning before it reads a supplied reference path unless all governed human gates pass.

The current CI deliberately supplies a nonexistent reference path. Because real human review is pending, the guard must report `BLOCKED_HUMAN_QUALITY_GATES`, `reference_read_attempted=false`, and succeed without that file existing.

A later comparator result must satisfy `physics-reference-comparison.schema.json`, bind the exact candidate digest and both PDF hashes, declare `FINAL_COMPARATIVE_VALIDATION`, and preserve `raw_reference_used_as_runtime_template=false`. A real mature release additionally requires real-release-eligible human evidence and a real-release-eligible comparator receipt.

## Exit semantics

```text
0  PASS     real governed evidence resolves every required gate PASS
1  FAIL     machine, governed human, or final comparison gate fails
2  BLOCKED  required governed evidence is absent, pending, or TEST_ONLY
```

## Current honest state

P-K generation is machine-ready and produces the two real learner PDFs. P-L publication engineering is green. The product is **not mature** because no authorized human reviews exist and the final comparator is consequently not authorized to run.

The canonical CI proof is `.github/workflows/v2-physics-chain-g-to-l.yml`. It builds the exact candidate, projects the empty real HumanReview state, proves the reference cannot be read, and requires the governed release engine to return exit code 2.

`learning_effectiveness` remains separate. A polished/rendered PDF is not evidence of validated learning effectiveness.
