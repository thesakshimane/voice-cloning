# scripts/synthesize.py
import os
import numpy as np
from TTS.api import TTS
import soundfile as sf

def synthesize_speech(text, user_id="user_1", model_name="tts_models/multilingual/multi-dataset/your_tts"):
    # Set the base directory to the project root
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    embedding_dir = os.path.join(base_dir, "data", "embeddings", user_id)

    # Load the latest embedding
    embedding_files = sorted(os.listdir(embedding_dir))
    if not embedding_files:
        print(f"❌ No embeddings found for user '{user_id}'")
        return
    
    latest_embedding_file = os.path.join(embedding_dir, embedding_files[-1])
    speaker_embedding = np.load(latest_embedding_file)

    # Initialize the TTS model
    tts = TTS(model_name)
    
    # Generate the speech
    print(f"🗣️ Synthesizing: '{text}'")
    output_wav = tts.tts(text, speaker_wav=None, speaker_embedding=speaker_embedding)
    
    # Save the output
    output_file = os.path.join(base_dir, "data", f"{user_id}_synthesized.wav")
    sf.write(output_file, output_wav, 22050)
    
    print(f"✅ Saved synthesized speech as {output_file}")

# Test the function
if __name__ == "__main__":
    synthesize_speech("Hello, this is a test of my new voice cloning project!", user_id="user_1")
