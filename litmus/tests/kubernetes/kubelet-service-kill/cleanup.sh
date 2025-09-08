#!/bin/bash

sudo rm /etc/systemd/system/kubelet.service
kubectl delete -f fault.yaml
kubectl delete -f engine.yaml
kubectl delete chaosresults nginx-chaos-kubelet-service-kill -n litmus
