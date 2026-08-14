# Integrity / Anti-Gaming Rules

Never make a gate pass by weakening the gate instead of correcting production behavior unless the gate itself is independently demonstrated to be wrong.

Without independent justification, do not:

- relax a numerical or engineering tolerance because a test fails;
- replace an independent expected value with current production output;
- change implementation and oracle together and call the result independently verified;
- delete, disable, skip, or de-scope a difficult benchmark solely to obtain green status;
- convert a failure into a warning merely to pass a gate;
- classify an unexecuted check as `PASS`;
- classify code/source inspection as runtime execution;
- classify a test-harness/precondition failure as product `PASS` or product `FAIL` without separating the failure layers;
- call docs/schema/validator-only work production completion;
- hard-code fixture, project, benchmark, or test IDs into production behavior to satisfy a case;
- replace an independent oracle with the implementation under test;
- silence or reclassify a credible defect solely to obtain closure;
- mock the production integration path and claim the production capability is complete.

When a test or acceptance criterion appears wrong, demonstrate why using a stronger independent authority, record a `DEC-*` or `ISS-*` item as appropriate, then change the gate transparently.
