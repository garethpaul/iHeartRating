# Bounds-Based Rating Image Layout

status: completed

## Context

`layoutSubviews()` calculates child image sizes and spacing from the rating
view's `frame`. A view's frame is expressed in its superview's coordinate space
and changes when transforms are applied, while subview layout belongs in the
view's local `bounds` coordinate space. Scaled or rotated rating views can
therefore lay out hearts using transformed dimensions and produce oversized or
misaligned content.

## Completed Scope

- Calculate image width, height, spacing, and origin from `bounds`.
- Preserve existing minimum image size and single-image safeguards.
- Add XCTest coverage for a scaled rating view whose frame and bounds differ.
- Extend the dependency-free baseline so frame-based layout regressions fail
  even when a compatible Swift 2 toolchain is unavailable.
- Document the local-coordinate layout invariant.

## Verification

- `make check`
- `bash -n build.sh`
- `git diff --check`
- A mutation that restores `frame`-based image sizing must fail the baseline.
- Hosted macOS validation must parse both Xcode projects.

## Work Completed

- Changed child image sizing, spacing, and origin calculations to use the
  rating view's local `bounds` coordinate space.
- Preserved minimum image sizing, the single-image path, parser behavior,
  touch handling, and package metadata.
- Added transformed-view XCTest coverage and a dependency-free static contract
  rejecting frame-based layout regressions.

## Verification Completed

- All four Make gates, checker compilation, `bash -n build.sh`, and
  `git diff --check` passed locally; Xcode project parsing was truthfully
  skipped because Xcode is unavailable in the local environment.
- Implementation push run `27394309114` and pull-request run `27394315070`
  passed at commit `542646ef0f910afe803638be316194d4995654b7`; the hosted macOS
  gate parsed both Xcode projects and ran the rating baseline.
- Post-merge push run `27394330649` and CodeQL setup run `27402322718` passed
  at default-branch merge commit `7077f27aeed5950d99fc4944ac436d007136f193`.
- A mutation restoring `frame`-based image sizing was rejected by the
  baseline.
