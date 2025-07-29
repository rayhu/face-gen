import torch
import torchaudio
from tortoise.api import TextToSpeech
import time
import os
from .device_detection import get_optimal_device, configure_device_for_model

def generate_tts(text, output_path="audio/ray_audio.wav"):
    """
    Generate TTS audio from text using Tortoise TTS
    
    Args:
        text (str): Input text to convert to speech
        output_path (str): Output audio file path
    
    Returns:
        bool: True if successful, False otherwise
    """
    # Get optimal device for current environment
    device = get_optimal_device()
    print(f"Using device: {device}")
    print(f"Initializing Tortoise TTS on device: {device}")
    
    try:
        tts = TextToSpeech()
        
        # Configure models for the optimal device
        if device == 'mps':
            try:
                print("Attempting to use MPS acceleration...")
                if hasattr(tts, 'autoregressive'):
                    tts.autoregressive = configure_device_for_model(tts.autoregressive, 'mps')
                if hasattr(tts, 'diffusion'):
                    tts.diffusion = configure_device_for_model(tts.diffusion, 'mps')
                if hasattr(tts, 'vocoder'):
                    tts.vocoder = configure_device_for_model(tts.vocoder, 'mps')
                if hasattr(tts, 'clvp'):
                    tts.clvp = configure_device_for_model(tts.clvp, 'mps')
                print("Models configured for MPS device")
            except Exception as e:
                print(f"MPS configuration failed, falling back to CPU: {str(e)}")
                device = 'cpu'
                print(f"Switching to device: {device}")
        
        elif device == 'cuda':
            try:
                print("Attempting to use CUDA acceleration...")
                if hasattr(tts, 'autoregressive'):
                    tts.autoregressive = configure_device_for_model(tts.autoregressive, 'cuda')
                if hasattr(tts, 'diffusion'):
                    tts.diffusion = configure_device_for_model(tts.diffusion, 'cuda')
                if hasattr(tts, 'vocoder'):
                    tts.vocoder = configure_device_for_model(tts.vocoder, 'cuda')
                if hasattr(tts, 'clvp'):
                    tts.clvp = configure_device_for_model(tts.clvp, 'cuda')
                print("Models configured for CUDA device")
            except Exception as e:
                print(f"CUDA configuration failed, falling back to CPU: {str(e)}")
                device = 'cpu'
                print(f"Switching to device: {device}")
        
        print("Generating speech...")
        start_time = time.time()
        
        gen_audio = tts.tts(text)
        
        end_time = time.time()
        print(f"Generation time: {end_time - start_time:.2f} seconds")
        
        # Move audio data back to CPU and save
        if device in ['mps', 'cuda']:
            gen_audio = gen_audio.cpu()
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        torchaudio.save(output_path, gen_audio.squeeze(0), 24000)
        print("TTS saved to", output_path)
        return True
        
    except Exception as e:
        print(f"TTS generation failed: {str(e)}")
        print("Attempting to regenerate with CPU...")
        
        # Fallback to CPU
        device = 'cpu'
        tts = TextToSpeech()
        
        try:
            gen_audio = tts.tts(text)
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            torchaudio.save(output_path, gen_audio.squeeze(0), 24000)
            print("TTS generated successfully on CPU")
            return True
        except Exception as e2:
            print(f"CPU generation also failed: {str(e2)}")
            return False

if __name__ == "__main__":
    # This part is for standalone testing, not used by Flask app directly
    with open("assets/script.txt", "r", encoding="utf-8") as f:
        text = f.read()
    generate_tts(text)