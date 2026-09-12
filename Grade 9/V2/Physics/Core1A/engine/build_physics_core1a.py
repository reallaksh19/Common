#!/usr/bin/env python3
"""Compile a PhysicsCore1StudyPlan into a Core1A learner-publication plan.

Core1A owns publication composition, not Physics authority. It rearranges fields already
owned by P-G into a stable Grade-9 learning-page grammar and reports when the upstream
content is too generic to deserve a mature-textbook claim.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
ROOT = HERE.parents[1]
POLICY_PATH = ROOT / "registry" / "physics-core1a-publication-policy.json"


def canonical(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(obj, field=None):
    x = copy.deepcopy(obj)
    if field:
        x.pop(field, None)
    return hashlib.sha256(canonical(x).encode("utf-8")).hexdigest()


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save(path, obj):
    Path(path).write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def fail(code, detail=""):
    raise ValueError(f"{code}: {detail}" if detail else code)


def text(value):
    return str(value or "").strip()


def nonempty(*values):
    return [text(v) for v in values if text(v)]


def human(ref):
    s = text(ref)
    for prefix in (
        "PHY-CAP-", "PHY-PF-", "PHY-MODEL-", "PHY-LAW-", "PHY-CORE1-",
        "OBLIGATION_LEVEL:", "OBLIGATION_REP:", "REQUIRED:", "PROBE:",
    ):
        if s.startswith(prefix):
            s = s[len(prefix):]
            break
    s = re.sub(r"[_-]+", " ", s).strip().lower()
    return s[:1].upper() + s[1:] if s else "Physics concept"


def module(mid, kind, title, body, source_fields, *, answer=False, work=0, figure=None):
    return {
        "module_id": mid,
        "kind": kind,
        "title": title,
        "body": [text(x) for x in body if text(x)],
        "source_fields": sorted(set(source_fields)),
        "answer_revealing": bool(answer),
        "work_space_lines": int(work),
        "figure_request": figure,
    }


def figure_request(lesson, caption, mode="PREFER_SOURCE_GROUNDED"):
    reps = list(lesson.get("representation_requirements") or [])
    return {
        "mode": mode if reps else "SCHEMATIC_ONLY",
        "representation_requirements": reps,
        "caption": caption,
    }


def concept_badge(lesson):
    helper = text(lesson.get("concept_helper"))
    if helper:
        words = re.findall(r"[A-Za-z0-9]+", helper)
        if words:
            return " ".join(words[:5]).upper()
    family = human(lesson.get("primary_pck_family"))
    words = family.split()
    return " ".join(words[:4]).upper()


def template_findings(lesson, policy):
    haystacks = []
    worked = lesson.get("worked_example") or {}
    haystacks.extend([worked.get("prompt", "")])
    for step in worked.get("reasoning_steps") or []:
        haystacks.append(step.get("text", ""))
    for key in ("guided_attempt", "faded_attempt", "independent_attempt", "probe_attempt"):
        item = lesson.get(key) or {}
        haystacks.append(item.get("prompt", ""))
    joined = " ".join(text(x).lower() for x in haystacks)
    findings = []
    for phrase in policy["template_only_phrases"]:
        if phrase.lower() in joined:
            findings.append("CORE1A_TEMPLATE_ONLY_CONTENT")
            break
    return sorted(set(findings))


def worked_body(worked):
    if not worked:
        return []
    lines = [text(worked.get("prompt"))]
    for i, step in enumerate(worked.get("reasoning_steps") or [], 1):
        role = human(step.get("role"))
        lines.append(f"{i}. {role}: {text(step.get('text'))}")
    checks = [human(x) for x in worked.get("verification_steps") or []]
    if checks:
        lines.append("Check: " + "; ".join(checks))
    return [x for x in lines if x]


def practice_body(item):
    if not item:
        return []
    body = [text(item.get("prompt"))]
    checks = [human(x) for x in item.get("verification_steps") or []]
    if checks:
        body.append("After solving, check: " + "; ".join(checks))
    return body


def compile_full(lesson, lid, policy):
    mods = []
    badge = concept_badge(lesson)
    mods.append(module(f"{lid}-badge", "CONCEPT_BADGE", "Concept", [badge], ["concept_helper", "primary_pck_family"]))

    anchor = nonempty(lesson.get("see_phenomenon_anchor"), lesson.get("see_phase"))
    mods.append(module(
        f"{lid}-anchor", "REAL_WORLD_ANCHOR", "Start with the physical story", anchor,
        ["see_phenomenon_anchor", "see_phase"],
        figure=figure_request(lesson, "Figure: the physical situation before equations are chosen."),
    ))

    see_body = nonempty(lesson.get("see_system_frame_sign"), lesson.get("realize_phase"))
    see_body.extend([f"{i}. {text(x)}" for i, x in enumerate(lesson.get("realize_reconstruction_steps") or [], 1)])
    mods.append(module(
        f"{lid}-see", "SEE_IT", "See it → represent it", see_body,
        ["see_system_frame_sign", "realize_phase", "realize_reconstruction_steps"],
        figure=figure_request(lesson, "Figure: a representation that preserves the physical state."),
    ))

    key = nonempty(lesson.get("ordinary_language_explanation"), lesson.get("understand_phase"))
    mods.append(module(
        f"{lid}-key", "KEY_IDEA", "Key idea", key,
        ["ordinary_language_explanation", "understand_phase"],
    ))

    validity = list(lesson.get("model_validity_conditions") or [])
    if text(lesson.get("understand_relation_and_validity")):
        validity.insert(0, text(lesson["understand_relation_and_validity"]))
    mods.append(module(
        f"{lid}-model", "MODEL_CHECK", "Can I use this model?", validity or ["Check the stated conditions before using the relation."],
        ["understand_relation_and_validity", "model_validity_conditions", "model_validity_required"],
    ))

    worked = lesson.get("worked_example")
    mods.append(module(
        f"{lid}-worked", "WORKED_EXAMPLE", "Worked example", worked_body(worked),
        ["worked_example"], answer=True,
        figure=figure_request(lesson, "Figure: representation used by the worked example."),
    ))

    repair = lesson.get("misconception_repair") or {}
    trap = []
    if repair:
        trap = [
            "Common thought: " + text(repair.get("wrong_model")),
            "Why it feels reasonable: " + text(repair.get("why_plausible")),
            "Minimal contrast: " + text(repair.get("minimal_contrast")),
        ]
        trap.extend(["Repair: " + text(x) for x in repair.get("repair_steps") or []])
        if text(repair.get("retry_prompt")):
            trap.append("Retry: " + text(repair["retry_prompt"]))
    mods.append(module(
        f"{lid}-trap", "COMMON_TRAP", "Common trap", trap or ["Compare the tempting shortcut with the physical model before accepting it."],
        ["misconception_repair"],
    ))

    guided = lesson.get("guided_attempt")
    faded = lesson.get("faded_attempt")
    independent = lesson.get("independent_attempt")
    mods.append(module(
        f"{lid}-guided", "GUIDED_PRACTICE", "Try now — guided", practice_body(guided),
        ["guided_attempt"], work=max(3, policy["page"]["minimum_work_space_lines_guided"]),
    ))
    mods.append(module(
        f"{lid}-faded", "FADED_PRACTICE", "Try again — less help", practice_body(faded),
        ["faded_attempt"], work=max(3, policy["page"]["minimum_work_space_lines_guided"]),
    ))
    mods.append(module(
        f"{lid}-independent", "INDEPENDENT_PRACTICE", "Your turn", practice_body(independent),
        ["independent_attempt"], work=max(5, policy["page"]["minimum_work_space_lines_independent"]),
    ))

    checks = [human(x) for x in lesson.get("verification_steps") or []]
    if text(lesson.get("physical_verification")):
        checks.insert(0, text(lesson["physical_verification"]))
    mods.append(module(
        f"{lid}-check", "PHYSICAL_CHECK", "Check before you accept the answer", checks,
        ["physical_verification", "verification_steps"],
    ))

    selfcheck = []
    if repair and text(repair.get("retry_prompt")):
        selfcheck.append(text(repair["retry_prompt"]))
    if independent and text(independent.get("prompt")):
        selfcheck.append("Without looking back, name the first move you would make on the independent problem.")
    selfcheck.append("Explain the idea in one sentence without using a formula first.")
    mods.append(module(
        f"{lid}-self", "SELF_CHECK", "30-second check", selfcheck,
        ["misconception_repair.retry_prompt", "independent_attempt.prompt"],
    ))

    mods.append(module(
        f"{lid}-transfer", "TRANSFER_BRIDGE", "Where this idea goes next", [lesson.get("transfer_bridge")],
        ["transfer_bridge"],
    ))
    return mods


def compile_verify(lesson, lid):
    badge = concept_badge(lesson)
    return [
        module(f"{lid}-badge", "CONCEPT_BADGE", "Concept", [badge], ["concept_helper", "primary_pck_family"]),
        module(f"{lid}-key", "KEY_IDEA", "Activate", nonempty(lesson.get("activation")), ["activation"]),
        module(f"{lid}-ind", "INDEPENDENT_PRACTICE", "Verify independently", practice_body(lesson.get("independent_attempt")), ["independent_attempt"], work=5),
        module(f"{lid}-check", "PHYSICAL_CHECK", "Check", [human(x) for x in lesson.get("verification_steps") or []], ["verification_steps"]),
        module(f"{lid}-self", "SELF_CHECK", "30-second check", ["State the physical reason your answer is plausible."], ["verification_steps"]),
        module(f"{lid}-transfer", "TRANSFER_BRIDGE", "Transfer", nonempty(lesson.get("transfer_bridge")), ["transfer_bridge"]),
    ]


def compile_probe(lesson, lid):
    badge = concept_badge(lesson)
    probe = lesson.get("probe_attempt") or lesson.get("independent_attempt") or {}
    return [
        module(f"{lid}-badge", "CONCEPT_BADGE", "Concept", [badge], ["concept_helper", "primary_pck_family"]),
        module(f"{lid}-probe", "PROBE", "Try this before reading an explanation", practice_body(probe), ["probe_attempt", "independent_attempt"], work=6),
        module(f"{lid}-check", "PHYSICAL_CHECK", "Check", [human(x) for x in lesson.get("verification_steps") or []], ["verification_steps"]),
        module(f"{lid}-self", "SELF_CHECK", "What did the probe reveal?", ["Which part felt uncertain: the physical story, the representation, the relation, or the check?"], ["probe_requirements"]),
    ]


def validate_modules(lesson_plan, policy):
    mode = lesson_plan["lesson_mode"]
    kinds = [m["kind"] for m in lesson_plan["modules"]]
    if mode == "FULL_LEARNING":
        missing = [k for k in policy["full_learning_required_modules"] if k not in kinds]
        if missing:
            fail("CORE1A_REQUIRED_MODULE_MISSING", f"{lesson_plan['lesson_ref']}:{','.join(missing)}")
    elif mode == "CONCISE_VERIFY_ONLY":
        illegal = [k for k in kinds if k not in policy["verify_only_allowed_modules"]]
        if illegal:
            fail("CORE1A_VERIFY_ONLY_EXPANDED_TO_RETEACH", f"{lesson_plan['lesson_ref']}:{','.join(illegal)}")
    elif mode == "PROBE":
        illegal = [k for k in kinds if k not in policy["probe_allowed_modules"]]
        if illegal or ("PROBE" in kinds and kinds.index("PROBE") > 1):
            fail("CORE1A_RETEACH_BEFORE_PROBE", lesson_plan["lesson_ref"])


def build_publication_plan(core1, policy=None):
    policy = policy or load(POLICY_PATH)
    if core1.get("subject") != "PHYSICS":
        fail("CORE1A_SEMANTIC_DRIFT", "subject")
    if core1.get("pedagogy_model") != "SEE_REALIZE_UNDERSTAND":
        fail("CORE1A_SEMANTIC_DRIFT", "unexpected pedagogy model")

    lessons = []
    counts = {"FULL_LEARNING": 0, "CONCISE_VERIFY_ONLY": 0, "PROBE": 0}
    template_count = 0
    for lesson in core1.get("lessons") or []:
        mode = lesson["lesson_mode"]
        counts[mode] = counts.get(mode, 0) + 1
        lid = lesson["lesson_id"]
        if mode == "FULL_LEARNING":
            mods = compile_full(lesson, lid, policy)
        elif mode == "CONCISE_VERIFY_ONLY":
            mods = compile_verify(lesson, lid)
        elif mode == "PROBE":
            mods = compile_probe(lesson, lid)
        else:
            fail("CORE1A_SEMANTIC_DRIFT", f"unknown lesson mode {mode}")
        findings = template_findings(lesson, policy)
        template_count += int("CORE1A_TEMPLATE_ONLY_CONTENT" in findings)
        rec = {
            "lesson_ref": lid,
            "capability_ref": lesson["capability_ref"],
            "lesson_mode": mode,
            "treatment": lesson["treatment"],
            "concept_badge": concept_badge(lesson),
            "publication_template": policy["templates"][mode],
            "modules": mods,
            "content_maturity_findings": findings,
        }
        validate_modules(rec, policy)
        lessons.append(rec)

    aps = core1.get("appendices") or {}
    for key in ("appendix_a", "appendix_b", "appendix_c"):
        if not (aps.get(key) or {}).get("present"):
            fail("CORE1A_SEMANTIC_DRIFT", f"{key} missing")

    plan = {
        "plan_id": "PHY-P-GA-CORE1A-" + core1["plan_id"],
        "schema_version": "1.0.0",
        "subject": "PHYSICS",
        "product_id": "CORE_STUDY_GUIDE",
        "upstream_core1_plan_id": core1["plan_id"],
        "upstream_core1_digest": core1["plan_digest"],
        "two_product_topology_preserved": True,
        "lessons": lessons,
        "appendices": {
            "appendix_a_present": True,
            "appendix_b_present": True,
            "appendix_c_present": True,
        },
        "quality_summary": {
            "template_only_content_count": template_count,
            "full_learning_count": counts.get("FULL_LEARNING", 0),
            "compact_count": counts.get("CONCISE_VERIFY_ONLY", 0),
            "probe_count": counts.get("PROBE", 0),
        },
        "plan_digest": "",
    }
    plan["plan_digest"] = digest(plan, "plan_digest")
    return plan


def main(argv=None):
    p = argparse.ArgumentParser(description="Compile Physics Core (1) into Core (1A) publication plan and PDF")
    p.add_argument("--core1", required=True)
    p.add_argument("--out-dir", required=True)
    p.add_argument("--representations")
    p.add_argument("--plan-only", action="store_true")
    args = p.parse_args(argv)

    core1 = load(args.core1)
    policy = load(POLICY_PATH)
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    plan = build_publication_plan(core1, policy)
    plan_path = out / "physics-core1a-publication-plan.json"
    save(plan_path, plan)

    if not args.plan_only:
        sys.path.insert(0, str(HERE.parent))
        from render_physics_core1a import render_core1a  # noqa: E402
        reps = load(args.representations) if args.representations else None
        report = render_core1a(core1, plan, out / "physics-core-study-guide.pdf", policy, reps)
        save(out / "physics-core1a-quality-report.json", report)

    print(plan_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
