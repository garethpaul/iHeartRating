# Image Content Mode Propagation

status: planned

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

Pending implementation.

## Verification Completed

Pending implementation and exact evidence.
