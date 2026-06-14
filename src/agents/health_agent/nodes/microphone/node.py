import base64
import os

from src.agents.health_agent.nodes.transcriptor.capture import record_microphone
from src.agents.health_agent.state import State

DEFAULT_RECORD_SECONDS = float(os.getenv("MIC_RECORD_SECONDS", "10"))


def microphone_node(state: State) -> dict:
    wav_bytes = record_microphone(DEFAULT_RECORD_SECONDS)
    return {"audio_base64": base64.b64encode(wav_bytes).decode("ascii")}
