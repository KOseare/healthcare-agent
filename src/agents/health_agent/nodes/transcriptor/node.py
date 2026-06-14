import base64

from groq import Groq

from src.agents.health_agent.nodes.transcriptor.prompt import TRANSCRIPTION_PROMPT
from src.agents.health_agent.state import State

WHISPER_MODEL = "whisper-large-v3-turbo"


def transcriptor_node(state: State) -> dict:
    audio_base64 = state.get("audio_base64", "")
    if not audio_base64:
        raise ValueError("No audio in state. Run the microphone node first.")

    wav_bytes = base64.b64decode(audio_base64)
    client = Groq()
    transcription = client.audio.transcriptions.create(
        file=("recording.wav", wav_bytes),
        model=WHISPER_MODEL,
        prompt=TRANSCRIPTION_PROMPT,
    )
    return {"transcript": transcription.text, "audio_base64": ""}
