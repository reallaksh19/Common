# Parent / Program Engineering Issue Template

Use for `ISSUE_TOPOLOGY: PROGRAM_ISSUE_SET`.

```markdown
ISSUE_ROLE: PROGRAM_ROOT
PROGRAM_ID: PGM-<repo>-<short-task>
PROGRAM_WORK_ITEM_KEY: SELF_AFTER_CREATION
PROGRAM_BASIS_REVISION: PB-0001
COMMON_INPUT_SET_ID: <PROGRAM_ID>-INPUTS-v1
COMMON_BENCHMARK_SET_ID: <PROGRAM_ID>-BENCH-v1
COMMON_VALIDATION_SET_ID: <PROGRAM_ID>-VALID-v1
COMMON_ROADMAP_SET_ID: <PROGRAM_ID>-ROADMAP-v1

# Mission
<Original Owner intent, preserved without implementation-agent reinterpretation.>

# 0. Ground truth at program creation
Observed main: `<40-hex>`
Re-ground before every child activation.

# 1. Owner intent / original task ledger
| ID | Original requirement | Status | Owner source |
|---|---|---|---|
| TASK-001 | ... | OPEN | ... |

# 2. Owner Roadmap / authority ledger
| ID | Roadmap/source | Bound revision | Role | Status | Mutation authority |
|---|---|---|---|---|---|
| RM-001 | ... | ... | PRIMARY | ALIGNED | OWNER_ONLY |

# 3. Common input set
| ID | Source | Authority | Required data | Status | Drift / invalidation |
|---|---|---|---|---|---|
| INPUT-001 | ... | PRODUCTION_INPUT | ... | AVAILABLE | ... |

# 4. Common benchmark / oracle set
| ID | Type | Source | Inputs | Expected quantity | Tolerance | Independent? | Status |
|---|---|---|---|---|---|---|---|
| BM-001 | FROZEN_ANALYTICAL | ... | ... | ... | ... | YES | READY |

# 5. Common validation set
| ID | Gate / command / evidence | Required result | Applies to | Status |
|---|---|---|---|---|
| VAL-001 | ... | PASS | WP-001,WP-003 | NOT_RUN |

# 6. Global protected domains / exclusions
- NO ...

# 7. Program Definition of Done
The program is complete only when every required TASK row is satisfied/Owner-disposed, all required work packages/revisions are complete, common sets remain current, integration gates pass, and NOT_RUN/FAIL are not promoted.

# 8. Work-package partition / dependency registry
| WP | Relation | Child issue | Scope / deliverable | Owned authority/paths | Depends on | Parent rows used | Status | Chain / PR | Overlap |
|---|---|---|---|---|---|---|---|---|---|
| WP-001 | IMPLEMENTATION | PENDING | ... | ... | NONE | TASK-001; INPUT-001; BM-001; VAL-001 | PLANNED | PENDING | SAFE_DISJOINT |

# 9. Overlap rules
Before a child is activated, compare PARTITION_KEY, authority domains, expected changed paths and active sibling PRs. `BLOCKED_ACTIVE_SIBLING` or `UNKNOWN` => no material write authority.

# 10. Integration / closure gates
- ...

# 11. Relay contract
Every material child gets its own GitHub issue, WORK_ITEM_KEY, canonical engineering-pr-delivery-v2 chain and exclusive current agent instance. Parent issue is program/common-custody authority, not a shared multi-writer production chain.

# 12. Current program-status projection
Maintain operational child status in a mutable program-status comment/repository program-state artifact. Do not rewrite the original Owner contract on each agent turn.
```
