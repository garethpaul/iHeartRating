# Changes

- Preserved absolute Makefile roots containing spaces and added a recursive-safe full-baseline regression.
- Rejected ambiguous Makefile inputs so later recipes cannot replace verification gates.

## 2026-06-26T12:03:17Z — P3 documentation — package support boundary

- Clarified that CocoaPods and direct Xcode integration are the currently
  declared and verified distribution surfaces.
- Documented that Swift Package Manager is not supported without a
  `Package.swift`, resource rules, and hosted SwiftPM build evidence.
- Retired the completed package-support clarification priority and added a
  fail-closed baseline contract plus completed implementation plan.
- Validation passed the static/Make gates, both podspec syntax checks, four
  hostile documentation/manifest mutations, and `git diff --check`.

## 2026-06-25 — P2 correctness — accessibility boundary no-ops

- Made accessibility increment and decrement actions true no-ops at the rating
  boundaries so they do not send duplicate completed-update callbacks or start
  bounce feedback when the value cannot change.

## 2026-06-25T20:57:46Z — P2 correctness — cycle: constrained image spacing

- Threads: inspected the default branch, open work, rating bounds, hostile
  geometry normalization, intrinsic sizing, transformed layout, touch and
  accessibility paths, Xcode tests, static contracts, and hosted workflow; no
  open pull requests or issues were present.
- Bug fixed: constrained layout now caps each rating image to its available
  slot width, preventing oversized `minImageSize` values from producing
  negative spacing and overlapping interactive image frames.
- Files: `iHeartRatingView.swift`, `iHeartRatingTests.swift`,
  `scripts/check-baseline.py`, and
  `docs/plans/2026-06-25-constrained-rating-image-spacing.md`.
- Validation: reproduced the missing slot-cap contract, passed the static
  baseline, Python and shell syntax checks, and both CocoaPods spec checks.
- Blockers: Xcode and an iOS simulator are unavailable locally; hosted macOS
  executable tests and Objective-C header validation remain required.
- Next: visually verify extreme intrinsic minimums in compressed stack and
  Auto Layout containers across left-to-right and right-to-left interfaces.

## 2026-06-19

- Migrated the library, tests, and SampleApp from unbuildable Swift 2 project
  settings to Swift 5 with an iOS 12 deployment target.
- Prepared CocoaPods `0.2.0` metadata for the Swift 5/iOS 12 compatibility
  boundary while preserving external subclassing and Objective-C selectors.
- Added executable hosted simulator tests and generated Objective-C header
  checks while preserving the `heartRatingView:didUpdate:` and
  `heartRatingView:isUpdating:` selectors.
- Bounded hostile and extreme layout geometry before creating image frames or
  partial-rating masks, and added stable repeated-layout coverage.
- Capped `maxRating` at 100 before allocating paired image views.
- Added intrinsic content sizing for complete image pairs and zero intrinsic
  size for incomplete pairs.
- Added synchronized adjustable accessibility label, value, traits, and bounded
  increment/decrement actions.
- Updated CocoaPods metadata with the tested iOS and Swift versions.

## 2026-06-17

- External consumers can configure the public `imageContentMode` property while its existing observer keeps every rating image synchronized.

## 2026-06-14

- Made `imageContentMode` changes propagate to every existing image view and
  added regression coverage for all empty and full image pairs.

## 2026-06-13

- Made every Make verification target derive the checkout root so the static
  rating-view baseline works from external directories.
- Normalized infinite `minImageSize` width and height independently to zero
  while preserving valid companion dimensions.
- Normalized NaN `minImageSize` width and height independently to zero while
  preserving valid companion dimensions.
- Made incomplete image pair configuration hide full rating overlays and clear
  stale masks until both images are configured again.

## 2026-06-10

- Normalized NaN rating assignments to `minRating` before rendering or bounce
  index conversion.
- Added pinned, read-only macOS CI without persisted checkout credentials for
  the canonical `make check` baseline.
- Made Xcode-enabled checks parse both the library and SampleApp projects while
  keeping full Swift 2 compilation tied to a compatible legacy toolchain.
- Calculated rating image geometry from local bounds so view transforms do not
  distort child layout.

## 2026-06-09

- Added image layout invalidation when rating images change so refreshed masks
  use current image frames.
- Added local `make lint`, `make test`, and `make build` gate aliases for the
  static rating-view baseline.
- Guarded `touchesEnded` when the rating view is not editable so disabled
  controls do not send delegate updates or run bounce animations.
- Guarded empty touch-ending events so they do not send delegate updates or run
  bounce animations.
- Guarded empty began/moved touch events so they do not send live-update
  delegate callbacks.
- Clamped negative `minImageSize` values to zero before requesting layout.
- Guarded non-editable began/moved touch events so disabled controls do not
  send live-update delegate callbacks.

## 2026-06-08

- Added `make check` and a static baseline for project metadata, podspecs, plist/storyboard files, and rating-view guardrails.
- Hardened rating layout and touch handling for empty, single-item, zero-size, invalid `maxRating`, and out-of-range bounce configurations.
- Normalized public `rating` and `minRating` assignments so rating bounds remain consistent with `maxRating`.
- Kept the bounce animation independent of delegate callbacks when `shouldBounce` is enabled.
- Added focused unit coverage for the `maxRating` lower bound and zero-size image handling.
- Made `build.sh` POSIX-compatible and explicit about requiring Xcode before running simulator tests.
- Updated podspec social media URLs to HTTPS in the root and archived `0.1.6` specs.
