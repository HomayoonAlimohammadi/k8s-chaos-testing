# Kubernetes Chaos Testing

This repository contains chaos engineering tools and tests for Kubernetes clusters, helping you validate the resilience and reliability of your Kubernetes deployments.

## Repository Structure

### `/litmus`
Contains Litmus-based chaos experiments for Kubernetes:
- **Setup & Configuration**: Scripts to install and configure Litmus operator
- **Kubernetes Tests**: Comprehensive suite of chaos experiments for pods, nodes, services, and storage
- **Test Framework**: Automated test runner with filtering and cleanup capabilities

## Getting Started

For detailed setup instructions and test execution guidance, see:
**[Litmus Testing Instructions](./litmus/INSTRUCTIONS.md)**

## Quick Start

1. **Prerequisites**: Ensure you have a Kubernetes 1.34-classic/stable cluster
2. **Setup**: `cd litmus && make setup`
3. **Run Tests**: `make all` or `cd tests/kubernetes && python3 run.py`

## Test Categories

- **Pod-level Chaos**: CPU/memory stress, network faults, container kills
- **Node-level Chaos**: Resource exhaustion, restarts, drains, taints
- **Service-level Chaos**: Critical service disruptions
- **Storage Chaos**: Disk space exhaustion

Future additions may include load testing and application-specific chaos experiments.
