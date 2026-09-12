#!/usr/bin/env python3
"""P-G promoted Physics PCK registry with an honest promotion state machine.

Every asset is a *candidate* until its review ledger justifies a promotion state.
The promotion state is DERIVED from the ledger, never declared, and this module
can only ever reach ``PROMOTED_PILOT``:

    CANDIDATE
      -> EVIDENCE_REVIEWED        machine/AI evidence review passed
      -> PROMOTED_PILOT           + AI_ASSISTED_REFERENCE_REVIEW pedagogical PASS
                                  + machine SCOPE_AUTHORITY_PASS
      -> PROMOTED_RELEASE         + real SUBJECT_EXPERT_PASS and PEDAGOGY_EXPERT_PASS

``AI_ASSISTED_REFERENCE_REVIEW`` is advisory. It is structurally incapable of
satisfying the SUBJECT or PEDAGOGICAL *release* stage: those require an
authorized human reviewer class plus an attestation reference. No such
attestation exists in this repository, so every asset below records
``SUBJECT_EXPERT_PASS`` / ``PEDAGOGY_EXPERT_PASS`` as ``PENDING`` and
``PROMOTED_RELEASE`` is unreachable here. That is the intended, honest state.

The asset content is subject-wide generic Physics PCK. Topic instances
(kinematics, dynamics, ...) enter as *data* through capability/problem-family
refs from P-C/P-D, never as new families or new schema.
"""
import copy, hashlib, json

SUBJECT = "PHYSICS"
REGISTRY_ID = "PHY-P-G-PCK-v1"

REVIEW_STAGES = ("EVIDENCE", "PEDAGOGICAL", "SUBJECT", "SCOPE")
REVIEW_CLASSES = (
    "AI_ASSISTED_REFERENCE_REVIEW",
    "MACHINE_AUTHORITY_CHECK",
    "SUBJECT_EXPERT_PASS",
    "PEDAGOGY_EXPERT_PASS",
    "ASSESSMENT_EXPERT_PASS",
)
# Review classes that a repository automated agent is allowed to issue.
AUTOMATED_ISSUABLE = {"AI_ASSISTED_REFERENCE_REVIEW", "MACHINE_AUTHORITY_CHECK"}
# Review classes that require an authorized human reviewer + attestation.
HUMAN_ONLY = {"SUBJECT_EXPERT_PASS", "PEDAGOGY_EXPERT_PASS", "ASSESSMENT_EXPERT_PASS"}
REVIEWER_CLASSES = {
    "AI_ASSISTED_REFERENCE_REVIEW": "REPOSITORY_AUTOMATED_AGENT",
    "MACHINE_AUTHORITY_CHECK": "MACHINE_AUTHORITY_CHECK",
    "SUBJECT_EXPERT_PASS": "AUTHORIZED_HUMAN_SUBJECT_EXPERT",
    "PEDAGOGY_EXPERT_PASS": "AUTHORIZED_HUMAN_PEDAGOGY_EXPERT",
    "ASSESSMENT_EXPERT_PASS": "AUTHORIZED_HUMAN_ASSESSMENT_EXPERT",
}
PROMOTION_STATES = ("CANDIDATE", "EVIDENCE_REVIEWED", "PROMOTED_PILOT", "PROMOTED_RELEASE")

PCK_FAMILIES = (
    "PHENOMENON_ANCHOR",
    "SYSTEM_FRAME_SIGN_SETUP",
    "STATE_REPRESENTATION_TRANSLATION",
    "MODEL_SELECTION_AND_VALIDITY",
    "PHASE_CONTINUITY_REASONING",
    "RELATION_RECONSTRUCTION",
    "GRAPH_SLOPE_AREA_DECODING",
    "VECTOR_COMPONENT_DECOMPOSITION",
    "WORKED_REASONING_SEQUENCE",
    "MISCONCEPTION_MINIMAL_CONTRAST",
    "FIRST_MOVE_DECISION_SUPPORT",
    "PHYSICAL_VERIFICATION",
    "TRANSFER_VARIATION",
)


