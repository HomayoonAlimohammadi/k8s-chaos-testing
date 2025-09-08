#!/bin/bash

echo "hi!"
kubectl delete -f ../operator -f ../rbac
