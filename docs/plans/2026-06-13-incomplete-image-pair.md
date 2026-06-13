# Incomplete Rating Image Pair

status: planned

## Context

`HeartRatingView` overlays full images on empty images. When `emptyImage` is
cleared after layout, its image views become empty but `refresh()` can leave the
previous full overlays visible according to the current rating.

The control can therefore display a rating without its configured empty-image
baseline, even though layout depends on that image pair.

## Priority

Image configuration is public and mutable. An incomplete pair should render no
filled rating rather than stale or misleading overlays, without changing the
stored rating or rebuilding image views.

## Requirements

- R1. `refresh()` must hide every full image view when either `emptyImage` or
  `fullImage` is nil.
- R2. Hidden full image views must have stale masks removed.
- R3. Completing the image pair must restore normal whole, half, and floating
  rating rendering through the existing refresh path.
- R4. Rating values, image-view counts, layout math, bounce behavior, and
  delegate callbacks must remain unchanged.
- R5. Add XCTest coverage for clearing and restoring the image pair plus a
  static early-return contract.

## Implementation Units

### U1. Fail closed for incomplete images

- **Files:** `iHeartRating/iHeartRatingView.swift`
- Add an early refresh boundary that clears masks, hides full overlays, and
  returns before rating-based visibility logic.

### U2. Extend regression coverage

- **Files:** `iHeartRatingTests/iHeartRatingTests.swift`,
  `scripts/check-baseline.py`
- Prove overlay hiding after image removal and restoration after reconfiguration.

### U3. Document the rendering boundary

- **Files:** `README.md`, `SECURITY.md`, `VISION.md`, `CHANGES.md`
- Record deterministic rendering for incomplete image configuration.

## Scope Boundaries

- Do not change the public rating API, image layout, touch math, or animation.
- Do not modernize Swift, Xcode, deployment targets, podspec versions, or the
  example app.
- Do not claim local simulator execution when Xcode is unavailable.

## Verification

- `make lint`
- `make test`
- `make build`
- `make check`
- `python3 -m py_compile scripts/check-baseline.py`
- `sh -n build.sh`
- `ruby -c iHeartRating.podspec`
- `ruby -c iHeartRating/0.1.6/iHeartRating.podspec`
- `git diff --check`
- Hostile mutations removing the nil guard, mask cleanup, early return,
  regression test, plan status, or verification evidence must be rejected.
