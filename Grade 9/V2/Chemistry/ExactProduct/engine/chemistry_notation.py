#!/usr/bin/env python3
"""Subject-wide Chemistry notation parser for the V2 exact-product renderer.

This module is deliberately generic. It knows about chemical *notation*
(coefficient / element symbol / subscript / ionic charge / state symbol /
reaction arrow) and nothing about any particular topic. Redox, conservation,
acid-base and every other reaction type are handled as data flowing through the
same parse, never as separate code paths or separate schema shapes.

The parser exists so that the renderer can draw real vector diagrams whose
geometry is derived from the *actual* source-authorized notation tokens carried
by the C-H representation bundle, instead of hardcoded example formulas.
"""

import re

SUBSCRIPT_DIGITS = '₀₁₂₃₄₅₆₇₈₉'
SUPERSCRIPT_DIGITS = '⁰¹²³⁴⁵⁶⁷⁸⁹'
SUPERSCRIPT_PLUS = '⁺'
SUPERSCRIPT_MINUS = '⁻'
ARROWS = ('⇌', '⟶', '→', '=>', '->')
STATE_SYMBOLS = ('(s)', '(l)', '(g)', '(aq)')

_SUB_TO_ASCII = {c: str(i) for i, c in enumerate(SUBSCRIPT_DIGITS)}
_SUP_TO_ASCII = {c: str(i) for i, c in enumerate(SUPERSCRIPT_DIGITS)}
_ASCII_TO_SUB = {v: k for k, v in _SUB_TO_ASCII.items()}
_ASCII_TO_SUP = {v: k for k, v in _SUP_TO_ASCII.items()}

_ELEMENT = re.compile(r'[A-Z][a-z]{0,2}')


def to_subscript(value):
    return ''.join(_ASCII_TO_SUB.get(ch, ch) for ch in str(value))


def to_superscript(value):
    out = []
    for ch in str(value):
        if ch == '+':
            out.append(SUPERSCRIPT_PLUS)
        elif ch in '-−':
            out.append(SUPERSCRIPT_MINUS)
        else:
            out.append(_ASCII_TO_SUP.get(ch, ch))
    return ''.join(out)


def _ascii_digits(text, table):
    return ''.join(table.get(ch, ch) for ch in text)


class ChemistryNotationError(ValueError):
    """Raised when a source-authorized token cannot be parsed as notation."""


def _strip_state(text):
    for state in STATE_SYMBOLS:
        if text.endswith(state):
            return text[: -len(state)].strip(), state
    return text, None


def _strip_charge(text):
    """Split a trailing ionic charge from the formula body.

    Accepts the contract-required Unicode form (``Fe³⁺``) and also tolerates
    flat ASCII (``Fe3+``) so that a non-conforming upstream token is parsed and
    reported rather than silently mis-drawn.
    """
    unicode_charge = re.search(r'([' + SUPERSCRIPT_DIGITS + r']*)([' + SUPERSCRIPT_PLUS + SUPERSCRIPT_MINUS + r'])$', text)
    if unicode_charge:
        magnitude = _ascii_digits(unicode_charge.group(1), _SUP_TO_ASCII) or '1'
        sign = '+' if unicode_charge.group(2) == SUPERSCRIPT_PLUS else '-'
        return text[: unicode_charge.start()], magnitude, sign, True
    ascii_charge = re.search(r'(\d*)([+-])$', text)
    if ascii_charge:
        magnitude = ascii_charge.group(1) or '1'
        sign = ascii_charge.group(2)
        return text[: ascii_charge.start()], magnitude, sign, False
    return text, None, None, True


def _charge_display(magnitude, sign):
    if magnitude is None:
        return None
    head = '' if magnitude == '1' else magnitude
    return to_superscript(head + sign)


def _parse_body(body):
    """Parse a charge/state-free formula body into runs and an atom tally.

    Supports nested groups such as ``Ca(OH)₂`` and ``Fe₂(SO₄)₃``.
    """
    runs = []
    atoms = {}
    index = 0

    def multiply(tally, factor):
        return {k: v * factor for k, v in tally.items()}

    def merge(target, other):
        for k, v in other.items():
            target[k] = target.get(k, 0) + v

    def read_count():
        nonlocal index
        digits = ''
        while index < len(body) and (body[index] in SUBSCRIPT_DIGITS or body[index].isdigit()):
            digits += body[index]
            index += 1
        if not digits:
            return 1, None
        ascii_value = _ascii_digits(digits, _SUB_TO_ASCII)
        return int(ascii_value), ascii_value

    def parse_sequence(depth):
        nonlocal index
        local = {}
        while index < len(body):
            char = body[index]
            if char == ')':
                if depth == 0:
                    raise ChemistryNotationError('unbalanced group in ' + body)
                return local
            if char == '(':
                index += 1
                runs.append(('GROUP_OPEN', '('))
                inner = parse_sequence(depth + 1)
                if index >= len(body) or body[index] != ')':
                    raise ChemistryNotationError('unbalanced group in ' + body)
                index += 1
                runs.append(('GROUP_CLOSE', ')'))
                count, raw = read_count()
                if raw is not None:
                    runs.append(('SUBSCRIPT', raw))
                merge(local, multiply(inner, count))
                continue
            match = _ELEMENT.match(body, index)
            if not match:
                raise ChemistryNotationError('unreadable notation run in ' + body)
            symbol = match.group(0)
            index = match.end()
            runs.append(('ELEMENT', symbol))
            count, raw = read_count()
            if raw is not None:
                runs.append(('SUBSCRIPT', raw))
            merge(local, {symbol: count})
        if depth:
            raise ChemistryNotationError('unbalanced group in ' + body)
        return local

    atoms = parse_sequence(0)
    return runs, atoms


