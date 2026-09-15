# Executed-test ledger

All commands below were executed in the topic root during this run. `PASS` means that command's stated invariant passed; it does not imply independent subject approval or release.

| Test / command | Final result | Evidence / notes |
|---|---|---|
| `python qa/reconcile_inventory.py` | **PASS** | `qa/inventory-reconciliation.json`: reparsed corpus, 12 questions, Q02 table, source conventions, 159-atom denominator. Initial run exposed checker handling of unlabeled single-part Q07/Q12 and harmless convention wording normalization; checker repaired, source/inventory unchanged. |
| `python qa/check_source_fidelity.py` | **PASS** | `qa/source-fidelity-results.json`: Q01–Q12 exact immutable blocks, attribution/hints/answer anchors; Q12 underdetermination closure. Initial script had a boolean-unpack coding error; checker repaired, learner/source text unchanged. |
| `python qa/recompute.py` | **PASS** | `qa/arithmetic-results.json`: 46 independent-from-solution-string numerical/model checks, including generated positive controls and extension. |
| `python qa/run_similarity.py` | **PASS_REVIEW_ROUTING_COMPLETE** | `qa/similarity-results.json`: 0 lexical threshold flags, 0 short exact prose flags; four known structural revisits explicitly reviewed. No embedding model run. |
| `python qa/render_visuals.py` | **PASS** | `qa/visual-render-manifest.json`: 10/10 SVGs rasterized, nonblank, title/desc metadata. Initial metadata predicate looked only for literal `<title>`/`<desc>` and falsely failed tags with IDs; checker repaired. |
| Same-instance contact-sheet inspection | **SELF_REVIEW PASS** | `qa/visual-inspection.md`; `qa/visual-render/contact-sheet.png`. Functional arrows/labels/geometry present; no observed clipping. Not independent visual approval. |
| `python qa/validate_package.py` | **PASS** | `qa/package-validation.json`: final package/locator/register/asset/extension checks. Initial policy check incorrectly rejected explanatory phrases “no trigonometry”; it was narrowed to forbid actual trig functions (`sin/cos/tan/atan2`) in learner files, then passed. |
| Python bytecode compilation for QA scripts | **PASS** | Executed after final script edits; see final ledger note below. |
| JSON parse of repository JSON evidence | **PASS** | Executed after final artifact generation. |
| CSV parse of root/QA/change registers | **PASS** | Executed after final artifact generation. |

## Explicitly NOT_RUN

Fresh-agent cold restart; independent Physics review; independent pedagogy/assessment review; real learner trial; evaluator hidden mutations; owner approval; publication; merge. These statuses are preserved in `OWNER_BOARD.md` and packet handoffs.
