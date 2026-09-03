# Engineering GitHub Issue Template

Use this template as a starting structure. Replace every placeholder with live repository evidence or an explicit `UNRESOLVED` statement. Delete optional subsections only when genuinely inapplicable.

```markdown
# Mission

<One precise implementation mission. State what user/engineering path must become complete and auditable.>

This is an **ENGINEERING_CRITICAL** implementation issue when applicable. The implementing agent is expected to implement, validate, and preserve engineering/source authority—not merely review or redesign.

The target is not `<superficial UI/result symptom>`. The target is:

```text
<authoritative input>
  → <governed transformation>
  → <retained production artifact>
  → <calculation/processing boundary>
  → <accepted result>
  → <publication/output>
```

---

# 0. Ground truth at issue creation

Issue created against repository state observed on `<YYYY-MM-DD>`.

Observed default-branch head:

```text
<40-hex SHA>
```

Do **not** assume this SHA is still current when implementation begins. Re-ground first.

Applicable repository instructions:

```text
AGENTS.md
<applicable Common/local skill references>
```

Current production/repository facts:

```text
<fact 1 supported by current code>
<fact 2>
<current limitation or missing seam>
```

Open overlap/WIP state at creation:

```text
<PR/branch/claim or NONE>
```

---

# 1. Owner intent, authority and scope

## 1.1 Owner intent

<Restate the task without diluting it.>

## 1.2 Governing Owner Roadmap(s)

| Roadmap | Revision/blob | Role | Alignment | Mutation authority |
|---|---|---|---|---|
| `<path>` | `<sha/revision>` | PRIMARY / DEPENDENCY | ALIGNED / ... | OWNER_ONLY |

Issue assignment does **not** grant roadmap mutation authority.

## 1.3 Engineering/source authority

```text
<source authority>
<master/reference authority>
<solver/parser/orchestrator authority>
<result/publication authority>
```

## 1.4 Explicit scope

In scope:
- ...

Out of scope:
- ...

---

# 2. Definition of Done

The issue is complete only when all applicable states below are satisfied from a consistent current source/input basis.

## 2.1 `<STATE/PHASE A>`

1. ...
2. ...

Required invariant:

```text
<parent identity A>
  == <dependent parent B>
  == <execution parent C>
```

## 2.2 `<STATE/PHASE B>`

...

## 2.3 User-visible/output completion

The user-facing result must expose:

```text
<authoritative quantity/state>
<source/case/location custody>
<warning or qualification state>
```

Do not use rendered pixels/contours/log strings as engineering authority.

---

# 3. Required execution strategy

Implement in coherent PR-sized phases.

Recommended sequence:

```text
PR-A  <foundation / benchmark freeze>
PR-B  <primary production seam>
PR-C  <dependent route / UI / publication>
PR-D  <cross-route regression / anti-drift cleanup>
```

Adjust the number of phases to the task. Do not create artificial PRs when one coherent patch is safer.

Each PR:
- has one bounded authority domain;
- records PASS/FAIL/NOT_RUN truth;
- remains handover-ready under the live delivery protocol;
- requires Owner merge authorization unless explicitly granted otherwise.

---

# 4. Input/source inventory

## 4.1 Production inputs

| ID | Source / path | Authority class | Required data | Status | Invalidates / drift rule |
|---|---|---|---|---|---|
| INPUT-001 | `<path/url>` | PRODUCTION_INPUT | `<values/fields>` | AVAILABLE | `<dependent artifacts>` |
| INPUT-002 | `<path/url>` | OWNER_DATA / MASTER_DATA | ... | UNRESOLVED | ... |

Rules:
- Sample/mock fixtures are regression inputs, not production authority.
- Revision/UI hashes do not substitute for engineering semantic/source authority unless the registered contract says they do.
- Missing input authority is a blocker, not permission to invent defaults.

## 4.2 Regression/sample fixtures

```text
<fixture path/function>
<known sample identity/values>
```

State explicitly what the fixture **does not** prove.

---

# 5. Current production/repository path to preserve

Trace the live intended route with current names:

```text
<input/source>
→ <normalization/parse>
→ <authority/custody>
→ <derived artifact>
→ <preflight/authorization>
→ <calculation/processing>
→ <result acceptance>
→ <publication/presenter>
```

Actual anchors:

```text
<path:function>
<path:function>
<contract/type/schema>
```

Do not replace this path with a direct core call or duplicate store/controller/parser unless the issue explicitly authorizes architecture replacement.

---

# 6. Technical implementation instructions

## 6.1 First missing/wrong boundary

Current evidence indicates the first implementation boundary is:

```text
<exact boundary>
```

Evidence:
- `<file/function/state/test>`
- `<contradictory or missing behavior>`

Falsifier:

```text
<one observation that would prove this diagnosis wrong>
```

## 6.2 Minimum implementation skeleton

Structural guidance; adapt to the current public API. Do **not** create duplicate architecture merely to make this snippet compile.

```js
// Example language only; use the repository's actual language.
const source = <load-current-production-input>();
const normalized = <existing-normalize-api>(source);
const authority = <existing-authority-api>(normalized, {
  origin: '<explicit-origin>',
});

