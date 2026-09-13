#!/usr/bin/env python3
"""Typography and layout safety (M-UPGRADE-2 item 7).

Proof readability and layout safety are release semantics, not cosmetic QA. A page can be
structurally valid, deterministic and inside its bounds while still being unreadable,
collided or silently truncated. The seven-topic stress test produced all four failure modes:

* Euclid — large unused whitespace and microtype on the same page, and two-up solution
  blocks that collided;
* Polynomials — multipart workspace overflowing its allocated rectangle;
* Linear Equations — a following panel covering the tail of an option set;
* Number Systems — large empty lined regions beside generic verify boxes.

This module consumes the same ``math-rendered-object-map`` the source ledger uses, so the
two phases audit one object model rather than two. The map now also carries
``container_id`` (so containment can be told from collision), ``content_height_pt`` (so
measured height can be told from allocated height) and ``response_mode`` (so workspace can
follow the response the question actually demands).
"""
from __future__ import annotations

import copy
import hashlib
import json
from itertools import combinations
from pathlib import Path
from typing import Any

PHASE = Path(__file__).resolve().parents[1]
DEFAULT_REGISTRY = PHASE / "registry" / "math-typography-role-registry.json"
DEFAULT_POLICY = PHASE / "policies" / "math-layout-safety-policy.json"

FALSIFIERS = (
    "LEARNER_TEXT_BELOW_MIN_READABLE_SIZE",
    "DIAGRAM_LABEL_BELOW_MIN_READABLE_SIZE",
    "MICROTYPE_USED_WHILE_EXPANDABLE_SPACE_EXISTS",
    "LAYOUT_COMPONENT_INTERSECTION",
    "CONTENT_OVERFLOW",
    "NEGATIVE_REMAINING_HEIGHT",
    "WORKSPACE_RESPONSE_MODE_MISMATCH",
    "SOLUTION_BLOCK_PACKING_OVERFLOW",
    "LAYOUT_SAFETY_GATE_FAILED",
)


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(value: Any, omit: str | None = None) -> str:
    item = copy.deepcopy(value)
    if omit and isinstance(item, dict):
        item.pop(omit, None)
    return hashlib.sha256(canonical(item).encode("utf-8")).hexdigest()


def load(path: Path | str) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def fail(code: str, detail: str = "") -> None:
    raise ValueError(f"{code}:{detail}" if detail else code)


def _overlap(a: dict, b: dict) -> float:
    dx = min(a["x"] + a["w"], b["x"] + b["w"]) - max(a["x"], b["x"])
    dy = min(a["y"] + a["h"], b["y"] + b["h"]) - max(a["y"], b["y"])
    return min(dx, dy) if dx > 0 and dy > 0 else 0.0


def _area(box: dict) -> float:
    return box["w"] * box["h"]


# --------------------------------------------------------------------------
# measure-then-pack
# --------------------------------------------------------------------------
def measure_then_pack(blocks: list[dict], available_height_pt: float,
                      gap_pt: float) -> list[list[str]]:
    """Assign solution blocks to pages from their measured heights.

    One solution per page is correct when the content demands it; two-up is an
    optimisation. A block taller than a whole page still gets its own page, and the caller
    is told about it by ``CONTENT_OVERFLOW`` rather than by silent truncation.
    """
    pages: list[list[str]] = []
    current: list[str] = []
    used = 0.0
    for block in blocks:
        height = float(block["height_pt"])
        needed = height if not current else height + gap_pt
        if current and used + needed > available_height_pt:
            pages.append(current)
            current, used = [block["block_id"]], height
        else:
            current.append(block["block_id"])
            used += needed
    if current:
        pages.append(current)
    return pages


