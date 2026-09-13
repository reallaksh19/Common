#!/usr/bin/env python3
"""P-G authored-instance resolver: a worked example must resolve to an actual number.

Before this module a Core (1) "worked example" was an authoring *plan* — "select the
model, choose the relation, solve" — with no situation, no quantities and no result. A
learner cannot watch that being solved.

An authored instance is data: a situation, a declared frame, typed ``givens``, one
``unknown``, a typed ``reasoning_route`` and the checks. This module is the engine that
makes the data load-bearing:

* it evaluates each route state's ``equation`` with a restricted arithmetic evaluator
  (no ``eval``: an ``ast`` whitelist of arithmetic nodes, names and a fixed function set);
* it proves the route actually **transforms state** — every state's inputs must already
  be known, and the set of known symbols must grow through the route;
* it recomputes ``final_answer`` rather than trusting it, so a declared answer that does
  not follow from the declared route is a failure, not a claim;
* it runs the declared ``independent_verification`` as real arithmetic on a genuinely
  different expression, and rejects a "verification" that is the solving route again;
* it expands the declared per-given value lists into deterministic variants, so guided,
  faded, independent, retry and Appendix A items are different numbers on the same
  physics — each with its own computed answer, none of them asserted by hand.

Everything topic-specific lives in the instance registry. This engine knows arithmetic,
route structure and answer custody, and no Physics topic at all.
"""
from __future__ import annotations

import ast
import math
import re

# ---------------------------------------------------------------- falsifiers
WORKED_EXAMPLE_UNINSTANTIATED = "WORKED_EXAMPLE_UNINSTANTIATED"
WORKED_EXAMPLE_FINAL_ANSWER_MISSING = "WORKED_EXAMPLE_FINAL_ANSWER_MISSING"
WORKED_EXAMPLE_REASONING_DOES_NOT_TRANSFORM_STATE = (
    "WORKED_EXAMPLE_REASONING_DOES_NOT_TRANSFORM_STATE")
LEARNER_QUESTION_WITHOUT_ANSWER = "LEARNER_QUESTION_WITHOUT_ANSWER"
SELF_CHECK_SUBSTITUTED_FOR_ANSWER = "SELF_CHECK_SUBSTITUTED_FOR_ANSWER"
VERIFICATION_ROUTE_NOT_INDEPENDENT = "VERIFICATION_ROUTE_NOT_INDEPENDENT"
INSTANCE_VARIANT_VIOLATES_DECLARED_CONSTRAINT = "INSTANCE_VARIANT_VIOLATES_DECLARED_CONSTRAINT"

# Route-state roles. These are internal identifiers: the learner never reads them, the
# learner-copy registry maps them, and the schema/falsifiers keep using them verbatim.
ROUTE_ROLES = ("FRAME", "REPRESENT", "MODEL", "EXECUTE", "INTERPRET", "VERIFY")
COMPUTATIONAL_ROLES = ("EXECUTE",)

# Canonical P-D reasoning roles each route-state role stands for, so P-G never invents a
# reasoning vocabulary of its own.
ROUTE_ROLE_TO_CANONICAL = {
    "FRAME": ["DEFINE_SYSTEM", "CHOOSE_FRAME"],
    "REPRESENT": ["REPRESENT", "EXTRACT_KNOWNS_AND_HIDDEN_FACTS"],
    "MODEL": ["SELECT_MODEL", "CHECK_MODEL_VALIDITY", "CHOOSE_RELATION"],
    "EXECUTE": ["SOLVE"],
    "INTERPRET": ["INTERPRET_SIGN_DIRECTION", "INTERPRET_RESULT"],
    "VERIFY": ["CHECK_UNITS", "VERIFY_PHYSICAL_PLAUSIBILITY"],
}

TOLERANCE = 1e-6

FUNCTIONS = {
    "sqrt": math.sqrt,
    "abs": abs,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "radians": math.radians,
    "degrees": math.degrees,
    "min": min,
    "max": max,
    "round": round,
}
CONSTANTS = {"pi": math.pi, "e": math.e}