def canonical(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(obj, field=None):
    x = copy.deepcopy(obj)
    if field:
        x.pop(field, None)
    return hashlib.sha256(canonical(x).encode("utf-8")).hexdigest()


def review(stage, review_class, state, basis, attestation_ref=None):
    """One review-ledger row.

    ``attestation_ref`` is required for human-only classes and must be absent
    for automated classes. A human-only row without an attestation can only be
    PENDING; it is never allowed to read PASS.
    """
    return {
        "stage": stage,
        "review_class": review_class,
        "reviewer_authority_class": REVIEWER_CLASSES[review_class],
        "state": state,
        "basis": basis,
        "attestation_ref": attestation_ref,
    }


def default_ledger(family):
    """The only ledger this repository can honestly produce today."""
    return [
        review(
            "EVIDENCE",
            "AI_ASSISTED_REFERENCE_REVIEW",
            "PASS",
            "Asset content was checked against the P-D reasoning-role and "
            "verification-route vocabulary and the P-F treatment policy job list. "
            "Advisory only.",
        ),
        review(
            "SCOPE",
            "MACHINE_AUTHORITY_CHECK",
            "PASS",
            "Asset declares no canonical Physics beyond capability, physical-model, "
            "law and problem-family refs supplied by the P-C/P-D authorities.",
        ),
        review(
            "PEDAGOGICAL",
            "AI_ASSISTED_REFERENCE_REVIEW",
            "PASS",
            "SEE / REALIZE / UNDERSTAND phases are present and ordered, a "
            "reconstruction route exists before any stated relation, and no "
            "naked equation is offered as concept teaching. Advisory only; this "
            "does not substitute for PEDAGOGY_EXPERT_PASS.",
        ),
        review(
            "PEDAGOGICAL",
            "PEDAGOGY_EXPERT_PASS",
            "PENDING",
            "No authorized human pedagogy reviewer has attested to this asset.",
        ),
        review(
            "SUBJECT",
            "SUBJECT_EXPERT_PASS",
            "PENDING",
            "No authorized human Physics subject reviewer has attested to this asset.",
        ),
    ]


def derive_promotion_state(ledger):
    """Promotion state is computed from the ledger. Never declared."""
    def passed(stage, classes):
        return any(
            r["stage"] == stage and r["review_class"] in classes and r["state"] == "PASS"
            for r in ledger
        )

    if not passed("EVIDENCE", AUTOMATED_ISSUABLE | HUMAN_ONLY):
        return "CANDIDATE"
    pilot = passed("PEDAGOGICAL", AUTOMATED_ISSUABLE | HUMAN_ONLY) and passed(
        "SCOPE", AUTOMATED_ISSUABLE | HUMAN_ONLY
    )
    if not pilot:
        return "EVIDENCE_REVIEWED"
    if passed("SUBJECT", {"SUBJECT_EXPERT_PASS"}) and passed(
        "PEDAGOGICAL", {"PEDAGOGY_EXPERT_PASS"}
    ):
        return "PROMOTED_RELEASE"
    return "PROMOTED_PILOT"


def promotion_authority(ledger):
    state = derive_promotion_state(ledger)

    def state_of(stage, review_class):
        rows = [r for r in ledger if r["stage"] == stage and r["review_class"] == review_class]
        return rows[0]["state"] if rows else "ABSENT"

    return {
        "promotion_state": state,
        "authority_class": "REPOSITORY_PROGRAMME_PILOT_AUTHORITY",
        "evidence_review_state": state_of("EVIDENCE", "AI_ASSISTED_REFERENCE_REVIEW"),
        "pedagogical_ai_review_state": state_of("PEDAGOGICAL", "AI_ASSISTED_REFERENCE_REVIEW"),
        "scope_review_state": state_of("SCOPE", "MACHINE_AUTHORITY_CHECK"),
        "subject_expert_release_state": "GRANTED"
        if state_of("SUBJECT", "SUBJECT_EXPERT_PASS") == "PASS"
        else "NOT_GRANTED",
        "pedagogy_expert_release_state": "GRANTED"
        if state_of("PEDAGOGICAL", "PEDAGOGY_EXPERT_PASS") == "PASS"
        else "NOT_GRANTED",
        "final_product_release_blocked": state != "PROMOTED_RELEASE",
    }


def asset(
    family,
    *,
    see,
    realize,
    understand,
    physical_anchor,
    frame_sign_cue,
    representation_path,
    ordinary_language_bridge,
    model_rule_condition_cue,
    reconstruction_route,
    common_wrong_model,
    minimal_contrast,
    repair_route,
    verification_method,
    transfer_family,
    capability_refs=(),
    topic_scope_refs=(),
):
    ledger = default_ledger(family)
    row = {
        "asset_id": "PHY-PCK-" + family.replace("_", "-"),
        "family": family,
        "capability_refs": sorted(capability_refs),
        "topic_scope_refs": sorted(topic_scope_refs),
        "see_phase": see,
        "realize_phase": realize,
        "understand_phase": understand,
        "physical_anchor": physical_anchor,
        "system_frame_sign_cue": frame_sign_cue,
        "representation_path": list(representation_path),
        "ordinary_language_bridge": ordinary_language_bridge,
        "model_rule_condition_cue": model_rule_condition_cue,
        "reconstruction_route": list(reconstruction_route),
        "common_wrong_model": common_wrong_model,
        "minimal_contrast": minimal_contrast,
        "repair_route": list(repair_route),
        "verification_method": list(verification_method),
        "transfer_family": transfer_family,
        "raw_mature_reference_used": False,
        "review_ledger": ledger,
        "promotion_authority": promotion_authority(ledger),
        "asset_digest": "",
    }
    row["asset_digest"] = digest(row, "asset_digest")
    return row


def _assets():
    return [
        asset(
            "PHENOMENON_ANCHOR",
            see="Look at what physically happens in the situation before any symbol is written.",
            realize="Say the motion or interaction out loud as a sequence of physical events.",
            understand="Only a described physical situation can be modelled; the description fixes what the symbols will mean.",
            physical_anchor="Start from the observable situation: what moves, what stays put, and what changes between the start and the end.",
            frame_sign_cue="Name the moving object before naming any direction.",
            representation_path=["PHENOMENON", "DESCRIBED_EVENTS", "STATE_LIST"],
            ordinary_language_bridge="Describe the situation in ordinary words first: what happens, in what order, and what you are being asked about.",
            model_rule_condition_cue="A physical description is not yet a model; it is what the model has to match.",
            reconstruction_route=[
                "Name the object whose motion or state is being asked about.",
                "List the physical events in the order they happen.",
                "Mark which quantity the question actually asks for.",
            ],
            common_wrong_model="Jumping straight to a remembered formula because the numbers look familiar.",
            minimal_contrast="Same numbers, different physical situation: the remembered formula stops being the right one.",
            repair_route=[
                "Cover the numbers and re-describe the physical situation.",
                "Check whether the described events match the assumptions of the remembered relation.",
                "Choose the relation only after the description is fixed.",
            ],
            verification_method=["VERIFY_AGAINST_DESCRIBED_SITUATION"],
            transfer_family="SAME_PHYSICS_DIFFERENT_STORY",
        ),
        asset(
            "SYSTEM_FRAME_SIGN_SETUP",
            see="Look at where the origin is and which direction has been called positive.",
            realize="Draw the axis and the positive direction before substituting any number.",
            understand="A signed quantity has no meaning until the frame and sign convention are fixed; changing the convention changes the signs, not the physics.",
            physical_anchor="Pick a fixed point to measure from and one direction to call positive, then keep both for the whole problem.",
            frame_sign_cue="State the origin, the positive direction, and which object the frame is attached to.",
            representation_path=["SIGNED_AXIS", "SYSTEM_BOUNDARY", "SIGNED_STATE_TABLE"],
            ordinary_language_bridge="Decide once which way is positive; after that, a negative answer means the opposite direction, not a mistake.",
            model_rule_condition_cue="Every displacement, velocity and acceleration in this problem is signed with respect to the one declared positive direction.",
            reconstruction_route=[
                "Choose and mark the origin.",
                "Choose and mark the positive direction on the axis.",
                "Rewrite every given quantity with the sign that convention forces.",
            ],
            common_wrong_model="Treating downward motion as positive in one line and negative in the next.",
            minimal_contrast="The same fall written with upward-positive and with downward-positive: the numbers change sign, the physical outcome does not.",
            repair_route=[
                "Re-declare the positive direction explicitly.",
                "Re-sign every given quantity in one pass.",
                "Re-read the result and translate the sign back into a direction.",
            ],
            verification_method=["VERIFY_SIGN_AGAINST_DECLARED_FRAME"],
            transfer_family="SIGN_FRAME_DISCRIMINATION",
        ),
        asset(
            "STATE_REPRESENTATION_TRANSLATION",
            see="Look at the same physical state written as words, as a diagram and as a row of symbols.",
            realize="Fill the state table from the description, then read the diagram back out of the table.",
            understand="A representation carries the state, it does not add to it; anything not in the state is not available to use.",
            physical_anchor="A state is a snapshot: at one instant, where the object is, how fast it is going, and which way.",
            frame_sign_cue="Every entry in the state table carries the sign of the declared positive direction.",
            representation_path=["DESCRIBED_STATE", "STATE_TABLE", "DIAGRAM", "SYMBOLIC_RELATION"],
            ordinary_language_bridge="Write down what is known at the start and what is known at the end; the gap between the two rows is what you have to find.",
            model_rule_condition_cue="Translation between representations must preserve every state variable and its sign.",
            reconstruction_route=[
                "Build a two-row state table for the start state and the end state.",
                "Enter every known quantity with its unit and sign.",
                "Mark the unknown, and check the same state appears in the diagram.",
            ],
            common_wrong_model="Reading a number off a diagram without checking which state it belongs to.",
            minimal_contrast="The same number placed in the start row and in the end row: two different physical claims.",
            repair_route=[
                "Point to the instant each number describes.",
                "Move each number into the row for that instant.",
                "Re-read the diagram against the corrected table.",
            ],
            verification_method=["VERIFY_STATE_TABLE_CONSISTENCY", "VERIFY_DIMENSIONS"],
            transfer_family="SAME_CONCEPT_NEW_REPRESENTATION",
        ),
        asset(
            "MODEL_SELECTION_AND_VALIDITY",
            see="Look at the conditions the situation actually states before choosing a model.",
            realize="Check each assumption of the candidate model against a stated condition.",
            understand="A relation is only valid while its assumptions hold; outside them it gives a confident wrong answer.",
            physical_anchor="Ask what is being assumed constant, and whether the situation says it is.",
            frame_sign_cue="Model validity is checked in the same frame the relation will be used in.",
            representation_path=["STATED_CONDITIONS", "ASSUMPTION_CHECKLIST", "SELECTED_RELATION"],
            ordinary_language_bridge="Before using a relation, say in words what it assumes and point to where the question says that is true.",
            model_rule_condition_cue="Name the model, list its assumptions, and mark each assumption as stated, implied or absent.",
            reconstruction_route=[
                "List the candidate physical models for this situation.",
                "Write each model's assumptions as a checklist.",
                "Reject any model whose assumption is contradicted by a stated condition.",
            ],
            common_wrong_model="Using a constant-rate relation for a situation that changes rate part-way through.",
            minimal_contrast="One situation that satisfies the assumption and one that violates it, with the same given numbers.",
            repair_route=[
                "Re-read the situation for any change in the assumed-constant quantity.",
                "Split the situation where the assumption breaks.",
                "Re-select a model that is valid on each part.",
            ],
            verification_method=["VERIFY_MODEL_ASSUMPTIONS_HOLD"],
            transfer_family="MODEL_VALIDITY_HIDDEN_CONDITION",
        ),
        asset(
            "PHASE_CONTINUITY_REASONING",
            see="Look at where the motion changes character, and what is shared across that boundary.",
            realize="Draw a phase strip and mark the quantity that must carry over unchanged.",
            understand="At a phase boundary the state is continuous even when the rate is not; the end state of one phase is the start state of the next.",
            physical_anchor="The object does not teleport: position and velocity at the instant of the change belong to both phases.",
            frame_sign_cue="Keep one frame and one sign convention across every phase.",
            representation_path=["PHASE_STRIP", "PER_PHASE_STATE_TABLE", "CONTINUITY_LINK"],
            ordinary_language_bridge="Solve one stage at a time, and hand the end of each stage to the start of the next.",
            model_rule_condition_cue="Each phase gets its own relation; the shared boundary state links them.",
            reconstruction_route=[
                "Mark every instant at which the motion changes character.",
                "Give each phase its own state table and relation.",
                "Copy the boundary state forward as the next phase's start state.",
            ],
            common_wrong_model="Applying a single whole-journey relation across a change of acceleration.",
            minimal_contrast="One-phase and two-phase versions of the same journey giving different results from the same total time.",
            repair_route=[
                "Identify the instant the rate changes.",
                "Recompute the boundary state from the first phase.",
                "Restart the second phase from that state rather than from the original start.",
            ],
            verification_method=["VERIFY_PHASE_CONTINUITY", "VERIFY_TOTALS_SUM_OVER_PHASES"],
            transfer_family="MULTIPHASE_STATE_PROPAGATION",
        ),
        asset(
            "RELATION_RECONSTRUCTION",
            see="Look at which state variables a relation connects, and which one is missing from it.",
            realize="Rebuild the relation from the meaning of the quantities rather than recalling its letters.",
            understand="A relation is a statement about states; choosing one means choosing which variable you are willing not to know.",
            physical_anchor="Each standard relation links a specific set of state variables and leaves exactly one out.",
            frame_sign_cue="Substitute signed values, not magnitudes, into the reconstructed relation.",
            representation_path=["STATE_TABLE", "VARIABLE_LINK_MAP", "SELECTED_RELATION"],
            ordinary_language_bridge="List what you know and what you want; pick the relation that contains exactly those and nothing you cannot get.",
            model_rule_condition_cue="State the relation, the variables it links, and the variable it deliberately omits.",
            reconstruction_route=[
                "Mark the known and wanted state variables in the state table.",
                "Find the relation whose variable set matches that marking.",
                "Write the relation out before substituting anything.",
            ],
            common_wrong_model="Choosing a relation by how familiar it looks rather than by which variables it links.",
            minimal_contrast="Two relations that share three variables and differ in the fourth, applied to the same state table.",
            repair_route=[
                "Rewrite the known/wanted marking.",
                "Re-derive which variable must be absent.",
                "Re-select on that basis and re-substitute.",
            ],
            verification_method=["VERIFY_DIMENSIONS", "VERIFY_RELATION_VARIABLE_MATCH"],
            transfer_family="SAME_MODEL_DIFFERENT_STORY",
        ),
        asset(
            "GRAPH_SLOPE_AREA_DECODING",
            see="Look at what each axis measures before reading any feature of the curve.",
            realize="Decode slope and area separately and say what each one is physically.",
            understand="On a graph of a state variable against time, slope is a rate and signed area is a change; which one you need is fixed by the question, not by the picture.",
            physical_anchor="A graph is a record of the motion, not a picture of the path.",
            frame_sign_cue="Area below the time axis is negative and subtracts from the total change.",
            representation_path=["SOURCE_GRAPH", "AXIS_MEANING", "SLOPE_OR_AREA_DECODE", "STATE_TABLE"],
            ordinary_language_bridge="Ask first: do I need how fast this is changing, or how much it has changed in total?",
            model_rule_condition_cue="Slope gives the rate of the plotted quantity; signed area under the curve gives the change in the quantity whose rate is plotted.",
            reconstruction_route=[
                "Read and state both axis labels and units.",
                "Decide whether the question asks for a rate or an accumulated change.",
                "Extract slope or signed area accordingly and put it into the state table.",
            ],
            common_wrong_model="Reading a velocity-time graph as if it were a picture of the path travelled.",
            minimal_contrast="The same plotted line read as a position-time graph and as a velocity-time graph.",
            repair_route=[
                "Re-read the vertical-axis label out loud.",
                "Re-decide between slope and area on that basis.",
                "Re-extract the value and re-check its unit.",
            ],
            verification_method=["VERIFY_GRAPH_AXIS_MEANING", "VERIFY_DIMENSIONS"],
            transfer_family="MIXED_GRAPH_MODEL_SELECTION",
        ),
        asset(
            "VECTOR_COMPONENT_DECOMPOSITION",
            see="Look at the direction of each vector quantity relative to the declared axis.",
            realize="Resolve each vector onto the axis and keep the sign the direction forces.",
            understand="Vector quantities combine by direction, not by size; along one axis that becomes signed addition.",
            physical_anchor="Two motions in opposite directions partly cancel; two in the same direction add.",
            frame_sign_cue="Resolve every vector onto the one declared positive direction before combining.",
            representation_path=["MOTION_VECTOR_DIAGRAM", "AXIS_PROJECTION", "SIGNED_STATE_TABLE"],
            ordinary_language_bridge="Draw the arrows first, then write each arrow as a signed number along your axis.",
            model_rule_condition_cue="Only components along the same axis may be added; relative quantities are differences of components.",
            reconstruction_route=[
                "Draw each vector quantity as an arrow with its direction.",
                "Project each arrow onto the declared axis and record its sign.",
                "Combine only the signed components, never the raw magnitudes.",
            ],
            common_wrong_model="Adding magnitudes of oppositely directed quantities.",
            minimal_contrast="The same two speeds combined as same-direction and as opposite-direction motion.",
            repair_route=[
                "Redraw the arrows with their real directions.",
                "Re-sign both components.",
                "Re-combine and re-read the direction of the result.",
            ],
            verification_method=["VERIFY_DIRECTION_OF_RESULT", "VERIFY_SIGN_AGAINST_DECLARED_FRAME"],
            transfer_family="SIGN_FRAME_DISCRIMINATION",
        ),
        asset(
            "WORKED_REASONING_SEQUENCE",
            see="Look at one complete solution in which every line says why, not just what.",
            realize="Re-run the same route on a new instance with the reasons still visible.",
            understand="A solution is a chain of justified moves; a chain with a missing justification is not a solution.",
            physical_anchor="Every line of work answers a question the previous line raised.",
            frame_sign_cue="The declared frame and signs are carried unchanged through every line.",
            representation_path=["STATE_TABLE", "JUSTIFIED_STEP_STACK", "RESULT_INTERPRETATION"],
            ordinary_language_bridge="Say what you are doing and why before you do it; the arithmetic is the last part.",
            model_rule_condition_cue="Each step names its reasoning role: read, define, extract, select, represent, choose, solve, check, interpret.",
            reconstruction_route=[
                "Write the reasoning role of each step before the step itself.",
                "Execute the step.",
                "State what the step established that the next step needs.",
            ],
            common_wrong_model="Presenting a correct final number as if it were the reasoning.",
            minimal_contrast="Two solutions with the same final number, one of which skips model selection.",
            repair_route=[
                "Re-label each existing line with its reasoning role.",
                "Insert the missing role.",
                "Re-check that the result still follows.",
            ],
            verification_method=["VERIFY_EACH_STEP_HAS_A_REASON", "VERIFY_PHYSICAL_PLAUSIBILITY"],
            transfer_family="SAME_MODEL_DIFFERENT_STORY",
        ),
        asset(
            "MISCONCEPTION_MINIMAL_CONTRAST",
            see="Look at two situations that differ in exactly one decisive physical feature.",
            realize="Name the one feature that changes the answer, and predict both outcomes before checking.",
            understand="A wrong model is usually right somewhere; the contrast shows exactly where it stops being right.",
            physical_anchor="Hold everything constant except the feature under test.",
            frame_sign_cue="Both cases in a contrast use the identical frame and sign convention.",
            representation_path=["CASE_A", "CASE_B", "DECISIVE_FEATURE_MARK"],
            ordinary_language_bridge="If these two look the same to you, this is the difference that matters.",
            model_rule_condition_cue="A contrast is valid only when exactly one feature differs between the two cases.",
            reconstruction_route=[
                "State the shortcut model being tested.",
                "Build the case where it works and the case where it fails.",
                "Mark the single feature that separates them.",
            ],
            common_wrong_model="Believing a shortcut is general because it worked on the cases seen so far.",
            minimal_contrast="A case pair in which the shortcut and the correct model give different answers.",
            repair_route=[
                "Predict both cases with the shortcut.",
                "Work both cases with the correct model.",
                "Say in one sentence which feature the shortcut ignores.",
            ],
            verification_method=["VERIFY_CONTRAST_ISOLATES_ONE_FEATURE"],
            transfer_family="MIXED_MODEL_DISCRIMINATION",
        ),
        asset(
            "FIRST_MOVE_DECISION_SUPPORT",
            see="Look at what is already fixed by the question before deciding anything.",
            realize="Make the first physically meaningful move and say why it is first.",
            understand="Most stalls are a missing first move, not a missing formula.",
            physical_anchor="The first move is always to fix the object, the frame and the states.",
            frame_sign_cue="Fixing the frame and the positive direction is itself the first move.",
            representation_path=["GIVEN_MARKUP", "FIRST_MOVE_CUE", "STATE_TABLE"],
            ordinary_language_bridge="If you are stuck, set up the axis and the two state rows; the next move usually becomes obvious.",
            model_rule_condition_cue="A decision cue may reorder the available moves but may not add Physics beyond the active study model.",
            reconstruction_route=[
                "Mark the object and the instants the question refers to.",
                "Fix the frame and the positive direction.",
                "Fill what is known into the start and end states.",
            ],
            common_wrong_model="Searching for a formula before the states exist.",
            minimal_contrast="The same question attempted with and without the state table set up first.",
            repair_route=[
                "Stop and set up the axis.",
                "Fill both state rows.",
                "Re-read the question for the wanted quantity.",
            ],
            verification_method=["VERIFY_FIRST_MOVE_IS_SUPPORTED_BY_GIVENS"],
            transfer_family="SAME_PHYSICS_DIFFERENT_STORY",
        ),
        asset(
            "PHYSICAL_VERIFICATION",
            see="Look at the result as a physical claim, not as a number.",
            realize="Run an independent check that could actually fail.",
            understand="A check that cannot fail is not a check; verification must be able to reject the answer.",
            physical_anchor="Ask whether the size, sign and direction of the answer are physically possible here.",
            frame_sign_cue="Translate the sign of the result back into a direction before accepting it.",
            representation_path=["RESULT", "INDEPENDENT_CHECK", "ACCEPT_OR_REJECT"],
            ordinary_language_bridge="Say what the answer means physically, then test that meaning against the situation.",
            model_rule_condition_cue="The verification route must be independent of the route that produced the answer.",
            reconstruction_route=[
                "State the result as a physical sentence with direction and unit.",
                "Choose a check that does not reuse the solving relation.",
                "Accept the result only if the check passes.",
            ],
            common_wrong_model="Re-reading the same substitution and calling it a check.",
            minimal_contrast="A dependent re-check and an independent check applied to a deliberately wrong answer.",
            repair_route=[
                "Identify which relation produced the answer.",
                "Pick a different route to the same quantity.",
                "Compare and resolve any disagreement.",
            ],
            verification_method=["VERIFY_DIMENSIONS", "VERIFY_PHYSICAL_PLAUSIBILITY"],
            transfer_family="PHYSICAL_VERIFICATION_WITHOUT_PROMPTING",
        ),
        asset(
            "TRANSFER_VARIATION",
            see="Look at the same physical structure wearing a different surface story.",
            realize="Map the new surface onto the structure you already reconstructed.",
            understand="Transfer is recognising structure under an unfamiliar surface, not recalling a solved problem.",
            physical_anchor="Change the story, keep the physics; change the physics, keep the story.",
            frame_sign_cue="A new surface still requires the frame and sign convention to be re-declared.",
            representation_path=["ORIGINAL_STRUCTURE", "SURFACE_CHANGE", "REMAPPED_STATE_TABLE"],
            ordinary_language_bridge="Ask what is the same as the worked example and what genuinely changed.",
            model_rule_condition_cue="A transfer variation keeps the problem family and changes the surface or the representation.",
            reconstruction_route=[
                "Name the problem family of the worked example.",
                "Change one of surface story or representation, not the family.",
                "Re-derive the state table under the new surface.",
            ],
            common_wrong_model="Pattern-matching a remembered problem instead of the structure.",
            minimal_contrast="Same surface with a different family, and same family with a different surface.",
            repair_route=[
                "Strip the surface wording back to states and relations.",
                "Compare those with the worked example's structure.",
                "Re-solve from the structure.",
            ],
            verification_method=["VERIFY_PHYSICAL_PLAUSIBILITY"],
            transfer_family="FAR_TRANSFER_NEW_CONTEXT",
        ),
    ]


def build_registry():
    assets = _assets()
    registry = {
        "registry_id": REGISTRY_ID,
        "schema_version": "1.0.0",
        "subject": SUBJECT,
        "pedagogy_model": "SEE_REALIZE_UNDERSTAND",
        "review_stages": list(REVIEW_STAGES),
        "review_classes": list(REVIEW_CLASSES),
        "automated_issuable_review_classes": sorted(AUTOMATED_ISSUABLE),
        "human_only_review_classes": sorted(HUMAN_ONLY),
        "promotion_states": list(PROMOTION_STATES),
        "families": list(PCK_FAMILIES),
        "assets": assets,
        "registry_digest": "",
    }
    registry["registry_digest"] = digest(registry, "registry_digest")
    return registry


if __name__ == "__main__":
    print(json.dumps(build_registry(), ensure_ascii=False, indent=2, sort_keys=True))
