# Adversarial protocol examples

These are protocol-level negative controls. The executable equivalents live in `tests/test_protocol.py` and `tests/test_pipeline.py`.

| Mutation / drift | Required outcome |
|---|---|
| Reviewer/Super Reviewer leaves internal fixable defect for earlier role | reject advancing outcome |
| reverse `repeat_stages` routing | reject record |
| Reviewer/Super Reviewer weakens protected harness/baseline/oracle/fixture set | reject acceptance basis |
| same principal is authorized for Coder and Reviewer | reject role basis |
| unverified/forged Owner command | reject command basis |
| required evidence points to wrong candidate | reject evidence |
| independent evidence points to wrong lease | reject evidence |
| evidence fixture set differs from protected surface | reject evidence |
| context event updated after snapshot time | reject snapshot |
| parent frontier lacks matching provider event | reject snapshot |
| PR head changes after review | REWORK / lease stale |
| target branch head changes after integration review | REWORK / lease stale |
| stacked predecessor head changes | lease stale |
| project protocol/harness digest changes | lease stale |
| environment digest changes | reject current evidence |
| required CI is on wrong SHA | no merge readiness |
| provider/workflow/app identity differs from policy | no merge readiness |
| mandatory CI step skipped | NOT_RUN, never PASS |
| required NOT_RUN without Owner waiver | no approval |
| required NOT_RUN with exact active waiver | STAGE_COMPLETE_WITH_WAIVER; result stays NOT_RUN |
| required FAIL or INCONCLUSIVE with waiver | no approval |
| waiver copied to another SHA/lease | reject waiver |
| waiver expires before merge | WAITING_OWNER; merge under expired waiver is invalid |
| canonical target observation names wrong reviewed head/merge | reject delivery |
| exact canonical relation target SHA differs from merge commit | reject delivery |
| descendant relation lacks provider ancestry proof | reject delivery |
| project escaped-defect regression names unknown criterion/harness | reject project protocol |
| criterion claims PASS while cited method evidence is FAIL/INCONCLUSIVE | reject contradictory verdict |
| required verification method has no evidence | reject acceptance |
| evidence names wrong project harness | reject evidence |
| CI trigger head is correct but tested integration tree is wrong | no merge readiness |
| PR-head policy is satisfied with synthetic-merge checkout | reject CI identity |
| CI_PROVIDER / EXTERNAL_ORACLE is impersonated by stage executor | reject provenance |
| Reviewer/Super Reviewer repairs before discovery freeze | reject stage completion |
| role-required discovery method omitted before repair | reject stage completion |
| material scope/acceptance-surface defect self-classified as bounded product fix | reject repair authority |
| independent class uses non-independent oracle basis | reject evidence |
| imported harness helper changes while manifest digest stays stale | reject acceptance surface |
| legacy stage status PASS used as lifecycle completion | reject schema |

