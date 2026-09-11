# Chemistry V2 generation entrypoint

This is the repository-authoritative cold-start entrypoint for Chemistry V2.

A fresh producer starts only from:

```text
ChemistrySourceSet        REQUIRED
QuestionSet / CorpusSet   REQUIRED
DeclaredTopicScope        REQUIRED
AttemptSet                OPTIONAL
repository-declared authorities
```

It must **not** start from a manually prepared source-obligation ledger, a pre-filtered eligible external-question set, a pre-resolved LearnerStudyModel, a pre-resolved scope package, a pre-classified problem-family map, issue/chat history, raw PR #157, historical learner PDFs or mature-reference screenshots.

## Runtime sequence

```text
C-A exact intake
→ C-B source-integrity / item-validity review
→ cold-start semantic derivation from raw source/question/corpus evidence
→ C-C scope reconciliation
→ C-D problem-family / reasoning semantics
→ C-E optional learner-evidence inference
→ C-F LearnerStudyScope / LearnerStudyModel
→ C-G Core1 authoring + Appendix A/B/C
→ C-H semantic Chemistry representations
→ C-I Core2 transfer
→ C-J source/corpus closure + evidence/longitudinal semantics
→ two-product semantic candidate package
→ cold-start report + authority trace
```

The semantic-derivation step is governed by `ColdStart/registry/chemistry-cold-start-derivation-policy.json`; it derives source obligations, assessment bindings and external-corpus classifications from raw normalized records and canonical Chemistry authority. The frozen C-C pilot registries may be used for tests/comparative validation, but they are not runtime inputs to the cold-start producer.

## Run A / Run B

Run A has no `AttemptSet`. Learner state stays unknown unless authorized evidence exists; no weakness may be invented.

Run B uses the same source, question/corpus and declared scope plus the repository-safe de-identified attempt fixture. Canonical source/scope/external classification, problem-family truth and primary external ownership must remain identical. Only learner-conditioned state, treatment and support may differ where authorized evidence warrants it.

## Product topology

C-K emits exactly two deterministic semantic learner candidates with frozen semantic identities:

1. `Core Study Guide` — main teaching + Appendix A Core Practice + Appendix B Core Solutions + Appendix C Printable Handout.
2. `ExamSIDE Solution & Transfer Book` — H0 attempt first, badges, PRIMARY/SUPPORTS, Core1/source links, H1/H2/H3, ChemistryReasoningRoute and complete solution/verification.

C-K does not claim rendered-PDF visual quality. Byte-level PDF rendering and authorized subject/pedagogy/assessment/visual release remain C-L.

## Authority trace

Every major learner-facing decision must carry non-empty repository authority references and an explanation. `agent decided` is not a valid authority. The required decision classes are inclusion, external eligibility, treatment depth, representation choice, condition/exception treatment, worked example, Appendix A, Appendix C, Core2 placement, PRIMARY/SUPPORTS, badge, hints, reasoning route, verification and longitudinal revisit.
