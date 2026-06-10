# NaN Rating Boundary

status: completed

## Context

The shared rating clamp handled ordinary out-of-range numbers but allowed NaN
to survive because comparisons with NaN are false. Rendering then hid all full
images, and bounce animation could attempt an unsafe `Int(NaN)` conversion.

## Completed Scope

- Normalized NaN ratings to the configured `minRating`.
- Applied the guard in the shared programmatic and touch rating boundary.
- Added XCTest and static baseline coverage with a nonzero minimum.
- Documented the rendering and animation safety invariant.

## Verification

- `make lint`
- `make test`
- `make build`
- `make check`
- `git diff --check`
