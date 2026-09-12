#!/usr/bin/env python3
"""Real vector-graphics teaching primitives for the Chemistry V2 exact product.

Every primitive declared by ``chemistry-teaching-primitive-registry.json``
(C-H) is drawn here with actual vector operations — ``line``, ``rect``,
``roundRect``, ``circle``, ``drawPath`` — instead of being emitted as a prose
label, which is the ``TEACHING_PRIMITIVE_LABEL_ONLY_NOT_REALIZED`` defect
issue #321 exists to fix.

Relationship to the shared MasterTemplates package
--------------------------------------------------
``Grade 9/V2/Shared/MasterTemplates/primitives`` is vendored verbatim from
PR #310 (commit ``88d3a719``) and treated as a read-only dependency. This
module is an **adapter**, not a fork:

* the house style comes from the vendored ``Palette`` / ``draw_card_box`` /
  ``draw_pill_badge`` / ``draw_arrow`` so Chemistry cannot drift into a second
  visual language;
* ``OxidationLaneDiagram.draw_lane`` is fully parameterised upstream and is
  called directly for the oxidation-state lane;
* ``VisualSemanticValidator`` is invoked **before every draw call**, so a
  primitive whose species or counts are not grounded in the item's own
  source-authorized data fails closed with ``UngroundedEntityError`` /
  ``ConservationError`` / ``RolePolarityError`` rather than drawing the wrong
  chemistry;
* the remaining primitive bodies live here because the vendored engines for
  them are still hardcoded to their prototype examples (see
  ``UPSTREAM_HARDCODED_ENGINES``). They are invoked through the same
  ``render_primitive(kind, params, canvas, bbox)`` interface, so each one can
  be swapped for its upstream engine the moment #310 parameterises it, without
  touching the renderer.

The module is subject-wide generic: reaction type and species role are *data*
flowing through one parse and one primitive set. Redox is one instance, not a
schema.
"""

import sys
from pathlib import Path

from reportlab.lib import colors

_SHARED = Path(__file__).resolve().parents[3] / 'Shared' / 'MasterTemplates'
if str(_SHARED) not in sys.path:
    sys.path.insert(0, str(_SHARED))

from primitives import base as _pbase                      # noqa: E402
from primitives import diagrams as _pdiagrams              # noqa: E402
from primitives import equations as _pequations            # noqa: E402
from primitives import (                                   # noqa: E402
    ConservationError,
    OxidationLaneDiagram,
    Palette,
    RolePolarityError,
    UngroundedEntityError,
    VisualSemanticValidator,
    VisualValidationError,
    draw_arrow,
    draw_card_box,
    draw_pill_badge,
)

from chemistry_notation import (                           # noqa: E402
    ChemistryNotationError,
    conservation_rows,
    element_tracks,
    is_equation,
    parse_equation,
    parse_species,
    tally,
    to_subscript,
)

# Upstream engines that still draw their prototype example regardless of the
# arguments passed. Using them would reintroduce exactly the defect #321 is
# fixing (a sulfate diagram on an ion-charge item), so this adapter draws those
# primitives from real data instead and reports the gap to PR #310.
UPSTREAM_HARDCODED_ENGINES = {
    'FormulaAnatomyEngine.draw_formula_anatomy': 'accepts a species argument but always draws 2 SO4^2- '
                                                 'and the caption "Atoms per sulfate ion"',
    'ParticleLatticeDiagram.draw_reaction_chamber': 'takes only a title; always draws 2 H2 + O2 -> 2 H2O',
}

FONT = _pbase.FONT_NAME
BOLD = _pbase.FONT_BOLD

# Semantic colour roles, mapped onto the shared MasterTemplates palette so the
# Chemistry renderer and the shared library stay one visual system.
PALETTE = {
    'ink': Palette.TEXT_PRIMARY,
    'muted': Palette.TEXT_MUTED,
    'faint': colors.HexColor('#94A3B8'),
    'rule': Palette.BORDER_CARD,
    'panel': Palette.BG_CARD,
    'navy': Palette.MATH_DARK,
    'navy_text': colors.white,
    'teal': Palette.CHEM_DARK,
    'teal_fill': Palette.CHEM_LIGHT,
    'blue': Palette.PHYSICS_BLUE,
    'blue_fill': Palette.MATH_LIGHT,
    'amber': Palette.WARNING,
    'amber_fill': colors.HexColor('#FEF3C7'),
    'red': Palette.DANGER,
    'red_fill': colors.HexColor('#FEF2F2'),
    'green': Palette.CHEM_MED,
    'green_fill': Palette.CHEM_LIGHT,
}

RUN_COLORS = {
    'COEFFICIENT': 'blue',
    'ELEMENT': 'ink',
    'SUBSCRIPT': 'amber',
    'CHARGE': 'red',
    'STATE': 'teal',
    'GROUP_OPEN': 'ink',
    'GROUP_CLOSE': 'ink',
}

# Deterministic Dalton-sphere fills. Elements the shared palette names keep its
# colour; anything else is assigned by sorted position so the same input always
# produces the same picture and no element carries an invented meaning.
NAMED_ELEMENT_FILLS = {
    'H': Palette.ELEMENT_H,
    'O': Palette.ELEMENT_O,
    'C': Palette.ELEMENT_C,
    'N': Palette.ELEMENT_N,
    'Cl': Palette.ELEMENT_CL,
}
FALLBACK_ELEMENT_FILLS = [
    Palette.ELEMENT_METAL,
    colors.HexColor('#7C3AED'),
    colors.HexColor('#0891B2'),
    colors.HexColor('#D97706'),
    colors.HexColor('#BE123C'),
]

PRIMITIVE_KINDS = (
    'MACRO_OBSERVATION_VIEW',
    'PARTICLE_MODEL_VIEW',
    'MACRO_PARTICLE_SYMBOLIC_BRIDGE',
    'FORMULA_ANATOMY_VIEW',
    'CHARGE_SUBSCRIPT_CONTRAST',
    'COEFFICIENT_SUBSCRIPT_CONTRAST',
    'CONSERVATION_LEDGER',
    'REACTION_BEFORE_AFTER_MAP',
    'SPECIES_ROLE_MAP',
    'RULE_PRIORITY_LADDER',
    'CONDITION_EXCEPTION_GATE',
    'STRUCTURE_SITE_ANNOTATION',
    'OXIDATION_STATE_LANE',
    'SELF_OTHER_AGENT_FRAME',
    'SPLIT_CONVERGE_TOPOLOGY',
    'EVIDENCE_CLAIM_REASONING_CHAIN',
    'APPARATUS_METHOD_FLOW',
    'OBSERVATION_INFERENCE_TABLE',
    'MINIMAL_CHEMISTRY_CONTRAST',
    'FORMULA_EQUATION_CHECK_STRIP',
)

# Learner-readable titles. These are the only strings the renderer contributes;
# every chemical value comes from source semantic data.
PRIMITIVE_TITLES = {
    'MACRO_OBSERVATION_VIEW': 'What was actually observed',
    'PARTICLE_MODEL_VIEW': 'Particle view of the same substance',
    'MACRO_PARTICLE_SYMBOLIC_BRIDGE': 'Same chemical entity across three views',
    'FORMULA_ANATOMY_VIEW': 'Anatomy of the formula',
    'CHARGE_SUBSCRIPT_CONTRAST': 'Charge position versus subscript position',
    'COEFFICIENT_SUBSCRIPT_CONTRAST': 'Coefficient position versus subscript position',
    'CONSERVATION_LEDGER': 'Atom ledger before and after',
    'REACTION_BEFORE_AFTER_MAP': 'Track each element from before to after',
    'SPECIES_ROLE_MAP': 'Sort the species before naming any role',
    'RULE_PRIORITY_LADDER': 'Order in which the rule is consulted',
    'CONDITION_EXCEPTION_GATE': 'Condition gate before the rule applies',
    'STRUCTURE_SITE_ANNOTATION': 'Track the exact structural site',
    'OXIDATION_STATE_LANE': 'Oxidation-state lane, before to after',
    'SELF_OTHER_AGENT_FRAME': 'What the species does to itself, and to the other',
    'SPLIT_CONVERGE_TOPOLOGY': 'Does one state split, or do two converge?',
    'EVIDENCE_CLAIM_REASONING_CHAIN': 'Evidence, link, claim',
    'APPARATUS_METHOD_FLOW': 'Property, apparatus, intended observation',
    'OBSERVATION_INFERENCE_TABLE': 'Observation kept apart from inference',
    'MINIMAL_CHEMISTRY_CONTRAST': 'Two cases, one decisive difference',
    'FORMULA_EQUATION_CHECK_STRIP': 'Run these checks before accepting',
}

