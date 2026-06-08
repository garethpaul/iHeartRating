# Changes

## 2026-06-08

- Added `make check` and a static baseline for project metadata, podspecs, plist/storyboard files, and rating-view guardrails.
- Hardened rating layout and touch handling for empty, single-item, zero-size, invalid `maxRating`, and out-of-range bounce configurations.
- Added focused unit coverage for the `maxRating` lower bound and zero-size image handling.
- Made `build.sh` POSIX-compatible and explicit about requiring Xcode before running simulator tests.
- Updated podspec social media URLs to HTTPS in the root and archived `0.1.6` specs.
