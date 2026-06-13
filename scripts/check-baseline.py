#!/usr/bin/env python3
from pathlib import Path
import plistlib
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
BASELINE_PLAN = ROOT / "docs/plans/2026-06-08-rating-baseline.md"
MAKE_GATES_PLAN = ROOT / "docs/plans/2026-06-09-make-gate-aliases.md"
RATING_BOUNDS_PLAN = ROOT / "docs/plans/2026-06-08-rating-bounds.md"
BOUNCE_PLAN = ROOT / "docs/plans/2026-06-08-bounce-without-delegate.md"
NONEDITABLE_PLAN = ROOT / "docs/plans/2026-06-09-noneditable-touch-end.md"
EMPTY_TOUCH_PLAN = ROOT / "docs/plans/2026-06-09-empty-touch-end.md"
MIN_IMAGE_SIZE_PLAN = ROOT / "docs/plans/2026-06-09-min-image-size-guard.md"
EMPTY_TOUCH_PHASE_PLAN = ROOT / "docs/plans/2026-06-09-empty-touch-phase-guard.md"
NONEDITABLE_TOUCH_PHASE_PLAN = ROOT / "docs/plans/2026-06-09-noneditable-touch-phase-guard.md"
IMAGE_LAYOUT_PLAN = ROOT / "docs/plans/2026-06-09-rating-image-layout-invalidation.md"
HOSTED_VALIDATION_PLAN = ROOT / "docs/plans/2026-06-10-hosted-project-validation.md"
NAN_RATING_PLAN = ROOT / "docs/plans/2026-06-10-nan-rating-boundary.md"
BOUNDS_LAYOUT_PLAN = ROOT / "docs/plans/2026-06-12-bounds-based-image-layout.md"
INCOMPLETE_IMAGE_PLAN = ROOT / "docs/plans/2026-06-13-incomplete-image-pair.md"
NAN_MIN_IMAGE_SIZE_PLAN = ROOT / "docs/plans/2026-06-13-nan-min-image-size.md"


def require(condition, message, failures):
    if not condition:
        failures.append(message)


def read(relative_path):
    return (ROOT / relative_path).read_text(encoding="utf-8", errors="replace")


def parse_xml(relative_path, failures):
    try:
        ET.parse(str(ROOT / relative_path))
    except ET.ParseError as error:
        failures.append(f"{relative_path} is not well-formed XML: {error}")


def parse_plist(relative_path, failures):
    try:
        with (ROOT / relative_path).open("rb") as file:
            return plistlib.load(file)
    except Exception as error:
        failures.append(f"{relative_path} is not a readable plist: {error}")
        return {}