ROLE_TITLES = {
    'REACTANT_SPECIES': 'Reactant species',
    'CHANGING_SPECIES': 'Species that changes',
    'SPECTATOR_IF_PRESENT': 'Spectator (if present)',
    'PRODUCT_SPECIES': 'Product species',
    'SELF': 'What it does itself',
    'OTHER': 'What it causes in the other',
}

# Primitives whose drawn content makes a conservation claim, and must therefore
# clear the vendored validator's atom-ledger gate before anything is drawn.
CONSERVATION_GATED = {
    'CONSERVATION_LEDGER',
    'REACTION_BEFORE_AFTER_MAP',
    'MACRO_PARTICLE_SYMBOLIC_BRIDGE',
    'PARTICLE_MODEL_VIEW',
}

# Primitives whose drawn content makes an oxidation-state / agent-role claim.
REDOX_GATED = {
    'OXIDATION_STATE_LANE',
    'SPLIT_CONVERGE_TOPOLOGY',
}


class PrimitiveDataUnavailable(ValueError):
    """Raised when source semantic data cannot support a primitive honestly.

    The renderer must never substitute invented chemistry for missing data, so
    callers catch this and simply do not draw the primitive.
    """


def use_fonts(regular, bold, oblique=None):
    """Bind the renderer's registered Unicode fonts, portably.

    The vendored ``base`` module resolves fonts at import time from
    ``C:\\Windows\\Fonts\\...`` and otherwise falls back to Helvetica, whose
    WinAnsi encoding cannot represent the Unicode subscripts and superscript
    charges the C-H notation contract requires. Rebinding the already-imported
    names is runtime configuration of the vendored package, not a modification
    of its files, and keeps the Chemistry output portable on Linux CI.
    """
    global FONT, BOLD
    FONT = regular or _pbase.FONT_NAME
    BOLD = bold or _pbase.FONT_BOLD
    for module in (_pbase, _pdiagrams, _pequations):
        module.FONT_NAME = FONT
        module.FONT_BOLD = BOLD
        module.FONT_OBLIQUE = oblique or FONT


def _c(name):
    return PALETTE[name]


def _clip(text, canvas, font, size, width):
    text = str(text or '')
    if canvas.stringWidth(text, font, size) <= width:
        return text
    while text and canvas.stringWidth(text + '…', font, size) > width:
        text = text[:-1]
    return (text + '…') if text else ''


def _wrap(text, canvas, font, size, width, max_lines=None):
    words = str(text or '').split()
    lines = []
    current = ''
    for word in words:
        trial = (current + ' ' + word).strip()
        if canvas.stringWidth(trial, font, size) <= width or not current:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    if max_lines is not None and len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = _clip(lines[-1] + ' …', canvas, font, size, width)
    return lines or ['']


# ---------------------------------------------------------------------------
# low-level vector helpers (shared house style)
# ---------------------------------------------------------------------------

def panel(c, x, y, w, h, title=None, accent='teal'):
    """Shared MasterTemplates card frame with the primitive's learner title."""
    draw_card_box(c, x, y, w, h, title=title, title_color=_c(accent))
    return y + h - (28 if title else 8)


def box(c, x, y, w, h, fill=None, stroke='rule', radius=4, width=0.8, dash=None):
    c.saveState()
    c.setLineWidth(width)
    if dash:
        c.setDash(*dash)
    c.setStrokeColor(_c(stroke))
    if fill:
        c.setFillColor(_c(fill))
    c.roundRect(x, y, w, h, radius, fill=1 if fill else 0, stroke=1)
    c.restoreState()


def label(c, x, y, text, size=7.2, color='muted', font=None, width=None, align='left'):
    font = font or FONT
    text = str(text or '')
    if width is not None:
        text = _clip(text, c, font, size, width)
    c.setFont(font, size)
    c.setFillColor(_c(color))
    if align == 'center':
        c.drawCentredString(x, y, text)
    elif align == 'right':
        c.drawRightString(x, y, text)
    else:
        c.drawString(x, y, text)
    return c.stringWidth(text, font, size)


def paragraph(c, x, y, text, w, size=7.2, color='muted', leading=9.0, max_lines=3, font=None):
    font = font or FONT
    lines = _wrap(text, c, font, size, w, max_lines)
    for index, line in enumerate(lines):
        label(c, x, y - index * leading, line, size=size, color=color, font=font)
    return y - (len(lines) - 1) * leading


def arrow(c, x0, y0, x1, y1, color='teal', width=1.4, head=5.0, dashed=False):
    draw_arrow(c, x0, y0, x1, y1, _c(color), line_width=width, head_len=head,
               head_width=head * 0.55, dashed=dashed)


def pill(c, x, y, text, fill='panel', color='amber', size=6.6, height=13):
    return draw_pill_badge(c, x, y + height / 2, text, _c(fill), _c(color),
                           font=BOLD, font_size=size, height=height, padding_x=7)


def tick_box(c, x, y, size=8):
    c.setStrokeColor(_c('faint'))
    c.setFillColor(colors.white)
    c.setLineWidth(0.8)
    c.rect(x, y, size, size, fill=1, stroke=1)


def rule_line(c, x0, y, x1, color='rule', width=0.6, dash=None):
    c.saveState()
    c.setStrokeColor(_c(color))
    c.setLineWidth(width)
    if dash:
        c.setDash(*dash)
    c.line(x0, y, x1, y)
    c.restoreState()


def species_width(c, species, size):
    total = 0.0
    for kind, text in species['runs']:
        glyph = to_subscript(text) if kind == 'SUBSCRIPT' else text
        font = BOLD if kind in ('ELEMENT', 'COEFFICIENT') else FONT
        total += c.stringWidth(glyph, font, size)
    return total


def draw_species(c, x, y, species, size=13, highlight=None, dim=False):
    """Draw one parsed species as coloured positional runs.

    Returns ``(kind, x0, x1, glyph)`` marks so callouts can point at the exact
    glyph they annotate. Unicode subscript/superscript glyphs are preserved so
    the extracted text layer stays unambiguous per the C-H notation contract.
    """
    marks = []
    cursor = x
    for kind, text in species['runs']:
        glyph = to_subscript(text) if kind == 'SUBSCRIPT' else text
        font = BOLD if kind in ('ELEMENT', 'COEFFICIENT') else FONT
        color = 'faint' if dim else RUN_COLORS.get(kind, 'ink')
        if highlight and kind != highlight:
            color = 'faint'
        c.setFont(font, size)
        c.setFillColor(_c(color))
        c.drawString(cursor, y, glyph)
        width = c.stringWidth(glyph, font, size)
        marks.append((kind, cursor, cursor + width, glyph))
        cursor += width
    return marks


def _mark(marks, kind):
    for entry in marks:
        if entry[0] == kind:
            return entry
    return None


def element_fills(elements):
    fills = {}
    spare = 0
    for element in sorted(elements):
        if element in NAMED_ELEMENT_FILLS:
            fills[element] = NAMED_ELEMENT_FILLS[element]
        else:
            fills[element] = FALLBACK_ELEMENT_FILLS[spare % len(FALLBACK_ELEMENT_FILLS)]
            spare += 1
    return fills


def atom_cluster(c, x, y, species, fills, radius=6.0, spread=13.0):
    """Draw one particle as Dalton spheres, one per atom.

    Composition and count come from the parsed formula only; no bonding
    geometry or particle size is claimed beyond the school-level count model.
    """
    atoms = []
    for element in sorted(species['atoms']):
        atoms.extend([element] * species['atoms'][element])
    start = x - (len(atoms) - 1) * spread / 2
    for index, element in enumerate(atoms):
        cx = start + index * spread
        c.setFillColor(fills[element])
        c.setStrokeColor(colors.white)
        c.setLineWidth(0.8)
        c.circle(cx, y, radius, fill=1, stroke=1)
        c.setFillColor(colors.white)
        c.setFont(BOLD, 5.4)
        c.drawCentredString(cx, y - 1.9, element)
    return len(atoms)


# ---------------------------------------------------------------------------
# parameter normalisation
# ---------------------------------------------------------------------------

def _first_equation(tokens):
    for token in tokens:
        if is_equation(token):
            try:
                return parse_equation(token)
            except ChemistryNotationError:
                continue
    return None


def _species_list(tokens):
    out = []
    for token in tokens:
        if is_equation(token):
            try:
                equation = parse_equation(token)
            except ChemistryNotationError:
                continue
            out.extend(equation['reactants'] + equation['products'])
            continue
        try:
            out.append(parse_species(token))
        except ChemistryNotationError:
            continue
    return out


