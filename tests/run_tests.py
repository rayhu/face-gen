#!/usr/bin/env python3
"""
Face-Gen Test Runner
Runs all tests in the tests folder
"""

import os
import sys
import subprocess
import importlib.util
from pathlib import Path

def run_test_file(test_file):
    """Run a single test file"""
    print(f"\n🧪 Running {test_file}...")
    print("-" * 50)
    
    try:
        # Run the test file
        result = subprocess.run([
            sys.executable, test_file
        ], capture_output=True, text=True, cwd=os.path.dirname(test_file))
        
        if result.returncode == 0:
            print(f"✅ {test_file} passed")
            return True
        else:
            print(f"❌ {test_file} failed")
            print(f"Error: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ {test_file} crashed: {e}")
        return False

def run_all_tests():
    """Run all test files in the tests folder"""
    print("🚀 Face-Gen Test Suite")
    print("=" * 50)
    
    # Get all test files
    tests_dir = Path(__file__).parent
    test_files = [
        "test_device_detection.py",
        "test_setup.py",
        "test_docker.py"
    ]
    
    results = []
    for test_file in test_files:
        test_path = tests_dir / test_file
        if test_path.exists():
            success = run_test_file(str(test_path))
            results.append((test_file, success))
        else:
            print(f"⚠️  {test_file} not found")
    
    # Summary
    print("\n📋 Test Summary")
    print("=" * 20)
    
    passed = 0
    total = len(results)
    
    for test_file, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{test_file}: {status}")
        if success:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
    else:
        print("⚠️  Some tests failed.")
    
    return passed == total

def run_specific_test(test_name):
    """Run a specific test"""
    tests_dir = Path(__file__).parent
    test_file = tests_dir / f"{test_name}.py"
    
    if test_file.exists():
        return run_test_file(str(test_file))
    else:
        print(f"❌ Test file {test_name}.py not found")
        return False

def main():
    """Main function"""
    if len(sys.argv) > 1:
        # Run specific test
        test_name = sys.argv[1]
        success = run_specific_test(test_name)
    else:
        # Run all tests
        success = run_all_tests()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main() 