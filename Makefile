SHELL := /bin/bash

.PHONY: help
help: ## Display this help.
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_0-9-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

.PHONY: all
all: help

##@ MacOS

.PHONY: build-venv
build-venv:	## Build virtual env from requirements.txt
	$(info Build virtual env..)
	pip install virtualenv
	virtualenv venv
	. venv/bin/activate
	pip install -r requirements.txt

.PHONY: start-venv
start-venv:	## Activate virtual env
	$(info Activate virtual env..)
	. venv/bin/activate

.PHONY: end-venv
end-venv:	## Deactivate virtual env
	$(info Deactivate virtual env..)
	deactivate