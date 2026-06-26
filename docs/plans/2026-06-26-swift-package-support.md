# Swift Package Manager Support Boundary

Status: completed

## Context

The repository distributes the library through its Xcode project and CocoaPods
podspecs. It does not contain a `Package.swift`, but the README did not state
whether Swift Package Manager was supported.

## Work Completed

- Documented CocoaPods and direct Xcode integration as the supported surfaces.
- Stated that Swift Package Manager is not currently declared or verified.
- Required a focused future change to add a manifest, resource rules, and hosted verification.
- Retired the completed roadmap clarification item.
- Added a static contract for the documentation and absent-manifest boundary.

## Verification Completed

- `python3 scripts/check-baseline.py` passed.
- `make lint`, `make test`, `make build`, and `make check` passed.
- Both checked-in CocoaPods podspecs passed Ruby syntax validation.
- Four focused hostile mutations were rejected across README guidance, absent
  manifest, vision invariant, and completed-plan evidence.
- `git diff --check` passed.
