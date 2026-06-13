# Normalize NaN Minimum Image Sizes

status: completed

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

- Normalized NaN width and height values independently to zero in the
  `minImageSize` setter.
- Preserved each valid companion dimension and the existing negative-value
  clamp.
- Added hosted XCTest cases for NaN width and NaN height assignments.
- Extended static contracts and configuration documentation without changing
  rating, touch, project, podspec, or workflow behavior.

## Verification Completed

- All four Make gates passed locally and reported that `xcodebuild` was
  unavailable, so only the static iOS baseline ran on this host.
- `python3 -m py_compile scripts/check-baseline.py`, `sh -n build.sh`,
  `ruby -c iHeartRating.podspec`, and `git diff --check` passed.
- Five isolated hostile mutations were rejected: removed width normalization,
  removed height normalization, removed XCTest coverage, stale plan status, and
  missing verification evidence.
- Exact-base comparison confirmed Xcode projects, podspecs, assets, and hosted
  workflow configuration remained unchanged.
- Intended-file generated-artifact and secret-pattern scans passed.
- Hosted macOS XCTest and CodeQL evidence is recorded separately after push;
  this plan claims only the completed local static verification.
