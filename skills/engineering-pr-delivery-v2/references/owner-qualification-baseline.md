# Owner Qualification Baseline — no-downgrade contract

## Purpose

Owner-authored expert questions in an issue, roadmap, current instruction or accepted handover are a qualification floor. They are not disposable seed prompts.

For every new question set, first classify:

```text
OWNER_QUALIFICATION_BASELINE_DISCOVERY: COMPLETE
OWNER_QUALIFICATION_BASELINE_SOURCE: NONE | <owner source locator>
OWNER_QUALIFICATION_BASELINE_MANIFEST: NONE | <repo-relative JSON path>
OWNER_QUALIFICATION_BASELINE_STATUS: NOT_APPLICABLE | SATISFIED | BLOCKED
```

If an Owner source contains qualification questions or explicit technical challenges, `SOURCE: NONE` is invalid.

## Manifest schema

Use a JSON file under the chain, for example:

```text
agents/chains/<CHAIN_ID>/qualification-baselines/<BASELINE_ID>.json
```

Canonical shape:

```json
{
  "version": 1,
  "baselineId": "QB-ISSUE-1535-A",
  "source": "github:reallaksh19/Advanced_Analysis#1535/Appendix-A",
  "sourceAuthority": "OWNER",
  "activeQuestionSetId": "QS-ADV-LAFEA3-1535-0011",
  "questions": [
    {
      "baselineQuestion": "Q1",
      "coveredBy": ["Q1", "Q2"],
      "requiredLiterals": ["N1=(0,0)", "N2=(40,0)", "N4=(22,2)"],
      "requiredConcepts": ["Jacobian", "det J", "centroid", "Hammer"],
      "requiredObligations": ["compute", "quantify", "negative"]
    }
  ]
}
```

`requiredLiterals` preserve supplied engineering payload. `requiredConcepts` preserve domain substance. `requiredObligations` preserve what the candidate must actually do.

## Coverage rules

For each baseline question:

1. every `coveredBy` active question must exist;
2. every required literal must appear in at least one covered active question after whitespace/case normalization;
3. every required concept must appear in at least one covered active question;
4. every required obligation stem must appear in at least one covered active question;
5. empty requirement arrays are allowed only if the Owner source genuinely contains none of that class;
6. deleting a numerical payload from the active prompt and leaving it only in a buried reference is not coverage;
7. a baseline question may map to multiple active questions, but the union must preserve the complete requirement set.

The validator does not decide whether the Owner's engineering question is correct. It preserves Owner-authored scope/difficulty until an Owner explicitly changes it.

## Source changes

If the Owner later replaces or modifies the baseline:

```text
old manifest remains immutable history
new baseline ID + source basis is created
active question set binds to the new baseline
```

Do not silently edit the old manifest to make a new pack appear compliant.

## Admission consequence

If an Owner baseline is required but coverage is incomplete:

```text
OWNER_QUALIFICATION_BASELINE_STATUS: BLOCKED
QUESTION_SET_ADMISSION_STATUS: INSUFFICIENT_TECHNICAL_DEPTH
WRITE_AUTHORITY: READ_ONLY on takeover
```

For the originating current custodian, a blocked baseline prevents beginning the next material batch because the crash qualification is not valid for that boundary.
