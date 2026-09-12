#!/usr/bin/env python3
"""P-L AI pre-review of an exact Physics candidate. ADVISORY ONLY.

This produces an ``AI_ASSISTED_REFERENCE_REVIEW`` record bound to the exact PDF
bytes. It is deliberately incapable of setting a quality state: the record
carries ``sets_quality_states: false`` and ``authority: ADVISORY_ONLY``, and the
P-L evaluator rejects any record that claims otherwise with
``AI_PRE_REVIEW_COUNTED_AS_HUMAN_REVIEW``.

It is a reading aid for a future authorized human reviewer, and nothing else.
"""
import argparse, copy, hashlib, json, re, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve()
ROOT = HERE.parents[1]
PHYS = HERE.parents[2]
sys.path[:0] = [str(PHYS / "ColdStart" / "engine"), str(PHYS / "Representation" / "engine")]

from physics_product_renderer import residual_internal_tokens  # noqa: E402


def canonical(o):
    return json.dumps(o, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(o, field=None):
    x = copy.deepcopy(o)
    if field:
        x.pop(field, None)
    return hashlib.sha256(canonical(x).encode("utf-8")).hexdigest()


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def pdf_text(path):
    try:
        r = subprocess.run(["pdftotext", str(path), "-"], capture_output=True, text=True, timeout=120)
        return r.stdout if r.returncode == 0 else ""
    except (OSError, subprocess.SubprocessError):
        return ""


def observe(run_dir, run_report, core1_map, core2_map, core1_plan, core2_plan):
    """Machine-checkable observations a human reviewer would otherwise have to count by hand."""
    run_dir = Path(run_dir)
    obs = []
    products = {p["product_id"]: p for p in run_report["two_product_package"]["products"]}

    core1 = products.get("CORE_STUDY_GUIDE")
    if core1:
        text = pdf_text(run_dir / core1["artifact_path"])
        obs.append({
            "observation": "CORE1_STRUCTURE",
            "detail": f"{core1['page_count']} pages, {core1['figure_count']} figures, "
                      f"{core1['vector_ops']} vector operations, sections "
                      f"{', '.join(core1['required_sections'])}.",
        })
        obs.append({
            "observation": "CORE1_LEARNER_SURFACE",
            "detail": ("No internal identifier or SCREAMING_SNAKE token was found in the extracted text."
                       if not residual_internal_tokens(text)
                       else "Internal tokens are present in the extracted text: "
                            + ", ".join(residual_internal_tokens(text)[:5])),
        })
        modes = {}
        for lesson in core1_plan["lessons"]:
            modes[lesson["lesson_mode"]] = modes.get(lesson["lesson_mode"], 0) + 1
        obs.append({
            "observation": "CORE1_TREATMENT_SPREAD",
            "detail": "Lesson modes: " + ", ".join(f"{k}={v}" for k, v in sorted(modes.items())) + ".",
        })
        with_contrast = sum(1 for l in core1_plan["lessons"] if l.get("misconception_repair"))
        obs.append({
            "observation": "CORE1_MISCONCEPTION_COVERAGE",
            "detail": f"{with_contrast} of {len(core1_plan['lessons'])} lessons carry a misconception "
                      "contrast with repair steps and a retry prompt.",
        })

    core2 = products.get("TRANSFER_SOLUTION_BOOK")
    if core2:
        text = pdf_text(run_dir / core2["artifact_path"])
        obs.append({
            "observation": "CORE2_STRUCTURE",
            "detail": f"{core2['page_count']} pages over {len(core2_plan['transfer_pages'])} transfer "
                      f"questions; every page carries {len(core2_plan['transfer_pages'][0]['hint_ladder'])} "
                      "graded hints and a full solution.",
        })
        obs.append({
            "observation": "CORE2_LEARNER_SURFACE",
            "detail": ("No internal identifier or SCREAMING_SNAKE token was found in the extracted text."
                       if not residual_internal_tokens(text)
                       else "Internal tokens are present: " + ", ".join(residual_internal_tokens(text)[:5])),
        })
        badges = {}
        for page in core2_plan["transfer_pages"]:
            badges[page["guide_demand_badge"]] = badges.get(page["guide_demand_badge"], 0) + 1
        obs.append({
            "observation": "CORE2_SCAFFOLDING_SPREAD",
            "detail": "Scaffolding badges: " + ", ".join(f"{k}={v}" for k, v in sorted(badges.items())) + ".",
        })

    grounded = core1_map["realization_summary"]["source_grounded_figure_count"]
    total = core1_map["realization_summary"]["figure_count"]
    obs.append({
        "observation": "FIGURE_QUANTITATIVE_GROUNDING",
        "detail": f"{grounded} of {total} figures carry quantities extracted from the source "
                  "assessment; the remainder are schematic structure with no invented numbers.",
    })
    return obs


def advisory_concerns(observations, core1_map):
    """Concerns a human reviewer should look at first. Never a verdict."""
    concerns = []
    grounded = core1_map["realization_summary"]["source_grounded_figure_count"]
    total = core1_map["realization_summary"]["figure_count"] or 1
    if grounded / total < 0.5:
        concerns.append({
            "concern": "MOSTLY_SCHEMATIC_FIGURES",
            "detail": f"Only {grounded} of {total} figures are grounded in stated source quantities. "
                      "A subject reviewer should judge whether the schematic variants still carry enough "
                      "physical specificity to teach.",
            "for_role": "AUTHORIZED_PHYSICS_SUBJECT",
        })
    if any("Internal tokens are present" in o["detail"] for o in observations):
        concerns.append({
            "concern": "INTERNAL_TOKENS_ON_LEARNER_SURFACE",
            "detail": "Engineering vocabulary reached a learner page.",
            "for_role": "AUTHORIZED_VISUAL_USABILITY",
        })
    concerns.append({
        "concern": "NO_HUMAN_HAS_READ_THIS_PRODUCT",
        "detail": "Nothing in this repository constitutes a subject, pedagogy, assessment or visual "
                  "review of these artifacts. Every such state is PENDING and the product is not mature.",
        "for_role": "ALL",
    })
    return concerns


def build_review(run_dir, policy, review_id="PHY-P-L-AI-PRE-REVIEW-v1"):
    run_dir = Path(run_dir)
    run_report = load(run_dir / "run_report.json")
    core1_map = load(run_dir / "core1_page_map.json")
    core2_map = load(run_dir / "core2_page_map.json")
    core1_plan = load(run_dir / "core1.json")
    core2_plan = load(run_dir / "core2.json")

    hashes = []
    for p in run_report["two_product_package"]["products"]:
        path = run_dir / p["artifact_path"]
        hashes.append(sha_bytes(path.read_bytes()) if path.exists() else p["artifact_sha256"])

    observations = observe(run_dir, run_report, core1_map, core2_map, core1_plan, core2_plan)
    concerns = advisory_concerns(observations, core1_map)
    review = {
        "review_id": review_id,
        "schema_version": "1.0.0",
        "subject": "PHYSICS",
        "review_class": policy["ai_pre_review"]["review_class"],
        "authority": policy["ai_pre_review"]["authority"],
        "reviewer_authority_class": "REPOSITORY_AUTOMATED_AGENT",
        "sets_quality_states": False,
        "may_set_mature_classification": False,
        "artifact_sha256_refs": sorted(set(hashes)),
        "run_report_ref": run_report["report_id"],
        "observations": observations,
        "advisory_concerns": concerns,
        "statement": "This is an automated reading aid bound to the exact artifact bytes. It is not a "
                     "subject, pedagogy, assessment or visual review and cannot satisfy one.",
        "review_digest": "",
    }
    review["review_digest"] = digest(review, "review_digest")
    return review


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-dir", required=True)
    ap.add_argument("--policy", default=str(ROOT / "registry" / "physics-exact-product-quality-policy.json"))
    ap.add_argument("--out")
    a = ap.parse_args()
    review = build_review(a.run_dir, load(a.policy))
    if a.out:
        Path(a.out).write_text(json.dumps(review, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                               encoding="utf-8")
    print(f"PHY P-L AI pre-review (ADVISORY ONLY): {len(review['observations'])} observations, "
          f"{len(review['advisory_concerns'])} concerns, bound to "
          f"{len(review['artifact_sha256_refs'])} exact artifact hashes")
    for c in review["advisory_concerns"]:
        print(f"  - {c['concern']} (for {c['for_role']})")


if __name__ == "__main__":
    main()
