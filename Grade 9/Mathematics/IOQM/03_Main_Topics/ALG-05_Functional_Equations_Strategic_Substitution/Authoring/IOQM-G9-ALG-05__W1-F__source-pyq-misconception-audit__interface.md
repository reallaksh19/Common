---
main_topic_id: IOQM-G9-ALG-05
microstream_id: W1-F
microstream_title: Source, PYQ, and misconception audit
owner_role: RESEARCH_INTERFACE_ONLY
status: READY_FOR_LEAD
canonical_teaching_owner: IOQM-G9-ALG-05
prerequisite_interfaces: [ALG01_Stable_Prerequisite_Interface_v1@fc685ff0a2e9bd67fbd6a920e730b7fff633404b]
source_cutoff: 2026-09-02
---

# A. Scope boundary
Own: custody of the two validated IOQM anchors, mechanism fingerprints, answer verification, source-to-teaching traceability, and topic-wide misconception checks. Exclude rewriting official stems as invented variants, unsupported historical claims, and any expansion into abstract function theory.

# B. Learner-state model
`PRIOR_KNOWLEDGE:` substitution and elementary equation solving.  
`LIKELY_HALF_KNOWLEDGE:` remembers isolated tricks or sample values without knowing why they work.  
`MISSING_BRIDGES:` source-faithful mechanism recognition, domain legality, proof completeness, and distinction between historical evidence and authored transfer.  
`OWNERSHIP_TARGET:` recognize a strategic mechanism while keeping proof obligations and source status explicit.

# C. Mathematical invariant / governing structure
`SOURCE ID -> DOMAIN -> MECHANISM -> FIRST MOVE -> COMPLETE DERIVATION -> ORIGINAL-CONTEXT CHECK`.  
A source anchor licenses a mechanism only at the depth actually justified by the problem and its verified solution.

# D. Representation inventory
| Representation | Exposes | First move | Condition | Wrong choice |
|---|---|---|---|---|
| stable source ID | custody | resolve exact year/question | verified ledger | paraphrase as if verbatim |
| official stem | domain/mechanism | preserve source meaning | no silent alteration | normalize away constraints |
| mechanism fingerprint | transferable structure | identify collapse/pair/combine | independent derivation | memorize surface syntax |
| authored transfer | changed surface | re-prove from stated domain | answer independently checked | cite PYQ as proof of variant |

# E. Decision boundaries
| Surface | A | B | Question | Trap |
|---|---|---|---|---|
| source/variant | historical item | authored transfer | is this exact wording source-controlled? | blurred provenance |
| answer/mechanism | key value | mathematical derivation | can the result be independently reproduced? | key-only trust |
| pattern/proof | observed values | all-input argument | what closes the proof for the whole domain? | finite-value guessing |
| FE/recurrence | original all-input relation | derived step relation | does the derived relation imply the original statement? | one-way proof leak |

# F. Misconception/diagnosis catalogue
```text
ERROR_CODE: SOURCE_VARIANT_BLUR
WRONG_MOVE: presents an authored transfer item as though it were the historical PYQ.
WHY_TEMPTING: the mechanism is intentionally similar.
MISSING_LINK_CLASS: SOURCE_CUSTODY
REPAIR_INVARIANT: attach stable ID only to the verified historical anchor; label transfer by mechanism, not provenance.
FALSIFIER_OR_CONTRAST: changed constants or domains make the item authored even when the first move is identical.
```
```text
ERROR_CODE: KEY_WITHOUT_PROOF
WRONG_MOVE: accepts an official answer without independently checking the mathematics.
WHY_TEMPTING: official keys are authoritative for the final answer.
MISSING_LINK_CLASS: VERIFICATION
REPAIR_INVARIANT: reconstruct the solution from the source relation and domain, then compare with the key.
FALSIFIER_OR_CONTRAST: a correct key does not certify an unrelated derivation.
```
```text
ERROR_CODE: RECURRENCE_PROOF_LEAK
WRONG_MOVE: derives a recurrence-like consequence and treats it as sufficient proof of the original functional equation.
WHY_TEMPTING: the recurrence may determine many values.
MISSING_LINK_CLASS: PROOF_COMPLETENESS
REPAIR_INVARIANT: verify any proposed global formula in the original all-input equation.
FALSIFIER_OR_CONTRAST: a consequence need not be equivalent to the original relation.
```

