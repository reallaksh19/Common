# Packet sufficiency and inter-Core contracts

Status: PROPOSED CONTRACT. This is a semantic specification to inform later schemas. Field presence does not establish content quality.

## Design test

A fresh receiving agent must be able to identify the task, retrieve original evidence, reconstruct the important reasoning, detect a planted false claim, and continue without asking the previous instance to remember its rationale. Packet brevity is useful only while this remains possible.

A packet is a reviewable claim or decision with evidence. It is not the evidence authority merely because another agent produced it. Referencing a source also does not make every elaboration a quoted or observed fact.

## Shared envelope

| Field | Required meaning |
|---|---|
| packet_id / family / schema_version | Stable identity, typed payload and interpretation rules |
| packet_version / content_digest | Immutable version; digest algorithm and canonical serialization rule explicitly specified |
| run_id / task_id / attempt_id / bundle_id | Product, logical work, particular attempt and 1–3-subtopic assignment |
| subtopic_ids / capability_ids | Scope and affected capabilities; prerequisite refs can point outside this bundle |
| producer | Role, profile ID/version, instance ID, model/config identity where available; tool/human origin separately |
| source_refs | Immutable source ID/version, exact page/region/question/line locator, original and normalized links, retrieval status |
| dependency_refs | Exact packet/artifact versions and dependency kind: semantic, demand, representation, teaching, policy or assembly |
| grounding_kind | Direct source observation, reasoned derivation, pedagogical elaboration, new exercise, owner instruction or unverified proposal |
| epistemic_status | Observed, supported, disputed, unsupported or unknown, with reasons and evidence scope |
| confidence | Reasoned uncertainty and limits; optional calibrated score with stated basis, never a guessed universal probability |
| review_refs | Independent claim-level dispositions and the basis each reviewer actually used |
| owner_brief_ref / override_refs | Exact controlling policy versions and local decisions |
| supersedes / lifecycle_state | History linkage; draft, accepted, rejected, quarantined or superseded |
| payload | The intellectually necessary content; no acceptance through an empty generic narrative |

Use a manifest to locate packets. Keep committed accepted versions immutable. IDs survive display renumbering and reshards. A changed explanation is a new version; a changed ID alone must not hide unchanged duplicated work.

## What must travel inline

Inline: task/goal, scope boundaries, key assumptions, decisive reasoning, contested claims, unresolved gaps, immediate obligations, exact dependencies and retrieval locators. The receiver should see that a hidden-condition risk exists before deciding which source to open.

Referenced and fetched as needed: complete original pages, large question collections, extended derivations, full drawings, all candidate representations and prior audit logs. A manifest provides discoverability and access to the complete available original source; scoped retrieval must not conceal inconvenient source regions.

A small bundle does not justify thousands of vague references. Resolve the critical set before proceeding. A missing image, inaccessible formula crop or broken reference is a gap with a consequence, not permission to guess.

## Family map

| Packet | Producer → consumer | Minimum payload that preserves intellectual work |
|---|---|---|
| GT | Core0 → all | Source inventory; stable original locators and normalized mappings; figures/options/keys; declared scope authority; integrity and absence states |
| R | Governor → worker/recovery | Evidence-based route; eligible profiles; selected instance; bundle/version; reason; rejected alternatives; task signature; budget and stop conditions |
| G | Any → Governor/Join | Missing item or uncertainty, affected claims/capabilities, what cannot be concluded, permitted bounded continuation and resolution action |
| K | Core1 → Core2/Join/1A/2A | Definitions versus laws/models; dependencies; derivation spine with justifications; assumptions/limits; interpretation, invariants, contrasts and representation affordances |
| D | Core2 → Core1/Join/1A/2A | Original question refs; complete interpretation; verified solution route(s); recognition cue; first non-obvious move; dependency set; difficulty dimensions; wrong chains; hint semantics; transfer envelope and evidence limits |
| V | Independent receiver/reviewer → Join | Claim version; independent source-only result; comparison disposition; evidence; correction or consequence; reviewer exposure/role record |
| J | Join coordinator → 1A/Governor | Validated K/D intersection and differences; release-critical conflicts; prerequisite closure; owner brief; per-capability assimilation obligations and acceptance criteria |
| CT | Core1A → plan/reviewer | Intended before/after understanding; difficult distinction; transformation; required experience; explanation/check that would expose failure |
| LA | Core1A → author/reviewer | One meaningful learning transition; entry capability assumption; action; justification; expected interpretation; split rationale; reconstruction into larger concept |
| IC | Core1/1A → reviewer | Ordered reasoning edges, rule justifying each, prerequisite, hidden-condition risk, permitted jump assumption and unresolved edge |
| EA | Core1/1A → author/reviewer | Valid derivation plus teaching expansion: parent relation, conditions, symbols/units or domains, legal transformations, meaning, cases and failure boundary |
| RR | Core1A → representation selection | Cognitive need; what to notice; conventions prerequisite; required relationships; accessibility need; must_not_imply |
| RC | Core1A/tool → selector | Candidate visual/model/analogy, mapped concepts, benefit, extra interpretation load, failure risks and production feasibility |
| RD | Selector → author/reviewer | Chosen candidate, rationale, alternatives/rejection, reading order, exact equation/word bridge, conventions and visual QA obligations |
| MC | Core1A → author/2A | Plausible wrong causal chain, diagnostic contrast, correction explanation, boundary of analogy and follow-up check |
| SB | Core1A → author | Symbol-to-meaning mapping, referent/domain/unit, link to visual/words and ambiguity checks |
| FP | Core1A → author/2A | Worked decision, exact support removed at each stage, retained support, independent responsibility and intended check |
| A | Core1A → realization/QA | Ordered composition of these accepted pieces, obligation coverage, scoped learner assumptions, owner treatment and unresolved work |
| T | Content reviewer after realization → 2A | Exact accepted artifact version, capability, explanation/visual/example/task locators, support depth and limits, content-review evidence; no inferred mastery |
| X | Core2A → reviewer/publisher | Full question, diagram/options if any, exact answer and solution, selected owner level, semantic/demand/T dependencies, hint semantics, provenance, transfer legality and review result |
| LS | Owner/intake → all | Capability-specific reported/observed/assumed readiness; percentage context and uncertainty; representation/algebra/language prerequisites; no fabricated diagnostics |
| PUR | Owner/intake → Governor/1A/2A | Owner practice/learning brief: purpose, audience, target, allowed range, support, count/time, sources, exclusions and success definition |
| OVR | Owner/control → affected stages | Finding preserved, explicit owner decision, hard/soft scope and duration, impacted claims/tasks, final action and downstream disclosure |

