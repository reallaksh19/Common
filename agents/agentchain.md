# Engineering Agent Chain

AGENTCHAIN_VERSION: 2

## ACTIVE CHAINS

| Chain | Mission | Latest endpoint | PR | State | Authority domain | Next action |
|---|---|---|---|---|---|---|
| COMMON-ENG-PR-DELIVERY-V2 | Introduce crash-safe repo-wide engineering relay Skill without replacing v1 yet | EP-0001 | #17 | QUALIFICATION_REQUIRED | Cross-repository engineering-agent delivery governance | Execute the v2 self-test, independently audit the relay gates, then prepare the minimal adoption leg if the evidence passes |

# ENDPOINTS

## EP-0001

CHAIN_ID: COMMON-ENG-PR-DELIVERY-V2
LEG_ID: LEG-001
ENDPOINT_ID: EP-0001
PREVIOUS_ENDPOINT: NONE — chain start

CREATED_AT: 2026-08-27
ENDPOINT_REASON: NORMAL_CHECKPOINT

TASK / ISSUE: Owner-directed engineering relay v2 redesign
PR: #17
BRANCH: engineering-pr-delivery-v2-relay

CHECKPOINT_HEAD: fdeab8553196d69ace9c021d79e790fdbd65d6fd
MAIN_HEAD_OBSERVED: 551d614c581f39a47015106ae9866c44304d8e9f
MERGE_BASE: 551d614c581f39a47015106ae9866c44304d8e9f

STATE: QUALIFICATION_REQUIRED

### Mission

Create `engineering-pr-delivery-v2` as a sibling of the current workreport-centric Skill. V2 must operate as a crash-safe relay: `agents/agentchain.md` is the repo-wide baton, graceful handoff is optional, each non-terminal endpoint indexes all required engineering/reference material and contains exactly five questions for the next unresolved leg, and a candidate cannot self-award engineering-critical write authority.

### This leg completed

- Added the complete initial v2 Skill entry point and OpenAI interface metadata.
- Added relay model, endpoint schema/template, crash recovery, source/benchmark/common-document indexing, chain-level multi-agent coordination, engineering validation, anti-gaming, Git/PR, and AUTO MODE references.
- Added separate candidate-answer and verifier-verdict qualification templates.
- Added executable validators for `agentchain.md` and independent qualification verdicts plus a composite checker.
- Added synthetic self-tests containing positive relay fixtures and negative cases for candidate self-verification and empty benchmark custody.
- Opened draft PR #17 from exact `main@551d614c581f39a47015106ae9866c44304d8e9f`.
- Preserved the legacy `skills/engineering-pr-delivery/**` package and root `AGENTS.md` unchanged in this leg.

### Currently in progress

V2 initial implementation is present in draft PR #17. Execution of the new Python self-test is still required in an environment with a repository checkout or equivalent executable access. Adoption into root `AGENTS.md` and downstream repositories has deliberately not started.

### Remaining work

1. Execute `python skills/engineering-pr-delivery-v2/scripts/self_test.py` against the actual PR head.
2. Independently audit the validator semantics, especially endpoint lineage, question-set requirements, source inventories, self-verification rejection, score arithmetic, and material-state freshness assumptions.
3. Correct any defects found without modifying the legacy Skill.
4. After the v2 package is technically accepted, perform a separate minimal adoption leg: update `Common/AGENTS.md` to recognize v2 and pilot the relay on one real engineering repository/workstream.
5. Do not roll out downstream until an A -> B -> C relay including one simulated abrupt agent loss has been demonstrated.

### Exact next action

Execute `python skills/engineering-pr-delivery-v2/scripts/self_test.py` on PR #17 head and inspect every expected PASS/FAIL outcome; if any negative fixture is accepted or any positive fixture is rejected, isolate the validator defect before touching adoption policy.

### Known / proven

- Live base at branch creation was `main@551d614c581f39a47015106ae9866c44304d8e9f`.
- PR #17 exists as an open draft and the implementation before this metadata endpoint was additive under `skills/engineering-pr-delivery-v2/**`.
- V2 text explicitly removes mandatory per-PR workreports from its default relay architecture.
- The v2 qualification protocol separates endpoint author, incoming candidate, and verifier roles and declares `candidate_id == verifier_id` incapable of granting engineering-critical `WRITE_ALLOWED`.
- The v2 endpoint contract requires the six inventories: Inputs, Benchmarks, Common/Governing Documents, Authoritative Sources, Production Paths, Validation/Test Paths.