def build_params(*, primitive_id, tokens=(), title=None, instructional_job='', attention_target='',
                 learner_action='', condition_context=(), species_roles=(), checks=(),
                 observation=None, claim=None, oxidation_states=(), particles=(), site_labels=(),
                 declared_entities=(), accessibility_text='', safe=None):
    """Normalise one representation / visual-spec record into render params.

    ``safe`` is the renderer's learner-surface text mapper; every free string is
    pushed through it so no internal identifier can reach a drawn glyph.
    ``declared_entities`` is the item's own chemical scope, used by the
    vendored ``VisualSemanticValidator`` entity-closure gate.
    """
    clean = safe or (lambda value: value)
    tokens = [str(t) for t in tokens if str(t).strip()]
    declared = [str(t) for t in declared_entities if str(t).strip()] or tokens
    return {
        'primitive_id': primitive_id,
        'title': title or PRIMITIVE_TITLES.get(primitive_id, 'Chemistry view'),
        'tokens': tokens,
        'species': _species_list(tokens),
        'equation': _first_equation(tokens),
        'declared_entities': declared,
        'declared_species': {s['raw'] for s in _species_list(declared)},
        'instructional_job': clean(instructional_job),
        'attention_target': clean(attention_target),
        'learner_action': clean(learner_action),
        'condition_context': [clean(x) for x in condition_context if str(x).strip()],
        'species_roles': [ROLE_TITLES.get(str(x), clean(x)) for x in species_roles],
        'checks': [clean(x) for x in checks if str(x).strip()],
        'observation': clean(observation) if observation else None,
        'claim': clean(claim) if claim else None,
        'oxidation_states': list(oxidation_states),
        'particles': list(particles),
        'site_labels': [clean(x) for x in site_labels],
        'accessibility_text': clean(accessibility_text),
    }


# ---------------------------------------------------------------------------
# fail-closed pre-render validation (vendored VisualSemanticValidator)
# ---------------------------------------------------------------------------

def _item_data(params):
    return {
        'chemical_entities': sorted(set(params['declared_entities']) | params['declared_species']),
        'entities': sorted(params['declared_species']),
    }


def _assert_entity_closure(params, drawn_species):
    """Gate 1: every species about to be drawn must be in the item's own scope.

    Uses the vendored ``UngroundedEntityError`` so Chemistry reports the same
    failure class as the shared library, rather than inventing a parallel one.
    """
    declared = params['declared_species']
    if not declared:
        return
    ungrounded = {s['raw'] for s in drawn_species} - declared
    if ungrounded:
        raise UngroundedEntityError(
            '[GATE-01 FAIL: ENTITY_CLOSURE] %s would draw ungrounded species %s; '
            'item scope is %s.' % (params['primitive_id'], sorted(ungrounded), sorted(declared)))


def _prevalidate(kind, params):
    """Run the vendored validator before any drawing operation is issued."""
    item = _item_data(params)
    equation = params['equation']
    if kind in CONSERVATION_GATED:
        if equation is not None:
            VisualSemanticValidator.validate(
                'PARTICULATE_MODEL', item,
                {'reactants': tally(equation['reactants']), 'products': tally(equation['products'])})
            _assert_entity_closure(params, equation['reactants'] + equation['products'])
        elif params['species']:
            _assert_entity_closure(params, params['species'])
    elif kind in REDOX_GATED:
        for pair in _oxidation_pairs(params):
            VisualSemanticValidator.validate(
                'OXIDATION_STATE_LANE', item,
                {'reactant_species': pair['before_species'], 'product_species': pair['after_species'],
                 'reactant_on': str(pair['before']), 'product_on': str(pair['after']),
                 'assigned_role': ''})
    elif params['species']:
        _assert_entity_closure(params, params['species'])
    return True


# ---------------------------------------------------------------------------
# primitive bodies
# ---------------------------------------------------------------------------

def _pick_species(params, need=None):
    candidates = params['species'] or []
    if not candidates:
        raise PrimitiveDataUnavailable('no parsable species token for ' + params['primitive_id'])
    if need == 'SUBSCRIPT':
        ranked = [s for s in candidates if s['subscripts']] or candidates
    elif need == 'CHARGE':
        ranked = [s for s in candidates if s['charge']] or candidates
    elif need == 'COEFFICIENT':
        ranked = [s for s in candidates if s['coefficient_text']] or candidates
    elif need == 'BOTH':
        ranked = [s for s in candidates if s['subscripts'] and s['charge']] or \
                 [s for s in candidates if s['subscripts'] or s['charge']] or candidates
    else:
        ranked = candidates
    return sorted(ranked, key=lambda s: (-len(s['runs']), s['raw']))[0]


def _draw_formula_anatomy(c, x, y, w, h, params):
    """Data-driven replacement for the still-hardcoded upstream engine.

    ``FormulaAnatomyEngine.draw_formula_anatomy`` accepts a ``species`` argument
    but always draws ``2 SO4^2-``; drawing that on, say, an ``Fe³⁺`` item is the
    exact defect this issue fixes. Every glyph and callout numeral below is read
    off the item's own parsed token.
    """
    species = _pick_species(params, 'BOTH')
    top = panel(c, x, y, w, h, params['title'])
    label(c, x + 12, top, params['attention_target'] or 'Notation position and its meaning.',
          size=6.8, color='muted', width=w - 24)

    formula_y = y + (h - 26) / 2 + 2
    size = 22
    formula_x = x + (w - species_width(c, species, size)) / 2
    marks = draw_species(c, formula_x, formula_y, species, size=size)
    rule_line(c, x + 14, formula_y - 12, x + w - 14, color='rule', dash=(2, 3))

    # role -> (colour, heading, meaning). Only positions the token actually has
    # are annotated, and every numeral shown is read off the token itself.
    roles = []
    coefficient = _mark(marks, 'COEFFICIENT')
    if coefficient:
        roles.append((coefficient, 'blue', 'COEFFICIENT ' + coefficient[3], 'how many whole species'))
    subscript = _mark(marks, 'SUBSCRIPT')
    if subscript:
        roles.append((subscript, 'amber', 'SUBSCRIPT ' + ''.join(species['subscripts']),
                      'atoms inside one species'))
    charge = _mark(marks, 'CHARGE')
    if charge:
        roles.append((charge, 'red', 'IONIC CHARGE ' + charge[3], 'net charge on the whole ion'))
    state = _mark(marks, 'STATE')
    if state:
        roles.append((state, 'teal', 'STATE ' + state[3], 'physical state as recorded'))
    if not roles:
        element = _mark(marks, 'ELEMENT')
        roles.append((element, 'blue', 'ELEMENT ' + element[3], 'which atom is present'))

    # Two fixed callout columns with elbow leaders, so labels never collide with
    # the formula or with each other however many positions the token carries.
    col_w = 152.0
    left_x = x + 14
    right_x = x + w - 14 - col_w
    top_row = formula_y + 34
    bottom_row = formula_y - 30
    slots = [(left_x, top_row, 'left'), (right_x, top_row, 'right'),
             (left_x, bottom_row, 'left'), (right_x, bottom_row, 'right')]
    for index, (mark, color, head, note) in enumerate(roles[:4]):
        sx, sy, side = slots[index]
        anchor = (mark[1] + mark[2]) / 2
        pin_y = formula_y + (size + 3) if sy > formula_y else formula_y - 5
        elbow_y = sy + 3
        edge = sx + col_w if side == 'left' else sx
        c.saveState()
        c.setStrokeColor(_c(color))
        c.setLineWidth(0.9)
        c.line(anchor, pin_y, anchor, elbow_y)
        c.line(anchor, elbow_y, edge + (4 if side == 'left' else -4), elbow_y)
        c.setFillColor(_c(color))
        c.circle(anchor, pin_y, 1.7, fill=1, stroke=0)
        c.restoreState()
        label(c, sx, sy, head, size=6.8, color=color, font=BOLD, width=col_w)
        label(c, sx, sy - 8.5, note, size=6.3, color='muted', width=col_w)

    label(c, x + 12, y + 8, params['learner_action'] or 'Name each position before interpreting the formula.',
          size=6.3, color='muted', width=w - 24)


