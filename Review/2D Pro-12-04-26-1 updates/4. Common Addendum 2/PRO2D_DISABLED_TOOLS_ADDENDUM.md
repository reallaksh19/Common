# Pro 2D disabled-tools addendum

This addendum is intentionally narrow.

It covers only the three icons that should remain blocked for now:
- `Measure`
- `Bend`
- `Tee`

## Decision

These tools should stay **visible but blocked**.

They should **not** be hidden, and they should **not** silently no-op.

That is the correct product behavior because:
- users can see the intended professional roadmap,
- the UI stays honest about what is not ready,
- accidental activation does not put the canvas into a fake or partial mode.

## What was weak before

In the current bundle, the disabled state is visually correct, but operationally weak:
- native `disabled` buttons prevent activation, but they also prevent a useful explanation workflow,
- there is no structured reason/checklist attached to the blocked tools,
- the app does not surface what is missing before these tools can be enabled.

## What this addendum changes

### 1) Tool metadata becomes explicit

`Pro2D_ToolRegistry.mjs`
- keeps `implemented: false` for `measure`, `bend`, `tee`
- adds `status: 'planned'`
- adds a short blocked reason
- adds an `enableCriteria` checklist for each blocked tool
- exports `Pro2D_blockedToolIds`
- exports `Pro2D_getBlockedToolMessage()`

### 2) Disabled tools become explainable instead of dead

`Pro2D_LeftRail.tsx`
- blocked tools remain non-activating
- clicking them now calls `onBlockedTool()` instead of doing nothing
- the tile shows a `Planned` badge
- `aria-disabled` is used instead of hard `disabled`, so the explanation flow still works

`Pro2D_Ribbon.tsx`
- same behavior for ribbon actions
- blocked tools show a `Planned` badge
- clicking them calls `onBlockedAction()`

### 3) The shell shows the reason and the enable gate

`Pro2D_AppShell.tsx`
- records blocked-tool attempts in the log
- shows a dismissible banner:
  - why the tool is still blocked
  - what must exist before it can be enabled

This keeps the UI professional:
- not hidden
- not fake
- not silent

## Why each tool stays blocked

### Measure

Keep blocked until all of these exist:
- two-point and chained measurement commands
- persistent dimension entities in canonical doc
- snapped references that survive reload/export
- report/export from measure state

Without that, Measure would be decorative, not professional.

### Bend

Keep blocked until all of these exist:
- topology-aware elbow insertion
- spec/radius lookup by pipe size/schedule
- upstream/downstream split with quantity preservation
- canonical bend persistence and export

Without that, Bend risks corrupting topology and quantities.

### Tee

Keep blocked until all of these exist:
- branch intersection detection
- main-run vs branch-run ownership model
- segment splitting at the branch node
- canonical tee/olet persistence and export

Without that, Tee risks invalid connectivity and wrong route semantics.

## Why this is better than simply hiding them

Hiding them would reduce honesty.

Leaving them as inert disabled buttons is also weak because it gives no path forward.

The right compromise is:
- **visible**
- **blocked**
- **explainable**
- **testable**

## Included smoke test

`tests/pro2d_disabled_tools_smoke.mjs`

Checks that:
- `measure`, `bend`, `tee` remain blocked
- all three have enable criteria
- all three produce a readable blocked message

## Files in this ZIP

- `PRO2D_DISABLED_TOOLS_ADDENDUM.md`
- `js/pro2dcanvas/Pro2D_ToolRegistry.mjs`
- `js/pro2dcanvas/Pro2D_LeftRail.tsx`
- `js/pro2dcanvas/Pro2D_Ribbon.tsx`
- `js/pro2dcanvas/Pro2D_AppShell.tsx`
- `js/smart2dcanvas/Smart2Dcanvas_StatusBar.tsx`
- `tests/pro2d_disabled_tools_smoke.mjs`
