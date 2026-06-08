## iHeartRating Vision

iHeartRating is an iOS rating view library that lets apps use custom images for
rating controls.

The repository is useful as a small Swift library with a podspec, sample usage,
screenshots, and tests. Project setup and examples live in [`README.md`](README.md).

The goal is to keep the component simple, reusable, and predictable for app
developers.

The current focus is:

Priority:

- Preserve the image-based rating view API
- Keep delegate callbacks for updating and completed rating changes clear
- Maintain podspec and sample app alignment
- Avoid growing the library beyond focused rating behavior

Next priorities:

- Document supported rating ranges, half-step behavior, and customization options
- Modernize Swift/project settings in a dedicated pass
- Add tests for rating calculations and delegate calls
- Clarify package-manager support if revived

Contribution rules:

- One PR = one focused API, test, sample, or documentation change.
- Keep the library lightweight and dependency-free.
- Run the build script or Xcode tests before pushing behavior changes.
- Preserve API compatibility for consumers where possible.

## Security

This UI component has low security risk, but it should not crash on malformed
configuration or unexpected image assets.

## What We Will Not Merge (For Now)

- Broad UI frameworks unrelated to rating controls
- API-breaking changes without migration notes
- Package metadata changes without verification
- Behavior changes without tests or sample updates
