# scripts/capture.py (Updated to return file path)
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
    # Ensure format is paInt16 for standard WAV
    stream = audio.open(format=pyaudio.paInt16, channels=channels, rate=sample_rate, input=True, frames_per_buffer=1024)

    print(f"🎤 Recording for {duration} seconds for user '{user_id}'...")
    frames = []

    try:
        for _ in range(0, int(sample_rate / 1024 * duration)):
            data = stream.read(1024)
            frames.append(data)
        print("Recording finished.")
    except KeyboardInterrupt:
        print("\nRecording stopped manually.")
    except Exception as e:
        print(f"❌ Error during recording: {e}")
        # Clean up resources even if recording failed
        stream.stop_stream()
        stream.close()
        audio.terminate()
        return None # Indicate failure

    # Stop Recording
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save the recording
    try:
        with wave.open(output_file, 'wb') as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
            wf.setframerate(sample_rate)
            wf.writeframes(b''.join(frames))
        print(f"✅ Saved recording as {output_file}")
        return output_file # Return the path of the saved file
    except Exception as e:
        print(f"❌ Error saving recording to {output_file}: {e}")
        return None # Indicate failure

# Test the function (optional, can be run directly or imported)
if __name__ == "__main__":
    recorded_file = record_audio(user_id="user_1", duration=5)
    if recorded_file:
        print(f"Recording saved successfully at: {recorded_file}")
    else:
        print("Recording failed.")