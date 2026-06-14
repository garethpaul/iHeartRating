# Image Content Mode Propagation

status: completed

## Context

`HeartRatingView` applies `imageContentMode` only while image views are first
created. Updating the property later leaves all existing empty and full image
views on the previous mode, so the configured view state and rendered children
diverge.

## Priority

This is a narrow reusable-view consistency defect. The fix should update the
already-created image views without changing rating, touch, animation, or image
layout behavior.

## Scope

1. Propagate every `imageContentMode` assignment to existing empty and full
   image views.
2. Request layout after propagation so geometry can respond to the new mode.
3. Add an XCTest covering both halves of every existing image pair.
4. Add mutation-sensitive static and plan contracts plus synchronized guidance.

## Verification Plan

- Run all four Make gates from the checkout and through the absolute Makefile
  path from an external directory.
- Run checker compilation, `build.sh` syntax, and both podspec syntax checks.
- Reject mutations that remove content-mode propagation, its XCTest, plan
  completion, or recorded evidence.
- Inspect the exact diff, generated artifacts, and changed lines for secrets.

## Risk And Rollback

The change only updates existing child `UIImageView.contentMode` values and
requests layout. Rollback restores initialization-only behavior; no persisted
data or network behavior is involved.

## Work Completed

- Added an `imageContentMode` property observer that updates all existing empty
  and full image views and requests layout.
- Added an XCTest that verifies all ten default image views adopt the changed
  content mode.
- Added static implementation, test, documentation, and completed-plan
  contracts plus synchronized maintenance guidance.

## Verification Completed

- All four Make gates passed in an isolated completed-plan preflight copy and
  again in the implementation worktree.
- The absolute Makefile check passed from an external directory.
- `python3 -m py_compile scripts/check-baseline.py` passed; its exact generated
  bytecode path was removed before the final artifact audit.
- `sh -n build.sh` passed.
- Both podspec syntax checks passed with `ruby -c`.
- Four isolated hostile mutations were rejected: removing either propagation
  loop, removing the observer layout request, and removing XCTest discovery.
- `git diff --check` passed, along with exact intended-path, generated-artifact,
  changed-line secret, dependency, vendored-file, project, and workflow audits.
- Local `xcodebuild` was unavailable on Linux; no full Swift 2 compile or
  simulator execution is claimed.
