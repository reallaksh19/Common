# Chemistry learner-product maturity — agent handoff

This is a **working handoff, not a release claim**. It is the sibling of
`../NCERT-Core-Workbench/`, and it exists because that workbench's own "Draft
status / next steps" named four things that were still only documented prose,
plus three more the owner's stress-test review of PR #322 found on top of them.
This handoff records what of that is now first-class machine-checkable contract,
what is not, and in which order to do the rest.

Read `../NCERT-Core-Workbench/README.md` and `WORKFLOW.md` first. Nothing here
replaces them: the authoring discipline is still theirs, and the four topic
baselines are still the proof corpus. What changed is that the rules stopped
being advice and became registries with falsifiers.

## 0. Fast start

```bash
# Refuse to start if any required upstream contract is missing.
python 'Grade 9/V2/Chemistry/GenerationContract/engine/validate_chemistry_generation_contract.py'

# Everything, in phase order.
python 'Grade 9/V2/Chemistry/GenerationContract/contracts/validate_contracts.py'
python 'Grade 9/V2/Chemistry/GenerationContract/tests/test_chemistry_generation_contract.py'
python 'Grade 9/V2/Chemistry/CoverageClosure/tests/test_chemistry_source_ingestion.py'
python 'Grade 9/V2/Chemistry/Representation/tests/test_chemistry_visual_obligations.py'
python 'Grade 9/V2/Chemistry/CoreAuthoring/tests/test_chemistry_instructional_depth.py'
python 'Grade 9/V2/Chemistry/CoverageClosure/tests/test_chemistry_answer_custody.py'
python 'Grade 9/V2/Chemistry/ExactProduct/tests/test_chemistry_legibility.py'
python 'Grade 9/V2/Chemistry/ExactProduct/tests/test_chemistry_learner_copy.py'

# Re-render and re-freeze the exact candidate.
python 'Grade 9/V2/Chemistry/ExactProduct/engine/realize_chemistry_exact_product.py' --out /tmp/chem
python 'Grade 9/V2/Chemistry/ExactProduct/engine/freeze_chemistry_candidate.py' --verify \
  'Grade 9/V2/Chemistry/ExactProduct/candidates/CHEM-C-L-EXACT-CANDIDATE-A'
```

`STATUS.json` beside this file is the machine-readable version of everything
below, including exact hashes.

## 1. Start here, not at the pages

`Grade 9/V2/Chemistry/GENERATION_CONTRACT.json` is now the single entry point.
It declares thirteen phases in dependency order, and for each one its obligation,
its required registry and engine paths, what it produces and which falsifiers it
owns:

```text
SOURCE_INGESTION -> SOURCE_SCOPE_CLASSIFICATION -> CAPABILITY_DERIVATION -> CORE1_STUDY_MODEL
-> INSTRUCTIONAL_AUTHORING -> PROBLEM_AUTHORING -> PCK_BINDING -> VISUAL_OBLIGATION_BINDING
-> CORE2_PRIMARY_OWNERSHIP -> REALIZATION -> VISUAL_AND_LEGIBILITY_PREFLIGHT -> COVERAGE_CLOSURE
-> CUSTODY_FREEZE
```

The gate is fail-closed in both directions. A missing registry or engine path
refuses the contract; an execution log that skips a phase, runs one before its
dependency, or contains an undeclared phase refuses the run. You should not need
to read this README to find your obligations — that is the point of the contract.

## 2. What became a contract in this pass

| Workbench rule (prose) | Now (machine-checkable) |
|---|---|
| "Freeze the denominator before authoring" | `CoverageClosure/registry/chemistry-source-ingestion-profile.json` + `freeze_chemistry_source_denominator.py`. Counters are re-derived from declared evidence and compared with what was frozen; `assert_authoring_allowed` gates the authoring phases. |
| "Derive what the learner actually has to do" | `AssessmentScope/registry/chemistry-capability-taxonomy.json`. 24 chapter-generic capabilities, each with a learner-can statement, required source evidence, PCK family, verification checks and allowed visual families. |
| "Assign visual obligations before prose" | `Representation/registry/chemistry-visual-obligation-profile.json` + a per-lesson, per-question ledger. Nine new quantitative/classification primitive families registered. |
| "A hint must produce a learner action" | `CoreAuthoring/registry/chemistry-helper-pedagogy-profile.json`. Seven intent classes, a verb lexicon, non-actionable patterns, and 25 per-family actionable first moves. |
| "Core 1 is teaching, not a summary sheet" | `CoreAuthoring/registry/chemistry-core1-depth-profile.json`. Eleven spine roles required for every full-learning capability. |
| "No question without a checkable answer path" | `CoverageClosure/registry/chemistry-answer-custody-profile.json`. Both surfaces emit `answer_path`; counters reconcile 41/41/41 live and 68/27/38/11 against the four authored baselines. |
| "8 pt is a floor, not a target" | `ExactProduct/registry/chemistry-legibility-target-profile.json`. Body 10.5 pt, stems 12.5 pt, a derived line cap and a leading-ratio rule. |
| (new) No clinical label on a learner page | `CoreAuthoring/registry/chemistry-learner-copy-titles.json` + `learner_copy_guard.py`. 49 roles mapped; every heading resolved fail-closed; every rendered page scanned. |

## 3. Current artifacts

