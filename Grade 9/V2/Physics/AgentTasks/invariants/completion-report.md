# Standardized Execution Report Contract

Every executing agent must return this exact report structure upon completing or blocking a task. The output consists of a human-readable Markdown section followed by a fenced JSON block complying with `execution-report.schema.json`.

---

## Markdown Report Template

```markdown
# Execution Report

## 1. Execution identity
Prompt ID: <PROMPT_ID>
Task instance: <TASK_INSTANCE_ID>
Repository: <REPOSITORY>
Branch: <TARGET_BRANCH>
Starting HEAD: <START_HEAD>
Ending HEAD: <END_HEAD>

## 2. Mission result
<COMPLETE | PARTIAL | BLOCKED>

## 3. Repository authority discovered
- Manifests: <list of manifests consulted>
- Schemas: <list of Draft 2020-12 schemas enforced>
- Policy: <applicable policy documents>
- Producers: <governing producer scripts/engines>
- Consumers: <downstream consumers/validators>
- CI: <applicable GitHub Actions workflows>

## 4. Changes made
For each changed file:
- Path: <relative path>
- Reason: <justification>
- Tier: <DATA_ONLY | SCHEMA | GENERIC_ENGINE | SUBJECT_ADAPTER | BLUEPRINT | TEST | DOC | SCHEMA_EXTENSION | SUBJECT_ADAPTER_CHANGE | GENERIC_ENGINE_CHANGE | BLUEPRINT_CHANGE>
- Authority impact: <description of custody/authority changes>

## 5. Derived state before
<Description or summary of system/data state prior to execution>

## 6. Derived state after
<Description or summary of system/data state following execution>

## 7. Tests/falsifiers
| Test Name / Command | Result (PASS/FAIL/SKIPPED/NOT_RUN) | Evidence / Exit Code |
|---------------------|------------------------------------|----------------------|
| <test_1>            | <result_1>                         | <evidence_1>         |

## 8. CI status
| Workflow | Run Trigger / ID | Result |
|----------|------------------|--------|
| <wf_1>   | <run_1>          | <res_1>|

## 9. Invariants checked
- Invariant A (Repository authority): <VERIFIED | BLOCKED>
- Invariant B (Current schemas): <VERIFIED | BLOCKED>
- Invariant C (Canonical over diagnostic): <VERIFIED | BLOCKED>
- Invariant D (Case facts in data): <VERIFIED | BLOCKED>
- Invariant E (No Blueprint case branches): <VERIFIED | BLOCKED>
- Invariant F (No inferred evidence): <VERIFIED | BLOCKED>
- Invariant G (Learner state invariant on truth): <VERIFIED | BLOCKED>
- Invariant H (Research depth invariant on base): <VERIFIED | BLOCKED>
- Invariant I (No fabricated cross-domain authority): <VERIFIED | BLOCKED>
- Invariant J (Publication authority separated): <VERIFIED | BLOCKED>
- Invariant K (Anti-mutation custody): <VERIFIED | BLOCKED>
- Invariant L (Justified workflows): <VERIFIED | BLOCKED>
- Invariant M (Fail-closed honest stop): <VERIFIED | BLOCKED>

## 10. Known limitations
- <Declared limitation 1>
- <Declared limitation 2>

## 11. Unresolved issues
- <Unresolved issue or blocker 1>

## 12. Architecture findings
- Reusable improvement discovered: <finding>
- Remaining case coupling: <coupling>
- Scalability concern: <concern>

## 13. No-memory declaration
State whether completion depended on any information not recoverable from repository or declared external sources:
`MEMORY_INDEPENDENCE_VERIFIED: TRUE` (or FALSE if contaminated).

## 14. Recommended next task
<Suggested immediate next task instance or follow-up prompt ID>
```

---

## Machine JSON Contract

Following the Markdown report, the agent must output a single JSON block conforming to `execution-report.schema.json`:

```json
{
  "prompt_id": "<PROMPT_ID>",
  "task_instance_id": "<TASK_INSTANCE_ID>",
  "start_head": "<START_HEAD>",
  "end_head": "<END_HEAD>",
  "result": "COMPLETE",
  "changed_files": [
    {
      "path": "<path>",
      "reason": "<reason>",
      "tier": "DATA_ONLY",
      "authority_impact": "<impact>"
    }
  ],
  "tests": [
    {
      "test": "<test_command>",
      "result": "PASS",
      "evidence": "<output_summary>"
    }
  ],
  "workflows": [
    {
      "workflow": "<workflow_name>",
      "run": "<run_id>",
      "result": "<status>"
    }
  ],
  "blockers": [],
  "limitations": [
    "<limitation_1>"
  ],
  "architecture_findings": [
    "<finding_1>"
  ],
  "memory_dependency_detected": false,
  "recommended_next_task": "<next_task_id>"
}
```
