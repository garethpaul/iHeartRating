---
title: "fix: Expose image content mode to library consumers"
type: fix
date: 2026-06-17
status: completed
---

# fix: Expose image content mode to library consumers

## Summary

Make `HeartRatingView.imageContentMode` part of the public library API so
applications importing iHeartRating can configure the rendering mode that the
view already propagates to every empty and full rating image.

## Problem Frame

The property is documented as configurable and its observer correctly updates
existing child views, but its declaration has internal access. The current
XCTest target uses `@testable import`, so its propagation test passes even
though an external CocoaPods or framework consumer cannot assign the property.

## Requirements

- R1. `imageContentMode` must be publicly readable and writable from an
  importing application.
- R2. The default must remain `ScaleAspectFit`.
- R3. Assignments must continue updating every existing empty and full image
  view and requesting layout.
- R4. The property must not become `@IBInspectable`; the legacy Interface
  Builder inspection surface does not support arbitrary enum properties.
- R5. Maintained checks and documentation must reject a regression to internal
  access, removal of propagation, stale plan status, or missing verification.

## Implementation Units

### U1. Correct the library access boundary

- **Files:** `iHeartRating/iHeartRatingView.swift`.
- **Approach:** Add public access to the existing property declaration without
  changing its type, default, observer, layout invalidation, or child-view
  initialization behavior.
- **Verification:** Source inspection confirms the public declaration and the
  existing propagation test remains intact.

### U2. Protect the consumer contract

- **Files:** `scripts/check-baseline.py`, `README.md`, `VISION.md`,
  `SECURITY.md`, `CHANGES.md`, `AGENTS.md`, this plan.
- **Approach:** Add an exact public-surface contract and synchronized guidance
  that distinguishes external configurability from internal `@testable`
  coverage.
- **Verification:** Root and external-directory Make gates pass; isolated
  mutations removing public access, propagation, guidance, plan status, or
  plan evidence fail for their intended reason.

## Scope Boundaries

- Do not rename the property or change its `UIViewContentMode` type.
- Do not change rating, touch, mask, animation, or layout behavior.
- Do not modernize the Swift 2 syntax, deployment target, pod version, or
  archival Xcode projects in this change.

## Risks

- This expands the source-compatible public API but does not change binary or
  persisted-data formats.
- Linux cannot compile the UIKit module; static public-surface contracts and
  hosted Xcode project parsing remain the available verification boundary.

## Related Work

- `docs/plans/2026-06-14-image-content-mode-propagation.md` established the
  observer behavior this change exposes to consumers.

## Work Completed

- Made the existing `imageContentMode` property publicly readable and writable
  without changing its type, default, observer, or child-view behavior.
- Added a maintained source contract that distinguishes public API access from
  the legacy XCTest target's `@testable` visibility.
- Synchronized consumer and maintainer guidance without expanding the
  Interface Builder, deployment, or package-version surface.

## Verification Completed

- All four Make gates passed: `make lint`, `make test`, `make build`, and
  `make check`.
- The external-directory absolute Makefile check passed from `/tmp`.
- `xcodebuild` was unavailable locally, so the maintained static source,
  project, plist, workflow, podspec, documentation, and plan contracts ran.
- `python3 -m py_compile scripts/check-baseline.py`, `sh -n build.sh`, both
  podspec syntax checks, and `git diff --check` passed.
- Seven isolated hostile mutations were rejected for public access, the
  default mode, Interface Builder exposure, observer propagation, guidance,
  plan status, and plan evidence.
