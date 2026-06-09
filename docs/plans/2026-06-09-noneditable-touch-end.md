# iHeartRating Non-Editable Touch End Guard

status: completed

## Context

`HeartRatingView.handleTouchAtLocation` already ignores touches when
`editable` is false, but `touchesEnded` still notified the delegate and ran the
bounce path. Disabled controls should not emit completed-rating callbacks or
touch animations.

## Objectives

- Return early from `touchesEnded` when `editable` is false.
- Preserve delegate callbacks and bounce behavior for editable controls.
- Add focused XCTest coverage for the non-editable completion path.
- Extend `scripts/check-baseline.py` so the guard remains visible without
  Xcode locally.

## Verification

- `make check`
- `python3 scripts/check-baseline.py`
- `git diff --check`
