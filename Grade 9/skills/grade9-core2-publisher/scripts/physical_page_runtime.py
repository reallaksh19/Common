#!/usr/bin/env python3
"""Physical-page instrumentation for Core (2) learner Study Guides.

The tracker records placement while ReportLab lays out the document. It does
not infer content custody from concatenated PDF text. Split Paragraphs remain
associated with the same content_ref, producing one fragment record per actual
physical page on which the semantic item is drawn.

Learner PDFs deliberately do not print internal section IDs, layout-relation
metadata, or Core (1) research IDs after every block. Those remain available in
the semantic models, PublicationStructure, LearningDesign and PhysicalPageMap.
Keeping machine custody out of the learner surface prevents traceability
metadata from creating artificial pagination and makes the rendered product
closer to the mature PR156/PR157 learner-first morphology.
"""
from __future__ import annotations

import hashlib
from collections import defaultdict
from pathlib import Path

import pymupdf as fitz
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import Flowable, PageBreak, Paragraph, SimpleDocTemplate, Spacer


DEFAULT_FINAL_PAGE_FILL = 0.18


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


class PlacementTracker:
    def __init__(self) -> None:
        self.fragments: dict[tuple[str, str], list[dict]] = defaultdict(list)
        self.learning_refs: dict[tuple[str, str], tuple[str, ...]] = {}
        self.intent_heading_pages: dict[str, set[int]] = defaultdict(set)

    def add_content(
        self,
        page_intent_id: str,
        content_ref: str,
        learning_design_refs: list[str],
        page: int,
        x: float,
        y: float,
        width: float,
        height: float,
    ) -> None:
        key = (page_intent_id, content_ref)
        self.learning_refs[key] = tuple(learning_design_refs)
        self.fragments[key].append(
            {
                "page": int(page),
                "x0": round(float(x), 3),
                "y0": round(float(y), 3),
                "x1": round(float(x + max(width, 0)), 3),
                "y1": round(float(y + max(height, 0)), 3),
            }
        )

    def add_intent_heading(self, page_intent_id: str, page: int) -> None:
        self.intent_heading_pages[page_intent_id].add(int(page))


class TrackedFlowable(Flowable):
    """Transparent wrapper preserving ReportLab split behavior and draw boxes."""

    def __init__(
        self,
        child: Flowable,
        tracker: PlacementTracker,
        page_intent_id: str,
        content_ref: str | None = None,
        learning_design_refs: list[str] | None = None,
        intent_heading: bool = False,
    ) -> None:
        super().__init__()
        self.child = child
        self.tracker = tracker
        self.page_intent_id = page_intent_id
        self.content_ref = content_ref
        self.learning_design_refs = list(learning_design_refs or [])
        self.intent_heading = intent_heading
        self.width = 0.0
        self.height = 0.0
        self.hAlign = getattr(child, "hAlign", "LEFT")

    def wrap(self, avail_width, avail_height):
        self.width, self.height = self.child.wrap(avail_width, avail_height)
        return self.width, self.height

    def split(self, avail_width, avail_height):
        pieces = self.child.split(avail_width, avail_height)
        return [
            TrackedFlowable(
                piece,
                self.tracker,
                self.page_intent_id,
                self.content_ref,
                self.learning_design_refs,
                self.intent_heading,
            )
            for piece in pieces
        ]

    def getSpaceBefore(self):
        return self.child.getSpaceBefore() if hasattr(self.child, "getSpaceBefore") else 0

    def getSpaceAfter(self):
        return self.child.getSpaceAfter() if hasattr(self.child, "getSpaceAfter") else 0

    def getKeepWithNext(self):
        return self.child.getKeepWithNext() if hasattr(self.child, "getKeepWithNext") else 0

    def drawOn(self, canv, x, y, _sW=0):
        page = canv.getPageNumber()
        if self.intent_heading:
            self.tracker.add_intent_heading(self.page_intent_id, page)
        if self.content_ref is not None:
            self.tracker.add_content(
                self.page_intent_id,
                self.content_ref,
                self.learning_design_refs,
                page,
                x,
                y,
                self.width,
                self.height,
            )
        return self.child.drawOn(canv, x, y, _sW)