const current = <existing-store-or-orchestrator>({
  source: normalized,
  sourceAuthority: authority,
});

// Bind the existing governed parents. Do not manufacture solver/parser topology here.
current.<existing-bind-parent>(<parent-evidence>);
current.<existing-bind-profile>(<profile>);

const produced = current.<existing-produce-action>();
assert(produced.<qualification-field> === 'PASS');

const prepared = current.<existing-preflight-or-prepare>();
assert(prepared.<authorization-field> === 'READY');

current.<existing-run-action>();

const after = current.<existing-state-reader>();
assert(after.<execution-status> === '<expected-status>');
assert(after.<retained-parent-id> === produced.<retained-parent-id>);
```

If a function name/signature differs on live main:

```text
use the existing live public API
DO NOT add a second path to satisfy this skeleton
```

## 6.3 Expected changed files/domains

```text
<path 1>
<path 2>
<test path>
```

## 6.4 Protected unchanged files/domains

```text
<solver formulation / parser grammar / source oracle / roadmap / workflow / etc.>
```

Changing a protected domain requires separate evidence and Owner authority where applicable.

---

# 7. PASS / FAIL / NOT_RUN criteria

## 7.1 Focused product/implementation gate

| Gate | Expected result | Evidence |
|---|---|---|
| `<command/test>` | PASS | `<specific assertion>` |
| `<negative test>` | PASS | `<must reject stale/invalid case>` |
| `<runtime route>` | PASS | `<exact state/hash/result>` |

Concrete required conditions:

```text
<field> == <value>
<count> == 0
<hash A> == <hash B>
<residual> <= <tolerance + units>
```

## 7.2 Validation truth

Never conflate:

```text
PASS
FAIL
NOT_RUN
NOT_APPLICABLE
```

Infrastructure failure, empty workflow jobs, source inspection, mergeability, or an unexecuted test is not PASS.

## 7.3 Before/after expectation

Before patch:

```text
<expected failing/absent behavior>
```

After patch:

```text
<expected PASS behavior>
```

Neighbor behavior that must remain unchanged:

```text
<regression boundary>
```

---

# 8. Benchmark / independent oracle criteria

| ID | Type | Definition/source | Inputs | Expected quantity | Tolerance | Independent? | Status |
|---|---|---|---|---|---|---|---|
| BM-001 | FROZEN_ANALYTICAL | `<path/ref>` | `<actual values>` | `<expected>` | `<tol>` | YES | READY / NOT_RUN |
| BM-002 | PRODUCT_REGRESSION | `<test/fixture>` | ... | ... | ... | NO | READY |

Allowed benchmark classes:

```text
FROZEN_ANALYTICAL
AUTHORITATIVE_REFERENCE
EXPERIMENTAL
CROSS_SOLVER
FROZEN_EXTERNAL_DATA
PRODUCT_REGRESSION
```

Critical anti-circularity rules:

```text
production output must not choose the independent expected value
tolerance must not be relaxed because production fails
product regression must not be called an independent oracle
moving maxima/interpolated display values must not replace fixed physical probes when the benchmark requires fixed probes
```

If no valid independent benchmark exists yet, freeze/qualify one before treating production as numerically validated.

---

# 9. Anti-drift / fail-closed logic

Before production mutation:

```text
1. re-ground live main
2. re-read this issue and current Owner comments
3. re-read applicable Owner Roadmap(s)
4. inspect open PR/WIP overlap
5. compare creation-time assumptions to live code
6. classify drift
```

Drift outcomes:

```text
NO_MATERIAL_DRIFT
STATUS_ONLY
ASSUMPTION_OBSOLETE
OWNER_INTENT_CHANGED
SOURCE_ORACLE_AUTHORITY_CHANGED
OVERLAP_CONFLICT
UNKNOWN
```

Rules:
- `NO_MATERIAL_DRIFT` → proceed.
- `STATUS_ONLY` → update current status; proceed only if scope/authority unchanged.
- `ASSUMPTION_OBSOLETE` → do not implement the stale assumption; prove current behavior and revise the plan inside existing Owner intent.
- `OWNER_INTENT_CHANGED`, `SOURCE_ORACLE_AUTHORITY_CHANGED`, `UNKNOWN` → READ_ONLY until re-grounded/authorized.
- `OVERLAP_CONFLICT` → coordinate/take over/partition; do not silently create a second writer.

Forbidden anti-drift shortcuts:

```text
NO hard-coded stale SHA as production authority
NO hidden default engineering input
NO direct-core bypass of required public route
NO benchmark expected-value regeneration from production output
NO tolerance weakening to obtain PASS
NO capability/registry wording wider than proven behavior
NO roadmap/source/oracle mutation without authority
NO NOT_RUN -> PASS promotion
```

---

# 10. Negative tests and falsifiers

At minimum include:

1. one deliberately stale-parent/input case;
2. one malformed/invalid input case;
3. one case proving the public route—not a direct shortcut—was used;
4. one benchmark falsifier/neighbor case;
5. one hypothesis falsifier for the proposed first patch.

Example:

```text
Change <parent semantic field> without regenerating <dependent artifact>.
Expected: run/compile/publication is rejected with <specific state/error>.
```

---

# 11. Explicit exclusions / non-goals

```text
NO <unrelated formulation>
NO <source-schema expansion>
NO benchmark re-baselining from output
NO <unrelated UI/architecture rewrite>
NO Owner Roadmap mutation
NO merge without Owner authorization
```

Use only relevant exclusions.

---

# 12. Validation matrix

| Boundary | PASS required? | Independent oracle? | Negative test? | Current creation-time status |
|---|---:|---:|---:|---|
| Input/source custody | YES | N/A | YES | NOT_RUN / SOURCE_INSPECTED |
| Production path | YES | N/A | YES | NOT_RUN |
| Numerical/semantic correctness | YES | YES where applicable | YES | NOT_RUN |
| Output/publication | YES | depends | YES | NOT_RUN |
| Anti-drift | YES | N/A | YES | NOT_RUN |

Creation-time source inspection does not pre-qualify implementation tests.

---

# 13. Delivery / handover contract

Implementation must follow the live repository delivery policy.

For GitHub-issue-based work, the issue becomes the original task/Owner-baseline source; the implementation chain should bind the stable work item:

```text
WORK_ITEM_SOURCE: GITHUB_ISSUE
WORK_ITEM_KEY: github:<owner>/<repo>#<this-issue-number>
```

Do not duplicate the full delivery protocol in this issue. Read the live Common skill.

Merge authority:

```text
OWNER_ONLY
```

unless the Owner explicitly states otherwise.

---

# Appendix A — implementation qualification

Incoming agent must answer from the **live repository plus the issue inputs**, not from textbook memory or this issue alone.

QUESTION_PROFILE: <NUMERICAL_ENGINEERING | SOFTWARE_ENGINEERING | SOURCE_GOVERNANCE>

## Q1 — Walk me through the actual case

<Use a real object/case/file/function/ID. Ask the agent to trace it end-to-end and name exact boundaries and values/hashes that should survive.>

## Q2 — Do this calculation/reconstruction before touching the code

<Supply the actual numeric/byte/state inputs. Require a hand calculation or deterministic reconstruction, predicted intermediate values, and the first production function that should agree.>

## Q3 — Show me where the wrong/stale state gets stopped

<Give one specific mutation/stale-parent case. Require the exact gate, expected rejection state, and one falsifier that would prove the candidate misunderstood custody.>

## Q4 — Prove the benchmark independently

<Require an analytical/reference/cross-solver reconstruction using actual inputs, units/sign/tolerance, without reading production output first.>

## Q5 — What is the smallest patch you would make?

<Require exact files/functions, expected failing evidence before, PASS after, protected unchanged domains, negative test, rollback condition and NO-PATCH case.>

Automatic qualification failure if the answer fabricates repository evidence, changes an oracle to match output, treats a visual result as validation, or answers without the required hand/exact reconstruction.
```