_ALLOWED_NODES = (
    ast.Expression, ast.BinOp, ast.UnaryOp, ast.Constant, ast.Name, ast.Load, ast.Call,
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow, ast.USub, ast.UAdd, ast.Mod,
    ast.Compare, ast.Lt, ast.LtE, ast.Gt, ast.GtE, ast.Eq, ast.NotEq,
    ast.BoolOp, ast.And, ast.Or,
)


class InstanceError(ValueError):
    """Raised with a falsifier code as its prefix, like every other engine here."""


def fail(code, detail=""):
    raise InstanceError(f"{code}: {detail}" if detail else code)


# ------------------------------------------------------------- safe arithmetic


def evaluate(expression, symbols, where=""):
    """Evaluate one arithmetic expression against a symbol table.

    Deliberately not ``eval``: the expression is parsed and every node type is checked
    against a whitelist, names must be declared symbols or known constants, and only the
    fixed function set above may be called.
    """
    try:
        tree = ast.parse(str(expression), mode="eval")
    except SyntaxError as exc:
        fail(WORKED_EXAMPLE_UNINSTANTIATED, f"{where}: cannot parse '{expression}' ({exc.msg})")
    for node in ast.walk(tree):
        if not isinstance(node, _ALLOWED_NODES):
            fail(WORKED_EXAMPLE_UNINSTANTIATED,
                 f"{where}: '{expression}' uses {type(node).__name__}, which is not arithmetic")
        if isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name) or node.func.id not in FUNCTIONS:
                fail(WORKED_EXAMPLE_UNINSTANTIATED, f"{where}: unknown function in '{expression}'")
        if isinstance(node, ast.Name) and node.id not in symbols and node.id not in CONSTANTS \
                and node.id not in FUNCTIONS:
            fail(WORKED_EXAMPLE_REASONING_DOES_NOT_TRANSFORM_STATE,
                 f"{where}: '{expression}' reads '{node.id}', which no earlier state produced")

    def walk(node):
        if isinstance(node, ast.Expression):
            return walk(node.body)
        if isinstance(node, ast.Constant):
            if not isinstance(node.value, (int, float)) or isinstance(node.value, bool):
                fail(WORKED_EXAMPLE_UNINSTANTIATED, f"{where}: non-numeric constant")
            return node.value
        if isinstance(node, ast.Name):
            if node.id in symbols:
                return symbols[node.id]
            return CONSTANTS[node.id]
        if isinstance(node, ast.UnaryOp):
            v = walk(node.operand)
            return -v if isinstance(node.op, ast.USub) else +v
        if isinstance(node, ast.BinOp):
            a, b = walk(node.left), walk(node.right)
            if isinstance(node.op, ast.Add):
                return a + b
            if isinstance(node.op, ast.Sub):
                return a - b
            if isinstance(node.op, ast.Mult):
                return a * b
            if isinstance(node.op, ast.Div):
                if b == 0:
                    fail(WORKED_EXAMPLE_UNINSTANTIATED, f"{where}: division by zero in '{expression}'")
                return a / b
            if isinstance(node.op, ast.Pow):
                return a ** b
            if isinstance(node.op, ast.Mod):
                return a % b
        if isinstance(node, ast.Compare):
            left = walk(node.left)
            for op, comparator in zip(node.ops, node.comparators):
                right = walk(comparator)
                ok = {
                    ast.Lt: left < right, ast.LtE: left <= right, ast.Gt: left > right,
                    ast.GtE: left >= right, ast.Eq: abs(left - right) <= TOLERANCE,
                    ast.NotEq: abs(left - right) > TOLERANCE,
                }[type(op)]
                if not ok:
                    return False
                left = right
            return True
        if isinstance(node, ast.BoolOp):
            values = [walk(v) for v in node.values]
            return all(values) if isinstance(node.op, ast.And) else any(values)
        if isinstance(node, ast.Call):
            return FUNCTIONS[node.func.id](*[walk(a) for a in node.args])
        fail(WORKED_EXAMPLE_UNINSTANTIATED, f"{where}: unsupported expression '{expression}'")

    return walk(tree)


def tidy(value, places=4):
    """Round away float noise without pretending to a precision the data does not have."""
    if isinstance(value, bool):
        return value
    v = round(float(value), places)
    return int(v) if v == int(v) else v


def fmt(value, unit=""):
    v = tidy(value, 2)
    return f"{v} {unit}".strip() if unit else str(v)