def _draw_position_contrast(c, x, y, w, h, params, first, second, first_note, second_note):
    """Shared body for the two 'one decisive notation position' contrasts.

    The *same* source token is drawn twice; only which position is highlighted
    changes. No second species is invented, so ``ONE_DECISIVE_FEATURE`` and
    ``IRRELEVANT_CONTEXT_HELD_CONSTANT`` both hold literally.
    """
    species = _pick_species(params, 'BOTH')
    kinds = {kind for kind, _ in species['runs']}
    if not ({first, second} <= kinds):
        raise PrimitiveDataUnavailable('token lacks both contrasted positions: ' + species['raw'])
    top = panel(c, x, y, w, h, params['title'])
    label(c, x + 12, top, 'Same species, same symbols — only the position you read changes.',
          size=6.8, color='muted', width=w - 24)

    case_w = (w - 34) / 2
    case_h = h - 54
    case_y = y + 14
    for index, (kind, note, accent) in enumerate(((first, first_note, 'blue'), (second, second_note, 'red'))):
        cx = x + 12 + index * (case_w + 10)
        box(c, cx, case_y, case_w, case_h, fill='panel', stroke=accent, width=1.0)
        label(c, cx + 8, case_y + case_h - 12, 'CASE ' + ('A' if index == 0 else 'B'),
              size=6.6, color=accent, font=BOLD)
        size = 18
        fx = cx + (case_w - species_width(c, species, size)) / 2
        fy = case_y + case_h - 42
        marks = draw_species(c, fx, fy, species, size=size, highlight=kind)
        mark = _mark(marks, kind)
        if mark:
            c.setStrokeColor(_c(accent))
            c.setLineWidth(1.2)
            c.roundRect(mark[1] - 2.5, fy - 4, (mark[2] - mark[1]) + 5, size + 4, 3, fill=0, stroke=1)
            arrow(c, (mark[1] + mark[2]) / 2, fy - 8, (mark[1] + mark[2]) / 2, fy - 16,
                  color=accent, width=0.9, head=3.5)
        paragraph(c, cx + 8, case_y + 16, note, case_w - 16, size=6.5, color='ink', max_lines=3)
    label(c, x + 12, y + 5, params['learner_action'] or 'State what the numeral means in each position.',
          size=6.3, color='muted', width=w - 24)


def _draw_charge_subscript_contrast(c, x, y, w, h, params):
    _draw_position_contrast(
        c, x, y, w, h, params, 'SUBSCRIPT', 'CHARGE',
        'The lowered numeral counts atoms inside the species.',
        'The raised numeral with a sign is the net charge on the whole ion.')


def _draw_coefficient_subscript_contrast(c, x, y, w, h, params):
    _draw_position_contrast(
        c, x, y, w, h, params, 'COEFFICIENT', 'SUBSCRIPT',
        'The leading numeral counts whole species.',
        'The lowered numeral counts atoms inside one species.')


def _draw_conservation_ledger(c, x, y, w, h, params):
    equation = params['equation']
    if equation is None:
        raise PrimitiveDataUnavailable('conservation ledger needs a reaction token')
    rows = conservation_rows(equation)
    top = panel(c, x, y, w, h, params['title'])
    label(c, x + 12, top, equation['raw'], size=11, color='ink', font=BOLD, width=w - 24)

    table_y = y + 20
    table_h = h - 62
    row_h = min(16.0, table_h / max(len(rows) + 1, 2))
    col_x = [x + 12, x + 62, x + 132, x + 212]
    table_w = w - 24
    header_y = table_y + table_h - row_h

    c.setFillColor(_c('blue_fill'))
    c.setStrokeColor(_c('rule'))
    c.setLineWidth(0.6)
    c.rect(x + 12, header_y, table_w, row_h, fill=1, stroke=1)
    for text, cx in zip(('Element', 'Before', 'After', 'Matched?'), col_x):
        label(c, cx + 4, header_y + row_h / 2 - 2.4, text, size=6.8, color='navy', font=BOLD)

    for index, row in enumerate(rows):
        ry = header_y - (index + 1) * row_h
        if ry < table_y - 1:
            break
        c.setStrokeColor(_c('rule'))
        c.setLineWidth(0.5)
        c.rect(x + 12, ry, table_w, row_h, fill=0, stroke=1)
        label(c, col_x[0] + 4, ry + row_h / 2 - 2.4, row['element'], size=8, color='ink', font=BOLD)
        for value, cx, swatch in ((row['before'], col_x[1], 'blue'), (row['after'], col_x[2], 'teal')):
            label(c, cx + 4, ry + row_h / 2 - 2.4, str(value), size=8, color='ink', font=BOLD)
            for tick in range(min(int(value), 8)):
                c.setFillColor(_c(swatch))
                c.rect(cx + 16 + tick * 5.4, ry + row_h / 2 - 3, 3.6, 6, fill=1, stroke=0)
        ok = row['balanced']
        c.setStrokeColor(_c('green') if ok else _c('red'))
        c.setLineWidth(1.3)
        mx, my = col_x[3] + 6, ry + row_h / 2
        if ok:
            c.line(mx, my, mx + 3, my - 3.4)
            c.line(mx + 3, my - 3.4, mx + 9, my + 4)
        else:
            c.line(mx, my - 3.5, mx + 8, my + 3.5)
            c.line(mx, my + 3.5, mx + 8, my - 3.5)
        label(c, col_x[3] + 20, ry + row_h / 2 - 2.4, 'same' if ok else 'differs',
              size=6.4, color='green' if ok else 'red')

    label(c, x + 12, y + 7, params['learner_action'] or 'Compare each row and stop at the first mismatch.',
          size=6.4, color='muted', width=w - 24)


def _draw_particle_model(c, x, y, w, h, params, embedded=False, title=None):
    """Data-driven replacement for the still-hardcoded upstream engine.

    ``ParticleLatticeDiagram.draw_reaction_chamber`` takes only a title and
    always draws ``2 H2 + O2 -> 2 H2O``. Particle identity and count here come
    from the item's own ``PARTICLE_COUNT`` figure semantics or parsed formula.
    """
    particles = []
    for entry in params['particles']:
        formula = str(entry.get('formula', '')).strip()
        count = int(entry.get('count', 0))
        if not formula or count < 1:
            raise PrimitiveDataUnavailable('invalid particle-count entry')
        particles.append((parse_species(formula), count))
    if not particles:
        particles = [(_pick_species(params), 1)]
    if not embedded:
        top = panel(c, x, y, w, h, title or params['title'])
        label(c, x + 12, top, 'School-level particle-count model — composition and count only.',
              size=6.5, color='muted', width=w - 24)
    elements = sorted({e for species, _ in particles for e in species['atoms']})
    fills = element_fills(elements)

    inner_x = x + 12
    inner_y = y + (30 if not embedded else 16)
    inner_w = w - 24
    cursor_x = inner_x + 30
    cursor_y = y + h - (60 if not embedded else 26)
    drawn = 0
    counts = {}
    for species, count in particles:
        for _ in range(count):
            cluster_w = max(38.0, 16.0 + 13.0 * sum(species['atoms'].values()))
            if cursor_x + cluster_w > inner_x + inner_w:
                cursor_x = inner_x + 30
                cursor_y -= 34
            if cursor_y < inner_y + 12:
                break
            box(c, cursor_x - cluster_w / 2, cursor_y - 13, cluster_w, 26, stroke='rule', radius=9)
            atom_cluster(c, cursor_x, cursor_y, species, fills)
            label(c, cursor_x, cursor_y - 21, species['raw'], size=6.6, color='muted', align='center')
            cursor_x += cluster_w + 14
            drawn += 1
            for element, number in species['atoms'].items():
                counts[element] = counts.get(element, 0) + number
    legend_x = inner_x + 2
    legend_y = y + (16 if not embedded else 6)
    for element in elements:
        c.setFillColor(fills[element])
        c.circle(legend_x + 3, legend_y + 3, 3.2, fill=1, stroke=0)
        width = label(c, legend_x + 9, legend_y + 1, '%s × %d' % (element, counts.get(element, 0)),
                      size=6.4, color='muted')
        legend_x += width + 20
    label(c, x + w - 12, legend_y + 1, '%d particle(s) shown' % drawn, size=6.4,
          color='muted', align='right')
    return drawn


def _draw_particle_model_view(c, x, y, w, h, params):
    _draw_particle_model(c, x, y, w, h, params)


