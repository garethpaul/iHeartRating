# iHeartRating Bounce Without Delegate

status: completed

## Context

`HeartRatingView.shouldBounce` is a view behavior, but the bounce animation was
nested inside the delegate callback branch in `touchesEnded`. A rating view
without a delegate could update visually during touches but would not run the
configured bounce animation.

## Objectives

- Preserve the delegate `didUpdate` callback.
- Run the bounce animation whenever `shouldBounce` is enabled, even when no
  delegate is attached.
- Keep the existing clamped image index guard for bounce animation.
- Extend the static baseline so bounce stays independent from delegate
  callbacks.

## Verification

- `make check`
- `python3 scripts/check-baseline.py`
- `git diff --check`
