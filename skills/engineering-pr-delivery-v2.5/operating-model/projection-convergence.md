# Projection convergence and relay readiness

Repository roadmap/state remains authoritative. GitHub Issues or other human coordination surfaces are projections, but custody transfer is not fully handover-ready until required projections are synchronized.

`REPO_STATE.projection` records whether publication is required and whether it is `IN_SYNC`, `PENDING`, `STALE`, or `NOT_REQUIRED`. An in-sync projection binds to the current roadmap revision and current execution reference (serial EP, parallel plan, or `NONE`).

`REPO_STATE.relay_readiness` separates:
- `repository_ready`: a replacement agent can recover authoritative repository state without chat;
- `projection_ready`: every required external coordination projection is synchronized;
- `handover_ready`: both predicates are true.

Projection lag does not rewrite engineering truth and does not automatically create an engineering hard stop. It prevents declaring complete custody transfer until reconciled. Release qualification is separate from relay handover readiness.
