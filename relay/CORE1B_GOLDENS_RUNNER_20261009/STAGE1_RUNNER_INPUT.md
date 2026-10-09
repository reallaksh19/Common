# Runner B — Stage 1 ONLY: Core1B learner goldens / 4×7 QRT

**Case:** Grade9v3.5 / Core1B — three student-facing golden sample cases across the original Question Review Template (QRT) matrix  
**Packet class:** sanitized original-source and Owner WHAT/WHY intake; independent planning only  
**Packet date:** 2026-10-09  
**Status:** PREPARED FOR RESTRICTED RUNNER; **not launched, not sealed, not independently reviewed**

> **Access condition.** The controller/operator must start a **fresh Runner B** in a technically restricted, read-only workspace containing *only* this packet and the listed immutable source files at the pinned historical cutoff below. Do not provide ongoing Agent A chat/history, current GitHub, current pull requests, recent changes, test results, expected golden answers, Stage 2, or the operator guide. If that separation cannot be enforced, the Runner must report `STAGE1_ISOLATION_NOT_ENFORCED` and stop; if it has already seen the current Agent A implementation, report `STAGE1_CONTAMINATED` and request a fresh session. Markdown alone is not an isolation mechanism.

## A. Governing responsibility and honest provenance

- **Responsibility:** Examine how to preserve three meaningful, student-facing Core1B reconstruct-and-repair cases as **golden regression fixtures**, each exercising an intentionally different part of the existing 4-band × 7-demand QRT matrix, without mistaking a browser click or a scored count for actual learning.
- **Owner utterances (verbatim from the active conversation; these are source requirements, not independent proof of acceptance):**
  - “now shoe me real 3 cases, were I can try as student”
  - “buttons are not working”
  - “could have been a better message which kid will feel motivated.”
  - “Where is the answer1”
  - “save 3 samples, covering diff 4x7 matrix, we will have these as golden fixtures, then we save in your PR”
- **Additional expressed purpose, still to evaluate against actual source:** Core1B is intended to elicit learners' own reconstruction, identify and repair a misconception, and challenge transfer at a changed boundary—not just to serve as a second explanation or gated answer key.
- **Original governing parent:** Grade9v3.5 issue #294, *[IMO CORE PLAN] Rights-aware source Core2 and canonical-math Core1A vertical slice*. The issue's latest mutable discussion is **not** a Stage 1 input.
- **Repository:** `reallaksh19/Grade9v3.5`.
- **Immutable historical research cutoff:** `778eb35a70517a46108ad0a5dc01dfc89f61c0e3` (a source snapshot recorded before this golden-fixture request). **This is NOT independently established as Agent A's actual task-start SHA. Actual task-start: UNKNOWN.** Do not substitute moving `main` or later commits.
- **No claim** of official exam-source custody, curriculum adoption, teacher authorization, learner trial, product release, or independently accepted QRT mapping.

## B. What must work, and why it matters

1. **Three useful, distinct student journeys.** A Grade 9 learner must see a coherent problem, make an independent initial attempt, receive *diagnostic rather than answer-spoiling* prompts, repair reasoning, locate a clearly labeled worked explanation after appropriate commitment, and separately attempt a changed-boundary question. A short or incorrect first idea must be welcomed. The Owner's “buttons are not working” report makes the interaction's actual usability an acceptance concern.
2. **Motivation and findability.** The first instruction should invite thinking without implying that random text is the goal. “Where is Answer 1?” must have an immediately discoverable, accessible explanation at the correct stage—not an invisible or misleading reveal.
3. **Goldens, not just stored questions.** Future regression tests should detect meaningful losses in problem meaning, staged commitments, misconception diagnosis, worked reasoning, boundary independence, source identity and student-facing behavior—not merely a file count or green badge.
4. **Honest 4×7 relationship.** The authoritative matrix has seven demand dimensions (`RETRIEVE`, `EXPLAIN`, `APPLY`, `MODEL`, `REPRESENT`, `SYNTHESIZE`, `JUSTIFY`) crossed with four bands (`D1`–`D4`). These are **28 possible cells**. Three samples cannot validate every cell. The correct demand/band placement for each sample must be justified from the original matrix and the decisive learner work, not preselected or treated as approved classification.
5. **Authority boundaries.** The mathematics divisibility case belongs to an authored TEST pilot, not an official licensed SOF/NCERT problem. The algebra and physics cases were introduced as demonstrations in the conversation and are not accepted curriculum/source packages. Preserve that distinction.

