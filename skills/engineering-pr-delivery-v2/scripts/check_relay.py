#!/usr/bin/env python3
from pathlib import Path
import argparse
import re
import subprocess
import sys


def run(script: str, *args: str) -> int:
    return subprocess.run([sys.executable, str(Path(__file__).with_name(script)), *args]).returncode


def protocol_version(path: str | None):
    if not path:
        return None
    text = Path(path).read_text(encoding="utf-8")
    m = re.search(r"(?mi)^\s*QUALIFICATION_PROTOCOL_VERSION\s*:\s*([^\n#]+)", text)
    return m.group(1).strip() if m else None


def repo_root_for(relay: Path):
    if relay.is_file():
        return relay.parent.parent if relay.parent.name == "agents" else relay.parent
    if relay.name == "chains" and relay.parent.name == "agents":
        return relay.parent.parent
    return relay


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("relay")
    parser.add_argument("legacy_answer", nargs="?")
    parser.add_argument("legacy_verdict", nargs="?")
    parser.add_argument("--endpoint")
    parser.add_argument("--admission")
    parser.add_argument("--answer")
    parser.add_argument("--verdict")
    parser.add_argument("--reconciliation")
    parser.add_argument("--active", help="ACTIVE.md for the material leg; enables current adoption gate")
    parser.add_argument("--base-ref", help="material-leg base ref; enables legacy-write and prework audit")
    parser.add_argument("--head-ref", default="HEAD")
    args = parser.parse_args()

    answer = args.answer or args.legacy_answer
    verdict = args.verdict or args.legacy_verdict
    relay = Path(args.relay).resolve()
    root = repo_root_for(relay)

    if relay.is_file():
        rc = run("validate_agentchain.py", str(relay))
        structure = "legacy relay index"
    else:
        rc = 0
        for script in (
            "validate_repository_overlay.py",
            "validate_chain_store.py",
            "validate_roadmap_bindings.py",
            "validate_handover_snapshot.py",
            "validate_handover_readiness.py",
            "validate_qualification_questions.py",
            "validate_qualification_profile.py",
            "validate_engineering_question_payload.py",
            "validate_owner_qualification_baseline.py",
            "validate_work_item_exclusivity.py",
            "validate_material_leg_history.py",
        ):
            rc |= run(script, str(root if script in {
                "validate_repository_overlay.py", "validate_engineering_question_payload.py",
                "validate_owner_qualification_baseline.py", "validate_work_item_exclusivity.py",
                "validate_handover_readiness.py", "validate_material_leg_history.py"
            } else relay))
        structure = "project-overlay + canonical relay + roadmap + handover-v2 + readiness + expert-question + concrete-payload + Owner-baseline + exact-work-item + material-history gates"

    if args.active:
        rc |= run("validate_leg_adoption.py", str(root), args.active)
    if args.base_ref:
        rc |= run("validate_legacy_relay_diff.py", str(root), args.base_ref, args.head_ref)
        if not args.active:
            print("FAIL: --base-ref material-leg audit requires --active for prework history proof", file=sys.stderr)
            rc |= 1
        else:
            rc |= run("validate_prework_history.py", str(root), args.base_ref, args.head_ref, args.active)

    v3 = protocol_version(answer) == "3" or protocol_version(verdict) == "3"
    if args.admission:
        if not args.endpoint:
            print("FAIL: --admission requires --endpoint", file=sys.stderr)
            rc |= 1
        else:
            admission_args = [args.endpoint, args.admission]
            if answer:
                admission_args.append(answer)
            rc |= run("validate_question_set_admission.py", *admission_args)
    elif v3 and (answer or verdict):
        print("FAIL: version-3 takeover qualification requires --endpoint and --admission first", file=sys.stderr)
        rc |= 1

    if answer:
        rc |= run("validate_candidate_answer.py", answer)
    if verdict:
        if not answer:
            print("FAIL: verdict requires candidate answer", file=sys.stderr)
            rc |= 1
        else:
            rc |= run("validate_qualification.py", answer, verdict)

    if args.reconciliation:
        if not verdict:
            print("FAIL: reconciliation requires completed qualification verdict", file=sys.stderr)
            rc |= 1
        else:
            rc |= run("validate_post_basis_drift.py", args.reconciliation)

    if rc == 0:
        print(f"PASS: {structure}")
        if args.active:
            print("PASS: material leg has current Common basis, exact work-item custody, handover-v2 readiness, Owner-baseline discovery and profile-v2 Q1-Q5")
        if args.base_ref:
            print("PASS: current material-leg diff avoids legacy relay writes and Git history proves pre-work Q1-Q5 preceded mutation")
        if not relay.is_file():
            print("PASS: completed AUTO/material batches have append-only receipts with no hidden inter-leg/trailing material")
        if v3 and verdict and not args.reconciliation:
            print("NOTE: qualified READ_ONLY; post-basis reconciliation is still required before WRITE_ALLOWED.")
    return 1 if rc else 0


if __name__ == "__main__":
    raise SystemExit(main())
