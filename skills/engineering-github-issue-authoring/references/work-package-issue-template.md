# Work-Package / Revision Engineering Issue Template

Use one child issue per bounded implementation partition. Use `REVISION` only for a material revision of completed/frozen predecessor work.

```markdown
ISSUE_ROLE: WORK_PACKAGE | REVISION
PROGRAM_ID: <PROGRAM_ID>
PARENT_WORK_ITEM_KEY: github:<owner>/<repo>#<parent>
WORK_PACKAGE_ID: WP-001
WORK_PACKAGE_RELATION: IMPLEMENTATION | VALIDATION | INTEGRATION | REVISION
PARTITION_KEY: <PROGRAM_ID>/WP-001
PREDECESSOR_WORK_ITEM_KEY: NONE | github:<owner>/<repo>#<predecessor>
REVISION_SEQUENCE: 0 | 1 | 2 ...

INHERITED_PROGRAM_BASIS_REVISION: PB-0001
INHERITED_INPUT_SET_ID: <exact parent ID>
INHERITED_BENCHMARK_SET_ID: <exact parent ID>
INHERITED_VALIDATION_SET_ID: <exact parent ID>
INHERITED_ROADMAP_SET_ID: <exact parent ID>
PARENT_TASK_ROWS: TASK-001,TASK-004
USES_INPUT_ROWS: INPUT-001,INPUT-003
USES_BENCHMARK_ROWS: BM-001
USES_VALIDATION_ROWS: VAL-002,VAL-004

# Mission
<One bounded child deliverable. Do not restate/reinterpret the entire parent program.>

# 0. Parent/common custody
Parent program: <link>
Parent basis: PB-0001
This child inherits the listed common sets exactly. If one is wrong/stale, stop and revise the parent basis rather than silently redefining it here.

# 1. Bounded scope / partition
OWNED_AUTHORITY_DOMAINS:
- ...
OWNED_PATHS_OR_COMPONENTS:
- ...
READ_DEPENDENCIES:
- ...
PROTECTED_SIBLING_DOMAINS:
- ...
DEPENDENCY_PREDECESSORS:
- ...

Overlap classification at creation: SAFE_DISJOINT | SAFE_SERIALIZED | COORDINATION_REQUIRED | BLOCKED_ACTIVE_SIBLING | UNKNOWN

# 2. Ground truth at child creation
Observed main: `<40-hex>`
Open sibling PR/WIP state: ...
Re-ground parent basis/common set IDs and live main before material mutation.

# 3. Definition of Done
- ...

# 4. Child-specific inputs / fixtures
Only add local rows that are not already parent common rows.

# 5. Current production/repository path
...

# 6. Technical implementation instructions
Include live paths/APIs and minimum-to-code skeleton.

# 7. Expected changed / protected files
...

# 8. PASS / FAIL / NOT_RUN criteria
...

# 9. Parent benchmark / validation obligations
For each inherited BM/VAL row used by this child, state how this child produces evidence without redefining expected values/tolerances.

# 10. Anti-drift / sibling-overlap gate
- parent basis/set ID drift => READ_ONLY until reconciled;
- active sibling overlapping PARTITION_KEY/write domain => BLOCKED;
- stale issue assumption => correct plan with evidence, do not implement stale assumption;
- NOT_RUN remains NOT_RUN.

# 11. Revision-only predecessor custody
For ISSUE_ROLE: REVISION, state:
- PREDECESSOR_ACCEPTED_ENDPOINT;
- PREDECESSOR_PR;
- exact defect/revision reason;
- evidence retained from predecessor;
- evidence superseded by this revision;
- rollback/NO-PATCH case.

# 12. Relay contract
WORK_ITEM_SOURCE: GITHUB_ISSUE
WORK_ITEM_KEY: github:<owner>/<repo>#<this-child>
WORK_ITEM_MODE: EXCLUSIVE
PROGRAM_WORK_ITEM_KEY: <parent>
WORK_PACKAGE_ID: WP-001
PARTITION_KEY: <...>

Takeover of this unfinished child stays on this issue and relay chain. Do not create a new child solely because the agent changed.

# Appendix A — implementation qualification
<Exactly five live-repository implementation questions, with real hand/exact reconstruction according to the skill.>
```