def _draw_bridge(c, x, y, w, h, params):
    species = _pick_species(params)
    top = panel(c, x, y, w, h, params['title'])
    label(c, x + 12, top, params['attention_target'] or 'The same entity, read three ways.',
          size=6.6, color='muted', width=w - 24)
    panel_w = (w - 24 - 2 * 16) / 3
    panel_h = h - 58
    panel_y = y + 16
    titles = ('Stated / observed', 'Particle model', 'Symbolic notation')
    for index, caption in enumerate(titles):
        px = x + 12 + index * (panel_w + 16)
        box(c, px, panel_y, panel_w, panel_h, fill='panel', stroke='rule')
        label(c, px + panel_w / 2, panel_y + panel_h - 12, caption, size=6.8,
              color='navy', font=BOLD, align='center', width=panel_w - 8)
        if index == 0:
            paragraph(c, px + 7, panel_y + panel_h - 26,
                      params['instructional_job'] or 'Same entity and same count as stated.',
                      panel_w - 14, size=6.3, color='ink', max_lines=5)
        elif index == 1:
            atom_cluster(c, px + panel_w / 2, panel_y + panel_h / 2 - 2, species,
                         element_fills(species['atoms']))
            label(c, px + panel_w / 2, panel_y + 12, 'identity and count preserved',
                  size=6.1, color='muted', align='center', width=panel_w - 8)
        else:
            size = 15
            draw_species(c, px + (panel_w - species_width(c, species, size)) / 2,
                         panel_y + panel_h / 2 - 6, species, size=size)
            label(c, px + panel_w / 2, panel_y + 12, 'same identity, written down',
                  size=6.1, color='muted', align='center', width=panel_w - 8)
        if index < 2:
            arrow(c, px + panel_w + 2, panel_y + panel_h / 2, px + panel_w + 13, panel_y + panel_h / 2,
                  color='teal', width=1.2, head=4)
    label(c, x + 12, y + 5, params['learner_action'] or 'Trace the same entity across all three panels.',
          size=6.3, color='muted', width=w - 24)


def _draw_reaction_before_after(c, x, y, w, h, params):
    equation = params['equation']
    if equation is None:
        raise PrimitiveDataUnavailable('before/after map needs a reaction token')
    top = panel(c, x, y, w, h, params['title'])
    label(c, x + 12, top, equation['raw'], size=9, color='ink', font=BOLD, width=w - 24)

    side_w = (w - 24 - 34) / 2
    side_h = h - 70
    side_y = y + 24
    lefts, rights = [], []
    for index, (species_list, sx, store) in enumerate((
            (equation['reactants'], x + 12, lefts),
            (equation['products'], x + 12 + side_w + 34, rights))):
        box(c, sx, side_y, side_w, side_h, stroke='rule')
        label(c, sx + 6, side_y + side_h - 11, 'BEFORE' if index == 0 else 'AFTER',
              size=6.5, color='navy', font=BOLD)
        slot_h = (side_h - 18) / max(len(species_list), 1)
        for slot, species in enumerate(species_list):
            cy = side_y + side_h - 18 - slot * slot_h - slot_h / 2
            box(c, sx + 8, cy - 9, side_w - 16, 18, fill='blue_fill' if index == 0 else 'teal_fill',
                stroke='blue' if index == 0 else 'teal', radius=4, width=0.7)
            draw_species(c, sx + 14, cy - 3.5, species, size=10)
            store.append((cy, species))
    arrow(c, x + 12 + side_w + 6, side_y + side_h / 2, x + 12 + side_w + 28, side_y + side_h / 2,
          color='teal', width=1.6, head=5.5)
    label(c, x + 12 + side_w + 17, side_y + side_h / 2 + 8, equation['arrow'], size=8,
          color='teal', font=BOLD, align='center')

    tracks = [t for t in element_tracks(equation) if t['present_both_sides']]
    for track in tracks:
        for li in track['reactant_indices']:
            for ri in track['product_indices']:
                if li >= len(lefts) or ri >= len(rights):
                    continue
                y0 = lefts[li][0]
                y1 = rights[ri][0]
                c.saveState()
                c.setStrokeColor(_c('amber' if track['changed'] else 'faint'))
                c.setLineWidth(0.7)
                c.setDash(2, 2)
                c.line(x + 12 + side_w - 6, y0, x + 12 + side_w + 6, (y0 + y1) / 2)
                c.line(x + 12 + side_w + 28, (y0 + y1) / 2, x + 12 + side_w + 40, y1)
                c.restoreState()
    legend_x = x + 12
    for text, color in (('tracked element changes host species', 'amber'),
                        ('tracked element unchanged', 'faint')):
        c.saveState()
        c.setStrokeColor(_c(color))
        c.setLineWidth(1.1)
        c.setDash(2, 2)
        c.line(legend_x, y + 12, legend_x + 14, y + 12)
        c.restoreState()
        legend_x += 26 + label(c, legend_x + 18, y + 9.5, text, size=6.2, color='muted')
    label(c, x + w - 12, y + 9.5, 'Elements tracked: ' + ', '.join(t['element'] for t in tracks),
          size=6.2, color='muted', align='right')


def _draw_species_role_map(c, x, y, w, h, params):
    equation = params['equation']
    if equation is None:
        raise PrimitiveDataUnavailable('species role map needs a reaction token')
    roles = params['species_roles'] or [ROLE_TITLES['REACTANT_SPECIES'], ROLE_TITLES['PRODUCT_SPECIES']]
    top = panel(c, x, y, w, h, params['title'])
    label(c, x + 12, top, equation['raw'], size=9, color='ink', font=BOLD, width=w - 24)
    lane_h = (h - 66) / max(len(roles), 1)
    lane_y = y + 22
    for index, role in enumerate(reversed(roles)):
        ly = lane_y + index * lane_h
        box(c, x + 12, ly + 1.5, w - 24, lane_h - 3, fill='panel', stroke='rule', radius=3)
        label(c, x + 18, ly + lane_h / 2 - 2.4, role, size=6.9, color='navy', font=BOLD, width=120)
        c.saveState()
        c.setStrokeColor(_c('rule'))
        c.setLineWidth(0.6)
        c.line(x + 142, ly + 2, x + 142, ly + lane_h - 2)
        c.restoreState()
        role_key = role.lower()
        if 'reactant' in role_key:
            chips = equation['reactants']
        elif 'product' in role_key:
            chips = equation['products']
        else:
            chips = []
        if chips:
            cursor = x + 152
            for species in chips:
                width = species_width(c, species, 9) + 16
                box(c, cursor, ly + lane_h / 2 - 8, width, 16, fill='blue_fill', stroke='blue',
                    radius=8, width=0.7)
                draw_species(c, cursor + 8, ly + lane_h / 2 - 3, species, size=9)
                cursor += width + 8
        else:
            c.saveState()
            c.setStrokeColor(_c('faint'))
            c.setLineWidth(0.7)
            c.setDash(3, 2)
            c.roundRect(x + 152, ly + lane_h / 2 - 8, w - 176, 16, 4, fill=0, stroke=1)
            c.restoreState()
            label(c, x + 158, ly + lane_h / 2 - 2.4, 'fill only from the evidence above',
                  size=6.2, color='faint')
    label(c, x + 12, y + 7, params['learner_action'] or 'Sort every species before attaching any role.',
          size=6.3, color='muted', width=w - 24)


def _draw_rule_priority_ladder(c, x, y, w, h, params):
    steps = ['Read the rule as stated for this task']
    if params['condition_context']:
        steps.append('Check the stated condition: ' + params['condition_context'][0])
        if len(params['condition_context']) > 1:
            steps.append('Check the stated exception: ' + params['condition_context'][1])
    else:
        steps.append('Check whether any stated condition applies')
    steps.append('Apply the rule, or apply the override the condition requires')
    top = panel(c, x, y, w, h, params['title'])
    label(c, x + 12, top, params['attention_target'] or 'Rule selection before the condition decision.',
          size=6.6, color='muted', width=w - 24)
    step_h = min(21.0, (h - 62) / len(steps))
    gap = min(9.0, max((h - 62 - step_h * len(steps)) / max(len(steps) - 1, 1), 2.0))
    cursor = y + h - 44 - step_h
    for index, step in enumerate(steps):
        accent = 'blue' if index < len(steps) - 1 else 'green'
        box(c, x + 34, cursor, w - 58, step_h, fill='panel', stroke=accent, radius=4, width=0.9)
        c.setFillColor(_c(accent))
        c.circle(x + 24, cursor + step_h / 2, 7.5, fill=1, stroke=0)
        label(c, x + 24, cursor + step_h / 2 - 2.6, str(index + 1), size=7.4,
              color='navy_text', font=BOLD, align='center')
        label(c, x + 44, cursor + step_h / 2 - 2.4, step, size=6.8, color='ink', width=w - 84)
        if index < len(steps) - 1:
            arrow(c, x + 24, cursor - 1, x + 24, cursor - gap + 1, color='faint', width=0.9, head=3.5)
        cursor -= step_h + gap
    label(c, x + 12, y + 7, 'Stop at the first step whose stated condition decides the case.',
          size=6.3, color='muted', width=w - 24)


