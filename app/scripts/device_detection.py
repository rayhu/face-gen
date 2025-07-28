#!/usr/bin/env python3
"""
Device Detection for Face-Gen
Automatically detects and configures the best available device for AI processing
"""

import os
import torch
import platform
import subprocess

def detect_environment():
    """Detect the current environment (Docker, local, cloud)"""
    # Check if running in Docker
    docker_env = os.path.exists('/.dockerenv')
    
    # Check if running in Kubernetes
    k8s_env = os.path.exists('/var/run/secrets/kubernetes.io/')
    
    # Check OS
    os_name = platform.system()
    os_version = platform.release()
    
    return {
        'docker': docker_env,
        'kubernetes': k8s_env,
        'os': os_name,
        'os_version': os_version,
        'architecture': platform.machine()
    }

def detect_mps_availability():
    """Detect MPS availability with detailed checks"""
    try:
        # Check if PyTorch supports MPS
        mps_available = torch.backends.mps.is_available()
        
        if not mps_available:
            return {
                'available': False,
                'reason': 'PyTorch MPS not available',
                'device': 'cpu'
            }
        
        # Check if we can actually use MPS
        try:
            test_tensor = torch.randn(1, 1).to('mps')
            test_result = test_tensor + test_tensor
            mps_working = True
        except Exception as e:
            mps_working = False
            mps_error = str(e)
        
        if mps_working:
            return {
                'available': True,
                'reason': 'MPS available and working',
                'device': 'mps'
            }
        else:
            return {
                'available': False,
                'reason': f'MPS available but not working: {mps_error}',
                'device': 'cpu'
            }
            
    except Exception as e:
        return {
            'available': False,
            'reason': f'MPS detection failed: {str(e)}',
            'device': 'cpu'
        }

def detect_cuda_availability():
    """Detect CUDA availability"""
    try:
        cuda_available = torch.cuda.is_available()
        if cuda_available:
            return {
                'available': True,
                'device': 'cuda',
                'count': torch.cuda.device_count(),
                'current': torch.cuda.current_device(),
                'name': torch.cuda.get_device_name(0)
            }
        else:
            return {
                'available': False,
                'device': 'cpu'
            }
    except Exception as e:
        return {
            'available': False,
            'device': 'cpu',
            'error': str(e)
        }

def get_optimal_device():
    """Get the optimal device for the current environment"""
    env_info = detect_environment()
    mps_info = detect_mps_availability()
    cuda_info = detect_cuda_availability()
    
    print("🔍 Device Detection Results:")
    print(f"   Environment: {'Docker' if env_info['docker'] else 'Local'}")
    print(f"   OS: {env_info['os']} {env_info['os_version']}")
    print(f"   Architecture: {env_info['architecture']}")
    print(f"   MPS: {'✅ Available' if mps_info['available'] else '❌ Not available'}")
    print(f"   CUDA: {'✅ Available' if cuda_info['available'] else '❌ Not available'}")
    
    # Priority order: MPS > CUDA > CPU
    if mps_info['available'] and not env_info['docker']:
        print("🎯 Using MPS (Apple Silicon GPU)")
        return 'mps'
    elif cuda_info['available']:
        print("🎯 Using CUDA (NVIDIA GPU)")
        return 'cuda'
    else:
        print("🎯 Using CPU (fallback)")
        return 'cpu'

def configure_device_for_model(model, device):
    """Configure a model for the specified device"""
    try:
        if device == 'mps':
            # Special handling for MPS
            model = model.to('mps')
            print("✅ Model moved to MPS device")
        elif device == 'cuda':
            # CUDA handling
            model = model.to('cuda')
            print("✅ Model moved to CUDA device")
        else:
            # CPU handling
            model = model.to('cpu')
            print("✅ Model moved to CPU device")
        
        return model
    except Exception as e:
        print(f"⚠️  Failed to move model to {device}, falling back to CPU: {e}")
        return model.to('cpu')

def get_device_info():
    """Get comprehensive device information"""
    env_info = detect_environment()
    mps_info = detect_mps_availability()
    cuda_info = detect_cuda_availability()
    optimal_device = get_optimal_device()
    
    return {
        'environment': env_info,
        'mps': mps_info,
        'cuda': cuda_info,
        'optimal_device': optimal_device,
        'recommendations': get_recommendations(env_info, mps_info, cuda_info)
    }

def get_recommendations(env_info, mps_info, cuda_info):
    """Get recommendations for optimal performance"""
    recommendations = []
    
    if env_info['docker']:
        recommendations.append("🐳 Running in Docker - MPS may not be available")
        recommendations.append("💡 Consider using host networking for better performance")
    
    if mps_info['available'] and not env_info['docker']:
        recommendations.append("🍎 Apple Silicon detected - MPS acceleration available")
        recommendations.append("⚡ Expect 2-5x performance improvement for large operations")
    
    if cuda_info['available']:
        recommendations.append("🟢 CUDA detected - GPU acceleration available")
        recommendations.append("🚀 Expect significant performance improvement")
    
    if not mps_info['available'] and not cuda_info['available']:
        recommendations.append("💻 CPU-only mode - Consider upgrading for better performance")
        recommendations.append("📈 Large operations may be slower")
    
    return recommendations

if __name__ == "__main__":
    print("🎭 Face-Gen Device Detection")
    print("=" * 40)
    
    device_info = get_device_info()
    
    print("\n📊 Summary:")
    print(f"   Optimal Device: {device_info['optimal_device'].upper()}")
    
    print("\n💡 Recommendations:")
    for rec in device_info['recommendations']:
        print(f"   • {rec}")
    
    print(f"\n🎯 Ready to use device: {device_info['optimal_device']}") 