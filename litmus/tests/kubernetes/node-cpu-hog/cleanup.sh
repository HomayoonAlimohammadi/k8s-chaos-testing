#!/bin/bash

kubectl delete -f fault.yaml
kubectl delete -f engine.yaml
kubectl delete chaosresults nginx-chaos-node-cpu-hog -n litmus