# --------------------------------------------------------------------------
# the audit
# --------------------------------------------------------------------------
def audit_layout(object_map: dict, *, registry: dict | None = None,
                 policy: dict | None = None) -> dict:
    """Build the layout audit. Never raises; ``status`` carries the verdict."""
    registry = registry if registry is not None else load(DEFAULT_REGISTRY)
    policy = policy if policy is not None else load(DEFAULT_POLICY)

    roles = registry["roles"]
    workspace_requirements = registry["workspace_requirements"]
    tolerance = float(registry["collision_policy"]["sibling_overlap_tolerance_pt"])
    whitespace_threshold = float(registry["whitespace_policy"]["unused_page_area_ratio_threshold"])
    gap = float(registry["solution_packing_policy"]["inter_block_gap_pt"])

    objects = object_map["objects"]
    margin = float(object_map["printable_margin_pt"])
    page_w = float(object_map["page_width_pt"])
    page_h = float(object_map["page_height_pt"])
    printable_area = max((page_w - 2 * margin) * (page_h - 2 * margin), 1.0)
    printable_height = page_h - 2 * margin

    # -- typography -------------------------------------------------------
    below_minimum: list[str] = []
    below_preferred: list[str] = []
    roles_used: set[str] = set()
    for obj in objects:
        role = obj["typography_role"]
        roles_used.add(role)
        spec = roles.get(role)
        if spec is None:
            below_minimum.append(f"{obj['object_id']}:UNKNOWN_ROLE:{role}")
            continue
        size = float(obj["font_size_pt"])
        if size < float(spec["min_pt"]):
            below_minimum.append(f"{obj['object_id']}:{role}:{size}<{spec['min_pt']}")
        elif size < float(spec["preferred_pt"]):
            below_preferred.append(f"{obj['object_id']}:{role}:{size}<{spec['preferred_pt']}")

    # -- sibling collisions ----------------------------------------------
    intersections: list[str] = []
    pairs_checked = 0
    by_page_container: dict[tuple[int, str], list[dict]] = {}
    for obj in objects:
        key = (obj["page"], obj.get("container_id") or "__page__")
        by_page_container.setdefault(key, []).append(obj)
    for (page, container), siblings in sorted(by_page_container.items()):
        for a, b in combinations(sorted(siblings, key=lambda o: o["object_id"]), 2):
            pairs_checked += 1
            if _overlap(a["box"], b["box"]) > tolerance:
                intersections.append(
                    f"p{page}:{container}:{a['object_id']}~{b['object_id']}")

    # -- measured vs allocated -------------------------------------------
    content_overflow: list[str] = []
    negative_remaining: list[str] = []
    measured = 0
    children: dict[str, list[dict]] = {}
    for obj in objects:
        if obj.get("container_id"):
            children.setdefault(obj["container_id"], []).append(obj)
    by_id = {o["object_id"]: o for o in objects}
    for obj in objects:
        content = obj.get("content_height_pt")
        if content is None:
            continue
        measured += 1
        if float(content) > obj["box"]["h"] + tolerance:
            content_overflow.append(
                f"{obj['object_id']}:{content}>{obj['box']['h']}")
    for container_id, kids in sorted(children.items()):
        container = by_id.get(container_id)
        if container is None:
            continue
        needed = sum(float(k.get("content_height_pt") or k["box"]["h"]) for k in kids)
        if needed - container["box"]["h"] > tolerance:
            negative_remaining.append(
                f"{container_id}:needs={needed:.1f}>{container['box']['h']:.1f}")

    # -- workspace follows response mode ---------------------------------
    mismatched: list[str] = []
    response_modes: set[str] = set()
    workspaces = [o for o in objects if o["kind"] == "WORKSPACE"]
    for workspace in workspaces:
        mode = workspace.get("response_mode")
        if not mode:
            mismatched.append(f"{workspace['object_id']}:NO_RESPONSE_MODE")
            continue
        response_modes.add(mode)
        requirement = workspace_requirements.get(mode)
        if requirement is None:
            mismatched.append(f"{workspace['object_id']}:UNKNOWN_RESPONSE_MODE:{mode}")
            continue
        if workspace["box"]["h"] + tolerance < float(requirement["min_height_pt"]):
            mismatched.append(f"{workspace['object_id']}:{mode}:"
                              f"{workspace['box']['h']:.1f}<{requirement['min_height_pt']}")

    # -- solution packing --------------------------------------------------
    overflowing_pages: list[str] = []
    solution_pages: dict[int, list[dict]] = {}
    for obj in objects:
        if obj["kind"] == "SOLUTION":
            solution_pages.setdefault(obj["page"], []).append(obj)
    for page, blocks in sorted(solution_pages.items()):
        needed = sum(float(b.get("content_height_pt") or b["box"]["h"]) for b in blocks)
        needed += gap * max(len(blocks) - 1, 0)
        if needed - printable_height > tolerance:
            overflowing_pages.append(
                f"p{page}:{len(blocks)}_blocks:{needed:.1f}>{printable_height:.1f}")

    # -- whitespace vs microtype ------------------------------------------
    unused_by_page: list[dict] = []
    microtype: list[str] = []
    pages = sorted({o["page"] for o in objects})
    for page in pages:
        page_objects = [o for o in objects if o["page"] == page]
        covered = sum(_area(o["box"]) for o in page_objects
                      if not o.get("container_id"))
        unused_ratio = max(0.0, min(1.0, 1.0 - covered / printable_area))
        unused_by_page.append({"page": page, "unused_ratio": round(unused_ratio, 4)})
        if unused_ratio >= whitespace_threshold:
            for obj in page_objects:
                spec = roles.get(obj["typography_role"])
                if spec is None or not spec.get("learner_visible"):
                    continue
                if float(obj["font_size_pt"]) < float(spec["preferred_pt"]):
                    microtype.append(f"p{page}:{obj['object_id']}:"
                                     f"{obj['font_size_pt']}<{spec['preferred_pt']}"
                                     f"@unused={unused_ratio:.2f}")

    blocked = bool(below_minimum or intersections or content_overflow
                   or negative_remaining or mismatched or overflowing_pages or microtype)
    audit = {
        "schema_version": "1.0.0",
        "subject": "MATHEMATICS",
        "map_ref": object_map["map_id"],
        "status": "BLOCKED" if blocked else "PASS",
        "pages": object_map["page_count"],
        "typography": {
            "objects_checked": len(objects),
            "roles_used": sorted(roles_used),
            "below_minimum": sorted(below_minimum),
            "below_preferred": sorted(below_preferred),
        },
        "collisions": {
            "sibling_pairs_checked": pairs_checked,
            "intersections": sorted(intersections),
        },
        "overflow": {
            "measured_objects": measured,
            "content_overflow": sorted(content_overflow),
            "negative_remaining_height": sorted(negative_remaining),
        },
        "workspace": {
            "checked": len(workspaces),
            "response_modes": sorted(response_modes),
            "mismatched": sorted(mismatched),
        },
        "solution_packing": {
            "mode": registry["solution_packing_policy"]["mode"],
            "pages_checked": len(solution_pages),
            "overflowing_pages": sorted(overflowing_pages),
        },
        "whitespace": {
            "unused_area_ratio_by_page": unused_by_page,
            "microtype_with_space_available": sorted(microtype),
        },
        "release_meaning": "PUBLICATION_ENGINEERING only; visual usability and expert "
                           "review PENDING",
    }
    audit["audit_id"] = "MATH-LSA-" + digest(audit)[:16]
    audit["audit_digest"] = digest(audit, "audit_digest")
    return audit


