# Constrained Rating Image Spacing

Status: Completed

## Problem

When `minImageSize.width` exceeded the width available to each rating slot, layout allowed every image to grow beyond its slot and compensated with negative spacing. Adjacent rating frames could overlap even though each frame remained finite and inside the control bounds.

## Change

Use the per-rating slot width as the maximum image width during constrained layout. Keep `minImageSize` in intrinsic content sizing, where Auto Layout can request the preferred unconstrained size.

## Verification Completed

- Added XCTest coverage requiring ordered, non-overlapping empty-image frames under an oversized minimum width.
- Added a dependency-free baseline contract for the slot-width cap and test intent.
- Passed the static baseline, Python compilation, shell syntax, and both podspec syntax checks.
- Local Xcode/simulator execution was unavailable; hosted macOS Xcode tests remain required before merge.
