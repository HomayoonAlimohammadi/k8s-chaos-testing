#!/bin/bash

kubectl apply -f ../rbac/superuser.yaml
kubectl apply -f ../operator/crds.yaml
kubectl apply -f ../operator/operator.yaml
