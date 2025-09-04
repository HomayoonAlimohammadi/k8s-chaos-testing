.PHONY: setup
setup:
	./hack/setup.sh

.PHONY: cleanup
cleanup:
	./hack/cleanup.sh

.PHONY: run
run: k8s-tests

.PHONY: kubernetes
k8s-tests:
	python3 ./kubernetes/run.py