# --------------------------------------------------------------- variants


def variant_values(instance, variant_index):
    """Deterministic per-variant given values from the instance's declared value lists.

    The lists are authored data with different lengths per given, so variants differ in
    more than one quantity instead of moving in lockstep.
    """
    values = {}
    for given in instance["givens"]:
        options = given.get("values")
        if options:
            values[given["symbol"]] = options[variant_index % len(options)]
        else:
            values[given["symbol"]] = given["value"]
    return values


def check_constraints(instance, symbols, where):
    for constraint in instance.get("constraints") or []:
        if not evaluate(constraint, symbols, where):
            fail(INSTANCE_VARIANT_VIOLATES_DECLARED_CONSTRAINT,
                 f"{where}: '{constraint}' does not hold for {symbols}")


# ------------------------------------------------------------------ resolve


def resolve_instance(instance, variant_index=0, instance_id=None, stage=None):
    """Resolve one authored instance to real numbers, or fail with a falsifier.

    Returns a resolved instance: the same declared structure with every route output and
    the final answer **computed**, plus the answer-custody objects (answer, quick check,
    independent verification) as three separate things.
    """
    where = instance_id or instance.get("instance_template_id", "instance")
    route = instance.get("reasoning_route") or []
    if not route:
        fail(WORKED_EXAMPLE_UNINSTANTIATED, where + ": no reasoning route")
    if not instance.get("givens"):
        fail(WORKED_EXAMPLE_UNINSTANTIATED, where + ": no givens")
    if not instance.get("unknown"):
        fail(WORKED_EXAMPLE_UNINSTANTIATED, where + ": no unknown")

    symbols = variant_values(instance, variant_index)
    given_symbols = set(symbols)
    check_constraints(instance, symbols, where)

    resolved_givens = []
    for given in instance["givens"]:
        resolved_givens.append({
            "symbol": given["symbol"],
            "quantity": given["quantity"],
            "value": tidy(symbols[given["symbol"]]),
            "unit": given.get("unit", ""),
            "sign_note": given.get("sign_note", ""),
            "stated_in_situation": True,
        })

    states, produced = [], []
    for state in route:
        role = state["role"]
        if role not in ROUTE_ROLES:
            fail(WORKED_EXAMPLE_REASONING_DOES_NOT_TRANSFORM_STATE,
                 f"{where}: unknown route-state role {role}")
        for ref in state.get("input_state_refs") or []:
            if ref not in symbols:
                fail(WORKED_EXAMPLE_REASONING_DOES_NOT_TRANSFORM_STATE,
                     f"{where}:{state['state_id']} reads '{ref}' before anything produced it")
        out = dict(state.get("output_state") or {})
        substitution = None
        if state.get("equation"):
            value = evaluate(state["equation"], symbols, f"{where}:{state['state_id']}")
            substitution = substitute(state["equation"], symbols)
            if out.get("symbol"):
                symbols[out["symbol"]] = value
                produced.append(out["symbol"])
            out["value"] = tidy(value)
        elif out.get("symbol") and "value" not in out:
            # a non-numeric output state (a declared frame, a selected model, a statement)
            out.setdefault("kind", "STATEMENT")
        states.append({
            "state_id": state["state_id"],
            "role": role,
            "canonical_role_refs": ROUTE_ROLE_TO_CANONICAL[role],
            "input_state_refs": list(state.get("input_state_refs") or []),
            "representation_ref": state.get("representation_ref"),
            "equation": state.get("equation"),
            "substitution": substitution,
            "why_valid": state.get("why_valid", ""),
            "output_state": out,
            "learner_text": render_state_text(state, out, substitution),
        })

    if not produced:
        fail(WORKED_EXAMPLE_REASONING_DOES_NOT_TRANSFORM_STATE,
             where + ": no route state produces a new quantity — the route restates the givens")
    if not set(produced) - given_symbols:
        fail(WORKED_EXAMPLE_REASONING_DOES_NOT_TRANSFORM_STATE,
             where + ": the route only recomputes quantities the situation already stated")
    if not any(s["role"] in COMPUTATIONAL_ROLES and s["equation"] for s in states):
        fail(WORKED_EXAMPLE_REASONING_DOES_NOT_TRANSFORM_STATE,
             where + ": no EXECUTE state carries a relation to substitute into")

    answer = resolve_final_answer(instance, symbols, where)
    quick_check = resolve_quick_check(instance, symbols, where)
    verification = resolve_verification(instance, symbols, states, answer, where)

    situation = fill_template(instance["situation"], instance, symbols)
    prompt = fill_template(instance["question"], instance, symbols)
    return {
        "instance_id": instance_id or f"{instance['instance_template_id']}-V{variant_index}",
        "instance_template_ref": instance["instance_template_id"],
        "problem_family_ref": instance["problem_family_ref"],
        "topic_ref": instance.get("topic_ref"),
        "support_stage": stage,
        "variant_index": variant_index,
        "situation": situation,
        "question": prompt,
        "frame": dict(instance["frame"]),
        "givens": resolved_givens,
        "unknown": dict(instance["unknown"]),
        "representation_refs": sorted({s["representation_ref"] for s in states if s["representation_ref"]}),
        "reasoning_route": states,
        "final_answer": answer,
        "quick_check": quick_check,
        "independent_verification": verification,
        "instantiated": True,
    }