# G. First-move cues
- Resolve the stable source ID and domain before interpreting the algebra.
- Recompute the answer independently before promoting the mechanism.
- Separate exact historical anchors from authored transfer items.
- If a formula was guessed from values, verify it for every allowed input in the original equation.

# H. H3 -> H0 fading plan
H3 source mechanism and first move supplied -> H2 mechanism named -> H1 source/domain cue only -> H0 changed-surface item with no historical label or hint.

# I. Validated IOQM source anchors
| ID | Year/Q | Status | Role | Mechanism | Figure | Verified key |
|---|---|---|---|---|---|---|
| IOQM-2025-Q14 | 2025 Q14 | CLEAN_OFFICIAL | primary | integer-domain zero collapse | no | 12 / FINAL_OFFICIAL |
| IOQM-2024-Q16 | 2024 Q16 | CLEAN_OFFICIAL | primary | involution partner + elimination | no | 08 / OFFICIAL_HBCSE_KEY |

Source custody retained in `01_Source_Coverage_Map.md`; no metadata-correction overlay affects either anchor.

# J. Source-independent mathematical trace
`IOQM-2025-Q14:` domain `Z`. From the source relation, `m=0` forces `f(1)=2`; then `n=0` forces `f(m)=m+1` for every integer `m`. Hence `f(1)+...+f(N)=N(N+3)/2`; `N=12` gives 90 and `N=13` gives 104, so the verified answer is 12.

`IOQM-2024-Q16:` domain `R`. Write the source equation at `x` and `3-x`: `3f(x)+4f(3-x)=x^2` and `4f(x)+3f(3-x)=(3-x)^2`. Elimination gives `7f(x)=x^2-24x+36`; therefore `f(27)-f(25)=8`, matching key `08`.

# K. Contrast-pair candidates
Historical source/authored transfer; official key/independent derivation; arbitrary/strategic substitution; functional equation/derived recurrence; finite-value guess/global proof; integer/real domain.

# L. Transfer candidates
Changed product-collapse constants; changed reflection center; underdetermined shift on `R`; integer propagation with negative inputs; candidate-formula verification; equation where injectivity is tempting but unnecessary.

# M. Candidate mastery items
Identify provenance; choose first move from mechanism; explain why a key alone is insufficient; reject a finite-value formula guess; distinguish consequence from equivalent reformulation; verify an authored transfer answer independently.

# N. Dependency declarations
`BRIDGE_REQUIRES` ALG-01 strategic substitution/equivalence discipline. `REQUIRES` frozen IOQM source ledger and exact stable IDs. `APPLIES` source custody, domain checking, independent solution verification, misconception auditing. No dependency inversion detected.

# O. Lead integration notes
Use the two PYQs as evidence for strategic input choice, not as a license to expose source-control machinery to learners. Keep stable IDs, provenance status, answer-ledger terms, microstream names, and production controls in authoring/teacher custody only. First mastery attempt remains unlabelled and unhinted.

# P. Independent QA status
`DERIVATIONS_CHECKED: PASS`  
`PROMOTED_NUMERICAL_ANSWERS_CHECKED: PASS`  
`SOURCE_IDS_VERIFIED: PASS`  
`SOURCE_TO_TRANSFER_BOUNDARY: PASS`  
`DOMAIN_AND_PROOF_COMPLETENESS: PASS`  
`DEPENDENCY_CONFLICTS: NONE`  
`OPEN_ISSUES: NONE_AFFECTING_INTEGRATION`  
`CLASSROOM_RETENTION_PSYCHOMETRIC_CALIBRATION_PUBLICATION: NOT_RUN`
