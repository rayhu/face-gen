import os
import subprocess
import time

def run_wav2lip(face_path="assets/face.jpg", audio_path="audio/ray_audio.wav", output_path="video/output.mp4"):
    """
    Run Wav2Lip to generate talking face video
    
    Args:
        face_path (str): Path to the face image
        audio_path (str): Path to the audio file
        output_path (str): Path for the output video
    
    Returns:
        bool: True if successful, False otherwise
    """
    print("🎬 Starting Wav2Lip video generation...")
    
    # Check if input files exist
    if not os.path.exists(face_path):
        print(f"❌ Face image not found: {face_path}")
        return False
    
    if not os.path.exists(audio_path):
        print(f"❌ Audio file not found: {audio_path}")
        return False
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    try:
        # Construct Wav2Lip command
        command = [
            "python", "Wav2Lip/inference.py",
            "--checkpoint_path", "Wav2Lip/checkpoints/wav2lip_gan.pth",
            "--face", face_path,
            "--audio", audio_path,
            "--outfile", output_path
        ]
        
        print(f"🚀 Running command: {' '.join(command)}")
        start_time = time.time()
        
        # Run Wav2Lip
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        
        end_time = time.time()
        print(f"⏱️  Wav2Lip generation time: {end_time - start_time:.2f} seconds")
        
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            print(f"✅ Video generated successfully!")
            print(f"📁 Output file: {output_path}")
            print(f"📊 File size: {file_size} bytes")
            return True
        else:
            print("❌ Output video file not found")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Wav2Lip failed: {e}")
        print(f"Error output: {e.stderr}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return False

def check_wav2lip_installation():
    """
    Check if Wav2Lip is properly installed
    
    Returns:
        bool: True if Wav2Lip is available, False otherwise
    """
    wav2lip_path = "Wav2Lip"
    checkpoint_path = "Wav2Lip/checkpoints/wav2lip_gan.pth"
    
    if not os.path.exists(wav2lip_path):
        print("❌ Wav2Lip directory not found")
        return False
    
    if not os.path.exists(checkpoint_path):
        print("❌ Wav2Lip checkpoint not found")
        return False
    
    print("✅ Wav2Lip installation check passed")
    return True

if __name__ == "__main__":
    if check_wav2lip_installation():
        run_wav2lip()
    else:
        print("❌ Wav2Lip not properly installed")