def _draw_condition_gate(c, x, y, w, h, params):
    condition = params['condition_context'][0] if params['condition_context'] else None
    if not condition:
        raise PrimitiveDataUnavailable('condition gate needs a recorded condition')
    top = panel(c, x, y, w, h, params['title'])
    equation = params['equation']
    if equation is not None:
        eq_y = top - 12
        cursor = x + 14
        for index, species in enumerate(equation['reactants']):
            draw_species(c, cursor, eq_y, species, size=11)
            cursor += species_width(c, species, 11)
            if index < len(equation['reactants']) - 1:
                cursor += label(c, cursor + 4, eq_y, '+', size=11, color='ink', font=BOLD) + 8
        arrow(c, cursor + 10, eq_y + 3.5, cursor + 44, eq_y + 3.5, color='teal', width=1.2, head=4.5)
        label(c, cursor + 27, eq_y + 9, condition, size=6.8, color='amber', font=BOLD,
              align='center', width=60)
        cursor += 52
        for index, species in enumerate(equation['products']):
            draw_species(c, cursor, eq_y, species, size=11)
            cursor += species_width(c, species, 11)
            if index < len(equation['products']) - 1:
                cursor += label(c, cursor + 4, eq_y, '+', size=11, color='ink', font=BOLD) + 8
        label(c, x + 14, eq_y - 12, 'The recorded condition stays attached to the arrow.',
              size=6.3, color='muted', width=w - 28)

    gate_cy = y + 46
    gate_cx = x + 78
    path = c.beginPath()
    path.moveTo(gate_cx, gate_cy + 26)
    path.lineTo(gate_cx + 56, gate_cy)
    path.lineTo(gate_cx, gate_cy - 26)
    path.lineTo(gate_cx - 56, gate_cy)
    path.close()
    c.setFillColor(_c('amber_fill'))
    c.setStrokeColor(_c('amber'))
    c.setLineWidth(1.0)
    c.drawPath(path, fill=1, stroke=1)
    label(c, gate_cx, gate_cy + 4, 'Is this condition', size=6.5, color='amber', font=BOLD, align='center')
    label(c, gate_cx, gate_cy - 4, 'stated for this task?', size=6.5, color='amber', font=BOLD, align='center')
    label(c, gate_cx, gate_cy - 34, condition, size=7.2, color='ink', font=BOLD, align='center', width=150)

    for index, (answer, note, color) in enumerate((
            ('YES', 'Keep it attached and apply the version it requires.', 'green'),
            ('NO', 'Apply the default rule with nothing added.', 'blue'))):
        by = gate_cy + 16 - index * 34
        arrow(c, gate_cx + 58, gate_cy, gate_cx + 86, by, color=color, width=0.9, head=4)
        width = pill(c, gate_cx + 88, by - 6.5, answer, fill='panel', color=color)
        label(c, gate_cx + 94 + width, by - 2.4, note, size=6.5, color='ink',
              width=max(x + w - 12 - (gate_cx + 94 + width), 40))


def _draw_structure_site(c, x, y, w, h, params):
    species = _pick_species(params)
    sites = params['site_labels'] or []
    top = panel(c, x, y, w, h, params['title'])
    label(c, x + 12, top, params['attention_target'] or 'The exact site the rule applies to.',
          size=6.6, color='muted', width=w - 24)
    nodes = []
    for element in sorted(species['atoms']):
        nodes.extend([element] * species['atoms'][element])
    if not nodes:
        raise PrimitiveDataUnavailable('structure annotation needs a parsable formula')
    spacing = min(56.0, (w - 60) / max(len(nodes), 1))
    start = x + 30
    cy = y + h * 0.46
    for index, element in enumerate(nodes):
        cx = start + index * spacing
        if index:
            c.setStrokeColor(_c('muted'))
            c.setLineWidth(1.0)
            c.line(cx - spacing + 11, cy, cx - 11, cy)
        target = bool(sites) and index == 0
        c.setFillColor(_c('amber_fill') if target else colors.white)
        c.setStrokeColor(_c('amber') if target else _c('muted'))
        c.setLineWidth(1.4 if target else 0.9)
        c.circle(cx, cy, 11, fill=1, stroke=1)
        label(c, cx, cy - 3, element, size=8.4, color='ink', font=BOLD, align='center')
        site_id = sites[index] if index < len(sites) else 'site %d' % (index + 1)
        label(c, cx, cy - 24, site_id, size=6.2, color='muted', align='center', width=spacing)
    label(c, x + 12, y + 8, params['learner_action'] or 'Track the labelled site, not the whole formula.',
          size=6.3, color='muted', width=w - 24)


def _state_text(value):
    return '%+d' % value if value else '0'


def _oxidation_pairs(params):
    """Source-authorized oxidation-state pairs; never guessed."""
    explicit = []
    for entry in params['oxidation_states']:
        element = str(entry.get('element', '')).strip()
        before = entry.get('before')
        after = entry.get('after')
        if not element or before is None or after is None:
            continue
        explicit.append({
            'element': element,
            'before': int(before),
            'after': int(after),
            'before_species': str(entry.get('before_species', '')) or element,
            'after_species': str(entry.get('after_species', '')) or element,
        })
    if explicit:
        return explicit
    equation = params['equation']
    if equation is None:
        raise PrimitiveDataUnavailable('oxidation-state lane needs explicit states or a reaction token')
    derived = []
    for track in element_tracks(equation):
        if not track['present_both_sides']:
            continue
        before_species = equation['reactants'][track['reactant_indices'][0]]
        after_species = equation['products'][track['product_indices'][0]]
        # Only a monatomic species lets oxidation state be read off the notation
        # itself (the ON of a monatomic ion equals its charge). Anything else
        # needs explicit upstream data; the renderer must not guess.
        if sum(before_species['atoms'].values()) != 1 or sum(after_species['atoms'].values()) != 1:
            continue
        before = (before_species['charge_magnitude'] or 0) * (1 if before_species['charge_sign'] == '+' else -1)
        after = (after_species['charge_magnitude'] or 0) * (1 if after_species['charge_sign'] == '+' else -1)
        if before == after:
            continue
        derived.append({'element': track['element'], 'before': before, 'after': after,
                        'before_species': before_species['raw'], 'after_species': after_species['raw']})
    if not derived:
        raise PrimitiveDataUnavailable('no source-authorized oxidation-state values available')
    return derived


def _draw_oxidation_state_lane(c, x, y, w, h, params):
    """Delegates to the vendored ``OxidationLaneDiagram``.

    That engine is fully parameterised upstream (it documents "NO hardcoded
    fallback entities"), so Chemistry calls it directly rather than drawing a
    second, divergent lane. Values come from ``_oxidation_pairs``, which either
    reads explicit source data or derives monatomic-ion states — never guesses.
    """
    pairs = _oxidation_pairs(params)
    lane_h = h / len(pairs)
    for index, pair in enumerate(pairs):
        delta = pair['after'] - pair['before']
        OxidationLaneDiagram.draw_lane(
            c, x, y + h - (index + 1) * lane_h, w, lane_h - 4,
            reactant_label=pair['before_species'],
            reactant_on=_state_text(pair['before']),
            product_label=pair['after_species'],
            product_on=_state_text(pair['after']),
            delta_text='%s: state change %+d' % (pair['element'], delta),
            electron_text='%s — read the direction before naming any agent'
                          % ('increase' if delta > 0 else 'decrease'),
            title=params['title'] if index == 0 else params['title'] + ' (continued)')


def _draw_self_other_frame(c, x, y, w, h, params):
    top = panel(c, x, y, w, h, params['title'])
    label(c, x + 12, top, params['attention_target'] or 'What it undergoes versus what it causes.',
          size=6.6, color='muted', width=w - 24)
    col_w = (w - 34) / 2
    col_h = h - 58
    col_y = y + 20
    for index, (caption, note, accent) in enumerate((
            ('SELF — what this species undergoes', 'Fill this from the evidence first.', 'blue'),
            ('OTHER — what it causes in the other species', 'Fill this only after SELF is settled.', 'green'))):
        cx = x + 12 + index * (col_w + 10)
        box(c, cx, col_y, col_w, col_h, fill='panel', stroke=accent, width=0.9)
        label(c, cx + 8, col_y + col_h - 12, caption, size=6.6, color=accent, font=BOLD, width=col_w - 16)
        for line in range(2):
            rule_line(c, cx + 8, col_y + col_h - 26 - line * 14, cx + col_w - 8,
                      color='faint', dash=(2, 2))
        label(c, cx + 8, col_y + 6, note, size=6.2, color='muted', width=col_w - 16)
    arrow(c, x + 12 + col_w + 2, col_y + col_h / 2, x + 12 + col_w + 8, col_y + col_h / 2,
          color='faint', width=0.9, head=3.5)
    label(c, x + 12, y + 6, 'Attach the role name only after both columns are filled.',
          size=6.3, color='muted', width=w - 24)


