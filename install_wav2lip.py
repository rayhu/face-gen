#!/usr/bin/env python3
"""
Wav2Lip Installation Script
Automatically installs and configures Wav2Lip for the digital avatar project
"""

import os
import subprocess
import sys
import urllib.request
import zipfile
import shutil

def run_command(command, description):
    """Run a command and display progress"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def download_file(url, filename):
    """Download a file from URL"""
    print(f"📥 Downloading {filename}...")
    try:
        urllib.request.urlretrieve(url, filename)
        print(f"✅ Downloaded {filename}")
        return True
    except Exception as e:
        print(f"❌ Failed to download {filename}: {e}")
        return False

def install_wav2lip():
    """Install Wav2Lip"""
    print("🚀 Installing Wav2Lip...")
    print("=" * 50)
    
    # Check if Wav2Lip already exists
    if os.path.exists("Wav2Lip"):
        print("✅ Wav2Lip directory already exists")
        return True
    
    # Clone Wav2Lip repository
    if not run_command("git clone https://github.com/Rudrabha/Wav2Lip.git", "Cloning Wav2Lip repository"):
        return False
    
    # Download pre-trained models
    models_dir = "Wav2Lip/checkpoints"
    os.makedirs(models_dir, exist_ok=True)
    
    model_urls = {
        "wav2lip_gan.pth": "https://github.com/Rudrabha/Wav2Lip/releases/download/v1.0/wav2lip_gan.pth",
        "wav2lip.pth": "https://github.com/Rudrabha/Wav2Lip/releases/download/v1.0/wav2lip.pth"
    }
    
    for model_name, url in model_urls.items():
        model_path = os.path.join(models_dir, model_name)
        if not os.path.exists(model_path):
            if not download_file(url, model_path):
                return False
        else:
            print(f"✅ {model_name} already exists")
    
    # Install Wav2Lip dependencies
    print("📦 Installing Wav2Lip dependencies...")
    wav2lip_requirements = [
        "numpy",
        "opencv-python",
        "librosa",
        "scipy",
        "tqdm",
        "matplotlib",
        "tensorboard",
        "scikit-image",
        "scikit-learn",
        "basicsr",
        "facexlib",
        "gfpgan",
        "realesrgan"
    ]
    
    for package in wav2lip_requirements:
        if not run_command(f"pip install {package}", f"Installing {package}"):
            print(f"⚠️  Failed to install {package}, continuing...")
    
    print("✅ Wav2Lip installation completed!")
    return True

def test_wav2lip():
    """Test Wav2Lip installation"""
    print("\n🧪 Testing Wav2Lip installation...")
    
    # Check if required files exist
    required_files = [
        "Wav2Lip/inference.py",
        "Wav2Lip/checkpoints/wav2lip_gan.pth",
        "Wav2Lip/checkpoints/wav2lip.pth"
    ]
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path} exists")
        else:
            print(f"❌ {file_path} missing")
            return False
    
    print("✅ Wav2Lip installation test passed!")
    return True

def create_sample_assets():
    """Create sample assets for testing"""
    print("\n📁 Creating sample assets...")
    
    # Create assets directory
    os.makedirs("assets", exist_ok=True)
    
    # Create a sample face image (placeholder)
    sample_face_path = "assets/sample_face.jpg"
    if not os.path.exists(sample_face_path):
        print("📝 Creating sample face image...")
        # This would create a simple placeholder image
        # For now, we'll just create the directory structure
        print("✅ Assets directory created")
    
    return True

def main():
    """Main installation function"""
    print("🎯 Digital Avatar Project - Wav2Lip Installation")
    print("=" * 60)
    
    # Install Wav2Lip
    if not install_wav2lip():
        print("❌ Wav2Lip installation failed")
        return False
    
    # Test installation
    if not test_wav2lip():
        print("❌ Wav2Lip test failed")
        return False
    
    # Create sample assets
    create_sample_assets()
    
    print("\n🎉 Installation completed successfully!")
    print("\n📋 Next steps:")
    print("1. Activate your conda environment: conda activate face-gen")
    print("2. Set environment variable: export KMP_DUPLICATE_LIB_OK=TRUE")
    print("3. Run the Flask app: python app/main.py")
    print("4. Open your browser to: http://localhost:5000")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 