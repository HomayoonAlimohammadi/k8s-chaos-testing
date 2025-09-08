#!/bin/bash

set -a
. ../vars.env
set +a

kubectl apply -f fault.yaml
envsubst < engine.yaml | kubectl apply -f -