## C. Three original user-visible task prompts (INPUTS, **not expected answers**)

The following are situation inputs taken from the student-facing conversation. Their full solutions and any later Agent A fixture payloads are deliberately withheld.

**Case A — consecutive factors / mathematics.** A student checks `t=3,4,5` and finds `(t−2)(t−1)t` divisible by `6`. The student says checking these values proves it for **every integer `t≥3`**. Ask the learner whether that is a valid universal proof and to reconstruct the reasoning for arbitrary `t`. Changed situation: test a related assertion about *two* consecutive factors and explain its validity or failure.

**Case B — algebraic identity / mathematics.** A learner writes `(x+2)² = x²+4`, and notes agreement at `x=0`. Ask whether the claimed identity holds for every real `x`, what the original multiplication means and why one matching example may mislead. Changed situation: identify which input values, if any, make the proposed equality true.

**Case C — journey / physics.** A student walks `60 m` east followed by `60 m` west in `40 s`, ends at the start and says the average *speed* must be zero. Ask the learner to choose the physical quantities, interpret the journey, and distinguish any wrong inference. Changed situation: `60 m` east and `30 m` west in `30 s`; consider both the relevant averages and direction.

**Authenticity:** these are authored/conversation teaching prompts; no claim that cases B/C came from authenticated exam papers or that any worked answers are independently reviewed. No synthetic learner clicks count as human learning outcomes.

## D. Immutable ORIGINAL source allowlist (exact historical cutoff only)

The operator must supply repository file bytes **at `778eb35a70517a46108ad0a5dc01dfc89f61c0e3`**, not a live GitHub checkout. File Git object IDs below were read back at the cutoff; they identify immutable blobs, **not a source-acceptance signature**.

| Original file allowed for independent inspection | Git blob ID at frozen cutoff |
| --- | --- |
| `Shared/quality/question-demand-matrix.v1.json` | `3779a53ae7d20efbb4644bc3f9243909e93dc145` |
| `Shared/vocabularies/cognitive-demand.v1.json` | `b19b39586632cabb637a61fd05fdaaef105305ef` |
| `Shared/tools/question_review_matrix.py` | `42a51307d8d0f4b5254c610f7fefd62e27a09cd5` |
| `Shared/tools/render_core.py` | `9302174e1491138a459a80e9d3f176b83b19e6d7` |
| `TEST/imo-research/pilots/core1a-render-qualified-divisibility.v1.json` | `e8b1dcae1014f9a9a2cce7c2489b21b36c049f81` |
| `TEST/products/core1b-authored-reconstruction-journey.manifest.json` | `35b57884c605e324542201d99c62ff42174a2699` |
| `tests/test_core1b_reconstruction_maturity.py` | `b340269974323da72e4bd3d58ae19449728bb852` |
| `tools/site-audit/core1b-reconstruction-audit.mjs` | `08db5ee227a5ce0f16f8431e1276684ed7a9474d` |
| `.github/workflows/core1b-reconstruction-maturity.yml` | `3fbd48692b1f302d7d709ee0f1245f6f4cef4973` |

**Original-consumer questions (not architectural answers):** inspect how the original authored pilot becomes role-specific HTML; how learner commitments/reveals are represented; how the matrix resolves a demand × band; how the original tests and browser checks observe behavior; and where those observables fail to demonstrate actual Grade 9 understanding. Trace actual source-to-UI call sites and back again. If a necessary direct import/source is not on the allowlist, record **NEEDS_OPERATOR_ALLOWLIST_DECISION**; do not silently open another file or use current GitHub.

