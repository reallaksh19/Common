#!/usr/bin/env python3
"""Falsifiers for the two defects issue #321 exists to fix.

1. ``LEARNER_FACING_INTERNAL_IDENTIFIER_LEAK`` — no internal-identifier-shaped
   token may appear in any rendered learner-facing text run, and the guard must
   actually catch the real identifier spellings (including the ``EXT01`` class
   of external ref that the previous fixed-substring scan missed).
2. ``TEACHING_PRIMITIVE_LABEL_ONLY_NOT_REALIZED`` — every C-H primitive the
   PhysicalPageMap claims is backed by real vector drawing operations inside
   its recorded rectangle, drawn from the item's own chemistry.

Both are proved negatively as well as positively: the guard must reject a
deliberately leaked string, and the semantic validator must refuse to draw a
species that is not in the item's declared scope.
"""

import json, sys, tempfile
from pathlib import Path

import pymupdf
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.lib.pagesizes import A4

D = Path(__file__).resolve().parents[1]
REPO = D.parents[3]
sys.path[:0] = [str(D / 'engine'), str(D / 'validator')]

from realize_chemistry_exact_product import realization, register_fonts   # noqa: E402
from audit_chemistry_exact_candidate import audit                          # noqa: E402
from validate_chemistry_custody import validate as validate_custody        # noqa: E402
import chemistry_visual_primitives as VP                                   # noqa: E402
import learner_surface_guard as GUARD                                      # noqa: E402
from chemistry_notation import parse_equation, parse_species, conservation_rows  # noqa: E402

passes = 0


def check(condition, label):
    global passes
    assert condition, label
    passes += 1


def expect_raises(exc, fn, label):
    global passes
    try:
        fn()
    except exc:
        passes += 1
        return
    raise AssertionError('expected ' + label)


# --- guard shape rules, against the registries' real identifier spellings ---
for token in ['CAP-READ-FORMULA', 'CORE1-CAP-ATTACH-SPECIES-ROLE', 'CHEM-CONCEPT-ION-NOTATION',
              'PCK-CHEM-FIRST-MOVE', 'CHECK_SPECIES_IDENTITY', 'VERIFY_RESULT', 'READ_GIVEN',
              'OBLIGATION_LEVEL:SYMBOLIC', 'OBLIGATION_REP:FORMULA', 'ACTIVE_STUDY', 'FULL_LEARNING',
              'EXPLICIT_EXCEPTION', 'PF-AGENT_ROLE_ASSIGNMENT', 'QF-SPECIES-ROLE', 'CQ12', 'EXT05',
              'REP-CAP-PARSE-ION-CHARGE-01-FORMULA_ANATOMY_VIEW', 'MACRO_PARTICLE_SYMBOLIC_BRIDGE']:
    check(GUARD.find_internal_identifiers('lead in ' + token + ' trailing'), 'guard missed ' + token)

# legitimate learner-facing chemistry and prose must never trip the guard
for token in ['Zn + Cu²⁺ → Zn²⁺ + Cu', '2H₂ + O₂ → 2H₂O', 'Fe³⁺ and SO₄²⁻', 'H₂O(l)', '(aq) (s) (g)',
              'H0 — Attempt first', 'CHEMISTRY V2 | 3', 'Appendix A Core Practice', 'CASE A', 'CASE B',
              'ExamSIDE Solution & Transfer Book', 'BEFORE', 'AFTER', 'YES', 'NO', 'Separate ionic charge from subscripts']:
    check(not GUARD.find_internal_identifiers(token), 'guard false positive on ' + token)

expect_raises(ValueError, lambda: GUARD.assert_learner_safe('see CHECK_ATOMS'), 'guard assert on leak')

# --- notation parsing drives the pictures, generically -------------------
eq = parse_equation('2H₂ + O₂ → 2H₂O')
check(eq['reactant_tally'] == {'H': 4, 'O': 2} == eq['product_tally'], 'atom tally')
check(all(r['balanced'] for r in conservation_rows(eq)), 'conservation rows')
check(parse_species('SO₄²⁻')['atoms'] == {'O': 4, 'S': 1}, 'polyatomic ion parse')
check(parse_species('Fe₂(SO₄)₃')['atoms'] == {'Fe': 2, 'O': 12, 'S': 3}, 'nested group parse')
check(parse_species('Fe³⁺')['charge_magnitude'] == 3, 'ionic charge parse')