### Not proven

- The Python validators have not yet been executed against the actual committed files in this connected editing environment.
- The v2 model has not yet been piloted across multiple real agents.
- Crash recovery has not yet been demonstrated on a real partially advanced PR.
- Downstream repositories have not adopted the new Skill.

### NOT_RUN

- `python skills/engineering-pr-delivery-v2/scripts/self_test.py` — NOT_RUN in the connected editing environment.
- A -> B -> C real relay pilot — NOT_RUN.
- Simulated abrupt-agent-loss recovery on a real engineering workstream — NOT_RUN.
- Downstream adoption validation — NOT_RUN.

### Active hypothesis

A small repo-wide append-only endpoint ledger plus separate candidate/verifier qualification artifacts will preserve engineering continuity more reliably than large per-PR workreports, because the latest trusted state and next-agent exam exist continuously and do not depend on an outgoing agent performing a graceful handoff.

### Falsifier

The hypothesis is falsified or materially weakened if any of the following occurs during pilot: a new agent cannot safely recover the next leg from the latest endpoint plus indexed artifacts and live repository state; the validator permits candidate self-verification to grant write authority; the five questions become retrospective/generic rather than next-leg-specific; source/benchmark/common-document custody becomes stale or unmanageably duplicated; or abrupt loss still requires reconstructing essential intent from chat.

### Protected invariants

- Repository/live Git truth outranks stale relay metadata.
- Engineering validation integrity and independent-oracle boundaries from v1 are not weakened.
- Candidate self-verification cannot grant engineering-critical write authority.
- `NOT_RUN` remains explicit across relay endpoints.
- PR merge does not imply engineering-chain completion.
- Graceful handoff is optional; recovery must work from durable repository state.

### Do not redo

- Do not recreate the v2 package under another name unless this architecture is explicitly superseded.
- Do not reintroduce a mandatory large per-PR workreport into v2 as the primary baton.
- Do not replace the current v1 package in this leg; compatibility/adoption is a separate decision.

### Do not change

For this initial qualification leg, do not change:

- `skills/engineering-pr-delivery/**`;
- root `AGENTS.md`;
- repository workflows;
- unrelated Skills.

Any adoption pointer change belongs to the next accepted leg after v2 validation.

### Expected next-leg files / domains

If validator defects are found, only the affected files under:

- `skills/engineering-pr-delivery-v2/scripts/**`;
- directly corresponding v2 references/templates when semantics need correction.

After package acceptance, the separate adoption leg is expected to touch `AGENTS.md` and repo relay/pilot artifacts, not the legacy Skill implementation.

### Inputs

- `skills/engineering-pr-delivery/SKILL.md` @ `551d614c581f39a47015106ae9866c44304d8e9f` — legacy behavior being redesigned, not modified in LEG-001.
- `skills/engineering-pr-delivery/references/takeover-qualification.md` @ `551d614c581f39a47015106ae9866c44304d8e9f` — source of the existing five challenge archetypes and 92/17 thresholds retained conceptually.
- `skills/engineering-pr-delivery/references/continuous-handover.md` @ `551d614c581f39a47015106ae9866c44304d8e9f` — source of useful crash-recovery principles being simplified into the endpoint relay.

### Benchmarks

- `skills/engineering-pr-delivery-v2/scripts/self_test.py` @ PR #17 — structural relay test fixture set; classification: IMPLEMENTATION_COUPLED_SYNTHETIC, not an independent engineering oracle.
- Negative fixture: candidate and verifier both `agent-b` must be rejected.
- Negative fixture: empty Benchmarks inventory must be rejected.
- Positive fixture: 94/100 with minimum 18/20, separate candidate/verifier, matching basis head must pass structural qualification validation.

### Common / governing documents

- `AGENTS.md` @ `551d614c581f39a47015106ae9866c44304d8e9f` — current repository policy; still points to legacy v1 and is intentionally unchanged in LEG-001.
- `skills/engineering-pr-delivery-v2/SKILL.md` @ PR #17 — proposed v2 governing Skill for relay behavior.
- `skills/engineering-pr-delivery-v2/references/agentchain-schema.md` @ PR #17 — endpoint contract.
- `skills/engineering-pr-delivery-v2/references/qualification.md` @ PR #17 — takeover qualification contract.

### Authoritative sources