**Authentic input-fixture status:** the TEST pilot JSON and manifest exist at the pinned cutoff. Authentic licensed exam inputs for all three cases: **NOT ESTABLISHED**. Student attempt transcripts/observations: **NOT PROVIDED**. Goldens' expected reference answers: **WITHHELD**. These omissions are genuine uncertainty, not negative test results.

## E. Three independent, falsifiable challenge questions

- **Q1 — Source/authority:** From the pinned original code, which precise definitions and records determine a QRT cell and whether a problem is authorised TEST-only or canonical? How could a plausible but unsupported classification or source provenance be detected?
- **Q2 — Actual consumer and UX invariants:** Follow the original role-specific source to what the learner sees and does. Which original source/consumer links matter for independent attempts, diagnosis, repair and separate boundary reveal? Identify missing observations, including whether a short answer, paper response and early solution exposure are distinguishable from understanding.
- **Q3 — Real positive/negative acceptance:** What minimal three-case fixture-plus-test strategy would catch loss of mathematical meaning, misleading kid-facing language and accidental answer leakage *while* correctly stating that three cases cannot exercise all 28 QRT cells? Give genuine positive, negative, stale-source, ambiguous/provenance and user-observed oracles.

## F. Independent Runner work, not copied from Agent A

**No current Agent A code, changes, tests, PR metadata, CI statuses, solutions, template answers, or Stage 2 disclosure are supplied.** You are not asked to verify Agent A's approach. Use only this frozen source and authentic input card.

1. Reconstruct Owner intent → falsifiable outcomes → original source symbol → real consumer → unresolved gap, citing frozen paths and actually inspected functions.
2. Independently derive a defensible classification for each case; explain uncertainty, alternatives and what would invalidate your classification.
3. Formulate at least **two materially different feasible engineering designs**, their preservation/complexity/test tradeoffs and decisive evidence that would make you change your preferred design.
4. Construct at least **three concrete counterexamples** to your leading design (including response handling, answer ordering, source provenance and noncanonical cases as appropriate); keep real positive examples separate from synthetic stress tests.
5. Specify a bounded next implementation plan with authentic downstream checks, unanswered questions, High ROI and parked Medium ROI, and explicit Owner-held approval boundaries. Do **not** implement it yet.
6. Explain three ways your own proposed plan might be wrong and a decisive observation for each.
7. Produce a **new** `INDEPENDENT_STAGE1_RECONSTRUCTION.md` for external readback and freeze. An operator must verify exact bytes/digest and input visibility before any Stage 2 admission. Do not alter Agent A's repo/issues or grant yourself a writer lease.

**Stop at Stage 1.** Valid final labels only: `STAGE1_READY_FOR_EXTERNAL_SEAL`, `STAGE1_ISOLATION_NOT_ENFORCED`, `STAGE1_CONTAMINATED`, `STAGE1_INCOMPLETE_MISSING_EVIDENCE`. "Ready" requires independently verified technical isolation, not a self-assertion.

## G. Explicit pending / parked / unknown

- **Pending:** independent source-to-consumer interpretation, three defensible QRT classifications, meaningful golden behavior checks, kid-friendly and accessible interaction, solution/boundary custody, and human learner validation.
- **Parked:** filling the other 25 matrix cells, curriculum admission, non-TEST publication, authenticated exam-source harvesting, unrelated relay/platform refactoring, and automation of agent readiness. Re-entry only on a distinct Owner scope grant with source/custody evidence.
- **Unknown:** actual initial Agent A task-start SHA; whether the fresh Runner workspace can be strictly isolated; actual Stage 1 Runner identity; provider context/token telemetry; official-source rights; accepted reviewer outcome; externally observed learner effect.
- **Runner trigger:** **Owner explicitly requested preparation**. This is not a measured agent-life threshold, not a 70% crossing, and not a Runner launch.

**End of Stage 1-only packet.**