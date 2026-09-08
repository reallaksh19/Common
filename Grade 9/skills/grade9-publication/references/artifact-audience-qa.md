# Artifact Audience QA

Use this checkpoint set when Student Core, Self-Check, and Audit are emitted as separate artifacts.

## AD-40 SELF-CHECK AUDIENCE PURITY

The Self-Check PDF is a learner artifact. It may contain retrieval questions, revision prompts, reflection, confidence checks, and source-authored learner self-check statements. It must not contain publisher-process status such as:

- typography/render QA;
- source mapping or provenance counters;
- reconstruction/audit status;
- `PASS/PENDING` production checklists;
- source-focus metadata whose purpose is publisher traceability rather than learning.

If the source itself contains a publication-style completion checklist, preserve it in the Audit PDF and record the routing in the source-to-publication map. Do not delete it, but do not expose it as a learner self-check.

Fail if Self-Check asks the learner to interpret production language or if publisher QA appears as student progress.

## AD-41 SOURCE-STATUS vs PUBLICATION-STATUS SEPARATION

When the source says a production item is `PENDING`, `PASS`, `NEXT`, or similar, preserve that source status as source data in Audit. Track the reconstructed publication's own QA status separately.

Never silently overwrite `PENDING in source` with `PASS` merely because the new publication passed QA. The audit should make both states visible when materially relevant:

- source status: what the input PDF recorded;
- publication status: what the reconstructed batch actually achieved.

This prevents reconstruction QA from mutating source content.

## Release check

Before release:

1. scan Student Core and Self-Check for production terms;
2. route any publisher checklist/status to Audit;
3. verify source checklist items remain mapped;
4. record `student_audience_purity_findings = 0` and `self_check_audience_purity_findings = 0`.
