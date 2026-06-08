#!/bin/sh

set -eu

if ! command -v xcodebuild >/dev/null 2>&1; then
    echo "xcodebuild not found; install Xcode to run the iHeartRating test build." >&2
    exit 127
fi

ci_lib() {
    NAME="$1"
    xcodebuild -project iHeartRating.xcodeproj \
               -scheme "iHeartRatingTests" \
               -destination "platform=iOS Simulator,name=${NAME}" \
               -sdk iphonesimulator \
               build test
}

ci_lib "iPhone 5"
