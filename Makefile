.PHONY: __repository-make-authority build check lint test xcode-test
.SECONDEXPANSION:

ifneq ($(strip $(MAKEFILES)),)
$(error MAKEFILES must be empty; repository verification requires this Makefile to be loaded alone)
endif
override MAKEFILES :=
ifneq ($(origin MAKEFILE_LIST),file)
$(error MAKEFILE_LIST must not be overridden)
endif
override ROOT := $(shell sed_path=/usr/bin/sed; [ -x "$$sed_path" ] || sed_path=/bin/sed; [ -x "$$sed_path" ] || exit 1; path=$$(printf '%s' '$(subst ','"'"',$(value MAKEFILE_LIST))' | "$$sed_path" 's/^ //'); [ -f "$$path" ] || exit 1; directory=$${path%/*}; [ "$$directory" != "$$path" ] || directory=.; CDPATH= cd -- "$$directory" && /bin/pwd -P)
export ROOT
ifeq ($(strip $(ROOT)),)
$(error repository Makefile must be loaded alone)
endif

build check lint test xcode-test:: $$(if $$(filter file,$$(origin MAKEFILE_LIST)),,$$(error MAKEFILE_LIST must not be overridden))
build check lint test xcode-test:: $$(if $$(shell sed_path=/usr/bin/sed && [ -x "$$$$sed_path" ] || sed_path=/bin/sed && [ -x "$$$$sed_path" ] && path=$$$$(printf '%s' '$$(subst ','"'"',$$(MAKEFILE_LIST))' | "$$$$sed_path" 's/^ //') && [ -f "$$$$path" ] && printf '%s' ok),,$$(error repository Makefile must be loaded alone))
build check lint test xcode-test:: __repository-make-authority

__repository-make-authority::
	@:

lint test build:: check

xcode-test::
	@"$(ROOT)/build.sh"

check::
	@python3 "$(ROOT)/scripts/check-baseline.py"
	@python3 "$(ROOT)/scripts/test-make-spaced-path.py"
