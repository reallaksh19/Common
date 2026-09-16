# Testing blueprint

Every validation item declares obligation `MUST_PASS | SHOULD_RUN | INFORMATIONAL` and result `PASS | FAIL | NOT_RUN | NA`.

Map each required AC to verification; prefer deterministic tests/oracles for authoritative behavior; include negative/falsifier cases for permissive paths; use independent benchmarks when production could self-confirm; record exact command/environment/evidence; preserve truthful NOT_RUN with reason; never convert optional NOT_RUN into a hard stop. A MUST_PASS failure prevents claiming its mapped AC complete.