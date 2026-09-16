# Research evidence and architectural implications

Status: RESEARCH_REVIEW / ADVISORY. Access date: 2026-09-13. This is a focused investigation of the approved design questions, not a systematic review or a claim of evaluated system performance.

The owner requirements govern product goals. Research informs how to meet them. None of the sources below establishes that 20/50/80 percent, one inferential move, three subtopics, a fixed picture count, or a particular agent profile is an optimal universal rule.

## Evidence ledger

### P01 — Instruction, retrieval and explanatory questions

Pashler et al. (2007), [Organizing Instruction and Study to Improve Student Learning, IES/WWC](https://ies.ed.gov/ncee/wwc/practiceguide/1). Access: official recommendations page.

The guide recommends spacing, alternating worked solutions and problem solving, combining graphics with verbal explanation, connecting concrete and abstract representations, retrieval and explanatory questions. Evidence strength differs by recommendation.

Design implication: Core1A needs meaningful connections and explanatory prompts; Core2A may include retrieval and revisits when the owner requests them. This does not require a live student-tracking platform or one compulsory page sequence.

Limit: this guide does not validate the proposed agent architecture, prescribed packet fields, or a single pacing schedule for all children.

### P02 — Explanations tied to principles

Chi, Bassok, Lewis, Reimann and Glaser (1989), [Self-Explanations: How Students Study and Use Examples in Learning to Solve Problems](https://doi.org/10.1207/s15516709cog1302_1). Access: publisher abstract.

The study analyzes students' explanations while studying mechanics examples. Stronger learners connected steps to principles and conditions; weaker learners depended more heavily on examples.

Design implication: store what justifies a teaching transition and ask the child to explain a decisive step. A numbered list of algebraic lines does not establish that this connection is present.

Limit: an association observed in these learners is not proof that merely filling a why-step field improves every learner's understanding.

### P03 — Function and interpretation of multiple representations

Ainsworth (2006), [DeFT: A conceptual framework for considering learning with multiple representations](https://nottingham-repository.worktribe.com/output/23577631), [DOI](https://doi.org/10.1016/j.learninstruc.2006.03.001). Access: author-institution repository abstract; full-text retrieval was unavailable.

DeFT considers representation design, its learning function and the tasks the learner must perform with it. Multiple representations can help, but their benefits are not automatic.

Design implication: a representation packet must state the intended noticing, reading conventions, connection to other representations, and potential misinterpretations. Candidate selection should consider these obligations, not visual count.

Limit: this conceptual framework does not supply numerical candidate scores or a universal picture-first order.

### P04 — Support depends on relevant experience

Kalyuga, Ayres, Chandler and Sweller (2003), [The Expertise Reversal Effect](https://doi.org/10.1207/S15326985EP3801_4). Access: publisher and author-institution abstract records; full text unavailable.

The review examines interactions between instructional techniques and learner experience.

Design implication: maintain capability-specific assumptions/evidence and make optional compression explicit. Owner-requested detailed assimilation must remain available; a broad high-knowledge label cannot automatically suppress it.

Limit: no percentage cutoffs or mandatory treatment table are derived from this source.

### P05 — Transition from examples to independent work

Renkl and Atkinson (2003), [Structuring the Transition From Example Study to Problem Solving in Cognitive Skill Acquisition](https://doi.org/10.1207/S15326985EP3801_3). Access: publisher abstract.

The paper proposes progressively integrating problem-solving elements into example study.

Design implication: Core1A can identify exactly which support is removed and which decision becomes the learner's responsibility. Core2A can continue that progression when it matches the owner's goal.

Limit: fading is a design option with contextual support, not a guarantee of broad competitive transfer or a reason to force an independent attempt before every elementary demonstration.

### P06 — Chemistry requires explicit representational interpretation

Taber (2013), [Revisiting the chemistry triplet](https://pubs.rsc.org/is/content/articlehtml/2013/rp/c3rp00012e), DOI 10.1039/C3RP00012E. Access: full publisher HTML, especially sections on the symbolic domain and teaching implications.

The article examines macroscopic and submicroscopic conceptual knowledge and the symbolic resources used to express them. It cautions against treating the familiar triangle as a single uncontested ontology.

Design implication: Chemistry packets should state whether a symbol denotes particles, substance quantities, charge, or another feature, and teach transitions explicitly. A reaction equation and a reaction mechanism must have distinguishable explanatory roles.

Limit: the article supports a subject-specific account; it does not prescribe three simultaneous pictures or an identical representation sequence for every topic.

### A01 — Long context does not guarantee successful use

Liu et al. (2024), [Lost in the Middle: How Language Models Use Long Contexts](https://aclanthology.org/2024.tacl-1.9/), DOI 10.1162/tacl_a_00638. Access: proceedings abstract and study description.

In the models and retrieval tasks studied, use of relevant information varied with its position in a long context.

Design implication: test packet sufficiency and evidence retrieval with relevant details in different positions. A shared source manifest plus a scoped working set is a candidate design worth testing.

Limit: the paper establishes neither the optimal context length for current models nor the owner's three-subtopic limit. It does not prove that this proposed packet architecture outperforms full-context operation.

### A02 — Self-review needs an actual verification basis

Huang et al. (2024), [Large Language Models Cannot Self-Correct Reasoning Yet](https://arxiv.org/html/2310.01798v2). Access: full HTML, including limitations and experimental-design discussion.

The paper studies intrinsic correction without external feedback and reports limitations on reasoning tasks. It also stresses fair comparison of prompt quality and inference cost.

Design implication: fresh instances and self-critique must not substitute for source checking, independent solutions and explicit falsifiers. Compare relay variants using equal task information and comparable budgets.

Limit: findings concern the models, tasks and conditions studied. They do not establish that all contemporary models fail at self-correction, or that profile changes guarantee independence.

### A03 — Agent failures include coordination and verification

Cemri et al. (2025), [Why Do Multi-Agent LLM Systems Fail?](https://arxiv.org/abs/2503.13657v3). Access: version-3 abstract; the earlier attempted v4 URL was invalid and is not evidence.

The reported taxonomy groups observed failures under system design, inter-agent misalignment and task verification.

Design implication: test role assignment, incomplete handoffs, conflicting task interpretations and false completion separately from subject-answer correctness.

Limit: these observations motivate failure scenarios. They do not prove the four-Core relay, a Governor, or any profile-selection threshold effective.

### A04 — Provenance distinguishes artifacts, activities and agents

W3C (2013), [PROV-DM: The PROV Data Model](https://www.w3.org/TR/prov-dm/). Access: Recommendation.

PROV supplies concepts for entities, activities, agents and derivations.

Design implication: distinguish a packet's content/version, its producing activity and its agent instance/profile. Record derivation relationships and exact source/artifact references.

Limit: provenance explains origin and transformation; it does not certify scientific correctness or teaching quality. Adoption of the complete PROV serialization is not required by this proposal.

### A05 — Recovery requires durable execution history

Temporal, [Events and Event History](https://github.com/temporalio/documentation/blob/main/docs/encyclopedia/workflow/workflow-execution/event.mdx). Access: official source documentation, sections on events, history and side effects.

The documentation describes persistent events for workflow recovery and recording nondeterministic results for later replay.

Design implication: record model outputs and accepted state transitions; reuse accepted outputs on recovery rather than expecting another model call to reproduce identical prose.

Limit: this is a software pattern, not a recommendation to install Temporal. The project still needs its own atomic commit, duplicate-delivery and stale-work policies.

## Research disposition

| Question | Finding | Remaining evidence |
|---|---|---|
| Can decomposition and representations be made explicit? | Yes, as reviewable teaching decisions and outputs. | Determine whether the chosen decomposition actually works on representative topics. |
| Can schema validity certify intellectual depth? | No such guarantee is established. | Subject, pedagogy and rendered-artifact review are distinct. |
| Must Core1A always begin with a picture? | No universal order is supported here. | Select a representation for the named cognitive need and owner requirement. |
| Should owner goals be inferred from a knowledge percentage? | No; owner instruction independently supplies the goal. | Validate goal preservation under contrasting scenarios. |
| Does a fresh instance guarantee independent correctness? | No. | Evaluate actual information separation, source checking and error detection. |
| Can a useful packet replace all source access? | Not defensibly under this proposal. | Retain resolvable original evidence and test retrieval omissions. |
| Can every production choice be predetermined? | Control flow can be deterministic; content decisions still require constrained judgment. | Record alternatives, reasons, uncertainty and review evidence. |
| Does adding agents necessarily help? | The evidence does not justify that assumption. | Compare quality, error propagation, rework, cost and latency against strong baselines. |

## Deliberate limits of this review

No learner experiment, live multi-agent benchmark, model-ranking exercise, complete examination-archive study or production runtime evaluation has been performed. Existing research does not remove those future evaluation needs.

An ETS evidence-centered-design report was located, but the accessible page supplied limited abstract content and the attempted full-text URL failed. No detailed claim from that report is used here.

All proposal-specific rules in the architecture, packet and lifecycle documents are explicitly design recommendations unless marked OWNER_REQUIREMENT. They are not findings proved by these papers.
