#!/usr/bin/env python3
from pathlib import Path
import hashlib
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
VALIDATOR = HERE / "validate_roadmap_bindings.py"


def blob_sha(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def write_case(
    root: Path,
    *,
    roadmaps: str,
    review: str,
    state: str = "READY_FOR_NEXT_LEG",
    include_section: bool = True,
):
    chain = "TEST-ROADMAP"
    chain_dir = root / "agents" / "chains" / chain
    endpoint_dir = chain_dir / "endpoints"
    endpoint_dir.mkdir(parents=True, exist_ok=True)
    endpoint_lines = [
        f"CHAIN_ID: {chain}",
        "ENDPOINT_ID: EP-0001",
        f"ROADMAPS: {roadmaps}",
        f"ROADMAP_REVIEW_STATUS: {review}",
        f"STATE: {state}",
    ]
    if include_section:
        endpoint_lines.extend(
            [
                "",
                "### Owner roadmaps",
                "Binding/discovery/alignment evidence recorded for test fixture.",
            ]
        )
    (endpoint_dir / "EP-0001.md").write_text(
        "\n".join(endpoint_lines) + "\n", encoding="utf-8"
    )
    (chain_dir / "ACTIVE.md").write_text(
        "\n".join(
            [
                "CHAIN_STATE_VERSION: 2",
                f"CHAIN_ID: {chain}",
                "ACTIVE_ENDPOINT: EP-0001",
                f"ACTIVE_ENDPOINT_FILE: agents/chains/{chain}/endpoints/EP-0001.md",
                f"ROADMAPS: {roadmaps}",
                f"ROADMAP_REVIEW_STATUS: {review}",
                f"STATE: {state}",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def run(root: Path):
    return subprocess.run(
        [sys.executable, str(VALIDATOR), str(root)],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )


def expect(name: str, result, expected_rc: int) -> bool:
    if result.returncode != expected_rc:
        print(f"FAIL SELF-TEST: {name}; rc={result.returncode}; expected={expected_rc}")
        print(result.stdout)
        return False
    print(f"PASS SELF-TEST: {name}")
    return True


def main():
    ok = True

    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        roadmap = root / "docs" / "roadmaps" / "Overallroadmap_wrc.md"
        roadmap.parent.mkdir(parents=True, exist_ok=True)
        data = b"ROADMAP_AUTHORITY: OWNER_CONTROLLED\n"
        roadmap.write_bytes(data)
        binding = f"docs/roadmaps/Overallroadmap_wrc.md@{blob_sha(data)}"
        write_case(root, roadmaps=binding, review="COMPLETE")
        ok &= expect("valid pinned roadmap binding", run(root), 0)

    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        roadmap = root / "docs" / "roadmaps" / "Overallroadmap_wrc.md"
        roadmap.parent.mkdir(parents=True, exist_ok=True)
        old = b"old\n"
        roadmap.write_bytes(b"new\n")
        binding = f"docs/roadmaps/Overallroadmap_wrc.md@{blob_sha(old)}"
        write_case(root, roadmaps=binding, review="COMPLETE")
        ok &= expect("stale roadmap blob rejected", run(root), 1)

    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        write_case(
            root,
            roadmaps="NONE — policy-only test; no product roadmap applies",
            review="NOT_APPLICABLE",
        )
        ok &= expect("explicit no-applicable-roadmap accepted", run(root), 0)

    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        write_case(root, roadmaps="NONE — test", review="COMPLETE")
        ok &= expect("NONE with COMPLETE rejected", run(root), 1)

    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        missing = "docs/roadmaps/missing.md@" + "0" * 40
        write_case(root, roadmaps=missing, review="COMPLETE")
        ok &= expect("missing roadmap path rejected", run(root), 1)

    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        roadmap = root / "docs" / "roadmaps" / "Overallroadmap_wrc.md"
        roadmap.parent.mkdir(parents=True, exist_ok=True)
        data = b"blocked\n"
        roadmap.write_bytes(data)
        binding = f"docs/roadmaps/Overallroadmap_wrc.md@{blob_sha(data)}"
        write_case(root, roadmaps=binding, review="BLOCKED", state="READY_FOR_NEXT_LEG")
        ok &= expect("blocked roadmap review requires blocked chain", run(root), 1)

    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        write_case(
            root,
            roadmaps="NONE — policy-only test",
            review="NOT_APPLICABLE",
            include_section=False,
        )
        ok &= expect("missing Owner roadmaps evidence section rejected", run(root), 1)

    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
