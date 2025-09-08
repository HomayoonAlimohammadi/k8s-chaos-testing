#!/bin/bash

for i in {1..60}; do
  if kubectl get nodes --no-headers | grep -v " Ready " | grep -q .; then
    echo "Some nodes are not ready... ($i/30)"
    sleep 5
  else
    echo "All nodes are ready"
    break
  fi
done
