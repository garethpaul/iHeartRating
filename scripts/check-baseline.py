#!/usr/bin/env python3
from pathlib import Path
import plistlib
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "docs/plans/2026-06-08-rating-baseline.md"


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
    require("if image.size.width <= 0 || image.size.height <= 0 || size.width <= 0 || size.height <= 0" in rating_view,
            "sizeForImage must guard zero-sized images and containers",
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
    plan = PLAN.read_text(encoding="utf-8") if PLAN.exists() else ""
    require("make check" in readme and "build.sh" in readme and "podspec" in readme,
            "README must document static verification, build script, and podspec expectations",
            failures)
    require("scripts/check-baseline.py" in vision and "rating" in vision.lower(),
            "VISION must describe baseline validation for rating behavior",
            failures)
    require("malformed configuration" in security and "make check" in security,
            "SECURITY must document configuration hardening and verification",
            failures)
    require("zero-size" in changes and "podspec" in changes,
            "CHANGES must record rating edge-case and podspec updates",
            failures)
    require("status: completed" in plan,
            "plan must be marked completed",
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
