# Chemistry V2 C-I — Core2 External Transfer

C-I defines the semantic contract for the second Chemistry learner-facing product: the ExamSIDE/external Solution & Transfer Book.

## Authority chain

The full external candidate denominator remains owned by C-A/C-C. C-I consumes only candidates already classified `ELIGIBLE_IN_SCOPE`; it does not infer eligibility from provider topic labels or source titles. Each eligible candidate receives exactly one transfer page and one PRIMARY concept owner.

The repository acceptance corpus stores index metadata but not full attemptable external bodies. For this architecture fixture only, `fixtures/chemistry-external-transfer-source.fixture.json` supplies explicit synthetic source-body authority. Every body is bound to the exact C-A candidate digest and has its own deterministic body digest. This is a test authority, not a claim that index metadata alone is sufficient and not a production substitute for source-body custody.

## Transfer page contract

Every placed page contains:

- H0 independent attempt before support;
- exact synthetic source stem/options/subparts and required figure/condition semantics;
- SOURCE/YEAR/SESSION/SHIFT badges;
- guide-assigned reasoning-demand badge, explicitly non-psychometric;
- `CANONICAL_TRANSFER` badge;
- one PRIMARY concept/capability and separate SUPPORTS concepts/capabilities;
- learner-readable Core1 links, not opaque IDs alone;
- problem-family-shaped workspace;
- progressive H1 NOTICE, H2 RULE/MODEL/REPRESENTATION and H3 START;
- ChemistryReasoningRoute kept distinct from the hints;
- C-H teaching/source representation specs;
- complete reasoning-first solution and verification route;
- exact source link and fidelity digests.

Original external candidates remain excluded from Core1 worked examples and Appendix A items.

## Validation

`contracts/validate_contracts.py` validates the six required C-I contracts plus badge/concept/profile authority.

`tests/test_chemistry_core2_transfer.py` runs all 15 issue #271 falsifiers, proves placement of all five eligible synthetic candidates while preserving the six-candidate denominator, and proves deterministic replay.

C-I does not claim final corpus closure, longitudinal evidence update, cold-start orchestration, PDF usability or authorized human assessment/product approval.
