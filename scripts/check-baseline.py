#!/usr/bin/env python3

from __future__ import annotations

import ast
import plistlib
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def require(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def run(command: list[str], message: str, failures: list[str]) -> None:
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    if result.returncode != 0:
        failures.append(f"{message}: {result.stderr.strip() or result.stdout.strip()}")


def main() -> int:
    failures: list[str] = []
    source = read("iHeartRating/iHeartRatingView.swift")
    tests = read("iHeartRatingTests/iHeartRatingTests.swift")
    library_project = read("iHeartRating.xcodeproj/project.pbxproj")
    sample_project = read("example/SampleApp/SampleApp.xcodeproj/project.pbxproj")
    makefile = read("Makefile")
    build_script = read("build.sh")
    workflow = read(".github/workflows/check.yml")
    podspec = read("iHeartRating.podspec")

    require(
        "@objcMembers" in source and "open class HeartRatingView: UIView" in source,
        "HeartRatingView must preserve Objective-C exposure and external subclassing",
        failures,
    )
    require(
        "@objc(heartRatingView:didUpdate:)" in source
        and "@objc(heartRatingView:isUpdating:)" in source,
        "delegate selectors must remain stable for Objective-C consumers",
        failures,
    )
    require("public weak var delegate" in source, "delegate ownership must remain weak", failures)
    require(
        "public var imageContentMode: UIView.ContentMode" in source
        and source.count("$0.contentMode = imageContentMode") == 2,
        "public image content mode must propagate to both child image sets",
        failures,
    )
    require(
        "public override var intrinsicContentSize" in source
        and source.count("invalidateIntrinsicContentSize()") >= 4,
        "image, count, and minimum-size changes must invalidate intrinsic sizing",
        failures,
    )
    require(
        "private func finiteNonnegative" in source
        and "private static let maximumSafeDimension" in source
        and "maximumImageWidth" in source
        and "maskWidth" in source,
        "layout and mask geometry must pass through finite bounded normalization",
        failures,
    )
    require(
        "let maximumImageWidth = desiredImageWidth" in source
        and "testOversizedMinimumImageWidthDoesNotOverlapRatingFrames" in tests,
        "constrained rating image frames must not overlap when minimum width exceeds a slot",
        failures,
    )
    require(
        "guard emptyImage != nil, fullImage != nil" in source
        and "layer.mask = nil" in source
        and "isHidden = true" in source,
        "incomplete image pairs must fail closed and clear stale masks",
        failures,
    )
    require(
        "public override func accessibilityIncrement()" in source
        and "public override func accessibilityDecrement()" in source
        and "let adjustedRating = boundedRating(rating + delta)" in source
        and "guard adjustedRating != rating else" in source
        and "rating = adjustedRating" in source
        and "accessibilityTraits = editable ? [.adjustable] : [.staticText]" in source
        and 'accessibilityLabel = "Rating"' in source
        and "if accessibilityLabel == nil" in source,
        "the rating control must expose synchronized adjustable accessibility state",
        failures,
    )
    require(
        "guard editable, emptyImage != nil, fullImage != nil" in source
        and "guard editable, let touch = touches.first" in source
        and "guard editable, !touches.isEmpty" in source,
        "touch handling must reject invisible, noneditable, and empty interactions",
        failures,
    )

    required_tests = [
        "testMinimumImageSizeNormalizesEachInvalidDimension",
        "testMaximumRatingCountIsBoundedBeforeAllocatingImageViews",
        "testSizeForImageRejectsNonFiniteAndNonPositiveContainers",
        "testExtremeMinimumImageSizeStillProducesFiniteBoundedFrames",
        "testRepeatedLayoutKeepsPartialMaskFiniteAndStable",
        "testIntrinsicContentSizeTracksImagesCountAndMinimumSize",
        "testIncompleteImagePairHasNoIntrinsicSizeAndHidesOverlays",
        "testImageContentModePropagatesAndSurvivesImageViewReplacement",
        "testAccessibilityStateTracksRatingAndEditability",
        "testAccessibilityAdjustmentsNotifyOnlyWhenRatingChanges",
    ]
    for test_name in required_tests:
        require(f"func {test_name}()" in tests, f"missing focused XCTest {test_name}", failures)

    require(
        "private static let maximumRatingCount = 100" in source
        and "min(max(maxRating, 1), Self.maximumRatingCount)" in source,
        "maxRating must be bounded before child image view allocation",
        failures,
    )

    require(library_project.count("SWIFT_VERSION = 5.0;") == 4, "library and test targets must pin Swift 5", failures)
    require(sample_project.count("SWIFT_VERSION = 5.0;") == 6, "sample targets must pin Swift 5", failures)
    require(
        "IPHONEOS_DEPLOYMENT_TARGET = 9." not in library_project
        and "IPHONEOS_DEPLOYMENT_TARGET = 9." not in sample_project,
        "projects must not claim deployment targets unsupported by hosted Xcode",
        failures,
    )
    require('s.version      = "0.2.0"' in podspec, "podspec version must distinguish the Swift 5 platform update", failures)
    require('s.platform     = :ios, "12.0"' in podspec, "podspec must match the tested iOS deployment target", failures)
    require('s.swift_version = "5.0"' in podspec, "podspec must declare its Swift language version", failures)

    require("override ROOT := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))" in makefile, "Make targets must be location independent", failures)
    require(
        re.search(r"(?m)^xcode-test:\s*$", makefile) is not None
        and '"$(ROOT)/build.sh"' in makefile,
        "Makefile must expose the executable Xcode gate",
        failures,
    )
    require("mktemp -d" in build_script and "iHeartRating-Swift.h" in build_script, "Xcode gate must clean temporary output and inspect Objective-C API", failures)
    require("SampleApp.xcodeproj" in build_script and "iHeartRatingTests" in build_script, "Xcode gate must build the sample and run library tests", failures)

    require(workflow.count("permissions:\n  contents: read") == 1, "workflow permissions must stay read-only", failures)
    require("persist-credentials: false" in workflow, "checkout credentials must not persist", failures)
    require("run: make check" in workflow and "run: make xcode-test" in workflow, "hosted checks must execute static and Xcode gates", failures)
    require("timeout-minutes: 20" in workflow, "hosted Xcode execution must remain time bounded", failures)
    require(not re.search(r"(?m)^\s+[A-Za-z0-9_-]+:\s*write\s*$", workflow), "workflow must not gain write permissions", failures)

    for relative_path in [
        "iHeartRating/Info.plist",
        "iHeartRatingTests/Info.plist",
        "example/SampleApp/SampleApp/Info.plist",
        "example/SampleApp/SampleAppTests/Info.plist",
        "example/SampleApp/SampleAppUITests/Info.plist",
    ]:
        try:
            with (ROOT / relative_path).open("rb") as plist_file:
                plistlib.load(plist_file)
        except Exception as error:
            failures.append(f"invalid plist {relative_path}: {error}")

    for relative_path in [
        "example/SampleApp/SampleApp/Base.lproj/Main.storyboard",
        "example/SampleApp/SampleApp/Base.lproj/LaunchScreen.storyboard",
    ]:
        try:
            ET.parse(ROOT / relative_path)
        except Exception as error:
            failures.append(f"invalid storyboard {relative_path}: {error}")

    run(["ruby", "-c", str(ROOT / "iHeartRating.podspec")], "root podspec syntax check failed", failures)
    run(["sh", "-n", str(ROOT / "build.sh")], "build script syntax check failed", failures)
    try:
        ast.parse(Path(__file__).read_text(encoding="utf-8"))
    except SyntaxError as error:
        failures.append(f"baseline checker syntax check failed: {error}")

    if shutil.which("xcodebuild"):
        run(
            ["xcodebuild", "-list", "-project", str(ROOT / "iHeartRating.xcodeproj")],
            "xcodebuild could not parse iHeartRating.xcodeproj",
            failures,
        )
        run(
            ["xcodebuild", "-list", "-project", str(ROOT / "example/SampleApp/SampleApp.xcodeproj")],
            "xcodebuild could not parse SampleApp.xcodeproj",
            failures,
        )
    else:
        print("xcodebuild unavailable; executable iOS validation requires make xcode-test on macOS.")

    if failures:
        print("\n".join(failures), file=sys.stderr)
        return 1

    print("iHeartRating baseline checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
