# Infinite Minimum Image Size Normalization

status: completed

## Context

`minImageSize` normalizes negative and NaN dimensions, but positive infinity
still survives the property observer. Layout then selects an infinite maximum
dimension and can assign non-finite frames to the empty and full rating image
views.

## Requirements

- R1. Normalize positive and negative infinite width or height values to zero.
- R2. Normalize each dimension independently so a valid companion dimension is
  preserved.
- R3. Preserve existing NaN and negative-dimension normalization.
- R4. Keep compatibility with the repository's Swift 2-era public API and
  legacy Xcode project.
- R5. Add XCTest intent and mutation-sensitive static coverage without changing
  project files, assets, podspecs, or hosted workflow policy.

## Scope Boundaries

- Do not change rating bounds, touch behavior, image-pair visibility, bounce
  animation, or layout spacing.
- Do not modernize Swift syntax or project settings in this compatibility fix.
- Local Linux validation must remain truthful about unavailable `xcodebuild`.

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
- Hostile mutations must reject loss of width or height infinity guards,
  companion-dimension preservation, stale plan status, and missing verification
  evidence.

## Work Completed

- Normalized positive and negative infinite width and height values
  independently to zero in the `minImageSize` setter.
- Preserved valid companion dimensions and the existing NaN and negative-value
  behavior.
- Added XCTest intent for infinite width and height assignments.
- Extended static contracts and configuration documentation without changing
  project, podspec, asset, or workflow files.

## Verification Completed

- All four Make gates passed locally and reported that `xcodebuild` was
  unavailable, so only the static iOS baseline ran on this host.
- `python3 -m py_compile scripts/check-baseline.py`, `sh -n build.sh`,
  `ruby -c iHeartRating.podspec`,
  `ruby -c iHeartRating/0.1.6/iHeartRating.podspec`, and `git diff --check`
  passed.
- Five isolated hostile mutations were rejected: removed width infinity guard,
  removed height infinity guard, lost companion-dimension preservation, stale
  plan status, and missing verification evidence.
- Exact-base comparison confirmed Xcode projects, podspecs, assets, and hosted
  workflow configuration remained unchanged.
- Intended-file generated-artifact and secret-pattern scans passed.
- Hosted macOS project parsing and CodeQL evidence is recorded separately after
  push; this plan claims only the completed local static verification.
