HACK_DIR := hack
TESTS_DIR := tests
K8S_TESTS_DIR := $(TESTS_DIR)/kubernetes

.PHONY: setup
setup:
	cd $(HACK_DIR) && ./setup.sh

.PHONY: cleanup
cleanup:
	cd $(HACK_DIR) && ./cleanup.sh

.PHONY: all
all: k8s-tests

.PHONY: k8s-tests
k8s-tests: setup
	cd $(K8S_TESTS_DIR) && python3 run.py

