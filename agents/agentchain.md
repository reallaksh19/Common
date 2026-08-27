# Engineering Agent Chain

AGENTCHAIN_VERSION: 2

## ACTIVE CHAINS

| Chain | Mission | Latest endpoint | PR | State | Authority domain | Next action |
|---|---|---|---|---|---|---|
| COMMON-ENG-PR-DELIVERY-V2 | Introduce crash-safe repo-wide engineering relay Skill without replacing v1 yet | EP-0002 | #17 | QUALIFICATION_REQUIRED | Cross-repository engineering-agent delivery governance | Execute the v2 self-test on the latest material head and independently audit the validator semantics before adoption |

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

## EP-0002

CHAIN_ID: COMMON-ENG-PR-DELIVERY-V2
LEG_ID: LEG-001
ENDPOINT_ID: EP-0002
PREVIOUS_ENDPOINT: EP-0001

CREATED_AT: 2026-08-27
ENDPOINT_REASON: POST_MUTATION

TASK / ISSUE: Owner-directed engineering relay v2 redesign
PR: #17
BRANCH: engineering-pr-delivery-v2-relay

CHECKPOINT_HEAD: 4a207360c504ea45a426b3e3469f5fc2fb1fd35b
MAIN_HEAD_OBSERVED: 551d614c581f39a47015106ae9866c44304d8e9f
MERGE_BASE: 551d614c581f39a47015106ae9866c44304d8e9f

STATE: QUALIFICATION_REQUIRED

### Mission

Qualify the initial `engineering-pr-delivery-v2` relay package before any root-policy or downstream adoption.

### This leg completed

After EP-0001, tightened `validate_qualification.py` so a numerically passing candidate cannot be failed with a meaningless `AUTOMATIC_FAILURE_REASON: NONE`, and expanded `self_test.py` with negative fixtures for below-17 `PASS_WRITE_ALLOWED` and unjustified numeric-pass failure. The prior EP-0001 was preserved unchanged and this new endpoint was appended rather than rewriting history.

### Currently in progress

The v2 package and dogfood relay ledger are present in draft PR #17. Actual Python execution remains NOT_RUN in the connected editing environment.

### Remaining work

- Execute the committed self-test against this material checkpoint.
- Independently inspect the regex/field parsing for false PASS and false FAIL behavior.
- Reconcile PR diff and current `main` before any adoption change.
- If package validation succeeds, create a new leg for bounded adoption/pilot rather than modifying root policy inside this qualification leg.

### Exact next action

Run `python skills/engineering-pr-delivery-v2/scripts/self_test.py` at or against material checkpoint `4a207360c504ea45a426b3e3469f5fc2fb1fd35b`, confirm all seven expected fixture outcomes, and isolate any mismatch before changing v2 semantics or adoption policy.

### Known / proven

- EP-0001 remains in repository history unchanged.
- The current material validator head is `4a207360c504ea45a426b3e3469f5fc2fb1fd35b` before this relay-metadata commit.
- `validate_qualification.py` now treats `NONE`, `N/A`, `NA`, and `NOT_APPLICABLE` as non-substantive automatic-failure reasons when a numeric pass is overridden to `FAIL_READ_ONLY`.
- `self_test.py` now contains seven fixture checks including self-verification rejection, below-minimum pass rejection, unjustified numeric-pass failure rejection, and empty benchmark inventory rejection.

### Not proven

- No executable run of the committed validators has yet been observed.
- No independent agent has yet completed Q1-Q5 against this endpoint.
- No real abrupt-loss recovery pilot has yet been performed.

### NOT_RUN

- `python skills/engineering-pr-delivery-v2/scripts/self_test.py` — NOT_RUN.
- Independent qualification answer/verdict against QS-COMMON-V2-0002 — NOT_RUN.
- A -> B -> C relay pilot — NOT_RUN.

### Active hypothesis

The stricter qualification validator and expanded negative fixtures close the obvious structural paths by which a candidate could self-authorize or a verifier could misrepresent threshold/automatic-failure semantics, while keeping substantive expert judgment outside the structural parser.

### Falsifier

Any committed self-test negative fixture returning exit 0, any valid fixture returning nonzero, or any independent review showing that a candidate can obtain `PASS_WRITE_ALLOWED` through identity/score/basis manipulation falsifies the current validator hypothesis.

### Protected invariants

- Candidate self-verification never grants engineering-critical write authority.
- Total >=92 and every question >=17 remain the default numeric pass threshold.
- A verifier may override a numeric pass only for a substantive recorded automatic-failure reason.
- Missing benchmark/source/common-document custody must be explicit rather than silently omitted.
- Legacy v1 and root `AGENTS.md` remain unchanged during package qualification.

### Do not redo

- Do not replace EP-0001; supersede via later endpoint only.
- Do not recreate the old Appendix-A self-score model inside v2.
- Do not duplicate detailed evidence into `agentchain.md` when a path/locator suffices.

### Do not change

Until package qualification passes, do not change:

- root `AGENTS.md`;
- `skills/engineering-pr-delivery/**`;
- workflows;
- downstream repositories.

### Expected next-leg files / domains

If tests expose defects: only `skills/engineering-pr-delivery-v2/scripts/**` and directly coupled v2 reference/template semantics. If no defects are found, the next separate adoption leg may touch root policy and pilot artifacts.

