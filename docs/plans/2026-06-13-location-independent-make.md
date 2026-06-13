# Location-Independent iHeartRating Verification

status: planned

## Context

Absolute Makefile invocations resolve the maintained checker relative to the
caller instead of the checkout.

## Scope

1. Derive the checkout root from `MAKEFILE_LIST`.
2. Invoke the Python checker through its rooted path.
3. Add completed-plan, external-run, guidance, and mutation contracts.
4. Preserve Swift, tests, project, podspec, build script, and workflow files.

## Verification Plan

- Run all four Make gates from the checkout and a temporary directory.
- Run checker compilation, shell/podspec syntax, XML/plist parsing, and diff checks.
- Reject root, checker, plan status/evidence, and documentation mutations.
- Inspect intended paths, secrets, and generated artifacts.

## Work Completed

Pending implementation.

## Verification Completed

Pending implementation and validation.

## Risk And Rollback

Verification path resolution only; rollback restores the relative recipe.
