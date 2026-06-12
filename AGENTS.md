# AGENTS.md

## Repository purpose

`garethpaul/iHeartRating` is an Apple platform application or Swift sample. Simple Ratings View for iOS enabling you to use any image as a rating e.g. hearts, stars, pigeons etc.

## Project structure

- `Makefile` - repository verification targets
- `scripts` - baseline checks and helper scripts
- `docs` - plans, notes, and generated README assets
- `iHeartRating.xcodeproj` - Xcode project
- `assets` - repository source or sample assets
- `example` - repository source or sample assets
- `iHeartRating` - repository source or sample assets
- `iHeartRatingTests` - repository source or sample assets
- `screenshots` - repository source or sample assets

## Development commands

- Install dependencies: no repository-specific install command is documented.
- Full baseline: `make check`
- Local Apple development: `open iHeartRating.xcodeproj`
- If a command above skips because a platform toolchain is missing, verify on a machine with that SDK before claiming platform behavior is tested.

## Coding conventions

- Language mix noted in the README: Swift (6), C/C++ headers (1), shell (1).
- Preserve legacy Xcode project settings and signing assumptions unless the change is explicitly about modernization.

## Testing guidance

- Test-related files detected: `example/SampleApp/SampleAppTests/SampleAppTests.swift`, `example/SampleApp/SampleAppUITests/SampleAppUITests.swift`, `iHeartRating.podspec`, `iHeartRating.xcodeproj/xcshareddata/xcschemes/iHeartRatingTests.xcscheme`, `iHeartRating/0.1.6/iHeartRating.podspec`, `iHeartRatingTests/iHeartRatingTests.swift`
- Start with the narrowest relevant test or Make target, then run `make check` before handing off if the change is not documentation-only.
- Keep README verification notes in sync when commands, fixtures, or supported toolchains change.

## PR / change guidance

- Keep diffs focused on the requested repository and avoid unrelated modernization or formatting churn.
- Preserve public APIs, sample behavior, file formats, and documented environment variables unless the task explicitly changes them.
- Update tests, README notes, or docs/plans when behavior, security posture, or validation commands change.
- Call out skipped platform validation, legacy toolchain assumptions, and any risky files touched in the final summary.

## Safety and gotchas

- No required secret or credential file was identified in the repository scan. If you add integrations later, keep secrets out of git.
- UI configuration changes should not crash on empty image arrays, single-rating views, zero-sized images, negative `minImageSize`, invalid `maxRating`, inconsistent rating bounds, or out-of-range ratings.
- Keep rating image layout in local bounds coordinates so transforms do not
  distort child geometry.
- This looks like an Apple platform project or sample. Xcode, Swift, CocoaPods, and deployment target versions may need to match the original project era.
- See `SECURITY.md` for vulnerability reporting and safe research guidance.
- See `VISION.md` for project direction and contribution guardrails.
- See `docs/plans/2026-06-08-bounce-without-delegate.md` for the bounce-without-delegate guardrail.

## Agent workflow

1. Inspect the README, Makefile, manifests, and the files directly related to the request.
2. Make the smallest source or docs change that satisfies the task; avoid generated, vendored, or local-environment files unless required.
3. Run the narrowest useful validation first, then `make check` or the documented package/platform gate when available.
4. If a required SDK, service credential, or external runtime is unavailable, record the skipped command and why.
5. Summarize changed files, commands run, and remaining risks or follow-up validation.
