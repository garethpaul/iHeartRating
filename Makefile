.PHONY: build check lint test xcode-test

override ROOT := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))

lint test build: check

xcode-test:
	@"$(ROOT)/build.sh"

check:
	@python3 "$(ROOT)/scripts/check-baseline.py"
