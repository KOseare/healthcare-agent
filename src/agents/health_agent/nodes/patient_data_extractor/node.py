from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq
from pydantic import BaseModel, Field

from src.agents.health_agent.nodes.patient_data_extractor.prompt import SYSTEM_PROMPT
from src.agents.health_agent.state import State

PATIENT_DATA_MODEL = "llama-3.1-8b-instant"


class PersonalDataOutput(BaseModel):
    personal_data: list[str] = Field(
        default_factory=list,
        description="Lista de datos personales clínicamente relevantes extraídos de la transcripción.",
    )


def patient_data_extractor_node(state: State) -> dict:
    transcript = state.get("transcript", "")
    if not transcript:
        raise ValueError("No transcript in state. Run the transcriptor node first.")

    model = ChatGroq(model=PATIENT_DATA_MODEL, temperature=0)
    structured_model = model.with_structured_output(PersonalDataOutput)
    result = structured_model.invoke(
        [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=f"Transcripción:\n{transcript}"),
        ]
    )

    personal_data = (
        result.personal_data
        if isinstance(result, PersonalDataOutput)
        else result["personal_data"]
    )
    return {"personal_data": personal_data}
