# iHeartRating

<!-- README-OVERVIEW-IMAGE -->
![Project overview](docs/readme-overview.svg)

## Overview

`garethpaul/iHeartRating` is an Apple platform application or Swift sample. Simple Ratings View for iOS enabling you to use any image as a rating e.g. hearts, stars, pigeons etc.

This README is based on the checked-in source, manifests, scripts, and repository metadata on the `master` branch. The project language mix found during review was: Swift (6), C/C++ headers (1), shell (1).

## Repository Contents

- `CHANGES.md` - concise history of maintenance changes
- `Makefile` - local verification entry point
- `README.md` - project overview and local usage notes
- `build.sh`
- `example` - source or example code
- `iHeartRating` - source or example code
- `iHeartRating.xcodeproj` - Xcode project file
- `iHeartRating.podspec` - CocoaPods package metadata
- `iHeartRatingTests` - source or example code
- `SECURITY.md` - security reporting and disclosure guidance
- `scripts/check-baseline.py` - static rating-view and package verifier
- `VISION.md` - project direction and maintenance guardrails

Additional scan context:

- Source directories: example, iHeartRating, iHeartRatingTests
- Dependency and build manifests: iHeartRating.podspec
- Entry points or build surfaces: `make check`, build.sh, iHeartRating.xcodeproj
- Test-looking files: example/SampleApp/SampleAppTests/Info.plist, example/SampleApp/SampleAppTests/SampleAppTests.swift, example/SampleApp/SampleAppUITests/Info.plist, example/SampleApp/SampleAppUITests/SampleAppUITests.swift, iHeartRatingTests/Info.plist, iHeartRatingTests/iHeartRatingTests.swift

## Getting Started

### Prerequisites

- Git
- macOS with a current Xcode release for building Apple platform projects
- iOS 12 or newer for consumers
- Python 3 for local static verification on non-macOS hosts

### Setup

```bash
git clone https://github.com/garethpaul/iHeartRating.git
cd iHeartRating
make lint
make test
make build
make check
make xcode-test
```

The first four commands validate the location-independent static baseline.
`make xcode-test` selects an available iPhone simulator, runs the library XCTest
suite, checks the generated Objective-C compatibility header, and builds the
sample application.

## Running or Using the Project

- Open `iHeartRating.xcodeproj` in Xcode, choose the app or sample scheme, and run it on the matching simulator/device.
- Run `./build.sh` when Xcode and the required simulator runtime are installed.
- Use `example/SampleApp` for storyboard/sample-app behavior and `iHeartRating.podspec` for CocoaPods metadata review.

### Package Support

- CocoaPods and direct Xcode project integration are the currently declared and
  verified distribution surfaces.
- Swift Package Manager is not currently supported: this repository has no
  `Package.swift`, resource declaration, or hosted SwiftPM build.
- Adding SwiftPM support requires a focused change that defines the package
  products/targets, handles image resources, and adds executable hosted tests.

## Testing and Verification

Run the local static baseline:

```bash
make lint
make test
make build
make check
```

The `lint`, `test`, and `build` targets intentionally alias the static baseline.
Use `make xcode-test` for executable Swift, UIKit, Objective-C interoperability,
and sample-project evidence.

The baseline parses plist/storyboard/SVG files, validates both podspecs, checks `build.sh` shell syntax, verifies rating-view guards for empty, single-item, zero-size, negative `minImageSize`, invalid `maxRating`, rating bounds, non-editable touch endings, empty touch endings, empty began/moved touch events, out-of-range bounce configurations, and delegate-independent bounce behavior, and reports when Xcode is unavailable.
It also keeps non-editable began/moved touch events from sending live-update
delegate callbacks.
It also keeps image layout invalidation in the rating image setters so runtime
image changes recalculate frames before masks refresh.
Rating image geometry is calculated from the view's local bounds so transforms
do not inflate or misalign child images.
When a control is narrower than its intrinsic minimum, each image is capped to
its rating slot so interactive frames remain ordered and non-overlapping.
An incomplete image pair renders no full overlays: clearing either image hides
filled ratings and removes stale masks until both images are configured again.
NaN programmatic ratings fall back to `minRating` before mask rendering or
bounce animation indexing.
NaN `minImageSize` dimensions normalize independently to zero while valid
companion dimensions are preserved.
Infinite `minImageSize` dimensions normalize independently to zero while valid
companion dimensions are preserved.
`imageContentMode` changes propagate to every existing image view so already
created empty and full image pairs stay synchronized with the configured mode.
External consumers can configure the public `imageContentMode` property while its existing observer keeps every rating image synchronized.
Complete image pairs provide an intrinsic content size derived from the larger
configured image, `minImageSize`, and `maxRating`; incomplete pairs have zero
intrinsic size and clear stale filled-image masks.
Hostile NaN, infinite, negative, zero, and extreme finite geometry is normalized
or bounded before frames and masks reach Core Animation.
`maxRating` is capped at 100 before child image views are allocated, preventing
unbounded memory growth from malformed configuration.
The control is one adjustable accessibility element with a default `Rating`
label, a synchronized `<value> of <max>` value, and bounded increment/decrement
actions. Consumers may replace the accessibility label for localization.
As with UIKit generally, create and mutate `HeartRatingView` on the main thread.

