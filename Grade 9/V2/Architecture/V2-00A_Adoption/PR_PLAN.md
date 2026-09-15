# V2-00A Pull Request Plan

Issue: #178

## Proposed PR

Title: `V2-00A: add authority-safe adoption ledger and migration falsifiers`

Branch: `v2/00a-adoption-ledger-20260911`

Base: `main`

## Scope

The PR establishes migration governance only. It must not migrate subject content or produce learner-facing artifacts.

## Planned commits

1. **Constitution** — add V2-00A folder, authority classes, source disposition and benchmark firewall.
2. **Contract** — add JSON Schema plus seeded adoption ledger for PR #160/#161/#166/#167/#168 and selective references.
3. **Falsifiers** — add dependency-free validator and positive/negative fixtures.
4. **CI** — run the seeded ledger and regression fixtures on every relevant change.

The implementation may be delivered as fewer physical commits, but review should evaluate these four concerns separately.

## Required review questions

1. Does each old artifact family have exactly one declared source authority class and V2 owner?
2. Is `COPY` reserved for demonstrated semantic equivalence?
3. Are PR #161 publication mechanisms prevented from owning StudyModel decisions?
4. Are PR #166–#168 learner semantics prevented from mutating Core1 truth?
5. Are #168 synthetic fixtures impossible to interpret as production learner evidence?
6. Are #162/#163/#164 treated as selective references rather than a Grade-9 ontology source?
7. Is #165 benchmark-derived RCA kept out of producer truth?
8. Can PR #156/#157 enter only final-validation/RCA paths after a candidate exists?
9. Does every adopted item require new V2 validation instead of inheriting historical PASS state?
10. Can V2-01/V2-02 consume the ledger without importing an old branch?

## Acceptance commands

```bash
python "Grade 9/V2/Architecture/V2-00A_Adoption/validate_adoption_ledger.py" \
  "Grade 9/V2/Architecture/V2-00A_Adoption/adoption_ledger.json"
python -m unittest \
  "Grade 9/V2/Architecture/V2-00A_Adoption/test_validate_adoption_ledger.py"
```

## Explicitly deferred

- subject canonical migration;
- learner evidence migration;
- Study Synthesis implementation;
- longitudinal/adaptive scheduling;
- shared psychological/root-cause traits;
- learner PDFs;
- benchmark comparison;
- PR #156/#157 structural imitation.

## Follow-on PR boundaries

- **V2-01**: Core1 canonical authority and `CanonicalKnowledgeSet`, using only ledger-approved source mechanisms.
- **V2-02**: Learner Intelligence evidence/state, using only ledger-approved learner mechanisms and fixtures.
- **V2-03+**: goal/scope, Study Synthesis, Learning Design and publication according to #175 ownership.

Any future change that wants to reuse another old artifact must first extend the ledger and pass the same authority/falsifier review.
