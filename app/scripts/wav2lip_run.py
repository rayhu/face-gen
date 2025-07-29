import subprocess
import os
import time

def run_wav2lip(face_path, audio_path, output_path):
    """
    Run Wav2Lip to generate talking face video
    
    Args:
        face_path (str): Path to face image
        audio_path (str): Path to audio file
        output_path (str): Output video path
    
    Returns:
        bool: True if successful, False otherwise
    """
    print("Starting Wav2Lip video generation...")
    
    # Check if input files exist
    if not os.path.exists(face_path):
        print(f"Face image not found: {face_path}")
        return False
    
    if not os.path.exists(audio_path):
        print(f"Audio file not found: {audio_path}")
        return False
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Construct Wav2Lip command
    command = [
        "python", "Wav2Lip/inference.py",
        "--face", face_path,
        "--audio", audio_path,
        "--outfile", output_path,
        "--pads", "0", "20", "0", "0"
    ]
    
    try:
        print(f"Running command: {' '.join(command)}")
        start_time = time.time()
        
        # Run Wav2Lip
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        
        end_time = time.time()
        print(f"Wav2Lip generation time: {end_time - start_time:.2f} seconds")
        
        # Check if output file was created
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            print(f"Video generated successfully!")
            print(f"Output file: {output_path}")
            print(f"File size: {file_size} bytes")
            return True
        else:
            print("Output video file not found")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"Wav2Lip failed: {e}")
        print(f"Error output: {e.stderr}")
        return False
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return False

def check_wav2lip_installation():
    """
    Check if Wav2Lip is properly installed
    
    Returns:
        bool: True if Wav2Lip is properly installed, False otherwise
    """
    # Check if Wav2Lip directory exists
    if not os.path.exists("Wav2Lip"):
        print("Wav2Lip directory not found")
        return False
    
    # Check if checkpoint file exists
    checkpoint_path = "Wav2Lip/checkpoints/wav2lip_gan.pth"
    if not os.path.exists(checkpoint_path):
        print("Wav2Lip checkpoint not found")
        return False
    
    print("Wav2Lip installation check passed")
    return True

if __name__ == "__main__":
    # Test Wav2Lip installation
    if not check_wav2lip_installation():
        print("Wav2Lip not properly installed")
        exit(1)
    
    print("Wav2Lip installation verified successfully")