def parse_species(token):
    """Parse one source-authorized species token into structured notation.

    Returns a dict with the positional runs a renderer needs to draw formula
    anatomy, plus the atom tally a conservation ledger needs.
    """
    raw = str(token).strip()
    if not raw:
        raise ChemistryNotationError('empty species token')
    text, state = _strip_state(raw)
    coefficient_match = re.match(r'^(\d+)', text)
    coefficient = int(coefficient_match.group(1)) if coefficient_match else 1
    coefficient_raw = coefficient_match.group(1) if coefficient_match else None
    text = text[coefficient_match.end():] if coefficient_match else text
    body, magnitude, sign, unicode_charge = _strip_charge(text.strip())
    body = body.strip()
    if not body:
        raise ChemistryNotationError('species token has no formula body: ' + raw)
    body_runs, atoms = _parse_body(body)
    runs = []
    if coefficient_raw is not None:
        runs.append(('COEFFICIENT', coefficient_raw))
    runs.extend(body_runs)
    charge = _charge_display(magnitude, sign)
    if charge is not None:
        runs.append(('CHARGE', charge))
    if state is not None:
        runs.append(('STATE', state))
    return {
        'raw': raw,
        'coefficient': coefficient,
        'coefficient_text': coefficient_raw,
        'body': body,
        'atoms': {k: v for k, v in sorted(atoms.items())},
        'total_atoms': {k: v * coefficient for k, v in sorted(atoms.items())},
        'charge': charge,
        'charge_magnitude': int(magnitude) if magnitude else None,
        'charge_sign': sign,
        'charge_unicode_conforming': unicode_charge,
        'state': state,
        'runs': runs,
        'subscripts': [value for kind, value in body_runs if kind == 'SUBSCRIPT'],
        'elements': [value for kind, value in body_runs if kind == 'ELEMENT'],
    }


def split_arrow(token):
    for arrow in ARROWS:
        if arrow in token:
            left, right = token.split(arrow, 1)
            return left.strip(), arrow, right.strip()
    return None


def is_equation(token):
    return split_arrow(str(token)) is not None


def parse_equation(token):
    """Parse a source-authorized reaction token into two tallied sides."""
    raw = str(token).strip()
    split = split_arrow(raw)
    if split is None:
        raise ChemistryNotationError('token is not a reaction equation: ' + raw)
    left_text, arrow, right_text = split

    def side(text):
        species = []
        for part in re.split(r'\s\+\s', text):
            part = part.strip()
            if part:
                species.append(parse_species(part))
        if not species:
            raise ChemistryNotationError('reaction side has no species: ' + raw)
        return species

    left = side(left_text)
    right = side(right_text)
    return {
        'raw': raw,
        'arrow': arrow,
        'reactants': left,
        'products': right,
        'reactant_tally': tally(left),
        'product_tally': tally(right),
    }


def tally(species_list):
    total = {}
    for species in species_list:
        for element, count in species['total_atoms'].items():
            total[element] = total.get(element, 0) + count
    return {k: total[k] for k in sorted(total)}


def charge_tally(species_list):
    total = 0
    for species in species_list:
        if species['charge_magnitude'] is None:
            continue
        signed = species['charge_magnitude'] * (1 if species['charge_sign'] == '+' else -1)
        total += signed * species['coefficient']
    return total


def conservation_rows(equation):
    """Per-element before/after rows for a conservation ledger primitive."""
    elements = sorted(set(equation['reactant_tally']) | set(equation['product_tally']))
    rows = []
    for element in elements:
        before = equation['reactant_tally'].get(element, 0)
        after = equation['product_tally'].get(element, 0)
        rows.append({'element': element, 'before': before, 'after': after, 'balanced': before == after})
    return rows


def element_tracks(equation):
    """Track every element symbol from the reactant side to the product side.

    Purely notational: an element is 'tracked' wherever its symbol appears. No
    reaction-type knowledge is used, so the same code serves Redox,
    displacement, precipitation and every other family. ``changed`` means the
    element's host species text differs between the two sides, which is the
    only claim the notation itself supports.
    """
    tracks = []
    elements = sorted(set(equation['reactant_tally']) | set(equation['product_tally']))
    for element in elements:
        left = [i for i, s in enumerate(equation['reactants']) if element in s['atoms']]
        right = [i for i, s in enumerate(equation['products']) if element in s['atoms']]
        left_text = sorted({equation['reactants'][i]['raw'] for i in left})
        right_text = sorted({equation['products'][i]['raw'] for i in right})
        tracks.append({
            'element': element,
            'reactant_indices': left,
            'product_indices': right,
            'changed': left_text != right_text,
            'present_both_sides': bool(left) and bool(right),
        })
    return tracks


def ascii_ambiguity(token):
    """Report flat-ASCII notation the C-H notation contract forbids."""
    text = str(token)
    problems = []
    if re.search(r'[A-Za-z]\d', text):
        problems.append('FLAT_ASCII_SUBSCRIPT')
    if re.search(r'\d[+-](?![A-Za-z0-9])', text) or re.search(r'[A-Za-z]\d[+-]', text):
        problems.append('FLAT_ASCII_CHARGE')
    if re.search(r'(?<![a-z])e-(?![a-z])', text):
        problems.append('FLAT_ASCII_ELECTRON')
    return sorted(set(problems))
