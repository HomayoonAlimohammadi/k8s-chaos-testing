#!/bin/bash

DIR_NAME=$(basename "$(pwd)")

kubectl delete -f fault.yaml
kubectl delete -f engine.yaml
kubectl delete chaosresults nginx-chaos-$DIR_NAME -n litmus
