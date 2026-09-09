# Human review guide

Use the draft PR as the shared discussion. Comment inline on concept Markdown, schema or example JSON. For a PDF finding, comment in the PR conversation with filename, PDF page, question/lesson ID and a screenshot if useful. Page numbers include the opening teaching page.

## Suggested independent reviewers

These are proposed roles, not assigned people or completed approvals. Seek at least two independent teaching/subject judgements.

| Role | First reading | Decision to record |
|---|---|---|
| Physics teacher | Concept map, both teaching sections and quantitative solutions | Are models, signs, units, graph meanings and limits correct? |
| Teacher supporting a struggling learner | B30 pp1–9, handout p14, guided feedback p17 | Can the learner explain the picture and complete a faded step? Identify the first unsupported word or operation. |
| Teacher of stronger learners | B80 pp1–5, A7/A8 and solutions | Is depiction sufficient? Does challenge require model choice and transfer? |
| Assessment reviewer | Appendix A → hints → solutions | Are questions attemptable, hints progressive, answers withheld and repairs complete? |
| Publication reviewer | PDFs at normal size; printed handouts | Do placement, labels, whitespace and wording support explanation? Are navigation and grayscale distinctions usable? |
| Schema/tooling reviewer | Skills, JSON, validator, renderer and auditor | Does the executable contract prevent the stated failures and reproduce the supplied structure? |
| Cold-start reproducibility reviewer | Task brief, source authority and this repository only — no prior chat or unpublished context | Starting fresh, can the canonical skills be identified, the same source denominator frozen, artifacts routed correctly, the build reproduced, and the same audit/release evidence produced? If another agent cannot continue from the repository alone without reading chat history, the handoff is incomplete (this is IOQM's own final rule — reuse it here rather than a separate test). |

## Page-indexed route

| Target | B30 PDF pages | B80 PDF pages | Comment surface |
|---|---|---|---|
| Teaching and depiction | 1–9; especially guided tasks on 2 and 8 | 1–5 | Model `lessons` |
| Appendix A | 10–13, A1–A8 | 6–9, A1–A8 | Model `questions` |
| Printable Appendix B | 14 | 10 | Model `handout`; PDF screenshot |
| Optional H1/H2/H3 | 15–16 | 11–12 | Question `hints` |
| End solutions | 17 guided feedback; 18–21 A1–A8 | 13–16 A1–A8 | `guided_solutions` or question solution fields |
| Reference benchmark | Reference pp2, 9, 18–20, 23, 34 | Same reference | Adaptation table in `Physics_Rebuild_Review.md` |

Models live in `../../../skills/grade9-physics-publication/examples/`. The reference PDF covers different later Motion ideas: compare teaching/layout, not a common question denominator. Use `*.layout.json` for ID-to-page destinations. Shared A1, A2, A3 and A6 enable comparison but are not a validated diagnostic test.

## Passes and evidence

1. Read Core teaching independently before the previous review's conclusions. Record a successful explanation and a learning obstacle with locations.
2. Work questions without hints; then inspect H1/H2/H3 separately. Check ambiguity, missing representations and correctness.
3. Follow repair/return links, inspect Appendix B alone, and check necessary graphs/data recur in solutions.
4. Compare the old drafts and reference PDF. State what improved and what still needs revision.
5. Recheck repairs at the new commit and give a scoped decision. Technical checks are not educational approval.

```text
Role:
Commit reviewed:
Artifact / PDF page / lesson or question ID:
Severity: blocker | major | minor
Observation:
Likely learner consequence:
Suggested revision:
Recheck needed:
Decision: needs revision | acceptable for this pilot | unable to assess
```

Use one finding per thread. Reply with fixing commit/page; close after recheck. Keep unresolved major teaching/correctness findings visible. Actual learner trials should be recorded separately without personal data in this public repository.

## Approval checklist

- [ ] Physics accuracy independently checked, including negative coordinates and zero crossings.
- [ ] B30 picture → meaning → relation → faded step → independent attempt is workable.
- [ ] B80 retains meaningful depictions and tests transfer.
- [ ] Appendices, hints and end solutions are complete.
- [ ] Reference comparison and retained/rejected rules reviewed.
- [ ] Sources, original-item labels, badges and scope claims checked.
- [ ] Human layout/print review complete.
- [ ] Schema/tooling review complete with technical evidence.
- [ ] Cold-start reproducibility check complete: a fresh agent, given only the brief/source/repository, can find the canonical skills and reproduce the build and audit evidence.
- [ ] Blocking findings repaired and rechecked.
- [ ] Owner approves this Physics pilot before expansion.

Keep the PR draft for early comments. For formal approval, mark it ready and request selected reviewers. See GitHub's [draft behavior](https://docs.github.com/en/pull-requests/reference/pull-requests) and [review requests](https://docs.github.com/en/pull-requests/how-tos/create-pull-requests/requesting-a-pull-request-review). Use a separate linked issue for a broader Physics → Mathematics → Chemistry roadmap or a deferred task spanning PRs; keep page-level discussion here. No reviewers are assigned by this package.
