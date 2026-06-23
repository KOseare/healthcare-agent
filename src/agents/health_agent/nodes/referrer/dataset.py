import csv
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[5]
STAFF_CSV_PATH = PROJECT_ROOT / "src" / "assets" / "personal_clinica_argentina_mock.csv"

REFERRAL_PROMPT_COLUMNS = (
    "ID_Empleado",
    "Sexo",
    "Edad",
    "Especialidad",
    "Años_Experiencia",
)


def load_staff() -> list[dict[str, str]]:
    with open(STAFF_CSV_PATH, encoding="utf-8-sig", newline="") as csv_file:
        return list(csv.DictReader(csv_file))


def format_staff_for_prompt(staff: list[dict[str, str]]) -> str:
    filtered_staff = [
        {column: member[column] for column in REFERRAL_PROMPT_COLUMNS}
        for member in staff
    ]
    return json.dumps(filtered_staff, ensure_ascii=False, indent=2)


def find_staff_by_id(staff: list[dict[str, str]], employee_id: str) -> dict[str, str] | None:
    for member in staff:
        if member["ID_Empleado"] == str(employee_id):
            return member
    return None


def find_fallback_staff(staff: list[dict[str, str]]) -> dict[str, str]:
    for specialty in ("Médico Clínico", "Enfermero", "Enfermera"):
        for member in staff:
            if member["Especialidad"] == specialty:
                return member
    return staff[0]
