# iHeartRating Deep Review Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use executing-plans to implement this plan task-by-task.

**Goal:** Land the stacked rating-control fixes with finite layout geometry, useful Auto Layout sizing, accessible state, preserved Objective-C selectors, and real Xcode build/test evidence.

**Architecture:** Preserve `HeartRatingView` as the single owner of rating state and child image views. Modernize the legacy Swift syntax without redesigning the public control, centralize finite geometry normalization at the layout boundary, derive intrinsic size from the configured image pair and rating count, and keep accessibility state synchronized from the same refresh path.

**Tech Stack:** Swift 5, UIKit, XCTest, Xcode project builds, Python static baseline checks, GitHub Actions.

---

### Task 1: Establish Modern Build Failure

**Files:**
- Test: `iHeartRatingTests/iHeartRatingTests.swift`
- Modify: `iHeartRating.xcodeproj/project.pbxproj`

**Step 1:** Add focused modern XCTest cases for hostile geometry, repeated layout, intrinsic size, content-mode reinitialization, incomplete image pairs, and accessibility.

**Step 2:** Run `xcodebuild` and record the expected legacy Swift configuration/syntax failure.

**Step 3:** Set explicit Swift 5 project settings and modernize only the syntax required to compile the existing API and tests.

**Step 4:** Re-run the narrow test target and confirm the new behavior tests fail for missing implementation rather than project configuration.

### Task 2: Harden Geometry and Intrinsic Size

**Files:**
- Modify: `iHeartRating/iHeartRatingView.swift`
- Test: `iHeartRatingTests/iHeartRatingTests.swift`

**Step 1:** Verify hostile `NaN`, infinity, negative, zero, and extreme finite geometry tests fail.

**Step 2:** Add one finite nonnegative normalization boundary and use it for `minImageSize`, `sizeForImage`, layout bounds, mask widths, and intrinsic-size multiplication.

**Step 3:** Invalidate intrinsic content size when images, image count, or minimum image size changes.

**Step 4:** Run the focused XCTest cases and confirm every generated frame, mask, and intrinsic dimension is finite and stable across repeated layout passes.

### Task 3: Preserve API and Accessibility

**Files:**
- Modify: `iHeartRating/iHeartRatingView.swift`
- Test: `iHeartRatingTests/iHeartRatingTests.swift`

**Step 1:** Verify tests fail for missing adjustable traits, rating value, increment/decrement behavior, and image content mode after child-view replacement.

**Step 2:** Preserve Objective-C delegate selectors with explicit `@objc` declarations and expose compatible public members through `@objcMembers`.

**Step 3:** Make the view one accessibility element, synchronize label/value/traits, and implement bounded accessibility increment/decrement callbacks.

**Step 4:** Run XCTest and inspect the generated Swift Objective-C header after a successful framework build.

### Task 4: Make Validation Executable

**Files:**
- Modify: `Makefile`
- Modify: `build.sh`
- Modify: `.github/workflows/check.yml`
- Modify: `scripts/check-baseline.py`

**Step 1:** Add a location-independent `make xcode-test` command using a concrete available simulator.

**Step 2:** Extend static contracts to reject removal of finite geometry, intrinsic sizing, accessibility, Swift version, and hosted Xcode execution.

**Step 3:** Run `make check` from the repository and from an external directory, then run `make xcode-test`.

**Step 4:** Apply isolated hostile mutations and verify the static/XCTest gates reject them.

### Task 5: Document and Land

**Files:**
- Modify: `README.md`
- Modify: `CHANGES.md`
- Modify: `SECURITY.md`
- Modify: `VISION.md`

**Step 1:** Document the modern toolchain requirement, intrinsic sizing, accessibility behavior, main-thread UIKit contract, and residual visual/device validation.

**Step 2:** Scan the current tree and complete Git history for credentials without printing candidate values.

**Step 3:** Push one aggregate branch, open a consolidation PR against `master`, and wait for exact-head hosted Check and CodeQL evidence.

**Step 4:** Merge the aggregate PR, close PRs `#13`–`#19` as superseded, and verify the final protected branch SHA and zero open PRs.
