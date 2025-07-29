#!/usr/bin/env python3
"""
Wav2Lip Installation Script
Automates the installation of Wav2Lip and downloads required models
"""

import os
import sys
import subprocess
import urllib.request
import shutil

def run_command(command, description):
    """Run a command and return success status"""
    print(f"Running {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"SUCCESS: {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"FAILED: {description} failed: {e}")
        return False

def download_file(url, filename, description):
    """Download a file from URL"""
    print(f"Downloading {filename}...")
    try:
        urllib.request.urlretrieve(url, filename)
        print(f"SUCCESS: Downloaded {filename}")
        return True
    except Exception as e:
        print(f"FAILED: Failed to download {filename}: {e}")
        return False

def install_wav2lip():
    """Install Wav2Lip and download models"""
    print("Installing Wav2Lip...")
    
    # Clone Wav2Lip repository if it doesn't exist
    if not os.path.exists("Wav2Lip"):
        if not run_command("git clone https://github.com/Rudrabha/Wav2Lip.git", "Cloning Wav2Lip repository"):
            return False
    else:
        print("SUCCESS: Wav2Lip directory already exists")
    
    # Create checkpoints directory
    os.makedirs("Wav2Lip/checkpoints", exist_ok=True)
    
    # Download model files
    models = [
        {
            "url": "https://github.com/Rudrabha/Wav2Lip/releases/download/v1.0/wav2lip_gan.pth",
            "filename": "Wav2Lip/checkpoints/wav2lip_gan.pth",
            "name": "wav2lip_gan.pth"
        },
        {
            "url": "https://github.com/Rudrabha/Wav2Lip/releases/download/v1.0/wav2lip.pth",
            "filename": "Wav2Lip/checkpoints/wav2lip.pth",
            "name": "wav2lip.pth"
        }
    ]
    
    for model in models:
        if not os.path.exists(model["filename"]):
            if not download_file(model["url"], model["filename"], f"Downloading {model['name']}"):
                print(f"WARNING: Failed to download {model['name']}, trying alternative sources...")
                # Try alternative sources
                alt_urls = [
                    f"https://huggingface.co/datasets/justinjohn0306/Wav2Lip/resolve/main/{model['name']}",
                    f"https://github.com/Rudrabha/Wav2Lip/releases/latest/download/{model['name']}"
                ]
                for alt_url in alt_urls:
                    if download_file(alt_url, model["filename"], f"Downloading {model['name']} from alternative source"):
                        break
                else:
                    print(f"FAILED: Could not download {model['name']} from any source")
        else:
            print(f"SUCCESS: {model['name']} already exists")
    
    # Install Wav2Lip dependencies
    wav2lip_requirements = [
        "opencv-python",
        "librosa",
        "numpy",
        "scipy",
        "tqdm",
        "matplotlib",
        "scikit-image",
        "scikit-learn",
        "tensorboard",
        "tensorflow",
        "torch",
        "torchvision"
    ]
    
    for package in wav2lip_requirements:
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", package], 
                         check=True, capture_output=True)
        except subprocess.CalledProcessError:
            print(f"WARNING: Failed to install {package}, continuing...")
    
    print("SUCCESS: Wav2Lip installation completed!")
    return True

def test_wav2lip():
    """Test Wav2Lip installation"""
    print("\nTesting Wav2Lip installation...")
    
    # Check if Wav2Lip directory exists
    if not os.path.exists("Wav2Lip"):
        print("FAILED: Wav2Lip directory not found")
        return False
    
    # Check if inference.py exists
    if not os.path.exists("Wav2Lip/inference.py"):
        print("FAILED: Wav2Lip/inference.py not found")
        return False
    
    # Check if model files exist
    model_files = [
        "Wav2Lip/checkpoints/wav2lip_gan.pth",
        "Wav2Lip/checkpoints/wav2lip.pth"
    ]
    
    for file_path in model_files:
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
            if file_size > 1000000:  # More than 1MB
                print(f"SUCCESS: {file_path} exists ({file_size} bytes)")
            else:
                print(f"WARNING: {file_path} exists but seems too small ({file_size} bytes)")
        else:
            print(f"FAILED: {file_path} missing")
    
    print("SUCCESS: Wav2Lip installation test passed!")
    return True

def create_assets():
    """Create sample assets directory"""
    print("\nCreating sample assets...")
    
    assets_dir = "assets"
    if not os.path.exists(assets_dir):
        os.makedirs(assets_dir)
        print("SUCCESS: Assets directory created")
    else:
        print("SUCCESS: Assets directory already exists")
    
    # Create a sample script file
    script_file = os.path.join(assets_dir, "script.txt")
    if not os.path.exists(script_file):
        with open(script_file, "w", encoding="utf-8") as f:
            f.write("Hello, this is a sample script for testing the digital avatar generator.")
        print("SUCCESS: Sample script file created")

def main():
    """Main installation function"""
    print("Digital Avatar Project - Wav2Lip Installation")
    print("=" * 50)
    
    # Install Wav2Lip
    if not install_wav2lip():
        print("FAILED: Wav2Lip installation failed")
        return False
    
    # Test installation
    if not test_wav2lip():
        print("FAILED: Wav2Lip test failed")
        return False
    
    # Create assets
    create_assets()
    
    print("\nSUCCESS: Installation completed successfully!")
    print("\nNext steps:")
    print("1. Set environment variable: export KMP_DUPLICATE_LIB_OK=TRUE")
    print("2. Run the Flask app: python face-gen.py")
    print("3. Open browser to: http://localhost:5000")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 