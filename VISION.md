## iHeartRating Vision

This document explains the current state and direction of the project.
Project overview and developer docs: [`README.md`](README.md)

iHeartRating is an iOS rating view library that lets apps use custom images for
rating controls.

The repository is useful as a small Swift library with a podspec, sample usage,
screenshots, and tests. Project setup and examples live in [`README.md`](README.md).

The goal is to keep the component simple, reusable, and predictable for app
developers.

The current focus is:

Priority:

- Preserve the image-based rating view API
- Keep delegate callbacks for updating and completed rating changes clear
- Maintain podspec and sample app alignment
- Avoid growing the library beyond focused rating behavior
- Keep `scripts/check-baseline.py` passing for rating-view edge cases,
  rating bounds, `minImageSize` bounds, bounce behavior, podspec metadata,
  project files, non-editable began/moved touch handling, and build-script
  syntax
- Keep image layout invalidation tied to runtime rating image changes
- Keep child image geometry in the rating view's local bounds coordinate space
- Hide full overlays whenever an incomplete image pair is configured
- Normalize NaN rating assignments before rendering and animation indexing
- Normalize NaN `minImageSize` dimensions before image layout
- Normalize infinite `minImageSize` dimensions before image layout
- Keep `make lint`, `make test`, `make build`, and `make check` available as
  local verification gates
- Keep pinned, credential-free macOS CI parsing both Xcode projects through the
  canonical `make check` gate

Next priorities:

- Modernize Swift/project settings in a dedicated pass
- Add tests for rating calculations and delegate calls
- Clarify package-manager support if revived

Contribution rules:

- One PR = one focused API, test, sample, or documentation change.
- Keep the library lightweight and dependency-free.
- Run the build script or Xcode tests before pushing behavior changes.
- Preserve API compatibility for consumers where possible.

## Security

Canonical security policy and reporting:

- [`SECURITY.md`](SECURITY.md)

This UI component has low security risk, but it should not crash on malformed
configuration or unexpected image assets.

Current baseline: `make lint`, `make test`, `make build`, and `make check` run
`scripts/check-baseline.py` without Xcode. It verifies static project metadata,
CocoaPods specs, plist/storyboard files, build script syntax, and rating-view
guards for empty, single-item, zero-size, negative `minImageSize`, invalid
`maxRating`, inconsistent rating bounds, and out-of-range bounce configurations.
Bounce animation should remain independent of delegate callbacks, and
non-editable views or empty touch endings should ignore touch-ending delegate
and bounce work. Empty began/moved touch events should ignore live-update
delegate work. Non-editable began/moved touch events should also ignore
live-update delegate work.
Image layout invalidation should run when rating images change so masks refresh
against current frames.
Scaled or rotated rating views should continue laying out child images from
local bounds rather than transformed frame dimensions.
An incomplete image pair should render without full overlays or stale masks,
then restore normal rating rendering when both images are configured.
On macOS, the baseline should also parse both Xcode projects. Full Swift 2
compilation and simulator testing remain tied to Xcode 7.3 and a compatible
runtime.

## What We Will Not Merge (For Now)

- Broad UI frameworks unrelated to rating controls
- API-breaking changes without migration notes
- Package metadata changes without verification
- Behavior changes without tests or sample updates

This list is a roadmap guardrail, not a permanent rule.
Strong user demand and strong technical rationale can change it.
