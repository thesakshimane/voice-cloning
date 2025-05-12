import os
import numpy as np
import torch
from TTS.api import TTS
from scipy.io.wavfile import write
from pathlib import Path
import soundfile as sf

# Configuration
USER_ID = "user_1"
EMBEDDING_DIR = "data/embeddings"
OUTPUT_DIR = "outputs"
MODEL_NAME = "tts_models/en/vctk/vits"

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load the precomputed speaker embedding
embedding_file = os.path.join(EMBEDDING_DIR, f"{USER_ID}_embedding.npy")
if not os.path.exists(embedding_file):
    raise FileNotFoundError(f"Embedding file not found: {embedding_file}")

speaker_embedding = np.load(embedding_file)
print(f"🔍 Loaded speaker embedding: {speaker_embedding.shape}")

# Load TTS model
print(f"🎙️  Initializing TTS model: {MODEL_NAME}")
tts = TTS(MODEL_NAME)
print("✅  TTS model initialized.")

# Generate speech
text = "Hello! I am your AI voice."
print(f"📝 Synthesizing text: {text}")
audio = tts.tts(text, speaker_wav=None, speaker_embeddings=torch.tensor(speaker_embedding))

# Save the synthesized audio
output_file = os.path.join(OUTPUT_DIR, f"{USER_ID}_synthesized.wav")
sf.write(output_file, audio, 22050)
print(f"✅  Synthesis complete. Output saved at: {output_file}")
