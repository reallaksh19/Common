#!/usr/bin/env python3
"""Local v1.1 timer accounting state.

Accounting is mandatory Local state. A watchdog is a separate capability and must
never be fabricated merely because accounting is armed.
"""
from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from typing import Any

DEFAULT_BUDGETS = {"CODER": 15, "REVIEWER": 15, "COORDINATOR": 45, "PARENT_CHECK": 45}
ROLES = set(DEFAULT_BUDGETS)


class TimerError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise TimerError(message)


def instant(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    require(parsed.tzinfo is not None, "Timer timestamp requires timezone")
    return parsed.astimezone(timezone.utc)


def arm(role: str, *, started_at: str, budget_minutes: int | None = None, watchdog_available: bool = False, override_ref: str | None = None) -> dict[str, Any]:
    role = str(role).upper()
    require(role in ROLES, "Unknown timer role")
    budget = DEFAULT_BUDGETS[role] if budget_minutes is None else int(budget_minutes)
    require(budget > 0, "Timer budget must be positive")
    if budget != DEFAULT_BUDGETS[role]:
        require(bool(override_ref), "Non-default timer budget requires Owner override reference")
    instant(started_at)
    return {
        "schema": "local-stage-timer/v1",
        "role": role,
        "budget_minutes": budget,
        "accounting": "ARMED",
        "watchdog": "ACTIVE" if watchdog_available else "NOT_AVAILABLE",
        "started_at": started_at,
        "paused_at": None,
        "total_paused_seconds": 0,
        "stopped_at": None,
        "override_ref": override_ref,
    }


def pause(state: dict[str, Any], *, at: str) -> dict[str, Any]:
    s = deepcopy(state)
    require(s.get("accounting") == "ARMED" and s.get("stopped_at") is None, "Only active accounting can pause")
    require(s.get("paused_at") is None, "Timer is already paused")
    require(instant(at) >= instant(s["started_at"]), "Pause precedes timer start")
    s["paused_at"] = at
    return s


def resume(state: dict[str, Any], *, at: str) -> dict[str, Any]:
    s = deepcopy(state)
    require(s.get("paused_at") is not None, "Timer is not paused")
    pause_at = instant(s["paused_at"])
    resume_at = instant(at)
    require(resume_at >= pause_at, "Resume precedes pause")
    s["total_paused_seconds"] += int((resume_at - pause_at).total_seconds())
    s["paused_at"] = None
    return s


def stop(state: dict[str, Any], *, at: str) -> dict[str, Any]:
    s = deepcopy(state)
    require(s.get("stopped_at") is None, "Timer is already stopped")
    if s.get("paused_at") is not None:
        s = resume(s, at=at)
    require(instant(at) >= instant(s["started_at"]), "Stop precedes start")
    s["stopped_at"] = at
    s["accounting"] = "STOPPED"
    return s


def status(state: dict[str, Any], *, at: str) -> dict[str, Any]:
    now = instant(at)
    started = instant(state["started_at"])
    end = instant(state["stopped_at"]) if state.get("stopped_at") else now
    require(end >= started, "Timer observation precedes start")
    paused = int(state.get("total_paused_seconds", 0))
    if state.get("paused_at") is not None:
        pause_at = instant(state["paused_at"])
        require(end >= pause_at, "Timer observation precedes pause")
        paused += int((end - pause_at).total_seconds())
    active_seconds = max(0, int((end - started).total_seconds()) - paused)
    budget_seconds = int(state["budget_minutes"]) * 60
    return {
        "accounting": state["accounting"],
        "watchdog": state["watchdog"],
        "active_seconds": active_seconds,
        "budget_seconds": budget_seconds,
        "budget_exhausted": active_seconds >= budget_seconds,
        "paused": state.get("paused_at") is not None,
    }