def substitute(equation, symbols):
    """Show the relation with the numbers put in, which is what a learner needs to see."""
    def repl(m):
        name = m.group(0)
        if name in symbols:
            return str(tidy(symbols[name]))
        return name

    return re.sub(r"[A-Za-z_][A-Za-z0-9_]*", repl, str(equation))


def render_state_text(state, out, substitution):
    parts = []
    if state.get("why_valid"):
        parts.append(state["why_valid"])
    if state.get("equation"):
        line = f"{out.get('symbol', 'result')} = {state['equation']}"
        if substitution:
            line += f" = {substitution} = {fmt(out.get('value'), out.get('unit', ''))}"
        parts.append(line)
    elif out.get("statement"):
        parts.append(out["statement"])
    return " ".join(p for p in parts if p)


def fill_template(text, instance, symbols):
    """Substitute {symbol} placeholders with the variant's own values and units."""
    units = {g["symbol"]: g.get("unit", "") for g in instance["givens"]}

    def repl(m):
        name = m.group(1)
        if name not in symbols:
            fail(WORKED_EXAMPLE_UNINSTANTIATED, f"situation references unknown symbol {name}")
        return fmt(symbols[name], units.get(name, ""))

    return re.sub(r"\{([A-Za-z_][A-Za-z0-9_]*)\}", repl, str(text or ""))


def resolve_final_answer(instance, symbols, where):
    declared = instance.get("final_answer")
    if not declared:
        fail(WORKED_EXAMPLE_FINAL_ANSWER_MISSING, where)
    symbol = declared.get("symbol")
    if not symbol:
        fail(WORKED_EXAMPLE_FINAL_ANSWER_MISSING, where + ": no answer symbol")
    if symbol not in symbols:
        fail(WORKED_EXAMPLE_FINAL_ANSWER_MISSING,
             f"{where}: the route never produces the answer symbol '{symbol}'")
    value = tidy(symbols[symbol])
    components = []
    for comp in declared.get("components") or []:
        if comp["symbol"] not in symbols:
            fail(WORKED_EXAMPLE_FINAL_ANSWER_MISSING,
                 f"{where}: answer component '{comp['symbol']}' was never computed")
        components.append({
            "symbol": comp["symbol"],
            "quantity": comp.get("quantity", ""),
            "value": tidy(symbols[comp["symbol"]]),
            "unit": comp.get("unit", ""),
        })
    # Computed quantities carry their own units, which the givens table does not know,
    # so they are substituted before the givens are filled in.
    statement = str(declared.get("statement", ""))
    statement = statement.replace("{answer}", fmt(value, declared.get("unit", "")))
    for comp in components:
        statement = statement.replace("{" + comp["symbol"] + "}", fmt(comp["value"], comp["unit"]))
    statement = fill_template(statement, instance, symbols)
    return {
        "answer_id": f"{where}-ANSWER",
        "symbol": symbol,
        "value": value,
        "unit": declared.get("unit", ""),
        "components": components,
        "statement": statement or f"{symbol} = {fmt(value, declared.get('unit', ''))}",
        "is_resolved_result": True,
    }


