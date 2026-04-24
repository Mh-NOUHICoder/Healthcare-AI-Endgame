from enum import Enum
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class Specialty(str, Enum):
    PEDIATRICS = "pediatrics"
    CARDIOLOGY = "cardiology"
    DRUG_SAFETY = "drug_safety"
    ONCOLOGY = "oncology"
    NEUROLOGY = "neurology"
    GENERAL_PRACTICE = "general_practice"
    PSYCHIATRY = "psychiatry"

    @classmethod
    def list_all(cls):
        return [s.value for s in cls]

class ClinicalReport(BaseModel):
    summary: str
    assessment: str
    plan: str
    recommendations: List[str] = []
    specialty_specific_data: Dict[str, Any] = {}

class Patient(BaseModel):
    id: str
    age: Optional[int] = None
    gender: Optional[str] = None
    conditions: List[str] = []
    observations: List[str] = []

class MedicalQuery(BaseModel):
    patient_id: str
    query: str