def _tracked(child: Flowable, tracker: PlacementTracker, page_intent_id: str, item: dict) -> TrackedFlowable:
    return TrackedFlowable(
        child,
        tracker,
        page_intent_id,
        content_ref=item["item_id"],
        learning_design_refs=item.get("learning_design_refs", []),
    )


def _page_draw_fill(page) -> float:
    """Approximate occupied learner surface from reopened exact PDF bytes."""
    area = max(float(page.rect.width * page.rect.height), 1.0)
    occupied = 0.0
    for block in page.get_text("blocks"):
        if len(block) < 4:
            continue
        x0, y0, x1, y1 = map(float, block[:4])
        occupied += max(0.0, x1 - x0) * max(0.0, y1 - y0)
    for drawing in page.get_drawings():
        rect = drawing.get("rect")
        if rect is not None:
            occupied += max(0.0, float(rect.width)) * max(0.0, float(rect.height))
    return round(min(1.0, occupied / area), 6)


def build_page_map(model: dict, structure: dict, pdf_path: Path, tracker: PlacementTracker) -> dict:
    doc = fitz.open(pdf_path)
    page_count = len(doc)
    fill_by_page = {i + 1: _page_draw_fill(page) for i, page in enumerate(doc)}
    doc.close()

    placements = []
    pages_by_intent: dict[str, set[int]] = defaultdict(set)
    refs_by_page: dict[int, set[str]] = defaultdict(set)
    for (intent_id, content_ref), fragments in tracker.fragments.items():
        pages = sorted({row["page"] for row in fragments})
        pages_by_intent[intent_id].update(pages)
        for page in pages:
            refs_by_page[page].add(content_ref)
        row = {
            "content_ref": content_ref,
            "page_intent_id": intent_id,
            "physical_pages": pages,
            "fragments": fragments,
        }
        learning_refs = list(tracker.learning_refs.get((intent_id, content_ref), ()))
        if learning_refs:
            row["learning_design_refs"] = learning_refs
        placements.append(row)

    intent_rows = []
    intent_spec: dict[str, dict] = {}
    for intent in structure["study_guide"]["page_intents"]:
        iid = intent["page_intent_id"]
        pages = set(pages_by_intent.get(iid, set())) | set(tracker.intent_heading_pages.get(iid, set()))
        physical_pages = sorted(pages)
        row = {
            "page_intent_id": iid,
            "physical_pages": physical_pages,
            "content_refs": list(intent["content_refs"]),
            "pagination_policy": intent.get("pagination_policy", "PREFER_SINGLE_PAGE"),
            "split": len(physical_pages) > 1,
            "continuation_pages": physical_pages[1:],
            "whitespace_role": intent.get("whitespace_role", "NONE"),
        }
        if intent.get("max_physical_pages") is not None:
            row["max_physical_pages"] = intent["max_physical_pages"]
        if intent.get("minimum_final_page_fill") is not None:
            row["minimum_final_page_fill"] = intent["minimum_final_page_fill"]
        intent_rows.append(row)
        intent_spec[iid] = row

    starts: dict[int, set[str]] = defaultdict(set)
    continues: dict[int, set[str]] = defaultdict(set)
    for row in intent_rows:
        pages = row["physical_pages"]
        if pages:
            starts[pages[0]].add(row["page_intent_id"])
            for page in pages[1:]:
                continues[page].add(row["page_intent_id"])

    metrics = []
    for page in range(1, page_count + 1):
        fill = fill_by_page.get(page, 0.0)
        start_ids = sorted(starts.get(page, set()))
        continue_ids = sorted(continues.get(page, set()))
        whitespace_roles = {
            intent_spec[iid].get("whitespace_role", "NONE")
            for iid in start_ids + continue_ids
            if iid in intent_spec
        }
        declared_whitespace = next((x for x in whitespace_roles if x != "NONE"), None)
        thresholds = [
            float(intent_spec[iid].get("minimum_final_page_fill", DEFAULT_FINAL_PAGE_FILL))
            for iid in continue_ids
            if iid in intent_spec
        ]
        threshold = max(thresholds, default=DEFAULT_FINAL_PAGE_FILL)
        orphan = bool(continue_ids and not start_ids and not declared_whitespace and fill < threshold)
        if declared_whitespace:
            disposition = declared_whitespace
        elif orphan:
            disposition = "PATHOLOGICAL"
        else:
            disposition = "ACCEPTABLE"
        metric = {
            "page": page,
            "semantic_fill_ratio": fill,
            "starts_page_intent_ids": start_ids,
            "continues_page_intent_ids": continue_ids,
            "semantic_content_refs": sorted(refs_by_page.get(page, set())),
            "orphan_continuation": orphan,
            "underfill_disposition": disposition,
        }
        if not start_ids and not continue_ids:
            metric["reason"] = "Page is outside the main Study Guide page-intent surface (cover or appendix)."
        elif orphan:
            metric["reason"] = f"Continuation page fill {fill:.3f} is below declared/default threshold {threshold:.3f}."
        metrics.append(metric)

    return {
        "physical_page_map_id": "PPM-" + model["publication_id"],
        "schema_version": "1.0.0",
        "publication_structure_id": structure["publication_structure_id"],
        "publication_id": model["publication_id"],
        "pdf_role": "STUDY_GUIDE_PDF",
        "pdf_sha256": sha256_file(pdf_path),
        "physical_page_count": page_count,
        "page_intents": intent_rows,
        "content_placements": sorted(placements, key=lambda x: (x["page_intent_id"], x["physical_pages"], x["content_ref"])),
        "page_metrics": metrics,
    }


