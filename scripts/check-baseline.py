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
RATING_BOUNDS_PLAN = ROOT / "docs/plans/2026-06-08-rating-bounds.md"
BOUNCE_PLAN = ROOT / "docs/plans/2026-06-08-bounce-without-delegate.md"
NONEDITABLE_PLAN = ROOT / "docs/plans/2026-06-09-noneditable-touch-end.md"
EMPTY_TOUCH_PLAN = ROOT / "docs/plans/2026-06-09-empty-touch-end.md"
MIN_IMAGE_SIZE_PLAN = ROOT / "docs/plans/2026-06-09-min-image-size-guard.md"


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
        "docs/plans/2026-06-08-rating-bounds.md",
        "docs/plans/2026-06-08-bounce-without-delegate.md",
        "docs/plans/2026-06-09-noneditable-touch-end.md",
        "docs/plans/2026-06-09-empty-touch-end.md",
        "docs/plans/2026-06-09-min-image-size-guard.md",
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
    require("if minRating < 0" in rating_view and "if minRating > maxRating" in rating_view,
            "minRating must stay non-negative and not exceed maxRating",
            failures)
    require("self.rating = self.boundedRating(newRating)" in rating_view,
            "touch handling must reuse bounded rating normalization",
            failures)
    require("if image.size.width <= 0 || image.size.height <= 0 || size.width <= 0 || size.height <= 0" in rating_view,
            "sizeForImage must guard zero-sized images and containers",
            failures)
    require("if minImageSize.width < 0 || minImageSize.height < 0" in rating_view and
            "minImageSize = CGSize" in rating_view and "setNeedsLayout()" in rating_view,
            "minImageSize must be clamped to non-negative values and trigger layout",
            failures)
    require("let imageCount = self.emptyImageViews.count" in rating_view and "if imageCount == 0" in rating_view,
            "layoutSubviews must guard empty image arrays",
            failures)
    require("imageCount > 1 ?" in rating_view,
            "layoutSubviews must avoid dividing by imageCount - 1 for single-rating views",
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
    require(rating_view.count("if !self.editable") >= 2,
            "touch handling must ignore touchesEnded when the view is not editable",
            failures)
    require("if touches.isEmpty" in rating_view,
            "touchesEnded must ignore empty touch sets before delegate and bounce work",
            failures)
    require("testMaxRatingDoesNotStayBelowOne" in tests and "testZeroSizeImageReturnsZeroSize" in tests and
            "testRatingDoesNotExceedMaxRating" in tests and "testMinRatingDoesNotExceedMaxRating" in tests and
            "testMinImageSizeDoesNotStayNegative" in tests and
            "testTouchesEndedDoesNotNotifyWhenNotEditable" in tests and
            "testTouchesEndedDoesNotNotifyWithoutTouches" in tests,
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
    baseline_plan = BASELINE_PLAN.read_text(encoding="utf-8") if BASELINE_PLAN.exists() else ""
    rating_bounds_plan = RATING_BOUNDS_PLAN.read_text(encoding="utf-8") if RATING_BOUNDS_PLAN.exists() else ""
    bounce_plan = BOUNCE_PLAN.read_text(encoding="utf-8") if BOUNCE_PLAN.exists() else ""
    noneditable_plan = NONEDITABLE_PLAN.read_text(encoding="utf-8") if NONEDITABLE_PLAN.exists() else ""
    empty_touch_plan = EMPTY_TOUCH_PLAN.read_text(encoding="utf-8") if EMPTY_TOUCH_PLAN.exists() else ""
    min_image_size_plan = MIN_IMAGE_SIZE_PLAN.read_text(encoding="utf-8") if MIN_IMAGE_SIZE_PLAN.exists() else ""
    require("make check" in readme and "build.sh" in readme and "podspec" in readme and "delegate-independent bounce" in readme and "non-editable" in readme and "empty touch" in readme.lower() and "minImageSize" in readme,
            "README must document static verification, build script, and podspec expectations",
            failures)
    require("scripts/check-baseline.py" in vision and "rating" in vision.lower() and "bounce" in vision.lower() and "non-editable" in vision.lower() and "empty touch" in vision.lower() and "minImageSize" in vision,
            "VISION must describe baseline validation for rating behavior",
            failures)
    require("malformed configuration" in security and "make check" in security and "non-editable" in security and "empty touch" in security.lower() and "minImageSize" in security,
            "SECURITY must document configuration hardening and verification",
            failures)
    require("zero-size" in changes and "maxRating" in changes and "podspec" in changes and "rating bounds" in changes and "bounce" in changes and "not editable" in changes and "empty touch" in changes.lower() and "minImageSize" in changes,
            "CHANGES must record rating edge-case, rating bounds, and podspec updates",
            failures)
    require("status: completed" in baseline_plan and "status: completed" in rating_bounds_plan and "status: completed" in bounce_plan,
            "plans must be marked completed",
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

    if shutil.which("xcodebuild"):
        print("xcodebuild is available; run ./build.sh on macOS before release.")
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
