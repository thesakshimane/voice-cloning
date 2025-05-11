# scripts/encode.py
from resemblyzer import VoiceEncoder, preprocess_wav
import numpy as np
import os
import soundfile as sf

def generate_embedding(audio_file, user_id="default_user", model=None):
    # Set the base directory to the project root
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(base_dir, "data", "embeddings", user_id)
    os.makedirs(output_dir, exist_ok=True)

    # Load and preprocess the audio file
    wav = preprocess_wav(audio_file)
    model = model or VoiceEncoder()
    
    # Generate the embedding
    embedding = model.embed_utterance(wav)
    
    # Save the embedding as a .npy file
    embedding_file = os.path.join(output_dir, os.path.splitext(os.path.basename(audio_file))[0] + ".npy")
    np.save(embedding_file, embedding)

    print(f"✅ Saved embedding as {embedding_file}")
    return embedding

if __name__ == "__main__":
    # Use the latest recorded file
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    audio_dir = os.path.join(base_dir, "data", "raw", "user_1")
    latest_file = sorted(os.listdir(audio_dir))[-1]
    audio_path = os.path.join(audio_dir, latest_file)
    
    print(f"Generating embedding for: {audio_path}")
    embedding = generate_embedding(audio_path, user_id="user_1")
    print(f"🔊 Embedding Shape: {embedding.shape}")
    print(f"🔍 Embedding Sample: {embedding[:5]}")
