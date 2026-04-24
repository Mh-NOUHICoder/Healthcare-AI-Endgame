from typing import TypedDict, List, Optional

class ClinicaState(TypedDict):
    patient_id: str
    query: str
    patient_age: Optional[int]
    symptoms: List[str]
    conditions: List[str]
    target_collection: Optional[str]
    retrieved_docs: List[dict]
    final_answer: Optional[str]
    clinical_report: Optional[dict] = None
    citations: List[dict]
    error: Optional[str]
