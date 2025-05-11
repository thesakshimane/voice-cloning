# scripts/capture.py
import pyaudio
import wave
import os
import datetime

def record_audio(user_id="default_user", duration=5, sample_rate=16000, channels=1):
    # Set the base directory to the project root
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(base_dir, "data", "raw", user_id)
    os.makedirs(output_dir, exist_ok=True)

    # Generate a timestamped filename
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{user_id}_recording_{timestamp}.wav"
    output_file = os.path.join(output_dir, filename)

    # PyAudio Settings
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16, channels=channels, rate=sample_rate, input=True, frames_per_buffer=1024)
    
    print(f"🎤 Recording for {duration} seconds...")
    frames = []

    for _ in range(0, int(sample_rate / 1024 * duration)):
        data = stream.read(1024)
        frames.append(data)

    # Stop Recording
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save the recording
    with wave.open(output_file, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(sample_rate)
        wf.writeframes(b''.join(frames))

    print(f"✅ Saved recording as {output_file}")

# Test the function
if __name__ == "__main__":
    record_audio(user_id="user_1", duration=5)
