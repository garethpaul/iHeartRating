# Hosted Project Validation

status: completed

## Context

The static baseline covered source, package metadata, project inventory, and
rating-view guardrails, but it only printed a reminder when Xcode was present.
The repository also relied on a legacy Travis/Xcode 7.3 declaration with no
current hosted project-file check.

## Completed Scope

- Added a pinned GitHub Actions workflow with read-only repository permissions.
- Runs the canonical `make check` gate on a bounded `macos-15` job.
- Parses both the library and SampleApp Xcode projects when Xcode is available.
- Kept full Swift 2 compilation and simulator testing tied to Xcode 7.3 and its
  compatible runtime rather than claiming current-Xcode support.
- Extended the checker and documentation to preserve the CI contract.

## Verification

- `python3 scripts/check-baseline.py`
- `make check`
- workflow YAML parse
- `git diff --check`