def run(command, failures, message):
    result = subprocess.run(
        command,
        cwd=str(ROOT),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        failures.append(message + "\n" + (result.stderr or result.stdout).strip())


def main():
    failures = []
    required_files = [
        ".gitignore",
        ".github/workflows/check.yml",
        ".travis.yml",
        "CHANGES.md",
        "LICENSE",
        "Makefile",
        "README.md",
        "SECURITY.md",
        "VISION.md",
        "build.sh",
        "iHeartRating.podspec",
        "iHeartRating/0.1.6/iHeartRating.podspec",
        "iHeartRating.xcodeproj/project.pbxproj",
        "iHeartRating/Info.plist",
        "iHeartRating/iHeartRating.h",
        "iHeartRating/iHeartRatingView.swift",
        "iHeartRatingTests/Info.plist",
        "iHeartRatingTests/iHeartRatingTests.swift",
        "example/SampleApp/README.md",
        "example/SampleApp/SampleApp.xcodeproj/project.pbxproj",
        "example/SampleApp/SampleApp/Info.plist",
        "example/SampleApp/SampleApp/Base.lproj/Main.storyboard",
        "example/SampleApp/SampleApp/Base.lproj/LaunchScreen.storyboard",
        "screenshots/heart_app_example.gif",
        "assets/logo.png",
        "assets/storyboard.png",
        "docs/readme-overview.svg",
        "docs/plans/2026-06-08-rating-baseline.md",
        "docs/plans/2026-06-09-make-gate-aliases.md",
        "docs/plans/2026-06-08-rating-bounds.md",
        "docs/plans/2026-06-08-bounce-without-delegate.md",
        "docs/plans/2026-06-09-noneditable-touch-end.md",
        "docs/plans/2026-06-09-empty-touch-end.md",
        "docs/plans/2026-06-09-min-image-size-guard.md",
        "docs/plans/2026-06-09-empty-touch-phase-guard.md",
        "docs/plans/2026-06-09-noneditable-touch-phase-guard.md",
        "docs/plans/2026-06-09-rating-image-layout-invalidation.md",
        "docs/plans/2026-06-10-hosted-project-validation.md",
        "docs/plans/2026-06-10-nan-rating-boundary.md",
        "docs/plans/2026-06-12-bounds-based-image-layout.md",
        "docs/plans/2026-06-13-incomplete-image-pair.md",
        "docs/plans/2026-06-13-nan-min-image-size.md",
    ]

    for relative_path in required_files:
        require((ROOT / relative_path).is_file(), f"Required file missing: {relative_path}", failures)

    for xml_file in [
        "example/SampleApp/SampleApp/Base.lproj/Main.storyboard",
        "example/SampleApp/SampleApp/Base.lproj/LaunchScreen.storyboard",
        "docs/readme-overview.svg",
    ]:
        parse_xml(xml_file, failures)

    for plist_file in [
        "iHeartRating/Info.plist",
        "iHeartRatingTests/Info.plist",
        "example/SampleApp/SampleApp/Info.plist",
        "example/SampleApp/SampleAppTests/Info.plist",
        "example/SampleApp/SampleAppUITests/Info.plist",
    ]:
        parse_plist(plist_file, failures)

    run(["sh", "-n", "build.sh"], failures, "build.sh must be valid POSIX shell")

    build_sh = read("build.sh")
    require("command -v xcodebuild" in build_sh and "xcodebuild not found" in build_sh,
            "build.sh must fail clearly when Xcode is unavailable",
            failures)
    require("ci_lib()" in build_sh and "function ci_lib" not in build_sh,
            "build.sh must use POSIX function syntax",
            failures)

    rating_view = read("iHeartRating/iHeartRatingView.swift")
    tests = read("iHeartRatingTests/iHeartRatingTests.swift")
    refresh_body = rating_view.split("func refresh() {", 1)[1].split("// MARK: Layout helper classes", 1)[0]
    incomplete_image_branch = re.search(
        r"if self\.emptyImage == nil \|\| self\.fullImage == nil \{(?P<body>.*?)\n\s*return\s*\n\s*\}",
        refresh_body,
        re.DOTALL,
    )
    require(rating_view.count("let maxImageWidth =") == 1,
            "layoutSubviews must declare maxImageWidth once",
            failures)
    require("if maxRating < 1" in rating_view and "maxRating = 1" in rating_view,
            "maxRating must be clamped to a supported lower bound",
            failures)
    require("private func boundedRating" in rating_view and
            "return min(max(rating, Float(self.minRating)), Float(self.maxRating))" in rating_view,
            "rating assignments must be bounded by minRating and maxRating",
            failures)
    require("if rating != rating" in rating_view and "return Float(self.minRating)" in rating_view,
            "NaN ratings must fall back to minRating before rendering or bounce indexing",
            failures)
    require("if minRating < 0" in rating_view and "if minRating > maxRating" in rating_view,
            "minRating must stay non-negative and not exceed maxRating",
            failures)
    require("self.rating = self.boundedRating(newRating)" in rating_view,
            "touch handling must reuse bounded rating normalization",
            failures)
    require("if image.size.width <= 0 || image.size.height <= 0 || size.width <= 0 || size.height <= 0" in rating_view,
            "sizeForImage must guard zero-sized images and containers",
            failures)
    require("minImageSize.width < 0 || minImageSize.height < 0" in rating_view and
            "minImageSize = CGSize" in rating_view and "setNeedsLayout()" in rating_view,
            "minImageSize must be clamped to non-negative values and trigger layout",
            failures)
    require("minImageSize.width != minImageSize.width" in rating_view and
            "minImageSize.height != minImageSize.height" in rating_view and
            rating_view.count("? CGFloat(0.0) : max(CGFloat(0.0), minImageSize.") == 2,
            "minImageSize must normalize NaN width and height independently",
            failures)
    require(re.search(r"@IBInspectable public var emptyImage: UIImage\? \{.*?didSet \{.*?self\.setNeedsLayout\(\).*?self\.refresh\(\)", rating_view, re.DOTALL),
            "emptyImage changes must invalidate layout before refreshing masks",
            failures)
    require(re.search(r"@IBInspectable public var fullImage: UIImage\? \{.*?didSet \{.*?self\.setNeedsLayout\(\).*?self\.refresh\(\)", rating_view, re.DOTALL),
            "fullImage changes must invalidate layout before refreshing masks",
            failures)
    require("let imageCount = self.emptyImageViews.count" in rating_view and "if imageCount == 0" in rating_view,
            "layoutSubviews must guard empty image arrays",
            failures)
    require("imageCount > 1 ?" in rating_view,
            "layoutSubviews must avoid dividing by imageCount - 1 for single-rating views",
            failures)
    require("let layoutBounds = self.bounds" in rating_view and
            "layoutBounds.size.width / CGFloat(imageCount)" in rating_view and
            "max(self.minImageSize.height, layoutBounds.size.height)" in rating_view and
            "layoutBounds.origin.x" in rating_view and "layoutBounds.origin.y" in rating_view,
            "layoutSubviews must calculate image geometry in local bounds coordinates",
            failures)
    require("self.frame.size.width / CGFloat(imageCount)" not in rating_view and
            "max(self.minImageSize.height, self.frame.size.height)" not in rating_view,
            "layoutSubviews must not size child images from transformed frame coordinates",
            failures)
    require("if self.emptyImageViews.isEmpty" in rating_view,
            "touch handling must guard empty image arrays",
            failures)
    require("if imageView.frame.size.width <= 0" in rating_view,
            "touch handling must guard zero-width image frames",
            failures)
    require("shouldBounce && !self.fullImageViews.isEmpty" in rating_view and "min(max(rawImageViewIndex, 0), self.fullImageViews.count - 1)" in rating_view,
            "bounce handling must clamp the animated image index",
            failures)
    require("private func bounceImageForCurrentRating()" in rating_view and "self.bounceImageForCurrentRating()" in rating_view,
            "bounce handling must run independently of delegate callbacks",
            failures)
    require(rating_view.count("if !self.editable") >= 4,
            "touch handling must ignore began, moved, and ended touches when the view is not editable",
            failures)
    require("if touches.isEmpty" in rating_view,
            "touch handlers must ignore empty touch sets before delegate and bounce work",
            failures)
    require(rating_view.count("if touches.isEmpty") >= 3,
            "touchesBegan, touchesMoved, and touchesEnded must all guard empty touch sets",
            failures)
    require(incomplete_image_branch is not None and
            "for imageView in self.fullImageViews" in incomplete_image_branch.group("body") and
            "imageView.layer.mask = nil" in incomplete_image_branch.group("body") and
            "imageView.hidden = true" in incomplete_image_branch.group("body"),
            "refresh must clear and hide full overlays before returning for an incomplete image pair",
            failures)
    require("testMaxRatingDoesNotStayBelowOne" in tests and "testZeroSizeImageReturnsZeroSize" in tests and
            "testRatingDoesNotExceedMaxRating" in tests and "testMinRatingDoesNotExceedMaxRating" in tests and
            "testNaNRatingFallsBackToMinRating" in tests and "Float(0.0) / Float(0.0)" in tests and
            "testMinImageSizeDoesNotStayNaN" in tests and
            "CGSize(width: nan, height: 12)" in tests and
            "CGSize(width: 15, height: nan)" in tests and
            "XCTAssert(hrv.minImageSize.height == 12)" in tests and
            "XCTAssert(hrv.minImageSize.width == 15)" in tests and
            "testMinImageSizeDoesNotStayNegative" in tests and
            "testLayoutUsesLocalBoundsWhenViewIsScaled" in tests and
            "testIncompleteImagePairHidesAndRestoresFullImages" in tests and
            "XCTAssertTrue(firstFullImageView.hidden)" in tests and
            "XCTAssertNil(firstFullImageView.layer.mask)" in tests and
            tests.count("XCTAssertFalse(firstFullImageView.hidden)") == 2 and
            "CGAffineTransformMakeScale(2, 2)" in tests and
            "hrv.bounds.size.width == 100" in tests and
            "testTouchesEndedDoesNotNotifyWhenNotEditable" in tests and
            "testTouchesEndedDoesNotNotifyWithoutTouches" in tests and
            "testTouchesBeganDoesNotNotifyWithoutTouches" in tests and
            "testTouchesMovedDoesNotNotifyWithoutTouches" in tests,
            "unit tests must cover rating bounds, maxRating lower bound, zero-size image handling, and touch-end guards",
            failures)

    root_podspec = read("iHeartRating.podspec")
    archived_podspec = read("iHeartRating/0.1.6/iHeartRating.podspec")
    for name, podspec in [("iHeartRating.podspec", root_podspec), ("iHeartRating/0.1.6/iHeartRating.podspec", archived_podspec)]:
        require('s.name         = "iHeartRating"' in podspec, f"{name} must keep the pod name", failures)
        require('s.version      = "0.1.6"' in podspec, f"{name} must keep version 0.1.6", failures)
        require('s.source       = { :git => "https://github.com/garethpaul/iHeartRating.git", :tag => s.version }' in podspec,
                f"{name} must use HTTPS git source and tag by version",
                failures)
        require('s.social_media_url   = "https://twitter.com/gpj"' in podspec,
                f"{name} must use HTTPS social media URL",
                failures)
        require('s.source_files = "iHeartRating/*.{swift}"' in podspec,
                f"{name} must keep the Swift source glob",
                failures)

    readme = read("README.md")
    vision = read("VISION.md")
    security = read("SECURITY.md")
    changes = read("CHANGES.md")
    makefile = read("Makefile")
    baseline_plan = BASELINE_PLAN.read_text(encoding="utf-8") if BASELINE_PLAN.exists() else ""
    make_gates_plan = MAKE_GATES_PLAN.read_text(encoding="utf-8") if MAKE_GATES_PLAN.exists() else ""
    rating_bounds_plan = RATING_BOUNDS_PLAN.read_text(encoding="utf-8") if RATING_BOUNDS_PLAN.exists() else ""
    bounce_plan = BOUNCE_PLAN.read_text(encoding="utf-8") if BOUNCE_PLAN.exists() else ""
    noneditable_plan = NONEDITABLE_PLAN.read_text(encoding="utf-8") if NONEDITABLE_PLAN.exists() else ""
    empty_touch_plan = EMPTY_TOUCH_PLAN.read_text(encoding="utf-8") if EMPTY_TOUCH_PLAN.exists() else ""
    min_image_size_plan = MIN_IMAGE_SIZE_PLAN.read_text(encoding="utf-8") if MIN_IMAGE_SIZE_PLAN.exists() else ""
    empty_touch_phase_plan = EMPTY_TOUCH_PHASE_PLAN.read_text(encoding="utf-8") if EMPTY_TOUCH_PHASE_PLAN.exists() else ""
    noneditable_touch_phase_plan = NONEDITABLE_TOUCH_PHASE_PLAN.read_text(encoding="utf-8") if NONEDITABLE_TOUCH_PHASE_PLAN.exists() else ""
    image_layout_plan = IMAGE_LAYOUT_PLAN.read_text(encoding="utf-8") if IMAGE_LAYOUT_PLAN.exists() else ""
    hosted_validation_plan = HOSTED_VALIDATION_PLAN.read_text(encoding="utf-8") if HOSTED_VALIDATION_PLAN.exists() else ""
    nan_rating_plan = NAN_RATING_PLAN.read_text(encoding="utf-8") if NAN_RATING_PLAN.exists() else ""
    bounds_layout_plan = BOUNDS_LAYOUT_PLAN.read_text(encoding="utf-8") if BOUNDS_LAYOUT_PLAN.exists() else ""
    incomplete_image_plan = INCOMPLETE_IMAGE_PLAN.read_text(encoding="utf-8") if INCOMPLETE_IMAGE_PLAN.exists() else ""
    nan_min_image_size_plan = NAN_MIN_IMAGE_SIZE_PLAN.read_text(encoding="utf-8") if NAN_MIN_IMAGE_SIZE_PLAN.exists() else ""
    workflow = read(".github/workflows/check.yml")
    require(".PHONY: build check lint test" in makefile and "lint test build: check" in makefile,
            "Makefile must expose lint, test, and build aliases for the local baseline",
            failures)
    require("make lint" in readme and "make test" in readme and "make build" in readme and "make check" in readme and "build.sh" in readme and "podspec" in readme and "delegate-independent bounce" in readme and "non-editable" in readme and "empty touch" in readme.lower() and "minImageSize" in readme and "image layout invalidation" in readme and "local bounds" in readme.lower(),
            "README must document static verification, build script, and podspec expectations",
            failures)
    require("empty began/moved touch" in readme,
            "README must document empty began/moved touch guards",
            failures)
    require("non-editable began/moved touch" in readme,
            "README must document non-editable began/moved touch guards",
            failures)
    require("incomplete image pair" in readme.lower(),
            "README must document fail-closed rendering for incomplete image pairs",
            failures)
    require("NaN `minImageSize` dimensions normalize independently" in readme and
            "NaN `minImageSize` dimensions must normalize to zero" in security and
            "Normalize NaN `minImageSize` dimensions" in vision and
            "Normalized NaN `minImageSize` width and height independently" in changes,
            "Docs must record NaN minimum-image-size normalization",
            failures)
    require("scripts/check-baseline.py" in vision and "make lint" in vision and "make test" in vision and "make build" in vision and "rating" in vision.lower() and "bounce" in vision.lower() and "non-editable" in vision.lower() and "empty touch" in vision.lower() and "empty began/moved touch" in vision.lower() and "minImageSize" in vision and "image layout invalidation" in vision and "local bounds" in vision.lower(),
            "VISION must describe baseline validation for rating behavior",
            failures)
    require("non-editable began/moved touch" in vision,
            "VISION must describe non-editable began/moved touch guards",
            failures)
    require("incomplete image pair" in vision.lower(),
            "VISION must describe fail-closed rendering for incomplete image pairs",
            failures)
    require("malformed configuration" in security and "make check" in security and "non-editable" in security and "empty touch" in security.lower() and "minImageSize" in security and "image layout invalidation" in security and "local bounds" in security.lower(),
            "SECURITY must document configuration hardening and verification",
            failures)
    require("incomplete image pair" in security.lower(),
            "SECURITY must document incomplete image-pair hardening",
            failures)
    require("zero-size" in changes and "maxRating" in changes and "podspec" in changes and "rating bounds" in changes and "bounce" in changes and "not editable" in changes and "empty touch" in changes.lower() and "minImageSize" in changes and "image layout invalidation" in changes and "local bounds" in changes.lower() and "make lint" in changes and "make test" in changes and "make build" in changes,
            "CHANGES must record rating edge-case, rating bounds, and podspec updates",
            failures)
    require("empty began/moved touch" in changes,
            "CHANGES must record empty began/moved touch guards",
            failures)
    require("non-editable began/moved touch" in changes,
            "CHANGES must record non-editable began/moved touch guards",
            failures)
    require("incomplete image pair" in changes.lower(),
            "CHANGES must record incomplete image-pair rendering behavior",
            failures)
    require("status: completed" in baseline_plan and "status: completed" in rating_bounds_plan and "status: completed" in bounce_plan,
            "plans must be marked completed",
            failures)
    require("status: completed" in make_gates_plan,
            "make gate aliases plan must be marked completed",
            failures)
    require("status: completed" in noneditable_plan,
            "non-editable touch-end plan must be marked completed",
            failures)
    require("status: completed" in empty_touch_plan,
            "empty touch-end plan must be marked completed",
            failures)
    require("status: completed" in min_image_size_plan,
            "min image size plan must be marked completed",
            failures)
    require("status: completed" in empty_touch_phase_plan,
            "empty touch phase plan must be marked completed",
            failures)
    require("status: completed" in noneditable_touch_phase_plan,
            "non-editable touch phase plan must be marked completed",
            failures)
    require("status: completed" in image_layout_plan,
            "rating image layout invalidation plan must be marked completed",
            failures)
    require("status: completed" in hosted_validation_plan and "make check" in hosted_validation_plan,
            "hosted project validation plan must be completed and document make check",
            failures)
    require("status: completed" in nan_rating_plan and "make check" in nan_rating_plan,
            "NaN rating boundary plan must be completed and document verification",
            failures)
    require("status: completed" in incomplete_image_plan and
            "All four Make gates" in incomplete_image_plan and
            "hostile mutations" in incomplete_image_plan.lower(),
            "incomplete image pair plan must record completed status and actual verification",
            failures)
    nan_min_image_size_statuses = re.findall(
        r"^status: .+$", nan_min_image_size_plan, flags=re.MULTILINE
    )
    nan_min_image_size_sections = nan_min_image_size_plan.split(
        "## Verification Completed\n", 1
    )
    nan_min_image_size_verification = (
        nan_min_image_size_sections[1]
        if len(nan_min_image_size_sections) == 2 else ""
    )
    nan_min_image_size_required_evidence = (
        "All four Make gates",
        "`xcodebuild` was",
        "python3 -m py_compile scripts/check-baseline.py",
        "sh -n build.sh",
        "ruby -c iHeartRating.podspec",
        "git diff --check",
        "Five isolated hostile mutations",
        "Hosted macOS XCTest and CodeQL evidence",
    )
    require(nan_min_image_size_statuses == ["status: completed"]
            and all(item in nan_min_image_size_verification
                    for item in nan_min_image_size_required_evidence)
            and re.search(r"\b(?:pending|todo|tbd|not run)\b",
                          nan_min_image_size_verification,
                          re.IGNORECASE) is None,
            "NaN minImageSize plan must record completed status and actual local verification",
            failures)
    bounds_layout_statuses = re.findall(
        r"^status: .+$", bounds_layout_plan, flags=re.MULTILINE
    )
    bounds_layout_sections = bounds_layout_plan.split("## Verification Completed\n", 1)
    bounds_layout_verification = (
        bounds_layout_sections[1] if len(bounds_layout_sections) == 2 else ""
    )
    bounds_layout_required_evidence = (
        "All four Make gates",
        "push run `27394309114`",
        "pull-request run `27394315070`",
        "push run `27394330649`",
        "CodeQL setup run `27402322718`",
        "mutation restoring `frame`-based image sizing",
    )
    require(bounds_layout_statuses == ["status: completed"]
            and all(item in bounds_layout_verification for item in bounds_layout_required_evidence)
            and re.search(r"\b(?:pending|todo|tbd|not run)\b", bounds_layout_verification, re.IGNORECASE) is None,
            "bounds-based image layout plan must record completed status and actual verification",
            failures)
    require(workflow.count("permissions:\n  contents: read") == 1 and
            not re.search(r"(?m)^\s{2,}permissions:\s*$", workflow) and
            not re.search(r"(?m)^\s+[A-Za-z0-9_-]+:\s*write\s*$", workflow),
            "Check workflow must use one top-level read-only permissions block",
            failures)
    require("cancel-in-progress: true" in workflow and "runs-on: macos-15" in workflow and
            "timeout-minutes: 10" in workflow,
            "Check workflow must bound duplicate and long-running macOS jobs",
            failures)
    require(workflow.count("uses: actions/checkout@df4cb1c069e1874edd31b4311f1884172cec0e10") == 1 and
            "persist-credentials: false" in workflow and
            "run: make check" in workflow,
            "Check workflow must pin one credential-free checkout and run the canonical baseline",
            failures)

    if shutil.which("xcodebuild"):
        run(["xcodebuild", "-list", "-project", "iHeartRating.xcodeproj"],
            failures, "xcodebuild must parse iHeartRating.xcodeproj")
        run(["xcodebuild", "-list", "-project", "example/SampleApp/SampleApp.xcodeproj"],
            failures, "xcodebuild must parse the SampleApp project")
    else:
        print("xcodebuild unavailable; static iOS baseline only.")

    if failures:
        for failure in failures:
            print(failure, file=sys.stderr)
        return 1

    print("iHeartRating baseline checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
