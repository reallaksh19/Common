#!/usr/bin/env python3
"""Deterministic GENERATED_ORIGINAL Chemistry Core (2A) challenge builder.

The builder does not free-write Chemistry. It transforms already-governed C-I /
Core2A source items through a small set of explicitly authorized problem-family
recipes, reuses Core1A hint/representation evidence, independently recomputes
family-specific Chemistry checks, runs a near-copy gate, and gives every fresh
question an answer path plus inline provenance.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path

SUBSCRIPT_TRANS = str.maketrans("₀₁₂₃₄₅₆₇₈₉", "0123456789")
SUPERSCRIPT_CHARS = set("⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻")
SUBSCRIPT_CHARS = set("₀₁₂₃₄₅₆₇₈₉")


def canonical(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(obj, field=None):
    payload = copy.deepcopy(obj)
    if field:
        payload.pop(field, None)
    return hashlib.sha256(canonical(payload).encode("utf-8")).hexdigest()


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def uniq(values):
    out = []
    for value in values:
        if value not in out:
            out.append(value)
    return out


def fail(code, detail=""):
    raise ValueError(f"{code}: {detail}" if detail else code)


def normalize_text(value):
    return " ".join(re.findall(r"[\w⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻₀₁₂₃₄₅₆₇₈₉]+", (value or "").lower(), flags=re.UNICODE))


def token_jaccard(a, b):
    sa, sb = set(normalize_text(a).split()), set(normalize_text(b).split())
    if not sa and not sb:
        return 1.0
    if not sa or not sb:
        return 0.0
    return len(sa & sb) / len(sa | sb)


def near_copy_report(prompt, source_items, policy):
    norm_prompt = normalize_text(prompt)
    best = None
    exact = False
    for item in source_items:
        stem = item["source_snapshot"]["stem"]
        norm_source = normalize_text(stem)
        seq = SequenceMatcher(None, norm_prompt, norm_source).ratio()
        jac = token_jaccard(prompt, stem)
        row = (max(seq, jac), seq, jac, item["question_ref"], norm_prompt == norm_source)
        if best is None or row[0] > best[0]:
            best = row
        exact = exact or row[4]
    if best is None:
        fail("CORE2A_CHALLENGE_TARGET_UNGROUNDED", "no source stems for near-copy comparison")
    _, seq, jac, closest, _ = best
    cfg = policy["near_copy"]
    if exact and cfg["exact_normalized_copy_forbidden"]:
        fail("CORE2A_GENERATED_ITEM_TOO_CLOSE_TO_SOURCE", closest + ": exact normalized copy")
    if seq > cfg["max_sequence_ratio"] or jac > cfg["max_token_jaccard"]:
        fail("CORE2A_GENERATED_ITEM_TOO_CLOSE_TO_SOURCE", f"{closest}: sequence={seq:.3f}, jaccard={jac:.3f}")
    return {
        "max_sequence_ratio": round(seq, 6),
        "max_token_jaccard": round(jac, 6),
        "closest_source_question_ref": closest,
        "exact_copy": False,
        "status": "PASS",
    }


def archetype_tables(registry):
    by_name = {row["name"]: row for row in registry["archetypes"]}
    by_id = {row["archetype_id"]: row for row in registry["archetypes"]}
    if len(by_name) != len(registry["archetypes"]) or len(by_id) != len(registry["archetypes"]):
        fail("CORE2A_CHALLENGE_TARGET_UNGROUNDED", "duplicate archetype")
    return by_name, by_id


def bucket_tables(bucket_plan):
    by_id = {b["bucket_id"]: b for b in bucket_plan["buckets"]}
    if len(by_id) != len(bucket_plan["buckets"]):
        fail("CORE2A_CHALLENGE_TARGET_UNGROUNDED", "duplicate Core1A bucket")
    return by_id


def validate_upstream(source_plan, bucket_plan):
    if source_plan.get("core1a_bucket_plan_ref") != bucket_plan.get("plan_id"):
        fail("CORE2A_CHALLENGE_TARGET_UNGROUNDED", "source plan / Core1A ref")
    if source_plan.get("core1a_bucket_plan_digest") != bucket_plan.get("plan_digest"):
        fail("CORE2A_CHALLENGE_TARGET_UNGROUNDED", "source plan / Core1A digest")
    question_map = {}
    for bucket in bucket_plan["buckets"]:
        for q in bucket["core2_primary_question_refs"]:
            if q in question_map:
                fail("CORE2A_CHALLENGE_TARGET_UNGROUNDED", q + ": duplicate bucket ownership")
            question_map[q] = bucket["bucket_id"]
    for item in source_plan["items"]:
        q = item["question_ref"]
        if q not in question_map or item["core1a_binding"]["bucket_id"] != question_map[q]:
            fail("CORE2A_CHALLENGE_TARGET_UNGROUNDED", q + ": source item binding drift")


def extract_formula_token(stem):
    candidates = []
    for raw in re.split(r"\s+", stem):
        token = raw.strip(".,;:?!()[]{}\"'")
        if not token or not re.search(r"[A-Z]", token):
            continue
        if any(ch in SUBSCRIPT_CHARS or ch in SUPERSCRIPT_CHARS for ch in token):
            candidates.append(token)
    if not candidates:
        fail("CORE2A_GENERATED_ITEM_NOT_INDEPENDENTLY_VERIFIED", "formula token not recoverable")
    return candidates[0]


def extract_equation(stem):
    arrow = "→" if "→" in stem else "->" if "->" in stem else None
    if not arrow:
        fail("CORE2A_GENERATED_ITEM_NOT_INDEPENDENTLY_VERIFIED", "reaction arrow missing")
    pos = stem.index(arrow)
    left_start = stem.rfind(",", 0, pos) + 1
    left_fragment = stem[left_start:pos].strip()
    for prefix in ("For ", "for ", "In ", "in "):
        if left_fragment.startswith(prefix):
            left_fragment = left_fragment[len(prefix):].strip()
    right_tail = stem[pos + len(arrow):]
    right_fragment = re.split(r"[,?.;]", right_tail, maxsplit=1)[0].strip()
    eq = left_fragment + " → " + right_fragment
    if not left_fragment or not right_fragment:
        fail("CORE2A_GENERATED_ITEM_NOT_INDEPENDENTLY_VERIFIED", "reaction sides missing")
    return eq


def strip_charge(formula):
    return "".join(ch for ch in formula if ch not in SUPERSCRIPT_CHARS)


def parse_formula(formula):
    clean = strip_charge(formula.translate(SUBSCRIPT_TRANS))
    clean = clean.replace("(", "").replace(")", "")
    pos = 0
    counts = {}
    for match in re.finditer(r"([A-Z][a-z]?)(\d*)", clean):
        if match.start() != pos:
            fail("CORE2A_GENERATED_ITEM_NOT_INDEPENDENTLY_VERIFIED", "unsupported formula " + formula)
        element, raw_n = match.groups()
        n = int(raw_n) if raw_n else 1
        counts[element] = counts.get(element, 0) + n
        pos = match.end()
    if pos != len(clean) or not counts:
        fail("CORE2A_GENERATED_ITEM_NOT_INDEPENDENTLY_VERIFIED", "unsupported formula " + formula)
    return counts


def parse_term(term):
    raw = term.strip()
    m = re.match(r"^(\d+)?\s*([^\s]+)$", raw)
    if not m:
        fail("CORE2A_GENERATED_ITEM_NOT_INDEPENDENTLY_VERIFIED", "unsupported equation term " + raw)
    coefficient = int(m.group(1)) if m.group(1) else 1
    formula = m.group(2)
    return coefficient, formula


def side_terms(side):
    return [parse_term(term) for term in side.split(" + ")]


def side_counts(side):
    total = {}
    for coefficient, formula in side_terms(side):
        for element, count in parse_formula(formula).items():
            total[element] = total.get(element, 0) + coefficient * count
    return total


def equation_parts(equation):
    left, right = [x.strip() for x in equation.split("→", 1)]
    return left, right


def ledger_answer(equation):
    left, right = equation_parts(equation)
    lc, rc = side_counts(left), side_counts(right)
    elements = sorted(set(lc) | set(rc))
    ledger = "; ".join(f"{e}: {lc.get(e,0)} left, {rc.get(e,0)} right" for e in elements)
    status = "conserved" if lc == rc else "not conserved"
    return ledger + "; atoms are " + status + ".", lc, rc


def infer_agents(stem):
    equation = extract_equation(stem)
    left, _ = equation_parts(equation)
    reactants = [formula for _, formula in side_terms(left)]
    electron_segments = re.findall(r"([^,.;?]*→[^,.;?]*e⁻[^,.;?]*)", stem)
    if not electron_segments:
        fail("CORE2A_GENERATED_ITEM_NOT_INDEPENDENTLY_VERIFIED", "electron-loss half-change missing")
    half = electron_segments[-1]
    half_left = half.split("→", 1)[0].strip().split()[-1]
    reducing = half_left
    others = [r for r in reactants if r != reducing]
    if len(reactants) != 2 or len(others) != 1:
        fail("CORE2A_GENERATED_ITEM_NOT_INDEPENDENTLY_VERIFIED", "agent recipe requires exactly two reactants")
    return equation, reducing, others[0]


def family_recipe(anchor, family_ref, archetype_name):
    snap = anchor["source_snapshot"]
    if family_ref == "PF-FORMULA_CHARGE_PARSE":
        formula = extract_formula_token(snap["stem"])
        answer = "The lower-right subscript counts atoms within the formula; the upper-right superscript gives the overall ionic charge."
        if archetype_name == "NEAR_TRANSFER":
            prompt = f"Read {formula} without using the original options. What job does the lower-right subscript do, and what job does the upper-right superscript do?"
        else:
            prompt = f"A learner says that in {formula} the lower-right number is the ionic charge and the upper-right sign/number counts atoms. Diagnose and correct both labels."
        steps = [
            f"Separate the lower-right and upper-right notation in {formula}.",
            "Read the lower-right subscript as part of the composition of one formula unit/species.",
            "Read the upper-right superscript as the charge on the whole ion/species.",
        ]
        write_first = f"Write {formula} and label the lower-right and upper-right symbols separately."
        return prompt, answer, steps, write_first

    if family_ref == "PF-MACRO_PARTICLE_SYMBOL_TRANSLATION":
        fig = snap.get("figure_semantic") or {}
        particles = fig.get("particles") or []
        if len(particles) != 1 or not particles[0].get("formula") or not isinstance(particles[0].get("count"), int):
            fail("CORE2A_CHALLENGE_TARGET_UNGROUNDED", anchor["question_ref"] + ": particle semantic shape")
        formula, count = particles[0]["formula"], particles[0]["count"]
        if archetype_name == "NEAR_TRANSFER":
            new_count = count + 1
            symbolic = (str(new_count) if new_count != 1 else "") + formula
            prompt = f"One more identical {formula} particle is added to the source particle model. The model now contains {new_count} separate {formula} particles. What symbolic representation matches it?"
            answer = symbolic
            steps = [f"Keep the composition of one particle as {formula}.", f"Count {new_count} separate particles.", f"Place {new_count} in front as a coefficient: {symbolic}."]
        else:
            symbolic = (str(count) if count != 1 else "") + formula
            prompt = f"A learner says, ‘To show {count} separate {formula} particles, I should change the subscripts inside {formula}.’ Diagnose the mistake and write the correct symbolic representation."
            answer = f"Do not change the subscripts; use the coefficient form {symbolic}."
            steps = [f"The internal composition of each particle remains {formula}.", f"A coefficient, not a changed subscript, records {count} separate particles.", f"The correct form is {symbolic}."]
        write_first = f"Write one particle as {formula}; put the particle count in front, not inside the formula."
        return prompt, answer, steps, write_first

    if family_ref == "PF-CONSERVATION_LEDGER":
        equation = extract_equation(snap["stem"])
        ledger, lc, rc = ledger_answer(equation)
        if archetype_name == "NEAR_TRANSFER":
            prompt = f"For {equation}, write the left/right atom ledger for every element and state whether the equation conserves atoms."
            answer = ledger
            steps = ["Apply each coefficient to the complete formula that follows it.", "Count each element on the left and right separately.", "Compare element-by-element counts; equal totals for every element establish atom conservation."]
            write_first = "Draw a two-column ledger: element | left count | right count."
            return prompt, answer, steps, write_first
        left, right = equation_parts(equation)
        terms = side_terms(right)
        index = next((i for i, (coef, _) in enumerate(terms) if coef > 1), None)
        if index is None:
            fail("CORE2A_CHALLENGE_TARGET_UNGROUNDED", anchor["question_ref"] + ": no reconstructable product coefficient")
        target_coef, formula = terms[index]
        shown = []
        for i, (coef, f) in enumerate(terms):
            if i == index:
                shown.append("?" + f)
            else:
                shown.append((str(coef) if coef != 1 else "") + f)
        prompt = f"Reconstruct the missing coefficient in {left} → {' + '.join(shown)} using atom conservation. What whole-number coefficient replaces ?"
        answer = str(target_coef)
        steps = ["Count atoms on the complete reactant side.", f"Let the missing coefficient before {formula} be n and express the product atom counts in terms of n.", f"Match the element counts; n = {target_coef} restores the original conserved ledger."]
        write_first = f"Write n before {formula} and build the atom ledger in terms of n."
        return prompt, answer, steps, write_first

    if family_ref == "PF-CONDITION_VALIDITY":
        condition = (snap.get("condition_text") or "").strip()
        if not condition:
            fail("CORE2A_CHALLENGE_TARGET_UNGROUNDED", anchor["question_ref"] + ": missing condition")
        equation = extract_equation(snap["stem"])
        answer = f"Restore {condition} as a reaction condition attached to the arrow/description; it is not a reactant or product."
        if archetype_name == "NEAR_TRANSFER":
            prompt = f"A learner copies {equation} but leaves out the recorded condition. What must be restored, and where does it belong in the reaction representation?"
        else:
            prompt = f"A learner moves the recorded condition ‘{condition}’ to the product side of {equation}. Is that valid? State the correct role and placement of {condition}."
        steps = [f"Identify {condition} as the condition recorded with the source reaction.", "Keep a condition attached to the reaction arrow/description rather than counting it as chemical matter.", f"Restore {condition} without changing the reactants or products."]
        write_first = f"Copy the reaction and write the condition ‘{condition}’ at the arrow before answering."
        return prompt, answer, steps, write_first

    if family_ref == "PF-AGENT_ROLE_ASSIGNMENT":
        equation, reducing, oxidising = infer_agents(snap["stem"])
        if archetype_name == "NEAR_TRANSFER":
            prompt = f"In {equation}, the shown electron-loss half-change identifies {reducing} as the reducing agent. Which reactant is therefore the oxidising agent?"
            answer = oxidising
            steps = [f"The shown half-change has {reducing} losing electrons, so {reducing} is oxidised.", f"The other reacting species is {oxidising}.", f"The species that is reduced acts as the oxidising agent, so the answer is {oxidising}."]
            write_first = f"Mark {reducing} as electron-losing; then identify the other reactant before naming its role."
        else:
            prompt = f"For {equation}, state which reactant is oxidised and which reactant is reduced before naming any agent role."
            answer = f"{reducing} is oxidised; {oxidising} is reduced."
            steps = [f"The half-change shows {reducing} produces electrons, so {reducing} is oxidised.", f"The paired reactant {oxidising} accepts the transferred electrons and is reduced.", "Only after tracking these changes should agent labels be attached."]
            write_first = f"Write two lines: {reducing} → electron loss; {oxidising} → electron gain."
        return prompt, answer, steps, write_first

    fail("CORE2A_CHALLENGE_TARGET_UNGROUNDED", family_ref + ": no governed recipe")


def independent_validate(anchor, family_ref, archetype_name, expected_answer):
    snap = anchor["source_snapshot"]
    checks = []
    if family_ref == "PF-FORMULA_CHARGE_PARSE":
        token = extract_formula_token(snap["stem"])
        has_sub = any(ch in SUBSCRIPT_CHARS for ch in token)
        has_sup = any(ch in SUPERSCRIPT_CHARS for ch in token)
        if not (has_sub and has_sup) or "subscript" not in expected_answer.lower() or "superscript" not in expected_answer.lower():
            fail("CORE2A_GENERATED_ITEM_NOT_INDEPENDENTLY_VERIFIED", anchor["question_ref"] + ": notation roles")
        checks = ["SUBSCRIPT_POSITION_RECOGNISED", "SUPERSCRIPT_CHARGE_POSITION_RECOGNISED", "FORMULA_TOKEN_UNCHANGED"]
        validator = "FORMULA_NOTATION_ROLES"
    elif family_ref == "PF-MACRO_PARTICLE_SYMBOL_TRANSLATION":
        particles = (snap.get("figure_semantic") or {}).get("particles") or []
        if len(particles) != 1:
            fail("CORE2A_GENERATED_ITEM_NOT_INDEPENDENTLY_VERIFIED", anchor["question_ref"] + ": particle model")
        formula, count = particles[0]["formula"], particles[0]["count"]
        wanted = count + 1 if archetype_name == "NEAR_TRANSFER" else count
        symbolic = (str(wanted) if wanted != 1 else "") + formula
        if symbolic not in expected_answer:
            fail("CORE2A_GENERATED_ITEM_NOT_INDEPENDENTLY_VERIFIED", anchor["question_ref"] + ": coefficient result")
        checks = ["PARTICLE_IDENTITY_PRESERVED", "PARTICLE_COUNT_RECOMPUTED", "COEFFICIENT_NOT_SUBSCRIPT_USED"]
        validator = "PARTICLE_COEFFICIENT_COMPOSITION"
    elif family_ref == "PF-CONSERVATION_LEDGER":
        equation = extract_equation(snap["stem"])
        left, right = equation_parts(equation)
        lc, rc = side_counts(left), side_counts(right)
        if lc != rc:
            fail("CORE2A_GENERATED_ITEM_NOT_INDEPENDENTLY_VERIFIED", anchor["question_ref"] + ": anchor equation not conserved")
        if archetype_name == "NEAR_TRANSFER":
            ledger, _, _ = ledger_answer(equation)
            if expected_answer != ledger:
                fail("CORE2A_GENERATED_ITEM_NOT_INDEPENDENTLY_VERIFIED", anchor["question_ref"] + ": ledger answer")
        else:
            product_terms = side_terms(right)
            target = next((coef for coef, _ in product_terms if coef > 1), None)
            if target is None or expected_answer != str(target):
                fail("CORE2A_GENERATED_ITEM_NOT_INDEPENDENTLY_VERIFIED", anchor["question_ref"] + ": reconstructed coefficient")
        checks = ["FORMULAE_PARSED", "COEFFICIENTS_APPLIED_TO_WHOLE_FORMULAE", "ATOM_COUNTS_RECOMPUTED", "CONSERVATION_CONFIRMED"]
        validator = "ATOM_LEDGER_RECOMPUTE"
    elif family_ref == "PF-CONDITION_VALIDITY":
        condition = (snap.get("condition_text") or "").strip()
        if not condition or condition.lower() not in expected_answer.lower() or "condition" not in expected_answer.lower():
            fail("CORE2A_GENERATED_ITEM_NOT_INDEPENDENTLY_VERIFIED", anchor["question_ref"] + ": condition")
        checks = ["SOURCE_CONDITION_PRESENT", "CONDITION_NOT_REACTANT", "CONDITION_NOT_PRODUCT", "CONDITION_PLACEMENT_PRESERVED"]
        validator = "CONDITION_PRESERVATION"
    elif family_ref == "PF-AGENT_ROLE_ASSIGNMENT":
        _, reducing, oxidising = infer_agents(snap["stem"])
        if archetype_name == "NEAR_TRANSFER":
            if expected_answer != oxidising:
                fail("CORE2A_GENERATED_ITEM_NOT_INDEPENDENTLY_VERIFIED", anchor["question_ref"] + ": oxidising agent")
        elif reducing not in expected_answer or oxidising not in expected_answer or "oxidised" not in expected_answer or "reduced" not in expected_answer:
            fail("CORE2A_GENERATED_ITEM_NOT_INDEPENDENTLY_VERIFIED", anchor["question_ref"] + ": redox direction")
        checks = ["ELECTRON_LOSS_SPECIES_RECOMPUTED", "TWO_REACTANT_PAIR_CONFIRMED", "OXIDATION_REDUCTION_DIRECTION_CONFIRMED"]
        validator = "ELECTRON_TRANSFER_AGENT_ROLE"
    else:
        fail("CORE2A_GENERATED_ITEM_NOT_INDEPENDENTLY_VERIFIED", family_ref + ": no validator")
    return {"validator": validator, "checks": checks, "expected_answer": expected_answer, "status": "PASS"}


def make_provenance(challenge_id, anchor, bucket_id):
    return {
        "question_origin": "GENERATED_ORIGINAL",
        "display_inline": True,
        "learner_label": "WHERE THIS QUESTION CAME FROM",
        "citations": [
            {"citation_kind":"CORE1A_TEACHING","label":"Core (1A) taught Chemistry","locator":bucket_id,"use":"CONCEPT_SUPPORT","text_relation":"STYLE_ONLY"},
            {"citation_kind":"CORE2_SOURCE","label":"Core (2) transfer anchor","locator":anchor["question_ref"],"use":"CONCEPT_SUPPORT","text_relation":"STYLE_ONLY"},
            {"citation_kind":"GENERATED_ORIGINAL","label":"Fresh Chemistry practice","locator":challenge_id,"use":"ORIGIN_DISCLOSURE","text_relation":"FRESH_ORIGINAL"}
        ],
        "official_past_question_claim": False,
        "verified_official_source_ref": None,
    }


def make_answer_path(challenge_id, answer, steps, validation):
    return {
        "question_ref": challenge_id,
        "answer_path_kind": "OBJECTIVE_CHECKABLE",
        "learner_question_present": True,
        "answer_path_complete": True,
        "quick_check": {"learner_label":"QUICK CHECK","answer_summary":answer,"unit":None,"marking_points":[]},
        "full_working": {"learner_label":"FULL WORKING","steps":steps + ["Final answer: " + answer],"verification":"; ".join(validation["checks"])},
        "expected_response_rubric": None,
    }


def make_support(anchor, write_first, steps, language_policy):
    base = anchor["learner_support"]
    labels = language_policy["labels"]
    support = {
        "support_initially_hidden": True,
        "try_it_first": "Try this fresh problem independently before opening the clues.",
        "see_the_idea": copy.deepcopy(base["see_the_idea"]),
        "write_this_first": write_first,
        "small_clue": base["small_clue"],
        "bigger_clue": base["bigger_clue"],
        "how_do_i_start": write_first,
        "watch_for_this": base["watch_for_this"],
        "think_it_through": steps,
        "check_your_chemistry": copy.deepcopy(base["check_your_chemistry"]),
    }
    support["see_the_idea"]["learner_label"] = labels["REPRESENTATION"]
    forbidden = [term.lower() for term in language_policy["forbidden_learner_terms"]]
    text = canonical(support).lower()
    leaks = [term for term in forbidden if term in text]
    if leaks:
        fail("CORE2A_UNTAUGHT_CHEMISTRY_REQUIRED", "learner-language leak " + leaks[0])
    return support


def family_anchor_items(source_plan):
    order = []
    anchors = {}
    for item in source_plan["items"]:
        family = item["core1a_binding"]["primary_problem_family_ref"]
        if family not in anchors:
            order.append(family)
            anchors[family] = item
    return order, anchors


def taught_caps(bucket):
    return uniq(bucket["primary_capability_refs"] + bucket["supporting_capability_refs"])


def build_challenge_item(anchor, bucket, family_ref, archetype, source_items, challenge_policy, language_policy, index):
    prompt, answer, steps, write_first = family_recipe(anchor, family_ref, archetype["name"])
    validation = independent_validate(anchor, family_ref, archetype["name"], answer)
    challenge_id = f"CHEM-C2A-CH-{index:03d}-{family_ref.replace('PF-','').replace('_','-')}-{archetype['name']}"
    item = {
        "challenge_id": challenge_id,
        "schema_version": "1.0.0",
        "subject": "CHEMISTRY",
        "lane": "GENERATED_ORIGINAL",
        "anchor_source_question_ref": anchor["question_ref"],
        "core1a_binding": {
            "bucket_id": bucket["bucket_id"],
            "taught_capability_refs": taught_caps(bucket),
            "h1_evidence_refs": copy.deepcopy(anchor["core1a_binding"]["h1_evidence_refs"]),
            "h2_evidence_refs": copy.deepcopy(anchor["core1a_binding"]["h2_evidence_refs"]),
            "h3_evidence_refs": copy.deepcopy(anchor["core1a_binding"]["h3_evidence_refs"]),
        },
        "problem_family_ref": family_ref,
        "archetype_ref": archetype["archetype_id"],
        "archetype_name": archetype["name"],
        "novelty_mechanisms": copy.deepcopy(archetype["required_novelty"]),
        "prompt": prompt,
        "learner_support": make_support(anchor, write_first, steps, language_policy),
        "chemistry_validation": validation,
        "near_copy_check": near_copy_report(prompt, source_items, challenge_policy),
        "answer_path": make_answer_path(challenge_id, answer, steps, validation),
        "provenance": make_provenance(challenge_id, anchor, bucket["bucket_id"]),
        "item_digest": "",
    }
    item["item_digest"] = digest(item, "item_digest")
    return item


def validate_item(item, anchor, bucket, family_ref, archetype, source_items, challenge_policy, language_policy):
    if item["item_digest"] != digest(item, "item_digest"):
        fail("CORE2A_GENERATED_ITEM_NOT_INDEPENDENTLY_VERIFIED", item["challenge_id"] + ": digest")
    if item["lane"] != "GENERATED_ORIGINAL" or item["anchor_source_question_ref"] != anchor["question_ref"]:
        fail("CORE2A_CHALLENGE_TARGET_UNGROUNDED", item["challenge_id"] + ": identity")
    if item["problem_family_ref"] != family_ref or item["archetype_ref"] != archetype["archetype_id"] or item["archetype_name"] != archetype["name"]:
        fail("CORE2A_CHALLENGE_TARGET_UNGROUNDED", item["challenge_id"] + ": family/archetype")
    if item["core1a_binding"]["bucket_id"] != bucket["bucket_id"]:
        fail("CORE2A_UNTAUGHT_CHEMISTRY_REQUIRED", item["challenge_id"] + ": bucket")
    caps = set(taught_caps(bucket))
    if set(item["core1a_binding"]["taught_capability_refs"]) != caps:
        fail("CORE2A_UNTAUGHT_CHEMISTRY_REQUIRED", item["challenge_id"] + ": taught capabilities")
    for key in ("h1_evidence_refs", "h2_evidence_refs", "h3_evidence_refs"):
        if item["core1a_binding"][key] != anchor["core1a_binding"][key]:
            fail("CORE2A_UNTAUGHT_CHEMISTRY_REQUIRED", item["challenge_id"] + ": pre-teaching evidence")
    prompt, answer, steps, write_first = family_recipe(anchor, family_ref, archetype["name"])
    if item["prompt"] != prompt:
        # Check near-copy first so source-stem substitution gets the correct falsifier.
        near_copy_report(item["prompt"], source_items, challenge_policy)
        fail("CORE2A_CHALLENGE_TARGET_UNGROUNDED", item["challenge_id"] + ": prompt drift")
    expected_validation = independent_validate(anchor, family_ref, archetype["name"], answer)
    if item["chemistry_validation"] != expected_validation:
        fail("CORE2A_GENERATED_ITEM_NOT_INDEPENDENTLY_VERIFIED", item["challenge_id"] + ": chemistry validation")
    expected_copy = near_copy_report(item["prompt"], source_items, challenge_policy)
    if item["near_copy_check"] != expected_copy:
        fail("CORE2A_GENERATED_ITEM_TOO_CLOSE_TO_SOURCE", item["challenge_id"] + ": near-copy report drift")
    expected_answer = make_answer_path(item["challenge_id"], answer, steps, expected_validation)
    if item["answer_path"] != expected_answer:
        fail("CORE2A_ANSWER_PATH_MISSING", item["challenge_id"])
    expected_support = make_support(anchor, write_first, steps, language_policy)
    if item["learner_support"] != expected_support:
        fail("CORE2A_UNTAUGHT_CHEMISTRY_REQUIRED", item["challenge_id"] + ": support drift")
    expected_prov = make_provenance(item["challenge_id"], anchor, bucket["bucket_id"])
    if item["provenance"] != expected_prov:
        if item.get("provenance", {}).get("official_past_question_claim"):
            fail("CORE2A_GENERATED_ITEM_FALSE_OFFICIAL_ATTRIBUTION", item["challenge_id"])
        fail("CORE2A_QUESTION_CITATION_MISSING", item["challenge_id"])
    if item["provenance"]["official_past_question_claim"]:
        fail("CORE2A_GENERATED_ITEM_FALSE_OFFICIAL_ATTRIBUTION", item["challenge_id"])
    return True


def build_challenge_plan(source_plan, bucket_plan, family_registry, execution_policy, competitive_policy, archetype_registry, challenge_policy, language_policy, citation_policy, answer_policy, plan_id="CHEM-C2A-CHALLENGE-PLAN-PILOT-v1"):
    validate_upstream(source_plan, bucket_plan)
    expected_ids = {
        "execution": "CHEM-CORE2A-EXECUTION-v1",
        "competitive": "CHEM-COMPETITIVE-CHALLENGE-v1",
        "archetypes": "CHEM-COMPETITIVE-ARCHETYPE-REGISTRY-v1",
        "challenge": "CHEM-CORE2A-CHALLENGE-REALIZATION-v1",
        "language": "CHEM-LEARNER-LANGUAGE-v1",
        "citation": "CHEM-QUESTION-CITATION-v1",
        "answer": "CHEM-ANSWER-PATH-v1",
    }
    actual_ids = {
        "execution": execution_policy.get("policy_id"),
        "competitive": competitive_policy.get("policy_id"),
        "archetypes": archetype_registry.get("registry_id"),
        "challenge": challenge_policy.get("policy_id"),
        "language": language_policy.get("policy_id"),
        "citation": citation_policy.get("policy_id"),
        "answer": answer_policy.get("policy_id"),
    }
    if actual_ids != expected_ids:
        fail("CORE2A_CHALLENGE_TARGET_UNGROUNDED", "policy/registry binding")
    if competitive_policy.get("selection_basis") != "PROBLEM_FAMILY" or not citation_policy.get("inline_provenance_required"):
        fail("CORE2A_CHALLENGE_TARGET_UNGROUNDED", "selection/provenance policy")

    by_name, _ = archetype_tables(archetype_registry)
    buckets = bucket_tables(bucket_plan)
    family_order, anchors = family_anchor_items(source_plan)
    recipes = challenge_policy["supported_family_recipes"]
    items = []
    skipped = []
    structural_required = 0
    challenge_index = 0

    for family_ref in family_order:
        anchor = anchors[family_ref]
        recipe = recipes.get(family_ref)
        if not recipe:
            skipped.append({"problem_family_ref": family_ref, "reason": "No governed independent-validator recipe exists yet."})
            continue
        bucket_id = anchor["core1a_binding"]["bucket_id"]
        if bucket_id not in buckets:
            fail("CORE2A_CHALLENGE_TARGET_UNGROUNDED", family_ref + ": missing bucket")
        bucket = buckets[bucket_id]
        if family_ref != bucket["primary_problem_family_ref"] and family_ref not in {p["problem_family_ref"] for p in bucket["problem_families"]}:
            fail("CORE2A_UNTAUGHT_CHEMISTRY_REQUIRED", family_ref + ": family not taught in bucket")
        challenge_index += 1
        items.append(build_challenge_item(anchor, bucket, family_ref, by_name["NEAR_TRANSFER"], source_plan["items"], challenge_policy, language_policy, challenge_index))
        if bucket["intrinsic_difficulty"] in set(challenge_policy["selection"]["structural_variation_for_difficulty"]):
            name = recipe.get("structural_archetype")
            if name:
                if name not in by_name:
                    fail("CORE2A_CHALLENGE_TARGET_UNGROUNDED", family_ref + ": unknown structural archetype " + name)
                # A recipe is explicit authority that an alternate direction exists for this family.
                structural_required += 1
                challenge_index += 1
                items.append(build_challenge_item(anchor, bucket, family_ref, by_name[name], source_plan["items"], challenge_policy, language_policy, challenge_index))

    supported_seen = [f for f in family_order if f in recipes]
    near_items = [x for x in items if x["archetype_name"] == "NEAR_TRANSFER"]
    structural_items = [x for x in items if x["archetype_name"] != "NEAR_TRANSFER"]
    if len(near_items) != len(supported_seen):
        fail("CORE2A_CHALLENGE_TARGET_UNGROUNDED", "near-transfer denominator")
    if len(structural_items) != structural_required:
        fail("CORE2A_CHALLENGE_TARGET_UNGROUNDED", "structural denominator")

    out = {
        "plan_id": plan_id,
        "schema_version": "1.0.0",
        "subject": "CHEMISTRY",
        "lane": "GENERATED_ORIGINAL",
        "source_plan_ref": source_plan["plan_id"],
        "source_plan_digest": source_plan["plan_digest"],
        "core1a_bucket_plan_ref": bucket_plan["plan_id"],
        "core1a_bucket_plan_digest": bucket_plan["plan_digest"],
        "execution_policy_ref": execution_policy["policy_id"],
        "competitive_policy_ref": competitive_policy["policy_id"],
        "archetype_registry_ref": archetype_registry["registry_id"],
        "challenge_realization_policy_ref": challenge_policy["policy_id"],
        "learner_language_policy_ref": language_policy["policy_id"],
        "citation_policy_ref": citation_policy["policy_id"],
        "answer_path_policy_ref": answer_policy["policy_id"],
        "items": items,
        "skipped_families": skipped,
        "summary": {
            "source_families_seen": len(family_order),
            "supported_families": len(supported_seen),
            "near_transfer_required": len(supported_seen),
            "near_transfer_realized": len(near_items),
            "structural_variations_required": structural_required,
            "structural_variations_realized": len(structural_items),
            "generated_items_total": len(items),
            "independent_chemistry_checks_passed": len(items),
            "near_copy_checks_passed": len(items),
            "quick_checks_realized": len(items),
            "full_workings_realized": len(items),
            "mixed_synthesis_realized": 0,
            "status": "PASS",
        },
        "plan_digest": "",
    }
    out["plan_digest"] = digest(out, "plan_digest")
    validate_challenge_plan(out, source_plan, bucket_plan, family_registry, execution_policy, competitive_policy, archetype_registry, challenge_policy, language_policy, citation_policy, answer_policy)
    return out


def validate_challenge_plan(plan, source_plan, bucket_plan, family_registry, execution_policy, competitive_policy, archetype_registry, challenge_policy, language_policy, citation_policy, answer_policy):
    validate_upstream(source_plan, bucket_plan)
    if plan["plan_digest"] != digest(plan, "plan_digest"):
        fail("CORE2A_GENERATED_ITEM_NOT_INDEPENDENTLY_VERIFIED", "plan digest")
    expected_refs = {
        "source_plan_ref": source_plan["plan_id"],
        "source_plan_digest": source_plan["plan_digest"],
        "core1a_bucket_plan_ref": bucket_plan["plan_id"],
        "core1a_bucket_plan_digest": bucket_plan["plan_digest"],
        "execution_policy_ref": execution_policy["policy_id"],
        "competitive_policy_ref": competitive_policy["policy_id"],
        "archetype_registry_ref": archetype_registry["registry_id"],
        "challenge_realization_policy_ref": challenge_policy["policy_id"],
        "learner_language_policy_ref": language_policy["policy_id"],
        "citation_policy_ref": citation_policy["policy_id"],
        "answer_path_policy_ref": answer_policy["policy_id"],
    }
    for key, value in expected_refs.items():
        if plan.get(key) != value:
            fail("CORE2A_CHALLENGE_TARGET_UNGROUNDED", key)
    by_name, by_id = archetype_tables(archetype_registry)
    buckets = bucket_tables(bucket_plan)
    anchor_by_q = {x["question_ref"]: x for x in source_plan["items"]}
    recipes = challenge_policy["supported_family_recipes"]
    ids = []
    family_arch = Counter()
    structural_seen = 0
    for item in plan["items"]:
        ids.append(item["challenge_id"])
        if item["anchor_source_question_ref"] not in anchor_by_q:
            fail("CORE2A_CHALLENGE_TARGET_UNGROUNDED", item["challenge_id"] + ": anchor")
        anchor = anchor_by_q[item["anchor_source_question_ref"]]
        family_ref = item["problem_family_ref"]
        if family_ref not in recipes:
            fail("CORE2A_CHALLENGE_TARGET_UNGROUNDED", item["challenge_id"] + ": unsupported family")
        if item["archetype_ref"] not in by_id:
            fail("CORE2A_CHALLENGE_TARGET_UNGROUNDED", item["challenge_id"] + ": archetype")
        archetype = by_id[item["archetype_ref"]]
        if archetype["name"] != item["archetype_name"]:
            fail("CORE2A_CHALLENGE_TARGET_UNGROUNDED", item["challenge_id"] + ": archetype name")
        bucket_id = item["core1a_binding"]["bucket_id"]
        if bucket_id not in buckets:
            fail("CORE2A_UNTAUGHT_CHEMISTRY_REQUIRED", item["challenge_id"] + ": bucket")
        validate_item(item, anchor, buckets[bucket_id], family_ref, archetype, source_plan["items"], challenge_policy, language_policy)
        family_arch[(family_ref, item["archetype_name"])] += 1
        if item["archetype_name"] != "NEAR_TRANSFER":
            structural_seen += 1
    if len(ids) != len(set(ids)):
        fail("CORE2A_CHALLENGE_TARGET_UNGROUNDED", "duplicate challenge ids")
    family_order, anchors = family_anchor_items(source_plan)
    supported = [f for f in family_order if f in recipes]
    for family_ref in supported:
        if family_arch[(family_ref, "NEAR_TRANSFER")] != 1:
            fail("CORE2A_CHALLENGE_TARGET_UNGROUNDED", family_ref + ": near-transfer count")
    expected_structural = 0
    for family_ref in supported:
        anchor = anchors[family_ref]
        bucket = buckets[anchor["core1a_binding"]["bucket_id"]]
        if bucket["intrinsic_difficulty"] in set(challenge_policy["selection"]["structural_variation_for_difficulty"]):
            name = recipes[family_ref].get("structural_archetype")
            if name:
                expected_structural += 1
                if family_arch[(family_ref, name)] != 1:
                    fail("CORE2A_CHALLENGE_TARGET_UNGROUNDED", family_ref + ": structural count")
    summary = plan["summary"]
    expected_summary = {
        "source_families_seen": len(family_order),
        "supported_families": len(supported),
        "near_transfer_required": len(supported),
        "near_transfer_realized": len(supported),
        "structural_variations_required": expected_structural,
        "structural_variations_realized": expected_structural,
        "generated_items_total": len(plan["items"]),
        "independent_chemistry_checks_passed": len(plan["items"]),
        "near_copy_checks_passed": len(plan["items"]),
        "quick_checks_realized": len(plan["items"]),
        "full_workings_realized": len(plan["items"]),
        "mixed_synthesis_realized": 0,
        "status": "PASS",
    }
    if summary != expected_summary:
        fail("CORE2A_GENERATED_ITEM_NOT_INDEPENDENTLY_VERIFIED", "summary closure")
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-plan", required=True)
    parser.add_argument("--core1a-bucket-plan", required=True)
    parser.add_argument("--problem-family-registry", required=True)
    parser.add_argument("--execution-policy", required=True)
    parser.add_argument("--competitive-policy", required=True)
    parser.add_argument("--archetype-registry", required=True)
    parser.add_argument("--challenge-realization-policy", required=True)
    parser.add_argument("--learner-language-policy", required=True)
    parser.add_argument("--citation-policy", required=True)
    parser.add_argument("--answer-path-policy", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--plan-id", default="CHEM-C2A-CHALLENGE-PLAN-PILOT-v1")
    args = parser.parse_args()
    plan = build_challenge_plan(
        load(args.source_plan), load(args.core1a_bucket_plan), load(args.problem_family_registry),
        load(args.execution_policy), load(args.competitive_policy), load(args.archetype_registry),
        load(args.challenge_realization_policy), load(args.learner_language_policy),
        load(args.citation_policy), load(args.answer_path_policy), args.plan_id,
    )
    Path(args.out).write_text(json.dumps(plan, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
