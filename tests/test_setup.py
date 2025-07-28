#!/usr/bin/env python3
"""
Setup Test Script
Tests the current installation and identifies missing components
"""

import os
import sys
import torch
import subprocess

def test_environment():
    """Test the conda environment"""
    print("🧪 Testing Environment Setup")
    print("=" * 40)
    
    # Test Python version
    print(f"✅ Python version: {sys.version}")
    
    # Test PyTorch
    try:
        print(f"✅ PyTorch version: {torch.__version__}")
        print(f"✅ MPS available: {torch.backends.mps.is_available()}")
    except Exception as e:
        print(f"❌ PyTorch test failed: {e}")
        return False
    
    return True

def test_tortoise_tts():
    """Test Tortoise TTS installation"""
    print("\n🎤 Testing Tortoise TTS")
    print("-" * 20)
    
    try:
        from tortoise.api import TextToSpeech
        print("✅ Tortoise TTS import successful")
        
        # Test basic functionality
        tts = TextToSpeech()
        print("✅ Tortoise TTS initialization successful")
        return True
    except Exception as e:
        print(f"❌ Tortoise TTS test failed: {e}")
        return False

def test_wav2lip():
    """Test Wav2Lip installation"""
    print("\n🎬 Testing Wav2Lip")
    print("-" * 20)
    
    # Check if Wav2Lip directory exists
    if not os.path.exists("Wav2Lip"):
        print("❌ Wav2Lip directory not found")
        return False
    
    print("✅ Wav2Lip directory exists")
    
    # Check required files
    required_files = [
        "Wav2Lip/inference.py",
        "Wav2Lip/checkpoints/wav2lip_gan.pth"
    ]
    
    for file_path in required_files:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"✅ {file_path} exists ({size} bytes)")
            if size < 1000:  # Very small file
                print(f"⚠️  {file_path} seems too small, may be corrupted")
        else:
            print(f"❌ {file_path} missing")
            return False
    
    return True

def test_flask():
    """Test Flask installation"""
    print("\n🌐 Testing Flask")
    print("-" * 20)
    
    try:
        import flask
        print(f"✅ Flask version: {flask.__version__}")
        return True
    except Exception as e:
        print(f"❌ Flask test failed: {e}")
        return False

def test_directories():
    """Test required directories"""
    print("\n📁 Testing Directories")
    print("-" * 20)
    
    required_dirs = [
        "uploads",
        "audio", 
        "video",
        "assets"
    ]
    
    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            print(f"✅ {dir_path} exists")
        else:
            print(f"📁 Creating {dir_path}")
            os.makedirs(dir_path, exist_ok=True)
            print(f"✅ {dir_path} created")
    
    return True

def test_model_download():
    """Test model download functionality"""
    print("\n📥 Testing Model Download")
    print("-" * 20)
    
    # Try alternative download sources
    model_urls = [
        "https://huggingface.co/datasets/justinjohn0306/Wav2Lip/resolve/main/wav2lip_gan.pth",
        "https://github.com/Rudrabha/Wav2Lip/releases/download/v1.0/wav2lip_gan.pth"
    ]
    
    for url in model_urls:
        print(f"🔄 Trying to download from: {url}")
        try:
            import urllib.request
            urllib.request.urlretrieve(url, "Wav2Lip/checkpoints/wav2lip_gan_test.pth")
            size = os.path.getsize("Wav2Lip/checkpoints/wav2lip_gan_test.pth")
            if size > 1000000:  # More than 1MB
                print(f"✅ Download successful ({size} bytes)")
                # Replace the original file
                os.replace("Wav2Lip/checkpoints/wav2lip_gan_test.pth", "Wav2Lip/checkpoints/wav2lip_gan.pth")
                return True
            else:
                print(f"❌ Downloaded file too small ({size} bytes)")
                os.remove("Wav2Lip/checkpoints/wav2lip_gan_test.pth")
        except Exception as e:
            print(f"❌ Download failed: {e}")
    
    return False

def main():
    """Main test function"""
    print("🚀 Digital Avatar Project - Setup Test")
    print("=" * 50)
    
    tests = [
        ("Environment", test_environment),
        ("Tortoise TTS", test_tortoise_tts),
        ("Wav2Lip", test_wav2lip),
        ("Flask", test_flask),
        ("Directories", test_directories)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n📊 Test Results Summary")
    print("=" * 30)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your setup is ready.")
        print("\n🚀 Next steps:")
        print("1. Set environment variable: export KMP_DUPLICATE_LIB_OK=TRUE")
        print("2. Run the Flask app: python app/main.py")
        print("3. Open browser to: http://localhost:5000")
    else:
        print("⚠️  Some tests failed. Please check the issues above.")
        
        # Try to fix model issues
        if not test_model_download():
            print("\n💡 Model download failed. You may need to manually download the models.")
            print("Check the Wav2Lip repository for alternative download links.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 