import sounddevice as sd
import numpy as np

def record_audio(duration=3, fs=16000):
    print("Recording...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float32')
    sd.wait()
    print("Recording done.")
    return np.squeeze(recording), fs

