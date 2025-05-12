# scripts/capture_embeddings.py (Updated)
import os
import numpy as np
from TTS.api import TTS
import soundfile as sf

def capture_embeddings(user_id="user_1", model_name="tts_models/multilingual/multi-dataset/your_tts_ecapa"):
    # Set the base directory to the project root
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    embeddings_dir = os.path.join(base_dir, "data", "embeddings", user_id)
    os.makedirs(embeddings_dir, exist_ok=True)

    # Record a new audio sample
    input_file = os.path.join(base_dir, "data", f"{user_id}_sample.wav")
    print("🎤 Record your voice sample (press Ctrl+C to stop)...")
    os.system(f"python -m sounddevice {input_file} -d 10")

    # Load the TTS model (ECAPA-TDNN Encoder)
    print(f"🔄 Initializing ECAPA-TDNN Encoder...")
    encoder = TTS(model_name)

    # Generate the speaker embedding
    print(f"🔍 Generating embedding for '{user_id}'...")
    embedding = encoder.embed_utterance(input_file)
    print(f"🔍 Embedding Shape: {embedding.shape}")

    # Save the embedding
    embedding_file = os.path.join(embeddings_dir, f"{user_id}_embedding.npy")
    np.save(embedding_file, embedding)
    print(f"✅ Saved embedding as {embedding_file}")

# Test the function
if __name__ == "__main__":
    capture_embeddings("user_1")
