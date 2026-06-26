# Accessibility Boundary No-op Design

Status: Approved

## Problem

Accessibility increment and decrement actions clamp the requested value to the valid rating range, but they still report a completed update and start a bounce animation when the rating is already at that boundary. Consumers therefore receive a duplicate update for an action that did not change control state.

## Options

1. Compute the bounded candidate and return when it equals the current rating. This keeps the existing callback and animation behavior for real changes while making boundary actions true no-ops.
2. Reassign the bounded value and separately gate the callback and animation. This produces the same visible behavior but performs unnecessary property work and obscures the no-op contract.
3. Preserve duplicate boundary feedback. This retains compatibility with the accidental behavior but conflicts with the delegate's completed-update meaning.

## Decision

Use option 1. Accessibility actions only notify the delegate and bounce when they change the bounded rating. Touch handling remains unchanged because it has a separate interaction contract.

## Verification

- Update the focused XCTest to exercise an increment at the maximum boundary and require only changed ratings in the delegate history.
- Extend the dependency-free baseline to require the explicit no-op guard.
- Run the portable baseline locally and the simulator suite in hosted macOS CI.
