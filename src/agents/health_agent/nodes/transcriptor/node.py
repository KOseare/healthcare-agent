from pathlib import Path

from groq import Groq

from src.agents.health_agent.nodes.transcriptor.prompt import TRANSCRIPTION_PROMPT
from src.agents.health_agent.state import State

PROJECT_ROOT = Path(__file__).resolve().parents[5]
AUDIO_FILE_PATH = PROJECT_ROOT / "assets" / "audio" / "sample.m4a"
WHISPER_MODEL = "whisper-large-v3-turbo"


def transcriptor_node(state: State) -> dict:
    client = Groq()
    with open(AUDIO_FILE_PATH, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            file=(AUDIO_FILE_PATH.name, audio_file.read()),
            model=WHISPER_MODEL,
            prompt=TRANSCRIPTION_PROMPT,
        )
    return {"transcript": transcription.text}
