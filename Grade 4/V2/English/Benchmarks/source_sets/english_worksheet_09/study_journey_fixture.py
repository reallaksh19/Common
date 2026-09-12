"""Teach-first document journey for Grade-4 English Worksheet 09.

This fixture deliberately expands source questions into required learning before
publication. Every source-coverage claim points to real TeachingBlock IDs.
"""
from __future__ import annotations

from typing import Any, Dict, Iterable

REF_I = "ENG-G4-WS09:I"
REF_II = "ENG-G4-WS09:II"
REF_III = "ENG-G4-WS09:III"
REF_IV = "ENG-G4-WS09:IV"
REF_Q1 = "ENG-G4-WS09:V:Q1"
REF_Q2 = "ENG-G4-WS09:V:Q2"
REF_Q3 = "ENG-G4-WS09:V:Q3"
REF_Q4 = "ENG-G4-WS09:V:Q4"
ALL_REFS = [REF_I, REF_II, REF_III, REF_IV, REF_Q1, REF_Q2, REF_Q3, REF_Q4]
POEM_REFS = [REF_Q1, REF_Q2, REF_Q3, REF_Q4]


def B(
    block_id: str,
    block_type: str,
    title: str,
    body: str,
    refs: Iterable[str],
    *,
    audience: str = "STUDENT",
    visibility: str = "HIDDEN",
    prompt: str = "",
    solution: str = "",
    representation: str | None = None,
    support: str = "NONE",
    provenance: str = "PEDAGOGICAL_BRIDGE",
    params: dict[str, Any] | None = None,
) -> Dict[str, Any]:
    out: Dict[str, Any] = {
        "block_id": block_id,
        "block_type": block_type,
        "title": title,
        "body": body,
        "source_refs": list(refs),
        "audience": audience,
        "answer_visibility": visibility,
        "support_level": support,
        "provenance": provenance,
    }
    if prompt:
        out["learner_prompt"] = prompt
    if solution:
        out["solution_text"] = solution
    if representation:
        out["representation_ref"] = representation
    if params:
        out["semantic_params"] = dict(params)
    return out


def C(source_ref: str, objects: list[str], teach: list[str], model: list[str], practice: list[str], hints: list[str], verify: list[str], answer: list[str]) -> Dict[str, Any]:
    return {
        "source_ref": source_ref,
        "learning_object_refs": objects,
        "teach_block_refs": teach,
        "model_block_refs": model,
        "practice_block_refs": practice,
        "hint_block_refs": hints,
        "verify_block_refs": verify,
        "answer_or_rubric_block_refs": answer,
    }


