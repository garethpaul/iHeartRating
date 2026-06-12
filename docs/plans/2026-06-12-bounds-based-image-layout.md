# Bounds-Based Rating Image Layout

status: planned

## Context

`layoutSubviews()` calculates child image sizes and spacing from the rating
view's `frame`. A view's frame is expressed in its superview's coordinate space
and changes when transforms are applied, while subview layout belongs in the
view's local `bounds` coordinate space. Scaled or rotated rating views can
therefore lay out hearts using transformed dimensions and produce oversized or
misaligned content.

## Scope

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
