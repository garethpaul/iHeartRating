# Changes

## 2026-06-10

- Added pinned, read-only macOS CI for the canonical `make check` baseline.
- Made Xcode-enabled checks parse both the library and SampleApp projects while
  keeping full Swift 2 compilation tied to a compatible legacy toolchain.

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
