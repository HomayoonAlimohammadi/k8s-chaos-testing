# Litmus Chaos Testing Instructions

## Prerequisites

### Kubernetes Cluster Requirements
- **Kubernetes Version**: 1.34-classic/stable
- **Cluster Configuration**: 
  - High Availability (HA) with 3 control planes is recommended
  - Most tests should work on a single node cluster as well
  - Default managed etcd
  - Default bootstrap configurations

## Setup

### 1. Install Litmus Operator
Run the setup script to install the Litmus operator and required CRDs:

```bash
cd litmus
make setup
```

This will execute [`litmus/hack/setup.sh`](./hack/setup.sh) which applies:
- RBAC configurations ([`rbac/superuser.yaml`](./rbac/superuser.yaml))
- Custom Resource Definitions ([`operator/crds.yaml`](./operator/crds.yaml))
- Litmus operator ([`operator/operator.yaml`](./operator/operator.yaml))

## Running Tests

### Test Categories
Currently supported:
- **Kubernetes Tests**: Chaos experiments for Kubernetes resources

Planned for future releases:
- Load tests
- Application tests

### Available Commands

#### Run All Tests
```bash
cd litmus
make all
```
or
```bash
cd litmus
make k8s-tests
```

#### Run Tests Directly
```bash
cd litmus/tests/kubernetes
python3 run.py
```

### Test Runner Options

The main test runner ([`litmus/tests/kubernetes/run.py`](./tests/kubernetes/run.py)) supports several options:

#### Run Specific Tests
```bash
python3 run.py --tests "pod-delete,node-restart,container-kill"
```

#### Cleanup Only Mode
Run cleanup scripts for tests without executing the actual tests:
```bash
python3 run.py --cleanup
```

#### Skip Cleanup
Run tests without executing cleanup scripts afterward:
```bash
python3 run.py --no-cleanup
```

## Test Configuration

Tests can be configured by modifying environment variables in [`litmus/tests/kubernetes/vars.env`](./tests/kubernetes/vars.env). This file contains configuration options for individual chaos experiments, including parameters like chaos duration, target nodes, CPU cores, and other test-specific settings. Edit the [`vars.env`](./tests/kubernetes/vars.env) file before running tests to customize the behavior of specific experiments.

## Test Structure

Each test directory under [`litmus/tests/kubernetes/`](./tests/kubernetes/) contains three main scripts that are executed in order:

1. **`run.sh`**: Executes the chaos experiment
2. **`verify.sh`**: Verifies the expected behavior and validates results
3. **`cleanup.sh`**: Cleans up resources created during the test

### Available Tests

The following chaos experiments are available:

**Pod-level Experiments:**
- `pod-delete` - Deletes pods randomly
- `pod-cpu-hog` - Consumes CPU resources on pods
- `pod-cpu-hog-exec` - CPU stress using exec method
- `pod-memory-hog` - Consumes memory resources on pods
- `pod-memory-hog-exec` - Memory stress using exec method
- `pod-io-stress` - Performs I/O stress on pods
- `pod-network-latency` - Introduces network latency
- `pod-network-loss` - Introduces packet loss
- `pod-network-corruption` - Corrupts network packets
- `pod-network-duplication` - Duplicates network packets
- `pod-network-partition` - Creates network partitions
- `pod-network-rate-limit` - Limits network bandwidth
- `pod-dns-error` - Introduces DNS resolution errors
- `pod-dns-spoof` - Spoofs DNS responses
- `pod-http-latency` - Introduces HTTP latency
- `pod-http-status-code` - Modifies HTTP status codes
- `pod-http-modify-body` - Modifies HTTP response bodies
- `pod-http-modify-header` - Modifies HTTP headers
- `pod-http-reset-peer` - Resets HTTP connections
- `pod-autoscaler` - Tests pod autoscaling behavior
- `container-kill` - Kills containers within pods

**Node-level Experiments:**
- `node-cpu-hog` - Consumes CPU resources on nodes
- `node-memory-hog` - Consumes memory resources on nodes
- `node-io-stress` - Performs I/O stress on nodes
- `node-restart` - Restarts nodes
- `node-poweroff` - Powers off nodes
- `node-drain` - Drains nodes
- `node-taint` - Applies taints to nodes

**Service-level Experiments:**
- `docker-service-kill` - Kills Docker service
- `kubelet-service-kill` - Kills kubelet service

**Storage Experiments:**
- `disk-fill` - Fills up disk space

## Test Execution Flow

1. **Setup Phase**: The setup script installs required Litmus components
2. **Test Execution**: For each selected test:
   - `run.sh` creates and applies chaos experiment
   - `verify.sh` checks if the experiment executed correctly
   - `cleanup.sh` removes experiment resources (unless `--no-cleanup` is used)
3. **Results**: Test runner provides a summary of passed/failed tests

## Cleanup

To cleanup Litmus operator and related resources:
```bash
cd litmus
make cleanup
```

This will execute [`litmus/hack/cleanup.sh`](./hack/cleanup.sh).

## Troubleshooting

- Ensure your cluster has sufficient resources for chaos experiments
- Check that the Litmus operator is running: `kubectl get pods -n litmus`
- Review test logs if experiments fail
- Use `--cleanup` mode to clean up stuck resources from previous test runs
