from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "Item_Metadata.csv"

COLS = "item_id,source_year,source_question_number,source_paper_url,source_key_url,source_authority,key_status,question_mark_value,official_answer,primary_domain,main_topic_id,secondary_domains,mechanisms,visible_clues,hidden_invariant,first_move,prerequisites,decision_boundaries,figure_required,source_integrity_status,provenance,student_use_disposition,teacher_use_disposition,recognition_difficulty,representation_difficulty,execution_difficulty,transfer_difficulty,answer_verified_independently,classification_review_status,classification_confidence,notes".split(",")

rows = []


def historical(item, year, q, paper, key, authority, key_status, marks, answer, secondary, mechanisms, clues, invariant, first_move, boundaries, integrity, notes, recognition="MEDIUM", representation="MEDIUM", execution="MEDIUM", transfer="HIGH"):
    rows.append(dict(
        item_id=item,
        source_year=year,
        source_question_number=q,
        source_paper_url=paper,
        source_key_url=key,
        source_authority=authority,
        key_status=key_status,
        question_mark_value=marks,
        official_answer=answer,
        primary_domain="GEO",
        main_topic_id="IOQM-G9-GEO-04",
        secondary_domains=secondary,
        mechanisms=mechanisms,
        visible_clues=clues,
        hidden_invariant=invariant,
        first_move=first_move,
        prerequisites="GEO02 stable angle/polygon interface",
        decision_boundaries=boundaries,
        figure_required="false",
        source_integrity_status=integrity,
        provenance="HISTORICAL_VALIDATED_PYQ",
        student_use_disposition="PYQ_ANCHOR",
        teacher_use_disposition="PYQ_ANCHOR",
        recognition_difficulty=recognition,
        representation_difficulty=representation,
        execution_difficulty=execution,
        transfer_difficulty=transfer,
        answer_verified_independently="true",
        classification_review_status="INDEPENDENT_STATIC_REVIEWED",
        classification_confidence="HIGH",
        notes=notes,
    ))


p25 = "https://drive.google.com/file/d/13_o0QUmfqZJxc7IWrz6yqKivuyVC-wku/view"
k25 = "https://drive.google.com/file/d/18jKJ_2rUxgOlbg-2If_-oHzcH8JxzwT5/view"
p24 = "https://drive.google.com/file/d/1z7-3fJuk5BW9zx9SUEumcnuuE080pQJq/view"
k24 = "https://drive.google.com/file/d/1Li9nwrQ5to5OEkyEbCL9Q1AM2oa5rYsm/view"
p23 = "https://www.mtai.org.in/wp-content/uploads/2023/09/IOQM_Sep_2023_Question-paper-with-answer-key.pdf"

historical(
    "IOQM-2025-Q19", 2025, 19, p25, k25, "MTAI_OFFICIAL_SHARED_DRIVE", "FINAL_OFFICIAL", 3, 29, "ALG",
    "coordinate_circle;square;right_triangle",
    "right triangle 1,2; inscribed square; one vertex on circle centered at A",
    "line membership plus circle equation determines square side",
    "place right triangle on axes after identifying circle condition",
    "synthetic angle chase vs low-variable coordinates",
    "CLEAN_OFFICIAL_PAGE_VISUAL_CLOSED",
    "Official M1 printed page 7 rendered at 200 dpi; text-only, no printed figure; independent audit PASS.",
)

historical(
    "IOQM-2025-Q23", 2025, 23, p25, k25, "MTAI_OFFICIAL_SHARED_DRIVE", "FINAL_OFFICIAL", 5, 3, "ALG",
    "cyclicity;rectangle;coordinate_elimination",
    "rectangle; M,N on adjacent sides; equal lengths; C,D,M,N concyclic",
    "cyclicity is decisive non-generic constraint",
    "normalize rectangle and impose non-degenerate cyclicity before elimination",
    "generic rectangle algebra vs cyclic constraint; degenerate vs canonical reading",
    "CLEAN_OFFICIAL_PAGE_VISUAL_CLOSED_NONDEGENERATE",
    "Official M1 printed page 8 rendered at 200 dpi; no printed figure; final key rejects degenerate N=C branch; audit PASS.",
    recognition="HIGH", representation="HIGH", execution="HIGH",
)

historical(
    "IOQM-2025-Q30", 2025, 30, p25, k25, "MTAI_OFFICIAL_SHARED_DRIVE", "FINAL_OFFICIAL", 5, 10, "ALG",
    "intersecting_circles;internal_tangency;common_chord",
    "outer radius 10; two internally tangent inner circles; common intersections A,B; right angle OAB",
    "line of centres perpendicular common chord; radius sum invariant",
    "align common chord/centre direction before metric equations",
    "full radical-axis theory vs local common-chord fact",
    "CLEAN_OFFICIAL_PAGE_VISUAL_CLOSED",
    "Official M1 printed page 10 rendered at 200 dpi; text-only, no printed figure; audit PASS.",
    recognition="HIGH", representation="HIGH", execution="HIGH",
)

