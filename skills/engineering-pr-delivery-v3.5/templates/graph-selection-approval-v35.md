# V3.5 R2-C — Source-approved immutable graph selection

**NOT AN APPROVAL.** This is an issuance template for the Owner/Coordinator to use only after approving a real production graph/selection. A ChatGPT coding agent must not publish this template as if it were an Owner grant. No source approval for #600/#604/#712 has been established.

## Two independently governed issuances

1. **Graph selection:** a GitHub issue comment authored by the repository **OWNER**, scoped to the programme's governing issue, with exactly one `V35_GRAPH_SELECTION_APPROVAL_V1` block. It identifies an immutable **40-character Git commit SHA** and exact repository JSON file path, its raw UTF-8 SHA256, canonical DELP validated graph digest, graph generation, root, selected leaf, candidate PR, spec generation and the full Owner-origin mirror envelope. The code fetches and validates the content independently; never let the executor supply its own graph+matching digest.
2. **Scoreboard write permission:** separate existing `V35_SCOREBOARD_APPROVAL_V1` comment, scoped to **only** issue and PR managed titles/bodies, authored by a principal allowed in the approved graph's `programme.scoreboard_approvers`. This is not custody, Local merge authority, reviewer acceptance, or source proof.

The selected graph must be tracked in the repo at a stable **commit**, not `main` or a branch. The Owner mirror is also re-fetched from the native provider; its original chat URL remains `UNRESOLVED_CHAT_LINK` if unavailable.

### Example shape — PLACEHOLDERS, NOT VALID PROVIDER APPROVAL

```text
<!-- V35_GRAPH_SELECTION_APPROVAL_V1_BEGIN -->
```
```json
{
  "schema": "V35_GRAPH_SELECTION_APPROVAL_V1",
  "scope": "READ_MODEL_AND_ISSUE_PR_SCOREBOARD_ONLY",
  "repository": "<approved-owner/repo>",
  "root": "<Repository#root-issue>",
  "responsibility_ref": "<Repository#leaf-issue>",
  "pr_number": 0,
  "approval_issue": 0,
  "revoked": false,
  "native_custody_granted": false,
  "local_merge_authorized": false,
  "original_chat_authenticated": false,
  "graph_commit_sha": "<40-char immutable commit SHA>",
  "graph_path": "<exact repository path ending in .json>",
  "graph_file_sha256": "<sha256 of exact source file bytes>",
  "graph_digest": "<DELP.validate_graph(graph).digest>",
  "graph_generation": 0,
  "spec_generation": 0,
  "owner_claim_issue": 0,
  "owner_origin": {
    "verbatim": "<full unchanged original quotation>",
    "claim_origin": "https://github.com/<approved-owner/repo>/issues/<claim-issue>",
    "first_durable_mirror": "https://github.com/<approved-owner/repo>/issues/<claim-issue>#issuecomment-<id>",
    "original_source_status": "UNRESOLVED_CHAT_LINK",
    "original_source_ref": null
  }
}
```
```text
<!-- V35_GRAPH_SELECTION_APPROVAL_V1_END -->
```

The plain-text examples above are **not** executable permission. Real values must be independently reviewed for exact source graph, claim ownership, actual approval epoch and currentness. A valid typed comment is an authority record only for this **scoreboard source selection scope**, never a Local stage/merge/custody grant.

## Publisher invocation after the actual two approvals

- Inactive entrypoint: `scripts/integration_scoreboard_publish_v35.py`
- Read-only dry run: `--graph /path/to/local.json` with no `--apply`.
- Guarded live apply: `--graph-source-ref <real-GitHub-approved-comment-URL> --approval-ref <real-GitHub-scoreboard-comment-URL> --repository <repo> --responsibility <leaf> --pr <number> --apply`.
- The `--graph` value, if additionally supplied during apply, is **only** a redundant consistency check against immutable fetched content; it cannot create permission.
- Workflow template is `examples/integration/v35-scoreboard-workflow.template.yml`. **Do not install** without live approver/source, current exact-head tests, a trusted default-branch runner and explicit Owner/Local release. GitHub has no atomic CAS across issue status comments and PR title/body.