def page_map_path_for(study_pdf: Path) -> Path:
    suffix = "_Core2_Study_Guide.pdf"
    if study_pdf.name.endswith(suffix):
        return study_pdf.with_name(study_pdf.name[:-len(suffix)] + "_Core2_Physical_Page_Map.json")
    return study_pdf.with_suffix(".physical-pages.json")


def _arc_metadata(structure: dict) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for unit in structure["study_guide"]["learning_units"]:
        for step in unit["arc_steps"]:
            for ref in step["content_refs"]:
                out[ref] = {
                    "role": step["role"],
                    "support_state": step.get("support_state", ""),
                    "learner_visible_heading": step.get("learner_visible_heading"),
                }
    return out


_SELF_LABELED_PROMPT_PREFIX = {
    "NOTICE": "NOTICE",
    "GUIDED_1": "GUIDED 1",
    "INDEPENDENT_TRANSFER": "INDEPENDENT TRANSFER",
    "RETRIEVAL_CHECK": "RETRIEVAL CHECK",
}


def _content_carries_role_cue(meta: dict, item: dict) -> bool:
    """Return true when the learner prompt already prints its semantic role.

    This is intentionally narrow. We only suppress a separate H2 for generic
    pedagogical connectives whose text begins with the same learner-visible cue.
    Content/provenance is unchanged and the role remains explicit in structure.
    """
    if item.get("type") != "CONNECTIVE":
        return False
    prefix = _SELF_LABELED_PROMPT_PREFIX.get(meta.get("role"))
    if not prefix:
        return False
    return str(item.get("content", "")).strip().upper().startswith(prefix)