### Inputs

- EP-0001 in `agents/agentchain.md` — prior durable relay state.
- `skills/engineering-pr-delivery-v2/scripts/validate_qualification.py` @ material checkpoint `4a207360c504ea45a426b3e3469f5fc2fb1fd35b`.
- `skills/engineering-pr-delivery-v2/scripts/self_test.py` @ material checkpoint `4a207360c504ea45a426b3e3469f5fc2fb1fd35b`.

### Benchmarks

- `self_test.py` valid independent qualification: expected structural PASS.
- `self_test.py` self-verifier fixture: expected FAIL.
- `self_test.py` any-question-below-17 `PASS_WRITE_ALLOWED`: expected FAIL.
- `self_test.py` numeric-pass `FAIL_READ_ONLY` with `AUTOMATIC_FAILURE_REASON: NONE`: expected FAIL.
- `self_test.py` empty Benchmarks inventory: expected FAIL.
- Classification: IMPLEMENTATION_COUPLED_SYNTHETIC structural fixtures; they do not replace independent relay pilot evidence.

### Common / governing documents

- `AGENTS.md` @ `551d614c581f39a47015106ae9866c44304d8e9f` — current Common policy, unchanged.
- `skills/engineering-pr-delivery-v2/SKILL.md` @ PR #17.
- `skills/engineering-pr-delivery-v2/references/qualification.md` @ PR #17.
- `skills/engineering-pr-delivery-v2/references/agentchain-schema.md` @ PR #17.

### Authoritative sources

NONE — governance/tooling leg; no physical engineering standard is being modified. Current behavioral authority for this proposed Skill is its committed v2 specification plus owner-directed relay requirements encoded there.

### Production paths

- `skills/engineering-pr-delivery-v2/scripts/validate_qualification.py`
- `skills/engineering-pr-delivery-v2/scripts/validate_agentchain.py`
- `skills/engineering-pr-delivery-v2/SKILL.md`
- `skills/engineering-pr-delivery-v2/references/**`

### Validation / test paths

- `skills/engineering-pr-delivery-v2/scripts/self_test.py`
- `skills/engineering-pr-delivery-v2/scripts/check_relay.py`
- `skills/engineering-pr-delivery-v2/scripts/validate_agentchain.py`
- `skills/engineering-pr-delivery-v2/scripts/validate_qualification.py`

### Changed during this leg

After EP-0001 material basis, changed only:

- `skills/engineering-pr-delivery-v2/scripts/validate_qualification.py` — tightened substantive automatic-failure reason handling.
- `skills/engineering-pr-delivery-v2/scripts/self_test.py` — added two negative qualification fixtures.
- `agents/agentchain.md` — relay metadata/index update only in this commit.

### Validation summary

- Source inspection of the tightened validator: PASS for intended rule presence.
- Self-test fixture authoring: PASS by source inspection.
- Actual Python execution: NOT_RUN.
- Hosted PR workflows: none observed previously; no execution claim is made.

### Open risks / questions

- Structural parsers still cannot establish that Q1-Q5 are genuinely expert-level; this remains a verifier/pilot responsibility.
- Material-vs-metadata drift is semantically defined but not fully automated from Git diff classification.
- It remains undecided whether v2 becomes canonical immediately after package validation or only after a bounded real pilot.

### Next-agent qualification

QUALIFICATION_BASIS_HEAD: 4a207360c504ea45a426b3e3469f5fc2fb1fd35b
QUESTION_SET_ID: QS-COMMON-V2-0002
QUESTION_SET_STATUS: CURRENT

#### Q1 — Production Trace

Trace the live v2 path from `agents/agentchain.md` latest-endpoint discovery through `SKILL.md` sections 5/9/10, the candidate answer template, verifier verdict template, and `validate_qualification.py`. Identify exactly which rule is prose-only and which checks are executable for candidate/verifier identity, basis-head matching, score arithmetic, 92/17 thresholds, and substantive automatic-failure reasons.

#### Q2 — Current Unresolved Problem / Failure Isolation

Execute `self_test.py` or independently reproduce its seven cases against the current material checkpoint. State predicted exit behavior first. If any mismatch occurs, identify the first wrong parser/function and the smallest legitimate fix; do not modify qualification thresholds or weaken a negative fixture to obtain green status.

#### Q3 — Authority / Invariant

Explain the authority boundary between legacy root `AGENTS.md`, legacy `engineering-pr-delivery`, proposed `engineering-pr-delivery-v2`, and this dogfood `agentchain.md`. Identify what would become authoritative if root `AGENTS.md` points to v2 and which v1 evidence-integrity rules must be preserved during that adoption.

#### Q4 — Independent Validation

Without relying only on the structural validators, construct a manual qualification case where a candidate supplies plausible but fabricated repository anchors or a generic theory answer. Show why structural scripts alone cannot safely grant engineering expertise and define the verifier evidence needed to reject that candidate despite syntactically valid files.

#### Q5 — Next Contribution / Minimal Patch

If all package tests pass, specify the smallest separate adoption leg: exact Common files to change, exact legacy files to preserve, how to introduce v2 without erasing v1 traceability, the first real engineering workstream suitable for an A -> B -> C plus abrupt-loss pilot, and the acceptance evidence required before downstream rollout.
