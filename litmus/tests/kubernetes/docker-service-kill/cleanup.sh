#!/bin/bash

sudo rm /etc/systemd/system/docker.service
kubectl delete -f fault.yaml
kubectl delete -f engine.yaml
kubectl delete chaosresults nginx-chaos-docker-service-kill -n litmus
