from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq
from pydantic import BaseModel, Field

from src.agents.health_agent.nodes.referrer.dataset import (
    find_fallback_staff,
    find_staff_by_id,
    format_staff_for_prompt,
    load_staff,
)
from src.agents.health_agent.nodes.referrer.prompt import SYSTEM_PROMPT
from src.agents.health_agent.state import State

REFERRER_MODEL = "llama-3.1-8b-instant"


class ReferredProfessionalOutput(BaseModel):
    ID_Empleado: str = Field(
        description="ID_Empleado del profesional elegido, copiado exactamente del dataset."
    )
    motivo_derivacion: str = Field(
        description="Breve explicación en español de por qué se eligió este profesional."
    )


def _normalize_referral(result: ReferredProfessionalOutput, staff: list[dict[str, str]]) -> dict:
    matched = find_staff_by_id(staff, result.ID_Empleado)
    if matched is None:
        matched = find_fallback_staff(staff)
        matched = {
            **matched,
            "motivo_derivacion": (
                "Derivación de respaldo: no se pudo validar la selección del modelo. "
                f"Se asignó {matched['Especialidad']} {matched['Nombre']} {matched['Apellido']}."
            ),
        }
        return matched

    return {
        **matched,
        "motivo_derivacion": result.motivo_derivacion,
    }


def referrer_node(state: State) -> dict:
    symptoms = state.get("symptoms", [])
    personal_data = state.get("personal_data", [])
    staff = load_staff()

    symptoms_text = "\n".join(f"- {symptom}" for symptom in symptoms) or "- Sin síntomas registrados"
    personal_data_text = "\n".join(f"- {item}" for item in personal_data) or "- Sin datos personales registrados"

    model = ChatGroq(model=REFERRER_MODEL, temperature=0)
    structured_model = model.with_structured_output(ReferredProfessionalOutput)
    result = structured_model.invoke(
        [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(
                content=(
                    f"Síntomas del paciente:\n{symptoms_text}\n\n"
                    f"Datos personales del paciente:\n{personal_data_text}\n\n"
                    f"Personal disponible en la clínica (dataset):\n{format_staff_for_prompt(staff)}"
                )
            ),
        ]
    )

    referral = (
        result
        if isinstance(result, ReferredProfessionalOutput)
        else ReferredProfessionalOutput.model_validate(result)
    )
    return {"referred_professional": _normalize_referral(referral, staff)}
