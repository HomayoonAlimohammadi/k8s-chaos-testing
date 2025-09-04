#!/bin/bash

set -euo pipefail

TRIES=100
SLEEP=5

for ((i=1; i<=TRIES; i++)); do
  echo "[$i/$TRIES] Verifying..."
  if python3 ../util/check_result.py --name nginx-chaos-docker-service-kill --namespace litmus; then
    echo "Success!"
    exit 0
  fi
  if (( i < TRIES )); then
    echo "Retrying in $SLEEP seconds..."
    sleep "$SLEEP"
  fi
done

echo "Failed after $TRIES attempts."
exit 1
