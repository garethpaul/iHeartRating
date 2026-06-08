# Rating Bounds Plan

status: completed

## Context

`HeartRatingView` already clamps `maxRating` to a supported lower bound and guards layout/touch crashes, but direct public assignments can still leave `rating` outside the configured `minRating...maxRating` range. `minRating` can also be configured above `maxRating`, which makes delegate values and visual state harder to reason about.

## Objectives

- Normalize direct `rating` assignments to the configured rating range.
- Keep `minRating` non-negative and no greater than `maxRating`.
- Reuse the same bounds helper for touch-driven rating updates.
- Extend the static baseline so these guardrails remain visible without Xcode.

## Verification

- `make check`
- `python3 scripts/check-baseline.py`
- `git diff --check`
