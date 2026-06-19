#!/bin/sh

set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)

if ! command -v xcodebuild >/dev/null 2>&1 || ! command -v xcrun >/dev/null 2>&1; then
    echo "Xcode is required to run the iHeartRating build and test gate." >&2
    exit 127
fi

DERIVED_DATA=$(mktemp -d "${TMPDIR:-/tmp}/iHeartRating-derived.XXXXXX")
SAMPLE_DERIVED_DATA=$(mktemp -d "${TMPDIR:-/tmp}/iHeartRating-sample-derived.XXXXXX")
trap 'rm -rf "$DERIVED_DATA" "$SAMPLE_DERIVED_DATA"' EXIT HUP INT TERM

SIMULATOR_ID=${IOS_SIMULATOR_ID:-$(xcrun simctl list devices available -j | python3 -c '
import json, sys
devices = json.load(sys.stdin).get("devices", {})
for runtime in sorted(devices, reverse=True):
    for device in devices[runtime]:
        if device.get("isAvailable") and device.get("name", "").startswith("iPhone"):
            print(device["udid"])
            raise SystemExit(0)
raise SystemExit("no available iPhone simulator found")
')}
DESTINATION="platform=iOS Simulator,id=${SIMULATOR_ID}"

xcodebuild \
    -project "$ROOT/iHeartRating.xcodeproj" \
    -scheme iHeartRatingTests \
    -destination "$DESTINATION" \
    -derivedDataPath "$DERIVED_DATA" \
    CODE_SIGNING_ALLOWED=NO \
    test

GENERATED_HEADER=$(find "$DERIVED_DATA" -path '*/iHeartRating.framework/Headers/iHeartRating-Swift.h' -print -quit)
if [ -z "$GENERATED_HEADER" ]; then
    echo "Generated Objective-C compatibility header was not found." >&2
    exit 1
fi
grep -E '@property .*UIViewContentMode imageContentMode;' "$GENERATED_HEADER" >/dev/null
grep -E 'heartRatingView:.*didUpdate:\(float\)rating;' "$GENERATED_HEADER" >/dev/null
grep -E 'heartRatingView:.*isUpdating:\(float\)rating;' "$GENERATED_HEADER" >/dev/null

xcodebuild \
    -project "$ROOT/example/SampleApp/SampleApp.xcodeproj" \
    -scheme SampleApp \
    -destination "$DESTINATION" \
    -derivedDataPath "$SAMPLE_DERIVED_DATA" \
    CODE_SIGNING_ALLOWED=NO \
    build
