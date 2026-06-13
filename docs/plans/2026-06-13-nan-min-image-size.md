# Normalize NaN Minimum Image Sizes

status: planned

## Context

`minImageSize` clamps negative dimensions to zero, but comparisons with NaN are
false. A NaN width or height therefore survives configuration and can propagate
through layout `max(...)`, aspect sizing, and child image frames.

## Requirements

- R1. A NaN minimum-image width must normalize to zero.
- R2. A NaN minimum-image height must normalize to zero.
- R3. Each valid companion dimension must be preserved when the other dimension
  is NaN.
- R4. Existing negative-dimension clamping and ordinary positive sizing must
  remain unchanged.
- R5. Hosted XCTest and the deterministic checker must reject missing or
  one-sided NaN handling.

## Scope Boundaries

- Do not change rating, touch, bounce, image-pair, or layout coordinate behavior.
- Do not edit CocoaPods metadata, Xcode project settings, assets, or workflow
  configuration.

## Verification

- `make lint`
- `make test`
- `make build`
- `make check`
- `python3 -m py_compile scripts/check-baseline.py`
- `sh -n build.sh`
- `ruby -c iHeartRating.podspec`
- `git diff --check`
- Hostile mutations must reject removed width or height normalization, removed
  XCTest coverage, stale plan status, and missing verification evidence.

## Work Completed

Pending implementation.

## Verification Completed

Pending implementation and verification.
