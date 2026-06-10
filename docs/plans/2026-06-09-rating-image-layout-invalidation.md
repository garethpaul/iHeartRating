# Rating Image Layout Invalidation

status: completed

## Context

`HeartRatingView` lets consumers change `emptyImage` and `fullImage` at runtime.
Those setters updated existing image views and refreshed masks, but they did
not request layout. If replacement images had different dimensions, refreshed
partial-rating masks could run against stale frames until another layout pass.

## Completed Scope

- Requested layout when `emptyImage` changes before refreshing masks.
- Requested layout when `fullImage` changes before refreshing masks.
- Extended the static baseline so image setter layout invalidation remains
  covered without requiring local Xcode.
- Updated README, VISION, SECURITY, and CHANGES with the new guardrail.

## Verification

- `python3 scripts/check-baseline.py`
- `make lint`
- `make test`
- `make build`
- `make check`
- `git diff --check`
