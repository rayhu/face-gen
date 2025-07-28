#!/usr/bin/env python3
"""
Docker Test Script for Face-Gen
Tests Docker deployment and compares performance with local environment
"""

import os
import subprocess
import time
import json

def run_command(command, description):
    """Run a command and return results"""
    print(f"🔄 {description}...")
    start_time = time.time()
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=300)
        end_time = time.time()
        
        return {
            'success': result.returncode == 0,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'time': end_time - start_time,
            'returncode': result.returncode
        }
    except subprocess.TimeoutExpired:
        return {
            'success': False,
            'stdout': '',
            'stderr': 'Command timed out after 5 minutes',
            'time': 300,
            'returncode': -1
        }
    except Exception as e:
        return {
            'success': False,
            'stdout': '',
            'stderr': str(e),
            'time': 0,
            'returncode': -1
        }

def test_local_environment():
    """Test local environment performance"""
    print("🧪 Testing Local Environment")
    print("-" * 30)
    
    # Test device detection
    device_result = run_command(
        "python app/scripts/device_detection.py",
        "Testing device detection"
    )
    
    if device_result['success']:
        print("✅ Device detection successful")
        print(f"⏱️  Time: {device_result['time']:.2f} seconds")
    else:
        print("❌ Device detection failed")
        print(f"Error: {device_result['stderr']}")
    
    return device_result

def test_docker_environment():
    """Test Docker environment performance"""
    print("\n🐳 Testing Docker Environment")
    print("-" * 30)
    
    # Build Docker image
    build_result = run_command(
        "docker build -t face-gen-test .",
        "Building Docker image"
    )
    
    if not build_result['success']:
        print("❌ Docker build failed")
        print(f"Error: {build_result['stderr']}")
        return None
    
    print("✅ Docker image built successfully")
    print(f"⏱️  Build time: {build_result['time']:.2f} seconds")
    
    # Test device detection in Docker
    docker_device_result = run_command(
        "docker run --rm face-gen-test python app/scripts/device_detection.py",
        "Testing device detection in Docker"
    )
    
    if docker_device_result['success']:
        print("✅ Docker device detection successful")
        print(f"⏱️  Time: {docker_device_result['time']:.2f} seconds")
    else:
        print("❌ Docker device detection failed")
        print(f"Error: {docker_device_result['stderr']}")
    
    return docker_device_result

def compare_performance(local_result, docker_result):
    """Compare local vs Docker performance"""
    print("\n📊 Performance Comparison")
    print("-" * 30)
    
    if local_result and docker_result:
        print(f"Local Environment: {local_result['time']:.2f} seconds")
        print(f"Docker Environment: {docker_result['time']:.2f} seconds")
        
        if local_result['time'] > 0 and docker_result['time'] > 0:
            ratio = docker_result['time'] / local_result['time']
            print(f"Performance Ratio: {ratio:.2f}x (Docker/Local)")
            
            if ratio > 2:
                print("⚠️  Docker is significantly slower (expected due to no MPS)")
            elif ratio > 1.5:
                print("⚠️  Docker is slower (expected)")
            else:
                print("✅ Performance is acceptable")
    
    print("\n💡 Recommendations:")
    print("• Local environment: Best for development and testing")
    print("• Docker environment: Best for deployment and consistency")
    print("• MPS acceleration: Only available in local environment")

def test_docker_app():
    """Test the full Docker application"""
    print("\n🌐 Testing Docker Application")
    print("-" * 30)
    
    # Start Docker container
    start_result = run_command(
        "docker run -d --name face-gen-test-app -p 5000:5000 face-gen-test",
        "Starting Docker container"
    )
    
    if not start_result['success']:
        print("❌ Failed to start Docker container")
        return False
    
    print("✅ Docker container started")
    
    # Wait for app to start
    time.sleep(10)
    
    # Test application status
    status_result = run_command(
        "curl -s http://localhost:5000/status",
        "Testing application status"
    )
    
    if status_result['success']:
        try:
            status_data = json.loads(status_result['stdout'])
            print("✅ Application is running")
            print(f"Status: {status_data}")
        except json.JSONDecodeError:
            print("⚠️  Status response is not valid JSON")
    else:
        print("❌ Application status check failed")
    
    # Clean up
    cleanup_result = run_command(
        "docker stop face-gen-test-app && docker rm face-gen-test-app",
        "Cleaning up Docker container"
    )
    
    if cleanup_result['success']:
        print("✅ Docker container cleaned up")
    else:
        print("⚠️  Failed to clean up Docker container")
    
    return status_result['success']

def main():
    """Main test function"""
    print("🎭 Face-Gen Docker Test Suite")
    print("=" * 40)
    
    # Test local environment
    local_result = test_local_environment()
    
    # Test Docker environment
    docker_result = test_docker_environment()
    
    # Compare performance
    compare_performance(local_result, docker_result)
    
    # Test full application
    app_success = test_docker_app()
    
    print("\n📋 Test Summary")
    print("=" * 20)
    print(f"Local Environment: {'✅ Pass' if local_result and local_result['success'] else '❌ Fail'}")
    print(f"Docker Environment: {'✅ Pass' if docker_result and docker_result['success'] else '❌ Fail'}")
    print(f"Docker Application: {'✅ Pass' if app_success else '❌ Fail'}")
    
    if local_result and docker_result and app_success:
        print("\n🎉 All tests passed! Docker deployment is ready.")
    else:
        print("\n⚠️  Some tests failed. Check the output above for details.")

if __name__ == "__main__":
    main() 