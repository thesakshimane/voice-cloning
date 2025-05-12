import os
import numpy as np
import soundfile as sf
from resemblyzer import VoiceEncoder
import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings("ignore")

# Set the paths
USER_ID = "user_1"  # Replace this with the actual user ID as required
DATA_DIR = os.path.join("data", "raw", USER_ID)
OUTPUT_DIR = os.path.join("data", "embeddings", USER_ID)  # Embeddings now saved in data/embeddings/user_id
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Get all recordings
recordings = sorted([f for f in os.listdir(DATA_DIR) if f.endswith(".wav")])
if not recordings:
    print(f"❌ No recordings found for {USER_ID} in {DATA_DIR}. Make sure you have recorded at least one sample.")
    exit(1)

# Initialize Resemblyzer encoder
encoder = VoiceEncoder()
print("✅  Encoder initialized.")

# Loop through all recordings and generate embeddings for each
for recording in recordings:
    wav_file_path = os.path.join(DATA_DIR, recording)
    print(f"🗣️  Using voice sample: {wav_file_path}")

    # Load the audio file
    wav, sr = sf.read(wav_file_path)

    # Generate speaker embedding
    print(f"🔄 Generating embeddings for {USER_ID}...")
    embedding = encoder.embed_utterance(wav)
    print(f"🔍 Embedding Shape: {embedding.shape}")

    # Check if the embedding is 256-dimensional
    if embedding.shape[0] == 256:
        # Save the embeddings as a .npy file (one file per .wav)
        embedding_file = os.path.join(OUTPUT_DIR, f"{USER_ID}_{recording.replace('.wav', '_embedding.npy')}")
        np.save(embedding_file, embedding)
        print(f"✅  Embeddings saved to {embedding_file}")
    else:
        print(f"⚠️  Warning: Expected embedding size of 256, but got {embedding.shape[0]}. Check your model settings.")
