# COMB-03 - Production QA

Status: `INTEGRATED_PACKAGE_STATIC_QA_PASS`

| Gate | State | Evidence |
|---|---|---|
| issue #86 scope | PASS | tilings, path/state counting, deterministic state machines, recurrence derivation, reverse search and representation counting retained |
| current production base | PASS | refreshed onto `grade9-ioqm-90q-corpus-v1` after COMB-05 merge |
| COMB-01 provider | PASS_ACCEPTED | exact stable counting/model interface consumed; C01-1..C01-10 PASS |
| COMB-01 compatibility | PASS_6_OF_6 | retrieval-only, exact-one-branch, identity, overlap fail-closed, state-memory and ownership tests all PASS |
| ALG-04 provider | PASS_ACCEPTED | notation, initialization, explicit-v-recursive and algebraic verification retrieved only after structural derivation |
| Wave-0 promotion | PASS | provider/overlap gates passed before integrated learner prose was authored |
| ownership overlap | PASS | COMB-01, ALG-04, COMB-04 and NT-05 boundaries revalidated |
| source anchors | PASS | 2024 Q14/Q20; 2023 Q08/Q21/Q26 |
| historical answers | PASS | 80, 10, 59, 15, 19 independently verified |
| correction overlay | PASS_NOT_APPLICABLE | no overlay event for five COMB-03 anchors |
| source coverage / PYQ map | PASS | `01_Source_Coverage_Map.md` |
| integrated Assimilation Book | PASS | state-first doctrine, tilings, hidden memory, reverse search, carry state and recurrence-not-always contrast |
| First-Step Reference | PASS | compact object/state/sufficiency/exactly-once/base/representation/verify router |
| Recognition Lab | PASS_8 | representation and boundary recognition without method labels in answers |
| First-Line Lab | PASS_8 | state/first-transition writing before arithmetic |
| practice ladder | PASS_20 | five learner-visible stages; support fades without internal hint codes |
| transfer coverage | PASS | tilings -> strings -> finite memory -> deterministic machine -> partitions -> carry/bounded representation |
| first mastery attempt | PASS | Mixed Mastery Test is unlabelled and unhinted |
| mastery items | PASS_10 | numeric, modelling, WHY-NOT and boundary items |
| teacher key synchronization | PASS | all recognition, first-line, practice and mastery items answered in order after the corrected mastery-1 value |
| independent final-item audit | PASS_AFTER_CORRECTION | `Authoring/Independent_Final_Item_Audit.md`; pre-custody mismatch 89 -> 55 caught and corrected |
| metadata schema | PASS | frozen 31-column schema; 51 rows = 5 historical + 46 author-created |
| answer verification flag | PASS | every promoted row records `answer_verified_independently=true` |
| separate microstream interfaces | PASS_7 | tilings; path/state counting; deterministic machines; recurrence derivation; reverse search; representation counting; source audit |
| stable downstream interface | PASS | `Authoring/COMB03_Stable_State_Recurrence_Interface_v1.md` |
| learner prose control-plane scrub | PASS | no H0/H1/H2/H3, T2/T3/T4, wave states, owner/topic codes, dependency or architecture labels in learner Markdown/PDF text |
| student PDF preflight | PASS | 5 pages, openable, unencrypted, text-based |
| student PDF render inspection | PASS | all 5 pages inspected; no clipping/overlap/black squares/broken glyphs |
| teacher PDF preflight | PASS | 1-page custody companion, openable, unencrypted, text-based; full solutions remain in `Teacher_Diagnostic_Key.md` |
| teacher PDF render inspection | PASS | custody companion inspected; no clipping/overlap/black squares/broken glyphs |
| classroom timing/readability | NOT_RUN | evidence-dependent classroom gate |
| longitudinal retention | NOT_RUN | evidence-dependent |
| psychometric calibration | NOT_RUN | evidence-dependent |
| qualification/pass-mark calibration | NOT_RUN | unsupported by this static package |
| publication approval | NOT_RUN | separate human decision |

## Independent numerical checks

The final wording was recomputed separately from the Teacher Key. Checks include recurrence sequences, finite-state string counts, BFS minima for four machine targets, distinct-part DP, bounded powers-of-two DP and the gap count `C(5,3)=10`.

The independent pass caught one pre-custody mismatch in mastery item 1 (`89` was corrected to `55`). After correction, all promoted numerical answers match the synchronized key and metadata.

## PDF custody

Student:
- SHA-256 `ed7a8765e6a1f3a8649d60c9e7c47684cb27edbc470359f5d2d9aecf6ecb79f1`
- Git blob SHA-1 `c66c4f2123fae04a67bd7629ccea411c1df4b711`

Teacher companion:
- SHA-256 `5345cf2b7ceb6f5a4d290ae7573533ef25d79b6585327b2c400d4f03e987f8f4`
- Git blob SHA-1 `a62a5b8d990ff294cea6968464dde6716aa08f64`

## Static disposition

`STATIC_PRODUCTION_PACKAGE_PASS`

This is not a claim of classroom effectiveness, retention, psychometric calibration or publication readiness. Those gates remain `NOT_RUN`.