# --- the semantic validator must fail closed on ungrounded chemistry -----
register_fonts()
with tempfile.TemporaryDirectory() as td:
    probe = rl_canvas.Canvas(str(Path(td) / 'probe.pdf'), pagesize=A4, invariant=1)
    grounded = VP.build_params(primitive_id='FORMULA_ANATOMY_VIEW', tokens=['SO₄²⁻'],
                               declared_entities=['SO₄²⁻'])
    check(VP.render_primitive('FORMULA_ANATOMY_VIEW', grounded, probe, (42, 500, 500, 120))['primitive']
          == 'FORMULA_ANATOMY_VIEW', 'grounded primitive draws')
    # an item about SO₄²⁻ must never render an Fe³⁺ diagram
    ungrounded = VP.build_params(primitive_id='FORMULA_ANATOMY_VIEW', tokens=['Fe³⁺'],
                                 declared_entities=['SO₄²⁻'])
    expect_raises(VP.UngroundedEntityError,
                  lambda: VP.render_primitive('FORMULA_ANATOMY_VIEW', ungrounded, probe, (42, 300, 500, 120)),
                  'ungrounded species rejected')
    # a broken atom ledger must not be drawn as a conservation claim
    broken = VP.build_params(primitive_id='CONSERVATION_LEDGER', tokens=['H₂ + O₂ → H₂O'],
                             declared_entities=['H₂ + O₂ → H₂O'])
    expect_raises(VP.ConservationError,
                  lambda: VP.render_primitive('CONSERVATION_LEDGER', broken, probe, (42, 100, 500, 120)),
                  'unbalanced ledger rejected')
    # an oxidation lane with no source-authorized states must not be invented
    empty = VP.build_params(primitive_id='OXIDATION_STATE_LANE', tokens=[])
    expect_raises(VP.PrimitiveDataUnavailable,
                  lambda: VP.render_primitive('OXIDATION_STATE_LANE', empty, probe, (42, 100, 500, 100)),
                  'invented oxidation states rejected')

# --- the realized product itself ----------------------------------------
with tempfile.TemporaryDirectory() as td:
    out = Path(td)
    candidate, cold = realization(REPO, out)
    policy = json.loads((D / 'registry' / 'chemistry-exact-product-quality-policy.json').read_text())

    for name in ('core-study-guide.pdf', 'examside-solution-transfer-book.pdf'):
        doc = pymupdf.open(out / name)
        leaks = GUARD.scan_pages([p.get_text('text') for p in doc])
        check(not leaks, 'rendered leak in %s: %s' % (name, leaks))

    evidence = candidate['machine_evidence']
    check(evidence['learner_internal_identifier_leaks'] == 0, 'leak count')
    check(evidence['teaching_primitives_drawn'] >= 20, 'primitives drawn')
    check(len(evidence['teaching_primitive_kinds_realized']) >= policy['minimum_realized_primitive_kinds'],
          'realized primitive kinds below floor')
    check(evidence['actual_placement_evidence'], 'placement evidence')
    check(evidence['placement_bounds_violations'] == 0, 'bounds violations')
    check(evidence['orphan_continuations'] == 0, 'orphan continuations')

    # every claimed primitive is backed by vector ops inside its own rectangle
    for map_name, pdf_name in (('physical-page-map-core1.json', 'core-study-guide.pdf'),
                               ('physical-page-map-core2.json', 'examside-solution-transfer-book.pdf')):
        page_map = json.loads((out / map_name).read_text())
        doc = pymupdf.open(out / pdf_name)
        check(page_map['realized_primitives'], 'no realized primitives in ' + map_name)
        for entry in page_map['realized_primitives']:
            page = doc[entry['page'] - 1]
            height = float(page.rect.height)
            top, bottom = height - entry['y1'], height - entry['y0']
            hits = sum(1 for d in page.get_drawings()
                       if d['rect'].x0 >= entry['x0'] - 2 and d['rect'].x1 <= entry['x1'] + 2
                       and d['rect'].y0 >= top - 2 and d['rect'].y1 <= bottom + 2)
            check(hits >= 3, 'primitive %s on page %d is label-only (%d vector ops)'
                  % (entry['primitive'], entry['page'], hits))

    candidate, review = audit(out / 'exact-product-candidate.json', out / 'core-study-guide.pdf',
                              out / 'examside-solution-transfer-book.pdf', out / 'ai-pre-review.json',
                              out / 'physical-page-map-core1.json', out / 'physical-page-map-core2.json',
                              policy)
    check(review['state'] == 'PASS', 'AI pre-review: %s' % review['findings'])
    check(review['production_claim'] is False, 'AI pre-review must never claim production')
    check(review['reviewer_role'] == 'AI_PRE_REVIEW', 'AI pre-review role')
    check(set(review['not_established_by_this_review']) >= {'PEDAGOGICAL_DESIGN', 'VISUAL_USABILITY',
                                                            'MATURE_DESIGN_QUALITY'},
          'AI pre-review must disclaim the human gates')

    check(validate_custody(out, policy), 'independent custody validation')

# --- the frozen candidate must survive CI artifact expiry ---------------
DURABLE = D / 'candidates' / 'CHEM-C-L-EXACT-CANDIDATE-A'
sys.path.insert(0, str(D / 'engine'))
from freeze_chemistry_candidate import verify as verify_frozen   # noqa: E402
check(DURABLE.is_dir(), 'FROZEN_CANDIDATE_ONLY_IN_EXPIRING_CI_ARTIFACT: no durable copy in the repo')
frozen = verify_frozen(DURABLE)
check(frozen['ai_pre_review_state'] in ('PASS', 'FAIL'), 'frozen manifest records the real pre-review state')
check(all(v == 'PENDING' for k, v in frozen['quality_states'].items() if k != 'PUBLICATION_ENGINEERING'),
      'frozen manifest must not imply any human gate has passed')
check({'CORE_STUDY_GUIDE_PDF', 'EXAMSIDE_SOLUTION_TRANSFER_BOOK_PDF'} <= {f['role'] for f in frozen['files']},
      'durable copy must carry the exact PDFs')

print(f'CHEMISTRY C-L learner-surface and primitive-realization falsifiers: {passes} PASS')
print('Engineering only — subject, pedagogy, assessment and visual usability remain PENDING.')
