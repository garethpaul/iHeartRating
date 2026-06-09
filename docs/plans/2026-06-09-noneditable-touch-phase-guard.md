# Non-Editable Touch Phase Guard

status: completed

## Context

`touchesEnded` already ignored events while the rating view was not editable,
but `touchesBegan` and `touchesMoved` relied on `handleTouchAtLocation` to
short-circuit after a touch location was read. The public touch-phase overrides
should all make the disabled-control boundary explicit before delegate work can
happen.

## Completed Scope

- Added non-editable guards to `touchesBegan` and `touchesMoved`.
- Kept the existing lower-level `handleTouchAtLocation` editable guard.
- Extended the static baseline to preserve began/moved/ended touch guards.
- Updated README, VISION, and CHANGES to document the non-editable touch-phase
  guardrail.

## Verification

- `make check`
- `git diff --check`