def _split_converge_branches(params):
    """Branches for ONE element only; a topology never mixes elements."""
    pairs = _oxidation_pairs(params)
    by_element = {}
    for pair in pairs:
        by_element.setdefault(pair['element'], []).append(pair)
    for element in sorted(by_element):
        group = by_element[element]
        states = {(p['after_species'], p['after']) for p in group}
        if len(states) > 1:
            return group[0], sorted(states, key=lambda s: s[1])
    first = pairs[0]
    return first, [(first['after_species'], first['after'])]


def _draw_split_converge(c, x, y, w, h, params):
    hub, targets = _split_converge_branches(params)
    top = panel(c, x, y, w, h, params['title'])
    label(c, x + 12, top, params['attention_target'] or 'Same element, branches labelled by state.',
          size=6.6, color='muted', width=w - 24)
    cy = y + h / 2 - 8
    hub_x = x + 60
    branch_x = x + w - 120
    element = hub['element']
    box(c, hub_x - 34, cy - 13, 68, 26, fill='blue_fill', stroke='blue', radius=5)
    label(c, hub_x, cy - 3, hub['before_species'], size=8.4, color='ink', font=BOLD,
          align='center', width=62)
    label(c, hub_x, cy - 21, 'state ' + _state_text(hub['before']), size=6.4, color='muted', align='center')
    span = 28 if len(targets) > 1 else 0
    for index, (text, state) in enumerate(targets[:2]):
        by = cy + span - index * 2 * span
        arrow(c, hub_x + 36, cy, branch_x - 4, by, color='amber', width=1.1, head=4.5)
        box(c, branch_x, by - 13, 76, 26, fill='teal_fill', stroke='teal', radius=5)
        label(c, branch_x + 38, by - 3, text, size=8.4, color='ink', font=BOLD, align='center', width=70)
        label(c, branch_x + 38, by - 21, 'state ' + _state_text(state), size=6.4, color='muted', align='center')
    label(c, x + 12, y + 6,
          'Same element (%s) on every branch — classify only after every state is read.' % element,
          size=6.3, color='muted', width=w - 24)


def _draw_evidence_chain(c, x, y, w, h, params):
    top = panel(c, x, y, w, h, params['title'])
    stages = (
        ('EVIDENCE', params['observation'] or params['instructional_job'] or
         'What the task actually records.', 'blue'),
        ('LINK', params['attention_target'] or 'Which evidence supports which part of the claim.', 'amber'),
        ('CLAIM', params['claim'] or params['learner_action'] or
         'The chemical statement being tested.', 'green'),
    )
    box_w = (w - 24 - 2 * 18) / 3
    box_h = h - 50
    box_y = y + 16
    for index, (caption, text, accent) in enumerate(stages):
        bx = x + 12 + index * (box_w + 18)
        box(c, bx, box_y, box_w, box_h, fill='panel', stroke=accent, width=0.9)
        label(c, bx + 8, box_y + box_h - 12, caption, size=6.6, color=accent, font=BOLD)
        paragraph(c, bx + 8, box_y + box_h - 26, text, box_w - 16, size=6.4, color='ink', max_lines=6)
        if index < 2:
            arrow(c, bx + box_w + 2, box_y + box_h / 2, bx + box_w + 15, box_y + box_h / 2,
                  color='faint', width=1.0, head=4)
    label(c, x + 12, y + 5, 'An inference is only as strong as the recorded evidence behind it.',
          size=6.3, color='muted', width=w - 24)
    _ = top


def _draw_apparatus_flow(c, x, y, w, h, params):
    panel(c, x, y, w, h, params['title'])
    stages = (
        ('PROPERTY USED', params['attention_target'] or 'The property the method depends on.'),
        ('APPARATUS / METHOD', params['instructional_job'] or 'The apparatus feature that exploits it.'),
        ('INTENDED OBSERVATION', params['learner_action'] or 'What the method is meant to reveal.'),
    )
    step_h = (h - 34) / 3
    for index, (caption, text) in enumerate(stages):
        sy = y + h - 30 - (index + 1) * step_h
        body_h = step_h - 8
        box(c, x + 12, sy, w - 24, body_h, fill='panel', stroke='teal', radius=4, width=0.8)
        c.setFillColor(_c('teal'))
        c.rect(x + 12, sy, 4, body_h, fill=1, stroke=0)
        label(c, x + 24, sy + body_h - 11, caption, size=6.6, color='teal', font=BOLD)
        paragraph(c, x + 24, sy + body_h - 21, text, w - 48, size=6.5, color='ink', max_lines=1)
        if index < 2:
            arrow(c, x + w / 2, sy - 0.5, x + w / 2, sy - 6.5, color='faint', width=0.9, head=3.5)


def _draw_observation_inference_table(c, x, y, w, h, params):
    top = panel(c, x, y, w, h, params['title'])
    label(c, x + 12, top, params['attention_target'] or 'Literal evidence versus interpreted claim.',
          size=6.6, color='muted', width=w - 24)
    table_y = y + 16
    table_h = h - 54
    col_w = (w - 24) / 2
    header_h = 15
    for index, (caption, accent, fill) in enumerate((('OBSERVATION — what was recorded', 'blue', 'blue_fill'),
                                                     ('INFERENCE — what is claimed from it', 'amber', 'amber_fill'))):
        cx = x + 12 + index * col_w
        c.setFillColor(_c(fill))
        c.setStrokeColor(_c('rule'))
        c.setLineWidth(0.6)
        c.rect(cx, table_y + table_h - header_h, col_w, header_h, fill=1, stroke=1)
        label(c, cx + 6, table_y + table_h - header_h + 4.8, caption, size=6.5,
              color=accent, font=BOLD, width=col_w - 12)
    rows = 3
    row_h = (table_h - header_h) / rows
    for row in range(rows):
        ry = table_y + (rows - row - 1) * row_h
        for index in range(2):
            c.setStrokeColor(_c('rule'))
            c.setLineWidth(0.5)
            c.rect(x + 12 + index * col_w, ry, col_w, row_h, fill=0, stroke=1)
    first = params['observation'] or params['instructional_job']
    if first:
        paragraph(c, x + 18, table_y + table_h - header_h - 12, first, col_w - 12,
                  size=6.4, color='ink', max_lines=2)
    label(c, x + 12, y + 5, params['learner_action'] or 'Place each statement in the correct column.',
          size=6.3, color='muted', width=w - 24)


def _draw_macro_observation(c, x, y, w, h, params):
    panel(c, x, y, w, h, params['title'])
    evidence = params['observation'] or params['instructional_job'] or params['attention_target']
    if not evidence:
        raise PrimitiveDataUnavailable('macro observation view needs recorded evidence text')
    card_h = h - 58
    box(c, x + 12, y + 30, w - 24, card_h, fill='blue_fill', stroke='blue', width=1.0)
    c.setFillColor(_c('blue'))
    c.circle(x + 26, y + 30 + card_h - 14, 5.4, fill=1, stroke=0)
    label(c, x + 26, y + 30 + card_h - 16.4, 'i', size=7, color='navy_text', font=BOLD, align='center')
    label(c, x + 36, y + 30 + card_h - 16.4, 'RECORDED AT THE MACROSCOPIC LEVEL', size=6.6,
          color='blue', font=BOLD)
    paragraph(c, x + 20, y + 30 + card_h - 30, evidence, w - 40, size=7.0, color='ink', max_lines=3)
    c.saveState()
    c.setStrokeColor(_c('faint'))
    c.setLineWidth(0.8)
    c.setDash(3, 2)
    c.roundRect(x + 12, y + 10, w - 24, 17, 4, fill=0, stroke=1)
    c.restoreState()
    label(c, x + 20, y + 16, 'Nothing has been inferred yet — this box stays empty until you decide.',
          size=6.3, color='faint', width=w - 44)