def make_study_renderer(impl):
    """Return a drop-in tracked, learner-first Study Guide renderer."""

    def render(model: dict, plan: dict, path: Path):
        structure = impl._CURRENT_STRUCTURE
        if structure is None:
            print("CORE2_PUBLICATION_STRUCTURE_MISSING")
            raise SystemExit(2)

        tracker = PlacementTracker()
        st = impl.legacy._styles("SG")
        doc = SimpleDocTemplate(
            str(path),
            pagesize=A4,
            rightMargin=18 * mm,
            leftMargin=18 * mm,
            topMargin=16 * mm,
            bottomMargin=16 * mm,
            title=model["title"],
            author="Grade 9–11 Core (2) Publisher",
        )
        items = impl._content_map(model)
        reps = impl._rep_map(plan)
        arc = _arc_metadata(structure)
        story: list[Flowable] = [
            Paragraph(impl.legacy.safe(model["title"]), st["h1"]),
            Paragraph(impl.legacy.safe(model.get("subtitle", "")), st["body"]),
            PageBreak(),
        ]

        for page_intent in structure["study_guide"]["page_intents"]:
            iid = page_intent["page_intent_id"]
            story.append(
                TrackedFlowable(
                    Paragraph(impl.legacy.safe(page_intent["cognitive_job"]), st["h1"]),
                    tracker,
                    iid,
                    intent_heading=True,
                )
            )
            previous_heading: tuple[str, str] | None = None
            for ref in page_intent["content_refs"]:
                meta = arc[ref]
                item = items[ref]
                role = meta.get("learner_visible_heading") or meta["role"].replace("_", " ")
                support = meta.get("support_state", "")
                heading_key = (role, support)
                if heading_key != previous_heading:
                    if not _content_carries_role_cue(meta, item):
                        heading = f"{role} · {support}" if support else role
                        story.append(Paragraph(impl.legacy.safe(heading), st["h2"]))
                    previous_heading = heading_key
                story.append(_tracked(Paragraph(impl.legacy.safe(item["content"]), st["body"]), tracker, iid, item))
                if item.get("representation_instance_id"):
                    rep = reps[item["representation_instance_id"]]
                    story.append(_tracked(impl.StructuredRepresentationFlowable(rep), tracker, iid, item))
                    story.append(Spacer(1, 3 * mm))
            story.append(PageBreak())

        app_by_letter = {"A": "appendix_A", "B": "appendix_B", "C": "appendix_C"}
        for letter in structure["study_guide"]["appendix_order"]:
            app = model[app_by_letter[letter]]
            story.append(Paragraph(impl.legacy.safe(app["title"]), st["h1"]))
            for i, item in enumerate(app["items"], 1):
                story.append(Paragraph(impl.legacy.safe(f"{i}. {item['content']}"), st["body"]))
            story.append(PageBreak())

        doc.build(story, onFirstPage=impl.legacy.page_number, onLaterPages=impl.legacy.page_number)
        page_map = build_page_map(model, structure, path, tracker)
        contracts = Path(__file__).resolve().parents[3] / "architecture" / "core2" / "contracts" / "v1"
        impl.legacy.validate_schema("physical-page-map.schema.json", page_map, contracts)
        out = page_map_path_for(path)
        impl.legacy.write_json(out, page_map)
        print("PHYSICAL_PAGE_MAP_EMITTED = PASS")

    return render


def finalize_page_map(original_argv: list[str], legacy, contracts: Path) -> list[str]:
    def arg_value(name: str) -> str | None:
        if name not in original_argv:
            return None
        i = original_argv.index(name)
        return original_argv[i + 1] if i + 1 < len(original_argv) else None

    out_value = arg_value("--out")
    prefix = arg_value("--prefix")
    if not out_value or not prefix:
        return ["cannot finalize PhysicalPageMap without --out and --prefix"]
    out = Path(out_value)
    map_path = out / f"{prefix}_Core2_Physical_Page_Map.json"
    if not map_path.exists():
        return []
    manifest_path = out / f"{prefix}_Core2_Publication_Manifest.json"
    if not manifest_path.exists():
        return ["publisher did not emit PublicationManifest before PhysicalPageMap finalization"]
    page_map = legacy.load(map_path)
    legacy.validate_schema("physical-page-map.schema.json", page_map, contracts)
    manifest = legacy.load(manifest_path)
    artifacts = [x for x in manifest.get("artifacts", []) if x.get("role") != "PHYSICAL_PAGE_MAP"]
    artifacts.append(legacy.artifact("PHYSICAL_PAGE_MAP", map_path, "application/json"))
    manifest["artifacts"] = artifacts
    manifest["package_digest"] = legacy.package_digest(artifacts)
    legacy.validate_schema("publication-manifest.schema.json", manifest, contracts)
    legacy.write_json(manifest_path, manifest)
    print("PHYSICAL_PAGE_MAP_PACKAGE_BINDING = PASS")
    return []
