#!/usr/bin/env python3
"""
Device Detection Test for Face-Gen
Tests the device detection system in different environments
"""

import os
import sys
import subprocess
import time

# Add the parent directory to the path so we can import app modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_device_detection():
    """Test the device detection system"""
    print("Face-Gen Device Detection Test")
    print("=" * 40)
    
    try:
        # Import and test device detection
        from app.scripts.device_detection import get_device_info
        
        device_info = get_device_info()
        
        print("PASS: Device detection test")
        print(f"Optimal device: {device_info['optimal_device']}")
        
        return True
    except Exception as e:
        print(f"FAIL: Device detection test - {e}")
        return False

def test_environment_compatibility():
    """Test environment compatibility"""
    print("\nEnvironment Compatibility Test")
    print("-" * 30)
    
    # Test Docker environment detection
    docker_env = os.path.exists('/.dockerenv')
    print(f"Docker Environment: {'Yes' if docker_env else 'No'}")
    
    # Test MPS availability
    try:
        import torch
        mps_available = torch.backends.mps.is_available()
        print(f"MPS Available: {'Yes' if mps_available else 'No'}")
    except Exception as e:
        print(f"MPS Test Failed: {e}")
    
    # Test CUDA availability
    try:
        import torch
        cuda_available = torch.cuda.is_available()
        print(f"CUDA Available: {'Yes' if cuda_available else 'No'}")
    except Exception as e:
        print(f"CUDA Test Failed: {e}")
    
    return True

def test_performance_comparison():
    """Test performance comparison between devices"""
    print("\nPerformance Comparison Test")
    print("-" * 30)
    
    devices = ['cpu', 'mps', 'cuda']
    results = {}
    
    for device in devices:
        try:
            import torch
            if device == 'mps' and not torch.backends.mps.is_available():
                print(f"SKIP: {device.upper()} (not available)")
                continue
            elif device == 'cuda' and not torch.cuda.is_available():
                print(f"SKIP: {device.upper()} (not available)")
                continue
            
            # Simple performance test
            start_time = time.time()
            
            if device == 'cpu':
                tensor = torch.randn(1000, 1000)
                result = torch.mm(tensor, tensor)
            elif device == 'mps':
                tensor = torch.randn(1000, 1000).to('mps')
                result = torch.mm(tensor, tensor)
                result = result.cpu()
            elif device == 'cuda':
                tensor = torch.randn(1000, 1000).to('cuda')
                result = torch.mm(tensor, tensor)
                result = result.cpu()
            
            end_time = time.time()
            results[device] = end_time - start_time
            
            print(f"PASS: {device.upper()} - {results[device]:.3f} seconds")
            
        except Exception as e:
            print(f"FAIL: {device.upper()} test - {e}")
    
    # Compare results
    if len(results) > 1:
        print("\nPerformance Comparison:")
        fastest = min(results, key=results.get)
        for device, time_taken in results.items():
            ratio = time_taken / results[fastest]
            print(f"   {device.upper()}: {ratio:.2f}x slower than {fastest.upper()}")
    
    return True

def main():
    """Main test function"""
    print("Face-Gen Device Detection Test Suite")
    print("=" * 50)
    
    tests = [
        ("Device Detection", test_device_detection),
        ("Environment Compatibility", test_environment_compatibility),
        ("Performance Comparison", test_performance_comparison)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"CRASH: {test_name} test - {e}")
            results.append((test_name, False))
    
    # Summary
    print("\nTest Summary")
    print("=" * 20)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("All tests passed! Device detection is working correctly.")
    else:
        print("Some tests failed. Check the output above for details.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 