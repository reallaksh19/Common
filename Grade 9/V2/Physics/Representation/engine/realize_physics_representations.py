#!/usr/bin/env python3
"""P-H representation realization: draw every spec and emit hash-bound custody.

    PhysicsRepresentationBundle
  -> deterministic ReportLab render of every representation
  -> PhysicalPageMap carrying, per figure, the measured vector-operation count
     and the measured ink box emitted *while drawing*
  -> exact PDF SHA-256 bound into the page map
  -> independent custody audit (ported from PR #161 / #196)

This is the file that makes ``TEACHING_PRIMITIVE_LABEL_ONLY_NOT_REALIZED``
impossible to pass silently: the evidence recorded here is measured at draw
time, not planned.
"""
import argparse, copy, hashlib, json, sys
from pathlib import Path

D = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(D / "engine"))

from reportlab.pdfgen import canvas as rl_canvas  # noqa: E402
from physics_primitive_renderer import render_primitive  # noqa: E402
from physics_page_custody import reconciliation_errors  # noqa: E402


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


def fail(code, detail=""):
    raise ValueError(f"{code}: {detail}" if detail else code)


def realize(bundle, registry, contract, out_dir, artifact_name="physics-representations.pdf"):
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    page = contract["page"]
    place = contract["placement"]
    W, H = page["width_pt"], page["height_pt"]
    margin = page["margin_pt"]
    fig_w, fig_h, gap = place["figure_width_pt"], place["figure_height_pt"], place["figure_gap_pt"]
    tolerance = place["ink_tolerance_pt"]
    minimums = {p["primitive_id"]: p["minimum_vector_ops"] for p in registry["primitives"]}

    pdf_path = out / artifact_name
    c = rl_canvas.Canvas(str(pdf_path), pagesize=(W, H), invariant=1, pageCompression=1)
    c.setTitle("Physics V2 P-H representation realization")
    c.setAuthor("Physics V2 P-H deterministic representation renderer")

    page_no = 1
    y = H - margin - fig_h
    placements, intents, page_refs = [], [], {1: []}

    # one page intent per capability, so a capability's figures reconcile as a unit
    order = []
    for spec in bundle["representations"]:
        cap = spec["capability_ref"]
        if not order or order[-1][0] != cap:
            order.append((cap, []))
        order[-1][1].append(spec)

    for cap, specs in order:
        intent_id = "PI-" + cap
        pages_used = []
        for spec in specs:
            if y < margin:
                c.showPage()
                page_no += 1
                page_refs[page_no] = []
                y = H - margin - fig_h
            evidence = render_primitive(
                spec["primitive_id"], spec["render_params"], c, (margin, y, fig_w, fig_h)
            )
            if evidence["vector_ops"] < spec["minimum_vector_ops"]:
                fail("TEACHING_PRIMITIVE_LABEL_ONLY_NOT_REALIZED",
                     f"{spec['representation_id']}:{evidence['vector_ops']}<{spec['minimum_vector_ops']}")
            placements.append({
                "content_ref": spec["representation_id"],
                "page_intent_id": intent_id,
                "primitive": spec["primitive_id"],
                "page": page_no,
                "fragment_kind": "START",
                "x0": margin, "y0": y, "x1": margin + fig_w, "y1": y + fig_h,
                "ink_bbox": evidence["ink_bbox"],
                "vector_ops": evidence["vector_ops"],
                "text_ops": evidence["text_ops"],
                "op_histogram": evidence["op_histogram"],
                "quantitative_grounding": spec["quantitative_grounding"],
            })
            page_refs[page_no].append(spec["representation_id"])
            if page_no not in pages_used:
                pages_used.append(page_no)
            y -= fig_h + gap
        intents.append({
            "page_intent_id": intent_id,
            "capability_ref": cap,
            "physical_pages": sorted(pages_used),
            "content_refs": [s["representation_id"] for s in specs],
            "split": len(pages_used) > 1,
            "continuation_pages": sorted(pages_used)[1:],
        })

    c.save()
    pdf_bytes = pdf_path.read_bytes()
    pdf_sha = sha_bytes(pdf_bytes)

    metrics = []
    for p in range(1, page_no + 1):
        refs = page_refs.get(p, [])
        violations = sum(
            1 for x in placements
            if x["page"] == p and x["ink_bbox"] and not (
                x["x0"] - tolerance <= x["ink_bbox"]["x0"] and x["ink_bbox"]["x1"] <= x["x1"] + tolerance
                and x["y0"] - tolerance <= x["ink_bbox"]["y0"] and x["ink_bbox"]["y1"] <= x["y1"] + tolerance
            )
        )
        metrics.append({
            "page": p,
            "semantic_content_refs": refs,
            "orphan_continuation": False,
            "bounds_violations": violations,
            "underfill_disposition": "ACCEPTABLE" if refs else "PATHOLOGICAL",
        })

    page_map = {
        "physical_page_map_id": "PHY-P-H-PPM-" + bundle["bundle_id"],
        "schema_version": "1.0.0",
        "subject": "PHYSICS",
        "bundle_ref": bundle["bundle_id"],
        "bundle_digest": bundle["bundle_digest"],
        "artifact_path": artifact_name,
        "artifact_sha256": pdf_sha,
        "artifact_bytes": len(pdf_bytes),
        "physical_page_count": page_no,
        "page_width_pt": W,
        "page_height_pt": H,
        "actual_placement_evidence": True,
        "page_intents": intents,
        "content_placements": placements,
        "page_metrics": metrics,
        "realization_summary": {
            "figure_count": len(placements),
            "total_vector_ops": sum(p["vector_ops"] for p in placements),
            "total_text_ops": sum(p["text_ops"] for p in placements),
            "label_only_figure_count": sum(1 for p in placements if p["vector_ops"] <= 0),
            "source_grounded_figure_count": sum(
                1 for p in placements if p["quantitative_grounding"] == "SOURCE_QUANTITIES"
            ),
        },
        "page_map_digest": "",
    }
    page_map["page_map_digest"] = digest(page_map, "page_map_digest")

    errors = reconciliation_errors(page_map, W, H, minimums, tolerance)
    if errors:
        fail("PHYSICAL_PAGE_CUSTODY_FAILURE", "; ".join(errors[:6]))

    map_path = out / "physical_page_map.json"
    map_path.write_text(json.dumps(page_map, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                        encoding="utf-8")
    return page_map, pdf_path


def audit(page_map, pdf_bytes, registry, contract):
    """Independent recomputation of custody from the bytes and the map."""
    if sha_bytes(pdf_bytes) != page_map["artifact_sha256"]:
        fail("EXACT_ARTIFACT_HASH_MISMATCH")
    if page_map["page_map_digest"] != digest(page_map, "page_map_digest"):
        fail("PHYSICAL_PAGE_CUSTODY_FAILURE", "page map digest")
    minimums = {p["primitive_id"]: p["minimum_vector_ops"] for p in registry["primitives"]}
    errors = reconciliation_errors(
        page_map, page_map["page_width_pt"], page_map["page_height_pt"],
        minimums, contract["placement"]["ink_tolerance_pt"],
    )
    if errors:
        fail("PHYSICAL_PAGE_CUSTODY_FAILURE", "; ".join(errors[:6]))
    if page_map["realization_summary"]["label_only_figure_count"]:
        fail("TEACHING_PRIMITIVE_LABEL_ONLY_NOT_REALIZED", "audit")
    return True


def main():
    ap = argparse.ArgumentParser()
    for x in ["bundle", "primitive-registry", "render-contract", "out-dir"]:
        ap.add_argument("--" + x, required=True)
    a = ap.parse_args()
    bundle = load(a.bundle)
    registry = load(a.primitive_registry)
    contract = load(a.render_contract)
    page_map, pdf_path = realize(bundle, registry, contract, a.out_dir)
    audit(page_map, Path(pdf_path).read_bytes(), registry, contract)
    print(
        f"PHY P-H realization: {page_map['realization_summary']['figure_count']} figures, "
        f"{page_map['realization_summary']['total_vector_ops']} vector operations, "
        f"{page_map['physical_page_count']} pages, sha256={page_map['artifact_sha256'][:16]}"
    )


if __name__ == "__main__":
    main()
