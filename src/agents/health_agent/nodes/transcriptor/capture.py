import io
import wave

import numpy as np
import sounddevice as sd

DEFAULT_SAMPLE_RATE = 16000


def record_microphone(duration_seconds: float, sample_rate: int = DEFAULT_SAMPLE_RATE) -> bytes:
    print(f"Recording for {duration_seconds:.0f} seconds... Speak now.")
    frames = int(duration_seconds * sample_rate)
    audio = sd.rec(frames, samplerate=sample_rate, channels=1, dtype="int16")
    sd.wait()
    print("Recording finished.")

    buffer = io.BytesIO()
    with wave.open(buffer, "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(np.asarray(audio, dtype=np.int16).tobytes())

    return buffer.getvalue()
