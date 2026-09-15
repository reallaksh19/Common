# Independent arithmetic/model recomputation — EXECUTED SELF_CHECK

`qa/recompute.py` recomputed values directly from givens rather than reading the authored solution strings. **46 checks executed; 0 failed; status PASS.** This is a computationally separate path inside the same author execution, **not an independent human/agent reviewer**.

Checked source results include Q01 path/resultant averages; Q02 segment velocities/distance/average velocity; Q03 endpoint/displacement/distance; Q04–Q06 relative velocities and meetings/separation; Q07 and Q08 same-time tests; Q08 closest approach by completed-square result; Q09 river components/time/drift/path; Q10 rain relative vector; Q11 conversion/relative separation; and Q12 underdetermination.

Generated positive/negative controls recomputed include `2A-Q07`, `2A-Q08`, `2A-Q12`, `2B-Q07`, `2B-Q12` and extension `EXT-Q-001`. Limiting/model checks in `equation-register.json` separately cover zero displacement, observer reversal, equal-velocity separation and frame/unit consistency.
