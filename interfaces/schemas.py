from pydantic import BaseModel, Field
from typing import List, Optional, Any, Dict, Union

class CitationModel(BaseModel):
    source: str
    page: int

class RouterRequest(BaseModel):
    patient_id: str
    query: str

class RouterResponse(BaseModel):
    answer: str
    clinical_report: Optional[Dict[str, Any]] = None
    citations: List[CitationModel]
    specialty: str
    error: Optional[str] = None

# A2A Models
class A2AMessagePart(BaseModel):
    type: str = "text"
    text: Optional[str] = None
    content: Optional[str] = None

class A2AMessage(BaseModel):
    parts: Optional[List[A2AMessagePart]] = None
    text: Optional[str] = None

class A2AParams(BaseModel):
    id: Optional[str] = None
    sessionId: Optional[str] = None
    message: Optional[Union[str, A2AMessage]] = None
    input: Optional[Dict[str, Any]] = None  # Added to support common A2A test formats
    fhir_data: Optional[Any] = None

    class Config:
        extra = "allow"

class A2ARequest(BaseModel):
    jsonrpc: str = "2.0"
    method: str
    id: Union[str, int]
    params: Optional[A2AParams] = None

    class Config:
        extra = "allow"
