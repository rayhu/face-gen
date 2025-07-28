import torch
import torchaudio
from tortoise.api import TextToSpeech
import time
import os

def generate_tts(text, output_path="audio/ray_audio.wav"):
    """
    Generate TTS audio from text using Tortoise TTS
    
    Args:
        text (str): Input text to convert to speech
        output_path (str): Output audio file path
    
    Returns:
        bool: True if successful, False otherwise
    """
    # Detect and use MPS device for Apple Silicon optimization
    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    print(f"✅ Using device: {device}")
    print(f"🎤 Initializing Tortoise TTS on device: {device}")
    
    try:
        tts = TextToSpeech()
        
        # Try to move models to MPS device for acceleration
        if device.type == "mps":
            try:
                print("🚀 Attempting to use MPS acceleration...")
                if hasattr(tts, 'autoregressive'):
                    tts.autoregressive = tts.autoregressive.to(device)
                if hasattr(tts, 'diffusion'):
                    tts.diffusion = tts.diffusion.to(device)
                if hasattr(tts, 'vocoder'):
                    tts.vocoder = tts.vocoder.to(device)
                if hasattr(tts, 'clvp'):
                    tts.clvp = tts.clvp.to(device)
                print("✅ Models moved to MPS device")
            except Exception as e:
                print(f"⚠️  MPS move failed, falling back to CPU: {str(e)}")
                device = torch.device("cpu")
                print(f"🔄 Switching to device: {device}")
        
        print("🎵 Generating speech...")
        start_time = time.time()
        
        gen_audio = tts.tts(text)
        
        end_time = time.time()
        print(f"⏱️  Generation time: {end_time - start_time:.2f} seconds")
        
        # Move audio data back to CPU and save
        if device.type == "mps":
            gen_audio = gen_audio.cpu()
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        torchaudio.save(output_path, gen_audio.squeeze(0), 24000)
        print("✅ TTS saved to", output_path)
        return True
        
    except Exception as e:
        print(f"❌ TTS generation failed: {str(e)}")
        print("🔄 Attempting to regenerate with CPU...")
        
        # Fallback to CPU
        device = torch.device("cpu")
        tts = TextToSpeech()
        
        try:
            gen_audio = tts.tts(text)
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            torchaudio.save(output_path, gen_audio.squeeze(0), 24000)
            print("✅ TTS generated successfully on CPU")
            return True
        except Exception as e2:
            print(f"❌ CPU generation also failed: {str(e2)}")
            return False

if __name__ == "__main__":
    with open("assets/script.txt", "r", encoding="utf-8") as f:
        text = f.read()
    generate_tts(text)