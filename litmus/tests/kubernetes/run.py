import subprocess
import sys
import os
from pathlib import Path
import argparse


def run_script(script_path, test_name):
    """Run a script and return success status"""
    os.chdir(script_path.parent)
    try:
        result = subprocess.run(
            [script_path],
            text=True,
            timeout=300,
            stdout=sys.stdout,
            stderr=sys.stderr,
        )
        if result.returncode == 0:
            print(f"✓ {test_name}: {script_path.name} passed")
            return True
        else:
            print(f"✗ {test_name}: {script_path.name} failed")
            print(f"  Error: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print(f"✗ {test_name}: {script_path.name} timed out")
        return False
    except Exception as e:
        print(f"✗ {test_name}: {script_path.name} error - {e}")
        return False
    
def main(args):
    if args.cleanup:
        print("Running cleanup")
        cleanup(args)
    else:
        run_tests(args)

def cleanup(args):
    current_dir = Path(__file__).parent
    
    for test_dir in current_dir.iterdir():
        if not test_dir.is_dir():
            continue
            
        test_name = test_dir.name
        if test_name == "util":
            continue
        if test_name != "docker-service-kill": # TODO: remove
            print(f"⚠ Skipping cleanup: {test_name}")
            continue
        print(f"\nRunning cleanup: {test_name}")

        run_script(test_dir / 'cleanup.sh', test_name)


def run_tests(args):
    current_dir = Path(__file__).parent
    test_results = {}
    
    for test_dir in current_dir.iterdir():
        if not test_dir.is_dir():
            continue
            
        test_name = test_dir.name
        if test_name == "util":
            continue
        if test_name != "docker-service-kill": # TODO: remove
            print(f"⚠ Skipping test: {test_name}")
            continue
        print(f"\nRunning test: {test_name}")
        
        scripts = ['run.sh', 'verify.sh', 'cleanup.sh']
        test_passed = True
        
        for script_name in scripts:
            script_path = test_dir / script_name
            if script_path.exists():
                success = run_script(script_path, test_name)
                if not success:
                    test_passed = False
                    break  # Stop on first failure
            else:
                print(f"⚠ {test_name}: {script_name} not found")
                test_passed = False
                break
        
        test_results[test_name] = test_passed
    
    # Summary
    print("\n" + "="*50)
    print("TEST SUMMARY")
    print("="*50)
    
    passed_tests = [name for name, passed in test_results.items() if passed]
    failed_tests = [name for name, passed in test_results.items() if not passed]
    
    print(f"Total tests: {len(test_results)}")
    print(f"Passed: {len(passed_tests)}")
    print(f"Failed: {len(failed_tests)}")
    
    if passed_tests:
        print(f"\nPassed tests: {', '.join(passed_tests)}")
    
    if failed_tests:
        print(f"\nFailed tests: {', '.join(failed_tests)}")
        sys.exit(1)
    
    print("\nAll tests passed!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run Kubernetes chaos tests')
    parser.add_argument('--cleanup', action='store_true', 
                       help='Only run cleanup scripts')
    args = parser.parse_args()
    main(args)