def _draw_minimal_contrast(c, x, y, w, h, params):
    top = panel(c, x, y, w, h, params['title'])
    label(c, x + 12, top, params['attention_target'] or 'Exactly one decisive feature differs.',
          size=6.6, color='muted', width=w - 24)
    held = params['instructional_job'] or 'Everything except the decisive feature is held constant.'
    box(c, x + 12, y + h - 60, w - 24, 15, fill='panel', stroke='rule', radius=3)
    label(c, x + 18, y + h - 55.5, 'HELD CONSTANT: ' + held, size=6.3, color='muted', width=w - 36)
    case_w = (w - 34) / 2
    case_h = h - 82
    case_y = y + 16
    species = params['species'][0] if params['species'] else None
    for index, (caption, accent) in enumerate((('CASE A', 'blue'), ('CASE B', 'red'))):
        cx = x + 12 + index * (case_w + 10)
        box(c, cx, case_y, case_w, case_h, fill='panel', stroke=accent, width=0.9)
        label(c, cx + 8, case_y + case_h - 12, caption, size=6.6, color=accent, font=BOLD)
        if species is not None:
            size = 13
            draw_species(c, cx + (case_w - species_width(c, species, size)) / 2,
                         case_y + case_h / 2 - 2, species, size=size,
                         highlight='SUBSCRIPT' if index == 0 else 'CHARGE')
        rule_line(c, cx + 8, case_y + 15, cx + case_w - 8, color='faint', dash=(3, 2))
        label(c, cx + 8, case_y + 5, 'Predict this case before reading on.', size=6.1, color='faint')
    c.setFillColor(_c('red'))
    c.circle(x + 12 + case_w + 5, case_y + case_h / 2, 6.5, fill=1, stroke=0)
    label(c, x + 12 + case_w + 5, case_y + case_h / 2 - 2.4, '≠', size=8,
          color='navy_text', font=BOLD, align='center')


def _draw_check_strip(c, x, y, w, h, params):
    checks = params['checks'] or [params['learner_action'] or 'Run the checks this task requires.']
    panel(c, x, y, w, h, params['title'])
    tile_h = (h - 30) / max(len(checks), 1)
    for index, check in enumerate(checks):
        ty = y + h - 26 - (index + 1) * tile_h + 2
        box(c, x + 12, ty, w - 24, tile_h - 4, fill='panel', stroke='rule', radius=3)
        tick_box(c, x + 20, ty + tile_h / 2 - 6)
        label(c, x + 36, ty + tile_h / 2 - 2.6, check, size=6.8, color='ink', width=w - 60)
        c.setFillColor(_c('teal'))
        c.rect(x + 12, ty, 3, tile_h - 4, fill=1, stroke=0)


RENDERERS = {
    'MACRO_OBSERVATION_VIEW': _draw_macro_observation,
    'PARTICLE_MODEL_VIEW': _draw_particle_model_view,
    'MACRO_PARTICLE_SYMBOLIC_BRIDGE': _draw_bridge,
    'FORMULA_ANATOMY_VIEW': _draw_formula_anatomy,
    'CHARGE_SUBSCRIPT_CONTRAST': _draw_charge_subscript_contrast,
    'COEFFICIENT_SUBSCRIPT_CONTRAST': _draw_coefficient_subscript_contrast,
    'CONSERVATION_LEDGER': _draw_conservation_ledger,
    'REACTION_BEFORE_AFTER_MAP': _draw_reaction_before_after,
    'SPECIES_ROLE_MAP': _draw_species_role_map,
    'RULE_PRIORITY_LADDER': _draw_rule_priority_ladder,
    'CONDITION_EXCEPTION_GATE': _draw_condition_gate,
    'STRUCTURE_SITE_ANNOTATION': _draw_structure_site,
    'OXIDATION_STATE_LANE': _draw_oxidation_state_lane,
    'SELF_OTHER_AGENT_FRAME': _draw_self_other_frame,
    'SPLIT_CONVERGE_TOPOLOGY': _draw_split_converge,
    'EVIDENCE_CLAIM_REASONING_CHAIN': _draw_evidence_chain,
    'APPARATUS_METHOD_FLOW': _draw_apparatus_flow,
    'OBSERVATION_INFERENCE_TABLE': _draw_observation_inference_table,
    'MINIMAL_CHEMISTRY_CONTRAST': _draw_minimal_contrast,
    'FORMULA_EQUATION_CHECK_STRIP': _draw_check_strip,
}

BASE_HEIGHTS = {
    'MACRO_OBSERVATION_VIEW': 110,
    'PARTICLE_MODEL_VIEW': 122,
    'MACRO_PARTICLE_SYMBOLIC_BRIDGE': 136,
    'FORMULA_ANATOMY_VIEW': 112,
    'CHARGE_SUBSCRIPT_CONTRAST': 134,
    'COEFFICIENT_SUBSCRIPT_CONTRAST': 134,
    'CONSERVATION_LEDGER': 124,
    'REACTION_BEFORE_AFTER_MAP': 140,
    'SPECIES_ROLE_MAP': 120,
    'RULE_PRIORITY_LADDER': 140,
    'CONDITION_EXCEPTION_GATE': 152,
    'STRUCTURE_SITE_ANNOTATION': 108,
    'OXIDATION_STATE_LANE': 96,
    'SELF_OTHER_AGENT_FRAME': 116,
    'SPLIT_CONVERGE_TOPOLOGY': 122,
    'EVIDENCE_CLAIM_REASONING_CHAIN': 128,
    'APPARATUS_METHOD_FLOW': 124,
    'OBSERVATION_INFERENCE_TABLE': 116,
    'MINIMAL_CHEMISTRY_CONTRAST': 132,
    'FORMULA_EQUATION_CHECK_STRIP': 78,
}


def primitive_height(kind, params, width=None):
    """Deterministic drawn height for one primitive, before placement."""
    if kind not in BASE_HEIGHTS:
        raise PrimitiveDataUnavailable('unknown teaching primitive: ' + str(kind))
    height = float(BASE_HEIGHTS[kind])
    if kind == 'FORMULA_ANATOMY_VIEW':
        try:
            positions = {k for k, _ in _pick_species(params, 'BOTH')['runs']}
        except PrimitiveDataUnavailable:
            positions = set()
        annotated = len(positions & {'COEFFICIENT', 'SUBSCRIPT', 'CHARGE', 'STATE'})
        if annotated > 2:
            height += 40.0
    if kind == 'CONSERVATION_LEDGER' and params.get('equation'):
        height += 16.0 * max(len(conservation_rows(params['equation'])) - 2, 0)
    if kind == 'PARTICLE_MODEL_VIEW':
        total = sum(int(p.get('count', 0)) for p in params.get('particles', [])) or 1
        height += 34.0 * max((total - 1) // 4, 0)
    if kind == 'FORMULA_EQUATION_CHECK_STRIP':
        height += 17.0 * max(len(params.get('checks') or [1]) - 1, 0)
    if kind == 'SPECIES_ROLE_MAP':
        height += 22.0 * max(len(params.get('species_roles') or []) - 2, 0)
    if kind == 'OXIDATION_STATE_LANE':
        try:
            height *= max(len(_oxidation_pairs(params)), 1)
        except PrimitiveDataUnavailable:
            pass
    if kind == 'RULE_PRIORITY_LADDER':
        height += 16.0 * max(len(params.get('condition_context') or []) - 1, 0)
    return height


def render_primitive(kind, params, canvas, bbox):
    """Validate, then draw one teaching primitive; return placement evidence.

    ``bbox`` is ``(x, y_bottom, width, height)`` in PDF user space. The vendored
    ``VisualSemanticValidator`` runs *before* any drawing operation, so an
    ungrounded species, a broken atom ledger or an inverted agent role fails
    closed instead of reaching the page. The return value is the actual drawn
    rectangle, emitted at the same moment as the drawing operations so the
    PhysicalPageMap records real placement rather than a planned one.
    """
    if kind not in RENDERERS:
        raise PrimitiveDataUnavailable('unknown teaching primitive: ' + str(kind))
    x, y, w, h = bbox
    if w <= 0 or h <= 0:
        raise PrimitiveDataUnavailable('degenerate bbox for ' + kind)
    _prevalidate(kind, params)
    canvas.saveState()
    try:
        RENDERERS[kind](canvas, x, y, w, h, params)
    finally:
        canvas.restoreState()
    return {
        'primitive': kind,
        'x0': round(float(x), 2),
        'y0': round(float(y), 2),
        'x1': round(float(x + w), 2),
        'y1': round(float(y + h), 2),
        'validated_by': 'MasterTemplates.VisualSemanticValidator',
        'accessibility_text': params.get('accessibility_text') or params.get('title'),
    }


__all__ = [
    'ConservationError',
    'PrimitiveDataUnavailable',
    'PRIMITIVE_KINDS',
    'PRIMITIVE_TITLES',
    'RolePolarityError',
    'UPSTREAM_HARDCODED_ENGINES',
    'UngroundedEntityError',
    'VisualValidationError',
    'build_params',
    'primitive_height',
    'render_primitive',
    'use_fonts',
]
