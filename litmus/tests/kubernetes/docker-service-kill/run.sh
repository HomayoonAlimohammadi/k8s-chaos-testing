#!/bin/bash

set -euo pipefail

set -a
. ../vars.env
set +a

../util/nodes-ready.sh

if [[ ! -e /etc/systemd/system/docker.service ]]; then
  sudo ln -s /etc/systemd/system/snap.k8s.containerd.service /etc/systemd/system/docker.service || true
  sudo systemctl daemon-reload
fi
kubectl apply -f fault.yaml
envsubst < engine.yaml | kubectl apply -f -
