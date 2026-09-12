#!/usr/bin/env python3
"""Governed learner-facing copy vocabulary for the Physics learner products.

Internal role and state identifiers (``MISCONCEPTION_REPAIR``, ``WORKED``, ``GUIDED``,
``EXECUTE``, ``H1_NOTICE`` …) are the schema and falsifier vocabulary and are **not**
renamed by this module. What this module owns is the single translation point between
that vocabulary and the words a Grade-9 learner actually reads on the page.

Two jobs:

``learner_title(role)``
    the warm, plain-English heading that replaces the internal role on the page;

``learner_copy_violations(text)``
    the falsifier surface. If a raw internal identifier, or a clinical
    curriculum-design label such as "Misconception Repair" or "Readiness Gate",
    survives to rendered learner text, this returns it and the caller raises
    ``INTERNAL_ROLE_LABEL_ON_LEARNER_SURFACE``.

Both Core (1A) and the Core (2) transfer book import this module, so the vocabulary
cannot drift into two per-renderer dialects.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

REGISTRY_PATH = Path(__file__).resolve().parents[1] / "registry" / "physics-learner-copy-titles.json"

FALSIFIER = "INTERNAL_ROLE_LABEL_ON_LEARNER_SURFACE"

_CACHE = {}


def load_registry(path=None):
    key = str(path or REGISTRY_PATH)
    if key not in _CACHE:
        _CACHE[key] = json.loads(Path(key).read_text(encoding="utf-8"))
    return _CACHE[key]


def _normalise(role):
    s = str(role or "").strip()
    for prefix in ("PHY-ROLE-", "OBLIGATION_LEVEL:", "OBLIGATION_REP:", "REQUIRED:", "PROBE:"):
        if s.startswith(prefix):
            s = s[len(prefix):]
    return re.sub(r"[\s\-]+", "_", s).upper()


def humanize_role(role):
    """Last-resort wording for a role with no registry entry: plain, never SCREAMING_SNAKE."""
    s = _normalise(role).replace("_", " ").strip().lower()
    return s[:1].upper() + s[1:] if s else ""


def learner_title(role, registry=None, default=None):
    """The learner-facing heading for an internal role identifier."""
    reg = registry or load_registry()
    entry = reg["titles"].get(_normalise(role))
    if entry:
        return entry["learner_title"]
    if default is not None:
        return default
    return humanize_role(role)


def learner_subtitle(role, registry=None, default=""):
    reg = registry or load_registry()
    entry = reg["titles"].get(_normalise(role))
    return entry["learner_subtitle"] if entry else default


def is_mapped(role, registry=None):
    reg = registry or load_registry()
    return _normalise(role) in reg["titles"]


def unmapped_roles(roles, registry=None):
    reg = registry or load_registry()
    return sorted({_normalise(r) for r in roles if _normalise(r) and _normalise(r) not in reg["titles"]})


def apply_phrase_rewrites(text, registry=None):
    reg = registry or load_registry()
    s = str(text or "")
    for old, new in reg["phrase_rewrites"]:
        s = s.replace(old, new)
    return s


def _identifier_patterns(registry):
    key = id(registry)
    cached = _CACHE.get(("idpat", key))
    if cached is None:
        cached = [
            (ident, re.compile(r"(?<![A-Za-z0-9])" + re.escape(ident) + r"(?![A-Za-z0-9])"))
            for ident in registry["internal_role_identifiers"]
        ]
        _CACHE[("idpat", key)] = cached
    return cached


def _phrase_patterns(registry):
    key = id(registry)
    cached = _CACHE.get(("phrasepat", key))
    if cached is None:
        cached = [
            (phrase, re.compile(r"\b" + r"[\s\-]+".join(re.escape(w) for w in phrase.split()) + r"\b", re.I))
            for phrase in registry["clinical_label_phrases"]
        ]
        _CACHE[("phrasepat", key)] = cached
    return cached


def learner_copy_violations(text, registry=None):
    """Every internal role identifier or clinical label still present in learner text.

    An empty list is the only acceptable result for rendered learner-product text.
    """
    reg = registry or load_registry()
    s = str(text or "")
    found = set()
    for ident, pattern in _identifier_patterns(reg):
        if pattern.search(s):
            found.add(ident)
    for phrase, pattern in _phrase_patterns(reg):
        if pattern.search(s):
            found.add(phrase)
    return sorted(found)


def assert_learner_copy(text, where="", registry=None):
    bad = learner_copy_violations(text, registry)
    if bad:
        raise ValueError(f"{FALSIFIER}: {where}: {', '.join(bad[:5])}")
    return True


if __name__ == "__main__":  # pragma: no cover - manual inspection aid
    reg = load_registry()
    for role in sorted(reg["titles"]):
        print(f"{role:28s} -> {reg['titles'][role]['learner_title']}")
