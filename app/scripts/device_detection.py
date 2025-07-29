#!/usr/bin/env python3
"""
Device Detection for Face-Gen
Automatically detects and configures the best available device for AI processing
"""

import os
import platform
import torch
import psutil

def detect_environment():
    """
    Detect the current environment (Docker, local, OS, architecture)
    
    Returns:
        dict: Environment information
    """
    env_info = {
        'is_docker': os.path.exists('/.dockerenv'),
        'os': platform.system(),
        'architecture': platform.machine(),
        'python_version': platform.python_version(),
        'conda_env': os.environ.get('CONDA_DEFAULT_ENV', 'Not using conda')
    }
    return env_info

def detect_mps_availability():
    """
    Check if MPS (Metal Performance Shaders) is available
    
    Returns:
        dict: MPS availability information
    """
    mps_info = {
        'available': False,
        'functional': False,
        'reason': 'Not available'
    }
    
    try:
        # Check if PyTorch supports MPS
        if hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
            mps_info['available'] = True
            
            # Test if MPS actually works
            try:
                test_tensor = torch.randn(1, 1).to('mps')
                test_result = test_tensor + test_tensor
                mps_info['functional'] = True
                mps_info['reason'] = 'Available and functional'
            except Exception as e:
                mps_info['reason'] = f'Available but not functional: {str(e)}'
        else:
            mps_info['reason'] = 'PyTorch MPS not available'
            
    except Exception as e:
        mps_info['reason'] = f'Error checking MPS: {str(e)}'
    
    return mps_info

def detect_cuda_availability():
    """
    Check if CUDA is available
    
    Returns:
        dict: CUDA availability information
    """
    cuda_info = {
        'available': False,
        'functional': False,
        'reason': 'Not available'
    }
    
    try:
        if torch.cuda.is_available():
            cuda_info['available'] = True
            
            # Test if CUDA actually works
            try:
                test_tensor = torch.randn(1, 1).to('cuda')
                test_result = test_tensor + test_tensor
                cuda_info['functional'] = True
                cuda_info['reason'] = 'Available and functional'
            except Exception as e:
                cuda_info['reason'] = f'Available but not functional: {str(e)}'
        else:
            cuda_info['reason'] = 'PyTorch CUDA not available'
            
    except Exception as e:
        cuda_info['reason'] = f'Error checking CUDA: {str(e)}'
    
    return cuda_info

def get_optimal_device():
    """
    Determine the optimal device for the current environment
    
    Returns:
        str: Optimal device ('mps', 'cuda', or 'cpu')
    """
    env_info = detect_environment()
    mps_info = detect_mps_availability()
    cuda_info = detect_cuda_availability()
    
    # Priority: MPS > CUDA > CPU
    if mps_info['functional'] and not env_info['is_docker']:
        return 'mps'
    elif cuda_info['functional']:
        return 'cuda'
    else:
        return 'cpu'

def configure_device_for_model(model, device):
    """
    Move a PyTorch model to the specified device
    
    Args:
        model: PyTorch model
        device (str): Target device ('mps', 'cuda', 'cpu')
    
    Returns:
        model: Model moved to the specified device
    """
    try:
        if device == 'mps':
            model = model.to('mps')
            print("Model moved to MPS device")
        elif device == 'cuda':
            model = model.to('cuda')
            print("Model moved to CUDA device")
        else:
            model = model.to('cpu')
            print("Model moved to CPU device")
        return model
    except Exception as e:
        print(f"Failed to move model to {device}, falling back to CPU: {e}")
        return model.to('cpu')

def get_device_info():
    """
    Get comprehensive device information
    
    Returns:
        dict: Device information
    """
    env_info = detect_environment()
    mps_info = detect_mps_availability()
    cuda_info = detect_cuda_availability()
    optimal_device = get_optimal_device()
    
    device_info = {
        'environment': env_info,
        'mps': mps_info,
        'cuda': cuda_info,
        'optimal_device': optimal_device,
        'recommendations': get_recommendations(env_info, mps_info, cuda_info, optimal_device)
    }
    
    return device_info

def get_recommendations(env_info, mps_info, cuda_info, optimal_device):
    """
    Get performance recommendations based on device configuration
    
    Returns:
        list: List of recommendations
    """
    recommendations = []
    
    if optimal_device == 'mps':
        recommendations.append("Using MPS (Apple Silicon GPU)")
        recommendations.append("Expect 2-5x performance improvement for large operations")
    elif optimal_device == 'cuda':
        recommendations.append("Using CUDA (NVIDIA GPU)")
        recommendations.append("Expect significant performance improvement")
    else:
        recommendations.append("Using CPU (fallback)")
        recommendations.append("Large operations may be slower")
    
    if env_info['is_docker']:
        recommendations.append("Running in Docker - MPS not available in containers")
    
    return recommendations

def main():
    """Main function for device detection"""
    print("Face-Gen Device Detection")
    print("=" * 40)
    
    device_info = get_device_info()
    
    print("Device Detection Results:")
    print("-" * 30)
    print(f"   MPS: {'Available' if device_info['mps']['available'] else 'Not available'}")
    print(f"   CUDA: {'Available' if device_info['cuda']['available'] else 'Not available'}")
    print(f"   Environment: {device_info['environment']['os']} on {device_info['environment']['architecture']}")
    
    if device_info['optimal_device'] == 'mps':
        print("Using MPS (Apple Silicon GPU)")
    elif device_info['optimal_device'] == 'cuda':
        print("Using CUDA (NVIDIA GPU)")
    else:
        print("Using CPU (fallback)")
    
    print("\nSummary:")
    for rec in device_info['recommendations']:
        print(f"   - {rec}")
    
    print(f"\nReady to use device: {device_info['optimal_device']}")
    
    return device_info

if __name__ == "__main__":
    main() 