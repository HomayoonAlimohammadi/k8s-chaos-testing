#!/bin/bash

set -euo pipefail

set -a
. ../vars.env
set +a

../util/nodes-ready.sh

kubectl apply -f fault.yaml
envsubst < engine.yaml | kubectl apply -f -