NONE — this PR changes engineering-agent delivery governance, not a physical engineering calculation method. The owner-directed relay requirements are encoded in the proposed v2 Skill and this endpoint; no external engineering standard is being claimed as authority for the governance design.

### Production paths

- `skills/engineering-pr-delivery-v2/SKILL.md`
- `skills/engineering-pr-delivery-v2/references/**`
- `skills/engineering-pr-delivery-v2/agents/openai.yaml`

### Validation / test paths

- `skills/engineering-pr-delivery-v2/scripts/validate_agentchain.py`
- `skills/engineering-pr-delivery-v2/scripts/validate_qualification.py`
- `skills/engineering-pr-delivery-v2/scripts/check_relay.py`
- `skills/engineering-pr-delivery-v2/scripts/self_test.py`

### Changed during this leg

Before this endpoint metadata commit, PR #17 contained exactly 19 added v2 package files: `SKILL.md`, `agents/openai.yaml`, twelve reference/template files, and four Python validation/self-test scripts. No legacy Skill, root policy, or workflow file was modified.

### Validation summary

- Repository/base grounding: PASS by live GitHub observation at branch creation.
- Branch comparison before PR: PASS — branch was ahead of exact base and zero behind; all implementation paths were additive under `skills/engineering-pr-delivery-v2/**`.
- PR creation: PASS — draft PR #17 created.
- Hosted workflow evidence: NOT_RUN / NONE OBSERVED — no workflow runs were associated with the PR head when checked.
- Python self-test: NOT_RUN in connected editing environment.
- Real multi-agent relay validation: NOT_RUN.

### Open risks / questions

- RISK: structural Markdown validators cannot themselves prove that question content is genuinely expert-level; verifier review and real pilot evidence remain necessary.
- RISK: exact HEAD equality is insufficient to classify material vs metadata-only drift; v2 currently defines the semantic rule but does not automate full Git semantic classification.
- QUESTION: whether root `AGENTS.md` should make v2 canonical immediately after package validation or first run a bounded pilot while v1 remains default.
- QUESTION: whether downstream repositories should keep legacy status/claim/workreport files during migration or deprecate them once `agentchain.md` proves sufficient.

### Next-agent qualification

QUALIFICATION_BASIS_HEAD: fdeab8553196d69ace9c021d79e790fdbd65d6fd
QUESTION_SET_ID: QS-COMMON-V2-0001
QUESTION_SET_STATUS: CURRENT

#### Q1 — Production Trace

From live PR #17, trace how an incoming engineering-critical agent is supposed to move from `agents/agentchain.md` discovery through the v2 Skill, latest endpoint, candidate answer, verifier verdict, and finally into permitted production mutation. Name the exact v2 files/sections/scripts involved and identify the first point where v1-style self-scoring is prevented. Show what is policy-only versus machine-enforced.

#### Q2 — Current Unresolved Problem / Failure Isolation

Execute or independently reproduce the committed v2 self-test behavior. Predict the outcomes for the valid agentchain, valid independent qualification, self-verifier qualification, empty-benchmark endpoint, and composite gate before execution. If actual behavior differs, identify the smallest validator defect, its falsifier, and the first wrong function/regex rather than broadening the patch.

#### Q3 — Authority / Invariant

Reconcile current root `AGENTS.md` authority with the new sibling v2 Skill. Identify exactly why LEG-001 did not modify the root pointer or legacy Skill, what authority would change if `AGENTS.md` made v2 canonical, and which validation/anti-gaming invariants from v1 must survive adoption. Name at least one attractive but invalid shortcut that would silently weaken evidence or compatibility.

#### Q4 — Independent Validation

Design an independent crash-recovery test that does not merely call the v2 validators: construct a realistic A -> B scenario where Agent A disappears after the last endpoint but after at least one additional material commit. Specify what B must recover from the endpoint, what must be re-grounded live, how post-endpoint commits are classified, what observation would make continuation unsafe, and what evidence would demonstrate that chat history is unnecessary.

#### Q5 — Next Contribution / Minimal Patch

Assuming the v2 scripts pass and no semantic defect is found, define the smallest legitimate adoption contribution. State the exact files/domains expected to change, how `Common/AGENTS.md` should introduce v2 without destroying v1 traceability, what real repository/workstream should be used for the A -> B -> C pilot, what must remain unchanged, and what evidence must exist before downstream rollout or canonical promotion.
