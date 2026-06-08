# iHeartRating Baseline Plan

status: completed

## Context

`iHeartRating` is a legacy Swift iOS rating-view library with a CocoaPods spec, sample app, screenshots, and Xcode tests. This Linux host does not provide Xcode, so local verification needs a static baseline while full simulator tests remain a macOS/Xcode responsibility.

## Objectives

- Add a deterministic `make check` baseline for podspec metadata, plist/storyboard files, shell syntax, source inventory, and rating-view safety guardrails.
- Keep the existing Xcode project and sample app intact.
- Harden rating layout and touch handling around edge-case configuration values.
- Keep package metadata secure and consistent across the root and archived podspecs.

## Verification

- `make check`
- `python3 scripts/check-baseline.py`
- `sh -n build.sh`
- `git diff --check`
