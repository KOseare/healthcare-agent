from dotenv import load_dotenv

load_dotenv()

from src.agents.health_agent.main import agent

INITIAL_STATE = {
    "customer_name": "",
    "symptoms": [],
    "personal_data": [],
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
    print("\nPersonal data:")
    print(result["personal_data"])


if __name__ == "__main__":
    main()