historical(
    "IOQM-2024-Q17", 2024, 17, p24, k24, "MTAI_OFFICIAL_SHARED_DRIVE", "FINAL_OFFICIAL", 3, 25, "ALG",
    "circumcircle;chord;isosceles_symmetry;coordinates",
    "isosceles 20,20,30; altitude midpoint; chord through midpoint parallel base",
    "symmetry axis locates circumcentre; chord distance closes metric target",
    "place base symmetrically and use circle chord-distance relation",
    "generic chord theorem vs symmetry coordinates",
    "CLEAN_OFFICIAL_PAGE_VISUAL_CLOSED",
    "Official English printed page 6 rendered at 200 dpi; text-only, no printed figure; audit PASS.",
)

historical(
    "IOQM-2023-Q15", 2023, 15, p23, p23, "HBCSE_LINKED_MTAI", "HBCSE_LINKED_MTAI_EMBEDDED_KEY", 3, 3, "ALG",
    "circumcentres;unit_square;coordinates;symmetric_elimination",
    "unit square; M,N on adjacent sides; small triangle perimeter 2; two circumcentres",
    "perpendicular-bisector coordinates plus symmetric perimeter relation",
    "coordinate the square and solve circumcentre systems",
    "long synthetic chase vs orthogonal coordinates",
    "CLEAN_VALIDATED_PAGE_VISUAL_CLOSED",
    "HBCSE-linked MTAI printed page 5 screenshot inspected; text-only, no printed figure; audit PASS.",
    recognition="HIGH", representation="HIGH", execution="HIGH",
)


def authored(prefix, n, provenance, student_use, teacher_use, label, mechanisms):
    for i in range(1, n + 1):
        rows.append(dict(
            item_id=f"GEO04-{prefix}{i:02d}",
            primary_domain="GEO",
            main_topic_id="IOQM-G9-GEO-04",
            mechanisms=mechanisms,
            figure_required="false",
            source_integrity_status="CLEAN_VALIDATED",
            provenance=provenance,
            student_use_disposition=student_use,
            teacher_use_disposition=teacher_use,
            answer_verified_independently="true",
            classification_review_status="INDEPENDENT_STATIC_REVIEWED",
            classification_confidence="HIGH",
            notes=f"{label} {i}; synchronized teacher key.",
        ))


authored("R", 16, "AUTHOR_CREATED_FOUNDATION", "RECOGNITION_FIRST_LINE", "DIAGNOSTIC", "04 Lab item", "recognition;theorem_legality;first_move")
authored("P", 22, "AUTHOR_CREATED_PRACTICE_TRANSFER", "PRACTICE_TRANSFER", "DIAGNOSTIC", "05 Practice/Transfer item", "circle_structure;practice;transfer")
authored("M", 12, "AUTHOR_CREATED_MASTERY", "H0_MASTERY", "MASTERY_KEY", "06 Mixed Mastery item", "mixed_mastery;theorem_legality;route_choice")
authored("BA", 8, "AUTHOR_CREATED_BENCHMARK_DIAGNOSTIC", "BENCHMARK_ASSIMILATION", "DIAGNOSTIC", "07 Benchmark RECONNECT item", "benchmark_assimilation;diagnosis;transfer")
authored("BB", 6, "AUTHOR_CREATED_BENCHMARK_DIAGNOSTIC", "BENCHMARK_ASSIMILATION", "DIAGNOSTIC", "07 Benchmark Error Lab item", "benchmark_assimilation;diagnosis;transfer")
authored("BC", 8, "AUTHOR_CREATED_BENCHMARK_DIAGNOSTIC", "BENCHMARK_ASSIMILATION", "DIAGNOSTIC", "07 Benchmark ADOPT item", "benchmark_assimilation;diagnosis;transfer")
authored("BD", 6, "AUTHOR_CREATED_BENCHMARK_DIAGNOSTIC", "BENCHMARK_ASSIMILATION", "DIAGNOSTIC", "07 Benchmark TRANSFER item", "benchmark_assimilation;diagnosis;transfer")

rows.append(dict(
    item_id="GEO04-BRUBRIC",
    primary_domain="GEO",
    main_topic_id="IOQM-G9-GEO-04",
    mechanisms="six_question_assimilation;metacognition;transfer;theorem_legality",
    figure_required="false",
    source_integrity_status="CLEAN_VALIDATED",
    provenance="AUTHOR_CREATED_BENCHMARK_RUBRIC",
    student_use_disposition="BENCHMARK_ASSIMILATION",
    teacher_use_disposition="DIAGNOSTIC_RUBRIC",
    answer_verified_independently="true",
    classification_review_status="INDEPENDENT_STATIC_REVIEWED",
    classification_confidence="HIGH",
    notes="07 six-question assimilation rubric; teacher rubric independently synchronized.",
))

assert len(rows) == 84, len(rows)

with OUT.open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=COLS, extrasaction="raise")
    w.writeheader()
    w.writerows(rows)

with OUT.open(encoding="utf-8", newline="") as f:
    check = list(csv.reader(f))
assert len(check) == 85
assert all(len(r) == 31 for r in check)
assert all(r[27] == "true" for r in check[1:])

print(f"wrote {len(rows)} rows x {len(COLS)} columns -> {OUT}")