def assert_layout_safe(object_map: dict, *, registry: dict | None = None,
                       policy: dict | None = None) -> dict:
    """Fail-closed wrapper: every finding is raised under its own named gate."""
    registry = registry if registry is not None else load(DEFAULT_REGISTRY)
    audit = audit_layout(object_map, registry=registry, policy=policy)
    roles = registry["roles"]
    failures: list[str] = []

    for entry in audit["typography"]["below_minimum"]:
        role = entry.split(":")[1] if ":" in entry else ""
        code = ("DIAGRAM_LABEL_BELOW_MIN_READABLE_SIZE" if role == "DIAGRAM_LABEL"
                else "LEARNER_TEXT_BELOW_MIN_READABLE_SIZE")
        failures.append(f"{code}:{entry}")
    for entry in audit["collisions"]["intersections"]:
        failures.append(f"LAYOUT_COMPONENT_INTERSECTION:{entry}")
    for entry in audit["overflow"]["content_overflow"]:
        failures.append(f"CONTENT_OVERFLOW:{entry}")
    for entry in audit["overflow"]["negative_remaining_height"]:
        failures.append(f"NEGATIVE_REMAINING_HEIGHT:{entry}")
    for entry in audit["workspace"]["mismatched"]:
        failures.append(f"WORKSPACE_RESPONSE_MODE_MISMATCH:{entry}")
    for entry in audit["solution_packing"]["overflowing_pages"]:
        failures.append(f"SOLUTION_BLOCK_PACKING_OVERFLOW:{entry}")
    for entry in audit["whitespace"]["microtype_with_space_available"]:
        failures.append(f"MICROTYPE_USED_WHILE_EXPANDABLE_SPACE_EXISTS:{entry}")

    if failures:
        fail("LAYOUT_SAFETY_GATE_FAILED", "|".join(sorted(set(failures))))
    _ = roles
    return audit