The pinned, credential-free GitHub Actions check runs both `make check` and
`make xcode-test` on `macos-15`. The projects pin Swift 5 and iOS 12, the hosted
gate executes XCTest on a simulator, inspects the generated Swift-to-Objective-C
header, and compiles the SampleApp without signing.

When the required SDK or runtime is unavailable, use static checks and source review first, then verify on a machine that has the matching platform toolchain.

## Configuration and Secrets

- No required secret or credential file was identified in the repository scan. If you add integrations later, keep secrets out of git.

## Security and Privacy Notes

- Review changes touching network requests, sockets, or service endpoints; examples from the scan include example/SampleApp/SampleApp/Info.plist, example/SampleApp/SampleAppTests/Info.plist, example/SampleApp/SampleAppUITests/Info.plist, iHeartRating/Info.plist, and 1 more.
- Review changes touching mobile permissions or privacy-sensitive device data; examples from the scan include iHeartRating/iHeartRatingView.swift.
- Review changes touching file, media, JSON, XML, CSV, OCR, or data parsing; examples from the scan include example/SampleApp/SampleApp/Info.plist, example/SampleApp/SampleAppTests/Info.plist, example/SampleApp/SampleAppUITests/Info.plist, iHeartRating/Info.plist, and 2 more.
- UI configuration changes should not crash on empty image arrays, single-rating views, zero-sized images, negative `minImageSize`, invalid `maxRating`, inconsistent rating bounds, or out-of-range ratings.
- Runtime image changes should preserve image layout invalidation before mask
  refresh work runs.
- Rating image layout should use local bounds rather than transformed frame
  dimensions.
- Compressed layouts should cap images to their rating slots instead of
  allowing oversized minimum widths to create overlapping frames.
- An incomplete image pair should hide full overlays and clear stale masks
  until both rating images are configured.

## Maintenance Notes

- Every Make verification target derives the checkout root from the loaded
  Makefile, so an absolute Makefile path works from any working directory.
- This looks like an Apple platform project or sample. Xcode, Swift, CocoaPods, and deployment target versions may need to match the original project era.
- See `SECURITY.md` for vulnerability reporting and safe research guidance.
- See `VISION.md` for project direction and contribution guardrails.
- See `docs/plans/2026-06-08-bounce-without-delegate.md` for the bounce-without-delegate guardrail.
- See `docs/plans/2026-06-09-noneditable-touch-end.md` for the non-editable touch-ending guardrail.
- See `docs/plans/2026-06-09-empty-touch-end.md` for the empty touch-ending guardrail.
- See `docs/plans/2026-06-09-empty-touch-phase-guard.md` for the empty
  began/moved touch guardrail.
- See `docs/plans/2026-06-09-noneditable-touch-phase-guard.md` for the
  non-editable began/moved touch guardrail.
- See `docs/plans/2026-06-09-min-image-size-guard.md` for the `minImageSize` lower-bound guardrail.
- See `docs/plans/2026-06-09-rating-image-layout-invalidation.md` for the
  image layout invalidation guardrail.
- See `docs/plans/2026-06-10-nan-rating-boundary.md` for non-finite rating
  normalization.
- See `docs/plans/2026-06-12-bounds-based-image-layout.md` for transformed-view
  layout correctness.
- See `docs/plans/2026-06-13-incomplete-image-pair.md` for fail-closed image-pair
  rendering.
- See `docs/plans/2026-06-26-swift-package-support.md` for the current
  CocoaPods/Xcode-only package boundary.
- See `docs/plans/2026-06-09-make-gate-aliases.md` for the local gate alias guardrail.
- Run `make lint`, `make test`, `make build`, and `make check` before pushing changes to Swift sources, podspecs, plist/storyboard files, or build scripts.

## Contributing

Keep changes small and tied to the project that is already present in this repository. For code changes, document the toolchain used, avoid committing generated dependency directories or local configuration, and update this README when setup or verification steps change.