The frozen candidate is committed at
`Grade 9/V2/Chemistry/ExactProduct/candidates/CHEM-C-L-EXACT-CANDIDATE-A/`.

| File | Bytes | SHA-256 |
|---|---:|---|
| `core-study-guide.pdf` (48 pp) | 147080 | `b2489e20eceb3da69fa634327247aafc4efd177b934682ac700b5c8cfb8a6a7a` |
| `examside-solution-transfer-book.pdf` (13 pp) | 67166 | `81cf064bf685a2f880d54e95825fb7bec10b1b9da628e0739660b32a4c8bf65e` |
| `exact-product-candidate.json` | 8370 | `ce24f1b957b8d5277d9d0129bc13fb5ee664ae2a63645f2a4edf570e58c35e0a` |
| `visual-obligation-ledger.json` | 12210 | `19fff21875327d69332daf6658f13501caf7d0adaab52324f9bbe7e02a7b2f48` |

Frozen package digest: `6df16a446eeafe82800499b49835fdcd0ae87e20a2aacc162c8f99162a89c0e9`.
Candidate package digest: `07bfeef36f44002db28d86776aaca4dcac81ec089f03dde26bc1f3be4edffc98`.

Counters from that build: 41 questions / 41 immediate checks / 41 full solutions;
17 of 17 visual obligations realized; 5 of 5 questions carrying their required
visual; body 10.5 pt; stems 12.5 pt; 47 primitives drawn across 15 kinds.

## 4. Known limitations — read before claiming anything

1. **PR #346's source bundle does not reconstruct.** `bundles/final-sources/`
   decodes to 109144 bytes against a declared 117370; `part000` is 12528 base64
   characters short and `part002` is 1560 long, as committed, so
   `restore_source_bundle.py` fails its own integrity check and gzip cannot even
   start. The per-topic `coverage-ledger.csv` files are therefore **not
   recoverable from this branch**. Everything here that reconciles against the
   baselines uses `HANDOFF_MANIFEST.json` and `tools/validate_handoff.py`, which
   are intact and agree with each other. Restoring those bytes is the single
   highest-value thing an agent with the original workspace can do.
2. **The four topic baselines sit at `FROZEN_ELIGIBLE_ONLY`.** #346 recorded the
   retained denominator but never `TOTAL_SCANNED` or the exclusion count, so
   those counters are marked unresolved and the gate **refuses** to author a new
   chapter from them. This is deliberate: inferring them would be inventing.
3. **The ten new capabilities are declared, not exercised.** The committed
   fixture corpus contains only formula/particle/conservation/condition/species-role
   items, so no quantitative or classification item exists for the cold-start
   producer to bind them to. Their nine visual families are registered as
   `RENDERER_PENDING_FAIL_CLOSED`: a page needing one records it as unrealized
   and nothing is substituted.
4. **Two legibility targets are measured, not enforced.** Rendered pages contain
   spans down to 5.4 pt from the vendored `MasterTemplates/primitives` package,
   so `MIN_FONT_SIZE_FAILURE` was never actually enforced against the bytes.
   `document_minimum_font_pt` now reports it and the profile states plainly that
   it does not pass. `KEY_EQUATION` is unenforced because the authoring plans do
   not yet mark an equation as a distinct render role.
5. **"representation" still appears in body copy.** It is barred from headings
   and deliberately absent from `forbidden_anywhere_phrases`, because the word
   comes from C-G templates, the promoted PCK registry and C-H primitive
   descriptions — rewriting those is a subject-authoring pass, not a renderer
   change. Recorded as `known_learner_copy_debt` in the registry.
6. **No human gate has moved.** `SUBJECT_CORRECTNESS`, `PEDAGOGICAL_DESIGN`,
   `ASSESSMENT_DESIGN` and `VISUAL_USABILITY` are `PENDING`; the release decision
   is `BLOCKED` with exit code 2. Issue #274 stays open and correct. The AI
   pre-review is a firewall, not a review.

## 5. Next steps, in order

1. Restore PR #346's source bundle bytes, or re-export the four topics from the
   original workspace, so the per-item coverage ledgers come back. Without them
   the baselines cannot be promoted past `FROZEN_ELIGIBLE_ONLY`.
2. Supply a source corpus containing quantitative and classification items, so
   the ten new capabilities are instantiated rather than only declared. Their
   obligations will then show as `UNREALIZED` until step 3.
3. Implement vector renderers for the nine `RENDERER_PENDING_FAIL_CLOSED`
   primitive families, starting with `MASS_MOLE_PARTICLE_BRIDGE` and
   `MATTER_CLASSIFICATION_TREE` — those two cover the largest share of the
   68-item Some Basic Concepts baseline.
4. Declare a `KEY_EQUATION` content role in the C-G/C-I authoring contracts, then
   flip that legibility target to `ENFORCED`.
5. Raise the vendored primitive label sizes to 9 pt. This is a shared-package
   change: coordinate with Math and Physics before touching it, then flip
   `DIAGRAM_LABEL` to `ENFORCED` and assert the document minimum against the
   8 pt floor.
6. Do the subject-authoring copy pass that removes "representation" and similar
   producer vocabulary from body text, then add those words to
   `forbidden_anywhere_phrases`.
7. Only then seek the authorized human gates. Machine closure is
   `PUBLICATION_ENGINEERING` and nothing else.