def build_study_journey() -> Dict[str, Any]:
    learning_objects = [
        {
            "learning_object_id": "LO-ADJ-FAMILIES",
            "title": "Adjectives and the seven worksheet families",
            "learning_goal": "Identify adjectives and classify them using the worksheet's own seven-category questions instead of guessing.",
            "source_refs": [REF_I],
            "capability_refs": ["ENG-ADJ-IDENTIFY", "ENG-ADJ-CLASSIFY-SOURCE-MODEL"],
            "prerequisite_refs": [],
            "misconception_targets": ["ORIGIN_MATERIAL_CONFUSION", "SIZE_SHAPE_CONFUSION", "OPINION_FACT_CONFUSION"],
            "blocks": [
                B("ADJ-CONCEPT", "CONCEPT", "What an adjective does", "An adjective adds information about a noun. Start with the noun, then ask what each describing word tells you.", [REF_I], representation="NOUN_PHRASE_BUILDER"),
                B("ADJ-SOURCE-RULE", "SOURCE_RULE", "The seven worksheet families", "Use the printed source questions: opinion—what do I think or feel; size—how big/small/wide; age—how old/new; shape—what shape; colour—what colour; origin—where from; material—made of.", [REF_I], provenance="SOURCE_DERIVED", representation="ADJECTIVE_FAMILY_CARDS"),
                B("ADJ-MODEL", "WORKED_EXAMPLE", "Worked sort", "Classify by the question the word answers, not by memorising a column.", [REF_I], visibility="WORKED_EXAMPLE", solution="Swedish → Origin because it answers 'Where from?'; metal → Material because it answers 'Made of?'; wide → Size because it tells how wide/big; round → Shape."),
                B("ADJ-CONTRAST", "CONTRAST", "Do not mix these up", "Compare Swedish/wooden and wide/round. One contrast separates origin from material; the other separates size from shape.", [REF_I], representation="CONTRAST_PAIR", params={"contrasts": [["Swedish", "wooden"], ["wide", "round"]]}),
                B("ADJ-GUIDED", "GUIDED_PRACTICE", "Sort the source words", "Use the category questions and sort the visible worksheet words.", [REF_I], visibility="PARTIAL", prompt="Classify Japanese, leather, huge, tasty, pink, fascinating, plastic, new, round, Spanish, tiny, sad, wooden, wide, small, grey, wool, Swedish, metal, square, fantastic, yellow and old.", representation="CATEGORY_SORT_TABLE"),
                B("ADJ-HINTS", "HINT_LADDER", "If you get stuck", "H1 Spot it: ask what the word tells you. H2 Remember: the answer to that question names the family. H3 Picture it: place the word under the seven labelled headings.", [REF_I], support="H3", representation="CATEGORY_SORT_TABLE"),
                B("ADJ-VERIFY", "INDEPENDENT_RETRY", "Fresh adjective check", "Use new words so success cannot come from memorising the source list.", [REF_I], prompt="Classify enormous, ancient, oval, Brazilian, cotton, lovely and purple.", support="H0"),
                B("ADJ-ANSWER", "ANSWER_CHECK", "Classification check", "Check category reasoning, not just spelling. Origin words should be capitalised when they are proper adjectives.", [REF_I], audience="ADULT", visibility="ANSWER_KEY_ONLY", solution="enormous=Size; ancient=Age; oval=Shape; Brazilian=Origin; cotton=Material; lovely=Opinion; purple=Colour."),
            ],
            "independent_evidence_refs": ["ADJ-VERIFY"],
        },
        {
            "learning_object_id": "LO-ADJ-ORDER",
            "title": "Adjective order and source boundaries",
            "learning_goal": "Classify first, order second, and stop rather than invent a category when the worksheet model does not decide.",
            "source_refs": [REF_III],
            "capability_refs": ["ENG-ADJ-CLASSIFY-SOURCE-MODEL", "ENG-ADJ-ORDER", "ENG-ADJ-SOURCE-BOUNDARY"],
            "prerequisite_refs": ["LO-ADJ-FAMILIES"],
            "misconception_targets": ["ADJECTIVE_ORDER_SEQUENCE_ERROR", "SOURCE_MODEL_FORCE_FIT"],
            "blocks": [
                B("ORDER-RULE", "SOURCE_RULE", "The school adjective train", "For this worksheet: Opinion → Size → Age → Shape → Colour → Origin → Material → Noun. You do not need every carriage every time.", [REF_III], provenance="SOURCE_DERIVED", representation="ADJECTIVE_ORDER_TRAIN", params={"ordering": ["OPINION", "SIZE", "AGE", "SHAPE", "COLOUR", "ORIGIN", "MATERIAL", "NOUN"]}),
                B("ORDER-MODEL-TEMPLE", "WORKED_EXAMPLE", "Fix the temple phrase", "Find the noun, classify the describing words, then read the categories left to right.", [REF_III], visibility="WORKED_EXAMPLE", solution="stone=Material, ancient=Age, huge=Size, Indian=Origin → huge ancient Indian stone temple."),
                B("ORDER-MODEL-DOOR", "ANNOTATED_MODEL", "Fix the door phrase", "The source phrase is wooden beautiful large door. Classify before reordering.", [REF_III], visibility="WORKED_EXAMPLE", solution="wooden=Material, beautiful=Opinion, large=Size → beautiful large wooden door."),
                B("ORDER-BOUNDARY", "SOURCE_BOUNDARY", "What about traditional?", "The printed seven-column model does not give traditional a clean category. Mark the boundary explicitly; do not invent Quality, Condition or another eighth family.", [REF_III], provenance="SOURCE_DERIVED", representation="CONTRAST_PAIR"),
                B("ORDER-GUIDED", "GUIDED_PRACTICE", "Label before you order", "Write the category under each adjective before moving any word.", [REF_III], visibility="PARTIAL", prompt="Repair: plastic / round / new / fascinating / toy.", representation="ADJECTIVE_ORDER_TRAIN"),
                B("ORDER-HINTS", "HINT_LADDER", "If the order feels confusing", "H1 Find the noun. H2 Label each adjective by family. H3 Put only the needed family boxes in source order and read left to right.", [REF_III], support="H3", representation="ADJECTIVE_ORDER_TRAIN"),
                B("ORDER-VERIFY", "INDEPENDENT_RETRY", "Fresh order check", "Use a new phrase without looking back.", [REF_III], prompt="Rewrite: old / tiny / Brazilian / wooden / house.", support="H0"),
                B("ORDER-ANSWER", "ANSWER_CHECK", "Order check", "Accept source-grounded order and keep boundary words visibly unresolved unless a teacher/textbook supplies a category.", [REF_III], audience="ADULT", visibility="ANSWER_KEY_ONLY", solution="tiny old Brazilian wooden house."),
            ],
            "independent_evidence_refs": ["ORDER-VERIFY"],
        },
        {
            "learning_object_id": "LO-MYSTERY-OBJECT",
            "title": "Describe a mystery object",
            "learning_goal": "Move from adjective grammar to a meaningful description with material, origin and a plausible use.",
            "source_refs": [REF_II],
            "capability_refs": ["ENG-DESC-NOUN-PHRASE", "ENG-DESC-MATERIAL-ORIGIN", "ENG-DESC-PURPOSE-INFERENCE"],
            "prerequisite_refs": ["LO-ADJ-FAMILIES", "LO-ADJ-ORDER"],
            "misconception_targets": ["ADJECTIVE_LIST_WITHOUT_CLEAR_NOUN", "PURPOSE_STATED_WITHOUT_REASON"],
            "blocks": [
                B("MYSTERY-CONCEPT", "CONCEPT", "From grammar to meaning", "Choose the noun first. Add only useful details that help the reader picture the object or understand where it came from and what it may be used for.", [REF_II], representation="NOUN_PHRASE_BUILDER"),
                B("MYSTERY-MODEL", "ANNOTATED_MODEL", "A model structure", "Notice the jobs of each sentence rather than memorising the wording.", [REF_II], visibility="WORKED_EXAMPLE", solution="I found a fascinating tiny round object. It was made of metal and came from Sweden. I think it was used for keeping something small and precious."),
                B("MYSTERY-PLANNER", "GUIDED_PRACTICE", "Plan before sentences", "Plan the noun, useful adjectives, material, origin and possible purpose before writing.", [REF_II], visibility="PARTIAL", prompt="Plan a mysterious object using the worksheet response frame, then write three clear sentences.", representation="MYSTERY_OBJECT_PLANNER"),
                B("MYSTERY-DIAG", "MISCONCEPTION_CHECK", "More adjectives is not always better", "If the description becomes a long adjective pile, spread details across sentences and keep the noun clear.", [REF_II], representation="CONTRAST_PAIR"),
                B("MYSTERY-HINTS", "HINT_LADDER", "If you do not know what to write", "H1 Choose the noun. H2 Add one useful detail at a time. H3 Use the planner boxes: object, what it is like, made of/from, used for.", [REF_II], support="H3", representation="MYSTERY_OBJECT_PLANNER"),
                B("MYSTERY-VERIFY", "INDEPENDENT_RETRY", "Fresh mystery object", "Describe a different object without the sentence frame.", [REF_II], prompt="Imagine you found a strange box in an old attic. Describe it in two or three sentences and give one plausible use.", support="H0"),
                B("MYSTERY-RUBRIC", "RUBRIC", "Mystery-object rubric", "Look for a clear noun, suitable adjectives, material, origin and a plausible purpose. Wording can vary.", [REF_II], audience="ADULT", visibility="ANSWER_KEY_ONLY"),
            ],
            "independent_evidence_refs": ["MYSTERY-VERIFY"],
        },
        {
            "learning_object_id": "LO-TRAVEL-WRITING",
            "title": "Travel-blogger descriptive writing",
            "learning_goal": "Write a short place description that meets every visible source criterion without stuffing adjectives into one noun phrase.",
            "source_refs": [REF_IV],
            "capability_refs": ["ENG-DESC-OPENING", "ENG-DESC-VISUAL-DETAIL", "ENG-DESC-REVISION", "ENG-ADJ-ORDER"],
            "prerequisite_refs": ["LO-ADJ-ORDER"],
            "misconception_targets": ["ADJECTIVE_DUMP_WITHOUT_DESCRIPTION", "CHECKLIST_REQUIREMENT_OMITTED"],
            "blocks": [
                B("TRAVEL-CONCEPT", "CONCEPT", "Make the reader see the place", "Build the paragraph in four moves: interesting opening, what I see, zoom in on details, how I feel. Spread adjectives naturally across sentences.", [REF_IV], representation="TRAVEL_BLOGGER_PLANNER"),
                B("TRAVEL-SOURCE-RULE", "SOURCE_RULE", "What the worksheet checks", "The source asks for at least six adjectives, an interesting opening, visible details and correct adjective order, with adjectives underlined.", [REF_IV], provenance="SOURCE_DERIVED", representation="WRITING_CHECKLIST"),
                B("TRAVEL-MODEL", "ANNOTATED_MODEL", "Notice how a paragraph meets the checklist", "Study the structure, not the exact wording.", [REF_IV], visibility="WORKED_EXAMPLE", solution="What a wonderful sight greeted me at the coast! Near me, a wide blue sea sparkled in the sun. Colourful boats bobbed beside the pier, and children ran across the soft golden sand. Farther away, a small white lighthouse stood above the rocks. The whole place felt peaceful and bright."),
                B("TRAVEL-CONTRAST", "CONTRAST", "Natural writing vs adjective stuffing", "The worksheet asks for six adjectives in the whole description, not six before one noun. Strong nouns and verbs also help the reader picture the scene.", [REF_IV], representation="CONTRAST_PAIR"),
                B("TRAVEL-GUIDED", "GUIDED_PRACTICE", "Plan before you write", "Choose a destination, opening idea, near/far details and an adjective bank before drafting.", [REF_IV], visibility="PARTIAL", prompt="Plan a description of one source destination and draft 4–5 sentences.", representation="TRAVEL_BLOGGER_PLANNER"),
                B("TRAVEL-HINTS", "HINT_LADDER", "If the page feels blank", "H1 Pick one thing you can see. H2 Add a useful size/colour/material/origin detail. H3 Use Opening → What I see → Zoom in → How I feel.", [REF_IV], support="H3", representation="TRAVEL_BLOGGER_PLANNER"),
                B("TRAVEL-VERIFY", "INDEPENDENT_RETRY", "Fresh place description", "Use a new setting so the paragraph cannot be copied from the model.", [REF_IV], prompt="Write 4–5 sentences about a mountain village after light rain. Include an interesting opening, visible details and at least six adjectives; underline them.", support="H0"),
                B("TRAVEL-RUBRIC", "RUBRIC", "Travel-blogger rubric", "Check: interesting opening; six or more adjectives; visible details; source-model order where several adjectives precede one noun; adjectives underlined. Do not require exact wording.", [REF_IV], audience="ADULT", visibility="ANSWER_KEY_ONLY"),
            ],
            "independent_evidence_refs": ["TRAVEL-VERIFY"],
        },
        {
            "learning_object_id": "LO-POEM-READING",
            "title": "Read The Dodo's Story for meaning",
            "learning_goal": "Read the poem as a whole, understand key vocabulary, follow the four-stanza meaning and distinguish poem evidence from outside knowledge.",
            "source_refs": POEM_REFS,
            "capability_refs": ["ENG-POEM-READ-FOR-MEANING", "ENG-TEXT-EVIDENCE"],
            "prerequisite_refs": [],
            "misconception_targets": ["ANSWERING_FROM_MEMORY_INSTEAD_OF_TEXT", "OUTSIDE_RESEARCH_REPLACES_POEM"],
            "blocks": [
                B("POEM-ROUTINE", "READING_ROUTINE", "Read the poem more than once", "Preview the title; read aloud for the story; read again for clues; check important vocabulary; summarise each stanza before answering.", POEM_REFS, representation="STANZA_MEANING_MAP"),
                B("POEM-VOCAB", "VOCABULARY", "Words that unlock the poem", "gentle=calm and not fierce; soar=fly high; beneath=under; wandered=moved around; fearlessly=without showing fear; cleared=removed trees/plants; vanished=disappeared; precious=very valuable.", POEM_REFS, provenance="SOURCE_DERIVED"),
                B("POEM-MODEL", "ANNOTATED_MODEL", "Stanza-by-stanza meaning", "Stanza 1 introduces the Dodo; stanza 2 shows how it lived; stanza 3 brings human-linked dangers; stanza 4 gives the result and conservation message.", POEM_REFS, visibility="WORKED_EXAMPLE", solution="Dodo lives freely → humans and new dangers arrive → the Dodo disappears → the poem ends with a message about protecting living things."),
                B("POEM-SOURCE", "SOURCE_BOUNDARY", "Poem facts vs outside research", "For a comprehension question, use the poem as authority. Outside research may add detail or uncertainty, but it must not silently replace what the poem says.", POEM_REFS, provenance="SOURCE_DERIVED", representation="TEXT_VS_MY_THINKING"),
                B("POEM-GUIDED", "GUIDED_PRACTICE", "Summarise before answering", "Write one short sentence for each stanza, then identify the poem's topic and larger message.", POEM_REFS, visibility="PARTIAL", prompt="Summarise the four stanzas and write one sentence for the poem's message.", representation="STANZA_MEANING_MAP"),
                B("POEM-HINTS", "HINT_LADDER", "If the poem feels hard", "H1 Read one stanza only. H2 Say what changed in that stanza. H3 Put the four stanza summaries into a meaning map.", POEM_REFS, support="H3", representation="STANZA_MEANING_MAP"),
                B("POEM-VERIFY", "INDEPENDENT_RETRY", "Fresh poem reading", "Read a new short conservation poem and summarise the story/message without a hint.", POEM_REFS, prompt="Read a fresh short poem about a river, then write its topic and message in your own words.", support="H0"),
                B("POEM-ANSWER", "ANSWER_CHECK", "Reading check", "Accept concise summaries that preserve the four main meaning moves and separate poem evidence from outside knowledge.", POEM_REFS, audience="ADULT", visibility="ANSWER_KEY_ONLY"),
            ],
            "independent_evidence_refs": ["POEM-VERIFY"],
        },
        {
            "learning_object_id": "LO-Q1-EVIDENCE",
            "title": "Inference with Answer + Clue + Connection",
            "learning_goal": "Explain why forest clearing could harm the Dodo using a defensible answer, a poem clue and a clear connection.",
            "source_refs": [REF_Q1],
            "capability_refs": ["ENG-TEXT-EVIDENCE", "ENG-CAUSE-EFFECT", "ENG-INFERENCE"],
            "prerequisite_refs": ["LO-POEM-READING"],
            "misconception_targets": ["TEXT_EVIDENCE_NOT_PROVIDED", "CAUSE_NAMED_WITHOUT_CONNECTION"],
            "blocks": [
                B("Q1-CONCEPT", "CONCEPT", "A strong inference is not a guess", "Build three parts: ANSWER—what you think; CLUE—which words helped; CONNECTION—how the clue supports the answer.", [REF_Q1], representation="ANSWER_CLUE_CONNECTION"),
                B("Q1-MODEL", "WORKED_EXAMPLE", "Forest clearing model", "Use a line about the Dodo's food/home and connect it to the loss of forests.", [REF_Q1], visibility="WORKED_EXAMPLE", solution="Answer: clearing forests could reduce the Dodo's food and habitat. Clue: it ate fallen fruits beneath the trees. Connection: fewer trees could mean fewer fruit sources and less forest habitat."),
                B("Q1-CONTRAST", "CONTRAST", "Plausible is not yet supported", "Compare 'The forests were important' with a response that includes the relevant poem clue and explains why it matters.", [REF_Q1], representation="CONTRAST_PAIR"),
                B("Q1-GUIDED", "GUIDED_PRACTICE", "Build the three parts", "Complete Answer, Clue and Connection separately before combining them.", [REF_Q1], visibility="PARTIAL", prompt="Why would clearing forests be harmful to the Dodo? Fill Answer → Clue → Connection.", representation="ANSWER_CLUE_CONNECTION"),
                B("Q1-HINTS", "HINT_LADDER", "If you know the idea but cannot explain it", "H1 Which line tells what the Dodo got from the trees? H2 Use Answer + Clue + Connection. H3 Fill the three labelled boxes before writing a sentence.", [REF_Q1], support="H3", representation="ANSWER_CLUE_CONNECTION"),
                B("Q1-VERIFY", "INDEPENDENT_RETRY", "Fresh inference", "Use a different text so the wording must be built again.", [REF_Q1], prompt="From a fresh short passage, explain one cause-and-effect inference with a clue and connection.", support="H0"),
                B("Q1-RUBRIC", "RUBRIC", "Q1 evidence rubric", "Look for a defensible answer, a relevant poem clue and a connection. Do not exact-string match an open response.", [REF_Q1], audience="ADULT", visibility="ANSWER_KEY_ONLY"),
            ],
            "independent_evidence_refs": ["Q1-VERIFY"],
        },
        {
            "learning_object_id": "LO-Q2-MULTI-CAUSE",
            "title": "Bring multiple causes together",
            "learning_goal": "Recognise that Q2 asks for more than hunting and synthesise several human-linked clues.",
            "source_refs": [REF_Q2],
            "capability_refs": ["ENG-TEXT-EVIDENCE", "ENG-CAUSE-EFFECT", "ENG-MULTI-CLUE-SYNTHESIS"],
            "prerequisite_refs": ["LO-POEM-READING"],
            "misconception_targets": ["SINGLE_CAUSE_WHEN_MULTI_CAUSE_REQUIRED", "CLUE_LIST_WITHOUT_SYNTHESIS"],
            "blocks": [
                B("Q2-CONCEPT", "CONCEPT", "One clue is not the whole answer", "The word 'only' signals that you should test the hunting idea against other clues and collect more than one relevant human-linked action.", [REF_Q2], representation="MULTI_CLUE_TABLE"),
                B("Q2-MODEL", "WORKED_EXAMPLE", "Build a multi-cause answer", "Collect clues first, then explain how they contributed together.", [REF_Q2], visibility="WORKED_EXAMPLE", solution="No. The poem also mentions dogs and cats and says forests were cleared. These actions could make the Dodo less safe and reduce habitat/food, so hunting was not the only pressure."),
                B("Q2-DIAG", "DIAGNOSTIC_PROBE", "If the child names only hunting", "Ask: 'Find two other human-linked actions in the danger stanza.' This tests clue gathering before giving another explanation.", [REF_Q2], audience="BOTH", support="H1", representation="MULTI_CLUE_TABLE"),
                B("Q2-GUIDED", "GUIDED_PRACTICE", "Collect, then connect", "Fill a clue table with hunting, introduced animals and forest clearing; then write what the clues show together.", [REF_Q2], visibility="PARTIAL", prompt="Was hunting the only cause? Gather at least two other clues before writing your answer.", representation="MULTI_CLUE_TABLE"),
                B("Q2-HINTS", "HINT_LADDER", "If you stop after one cause", "H1 Look for another human-linked action. H2 Collect at least two non-hunting clues. H3 Use a clue table before writing the synthesis sentence.", [REF_Q2], support="H3", representation="MULTI_CLUE_TABLE"),
                B("Q2-VERIFY", "INDEPENDENT_RETRY", "Fresh synthesis", "Use a fresh paragraph containing three causes.", [REF_Q2], prompt="Explain why one cause alone is not the whole answer in a new three-cause paragraph.", support="H0"),
                B("Q2-RUBRIC", "RUBRIC", "Q2 synthesis rubric", "Look for a direct answer to 'only?', more than one relevant additional clue, and a sentence that connects the clues rather than merely listing them.", [REF_Q2], audience="ADULT", visibility="ANSWER_KEY_ONLY"),
            ],
            "independent_evidence_refs": ["Q2-VERIFY"],
        },
        {
            "learning_object_id": "LO-Q3Q4-TRANSFER-JUSTIFY",
            "title": "Transfer the message and justify a choice",
            "learning_goal": "Move beyond the poem carefully: connect a present-day threat to a protective action and make a hypothetical choice with a reason.",
            "source_refs": [REF_Q3, REF_Q4],
            "capability_refs": ["ENG-TRANSFER", "ENG-JUSTIFICATION", "ENG-POEM-READ-FOR-MEANING"],
            "prerequisite_refs": ["LO-POEM-READING"],
            "misconception_targets": ["TRANSFER_EXAMPLE_WITHOUT_PARALLEL", "PROTECTION_ACTION_NOT_LINKED_TO_THREAT", "CHOICE_WITHOUT_JUSTIFICATION", "REASON_NOT_CONNECTED_TO_CHOICE"],
            "blocks": [
                B("Q34-CONCEPT", "CONCEPT", "Two beyond-text structures", "Q3 uses Species → Threat → Action to help. Q4 uses Choice → Reason → Expected effect. More than one answer can be defensible if the reasoning is connected.", [REF_Q3, REF_Q4], representation="TEXT_VS_MY_THINKING"),
                B("Q3-MODEL", "ANNOTATED_MODEL", "Transfer model", "Use accurate outside knowledge only because Q3 asks you to go beyond the poem.", [REF_Q3], visibility="WORKED_EXAMPLE", solution="Sea turtles can be threatened by marine debris and damaged nesting habitat. People can keep beaches clean, reduce harmful waste and protect nesting areas because those actions address the threats named."),
                B("Q4-MODEL", "ANNOTATED_MODEL", "Choice + reason model", "Choose one event and explain the effect of changing it.", [REF_Q4], visibility="WORKED_EXAMPLE", solution="I would stop the forests from being cleared because the Dodos depended on trees for food and habitat. Protecting the forest could remove one major pressure on them."),
                B("Q34-GUIDED", "GUIDED_PRACTICE", "Use the right frame", "Plan Q3 in a three-column threat-action table and Q4 in a choice-reason frame.", [REF_Q3, REF_Q4], visibility="PARTIAL", prompt="Plan one Q3 response and one Q4 response before writing full sentences.", representation="TRANSFER_THREAT_ACTION_TABLE"),
                B("Q34-HINTS", "HINT_LADDER", "If the answer feels too open", "H1 Identify which frame the question needs. H2 For Q3 link the action to the threat; for Q4 link the reason to the chosen event. H3 Fill the frame boxes first.", [REF_Q3, REF_Q4], support="H3", representation="CHOICE_REASON_FRAME"),
                B("Q3-VERIFY", "TRANSFER", "Fresh transfer", "Use a different living species and a new threat-action pair.", [REF_Q3], prompt="Name another species affected by a human-linked threat and give one protective action that directly addresses that threat.", support="H0"),
                B("Q4-VERIFY", "INDEPENDENT_RETRY", "Fresh justification", "Use a different story so the child must rebuild the reasoning.", [REF_Q4], prompt="Choose one event from a fresh story that you would change and explain why that change matters.", support="H0"),
                B("Q3-RUBRIC", "RUBRIC", "Q3 transfer rubric", "Look for a living species, a plausible human-linked threat and a protective action that addresses that threat. Multiple answers are possible.", [REF_Q3], audience="ADULT", visibility="ANSWER_KEY_ONLY"),
                B("Q4-RUBRIC", "RUBRIC", "Q4 justification rubric", "Look for one event choice and a reason connected to its consequence. Do not require the model wording.", [REF_Q4], audience="ADULT", visibility="ANSWER_KEY_ONLY"),
            ],
            "independent_evidence_refs": ["Q3-VERIFY", "Q4-VERIFY"],
        },
    ]

    coverage = [
        C(REF_I, ["LO-ADJ-FAMILIES"], ["ADJ-CONCEPT", "ADJ-SOURCE-RULE", "ADJ-CONTRAST"], ["ADJ-MODEL"], ["ADJ-GUIDED"], ["ADJ-HINTS"], ["ADJ-VERIFY"], ["ADJ-ANSWER"]),
        C(REF_II, ["LO-MYSTERY-OBJECT"], ["MYSTERY-CONCEPT", "MYSTERY-DIAG"], ["MYSTERY-MODEL"], ["MYSTERY-PLANNER"], ["MYSTERY-HINTS"], ["MYSTERY-VERIFY"], ["MYSTERY-RUBRIC"]),
        C(REF_III, ["LO-ADJ-ORDER"], ["ORDER-RULE", "ORDER-BOUNDARY"], ["ORDER-MODEL-TEMPLE", "ORDER-MODEL-DOOR"], ["ORDER-GUIDED"], ["ORDER-HINTS"], ["ORDER-VERIFY"], ["ORDER-ANSWER"]),
        C(REF_IV, ["LO-TRAVEL-WRITING"], ["TRAVEL-CONCEPT", "TRAVEL-SOURCE-RULE", "TRAVEL-CONTRAST"], ["TRAVEL-MODEL"], ["TRAVEL-GUIDED"], ["TRAVEL-HINTS"], ["TRAVEL-VERIFY"], ["TRAVEL-RUBRIC"]),
        C(REF_Q1, ["LO-POEM-READING", "LO-Q1-EVIDENCE"], ["POEM-ROUTINE", "POEM-VOCAB", "Q1-CONCEPT", "Q1-CONTRAST"], ["POEM-MODEL", "Q1-MODEL"], ["POEM-GUIDED", "Q1-GUIDED"], ["POEM-HINTS", "Q1-HINTS"], ["Q1-VERIFY"], ["Q1-RUBRIC"]),
        C(REF_Q2, ["LO-POEM-READING", "LO-Q2-MULTI-CAUSE"], ["POEM-ROUTINE", "POEM-VOCAB", "Q2-CONCEPT"], ["POEM-MODEL", "Q2-MODEL"], ["POEM-GUIDED", "Q2-GUIDED"], ["Q2-DIAG", "Q2-HINTS"], ["Q2-VERIFY"], ["Q2-RUBRIC"]),
        C(REF_Q3, ["LO-POEM-READING", "LO-Q3Q4-TRANSFER-JUSTIFY"], ["POEM-ROUTINE", "POEM-SOURCE", "Q34-CONCEPT"], ["POEM-MODEL", "Q3-MODEL"], ["POEM-GUIDED", "Q34-GUIDED"], ["POEM-HINTS", "Q34-HINTS"], ["Q3-VERIFY"], ["Q3-RUBRIC"]),
        C(REF_Q4, ["LO-POEM-READING", "LO-Q3Q4-TRANSFER-JUSTIFY"], ["POEM-ROUTINE", "Q34-CONCEPT"], ["POEM-MODEL", "Q4-MODEL"], ["POEM-GUIDED", "Q34-GUIDED"], ["POEM-HINTS", "Q34-HINTS"], ["Q4-VERIFY"], ["Q4-RUBRIC"]),
    ]

    return {
        "schema_version": "1.0.0",
        "journey_id": "ENG-G4-WS09-STUDY-JOURNEY-001",
        "title": "Word Explorer: Adjective Order, Descriptive Writing and Poetry Comprehension",
        "grade_level": 4,
        "subject": "ENGLISH",
        "source_id": "ENG-G4-WS09",
        "required_source_refs": ALL_REFS,
        "learning_objects": learning_objects,
        "source_coverage": coverage,
    }


if __name__ == "__main__":
    from pathlib import Path
    import json, sys
    engine = Path(__file__).resolve().parents[3] / "StudyDesign" / "engine"
    sys.path.insert(0, str(engine))
    from study_journey import validate_study_journey  # type: ignore
    journey = build_study_journey()
    print(json.dumps(validate_study_journey(journey), indent=2))
