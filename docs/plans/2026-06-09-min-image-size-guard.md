# iHeartRating Min Image Size Guard

status: completed

## Context

`HeartRatingView.minImageSize` is inspectable from Interface Builder and feeds
layout sizing. The existing layout helper guarded zero-sized source images and
containers, but malformed negative minimum image sizes were still accepted as
configuration.

## Objectives

- Clamp negative `minImageSize` width and height values to zero.
- Request layout after `minImageSize` changes.
- Add focused XCTest source coverage for the negative configuration boundary.
- Extend the static baseline so the guard remains visible without local Xcode.

## Verification

- `python3 scripts/check-baseline.py`
- `make check`
- `git diff --check`
