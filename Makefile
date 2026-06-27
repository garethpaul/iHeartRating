.PHONY: build check lint test xcode-test

override empty :=
override space := $(empty) $(empty)
override makefile_space := __IHEARTRATING_MAKEFILE_SPACE__
override encoded_makefile_list := $(patsubst $(makefile_space)%,%,$(subst $(space),$(makefile_space),$(MAKEFILE_LIST)))
override ROOT := $(subst $(makefile_space),$(space),$(abspath $(dir $(lastword $(encoded_makefile_list)))))

lint test build: check

xcode-test:
	@"$(ROOT)/build.sh"

check:
	@python3 "$(ROOT)/scripts/check-baseline.py"
	@python3 "$(ROOT)/scripts/test-make-spaced-path.py"