def resolve_quick_check(instance, symbols, where):
    """One defining property, sign or unit. Never a substitute for the answer."""
    declared = instance.get("quick_check")
    if not declared:
        fail(LEARNER_QUESTION_WITHOUT_ANSWER, where + ": no quick check")
    holds = None
    if declared.get("property_expression"):
        holds = bool(evaluate(declared["property_expression"], symbols,
                              f"{where}:quick_check"))
        if not holds:
            fail(INSTANCE_VARIANT_VIOLATES_DECLARED_CONSTRAINT,
                 f"{where}: the declared quick check does not hold for this variant")
    return {
        "quick_check_id": f"{where}-QUICK-CHECK",
        "check_kind": declared.get("check_kind", "PROPERTY"),
        "prompt": fill_template(declared["prompt"], instance, symbols),
        "property_expression": declared.get("property_expression"),
        "property_holds": holds,
        "is_answer": False,
    }


def resolve_verification(instance, symbols, states, answer, where):
    """A genuinely distinct route to the same number, run as real arithmetic."""
    declared = instance.get("independent_verification")
    if not declared:
        fail(LEARNER_QUESTION_WITHOUT_ANSWER, where + ": no independent verification")
    equation = declared["equation"]
    solving_equations = {str(s["equation"]).replace(" ", "")
                         for s in states if s.get("equation")}
    if str(equation).replace(" ", "") in solving_equations:
        fail(VERIFICATION_ROUTE_NOT_INDEPENDENT,
             f"{where}: the verification repeats a solving-route relation")
    value = evaluate(equation, symbols, f"{where}:verification")
    mode = declared.get("compare_to", "FINAL_ANSWER")
    if mode == "FINAL_ANSWER":
        # compare against the full-precision route value, not the rounded display value
        expected = symbols[answer["symbol"]]
        expected_text = f"the answer, {fmt(expected, answer['unit'])}"
    else:
        expected = evaluate(declared["expected_equation"], symbols, f"{where}:verification-expected")
        expected_text = f"{declared['expected_equation']} = {fmt(expected)}"
    if abs(float(value) - float(expected)) > max(TOLERANCE, abs(float(expected)) * 1e-9):
        fail(VERIFICATION_ROUTE_NOT_INDEPENDENT,
             f"{where}: the second route gives {tidy(value)}, the first gives {tidy(expected)}")
    return {
        "verification_id": f"{where}-INDEPENDENT-VERIFICATION",
        "route_description": fill_template(declared["route_description"], instance, symbols),
        "equation": equation,
        "substitution": substitute(equation, symbols),
        "value": tidy(value),
        "compare_to": mode,
        "expected_equation": declared.get("expected_equation"),
        "agrees_with_answer": True,
        "agreement_text": f"This second route gives {fmt(value, answer['unit'] if mode == 'FINAL_ANSWER' else '')}, "
                          f"which matches {expected_text}.",
        "is_distinct_from_solving_route": True,
        "is_answer": False,
    }


# ------------------------------------------------------- answer-custody checks


def assert_answer_custody(question_object, where=""):
    """Every learner-facing question resolves to an explicit answer artifact.

    A hint, a self-check or a "check your reasoning" prompt is not an answer, and this is
    where that distinction is enforced rather than assumed.
    """
    answer = (question_object or {}).get("final_answer")
    if not answer or answer.get("value") is None or not answer.get("is_resolved_result"):
        fail(LEARNER_QUESTION_WITHOUT_ANSWER, where or "question")
    for key in ("quick_check", "independent_verification"):
        obj = question_object.get(key)
        if obj and obj.get("is_answer"):
            fail(SELF_CHECK_SUBSTITUTED_FOR_ANSWER, f"{where}:{key}")
    qc = question_object.get("quick_check") or {}
    iv = question_object.get("independent_verification") or {}
    if qc and iv and qc.get("prompt") and qc["prompt"] == iv.get("route_description"):
        fail(SELF_CHECK_SUBSTITUTED_FOR_ANSWER, f"{where}: quick check and verification collapsed")
    return True


def registry_index(registry):
    return {row["problem_family_ref"]: row for row in registry["instances"]}


def instance_for_family(registry, family_ref):
    return registry_index(registry).get(family_ref)
