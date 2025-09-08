#!/usr/bin/env python3
import argparse
import subprocess
import sys
import yaml


def main():
    """Check the verdict of a Litmus ChaosResult"""
    ap = argparse.ArgumentParser(description="Check Litmus ChaosResult verdict")
    ap.add_argument("-n", "--namespace", required=True, help="Kubernetes namespace")
    ap.add_argument("-r", "--name", required=True, help="ChaosResult name")
    args = ap.parse_args()

    # Run kubectl
    try:
        result = subprocess.run(
            ["kubectl", "get", "chaosresult", "-n", args.namespace, args.name, "-o", "yaml"],
            capture_output=True, text=True, check=True,
        )
    except subprocess.CalledProcessError as e:
        msg = (e.stderr or e.stdout or str(e)).strip()
        if "NotFound" in msg or "not found" in msg:
            print(f"[ERROR] ChaosResult '{args.name}' in namespace '{args.namespace}' not found")
        else:
            print(f"[ERROR] kubectl failed: {msg}")
        sys.exit(2)

    # Parse YAML
    try:
        data = yaml.safe_load(result.stdout)
    except yaml.YAMLError as e:
        print(f"[ERROR] failed to parse YAML: {e}")
        sys.exit(2)

    exp_status = (data or {}).get("status", {}).get("experimentStatus", {})
    phase = exp_status.get("phase")
    verdict = exp_status.get("verdict")

    # Require Completed + Pass (change condition if you only care about verdict)
    if phase == "Completed" and verdict == "Pass":
        print("ChaosResult verdict check passed")
    else:
        print(f"failed to meet condition (phase={phase}, verdict={verdict})")
        sys.exit(1)

    try:
        result = subprocess.run(
            ["kubectl", "get", "pod", "-n", args.namespace, "nginx-chaos-runner", "-o", "yaml"],
            capture_output=True, text=True, check=True,
        )
    except subprocess.CalledProcessError as e:
        msg = (e.stderr or e.stdout or str(e)).strip()
        if "NotFound" in msg or "not found" in msg:
            print(f"[ERROR] Pod 'nginx-chaos-runner' in namespace '{args.namespace}' not found")
        else:
            print(f"[ERROR] kubectl failed: {msg}")
        sys.exit(2)

    # Parse YAML
    try:
        data = yaml.safe_load(result.stdout)
    except yaml.YAMLError as e:
        print(f"[ERROR] failed to parse YAML: {e}")
        sys.exit(2)

    container_statuses = (data or {}).get("status", {}).get("containerStatuses", {})
    for cs in container_statuses:
        if cs.get("name") == "chaos-runner":
            state = cs.get("state", {})
            if "terminated" in state:
                term = state["terminated"]
                exit_code = term.get("exitCode")
                reason = term.get("reason", "")
                if int(exit_code) == 0 and reason == "Completed":
                    print("chaos-runner container exited successfully")
                else:
                    print(f"chaos-runner container failed to complete (exitCode={exit_code}, reason={reason})")
                    sys.exit(1)
            else:
                print("chaos-runner container is not terminated")
                sys.exit(1)


if __name__ == "__main__":
    main()
