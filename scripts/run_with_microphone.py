from dotenv import load_dotenv

load_dotenv()

from src.agents.health_agent.main import agent

INITIAL_STATE = {
    "customer_name": "",
    "symptoms": [],
    "diagnosis": "",
    "transcript": "",
    "audio_base64": "",
    "messages": [],
}


def main() -> None:
    result = agent.invoke(INITIAL_STATE)
    print("\nTranscript:")
    print(result["transcript"])
    print("\nSymptoms:")
    print(result["symptoms"])


if __name__ == "__main__":
    main()
