#!/bin/bash

DIR_NAME=$(basename "$(pwd)")

sudo rm /etc/systemd/system/docker.service
kubectl delete -f fault.yaml
kubectl delete -f engine.yaml
kubectl delete chaosresults nginx-chaos-$DIR_NAME -n litmus
