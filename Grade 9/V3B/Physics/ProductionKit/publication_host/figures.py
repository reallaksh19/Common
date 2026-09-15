"""Quantitative SVG instances from source atoms; no fixture geometry or defaults."""

from html import escape

from v3b.contracts import digest, require, strings, text
from .science import numeric_atom

WIDTH, HEIGHT, PAD = 560, 360, 58


def figure(ctx, block):
    spec = block["scene"]
    require(spec.get("kind") in {"VECTOR", "GRAPH"}, "FIGURE_FAMILY_UNSUPPORTED")
    for key in ("frame", "x_label", "y_label", "caption"):
        text(spec.get(key), "FIGURE_CONTEXT_REQUIRED")
    if spec["kind"] == "VECTOR":
        return _vector(ctx, block)
    return _graph(ctx, block)


def _bound(ctx, block, atom_id, unit):
    require(atom_id in block["source_atom_ids"], "FIGURE_SOURCE_BINDING_MISSING")
    return numeric_atom(ctx, atom_id, unit)


def _bounds(xs, ys):
    xmin, xmax, ymin, ymax = min(0, *xs), max(0, *xs), min(0, *ys), max(0, *ys)
    if xmin == xmax:
        xmin, xmax = -1, 1
    if ymin == ymax:
        ymin, ymax = -1, 1
    return xmin, xmax, ymin, ymax


def _mapping(bounds, equal, width=WIDTH, height=HEIGHT):
    xmin, xmax, ymin, ymax = bounds
    sx, sy = (width - 2 * PAD) / (xmax - xmin), (height - 2 * PAD) / (ymax - ymin)
    if equal:
        sx = sy = min(sx, sy)
    left = (width - (xmax - xmin) * sx) / 2
    top = (height - (ymax - ymin) * sy) / 2
    return lambda x, y: (left + (x - xmin) * sx, top + (ymax - y) * sy), (sx, sy)


def _line(p, q, **attrs):
    extra = " ".join(f'{k.replace("_", "-")}="{escape(str(v), quote=True)}"' for k, v in attrs.items())
    return f'<line x1="{p[0]:.6f}" y1="{p[1]:.6f}" x2="{q[0]:.6f}" y2="{q[1]:.6f}" {extra}/>'


def _label(x, y, value, anchor="middle"):
    return f'<text x="{x:.3f}" y="{y:.3f}" text-anchor="{anchor}" font-size="14">{escape(str(value))}</text>'


def _axes(spec, bounds, point, width=WIDTH, height=HEIGHT):
    xmin, xmax, ymin, ymax = bounds
    axis_x = 0 if xmin <= 0 <= xmax else xmin
    axis_y = 0 if ymin <= 0 <= ymax else ymin
    rows = [_line(point(xmin, axis_y), point(xmax, axis_y), stroke="#64748b"),
            _line(point(axis_x, ymin), point(axis_x, ymax), stroke="#64748b")]
    rows += [_label(width / 2, height - 10, spec["x_label"]),
             _label(10, 20, spec["y_label"], "start"),
             _label(point(axis_x, axis_y)[0] - 10, point(axis_x, axis_y)[1] + 20, f'{axis_x:g}')]
    if axis_y != 0:
        rows.append(_label(point(axis_x, axis_y)[0] - 8, point(axis_x, axis_y)[1], f'{axis_y:g}', 'end'))
    return rows


def _svg(block, rows, evidence, width=WIDTH, height=HEIGHT):
    title = escape(block["scene"]["caption"])
    rows = ['<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" '
            'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            '<path d="M 0 0 L 10 5 L 0 10 z" fill="#135b89"/></marker></defs>'] + rows
    xml = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
           f'role="img" aria-label="{title}" data-scene-digest="{digest(block["scene"])}">'
           f'<title>{title}</title><rect width="100%" height="100%" fill="white"/><g font-family="sans-serif" fill="#172c42">'
           + "".join(rows) + '</g></svg>')
    return xml, {**evidence, "frame": block["scene"]["frame"], "quantitative": True,
                 "width": width, "height": height, "minimum_label_px": 14}


def _vector(ctx, block):
    spec = block["scene"]
    text(spec.get("symbol"), "VECTOR_SYMBOL_REQUIRED")
    unit = text(spec.get("unit"), "VECTOR_UNIT_REQUIRED")
    x = _bound(ctx, block, spec["x_atom"], unit)
    y = _bound(ctx, block, spec["y_atom"], unit)
    bounds = _bounds([x], [y])
    xmin, xmax, ymin, ymax = bounds
    scale = min((WIDTH - 2 * PAD) / (xmax - xmin), (HEIGHT - 2 * PAD) / (ymax - ymin))
    width = max(280, (xmax - xmin) * scale + 2 * PAD)
    height = max(180, (ymax - ymin) * scale + 2 * PAD)
    point, scales = _mapping(bounds, equal=True, width=width, height=height)
    origin, end = point(0, 0), point(x, y)
    rows = _axes(spec, bounds, point, width=width, height=height)
    rows += [_line(origin, point(x, 0), stroke="#7b96ab", stroke_dasharray="5 3"),
             _line(point(x, 0), end, stroke="#7b96ab", stroke_dasharray="5 3")]
    if x == y == 0:
        rows.append(f'<circle cx="{origin[0]}" cy="{origin[1]}" r="4" fill="#135b89"/>')
    else:
        rows.append(_line(origin, end, stroke="#135b89", stroke_width="2.5",
                          marker_end="url(#arrow)", data_vector="resultant"))
    rows.append(f'<text x="{width / 2}" y="38" text-anchor="middle" font-size="16">'
                f'<tspan font-weight="bold">{escape(spec["symbol"])}</tspan>'
                f'<tspan> = ({x:g}, {y:g}) {escape(unit)}</tspan></text>')
    return _svg(block, rows, dict(kind="VECTOR", components=[x, y], unit=unit,
                                 origin=list(origin), endpoint=list(end), scale=list(scales)), width, height)


def _graph(ctx, block):
    spec = block["scene"]
    pairs = spec["points"]
    require(len(pairs) >= 2, "GRAPH_POINTS_REQUIRED")
    values = [(_bound(ctx, block, p[0], spec["x_unit"]),
               _bound(ctx, block, p[1], spec["y_unit"])) for p in pairs]
    require(all(b[0] > a[0] for a, b in zip(values, values[1:])), "GRAPH_DOMAIN_NOT_INCREASING")
    bounds = _bounds([p[0] for p in values], [p[1] for p in values])
    if 'y_min_atom' in spec:
        ymin = _bound(ctx, block, spec['y_min_atom'], spec['y_unit'])
        require(ymin <= min(p[1] for p in values) and ymin < bounds[3], 'GRAPH_RANGE_CLIPS_DATA')
        bounds = (bounds[0], bounds[1], ymin, bounds[3])
    point, scales = _mapping(bounds, equal=False)
    rows = _axes(spec, bounds, point)
    pixels = [point(*v) for v in values]
    for a, b in zip(pixels, pixels[1:]):
        rows.append(_line(a, b, stroke="#135b89", stroke_width="2.5", data_graph="segment"))
    for v, p in zip(values, pixels):
        rows.append(f'<circle cx="{p[0]}" cy="{p[1]}" r="3" fill="#135b89"/>')
        rows.append(_label(p[0], p[1] - 10, f'({v[0]:g}, {v[1]:g})'))
    return _svg(block, rows, dict(kind="GRAPH", points=values, pixels=pixels,
                                 scale=list(scales), y_axis_min=bounds[2]))
