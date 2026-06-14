from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq
from pydantic import BaseModel, Field

from src.agents.health_agent.nodes.symptom_extractor.prompt import SYSTEM_PROMPT
from src.agents.health_agent.state import State

SYMPTOM_MODEL = "llama-3.1-8b-instant"


class SymptomsOutput(BaseModel):
    symptoms: list[str] = Field(
        default_factory=list,
        description="Lista de síntomas reportados por el paciente extraídos de la transcripción.",
    )


def symptom_extractor_node(state: State) -> dict:
    transcript = state.get("transcript", "")
    if not transcript:
        raise ValueError("No transcript in state. Run the transcriptor node first.")

    model = ChatGroq(model=SYMPTOM_MODEL, temperature=0)
    structured_model = model.with_structured_output(SymptomsOutput)
    result = structured_model.invoke(
        [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=f"Transcripción:\n{transcript}"),
        ]
    )

    symptoms = result.symptoms if isinstance(result, SymptomsOutput) else result["symptoms"]
    return {"symptoms": symptoms}