These are typed records, not a requirement for 26 separate files or agents per atom. A single immutable bundle may contain related records; independent IDs permit selective retrieval and invalidation.

## K and D: the important middle, not just endpoints

A K equation record saying only v_y = u_y - gt loses why it applies. It must retain upward-positive convention, constant downward acceleration, elapsed-time origin, the relation between change in velocity and acceleration, substitution, dimensional meaning and the fact that zero velocity does not imply zero acceleration.

A D record saying only difficulty=hard and uses gravity loses the assessment author's intelligence. It should identify why an apex cue is tempting, why velocity and acceleration are confused, which component is zero, the first useful distinction, the permitted solution routes and which changed conditions would invalidate them.

K can cite a canonical derivation and D can reference it. D still needs to state the question-specific choice and condition, rather than duplicating the entire derivation or erasing its application.

## Claim-level validation

A V record applies to a particular claim version, not a whole packet by reputation.

| Disposition | Meaning and downstream action |
|---|---|
| CONFIRMED | Independently supported under the same scope and conditions; record basis |
| REFINED | Supported after an explicit qualification or correction; create a revised claim before acceptance |
| MISSING | Required semantic or demand content is absent; create an obligation or correction task |
| UNSUPPORTED | Current cited material does not support the assertion; do not turn it into established evidence |
| CONTRADICTED | Evidence or valid reasoning conflicts; quarantine impacted claims and resolve |
| OUT_OF_SCOPE | May be true but does not belong to the current authorized product; retain disposition |
| UNKNOWN | Available evidence/reviewer competence cannot decide; state consequence and escalation |

REFINED does not mean silently accepting the original. CONFIRMED without a retrieval/derivation basis is an agreement report, not independent validation.

Original question, normalized transcription and supplied key must be separately identifiable. A disagreement with the key records ANSWER_KEY_CONFLICT; it does not justify altering the original source record. A corrected publication answer needs its own reasoning and review.

## Receipt granularity

A T receipt for CAP-DISTINGUISH-VELOCITY-ACCELERATION should point to:
- the explanation stating the difference;
- the chosen picture and its legend;
- the interpreted equation step;
- the worked contrast and independent task if requested;
- the exact review and artifact version.

It must identify limitations, such as only vertical motion or no dot-product treatment. It must not count a heading, planned diagram or answer-only exercise as an explanation.

Core2A checks that each semantic requirement used in its question, hints and solution is supported or explicitly allowed under a declared diagnostic/stretch mode. Merely checking that the question's primary concept exists misses supporting prerequisites.

## Receiving algorithm

1. Verify task identity, owner brief, source manifest, scope and dependency versions.
2. In the role's initial independent phase, retrieve original inputs and record the applicable semantic/demand/pedagogical requirements before seeing upstream conclusions. Record what was visible.
3. Open the upstream packet working set; compare important claims and preserve useful valid work.
4. Resolve critical evidence references and any contradictory or missing context. Expand retrieval beyond the initial slice when scope demands it.
5. Emit V/G records and revisions. A receiving role cannot mark its own unreviewed additions independently confirmed.
6. Accept only the eligible scoped output with the exact input-version set. Preserve rejected attempts.
7. Hand over the next task's obligations, reasoning and resolvable originals; never rely on the current conversation as the sole memory.

## Sufficiency failures to test

- Equation IDs survive but signs, units or conditions disappear.
- A hint is linked to a concept title that never explains its crucial operation.
- Source text survives but an essential diagram or option is dropped.
- A family label survives but conditional transfer axes are lost.
- A packet quotes a key without an independent solution.
- A reshared bundle loses the prerequisite hosted in another bundle.
- A receipt points to an old manuscript while a current manuscript has removed the bridge.
- An owner's elementary goal becomes competitive because of the default profile.
- A fresh agent sees the previous answer before its supposedly blind pass.

See [evaluation scenarios](acceptance-and-evaluation.md). No numerical packet-size limit is proposed as an evidence-backed optimum.
